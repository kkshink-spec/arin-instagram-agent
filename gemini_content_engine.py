import os
import mimetypes
import struct
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    genai = None
    types = None
    HAS_GENAI = False

class GeminiContentEngine:
    """
    Google Gemini SDK(google-genai) 기반 바이럴 캡션, AI 프롬프트 및 릴스 오디오(TTS) 자동 생성 엔진
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if HAS_GENAI and self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def generate_caption_and_prompt(self, topic: str) -> dict:
        """
        주제를 기반으로 Gemini가 최고 성과의 인스타그램 캡션 및 영문 3D 미디어 프롬프트를 자동 생성합니다.
        """
        if not self.client:
            return None
            
        prompt = f"""당신은 인스타그램 저장률과 공유율을 극대화하는 바이럴 마케팅 전문가입니다.
주제: "{topic}"

이 주제에 맞춰 인스타그램 포스팅용 캡션을 작성해 주세요.
조건:
1. 강력한 훅(Hook) 헤드라인 문구
2. 시청자의 통증을 해결하는 3가지 실용적 포인트
3. 저장(Bookmark) 및 공유(Share)를 유도하는 CTA 문구
4. 관련 인기 해시태그 10개
5. 이미지 생성용 3D Glassmorphism 영문 프롬프트 (Prompt: ...)

한국어로 캡션을 작성하고, 마지막 줄에 "PROMPT: <영문 프롬프트>" 형태로 적어주세요."""

        try:
            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )
            full_text = response.text
            
            # PROMPT: 부분 분리
            image_prompt = "A high-impact 3D glassmorphism dark aesthetic card news cover artwork for Instagram, 8k render"
            caption_text = full_text
            
            if "PROMPT:" in full_text:
                parts = full_text.split("PROMPT:")
                caption_text = parts[0].strip()
                image_prompt = parts[1].strip()
                
            return {
                "caption": caption_text,
                "prompt": image_prompt
            }
        except Exception as e:
            print(f"[Gemini Content Engine Warning] {e}")
            return None

    def generate_reels_tts_audio(self, narration_text: str, output_path: str = "reels_narration.wav") -> str:
        """
        Gemini TTS 스피커 모델을 사용하여 릴스(Reels) 나레이션 음성 파일(.wav)을 자동 생성합니다.
        """
        if not self.client:
            raise Exception("GEMINI_API_KEY가 설정되지 않았습니다.")

        model = "gemini-2.5-flash"
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            response_modalities=["audio"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name="Zephyr"
                    )
                )
            ),
        )

        audio_bytes = b""
        for chunk in self.client.models.generate_content_stream(
            model=model,
            contents=narration_text,
            config=generate_content_config,
        ):
            if chunk.parts is None:
                continue
            if chunk.parts[0].inline_data and chunk.parts[0].inline_data.data:
                inline_data = chunk.parts[0].inline_data
                data_buffer = inline_data.data
                file_extension = mimetypes.guess_extension(inline_data.mime_type)
                if file_extension is None or file_extension != ".wav":
                    data_buffer = self._convert_to_wav(inline_data.data, inline_data.mime_type)
                audio_bytes += data_buffer

        with open(output_path, "wb") as f:
            f.write(audio_bytes)

        print(f"[+] 릴스 TTS 나레이션 음성 생성 완료: {output_path}")
        return output_path

    def _convert_to_wav(self, audio_data: bytes, mime_type: str) -> bytes:
        bits_per_sample = 16
        rate = 24000
        parts = mime_type.split(";")
        for param in parts:
            param = param.strip()
            if param.lower().startswith("rate="):
                try:
                    rate = int(param.split("=", 1)[1])
                except (ValueError, IndexError):
                    pass
        num_channels = 1
        data_size = len(audio_data)
        bytes_per_sample = bits_per_sample // 8
        block_align = num_channels * bytes_per_sample
        byte_rate = rate * block_align
        chunk_size = 36 + data_size

        header = struct.pack(
            "<4sI4s4sIHHIIHH4sI",
            b"RIFF", chunk_size, b"WAVE", b"fmt ",
            16, 1, num_channels, rate, byte_rate, block_align, bits_per_sample,
            b"data", data_size
        )
        return header + audio_data

    def generate_news_slides_from_headlines(self, headlines: list) -> list:
        """
        뉴스 헤드라인 리스트를 받아서 '1분 손해방지' 컨셉에 맞는 뉴스 1개를 선정하고,
        카드뉴스 슬라이드 5장(JSON 형식)을 생성합니다.
        """
        import json
        if not self.client:
            raise Exception("GEMINI_API_KEY가 설정되지 않았습니다.")
            
        headlines_text = "\n".join([f"{i+1}. {h}" for i, h in enumerate(headlines)])
        
        prompt = f"""당신은 인스타그램 저장률과 공유율을 극대화하는 바이럴 마케팅 전문가입니다.
