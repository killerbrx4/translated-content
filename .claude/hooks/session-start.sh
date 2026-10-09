#!/bin/bash
# ZENTURY Motion Studio: prepara a sessão na nuvem (idempotente, não interativo).
set -uo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

log() { echo "[zentury-setup] $*" >&2; }

# 1. Python: render bare-metal (Playwright), áudio (numpy), rastreamento de mão (MediaPipe), referências (yt-dlp)
pip install -q --disable-pip-version-check playwright imageio-ffmpeg numpy pillow mediapipe opencv-python-headless yt-dlp >/dev/null 2>&1 \
  && log "python ok" || log "AVISO: pip falhou (rede?)"

# 2. Bibliotecas de sistema do MediaPipe
if ! ldconfig -p 2>/dev/null | grep -q libEGL.so.1; then
  (apt-get install -y -q libegl1 libgles2 >/dev/null 2>&1 || (apt-get update -q >/dev/null 2>&1 && apt-get install -y -q libegl1 libgles2 >/dev/null 2>&1)) \
    && log "libEGL ok" || log "AVISO: libEGL não instalada"
fi

# 3. Skills do HyperFrames (core set) em ~/.claude/skills
npx --yes hyperframes@latest skills update >/dev/null 2>&1 && log "hyperframes skills ok" || log "AVISO: hyperframes skills update falhou"

# 4. Modelo de rastreamento de mão
MODEL_DIR="$HOME/.cache/zentury"; mkdir -p "$MODEL_DIR"
if [ ! -s "$MODEL_DIR/hand_landmarker.task" ]; then
  curl -sSfL -m 120 -o "$MODEL_DIR/hand_landmarker.task" \
    https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task \
    && log "modelo de mão ok" || log "AVISO: modelo de mão não baixado"
fi

# 5. Variáveis para a sessão
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  {
    echo "export ZENTURY_HAND_MODEL=\"$MODEL_DIR/hand_landmarker.task\""
    [ -x /opt/pw-browsers/chromium ] && echo 'export ZENTURY_CHROMIUM="/opt/pw-browsers/chromium"'
  } >> "$CLAUDE_ENV_FILE"
fi
exit 0
