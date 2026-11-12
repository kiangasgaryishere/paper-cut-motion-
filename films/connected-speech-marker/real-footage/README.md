# Real-footage edition

[Download the completed real-footage MP4](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/2da8beadd365b615a0513004c556a9e6f49b21a3/video/connected-speech-real-footage-v1.mp4). Verified downloaded bytes match the committed export.

User requested a separate version using the supplied movie clip and its own dialogue sound, replacing the English narrator sample. The original illustrated v1 MP4 remains available unchanged.

- First screening: 1.875–4.250 seconds, no subtitles and no underlying narrator sample or foley.
- After “فهمیدی چی گفت؟”, repeat the same clip at 6.000–8.375 seconds, with the English caption **Honey, what you doing?** White text sits on a charcoal panel.
- The replay adds 57 frames (2.375s). All subsequent voice, visuals, captions and effects shift together. Final duration: 60.375s, 1449 frames at 24fps.
- Lesson captions use white on charcoal for higher contrast. Final **LISTEN** remains English.
- The clip keeps its full wide composition inside the portrait paper scene. No face is cropped to force a vertical composition.
- No added music or new speech synthesis. Supplied movie sound remains intact apart from a -0.5dB headroom adjustment and 3ms endpoint ramps.

The actual movie wording is “Honey, what you doing?” (local English ASR evidence included); relevant written examples have been matched to it, rather than retaining the earlier narrator's “Darling, what are you doing?”. The Persian educational script and translation are retained.

## Build

From repository root, using the existing Opuscar environment:

```bash
PLAYWRIGHT_CHROME=/usr/bin/chromium LEMO_ANGLE=swiftshader node films/connected-speech-marker/tools/real-review.mjs
PLAYWRIGHT_CHROME=/usr/bin/chromium LEMO_ANGLE=swiftshader node core/render/video.mjs films/connected-speech-marker --fps 24 --workers 3 --size 1080x1920 --q real=1 --out films/connected-speech-marker/out/real-base.mp4
/workspace/lemo-opuscar/.venv/bin/python films/connected-speech-marker/tools/build-real.py
```

`out/mix.wav` is the mastered, original-clock base mix from the original film build. `build-real.py` replaces the narrator example, inserts the captioned movie replay and writes the exact edit map to `timeline.json`. The movie is frame-resampled from 23.976 to 24fps; audio is not stretched. A short held last frame pads the screening window. Native query flags leave the original default illustrated composition/caption treatment intact.

After building, run `/workspace/lemo-opuscar/.venv/bin/python films/connected-speech-marker/tools/verify-real.py`.

Final export: `video/connected-speech-real-footage-v1.mp4`. QC and delivery verification are recorded alongside this file. Representative frames are reviewed; no independent real-time listening review is claimed.
