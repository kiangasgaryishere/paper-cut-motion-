# 1904 Olympic marathon — cumulative video through 20 seconds

[Download the combined 20-second video](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/main/video/olympic-1904-20s-v1.mp4) · [Preview](preview-through-20s.jpg)

Two ten-second parts, portrait 1080×1920 at 30 fps. The uploaded **running.mp3** supplies the original absolute recording interval **[0,20 seconds)**. No narration speed change, repeated audio or narration fade at a part boundary. Speech has priority over the restrained sound effects; **no background music**.

**Delivery preference:** after every requested ten-second addition, append it to the previous parts and deliver the updated cumulative video. Retain the separate part for review. The next part starts at **20.000 seconds** of the same recording. Do not produce the remainder until requested.

| Recording time | Direction / speech |
|---|---|
| 0–10 s | Approved marathon opening, 1904 context, eighteen runners not finishing; rear-view runners follow the painted road into depth |
| 10–10.4 s | Road motion continues through the narration pause |
| 10.4–13.7 s | Félix introduced in his terracotta shirt and long trousers at the stadium |
| 13.7–15.967 s | Cuban harbor, steamship and a small travel fund accumulating |
| 15.967–18.267 s | Gambling table; three coins leave the frame and the purse stays empty |
| 18.267–20 s | Gentle emphasis on the empty purse and **He ran out of money!**, with Persian translation below |

The harbor, table, empty purse and hand are symbolic painted story illustrations, not an archival reconstruction. Félix retains the same generated portrait across his introduction and travel scene.

Separate review files:

- [Part 01, source 0–10 s](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/main/video/olympic-1904-part01-v2.mp4)
- [Part 02, source 10–20 s](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/main/video/olympic-1904-part02-v1.mp4)
- [Original unvoiced style test](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/main/video/olympic-1904-gouache-test-v1.mp4), retained as design history; its page is `index-v1.html`.

## Continuous timeline and assembly

`segments.json` records absolute recording time, source sample offsets, frame offsets and the cumulative delivery preference. At 48 kHz / 30 fps, each ten-second part contains **480,000 narration samples / 300 picture frames**. Part 02 starts at source sample 480,000 and frame 300; the next part starts at sample 960,000 and frame 600.

`prepare_voice.py` masters the entire recording once. Every part slices that same canonical master; narration is never independently normalized per part. `mix_part01.py` and `mix_part02.py` build narrator-first PCM mixes with effects-only edge fades. The canonical master's hash must match the approved first part before producing later mixes.

`assemble.py` joins the part mixes into one continuous PCM timeline and encodes AAC **once** for the combined video. It copies the picture streams, preserving the approved first part. Review-clip audio streams are removed before the video concat step so AAC encoder priming cannot shift the copied picture. Both final streams start at exactly zero.

The root page now previews the absolute **0–20 s** timeline. Render windows are `?start=0&end=10` and `?start=10&end=20`; `part02.js` extends the first-part drawing without replacing its scene functions. Later additions should extend `renderAbsolute`, maintain absolute cue times and append a manifest entry.

## Validation and timing limits

[Combined-file QC](QC-through-20s.json) verifies 20 seconds / 600 frames, full decoding, no detected black interval and identical decoded pictures for **all 300 approved first-part frames**. The first 480,000 PCM mix samples are also unchanged. Audio timing checks, including a window spanning the join at 10 seconds, found **zero sample lag** against the continuous mix. Video/audio start times are both zero.

Final combined loudness is **−13.91 LUFS** and true peak **−2.41 dBTP**. Minimum measured speech/effects separation during active 100 ms windows in part 02 is **21.02 dB**. [Layout checks](layout-QC-part02.json) cover 300 new frames and the four caption-start frames; heading/kicker spacing is checked using actual glyph ink bounds rather than the font's oversized line box. Encoded reference frames were visually inspected. No independent listening review was performed.

[First-part road checks](motion-layout-QC-v2.json) retain their 301 timeline samples / 2,107 runner positions; the rear three-quarter poses move along the road and shrink with depth. The painted run cycle remains deliberately limited, rather than fluid full character animation.

Captions are Persian-only; the English phrase appears in the teaching headline. Cue timing uses the supplied script, local Whisper segment estimates and detected pauses. Raw ASR spelling/numeral errors were corrected from the script. This is phrase-level timing, not independently verified word-level alignment. First-part timing is in `captions-part01.json`, second-part timing in `captions-part02.json`.

## Rebuild

After the repository setup, run from its root:

```bash
bash films/olympic-1904-gouache/build.sh
```

Set `FILM_PYTHON` if needed; the build uses the repository virtual environment or the prepared `/workspace/lemo-opuscar/.venv`. The build prepares the canonical voice, renders both windows, exports the separate clips and assembles the cumulative video. It reuses the committed painted assets; no image-generation API is needed to rebuild.

Relevant checks:

```bash
node films/olympic-1904-gouache/check-part01-v2.mjs
node films/olympic-1904-gouache/check-part02.mjs
python films/olympic-1904-gouache/verify_assembly.py
```

Use the configured Chromium and Python environment as in the build. Intermediate WAVs, picture-only extracts and frames live in ignored `out/` folders. They are recreated from the committed narration and assets. Local transcription models are optional analysis tools and are not needed for rendering.

## Style and provenance

The project adapts Lemo-Opuscar's **Welsh Valley Gouache**, Opuscar98 entry 14: opaque directional paint marks, gold light, olive fields and coal/slate darks. This is stylized illustration, not an exact historical portrait.

The stadium, Félix, running-pose sheets, harbor and empty-purse table paintings were generated for this project with the image-generation tool. The small moving coins are procedural painted marks attached to their surfaces. `assets/narration.mp3` is the user's uploaded recording. Existing font licenses under the repository's `licenses/` remain in force. Shared renderer: Lemo-Opuscar (MIT).
