import os
import sys

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from card_news_generator import CardNewsGenerator

slides_data = [
    {
        "badge": "1분 손해방지 꿀팁 STEP 01",
        "title": "2026년 새롭게 바뀐 정부지원\n안 받으면 나만 손해!",
        "desc": "올해부터 새롭게 도입된 파격적인 정부 지원 혜택!\n조건이 되는데도 몰라서 신청하지 않으면\n수천만 원의 지원금을 허공에 날리게 됩니다."
    },
    {
        "badge": "1분 손해방지 꿀팁 STEP 02",
        "title": "가장 핫한 '청년미래적금'\n만 19~34세라면 주목!",
        "desc": "월 최대 50만 원을 납입하면,\n정부가 무려 6~12%의 매칭 지원금을\n추가로 얹어주는 역대급 적금이 신설되었습니다."
    },
    {
        "badge": "1분 손해방지 꿀팁 STEP 03",
        "title": "3년 만기 채우면\n최대 2,200만 원 획득!",
        "desc": "매월 성실하게 3년 만기를 채우면\n원금에 정부 지원금과 이자까지 더해져\n최대 2,200만 원이라는 목돈을 쥘 수 있습니다."
    },
    {
        "badge": "1분 손해방지 꿀팁 STEP 04",
        "title": "🚨 정부 지원금 사칭\n신종 스미싱 절대 주의",
        "desc": "'정부 지원금 신청 대상입니다'라는 문자와 함께\nURL 링크가 왔다면 100% 사기입니다.\n정부기관은 절대 문자로 URL을 보내지 않습니다!"
    },
    {
        "badge": "1분 손해방지 CHECKLIST",
        "title": "안전하게 내 돈 지키기\n정부24에서 직접 신청!",
        "desc": "💡 청년미래적금 가입 대상 확인 필수\n💡 정부 지원금 신청은 오직 '정부24'에서만!\n👉 주변에 대상자인 청년, 자녀가 있다면\n이 게시물을 꼭 [공유]해서 알려주세요!"
    }
]

output_dir = os.path.join(os.path.dirname(__file__), "generated_slides", "latest_news")
generated_slides = CardNewsGenerator.generate_carousel_slides(slides_data, output_dir)
print(f"✅ 카드뉴스 생성 완료! 저장 위치: {output_dir}")
for slide in generated_slides:
    print(slide)
