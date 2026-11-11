#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
cd "$ROOT"
export PLAYWRIGHT_CHROME=${PLAYWRIGHT_CHROME:-/usr/bin/chromium}
export LEMO_ANGLE=${LEMO_ANGLE:-swiftshader}
PYTHON_BIN=${FILM_PYTHON:-$ROOT/.venv/bin/python}
if [ ! -x "$PYTHON_BIN" ]; then PYTHON_BIN=/workspace/lemo-opuscar/.venv/bin/python; fi
mkdir -p "$HERE/out" "$ROOT/video"
"$PYTHON_BIN" "$HERE/prepare_voice.py"
"$PYTHON_BIN" "$HERE/mix_part01.py"
"$PYTHON_BIN" "$HERE/mix_part02.py"
node core/render/video.mjs "$HERE" --fps 30 --workers 3 --size 1080x1920 --q 'start=0&end=10' --out "$HERE/out/part01-picture-v2.mp4"
ffmpeg -v error -y -i "$HERE/out/part01-picture-v2.mp4" -i "$HERE/out/part01-mix-v2.wav" -map 0:v -map 1:a -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a aac -b:a 256k -t 10 -movflags +faststart "$ROOT/video/olympic-1904-part01-v2.mp4"
node core/render/video.mjs "$HERE" --fps 30 --workers 3 --size 1080x1920 --q 'start=10&end=20' --out "$HERE/out/part02-picture-v1.mp4"
ffmpeg -v error -y -i "$HERE/out/part02-picture-v1.mp4" -i "$HERE/out/part02-mix-v1.wav" -map 0:v -map 1:a -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a aac -b:a 256k -t 10 -movflags +faststart "$ROOT/video/olympic-1904-part02-v1.mp4"
"$PYTHON_BIN" "$HERE/assemble.py"
