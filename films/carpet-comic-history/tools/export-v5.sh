#!/usr/bin/env bash
set -euo pipefail
ffmpeg -y -v error \
  -i video/carpet-comic-history-v4.mp4 \
  -i films/carpet-comic-history/out/mix-v5.wav \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -ar 48000 \
  -movflags +faststart -t 93 video/carpet-comic-history-v5.mp4
