# Connected Speech — Marker on Paper

**Preproduction review, not the final film.** [Persian review: three actual style frames and proposed storyboard](REVIEW.fa.md). [Source analysis](ANALYSIS.fa.md). [Style analysis](STYLE_ANALYSIS.fa.md).

User decisions: marker reconstruction of the opening film situation; complete production after reviewing the plan/style frames; then independent execution. Original supplied script and voice retained. Effects only, Persian captions, separate English examples. Native marker style proposed at 1080×1920 / 24 fps, drawings on twos, approximately 58 seconds including a short ending hold.

The official marker style/engine is newer than the existing local Opuscar clone. Selected source files were read from current upstream commit 3a7132b996be0241c1ea0ab180d519f06e6f10b6 without resetting/updating the existing library. Existing core dependencies, Chromium, FFmpeg, fonts and local ASR tools are reused; no unnecessary voice/music models or sample packs are installed.

`review.html` / `review.js` implement a **three-frame review gallery** using the real marker engine. `index.html` opens that gallery. They are not the 58-second animation and must not be exported or described as the completed film. Full production is pending the user's selected review checkpoint. `timeline.json` is a proposed source clock/shot plan; final captions and pen events are intentionally not marked complete.

The script/audio match includes an English quote that exists in the recording but not in the written script: “Darling, what are you doing?” The first hearing keeps the answer hidden. Source audio is 57.19625 seconds decoded; measured true peak exceeds output headroom, so final mastering is still required.

See CREDITS.md and licenses/ for source/code/font attribution. Upstream docs/poster are retained only locally in ignored reference/. Original review frames are committed. Temporary analysis WAVs and logs are ignored under analysis/out/.

Render the review gallery from this repository, or set LIB to an existing compatible Lemo-Opuscar library:

```bash
PLAYWRIGHT_CHROME=/usr/bin/chromium LEMO_ANGLE=swiftshader node films/connected-speech-marker/tools/render-review.mjs
```

Kalam glyphs are included. To rebuild them, use the configured Opuscar Python with NumPy, Pillow and SciPy:

```bash
"$LIB/.venv/bin/python" films/connected-speech-marker/tools/make_glyphs.py
```

Actual source metadata and preliminary ASR evidence are under analysis/. Decoder errors/recoveries and lack of independent listening review are documented; these are not final audio/caption QC results.
