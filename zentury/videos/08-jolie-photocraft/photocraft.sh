#!/usr/bin/env bash
# Etapas feitas no PhotoCraft (storytold/photocraft, CLI compilada com `cargo build --release -p photocraft-cli`).
# Uso: PC=/caminho/photocraft-cli FR=<pasta com frames 1080x1920 dos vídeos> ./photocraft.sh
set -euo pipefail
cd "$(dirname "$0")"; mkdir -p photocraft assets/photocraft; O=photocraft
# 1) "Jolie Look": Curves + Vibrance + Photo Filter num frame de referência → LUT .cube (vai para TODA a filmagem via ffmpeg lut3d)
$PC run "$FR/acai_pronto.png" \
  --cmd layer.newAdjustmentLayer.curves --params '{"points":[[0,8],[60,52],[128,134],[200,214],[255,252]],"red":[[0,0],[128,132],[255,255]],"blue":[[0,6],[128,124],[255,248]]}' \
  --cmd layer.newAdjustmentLayer.vibrance --params '{"vibrance":32,"saturation":6}' \
  --cmd layer.newAdjustmentLayer.photoFilter --params '{"filter":"warming81","density":14}' \
  --cmd file.export.colorLookupTables --params "{\"path\":\"$PWD/$O/jolie-look.cube\",\"size\":33,\"title\":\"Jolie Look (ZENTURY)\"}" --out $O/look-referencia.psd
# 2) Recortes de produto (Object Selection numa área) → adesivo com Stroke + Drop Shadow
cut() { $PC run "$1" --cmd layer.new.layerFromBackground --params '{}' --cmd select.object --params "{\"rect\":$2}" \
  --cmd select.modify.smooth --params '{"radius":4}' --cmd select.inverse --cmd edit.clear --cmd select.all \
  --cmd image.trim --params '{"basedOn":"transparent"}' --cmd image.canvasSize --params '{"width":80,"height":80,"relative":true,"extensionColor":"transparent"}' --out "$3-pad.png"
  $PC run "$3-pad.png" --cmd layer.layerStyle.stroke --params '{"size":16,"position":"outside","color":"#ffffff"}' \
  --cmd layer.layerStyle.dropShadow --params '{"color":"#1a0623","opacity":70,"distance":20,"size":14,"angle":90,"add":true}' --out "$3-sticker.png"; }
cut "$FR/acai_pronto_g.png" "[110,800,840,820]" $O/acai
cut "$FR/acai_puro_g.png" "[180,700,720,520]" $O/puro
# 3) Pôsteres em PSD com camadas (story 1080x1920 e feed 1080x1350): degradê, logo, títulos com sombra, adesivo, oferta e endereço.
#    Comandos: layer.newFillLayer.gradient · file.placeEmbedded · type.create (Montserrat) · layer.layerStyle.*  (ver BRIEF.md)
echo "ok"
