import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from insta_uploader import InstaUploader

ACCOUNT_ID = os.getenv('INSTAGRAM_ACCOUNT_ID', '27646020745040681')
ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN', 'IGAAO3WRMmXXFBZAFlkZA0ZA4cGpiOWYyZAlpBOWJEY0wzS1gyWE54N1RiNnlNQlhhdWg5RktFS1k5bGI3M1YwbXh2ZAFJGa2tfQk1ma3RqVTZAYOWRjVDlSd01pZAEdTUC1ldzdOV19tUTBxOVY4UU9zNmFQdDB3')

img_dir = r'C:\Users\k\.gemini\antigravity-ide\brain\c1b2f539-9b5f-4721-9fdf-e485ef3c9f56'
slides = [
    os.path.join(img_dir, 'slide_1_cover.png'),
    os.path.join(img_dir, 'slide_2_content.png'),
    os.path.join(img_dir, 'slide_3_content.png')
]

caption = """🚨 모르면 매달 최소 10만원 샌다! 2026 정부 지원금 & 환급금 손실 방지 꿀팁 TOP 3

📌 2026년 꼭 챙겨야 하는 필수 지원금 정보:
1️⃣ K-패스 & 대중교통 이용금액 최대 53% 환급
2️⃣ 청년/직장인 월세 연 최대 240만원 특별지원
3️⃣ 소멸되는 연차수당 및 세금 환급금 지키기

💡 "이 꿀팁을 지금 바로 [저장(Bookmark)]해 두고 필요할 때 꺼내보세요!"
✈️ "야근으로 고생하는 팀원/동료에게 [공유(Share)]해 보세요!"

#손해방지 #정부지원금 #환급금챙기기 #K패스 #월세지원금 #금융꿀팁 #알뜰생활 #재테크정보 #아린에이전트 #인스타그램카드뉴스"""

if __name__ == "__main__":
    print("🚀 인스타그램 캐러셀 포스팅 업로드 시작...")
    uploader = InstaUploader(ACCOUNT_ID, ACCESS_TOKEN, verbose=True)
    result = uploader.upload_carousel(slides, caption)
    print("✨ 최종 게시 결과:", result)
