import os
import sys
from card_news_generator import CardNewsGenerator
from trend_analyzer import TrendAnalyzer
from insta_uploader import InstaUploader

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("=== [Test] 한글 카드뉴스 자동 합성 및 인스타그램 업로드 검증 ===")

# 1. 'evening_2' (스마트폰 보안 설정) 슬롯 트렌드 데이터 가져오기
slot_data = TrendAnalyzer.get_trend_for_slot("evening_2")
print("주제:", slot_data["topic"])
print("슬라이드 개수:", len(slot_data["slides"]))

# 2. 카드뉴스 이미지 렌더링
base_dir = os.path.dirname(__file__)
out_dir = os.path.join(base_dir, "test_generated_slides")
slides = CardNewsGenerator.generate_carousel_slides(slot_data["slides"], out_dir)

print("\n[+] 생성된 슬라이드 경로 목록:")
for s in slides:
    print("  -", s)

# 3. 인스타그램에 캐러셀 업로드 테스트
account_id = os.getenv("INSTAGRAM_ACCOUNT_ID", "27646020745040681")
access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN", "IGAAO3WRMmXXFBZAFlkZA0ZA4cGpiOWYyZAlpBOWJEY0wzS1gyWE54N1RiNnlNQlhhdWg5RktFS1k5bGI3M1YwbXh2ZAFJGa2tfQk1ma3RqVTZAYOWRjVDlSd01pZAEdTUC1ldzdOV19tUTBxOVY4UU9zNmFQdDB3")

uploader = InstaUploader(account_id, access_token, verbose=True)
print("\n[+] 인스타그램 캐러셀 포스팅 업로드 시도 중...")
res = uploader.upload_carousel(slides, slot_data["caption"])

print("\n✨ 최종 결과:", res)
