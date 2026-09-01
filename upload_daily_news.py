import os
import sys
import argparse
from insta_uploader import InstaUploader

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

parser = argparse.ArgumentParser(description="인스타그램 및 스레드 자동 업로드 스크립트")
parser.add_argument("--account", "-a", type=int, default=1, help="업로드할 계정 번호 (1: 기본 계정, 2: 두 번째 계정... / 기본값: 1)")
args = parser.parse_args()

print(f"=== 🤖 [아린이의 일일 뉴스 카드뉴스 업로드] (계정 번호: {args.account}) ===")

base_dir = os.path.dirname(__file__)
out_dir = os.path.join(base_dir, "generated_slides", "daily_news")

# 1. 캡션 읽기
caption_file = os.path.join(out_dir, "caption.txt")
with open(caption_file, "r", encoding="utf-8") as f:
    caption = f.read()

# 2. 이미지 찾기
slides = [os.path.join(out_dir, f"carousel_slide_{i}.png") for i in range(1, 6)]

print("\n🖼️ [업로드 대상 이미지]:")
for idx, s in enumerate(slides, start=1):
    print(f"  - [{idx}번 슬라이드]: {s}")
    if not os.path.exists(s):
        print(f"    ❌ 파일 없음: {s}")
        sys.exit(1)

# 3. 인스타그램에 캐러셀 업로드
from dotenv import load_dotenv
load_dotenv()

if args.account == 1:
    account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
    access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    threads_token = os.getenv("THREADS_ACCESS_TOKEN")
else:
    account_id = os.getenv(f"INSTAGRAM_ACCOUNT_ID_{args.account}")
    access_token = os.getenv(f"INSTAGRAM_ACCESS_TOKEN_{args.account}")
    threads_token = os.getenv(f"THREADS_ACCESS_TOKEN_{args.account}")

if not account_id or not access_token:
    print(f"\n❌ [{args.account}번] 계정의 인증 정보(ID/TOKEN)가 .env 파일에 없습니다.")
    sys.exit(1)

uploader = InstaUploader(account_id, access_token, verbose=True)
print(f"\n🚀 [인스타그램 카드뉴스 업로드 요청... (계정 ID: {account_id})]")
res = uploader.upload_carousel(slides, caption)

print("\n✨ [인스타그램 업로드 결과]:", res)

# 4. 스레드(Threads) 업로드 (토큰이 있는 경우에만)
if threads_token:
    from threads_uploader import ThreadsUploader
    print("\n🚀 [스레드(Threads) 업로드 요청...]")
    
    # 스레드 텍스트 읽기
    threads_file = os.path.join(out_dir, "threads.txt")
    threads_text = ""
    if os.path.exists(threads_file):
        with open(threads_file, "r", encoding="utf-8") as f:
            threads_text = f.read()
            
    # 스레드는 카드뉴스 이미지 없이 텍스트 단독으로 업로드
    threads_uploader = ThreadsUploader(access_token=threads_token, verbose=True)
    threads_res = threads_uploader.upload_text(text=threads_text)
    print("\n✨ [스레드 업로드 결과]:", threads_res)
else:
    print("\n⚠️ [스레드 업로드 스킵]: THREADS_ACCESS_TOKEN 환경 변수가 설정되지 않았습니다.")
