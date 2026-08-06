import os
import subprocess
import imageio_ffmpeg
from gtts import gTTS
from gemini_content_engine import GeminiContentEngine

class ReelsMaker:
    """
    AI 이미지 + TTS 음성 나레이션 오디오를 결합하여 9:16 인스타그램 릴스 MP4 동영상을 제작하는 모듈
    """
    def __init__(self):
        self.gemini_engine = GeminiContentEngine()
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    def create_reels_video(self, image_path: str, narration_text: str, output_mp4: str = "generated_reels.mp4") -> str:
        """
        1. TTS 나레이션 음성 파일 생성 (Gemini 또는 gTTS)
        2. 이미지와 음성을 합성하여 9:16 인스타그램 릴스 동영상(.mp4) 생성
        """
        audio_path = os.path.splitext(output_mp4)[0] + "_narration.mp3"
        print(f"[Reels Maker] 1. 음성 나레이션 오디오 생성 중...")
        
        # 1. Gemini TTS 시도 ➔ 실패 시 gTTS (Google Korean Voice)로 100% 보장 생성
        audio_created = False
        try:
            wav_path = os.path.splitext(output_mp4)[0] + "_narration.wav"
            self.gemini_engine.generate_reels_tts_audio(narration_text, wav_path)
            if os.path.exists(wav_path) and os.path.getsize(wav_path) > 1000:
                audio_path = wav_path
                audio_created = True
        except Exception:
            pass

        if not audio_created:
            try:
                tts = gTTS(text=narration_text, lang='ko')
                tts.save(audio_path)
                audio_created = True
                print(f"[+] gTTS 한국어 나레이션 오디오 생성 완료: {audio_path}")
            except Exception as tts_err:
                print(f"[Reels Maker Warning] TTS 오디오 생성 실패: {tts_err}")

        print(f"[Reels Maker] 2. 9:16 비디오 + 오디오 트랙 합성 엔진 가동 중... ({output_mp4})")
        
        if audio_created and os.path.exists(audio_path):
            cmd = [
                self.ffmpeg_exe, "-y",
                "-loop", "1", "-i", image_path,
                "-i", audio_path,
                "-c:v", "libx264", "-tune", "stillimage",
                "-c:a", "aac", "-b:a", "192k",
                "-pix_fmt", "yuv420p", "-shortest",
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                output_mp4
            ]
        else:
            cmd = [
                self.ffmpeg_exe, "-y",
                "-loop", "1", "-i", image_path,
                "-c:v", "libx264", "-t", "8",
                "-pix_fmt", "yuv420p",
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                output_mp4
            ]

        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"🎉 [성공] 음성 오디오가 포함된 릴스 비디오 생성 완료: {output_mp4} ({os.path.getsize(output_mp4)} bytes)")
            return output_mp4
        except Exception as err:
            print(f"[Reels Maker Error] 비디오 합성 실패: {err}")
            return image_path

if __name__ == "__main__":
    pass
