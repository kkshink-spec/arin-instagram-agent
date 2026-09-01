import os
import sys
from card_news_generator import CardNewsGenerator
from trend_analyzer import TrendAnalyzer
from insta_uploader import InstaUploader

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("=== 🤖 [아린이의 5장 카드뉴스 최종 교정 및 발행 검증] ===")

# 1. 'morning_1' (K-패스 / 금융 지원금) 5장 슬라이드 트렌드 가져오기
slot_data = TrendAnalyzer.get_trend_for_slot("morning_1")
print("📌 주제:", slot_data["topic"])
print("📌 슬라이드 개수:", len(slot_data["slides"]))

# 2. 카드뉴스 이미지 5장 렌더링
base_dir = os.path.dirname(__file__)
out_dir = os.path.join(base_dir, "final_check_slides")
slides = CardNewsGenerator.generate_carousel_slides(slot_data["slides"], out_dir)

print("\n🖼️ [생성된 5장 한글 카드뉴스 이미지 파일 목록]:")
for idx, s in enumerate(slides, start=1):
    print(f"  - [{idx}번 슬라이드]: {s}")

# 3. 인스타그램에 캐러셀 업로드 테스트
account_id = os.getenv("INSTAGRAM_ACCOUNT_ID", "27646020745040681")
access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN", "IGAAO3WRMmXXFBZAFlkZA0ZA4cGpiOWYyZAlpBOWJEY0wzS1gyWE54N1RiNnlNQlhhdWg5RktFS1k5bGI3M1YwbXh2ZAFJGa2tfQk1ma3RqVTZAYOWRjVDlSd01pZAEdTUC1ldzdOV19tUTBxOVY4UU9zNmFQdDB3")

uploader = InstaUploader(account_id, access_token, verbose=True)
print("\n🚀 [인스타그램 5장 캐러셀 최종 업로드 요청...]")
res = uploader.upload_carousel(slides, slot_data["caption"])

print("\n✨ [업로드 결과]:", res)