다음은 오늘 한국의 주요 최신 뉴스 헤드라인입니다:

{headlines_text}

이 중에서 '생활 정보', '지원금', '세금', '스미싱/사기 주의', '부동산/금융' 등 대중이 알지 못하면 손해를 볼 수 있거나 돈이 되는 뉴스 1개를 선택하여, 5장짜리 카드뉴스 텍스트를 작성해주세요.

컨셉: 손해방지 꿀팁 (안 보면 나만 손해!)
조건:
- 인스타그램 모바일에서 읽기 편하게 글자를 최소화하세요. (매우 중요)
- 슬라이드 1~5의 'title'은 반드시 2줄 이내, 'desc'는 최대 5줄까지 작성할 수 있습니다.
- **카드뉴스 슬라이드 내부(title, desc)에는 이모지(Emoji)를 절대 사용하지 마세요. (글꼴 깨짐 방지)**
- **신뢰성 향상을 위해 뉴스 출처(언론사)와 발행일자는 카드뉴스 슬라이드 내부(title, desc)에는 절대 넣지 말고, 인스타그램 캡션(caption)은 맨 앞에, 스레드 포스트(threads_post)는 맨 마지막에만 표기해 주세요.**
- 슬라이드 1은 카드뉴스의 **메인 표지(Cover)**입니다. 'badge'는 "오늘의 손해방지 꿀팁"으로 고정하고, 'title'은 강력한 후킹(Hook) 문구, 'desc'는 호기심을 유발하는 부제목(서브카피)으로 작성하세요.
- 슬라이드 2~4는 핵심 내용, 슬라이드 5는 요약 및 공유(CTA) 유도
- **스레드(Threads) 글은 이미지가 첨부되지 않고 텍스트 단독으로 올라갑니다. 따라서 기사의 핵심 내용(무엇이 문제고, 어떻게 해야 하는지)이 모두 포함되도록 상세하게 적되, 트위터나 스레드 특유의 밈, 유머, 한탄, 혹은 뼈때리는 현실 조언 느낌으로 매우 힙하고 자연스럽게 작성하세요. "와 미쳤다", "다들 뉴스 보셨어요?", "이거 진짜 모르면 바보됨" 같은 찐텐션(진짜 감정)이 느껴지는 구어체를 사용하고, 줄바꿈을 적극 활용하세요. 출처는 맨 마지막 줄에 가볍게 (✍️출처: OOO) 형식으로 적어주세요.**
- **인스타그램 캡션(본문)은 독자가 충분히 이해하고 행동할 수 있도록 매우 상세하고 길게(기존 대비 2배 분량 이상) 작성해 주세요.**

결과물은 반드시 아래 JSON 형식으로만 출력하세요.
{{
  "slides": [
    {{
      "badge": "손해방지 꿀팁 STEP 01",
      "title": "슬라이드 1 제목 (두 줄 권장, \\n 사용)",
      "desc": "슬라이드 1 설명 (최대 다섯 줄, \\n 사용)"
    }},
    ... (총 5개)
  ],
  "caption": "인스타그램용 본문 텍스트 (기존보다 2배 이상 길고 상세하게 작성, 해시태그 포함, 맨 앞에 뉴스 출처 표기)",
  "threads_post": "스레드(Threads)용 짧고 친근한 텍스트 (맨 앞에 뉴스 출처 표기)"
}}"""
        try:
            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"[Gemini Content Engine Warning] {e}")
            return None

if __name__ == "__main__":
    pass
