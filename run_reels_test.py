import os
import sys
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from reels_maker import ReelsMaker
from insta_uploader import InstaUploader
from image_hoster import LocalMediaHoster

# 1. 릴스 배경 이미지 경로
IMAGE_PATH = r"C:\Users\k\.gemini\antigravity-ide\brain\4bb3554b-2db8-43ce-be50-87fa3f2227c9\reels_vertical_background_1785896221370.png"
NARRATION_TEXT = "안녕하세요! 2026년 인스타그램 릴스를 1초 만에 자동 생성해 주는 AI 아린 에이전트입니다. 오늘도 칼퇴를 꿈꾸는 모든 분들을 응원합니다!"

# 2. 릴스 캡션 및 해시태그
CAPTION = """🎥 [AI 자동 생성 릴스 테스트 ⚡]

Gemini 3.1 TTS 음성 나레이션과 AI 9:16 비디오 엔진으로 100% 자동 생성된 인스타그램 릴스입니다!

💡 릴스 제작 포인트:
• Gemini 3.1 Multi-Speaker 오디오 나레이션 자동 합성
• 9:16 모바일 세로 릴스 규격 비디오 자동 인코딩
• 인스타그램 Graph API v23.0 릴스 피드 자동 발행

#AI릴스 #인스타그램릴스 #Reels #AI음성생성 #GeminiTTS #릴스자동화 #아린에이전트 #Shorts #ReelsInstagram"""

ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "17841442055997951")
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "IGAAO3WRMmXXFBZAGFDNEg3ckdlcWZArSU04SmJybFBQR0htOERQMmw5dTZAmOXNDYk1WY1pabFBFUnp3VGpKVGxuQmJCaUdrX0MwV2JzOVR5SnRpZAm1kWkxCemJPM2lGMDJWbDZAsVkJtS0hQX2R6RzJpbHd5Q3FKTHJJeFJIWDNzQQZDZD")

if __name__ == "__main__":
    print("[Reels Test] 1. 릴스 9:16 비디오 생성 중...")
    maker = ReelsMaker()
    reels_video_path = os.path.join(os.path.dirname(__file__), "generated_reels_test.mp4")
    
    # 릴스 비디오 제작
    video_path = maker.create_reels_video(IMAGE_PATH, NARRATION_TEXT, reels_video_path)
    
    print("[Reels Test] 2. 인스타그램 릴스 피드 자동 게시 중...")
    uploader = InstaUploader(ACCOUNT_ID, ACCESS_TOKEN, verbose=False)
    result = uploader.upload_reels(video_path, CAPTION)
    
    print("✨ 릴스 포스팅 최종 결과:", result)
