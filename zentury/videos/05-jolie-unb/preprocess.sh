#!/usr/bin/env bash
# Pré-tratamento (576x1024 do WhatsApp) + recorte das apresentadoras no gancho (texto atrás delas).
# Uso: ./preprocess.sh /caminho/video.mov
set -euo pipefail
SRC="$1"; cd "$(dirname "$0")"
mkdir -p assets/footage assets/audio
ffmpeg -y -v error -i "$SRC" -vf "scale=1080:1920:flags=lanczos,unsharp=5:5:0.5:5:5:0.0,eq=contrast=1.06:saturation=1.08:gamma=0.98" \
  -an -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -g 15 -r 30 assets/footage/jolie.mp4
ffmpeg -y -v error -i "$SRC" -vn -ac 2 -ar 48000 assets/audio/voice.wav
# trecho do gancho (mesmo intervalo do corte c1 em edl.json) → recorte com alpha
ffmpeg -y -v error -ss 0.65 -to 2.98 -i assets/footage/jolie.mp4 -c:v libx264 -crf 14 -pix_fmt yuv420p assets/footage/hook.mp4
npx --yes hyperframes@0.8.139 remove-background assets/footage/hook.mp4 -o assets/footage/hook-cut.webm --quality best
echo ok
