#!/bin/bash
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
LIB=$(cd "$HERE/../../.." && pwd)
cd "$LIB"
export PLAYWRIGHT_CHROME=${PLAYWRIGHT_CHROME:-/usr/bin/chromium}
export LEMO_ANGLE=${LEMO_ANGLE:-swiftshader}
ffmpeg -v error -y -i "$HERE/narration.mp3" -ar 48000 -ac 1 "$HERE/voice.wav"
"$LIB/.venv/bin/python" "$HERE/mix.py"
node core/render/video.mjs "$HERE" --fps 30 --workers 3 --size 1080x1920 --out "$HERE/out/picture-v2.mp4"
sh core/render/mux.sh "$HERE/out/picture-v2.mp4" "$HERE/mix.wav" "$LIB/video/a-the-kings-v2.mp4" 30 0
