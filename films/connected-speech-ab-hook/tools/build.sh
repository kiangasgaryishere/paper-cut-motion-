#!/usr/bin/env bash
set -euo pipefail
PROJECT="$(cd "$(dirname "$0")/.." && pwd)"
REPO="$(cd "$PROJECT/../.." && pwd)"
PYTHON="${OPUSCAR_PYTHON:-/workspace/lemo-opuscar/.venv/bin/python}"
export PLAYWRIGHT_CHROME="${PLAYWRIGHT_CHROME:-/usr/bin/chromium}"
export LEMO_ANGLE="${LEMO_ANGLE:-swiftshader}"
mkdir -p "$PROJECT/out/clip"
ffmpeg -y -v error -i "$PROJECT/../connected-speech-marker/assets/mummy-real-clip.mp4" -vf fps=24 -q:v 2 "$PROJECT/out/clip/%02d.jpg"
node "$PROJECT/tools/review.mjs"
"$PYTHON" "$PROJECT/tools/mix.py"
node "$REPO/core/render/video.mjs" "$PROJECT" --fps 24 --workers 3 --size 1080x1920 --out "$PROJECT/out/picture.mp4"
ffmpeg -y -v error -i "$PROJECT/out/picture.mp4" -i "$PROJECT/out/mix.wav" -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -ar 48000 -t 69 -movflags +faststart "$REPO/video/connected-speech-ab-hook-v1.mp4"
"$PYTHON" "$PROJECT/tools/verify.py"
