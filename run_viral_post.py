import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from insta_uploader import InstaUploader

# 1. 생성된 바이럴 카드뉴스 이미지 경로
IMAGE_PATH = r"C:\Users\k\.gemini\antigravity-ide\brain\4bb3554b-2db8-43ce-be50-87fa3f2227c9\viral_cardnews_productivity_ai_1785893920672.png"

# 2. 조회수/저장률 폭발하는 카드뉴스 캡션 작성
CAPTION = """🚨 [조회수 폭발 이슈] 퇴근을 2시간 앞당기는 AI 생산성 치트키 TOP 3 ⚡

매일 반복되는 업무와 야근으로 지치셨나요? 
2026년 현직 일잘러들이 비밀리에 사용하는 **AI 업무 자동화 꿀팁 3가지**를 공개합니다!

---

💡 **1. 3분 만에 발표 자료 완성하는 'Gamma AI'**
• 텍스트나 주제만 입력하면 깔끔한 템플릿의 PPT와 슬라이드가 3분 만에 자동 생성됩니다.
• PPT 디자인 고민하느라 밤샘 작업하던 시대는 끝!

💡 **2. 10초 만에 이메일/보고서 작성하는 'Claude & ChatGPT'**
• 개요만 던져주면 완벽한 대화체와 비즈니스 톤앤매너로 서류 완성.
• 프롬프트 팁: "직장인 상사에게 보고하는 깔끔한 3줄 요약 양식으로 적어줘"

💡 **3. 반복 업무 1초 만에 없애는 'AI 자동화 프롬프트 템플릿'**
• 엑셀 데이터 정리, 회의록 요약, 정보 검색을 버튼 클릭 한 번으로 처리하세요.

---

📌 **이 포스팅이 도움 되셨다면?**
• 지금 바로 **[저장(Bookmark)]** 해두고 칼퇴할 때 꺼내보세요!
• 야근으로 고생하는 팀원/동료에게 **[공유(Share)]**해 보세요! ✈️

#AI생성 #생산성꿀팁 #카드뉴스 #칼퇴치트키 #업무자동화 #직장인꿀팁 #AI툴추천 #생성형AI #아린에이전트 #인스타그램트렌드 #WorkSmart"""

ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "17841442055997951")
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "IGAAO3WRMmXXFBZAGFDNEg3ckdlcWZArSU04SmJybFBQR0htOERQMmw5dTZAmOXNDYk1WY1pabFBFUnp3VGpKVGxuQmJCaUdrX0MwV2JzOVR5SnRpZAm1kWkxCemJPM2lGMDJWbDZAsVkJtS0hQX2R6RzJpbHd5Q3FKTHJJeFJIWDNzQQZDZD")

if __name__ == "__main__":
    uploader = InstaUploader(ACCOUNT_ID, ACCESS_TOKEN, verbose=False)
    result = uploader.upload_image(IMAGE_PATH, CAPTION)
    print("RESULT:", result)
