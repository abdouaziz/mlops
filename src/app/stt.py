from transformers import pipeline

from app import config
from app.storage import model_path


class Stt:
    def __init__(self):
        path = model_path("whisper-small", config.WHISPER_VERSION)
        self.pipe = pipeline("automatic-speech-recognition", model=str(path), device="cpu")

    def transcribe(self, audio_path: str) -> str:
        return self.pipe(audio_path)["text"].strip()
