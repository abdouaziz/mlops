from pydantic import BaseModel, Field


class SynthesizeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1000, examples=["salamalekum, na nga def"])


class TranscribeResponse(BaseModel):
    text: str
    latency_ms: int


class HealthResponse(BaseModel):
    status: str
    whisper_version: str
    tts_version: str
    models_loaded: list[str]
