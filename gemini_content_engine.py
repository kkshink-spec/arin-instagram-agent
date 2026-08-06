import os
import mimetypes
import struct

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
                model="gemini-2.5-flash",
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

if __name__ == "__main__":
    pass
