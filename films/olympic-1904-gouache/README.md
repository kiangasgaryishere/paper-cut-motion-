# 1904 Olympic marathon — part 01, revision 2

[Download the revised first 10 seconds](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/main/video/olympic-1904-part01-v2.mp4) · [Preview](preview-part01-v2.jpg)

Portrait 1080×1920, 30 fps, exactly 300 frames. This revision adds the supplied **running.mp3** narration and makes the runners travel **along the painted road into depth**, with rear three-quarter running poses and distance-dependent scale. The background and running figures share one camera transform; the figures no longer run sideways across the road.

The original recording's absolute interval **[0,10 seconds)** supplies the narration. No speed change, narration fade or repeated audio at a part boundary. Speech has priority over the restrained outdoor/footstep effects; no music.

| Recording time | Direction / speech |
|---|---|
| 0–3.367 s | Wide view with the opening “کمدی‌ترین مسابقهٔ تاریخ المپیک!” |
| 3.367–5.867 s | Closer view following the road; 1904 American Olympics |
| 5.867–10 s | Marathon view; the line about eighteen runners not finishing |

Félix's introduction begins around **10.45 seconds** in this recording, so his close-up belongs to the next part. The revised first part does not introduce him early or jump ahead to his clothing story. The original ten-second style test did preview that later material.

## Ten-second production and final assembly

`segments.json` records the absolute source intervals, audio sample offsets and video frame offsets. Part 01 is source samples `[0,480000)` at 48 kHz and video frames `[0,300)` at 30 fps. **The next part starts at recording time 10.000 seconds.** Future parts are produced only as requested.

`prepare_voice.py` masters the entire supplied recording once, using gentle presence treatment, compression and two-pass loudness normalization. Every part must slice that same canonical master, rather than normalize narration separately per part. Its waveform hash is recorded in `QC-part01-v2.json` to make unintended master changes detectable.

For final assembly, join the picture parts at their exact frame boundaries and encode the continuous narration plus the sound effects once. Avoid concatenating independently encoded AAC streams, whose priming/padding can introduce gaps. Per-part effects may have short fades; narration must remain continuous.

## Validation

The delivered file fully decodes, contains exactly ten seconds / 300 frames, and has no detected black interval. Encoded narration timing matches the master at sampled windows beginning at 1, 4 and 7 seconds with **zero sample lag**. The master also retains the pre-master recording's time origin in those windows. Final loudness is **−13.52 LUFS**, true peak **−2.46 dBTP**. The minimum measured speech/effects separation in active 100 ms windows is **22.19 dB**.

`motion-layout-QC-v2.json` checks 301 timeline samples and 2,107 runner positions: feet remain inside an independently traced corridor on the dirt track while on the visible path; movement aligns with the road tangent and scale decreases with depth. The three encoded shot references were visually inspected. Checks do not establish a fluid anatomical run cycle; the painted four-pose animation remains deliberately limited.

Captions use the supplied script, local Whisper segment estimates and detected pauses. ASR errors in spelling/numerals were corrected from the script. The first caption starts at the recording origin; later captions lead detected phrase onsets by roughly 36–50 ms. These are phrase-level cues, not independently verified word-level alignment. No independent listening review was performed.

## Rebuild

After the repository's existing setup, run from its root:

```bash
bash films/olympic-1904-gouache/build.sh
```

Set `FILM_PYTHON` if the Python environment is elsewhere. The script uses the repository virtual environment or the prepared `/workspace/lemo-opuscar/.venv`. Optional local transcription analysis is in `alignment/transcribe.py`; the model is not needed to render the included captions.

Checks:

```bash
node films/olympic-1904-gouache/check-part01-v2.mjs
python films/olympic-1904-gouache/verify_part01.py
```

Use the configured Chromium and Python environment as in the build. Intermediate WAVs and render frames are ignored by Git; they are recreated from the committed source MP3 and assets.

## Style and provenance

The project adapts Lemo-Opuscar's **Welsh Valley Gouache**, Opuscar98 entry 14: opaque painterly textures, gold light, olive fields and coal/slate darks. This is a stylized illustration, not an archival reconstruction or an exact portrait of Félix.

`stadium.png`, `felix.png`, `runners.png` and the revised `runners-rear-v2.png` were generated for this project with the image-generation tool. The user's supplied `assets/narration.mp3` is the recording source. The existing font and licenses under the repository's `licenses/` are retained. Shared rendering utilities are from Lemo-Opuscar (MIT).

[Original unvoiced style test (v1)](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/main/video/olympic-1904-gouache-test-v1.mp4) · [Original keyframes](preview.jpg). Its page is retained as `index-v1.html`; the default page and build now target part 01 revision 2.
