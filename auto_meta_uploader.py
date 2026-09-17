import os
import base64
from dotenv import load_dotenv
from openai import OpenAI
from insta_uploader import InstaUploader

# .env 로드 및 API 키 준비
load_dotenv()
meta_api_key = os.getenv("META_API_KEY")
account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")

if not all([meta_api_key, account_id, access_token]):
    print(" 환경 변수(META_API_KEY, INSTAGRAM_ACCOUNT_ID, INSTAGRAM_ACCESS_TOKEN)를 확인하세요.")
    exit(1)

def generate_and_upload(prompt, caption):
    print(" 1. 메타 AI 이미지 생성 요청 중...")
    client = OpenAI(
        base_url="https://api.meta.ai/v1",
        api_key=meta_api_key,
    )

    try:
        response = client.images.generate(
            model="muse-image-1.0",
            prompt=prompt,
            n=1,
            # Meta API returns base64 string instead of a URL in some configurations
            response_format="b64_json" 
        )
    except Exception as e:
        print(f" 이미지 생성 실패: {e}")
        return

    # Base64 이미지 데이터를 디코딩하여 로컬에 저장
    print(" 2. 이미지 다운로드 및 저장 중...")
    image_data = None
    if hasattr(response.data[0], 'b64_json') and response.data[0].b64_json:
        image_data = base64.b64decode(response.data[0].b64_json)
    elif hasattr(response.data[0], 'url') and response.data[0].url:
        import requests
        res = requests.get(response.data[0].url)
        image_data = res.content

    if not image_data:
        print(" 이미지 데이터를 받아오지 못했습니다.")
        return

    image_path = "meta_generated_image.jpg"
    with open(image_path, "wb") as f:
        f.write(image_data)
    
    print(f"[SUCCESS] 이미지 저장 완료: {image_path}")
    
    # 윈도우 환경에서 생성된 이미지 자동 열기 및 업로드 승인 단계 생략 (바로 업로드 진행)
    
    # 인스타그램 업로드
    print("3. 인스타그램 업로드 시작...")
    uploader = InstaUploader(account_id, access_token, verbose=True)
    
    upload_response = uploader.upload_image(image_path, caption)
    
    if "error" not in upload_response:
        print("\n[SUCCESS] 인스타그램 업로드 성공! (프로필에서 확인해보세요)")
    else:
        print(f"\n[ERROR] 업로드 실패: {upload_response}")


if __name__ == "__main__":
    print("=== 원스톱 카드뉴스 자동 업로더 ===")
    
    # 예시 프롬프트와 캡션
    default_prompt = "A cute watercolor painting of a red fox holding a small parcel box, simple background"
    default_caption = " 메타 AI로 그린 첫 번째 이미지입니다! 너무 귀엽지 않나요? \n\n#1분손해방지꿀팁 #수채화 #일러스트 #AI그림"
    
    # 원한다면 input()을 이용해 실행 시 직접 입력받을 수도 있습니다.
    # user_prompt = input("프롬프트(영어 추천): ") or default_prompt
    # user_caption = input("캡션(본문): ") or default_caption
    
    # 주의: 주석을 풀고 실행하면 바로 실제 인스타그램 계정에 업로드됩니다.
    generate_and_upload(default_prompt, default_caption)
    
    print(" 스크립트 세팅이 완료되었습니다. `auto_meta_uploader.py` 파일을 열어서")
    print("하단의 주석을 해제하시면 즉시 테스트 업로드가 가능합니다.")
