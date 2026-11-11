#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
cd "$ROOT"
export PLAYWRIGHT_CHROME=${PLAYWRIGHT_CHROME:-/usr/bin/chromium}
export LEMO_ANGLE=${LEMO_ANGLE:-swiftshader}
PYTHON_BIN=${FILM_PYTHON:-/workspace/lemo-opuscar/.venv/bin/python}
if [ ! -f "$HERE/out/voice-master-v2.wav" ]; then "$PYTHON_BIN" "$HERE/prepare_voice.py"; fi
if [ ! -f "$HERE/out/revision-v2-sfx.wav" ] || [ ! -f "$HERE/out/opening-delivery-v2.mp4" ]; then bash "$HERE/build-v2.sh"; fi
"$PYTHON_BIN" "$HERE/mix_revision_v3.py"
"$PYTHON_BIN" "$HERE/audible_sfx_v3.py"
node core/render/video.mjs "$HERE" --fps 30 --workers 3 --size 1080x1920 --q 'start=70&end=97.66666666666667' --out "$HERE/out/hicks-picture-v3.mp4"
ffmpeg -v error -y -i "$HERE/out/hicks-picture-v3.mp4" -an -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -movflags +faststart "$HERE/out/hicks-delivery-v3.mp4"
"$PYTHON_BIN" "$HERE/assemble_revision_v3.py"
