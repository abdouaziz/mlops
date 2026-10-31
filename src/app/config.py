import os
from pathlib import Path

# Racine du bucket monté par Cloud Storage FUSE (gs://models-weights-ai -> /mnt/models)
MODEL_ROOT = Path(os.environ.get("MODEL_ROOT", "/mnt/models"))
WHISPER_VERSION = os.environ.get("WHISPER_VERSION", "v1")
TTS_VERSION = os.environ.get("TTS_VERSION", "v1")
