import requests
import time
import os
from image_hoster import LocalMediaHoster

class InstaUploader:
    """
    Instagram Graph API v23.0을 사용한 이미지, 릴스(동영상), 캐러셀(다중 이미지) 자동 업로드 클래스
    """
    def __init__(self, account_id: str, access_token: str, verbose: bool = False):
        self.token = access_token
        self.version = "v23.0"
        self.verbose = verbose
        if access_token.startswith("IG"):
            self.base_url = f"https://graph.instagram.com/{self.version}"
            self.acc_id = account_id if account_id else "me"
        else:
            self.base_url = f"https://graph.facebook.com/{self.version}"
            self.acc_id = account_id
            
        # 60일 장기 토큰 무한 연장 (매 포스팅 실행 시 자동으로 만료일을 60일 뒤로 리셋)
        self.refresh_token()

    def refresh_token(self) -> str:
        """
        Instagram Login API 60일 장기 토큰을 하루에 최대 1회만 안전하게 연장(Refresh)하는 메서드
        (메타 보안 감지 방지: 24시간 간격 보호)
        """
        try:
            # 24시간 간격 기록 파일
            last_refresh_file = os.path.join(os.path.dirname(__file__), ".last_token_refresh")
            now_ts = time.time()
            
            if os.path.exists(last_refresh_file):
                try:
                    with open(last_refresh_file, "r") as f:
                        last_ts = float(f.read().strip())
                        # 24시간(86400초) 이내 이미 갱신했으면 메타 요청 스킵 (보안 보호)
                        if now_ts - last_ts < 86400:
                            return self.token
                except Exception:
                    pass

            if self.token.startswith("IG"):
                url = f"https://graph.instagram.com/refresh_access_token"
                params = {
                    "grant_type": "ig_refresh_token",
                    "access_token": self.token
                }
                res = requests.get(url, params=params, timeout=10).json()
                if "access_token" in res:
                    new_token = res["access_token"]
                    self.token = new_token
                    self.log(f"[+] Instagram 토큰 자동 갱신 완료! (새 만료 기간 60일 연장)")
                    
                    # 갱신 타임스탬프 기록
                    with open(last_refresh_file, "w") as f:
                        f.write(str(now_ts))
                    return new_token
        except Exception as e:
            self.log(f"[-] 토큰 갱신 경고: {e}")
        return self.token

    def log(self, msg: str):
        if self.verbose:
            print(msg)

    def _resolve_url(self, media_path_or_url: str) -> str:
        if media_path_or_url.startswith("http://") or media_path_or_url.startswith("https://"):
            return media_path_or_url
        if os.path.exists(media_path_or_url):
            return LocalMediaHoster.upload_file(media_path_or_url, verbose=self.verbose)
        return media_path_or_url

    def wait_for_container_status(self, container_id: str, timeout: int = 120, check_interval: int = 5) -> bool:
        status_url = f"{self.base_url}/{container_id}"
        params = {
            "fields": "status_code,status",
            "access_token": self.token
        }
        
        start_time = time.time()
        self.log(f" 컨테이너({container_id}) 처리 상태 확인 중...")
        
        while time.time() - start_time < timeout:
            res = requests.get(status_url, params=params).json()
            status_code = res.get("status_code")
            
            if status_code == "FINISHED":
                self.log(f"[+] 컨테이너 처리 완료! (status_code: {status_code})")
                return True
            elif status_code in ["ERROR", "EXPIRED"]:
                self.log(f"[-] 컨테이너 처리 에러 발생: {res}")
                return False
            
            self.log(f"   [대기 중...] 현재 상태: {status_code or 'PROCESSING'} ({int(time.time() - start_time)}초 경과)")
            time.sleep(check_interval)
            
        self.log("[-] 컨테이너 처리 시간 초과 (Timeout)")
        return False

    def ask_user_approval(self) -> bool:
        import ctypes
        # 0x4 = Yes/No, 0x20 = Question icon, 0x40000 = Topmost window
        MB_YESNO = 0x4
        MB_ICONQUESTION = 0x20
        MB_TOPMOST = 0x40000
        result = ctypes.windll.user32.MessageBoxW(
            0,
            "아린이가 생성한 게시물을 인스타그램에 발행하시겠습니까?\n(예: 업로드, 아니요: 취소)",
            "인스타그램 자동 업로드 승인",
            MB_YESNO | MB_ICONQUESTION | MB_TOPMOST
        )
        return result == 6  # 6 is IDYES

    def publish_container(self, creation_id: str) -> dict:
        self.log(f"[+] 게시물 최종 발행 요청 중... (Creation ID: {creation_id})")

        publish_url = f"{self.base_url}/{self.acc_id}/media_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": self.token
        }
        
        publish_res = requests.post(publish_url, data=publish_payload).json()
        
        if "error" in publish_res:
            self.log(f"[-] 게시물 발행 실패: {publish_res['error']}")
        else:
            media_id = publish_res.get("id")
            self.log(f" 성공적으로 게시되었습니다! (Media ID: {media_id})")
            
        return publish_res

    def upload_image(self, image_url: str, caption: str = "") -> dict:
        """
        단일 이미지 업로드 (웹 URL 또는 로컬 파일 경로)
        """
        resolved_url = self._resolve_url(image_url)
        self.log(f"[1/3] 이미지 컨테이너 생성 요청 중... (URL: {resolved_url})")
        container_url = f"{self.base_url}/{self.acc_id}/media"
        payload = {
            "image_url": resolved_url,
            "caption": caption,
            "access_token": self.token
        }
        
        res = requests.post(container_url, data=payload).json()
        if "error" in res:
            self.log(f"[-] 컨테이너 생성 실패: {res['error']}")
            return res
            
        creation_id = res.get("id")
        self.log(f"[+] 이미지 컨테이너 생성 완료 (Creation ID: {creation_id})")

        # 2. 상태 대기
        if self.wait_for_container_status(creation_id):
            # 3. 발행
            return self.publish_container(creation_id)
        else:
            return {"error": "미디어 서버 처리 실패"}

    def upload_reels(self, video_url: str, caption: str = "") -> dict:
        """
        릴스(동영상) 업로드 (웹 URL 또는 로컬 파일 경로)
        """
        resolved_url = self._resolve_url(video_url)
        print(f"[1/3] 릴스(동영상) 컨테이너 생성 요청 중... (URL: {resolved_url})")
        container_url = f"{self.base_url}/{self.acc_id}/media"
        payload = {
            "media_type": "REELS",
            "video_url": resolved_url,
            "caption": caption,
            "access_token": self.token
        }
        
        res = requests.post(container_url, data=payload).json()
        if "error" in res:
            print("[-] 릴스 컨테이너 생성 실패:", res["error"])
            return res
            
        creation_id = res.get("id")
        print(f"[+] 릴스 컨테이너 생성 완료 (Creation ID: {creation_id})")

        # 2. 동영상 인코딩 및 처리 대기 (동영상은 시간이 조금 더 소요될 수 있습니다)
        if self.wait_for_container_status(creation_id, timeout=300, check_interval=10):
            # 3. 발행
            return self.publish_container(creation_id)
        else:
            return {"error": "릴스 영상 서버 처리 실패"}

    def upload_carousel(self, image_urls: list, caption: str = "") -> dict:
        """
        캐러셀(다중 이미지) 업로드 (웹 URL 또는 로컬 파일 경로, 최대 10개)
        """
        print(f"[1/3] 캐러셀 미디어 아이템 {len(image_urls)}개 생성 중...")
        children_ids = []
        
        for idx, url in enumerate(image_urls, 1):
            resolved_url = self._resolve_url(url)
            container_url = f"{self.base_url}/{self.acc_id}/media"
            payload = {
                "image_url": resolved_url,
                "is_carousel_item": "true",
                "access_token": self.token
            }
            res = requests.post(container_url, data=payload).json()
            if "error" in res:
                print(f"[-] 캐러셀 슬라이드 {idx} 생성 실패:", res["error"])
                return res
            child_id = res.get("id")
            children_ids.append(child_id)
            print(f"   [+] 슬라이드 {idx}/{len(image_urls)} 완료 (ID: {child_id})")
        
        # 각 미디어 아이템 처리 확인
        print("[2/3] 캐러셀 슬라이드 항목 처리 확인 중...")
        for child_id in children_ids:
            if not self.wait_for_container_status(child_id):
                return {"error": f"슬라이드 아이템({child_id}) 처리 실패"}

        # 부모 캐러셀 컨테이너 생성
        print("[3/3] 부모 캐러셀 컨테이너 생성 및 발행 중...")
        carousel_payload = {
            "media_type": "CAROUSEL",
            "children": ",".join(children_ids),
            "caption": caption,
            "access_token": self.token
        }
        carousel_res = requests.post(f"{self.base_url}/{self.acc_id}/media", data=carousel_payload).json()
        if "error" in carousel_res:
            print("[-] 부모 캐러셀 컨테이너 생성 실패:", carousel_res["error"])
            return carousel_res
            
        carousel_id = carousel_res.get("id")
        if self.wait_for_container_status(carousel_id):
            return self.publish_container(carousel_id)
        else:
            return {"error": "부모 캐러셀 컨테이너 처리 실패"}


if __name__ == "__main__":
    # 사용자의 Account ID 및 Access Token
    ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "17841442055997951")
    ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "IGAAO3WRMmXXFBZAGFDNEg3ckdlcWZArSU04SmJybFBQR0htOERQMmw5dTZAmOXNDYk1WY1pabFBFUnp3VGpKVGxuQmJCaUdrX0MwV2JzOVR5SnRpZAm1kWkxCemJPM2lGMDJWbDZAsVkJtS0hQX2R6RzJpbHd5Q3FKTHJJeFJIWDNzQQZDZD")

    # 테스트 데이터
    TEST_IMAGE_URL = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800&auto=format&fit=crop"
    TEST_CAPTION = "안녕하세요! 아린인스타그램에이전트 업로드 테스트입니다.  #InstagramAPI #AutoPost #v23"

    uploader = InstaUploader(ACCOUNT_ID, ACCESS_TOKEN)
    
    # 1. 단일 이미지 업로드 테스트
    uploader.upload_image(TEST_IMAGE_URL, TEST_CAPTION)

