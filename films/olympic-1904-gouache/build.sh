#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
cd "$ROOT"
export PLAYWRIGHT_CHROME=${PLAYWRIGHT_CHROME:-/usr/bin/chromium}
export LEMO_ANGLE=${LEMO_ANGLE:-swiftshader}
mkdir -p "$HERE/out" "$ROOT/video"
"$ROOT/.venv/bin/python" "$HERE/sound.py"
node core/render/video.mjs "$HERE" --fps 30 --workers 3 --size 1080x1920 --out "$HERE/out/picture.mp4"
ffmpeg -v error -y -i "$HERE/out/picture.mp4" -i "$HERE/out/sound.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -t 10 -movflags +faststart "$ROOT/video/olympic-1904-gouache-test-v1.mp4"
