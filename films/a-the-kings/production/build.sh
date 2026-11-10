#!/bin/bash
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
LIB=$(cd "$HERE/../../.." && pwd)
cd "$LIB"
export PLAYWRIGHT_CHROME=${PLAYWRIGHT_CHROME:-/usr/bin/chromium}
export LEMO_ANGLE=${LEMO_ANGLE:-swiftshader}
ffmpeg -v error -y -i "$HERE/narration-v4.mp3" -ar 48000 -ac 1 "$HERE/voice.wav"
ffmpeg -v error -y -i "$HERE/voice.wav" -af 'highpass=f=75,equalizer=f=2500:t=q:w=0.8:g=1.3,acompressor=threshold=0.16:ratio=1.8:attack=12:release=140:makeup=1.15' -c:a pcm_f32le "$HERE/voice-v7.wav"
"$LIB/.venv/bin/python" "$HERE/mix_v7.py"
node core/render/video.mjs "$HERE" --fps 30 --workers 3 --size 1080x1920 --out "$HERE/out/picture-v7.mp4"
sh "$HERE/master_v7.sh" "$HERE/out/picture-v7.mp4" "$HERE/mix-v7.wav" "$LIB/video/a-the-kings-v7.mp4" 30 0
