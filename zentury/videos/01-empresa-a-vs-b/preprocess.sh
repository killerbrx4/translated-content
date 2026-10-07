#!/usr/bin/env bash
# Pré-tratamento da gravação do apresentador para o EP.01.
# Uso: ./preprocess.sh /caminho/gravacao.mp4
set -euo pipefail
SRC="$1"
mkdir -p assets/footage assets/audio assets/img
ffmpeg -y -v error -i "$SRC" -filter_complex \
  "[0:v]hflip,fps=30,scale=1080:1936:flags=lanczos,crop=1080:1920:0:8,unsharp=5:5:0.6:5:5:0.0,eq=contrast=1.10:brightness=-0.05:saturation=0.82:gamma=0.94,curves=all='0/0 0.12/0.07 0.5/0.47 0.85/0.80 1/0.92'[v];[0:a]highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-14:TP=-1.5:LRA=7[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 15 -pix_fmt yuv420p -g 15 -c:a aac -b:a 192k -ar 48000 assets/footage/presenter.mp4
ffmpeg -y -v error -i assets/footage/presenter.mp4 -vn -c:a aac -b:a 192k assets/audio/voice.m4a
ffmpeg -y -v error -ss 18.12 -i assets/footage/presenter.mp4 -frames:v 1 -q:v 2 assets/img/freeze.jpg
echo "ok: assets/footage/presenter.mp4, assets/audio/voice.m4a, assets/img/freeze.jpg"
