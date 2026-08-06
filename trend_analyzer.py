import random
from gemini_content_engine import GeminiContentEngine

class TrendAnalyzer:
    """
    인스타그램 알고리즘 및 트렌드 분석을 기반으로 하루 4개 슬롯별 맞춤 바이럴 주제 및 캡션을 생성하는 클래스
    """
    
    TOPICS_BY_SLOT = {
        "morning_1": [
            {
                "topic": "모르면 매달 10만원 손해 보는 알뜰 교통 & 금융 지원금 꿀팁",
                "prompt": "A modern 3D glassmorphism illustration showing a glowing shield protecting money, credit card, and piggy bank, vibrant neon magenta and gold accents, 8k dark aesthetic",
                "hook": "🚨 모르면 매달 최소 10만원 샌다! 2026 정부 지원금 & 환급금 손실 방지 꿀팁",
                "tags": "#1분손해방지꿀팁 #손해방지 #지원금환급 #금융꿀팁 #알뜰생활 #재테크정보 #아린에이전트"
            }
        ],
        "morning_2": [
            {
                "topic": "안 쓰는 자동결제 구독 안 꺼서 나가는 돈 막는 방법",
                "prompt": "A modern futuristic 3D smartphone screen displaying subscription cancellation alerts, glowing red stop sign icon, high-tech dark theme, 8k render",
                "hook": "⚠️ 매달 자동으로 내 통장에서 새어나가는 구독료 100% 차단하는 법",
                "tags": "#1분손해방지꿀팁 #구독료절약 #자동결제해지 #지출절감 #생활지혜 #돈아끼는법"
            }
        ],
        "lunch_1": [
            {
                "topic": "모르고 서명하면 큰일 나는 연봉 계약서 독소 조항 3가지",
                "prompt": "An executive desk with a glowing contract document under a 3D magnifying glass, warning icon hovering in neon amber light, professional dark style, 8k",
                "hook": "🛑 직장인 90%가 모르고 서명해서 손해 보는 근로/연봉계약서 독소 조항",
                "tags": "#1분손해방지꿀팁 #연봉계약서 #직장인손해방지 #근로기준법 #월급루팡 #노무꿀팁"
            }
        ],
        "evening_1": [
            {
                "topic": "연말정산 13월의 폭탄 피하고 환급금 수십만원 더 받는 방법",
                "prompt": "A glowing golden calculator on a dark glass table surrounded by tax deduction receipts, glowing green dollar arrows pointing up, 8k render",
                "hook": "💸 모르면 세금 폭탄 맞는다! 연말정산 환급금 손실 차단 체크리스트",
                "tags": "#1분손해방지꿀팁 #연말정산 #세금절약 #환급금챙기기 #13월의월급 #세금폭탄피하기"
            }
        ],
        "evening_2": [
            {
                "topic": "스마트폰 개인정보 유출돼 스팸/스미싱 손해 막는 필수 설정",
                "prompt": "A 3D smartphone wrapped in a glowing cyber security shield, neon blue and violet laser beams, dark cyber aesthetic, 8k",
                "hook": "🛡️ 해커에게 내 명의 뚫려서 재산 손해 보지 않는 스마트폰 보안 설정",
                "tags": "#1분손해방지꿀팁 #스마트폰보안 #스미싱예방 #개인정보보호 #해킹방지 #보안꿀팁"
            }
        ]
    }

    @classmethod
    def get_trend_for_slot(cls, slot_id: str) -> dict:
        candidates = cls.TOPICS_BY_SLOT.get(slot_id, cls.TOPICS_BY_SLOT["morning_1"])
        selected = random.choice(candidates)
        
        # Gemini API 키가 있는 경우 Gemini가 캡션 및 프롬프트 생성
        engine = GeminiContentEngine()
        if engine.client:
            gemini_result = engine.generate_caption_and_prompt(selected["topic"])
            if gemini_result:
                return {
                    "topic": selected["topic"],
                    "prompt": gemini_result["prompt"],
                    "caption": gemini_result["caption"]
                }

        caption = f"""{selected['hook']}

📌 2026년 인스타그램 알고리즘에서 성과를 내는 핵심 법칙:
1️⃣ 시각적 몰입감을 주는 3D & 고화질 미디어
2️⃣ 1초 만에 시선을 사로잡는 강력한 훅(Hook) 문구
3️⃣ 시청자의 문제를 바로 해결해 주는 실질적 가치
4️⃣ 나중에 다시 볼 수 있도록 유도하는 저장/공유 CTA

💡 "이 꿀팁을 지금 바로 [저장(Bookmark)]해 두고 필요할 때 꺼내보세요!"
✈️ "야근으로 고생하는 팀원/동료에게 [공유(Share)]해 보세요!"

{selected['tags']}"""

        return {
            "topic": selected["topic"],
            "prompt": selected["prompt"],
            "caption": caption
        }

if __name__ == "__main__":
    ta = TrendAnalyzer()
    print("오전 1차 트렌드 샘플:", ta.get_trend_for_slot("morning_1")["topic"])
