#!/usr/bin/env bash
# Pré-tratamento do vídeo 1 da Gamer Star (480x854 do WhatsApp, já editado pelo cliente).
# 1) A gravação foi feita com a câmera frontal espelhada: caixas das placas e a camisa da marca aparecem invertidas.
#    hflip deixa "GEFORCE RTX 4070" e "GAMER STAR" legíveis (as legendas queimadas ficam invertidas, mas são cobertas pela placa de legenda).
# 2) A voz é separada da música de fundo com Demucs (htdemucs_ft, pesos do Hugging Face dokodesuka/htdemucs_ft) para cortar sem saltos.
# Uso: ./preprocess.sh <video.mov> <vocals.wav do demucs>
set -euo pipefail
SRC="$1"; VOC="$2"; cd "$(dirname "$0")"
mkdir -p assets/footage assets/audio
ffmpeg -y -v error -i "$SRC" -vf "hflip,scale=1080:1920:flags=lanczos,unsharp=5:5:0.7:5:5:0.0,eq=contrast=1.05:saturation=1.06" \
  -an -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -g 15 -r 30 assets/footage/gamerstar.mp4
ffmpeg -y -v error -i "$VOC" -af "highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80" -ac 2 -ar 48000 -c:a pcm_s16le assets/audio/voice.wav
echo ok
