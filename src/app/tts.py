import io

import numpy as np
from scipy.io import wavfile

from app import config
from app.storage import model_path


class Tts:
    def __init__(self):
        from TTS.utils.synthesizer import Synthesizer

        path = model_path("vits-tts", config.TTS_VERSION)
        self.synth = Synthesizer(
            tts_checkpoint=str(path / "model.pth"),
            tts_config_path=str(path / "config.json"),
            use_cuda=False,
        )

    def synthesize(self, text: str) -> bytes:
        # Le modèle a été entraîné sur du texte en minuscules
        wav = self.synth.tts(text.lower())
        buffer = io.BytesIO()
        wavfile.write(buffer, self.synth.output_sample_rate, np.asarray(wav, dtype=np.float32))
        return buffer.getvalue()
