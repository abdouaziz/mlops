import os
import tempfile
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile
from fastapi.responses import Response

from app import config
from app.schemas import HealthResponse, SynthesizeRequest, TranscribeResponse
from app.stt import Stt
from app.tts import Tts

models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    models["stt"] = Stt()
    models["tts"] = Tts()
    yield
    models.clear()


app = FastAPI(title="MLOps Wolof", lifespan=lifespan)


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="ok",
        whisper_version=config.WHISPER_VERSION,
        tts_version=config.TTS_VERSION,
        models_loaded=sorted(models),
    )


@app.post("/transcribe", response_model=TranscribeResponse)
def transcribe(file: UploadFile):
    suffix = os.path.splitext(file.filename or "")[1]
    with tempfile.NamedTemporaryFile(suffix=suffix) as tmp:
        tmp.write(file.file.read())
        tmp.flush()
        start = time.perf_counter()
        text = models["stt"].transcribe(tmp.name)
    latency_ms = (time.perf_counter() - start) * 1000
    return TranscribeResponse(text=text, latency_ms=round(latency_ms))


@app.post("/synthesize")
def synthesize(request: SynthesizeRequest):
    audio = models["tts"].synthesize(request.text)
    return Response(content=audio, media_type="audio/wav")
