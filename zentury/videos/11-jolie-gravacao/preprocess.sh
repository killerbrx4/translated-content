#!/usr/bin/env bash
# Jolie · gravação de 20/10/2026. Vídeos vieram pelo WhatsApp (464x832, 60 fps); falas gravadas à parte no celular (.m4a).
# 1) Cada clipe usado → 1080x1920, 30 fps, upscale lanczos + nitidez leve + cor quente e consistente.
# 2) Falas do celular → limpeza leve (highpass, redução de ruído, compressão) a 48 kHz.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p assets/footage/n assets/audio/clean
for n in v01 v05 v06 v07 v08 v10 v11 v12 v14 v17 v18 v20 v23 v24 v25 v26 v27 v29 v30; do
  ffmpeg -y -v error -i assets/footage/raw/$n.mov -vf "scale=1080:1920:flags=lanczos,unsharp=5:5:0.6:5:5:0.0,eq=contrast=1.05:saturation=1.10:gamma=0.99,colorbalance=rs=0.02:bs=-0.02:rm=0.015:bm=-0.015" \
    -r 30 -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -g 15 -c:a aac -b:a 160k assets/footage/n/$n.mp4
done
for f in Pato__2 Pato__4 Pato__5 Pato__6 Pato__7 Avenida_Cln_2 Avenida_Cln_3; do
  ffmpeg -y -v error -i "assets/audio/raw/$f.m4a" -af "highpass=f=90,afftdn=nr=10:nf=-40,acompressor=threshold=-22dB:ratio=3:attack=5:release=90,equalizer=f=3500:t=q:w=1:g=2" -ac 1 -ar 48000 -c:a pcm_s16le assets/audio/clean/$f.wav
done
echo ok
