import os
import sys

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from card_news_generator import CardNewsGenerator

slides_data = [
    {
        "badge": "1분 손해방지 꿀팁 STEP 01",
        "title": "약정 끝난 인터넷\n그냥 쓰면 매달 손해?",
        "desc": "약정이 끝났는데도 그대로 방치하고 계신가요?\n나도 모르게 새어나가는 통신비와 못 받은 혜택,\n지금 당장 점검하지 않으면 호구 당합니다!"
    },
    {
        "badge": "1분 손해방지 꿀팁 STEP 02",
        "title": "안 쓰는 비싼 요금제\n1:1 상담으로 군살 빼기",
        "desc": "가족들의 실제 사용량에 맞지 않는\n비싼 요금제를 억지로 쓸 필요 없습니다.\n'인터넷원스톱센터'에서 무료로 거품을 빼드립니다."
    },
    {
        "badge": "1분 손해방지 꿀팁 STEP 03",
        "title": "복잡한 결합 할인\n놓치면 나만 억울함!",
        "desc": "스마트폰 결합, 가족 결합 등 숨어있는\n할인 조건들을 완벽하게 분석해 드립니다.\n몰라서 못 받은 할인액, 전부 찾아가세요."
    },
    {
        "badge": "1분 손해방지 꿀팁 STEP 04",
        "title": "우리집 & 우리 매장\n호갱 없는 맞춤형 구성",
        "desc": "일반 가정집부터 카페, 음식점 결제 회선까지!\n현장 상황과 동선에 맞춰 불필요한 장비 없이\n딱 필요한 최적의 환경만 정직하게 세팅합니다."
    },
    {
        "badge": "1분 손해방지 CHECKLIST",
        "title": "더 이상 손해 보지 마세요!\n실시간 견적 비교하기",
        "desc": "💡 나에게 맞는 속도와 약정 조건 무료 진단\n💡 숨은 결합 할인 찾고 통신비 다이어트\n👉 지금 바로 프로필 링크를 클릭해서\n무료 설치 상담과 실시간 견적을 확인하세요!"
    }
]

output_dir = os.path.join(os.path.dirname(__file__), "generated_slides", "isp_comparison")
generated_slides = CardNewsGenerator.generate_carousel_slides(slides_data, output_dir)
print(f"✅ 카드뉴스 생성 완료! 저장 위치: {output_dir}")
for slide in generated_slides:
    print(slide)
