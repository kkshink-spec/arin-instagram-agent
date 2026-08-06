import os
import sys
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from insta_uploader import InstaUploader
from image_hoster import LocalMediaHoster

# 1. 9:16 비디오 샘플 다운로드 후 Catbox.moe에 직링크 호스팅
sample_video_path = os.path.join(os.path.dirname(__file__), "sample_916_reels.mp4")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

if not os.path.exists(sample_video_path) or os.path.getsize(sample_video_path) < 50000:
    print("[Reels Test] 9:16 샘플 동영상 다운로드 중...")
    if os.path.exists(sample_video_path):
        os.remove(sample_video_path)
    res = requests.get("https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/person-bicycle-car-detection.mp4", headers=headers, timeout=30)
    with open(sample_video_path, "wb") as f:
        f.write(res.content)
    print(f"[+] 다운로드 완료: {sample_video_path} ({os.path.getsize(sample_video_path)} bytes)")

print("[Reels Test] Catbox.moe에 정적 MP4 직링크 호스팅 중...")
catbox_video_url = LocalMediaHoster.upload_file(sample_video_path, verbose=True)

CAPTION = """🎥 [AI 릴스 자동 발행 성공 테스트 ⚡]

Catbox.moe 정적 9:16 MP4 직링크 기반 Instagram Graph API v23.0 릴스 포스팅입니다!

#AI릴스 #인스타그램릴스 #Reels #ReelsVideo #자동포스팅 #아린에이전트"""

ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "17841442055997951")
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "IGAAO3WRMmXXFBZAGFDNEg3ckdlcWZArSU04SmJybFBQR0htOERQMmw5dTZAmOXNDYk1WY1pabFBFUnp3VGpKVGxuQmJCaUdrX0MwV2JzOVR5SnRpZAm1kWkxCemJPM2lGMDJWbDZAsVkJtS0hQX2R6RzJpbHd5Q3FKTHJJeFJIWDNzQQZDZD")

if __name__ == "__main__":
    uploader = InstaUploader(ACCOUNT_ID, ACCESS_TOKEN, verbose=True)
    result = uploader.upload_reels(catbox_video_url, CAPTION)
    print("✨ 릴스 포스팅 최종 결과:", result)
