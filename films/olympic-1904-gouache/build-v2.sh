#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
cd "$ROOT"
export PLAYWRIGHT_CHROME=${PLAYWRIGHT_CHROME:-/usr/bin/chromium}
export LEMO_ANGLE=${LEMO_ANGLE:-swiftshader}
PYTHON_BIN=${FILM_PYTHON:-/workspace/lemo-opuscar/.venv/bin/python}
"$PYTHON_BIN" "$HERE/prepare_voice.py"
# These canonical mixes are independent of the new visual renderer.
if [ ! -f "$HERE/out/part01-sfx-v2.wav" ]; then "$PYTHON_BIN" "$HERE/mix_part01.py"; fi
if [ ! -f "$HERE/out/part02-sfx-v1.wav" ]; then "$PYTHON_BIN" "$HERE/mix_part02.py"; fi
if [ ! -f "$HERE/out/part03-sfx-v1.wav" ]; then "$PYTHON_BIN" "$HERE/mix_part03.py"; fi
if [ ! -f "$HERE/out/part04-sfx-v1.wav" ]; then "$PYTHON_BIN" "$HERE/mix_part04.py"; fi
if [ ! -f "$HERE/out/part13-sfx-v1.wav" ]; then "$PYTHON_BIN" "$HERE/mix_finish.py"; fi
"$PYTHON_BIN" "$HERE/mix_revision_v2.py"
node core/render/video.mjs "$HERE" --fps 30 --workers 3 --size 1080x1920 --q 'start=0&end=20' --out "$HERE/out/opening-picture-v2.mp4"
ffmpeg -v error -y -i "$HERE/out/opening-picture-v2.mp4" -an -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -movflags +faststart "$HERE/out/opening-delivery-v2.mp4"
"$PYTHON_BIN" "$HERE/assemble_revision_v2.py"
