import os
import subprocess
import tempfile

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv("/Users/jojo/PycharmProjects/IntroToProgrammingProject/.env")

_GEMINI_TTS_MODEL = 'gemini-3.1-flash-preview-tts'


class PollyService:
    @staticmethod
    def synthesize(text: str, voice: str = 'Aoede') -> bytes:
        """Synthesize Spanish speech via Gemini TTS and return raw MP3 bytes."""
        client = genai.Client(api_key=os.getenv('GEMINI_KEY'))

        response = client.models.generate_content(
            model=_GEMINI_TTS_MODEL,
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=['AUDIO'],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice,
                        )
                    )
                ),
            ),
        )

        part = response.candidates[0].content.parts[0]
        raw_audio = part.inline_data.data  # SDK already decodes from base64 — use bytes directly
        mime = part.inline_data.mime_type

        # If Gemini returned a WAV/RIFF container, convert it directly.
        # If it returned raw L16 PCM, tell ffmpeg the encoding explicitly.
        if raw_audio[:4] == b'RIFF' or 'wav' in mime.lower():
            return PollyService._to_mp3_from_wav(raw_audio)

        # Raw PCM — parse sample rate from MIME (default 24 kHz)
        sample_rate = 24000
        if 'rate=' in mime:
            try:
                sample_rate = int(mime.split('rate=')[1].split(';')[0])
            except ValueError:
                pass

        return PollyService._to_mp3_from_pcm(raw_audio, sample_rate)

    # ── ffmpeg helpers ────────────────────────────────────────────────────────

    @staticmethod
    def _to_mp3_from_wav(wav_bytes: bytes) -> bytes:
        """Convert WAV bytes → MP3 via ffmpeg (auto-detected input format)."""
        return PollyService._run_ffmpeg(wav_bytes, '.wav', [])

    @staticmethod
    def _to_mp3_from_pcm(pcm_bytes: bytes, sample_rate: int) -> bytes:
        """Convert raw signed-16-bit-LE mono PCM → MP3 via ffmpeg."""
        pcm_args = ['-f', 's16le', '-ar', str(sample_rate), '-ac', '1']
        return PollyService._run_ffmpeg(pcm_bytes, '.pcm', pcm_args)

    @staticmethod
    def _run_ffmpeg(audio_bytes: bytes, in_suffix: str, extra_input_args: list) -> bytes:
        in_tmp = out_tmp = None
        try:
            in_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=in_suffix)
            in_tmp.write(audio_bytes)
            in_tmp.close()

            out_tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            out_tmp.close()

            cmd = ['ffmpeg', '-y'] + extra_input_args + ['-i', in_tmp.name, out_tmp.name]
            result = subprocess.run(cmd, capture_output=True)

            if result.returncode != 0:
                raise RuntimeError(
                    f"ffmpeg failed (exit {result.returncode}):\n"
                    + result.stderr.decode(errors='replace')
                )

            mp3 = open(out_tmp.name, 'rb').read()
            if not mp3:
                raise RuntimeError("ffmpeg produced an empty MP3 file.")
            return mp3
        finally:
            for path in (in_tmp, out_tmp):
                if path and os.path.exists(path.name):
                    try:
                        os.remove(path.name)
                    except OSError:
                        pass
