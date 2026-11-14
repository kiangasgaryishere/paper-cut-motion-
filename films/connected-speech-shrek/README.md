# Connected Speech — Shrek + Mummy edition

A new **87-second, 1080×1920 / 24fps** film from the newly supplied script, shrek.mp3, shrek1.mp4 and shrek2.mp4. Previous versions remain intact.

The opening jumps into Donkey's first sentence and Shrek's reaction, freezes, plays the actual frames in reverse and repeats only the first Donkey sentence. Both opening listens withhold English subtitles. The complete Shrek2 file is retained for the later captioned payoff. The Mummy appears first uncaptioned, then with “Honey, whatcha doing?” captions. Supplied movie audio is used for all screenings; the new voice's explicit full/reduced-form teaching readings remain as provided.

Blue and red marker ink now carry titles, word forms, links and heard targets, with black mainly scaffolding. This is a user-requested palette-weight adaptation of Lemo Marker on Paper, not a claim of strict original black-heavy colour grammar. The Persian caption box moves up **50px** (bottom 270px); movie captions move to bottom 290px. Main diagram content remains above captions.

The new narration is 69.485708 seconds at the final 48kHz decode clock. All its words are retained without speed changes. Only 47.5–48.875s of measured silence is removed. The last narration tail overlaps the ambient first half-second of the full Shrek clip, ending well before its actor dialogue. timeline.json contains every source/output frame mapping, including freeze, reverse and replay. No added music; film audio, native marker/paper foley and a short tape-scrub effect only.

## Build and dependencies

Existing Opuscar/Chromium/FFmpeg/Python dependencies are reused. Native engine/fonts/glyphs and the authorized Mummy clip are shared with ../connected-speech-marker. Generated JPEG frames and temporary WAVs/renders remain in ignored out/. A 12-frame image cache makes deterministic movie playback memory-bounded.

```bash
bash films/connected-speech-shrek/tools/build.sh
```

Use OPUSCAR_PYTHON and PLAYWRIGHT_CHROME to select existing runtimes. Output: `video/connected-speech-shrek-v1.mp4`. Review frames, storyboard, source analysis and QC evidence are included. Captions are phrase-level script/ASR/pause estimates, not an independently audited word-level transcript; no real-time listening review is claimed.
