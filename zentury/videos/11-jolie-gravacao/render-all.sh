#!/usr/bin/env bash
# Gera os vídeos da pasta edls/ (um por vez: build → mix → render → loudnorm → versão celular).
# Uso: ./render-all.sh [edls/01-tapioca.json ...]   (sem argumentos: todos, menos o 00 já entregue)
set -euo pipefail
cd "$(dirname "$0")"
FILES=("$@"); [ ${#FILES[@]} -eq 0 ] && FILES=(edls/0[1-9]*.json)
for f in "${FILES[@]}"; do
  n=$(basename "$f" .json)
  python3 -I src/build.py . "$f"
  python3 -I audio.py
  npx --yes hyperframes@0.8.139 render --quality delivery -o renders/raw.mp4 2>&1 | grep -E "rendered|rror" || true
  ffmpeg -y -v error -i renders/raw.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k -movflags +faststart "renders/jolie-$n.mp4"
  rm renders/raw.mp4
  ffmpeg -y -v error -i "renders/jolie-$n.mp4" -c:v libx264 -crf 22 -preset slow -c:a copy -movflags +faststart "renders/jolie-$n-celular.mp4"
  echo "== $n $(ffprobe -v error -show_entries format=duration -of csv=p=0 renders/jolie-$n.mp4)s"
done
python3 -I src/build.py . edl.json >/dev/null && python3 -I audio.py >/dev/null   # volta o index.html para o vídeo principal
