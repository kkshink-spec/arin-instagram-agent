import os
import sys
from dotenv import load_dotenv

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from card_news_generator import CardNewsGenerator
from insta_uploader import InstaUploader

load_dotenv()

slides_data = [
    {
        "badge": "오늘의 명언",
        "title": "성공의 비밀은\n어디에 있을까?",
        "desc": "매일 똑같은 하루를 보내면서\n다른 내일을 기대하는 것은 미친 짓이다.\n- 알베르 아인슈타인"
    },
    {
        "badge": "실행력의 중요성",
        "title": "시작이 반이다",
        "desc": "완벽한 타이밍이란 존재하지 않는다.\n가장 좋은 타이밍은 바로 지금, \n내가 시작하기로 마음먹은 순간이다."
    },
    {
        "badge": "포기하지 마세요",
        "title": "실패는 성공의 어머니",
        "desc": "나는 한 번도 실패한 적이 없다.\n단지 작동하지 않는 10,000가지 방법을\n발견했을 뿐이다.\n- 토마스 에디슨"
    },
    {
        "badge": "1분 손해방지 꿀팁",
        "title": "오늘 하루도\n파이팅입니다!",
        "desc": "당신의 도전을 응원합니다!\n유익하셨다면 [좋아요]와 [저장]을 꾹 눌러주세요!"
    }
]

def main():
    print("1. 카드뉴스 슬라이드 생성 중...")
    output_dir = os.path.join(os.path.dirname(__file__), "generated_slides", "quote_test")
    generated_slides = CardNewsGenerator.generate_carousel_slides(slides_data, output_dir)
    print(f"✅ 카드뉴스 생성 완료! 총 {len(generated_slides)}장")
    
    account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
    access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    
    if not account_id or not access_token:
        print("❌ INSTAGRAM_ACCOUNT_ID 또는 INSTAGRAM_ACCESS_TOKEN이 .env에 없습니다.")
        return
        
    print("\n2. 인스타그램 자동 업로드 시작...")
    uploader = InstaUploader(account_id=account_id, access_token=access_token, verbose=True)
    
    caption = "오늘의 명언으로 동기부여 팍팍 받아가세요! 💪\n\n여러분의 오늘 하루를 진심으로 응원합니다.\n\n#동기부여 #명언 #성공 #마인드셋 #자기계발 #아린스마트랩"
    
    result = uploader.upload_carousel(generated_slides, caption=caption)
    
    if "error" in result:
        print(f"\n❌ 업로드 실패: {result['error']}")
    else:
        print(f"\n✅ 업로드 대성공! 🚀 (Media ID: {result.get('id')})")

if __name__ == "__main__":
    main()
