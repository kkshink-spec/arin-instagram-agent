import requests
import os

class LocalMediaHoster:
    """
    로컬 이미지/영상 파일을 Instagram Graph API가 가져갈 수 있는 공개 URL(Direct Public Link)로 변환하는 클래스
    """
    @staticmethod
    def upload_file(file_path: str, verbose: bool = False) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
            
        target_path = file_path
        
        # 인스타그램 API 전용: PNG/WEBP 등 미디어를 JPEG(.jpg)로 자동 변환
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.png', '.webp', '.bmp', '.tiff']:
            jpg_path = os.path.splitext(file_path)[0] + "_converted.jpg"
            converted = False
            try:
                from PIL import Image
                with Image.open(file_path) as img:
                    rgb_img = img.convert('RGB')
                    rgb_img.save(jpg_path, 'JPEG', quality=95)
                target_path = jpg_path
                converted = True
                if verbose:
                    print(f"[JPG Conversion] PIL converted {ext} to JPEG: {target_path}")
            except Exception:
                pass
                
            if not converted:
                try:
                    import subprocess
                    ps_cmd = f"Add-Type -AssemblyName System.Drawing; [System.Drawing.Image]::FromFile('{file_path}').Save('{jpg_path}', [System.Drawing.Imaging.ImageFormat]::Jpeg)"
                    subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)
                    if os.path.exists(jpg_path):
                        target_path = jpg_path
                        if verbose:
                            print(f"[JPG Conversion] PowerShell converted {ext} to JPEG: {target_path}")
                except Exception as ps_err:
                    if verbose:
                        print(f"[JPG Conversion Warning] Could not convert to JPEG: {ps_err}")

        if verbose:
            print(f"[Hosting] Local media file uploading to public server... ({os.path.basename(target_path)})")
        
        # 1차 시도: Catbox.moe (인스타그램 API 전용 100% 정적 직링크 제공)
        try:
            url = "https://catbox.moe/user/api.php"
            data = {"reqtype": "fileupload"}
            with open(target_path, "rb") as f:
                files = {"fileToUpload": f}
                res = requests.post(url, data=data, files=files, timeout=15)
                if res.status_code == 200 and res.text.startswith("https://files.catbox.moe/"):
                    direct_url = res.text.strip()
                    if verbose:
                        print(f"[+] Public Direct URL created (Catbox): {direct_url}")
                    return direct_url
        except Exception as cat_err:
            if verbose:
                print(f"[Hosting Warning] Catbox upload failed, trying tmpfiles: {cat_err}")

        # 2차 시도 (Fallback): tmpfiles.org
        upload_url = "https://tmpfiles.org/api/v1/upload"
        with open(target_path, "rb") as f:
            files = {"file": f}
            response = requests.post(upload_url, files=files).json()
            
        if response.get("status") == "success":
            raw_url = response["data"]["url"]
            direct_url = raw_url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
            if verbose:
                print(f"[+] Public Direct URL created (tmpfiles): {direct_url}")
            return direct_url
        else:
            raise Exception(f"로컬 파일 호스팅 업로드 실패: {response}")

if __name__ == "__main__":
    # 테스트용
    pass
