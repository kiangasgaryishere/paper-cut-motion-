# Connected Speech — Marker on Paper

Completed 58-second educational Reel: **1080×1920, 24 fps, H.264/AAC 48 kHz**. [Download the completed MP4](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/98d1dfaeb1c866e4115fd308014f49e5e00d4922/video/connected-speech-marker-v1.mp4). Final export: `../../video/connected-speech-marker-v1.mp4`.

User-approved direction: marker reconstruction of the opening film situation, then complete independent production. Supplied narration retained in full without cuts or speed changes; 0.80375 seconds of silent ending hold. No music. Native felt-tip and paper effects follow exported pen events, duck under speech, and are suppressed during the initial English listening sample.

`index.html` loads the actual time-driven film. `film-art.js` contains ten original page compositions; `film.js` implements native progressive marker strokes, skeleton handwriting, ink density, drawing on twos, a 24 fps camera, peel and shape-matched push transitions. `timeline.json` controls pages and Persian captions. **LISTEN remains English in the final comment box and bottom caption**, as requested. English teaching examples are separate from Persian captions; the first listening example intentionally withholds its text.

The chosen Opuscar marker style is sourced from upstream commit `3a7132b996be0241c1ea0ab180d519f06e6f10b6`. This is a portrait adaptation, with joined Persian type on a separate matte-paper caption slip. Native Kalam lettering, black/blue/red semantics and minimal drawings are retained. No score, chalk, keyboard or generic transition pack has been added.

Rebuild with existing Chromium, FFmpeg, Node/playwright-core and an Opuscar Python containing NumPy, SciPy and SoundFile:

```bash
OPUSCAR_PYTHON=/workspace/lemo-opuscar/.venv/bin/python bash films/connected-speech-marker/tools/build.sh
```

Override PLAYWRIGHT_CHROME if required. The build exports rendering events, creates the mix, renders 1392 frames and muxes the versioned MP4. Fonts and glyph skeletons are included. Temporary renders/WAVs are ignored. `review.html` is the historical three-frame preproduction gallery, not the film.

See QC.json and analysis/production-* for actual checks and their limits. Representative frames and transitions were inspected; no independent real-time listening review is claimed. Captions are phrase-aligned from script and source pauses, not a manually audited word-level transcript. See CREDITS.md and licenses/ for attribution.

## Real-footage edition

A separate [real-footage revision](real-footage/README.md) uses the supplied movie picture and actor sound twice, first without captions, then with English captions. The later lesson captions are white on charcoal. Export: `../../video/connected-speech-real-footage-v1.mp4` (60.375 seconds). Original illustrated v1 is preserved.
