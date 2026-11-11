# 1904 Olympic marathon — completed gouache film, v2

[Download the complete film (1080×1920 MP4)](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/main/video/olympic-1904-final-v2.mp4) · [Watch only the revised first ten seconds](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/main/video/olympic-1904-opening-v2.mp4) · [Encoded-frame contact sheet](preview-revision-v2.jpg)

**2 minutes 6 seconds, 30 fps, 3,780 frames.** All of the uploaded **running.mp3** is included, through its decoded end at 125.543875 seconds. A 0.456125-second silent tail holds the completed comment prompt to 126 seconds. Persian-only subtitles accompany the painted illustrations and narrator-first sound effects. **No background music.**

## Revised opening and editorial sound bridges

The opening now cuts to two distinct painted compositions rather than repeatedly reframing the same stadium:

| Recording time | Picture and motion |
|---|---|
| 0–3.60 s | Original hook; the Olympic sentence begins over the outgoing hook |
| 3.60–7.30 s | New 1904 St Louis stadium entrance, tracking/pushing camera, waving American flag, nine rear-view runners following the road into depth; marathon accent appears on its spoken cue |
| 7.30–10.40 s | New exhausted-runner foreground, independently tracking valley, restrained breathing motion, animated **۱۸** emphasis and exactly eighteen pigment tally marks |
| 10.40 s onward | Félix and the rest of the completed story |

The two new narrative J-cuts let the incoming sentence begin before its picture, while captions retain their original relationship to the voice. Stadium applause starts before the entrance cut and trails onto the exhausted runners. A period engine is heard 0.80 seconds before the car appears. Fred's applause continues 0.68 seconds into the officials' reveal; Hicks's celebration continues about 0.56 seconds into the recap. These are short sound bridges, not a continuous music bed. See [absolute sound/visual timings](sound-bridges-v2.json).

Bottom captions remain Persian-only. The new title area has clear space above the scene. The US flag is confined to the Olympic venue; no modern Olympic rings are added to a 1904 setting. The eighteen tally marks emphasize the narrated number; the three illustrated resting men are representative, not a claim that only three people stopped.

## Complete story

| Recording time | Content |
|---|---|
| 0–10 s | Olympic hook, St Louis 1904, eighteen nonfinishers |
| 10–40 s | Félix, gambling loss, clothing and scissors, spoiled apples and roadside rest |
| 40–50 s | Félix's fourth place; Fred Lorz, calf cramp; **He dropped out** |
| 50–64 s | Car pickup, breakdown, getting out and running again |
| 64–75 s | Stadium arrival; officials discover the shortcut; **They found out** |
| 75–94 s | Thomas Hicks, exhaustion, imagined distance, assisted finish and championship |
| 94–108 s | Ten expressions highlighted as spoken with Persian meanings |
| 108–116 s | **GET + OUT → GET OUT** and a contextual Persian explanation |
| 116–126 s | Story/voice/speaking practice, sample exercises, typed **PHRASAL** comment prompt and ending hold |

The car and rear-view runners follow the road into depth. Fred's passenger disappears after he gets out. Character identities remain distinct. The scenes are symbolic painted illustrations, not archival reconstructions or exact portraits. Motion combines camera tracks/pushes, running poses, vehicle travel, smoke, falling fabric, paint accents, chalk and typing; it is not full anatomical character animation.

## Voice and timing

`prepare_voice.py` masters the entire recording once. The canonical 48 kHz waveform hash is checked before mixing. Narration is not cut, stretched, moved, repeated or faded at review-part boundaries. `mix_revision_v2.py` retains the existing Foley and adds the sparse sound bridges, then applies speech-aware ducking and an overlapping-window effect limiter. The continuous full mix is encoded to AAC once.

Captions use the supplied script, local Whisper segments and detected pauses. ASR errors in names, spelling and numerals were corrected against the script; an automatic transcription failure was recovered with an overlapping transcription. Continuous-speech caption splits remain estimates rather than independently verified word-level alignment. English examples appear in teaching headlines or on the board; bottom subtitles remain Persian. No independent listening review was performed; validation includes waveform checks and encoded-frame visual inspection.

## Assembly and validation

[Version 2 manifest](revision-v2.json) records the delivery blocks. Only the first twenty seconds are rendered again to accommodate the new 3.60/7.30/10.40-second cuts. All **3,180 decoded pictures from 20 seconds through the ending remain identical** to the completed v1. `assemble_revision_v2.py` removes AAC from source picture blocks, copies the picture packets and encodes the continuous PCM audio once, avoiding individual AAC priming gaps.

[Opening layout checks](layout-QC-opening-v2.json) inspect all 600 frames of the first twenty seconds, check Persian captions, foreground/caption separation, both narrative J-cuts, the number eighteen, forward movement along the road, and deterministic seeking. [Delivered MP4 checks](QC-revision-v2.json) cover duration, frame count, complete decoding, black intervals, unchanged later pictures, canonical narration, waveform lag around the edits/joins, speech/effect separation and encoded loudness/true peak. The ten-second preview is checked separately for exact duration and frame count. The delivered movie measures **−13.40 LUFS / −2.32 dBTP**; measured speech/effect separation stays at least **19.11 dB** in active speech windows. All eighteen encoded waveform checks report zero sample lag.

The full movie is tracked directly for a working raw GitHub download, without an LFS pointer. [Completed v1](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/main/video/olympic-1904-final-v1.mp4), [its QC](QC-through-126s.json), the earlier incremental assemblies and all review parts remain available. `segments.json` retains those original thirteen review intervals and points to the latest revision manifest.

## Rebuild

After the repository setup, run from its root:

```bash
bash films/olympic-1904-gouache/build-v2.sh
```

The build uses Chromium, FFmpeg, the prepared Python environment and the committed painted assets. Set `FILM_PYTHON` if the environment path differs. It reuses the committed later review videos, regenerates missing canonical Foley WAVs, renders the opening and assembles the complete v2 and ten-second preview. No image-generation API or transcription model is needed to rebuild this timeline.

```bash
PLAYWRIGHT_CHROME=/usr/bin/chromium LEMO_ANGLE=swiftshader node films/olympic-1904-gouache/check-opening-v2.mjs
/workspace/lemo-opuscar/.venv/bin/python films/olympic-1904-gouache/verify_revision_v2.py
```

`build.sh` rebuilds the original v1 using `edit=original` for its opening windows. `segments.json`, `mix_part01.py` through `mix_part04.py`, `mix_finish.py`, `encode_finish.py`, `assemble.py` and `verify_assembly.py` retain the original incremental workflow. Raw pictures, WAVs, logs and temporary frame extracts are ignored in `out/`. Different audio-toolchain versions should check the canonical waveform hash before replacing narration.

## Style and provenance

The film adapts Lemo-Opuscar's **Welsh Valley Gouache**, Opuscar98 entry 14: opaque directional paint, golden side-light, olive fields, coal/slate ridges and true-perspective roads. The character, landscape, stadium entrance, exhausted runners, car, officials, Hicks, finish and study-board assets were generated for this project using the image-generation tool. Text, camera motion, flag animation, wheels, smoke, chalk, rank graphics and typing are rendered in Canvas/HTML. The uploaded narration remains the user's project material. Font licenses under `licenses/` and the Lemo-Opuscar renderer's MIT credits are retained.
