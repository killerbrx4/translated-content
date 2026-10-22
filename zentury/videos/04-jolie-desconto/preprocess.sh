#!/usr/bin/env bash
# Pré-tratamento do anúncio enviado pelo cliente (576x1024, comprimido pelo WhatsApp).
# Uso: ./preprocess.sh /caminho/video.mov
set -euo pipefail
SRC="$1"; cd "$(dirname "$0")"
mkdir -p assets/footage assets/audio assets/img
# upscale 1080x1920 + nitidez leve + grade (contraste/saturação discretos, mantém o calor do dia)
ffmpeg -y -v error -i "$SRC" -vf "scale=1080:1920:flags=lanczos,unsharp=5:5:0.5:5:5:0.0,eq=contrast=1.06:saturation=1.08:gamma=0.98" \
  -an -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -g 15 -r 30 assets/footage/jolie.mp4
ffmpeg -y -v error -i "$SRC" -vn -ac 2 -ar 48000 assets/audio/voice.wav
# arte final do cliente (cartão de endereço), usada sem alteração
ffmpeg -y -v error -ss 28.6 -i "$SRC" -frames:v 1 -vf "scale=1080:1920:flags=lanczos,unsharp=3:3:0.4" assets/img/cartao-jolie.png
echo ok
