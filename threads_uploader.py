import requests
import time
import os
from image_hoster import LocalMediaHoster

class ThreadsUploader:
    """
    Threads Graph API v1.0을 사용한 이미지 자동 업로드 클래스
    """
    def __init__(self, access_token: str, account_id: str = "me", verbose: bool = False):
        self.token = access_token
        self.version = "v1.0"
        self.verbose = verbose
        self.base_url = f"https://graph.threads.net/{self.version}"
        self.acc_id = account_id

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
            "fields": "status,error_message",
            "access_token": self.token
        }
        
        start_time = time.time()
        self.log(f"⏳ 스레드 컨테이너({container_id}) 처리 상태 확인 중...")
        
        while time.time() - start_time < timeout:
            res = requests.get(status_url, params=params).json()
            status = res.get("status")
            
            if status == "FINISHED":
                self.log(f"[+] 스레드 컨테이너 처리 완료! (status: {status})")
                return True
            elif status in ["ERROR", "EXPIRED"]:
                self.log(f"[-] 스레드 컨테이너 처리 에러 발생: {res}")
                return False
            
            self.log(f"   [대기 중...] 현재 상태: {status or 'PROCESSING'} ({int(time.time() - start_time)}초 경과)")
            time.sleep(check_interval)
            
        self.log("[-] 스레드 컨테이너 처리 시간 초과 (Timeout)")
        return False

    def publish_container(self, creation_id: str) -> dict:
        self.log(f"[+] 스레드 게시물 최종 발행 요청 중... (Creation ID: {creation_id})")
        publish_url = f"{self.base_url}/{self.acc_id}/threads_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": self.token
        }
        
        publish_res = requests.post(publish_url, data=publish_payload).json()
        
        if "error" in publish_res:
            self.log(f"[-] 스레드 게시물 발행 실패: {publish_res['error']}")
        else:
            media_id = publish_res.get("id")
            self.log(f"🎉 성공적으로 스레드에 게시되었습니다! (Media ID: {media_id})")
            
        return publish_res

    def upload_text(self, text: str) -> dict:
        """
        텍스트 단독 스레드 업로드
        """
        self.log(f"[1/3] 스레드 텍스트 컨테이너 생성 요청 중...")
        container_url = f"{self.base_url}/{self.acc_id}/threads"
        payload = {
            "media_type": "TEXT",
            "text": text,
            "access_token": self.token
        }
        
        res = requests.post(container_url, data=payload).json()
        if "error" in res:
            self.log(f"[-] 스레드 텍스트 컨테이너 생성 실패: {res['error']}")
            return res
            
        creation_id = res.get("id")
        self.log(f"[+] 스레드 텍스트 컨테이너 생성 완료 (Creation ID: {creation_id})")

        if self.wait_for_container_status(creation_id):
            return self.publish_container(creation_id)
        else:
            return {"error": "스레드 미디어 서버 처리 실패"}

    def upload_image(self, image_url: str, text: str = "") -> dict:
        """
        단일 이미지 스레드 업로드
        """
        resolved_url = self._resolve_url(image_url)
        self.log(f"[1/3] 스레드 이미지 컨테이너 생성 요청 중... (URL: {resolved_url})")
        container_url = f"{self.base_url}/{self.acc_id}/threads"
        payload = {
            "media_type": "IMAGE",
            "image_url": resolved_url,
            "text": text,
            "access_token": self.token
        }
        
        res = requests.post(container_url, data=payload).json()
        if "error" in res:
            self.log(f"[-] 스레드 컨테이너 생성 실패: {res['error']}")
            return res
            
        creation_id = res.get("id")
        self.log(f"[+] 스레드 이미지 컨테이너 생성 완료 (Creation ID: {creation_id})")

        if self.wait_for_container_status(creation_id):
            return self.publish_container(creation_id)
        else:
            return {"error": "스레드 미디어 서버 처리 실패"}
