# Rahnama five features — Whiteboard

Original 76s portrait Reel from supplied Persian script and narration. Output: ../../video/rahnama-five-whiteboard-v1.mp4. Production notes: TREATMENT.md, STORYBOARD.md, ART_DIRECTION.md, SOUND_PLAN.md. No music. Complete narration retained. Whiteboard source/style and font credits in CREDITS.md. Captions use actual Noto Sans Arabic fallback because Morabba binary was unavailable.

Rebuild from repository root (Node/Chromium/FFmpeg and Opuscar Python dependencies described in setup/):

```bash
/workspace/lemo-opuscar/.venv/bin/python films/rahnama-five-whiteboard/tools/prepare.py
PLAYWRIGHT_CHROME=/usr/bin/chromium LEMO_ANGLE=swiftshader node films/rahnama-five-whiteboard/tools/check-film.mjs
/workspace/lemo-opuscar/.venv/bin/python films/rahnama-five-whiteboard/tools/mix.py
PLAYWRIGHT_CHROME=/usr/bin/chromium LEMO_ANGLE=swiftshader node core/render/video.mjs films/rahnama-five-whiteboard --fps 24 --workers 3 --size 1080x1920 --out films/rahnama-five-whiteboard/out/picture.mp4
ffmpeg -y -i films/rahnama-five-whiteboard/out/picture.mp4 -i films/rahnama-five-whiteboard/out/mix.wav -map 0:v:0 -map 1:a:0 -vf scale=in_range=pc:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709,format=yuv420p -c:v libx264 -crf 14 -preset medium -pix_fmt yuv420p -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 256k -ar 48000 -map_metadata -1 -movflags +faststart -t 76 video/rahnama-five-whiteboard-v1.mp4
/workspace/lemo-opuscar/.venv/bin/python films/rahnama-five-whiteboard/tools/document.py
/workspace/lemo-opuscar/.venv/bin/python films/rahnama-five-whiteboard/tools/verify.py
```

Out/stills/WAV intermediate files are ignored; source MP3, timing, code and final MP4 are retained. Rebuild paths reflect this managed environment; use an equivalent Python with numpy, scipy, Pillow/RAQM and soundfile elsewhere. No external paid model/API required to render.
