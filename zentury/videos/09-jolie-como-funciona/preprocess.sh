#!/usr/bin/env bash
# Pré-tratamento do primeiro criativo da Jolie (reedição) (576x1024 do WhatsApp). Sem fala; o áudio original é música de terceiros
# e é inteiro substituído pela trilha própria.
set -euo pipefail
SRC="$1"; cd "$(dirname "$0")"
mkdir -p assets/footage assets/audio
ffmpeg -y -v error -i "$SRC" -vf "scale=1080:1920:flags=lanczos,unsharp=5:5:0.5:5:5:0.0,eq=contrast=1.06:saturation=1.1:gamma=0.98" \
  -an -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -g 15 -r 30 assets/footage/jolie.mp4
ffmpeg -y -v error -i "$SRC" -vn -ac 2 -ar 48000 assets/audio/voice.wav
echo ok
