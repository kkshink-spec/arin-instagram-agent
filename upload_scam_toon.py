import os
from dotenv import load_dotenv
from insta_uploader import InstaUploader

# 환경 변수 로드 (.env 파일에서 INSTAGRAM_ACCOUNT_ID, INSTAGRAM_ACCESS_TOKEN 읽기)
load_dotenv()

# 업로더 인스턴스 생성
account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
uploader = InstaUploader(account_id, access_token, verbose=True)

# 1분 손해방지 꿀팁 - 중고거래 사기 방지 (테스트 이미지 3컷)
brain_dir = r"C:\Users\k\.gemini\antigravity-ide\brain\950000cb-fee0-4e02-ad95-898cb21d5939"
carousel_images = [
    os.path.join(brain_dir, "test_panel_3_handwriting.jpg"), # 썸네일
    os.path.join(brain_dir, "test_panel_1_handwriting.jpg"), # 1컷
    os.path.join(brain_dir, "test_panel_2_handwriting.jpg"), # 2컷
]

caption = """
🥕당근에서 아이패드 샀는데 '진짜 벽돌' 배송 온 썰 ㅋㅋㅋ (웃을 일이 아님)

"에이~ 난 안 당해!" 하시는 분들? 사기꾼들이 제일 좋아하는 마인드입니다. 🦊💢

요즘 중고거래 사기꾼들 폼 미쳤습니다. 
진짜 똑같이 생긴 '가짜 안전결제' 사이트 링크를 띡! 보내주는데, 
무심코 로그인하고 입금하는 순간? 내 통장 잔고는 공중분해 💸 안녕히 계세요 여러분~ 

🦊 얍쌉이의 뼈 때리는 꿀팁 한 줄 요약:
🚨 "판매자가 카톡으로 넘어오자고 하거나, 외부 링크를 주면서 결제하라고 한다? = 10000% 사기" 🚨

결제는 무조건 중고거래 앱 안에서만 하세요!! (앱 밖으로 나가는 순간 호구 잡히는 겁니다 🥲)

✨ 내 소중한 50만 원 지키는 방법 ✨
👉 지금 바로 우측 하단 [저장] 버튼 누르고,
👉 중고거래 자주 하는 호구(..아니 친구)에게 이 게시물을 [공유]해서 정신 차리게 해주세요!

.
.
#1분손해방지꿀팁 #얍쌉이툰 #중고거래 #당근마켓사기 #중고나라사기 #번개장터 #피싱사기 #안전거래사기 #앱테크 #짠테크 #재테크그램 #돈모으기 #금융치료 #자취생꿀팁 #사기조심
"""

print("인스타그램 캐러셀 업로드를 시작합니다...")
# 주석 해제 시 실제 인스타그램에 업로드 됩니다!
# response = uploader.upload_carousel(carousel_images, caption)
# print("업로드 결과:", response)
print("업로드 스크립트 세팅 완료! 실제 업로드를 원하시면 스크립트 안의 주석을 해제해 주세요.")
