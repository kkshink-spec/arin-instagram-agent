import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from reels_maker import ReelsMaker
from insta_uploader import InstaUploader

# 1. 릴스 세로 이미지 및 나레이션 텍스트
IMAGE_PATH = r"C:\Users\k\.gemini\antigravity-ide\brain\4bb3554b-2db8-43ce-be50-87fa3f2227c9\reels_vertical_background_1785896221370.png"
NARRATION_TEXT = "안녕하세요! 인스타그램 릴스 음성 자동 생성 테스트입니다. 한국어 나레이션 오디오와 9대 16 세로 비디오가 완벽하게 합성되어 게시됩니다."

CAPTION = """🎙️ [음성 나레이션 탑재 릴스 포스팅 ⚡]

한국어 TTS 음성 나레이션 트랙과 9:16 세로 비디오가 완벽하게 결합되어 자동 발행된 인스타그램 릴스입니다!

#AI릴스 #릴스음성 #인스타그램릴스 #Reels #AI나레이션 #자동포스팅 #아린에이전트"""

ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "17841442055997951")
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "IGAAO3WRMmXXFBZAGFDNEg3ckdlcWZArSU04SmJybFBQR0htOERQMmw5dTZAmOXNDYk1WY1pabFBFUnp3VGpKVGxuQmJCaUdrX0MwV2JzOVR5SnRpZAm1kWkxCemJPM2lGMDJWbDZAsVkJtS0hQX2R6RzJpbHd5Q3FKTHJJeFJIWDNzQQZDZD")

if __name__ == "__main__":
    print("[Reels Voice Test] 1. 음성 오디오 포함 9:16 MP4 비디오 합성 중...")
    maker = ReelsMaker()
    reels_mp4_path = os.path.join(os.path.dirname(__file__), "generated_reels_with_voice.mp4")
    video_path = maker.create_reels_video(IMAGE_PATH, NARRATION_TEXT, reels_mp4_path)
    
    print("[Reels Voice Test] 2. 음성 릴스 동영상 인스타그램 피드 게시 중...")
    uploader = InstaUploader(ACCOUNT_ID, ACCESS_TOKEN, verbose=True)
    result = uploader.upload_reels(video_path, CAPTION)
    
    print("✨ 음성 포함 릴스 최종 결과:", result)
