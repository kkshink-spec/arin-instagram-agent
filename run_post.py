import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from insta_uploader import InstaUploader

# 1. 생성된 이미지 경로
IMAGE_PATH = r"C:\Users\k\.gemini\antigravity-ide\brain\4bb3554b-2db8-43ce-be50-87fa3f2227c9\ai_image_prompt_tutorial_1785891845884.png"

# 2. 인스타그램 캡션 및 해시태그 작성
CAPTION = """✨ [AI 이미지 생성 핵심 프롬프트 가이드 🎨]

인공지능으로 내가 원하는 완벽한 이미지를 만드는 4가지 필수 법칙!

1️⃣ 주제 (Subject): 정확하게 나타낼 대상을 명시하세요.
👉 예시: "A creative digital creator"

2️⃣ 배경 및 분위기 (Environment): 어떤 장소와 분위기인지 묘사합니다.
👉 예시: "sleek futuristic studio with glowing holograms"

3️⃣ 화풍 및 스타일 (Style): 원하는 아트 스타일을 적어주세요.
👉 예시: "Cinematic digital art, 8k resolution"

4️⃣ 조명 및 색감 (Lighting): 조명 효과로 완성도를 끌어올립니다.
👉 예시: "Neon purple and cyan cinematic lighting"

💡 오늘의 추천 프롬프트:
"A creative digital creator sitting in a sleek futuristic studio surrounded by glowing holographic AI art prompts, cinematic lighting, 8k resolution"

인공지능 이미지 생성으로 나만의 멋진 창작물을 만들어보세요! 🚀

#AI아트 #AI이미지생성 #프롬프트엔지니어링 #AI교육 #인공지능그림 #디지털아트 #AI디자인 #생성형AI #아린에이전트 #ArtificialIntelligence #PromptEngineering"""

# 3. 업로더 객체 생성 및 포스팅
ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "27646020745040681")
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "IGAAO3WRMmXXFBZAFlkZA0ZA4cGpiOWYyZAlpBOWJEY0wzS1gyWE54N1RiNnlNQlhhdWg5RktFS1k5bGI3M1YwbXh2ZAFJGa2tfQk1ma3RqVTZAYOWRjVDlSd01pZAEdTUC1ldzdOV19tUTBxOVY4UU9zNmFQdDB3")

if __name__ == "__main__":
    uploader = InstaUploader(ACCOUNT_ID, ACCESS_TOKEN, verbose=False)
    result = uploader.upload_image(IMAGE_PATH, CAPTION)
    print("✨ 최종 업로드 성공 결과:", result)
