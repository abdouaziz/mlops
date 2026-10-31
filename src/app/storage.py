from pathlib import Path

from app import config


def model_path(name: str, version: str) -> Path:
    """Dossier d'un modèle dans le bucket monté : <MODEL_ROOT>/<name>/<version>/."""
    path = config.MODEL_ROOT / name / version
    if not (path / "config.json").exists():
        raise FileNotFoundError(
            f"{path}/config.json introuvable : le bucket est-il monté sur {config.MODEL_ROOT} ?"
        )
    return path
