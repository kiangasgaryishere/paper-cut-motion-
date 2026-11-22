#!/usr/bin/env bash
set -euo pipefail
# Native JPEG renderer is full-range BT.601. Convert actual samples to limited BT.709,
# then explicitly signal primaries/transfer in H.264 VUI as well as the MP4 container.
ffmpeg -y -v error -i films/carpet-comic-history/out/picture-v4.mp4 -i films/carpet-comic-history/out/mix-v4.wav -map 0:v:0 -map 1:a:0 -vf scale=in_range=pc:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709,format=yuv420p -c:v libx264 -crf 19 -maxrate 6M -bufsize 8M -preset fast -pix_fmt yuv420p -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 256k -ar 48000 -map_metadata -1 -bsf:v h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0 -movflags +faststart+write_colr -t 93 video/carpet-comic-history-v4.mp4
