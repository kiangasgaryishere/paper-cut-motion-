# 1904 Olympic marathon — completed gouache film

[Download the complete film (1080×1920 MP4)](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/main/video/olympic-1904-final-v1.mp4) · [Encoded-frame contact sheet](preview-through-126s.jpg)

**Complete: 2 minutes 6 seconds, 30 fps, 3,780 frames.** All of the uploaded **running.mp3** is included, through its decoded end at 125.543875 seconds. A 0.456125-second silent tail holds the completed comment prompt to 126 seconds; no narration is cut, stretched or faded. Narration and Persian-only subtitles accompany the painted illustrations and restrained procedural sound effects. **No background music.**

The first forty seconds are the approved material from the incremental reviews. The remaining narration, story, English examples, recap, explanation, practice preview and final **PHRASAL** comment prompt are now finished. The previous request to proceed one part at a time was superseded by the user's request to complete the entire video; no narration remains to be produced.

## Story and teaching beats

| Recording time | Content |
|---|---|
| 0–40 s | Approved opening; Félix, travel fund and gambling loss; clothing, tailor scissors, spoiled apples and roadside rest |
| 40–50 s | Félix's fourth-place result; Fred Lorz introduced with a calf cramp; **He dropped out** |
| 50–64 s | A period car picks Fred up; the car breaks down; he gets out and runs again |
| 64–75 s | Fred reaches the stadium; officials discover the car shortcut; **They found out** |
| 75–85 s | Thomas Hicks, exhaustion and the imagined twenty miles despite the nearby finish |
| 85–94 s | Trainers support Hicks across the ribbon; **They kept him going**; the real winner |
| 94–108 s | Ten useful expressions, highlighted individually as spoken, with Persian meanings |
| 108–116 s | Multiword-verb explanation using **GET + OUT → GET OUT**, with contextual Persian meaning |
| 116–122 s | Weekly story/voice/speaking practice and sample fill-in exercises |
| 122–126 s | **PHRASAL** types into the comment box; final invitation and a readable end hold |

The car and rear-view runner travel along the road into depth. Wheel accents stop at the breakdown, smoke rises briefly, and the passenger is removed from the car asset when Fred exits. Fred has an ivory shirt/navy band and no cap; Hicks has an olive singlet with terracotta trim; Félix retains his terracotta shirt, cap and cut shorts. The officials and finish scenes are symbolic painted illustrations, not archival reconstructions or exact portraits.

Motion is deliberately limited and painterly: camera tracks/pushes, running poses, vehicle travel, short wheel/smoke actions, falling fabric, chalk highlights and typing. It is not full anatomical character animation. The first forty-second review versions and every separate part remain in `video/` for comparison.

## Voice and caption timing

The full supplied recording is mastered once by `prepare_voice.py`. Every review part slices the same canonical 48 kHz master, whose waveform-file hash is checked before later mixes are built. There is no per-part narration normalization or narration edge fade.

Captions use the supplied script, local Whisper segments and detected pauses. Raw ASR errors in names, spelling and numerals were corrected from the script; a failed automatic segment was recovered with an overlapping transcription. Continuous-speech caption splits remain estimates, rather than independently verified word-level alignment. English example sentences appear in the teaching headline or on the board; bottom subtitles remain Persian. The useful-expression list follows the supplied narration.

`finish-data.json` contains the remaining absolute scene/caption times and ten recap highlights. Earlier cues are retained in `captions-part01.json` through `captions-part04.json`. No independent listening review was performed; validation includes waveform timing checks and visual inspection of encoded frames.

## Assembly and completion

`segments.json` is the source of absolute recording intervals, audio sample offsets and video frame offsets. The first twelve review parts are ten seconds each; the final review part is six seconds. Only the final part includes silent padding beyond the actual recording end.

`mix_part01.py` through `mix_part04.py` retain the approved initial mixes. `mix_finish.py` builds one continuous nonmusical effects mix for the remainder, applies speech-aware ducking and limits effect RMS under active speech, then slices it into review windows. Effects include cloth, scissors, apple/grass sounds, a period-car engine/stall, footsteps, short applause, chalk, paper, typing and send accents.

`encode_finish.py` extracts accurate frame windows from a continuous 40–126-second picture render. `assemble.py` copies all picture streams and encodes the continuous PCM narration/effects mix to AAC once. It removes review-clip AAC streams before video concatenation to prevent encoder priming from shifting the copied picture. Both final streams start at zero; no audio is concatenated in encoded AAC form.

The page previews the complete **0–126 s** timeline. Renderer query parameters `?start=40&end=126` select the remainder. `part02.js` through `part04.js` and `finish.js` extend `renderAbsolute` without replacing the original scene functions.

## Final validation

[Final MP4 QC](QC-through-126s.json) confirms:

- 126 seconds / 3,780 frames; full H.264/AAC decoding passed, no detected black interval.
- **All 1,200 decoded pictures in the approved first forty seconds remain identical**, and its PCM mix prefix is unchanged.
- Zero measured sample lag against the continuous mix in windows spanning **all twelve joins** and in the final CTA. No repeated/missing timeline samples.
- Entire canonical narration included, with only 0.456125 seconds of final silence added for the ending hold.
- Final encoded loudness **−13.40 LUFS**, true peak **−2.32 dBTP**.
- At least **19.11 dB** measured speech/effects separation in active 100 ms windows across the newly completed material.

[Remaining-scene layout checks](layout-QC-finish.json) sample 860 frames, check all 43 new caption starts, confirm all ten recap highlights and the complete **PHRASAL** keyword, and verify deterministic seeking back to the opening. Earlier layout and road checks remain in their versioned QC files. Selected encoded frames were visually inspected, including road travel, character identity, teaching text and the final prompt.

The finished file is approximately 61 MB and is tracked directly for a working raw GitHub download; no LFS pointer is used. The previous [40-second assembly](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/main/video/olympic-1904-40s-v1.mp4) and older reviews remain available.

## Rebuild

After the existing repository setup, run from its root:

```bash
bash films/olympic-1904-gouache/build.sh
```

Set `FILM_PYTHON` if needed. The build uses the repository virtual environment or the prepared `/workspace/lemo-opuscar/.venv`, configured Chromium and FFmpeg. It prepares the voice, renders the initial windows and continuous remainder, exports review parts and assembles the final movie. All painted assets are committed; no image-generation API or transcription model is required to rebuild the included timeline.

Useful checks:

```bash
node films/olympic-1904-gouache/check-finish.mjs
python films/olympic-1904-gouache/verify_assembly.py
```

Use the same browser/Python configuration as the build. WAVs, raw picture renders, intermediate extracts and frame references live in ignored `out/` folders. `alignment/` retains optional analysis evidence. Rebuilding on a different audio-toolchain version may require checking the canonical master hash rather than silently changing the voice level between parts.

## Style and provenance

The film adapts Lemo-Opuscar's **Welsh Valley Gouache**, Opuscar98 entry 14: opaque directional paint, golden side-light, olive fields, coal/slate ridges and true-perspective roads. The character, landscape, car, officials, Hicks, finish and study-board paintings were generated for this project using the image-generation tool. Text, camera motion, wheel accents, smoke, chalk, rank graphics and typing are rendered programmatically in Canvas/HTML. The uploaded narration remains the user's project material. Existing font licenses under `licenses/` and the Lemo-Opuscar renderer's MIT credits are retained.
