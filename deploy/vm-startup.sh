#!/bin/bash
# Script de démarrage de la VM (exécuté à chaque boot) :
# Docker, puis le bucket des modèles monté en lecture seule avec Cloud Storage FUSE.
set -euo pipefail

BUCKET=models-weights-ai
MOUNT=/mnt/models

if ! command -v docker >/dev/null; then
  curl -fsSL https://get.docker.com | sh
fi
gcloud auth configure-docker us-central1-docker.pkg.dev --quiet

if ! command -v gcsfuse >/dev/null; then
  . /etc/os-release
  curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg -o /usr/share/keyrings/cloud.google.asc
  echo "deb [signed-by=/usr/share/keyrings/cloud.google.asc] https://packages.cloud.google.com/apt gcsfuse-${VERSION_CODENAME} main" \
    > /etc/apt/sources.list.d/gcsfuse.list
  apt-get update && apt-get install -y gcsfuse
fi

mkdir -p "$MOUNT" /var/cache/gcsfuse
cat > /etc/gcsfuse.yaml <<'EOF'
# Les dossiers whisper-small/v1/ etc. n'existent pas comme objets : implicit-dirs les fait apparaître
implicit-dirs: true
# Cache disque : le modèle n'est lu sur le réseau qu'une fois, les redémarrages lisent le disque local
cache-dir: /var/cache/gcsfuse
file-cache:
  max-size-mb: -1
  cache-file-for-range-read: true
metadata-cache:
  ttl-secs: 60
EOF

# Montage avec l'identité de la VM (vm-sa) ; allow_other pour que les conteneurs puissent lire
mountpoint -q "$MOUNT" || gcsfuse --config-file /etc/gcsfuse.yaml -o ro,allow_other "$BUCKET" "$MOUNT"
