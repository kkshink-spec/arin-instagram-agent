import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from insta_uploader import InstaUploader

# 릴스 전용 9:16 세로 MP4 비디오 샘플 URL (Instagram Reels 공식 규격 9:16)
SAMPLE_VIDEO_URL = "https://assets.mixkit.co/videos/preview/mixkit-vertical-shot-of-a-neon-sign-at-night-42283-large.mp4"

CAPTION = """🎥 [AI 릴스 자동 발행 테스트 ⚡]

Instagram Graph API v23.0을 기반으로 자동 게시된 릴스(Reels) 동영상 포스팅입니다!

#AI릴스 #인스타그램릴스 #Reels #ReelsVideo #자동포스팅 #아린에이전트"""

ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "17841442055997951")
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "IGAAO3WRMmXXFBZAGFDNEg3ckdlcWZArSU04SmJybFBQR0htOERQMmw5dTZAmOXNDYk1WY1pabFBFUnp3VGpKVGxuQmJCaUdrX0MwV2JzOVR5SnRpZAm1kWkxCemJPM2lGMDJWbDZAsVkJtS0hQX2R6RzJpbHd5Q3FKTHJJeFJIWDNzQQZDZD")

if __name__ == "__main__":
    uploader = InstaUploader(ACCOUNT_ID, ACCESS_TOKEN, verbose=True)
    result = uploader.upload_reels(SAMPLE_VIDEO_URL, CAPTION)
    print("✨ 릴스 포스팅 최종 성공 결과:", result)
