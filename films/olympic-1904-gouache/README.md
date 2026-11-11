# 1904 Olympic marathon — completed gouache film, v3

[Download the complete film (1080×1920 MP4)](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/main/video/olympic-1904-final-v3.mp4) · [Hicks and recap-transition preview](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/main/video/olympic-1904-hicks-v3.mp4) · [Encoded-frame contact sheet](preview-hicks-v3.jpg)

**123⅔ seconds, 30 fps, 3,710 frames.** This revision adds three distinct moving Hicks compositions, removes the repeated championship sentence after **They kept him going**, and makes the action/teaching sound effects substantially more audible. Persian-only subtitles remain synchronized to the edited narration. **No background music.**

## Three new Hicks shots

| Output time | Picture and motion |
|---|---|
| 74.733–81.000 s | Close-up of the exhausted, thirsty Hicks with an empty bottle; slow camera push, restrained breathing sway and drifting dust |
| 81.000–85.133 s | Subjective view of the seemingly endless road despite the nearby finish; slow tilt/push and small landscape-only heat shimmer |
| 85.133–91.633 s | Three-quarter side view of trainers supporting Hicks through the finish; lateral camera track, loose-ribbon motion and dust |

The olive singlet, terracotta trim, tousled light-brown hair and thin moustache preserve Hicks's identity. The top title area is kept separate from the scene. At 91.633 seconds, the English example now leads directly into **حالا دقت کردی؟**, with a short trailing celebration and transition whoosh. The earlier sentence saying that he reached the finish and won is retained.

The original Olympic opening from v2 is preserved: venue cut at 3.60 seconds, exhausted nonfinishers at 7.30 seconds, then Félix at 10.40 seconds. Earlier sound bridges remain, including the approaching engine before the car appears and applause trailing across the officials' reveal.

## Exact sentence removal

Only original source time **91.633333–93.966667 s** is removed: the second **و بالاخره قهرمان شد!** and its surrounding pause. That is exactly **70 video frames / 112,000 audio samples**, reducing the film by 2⅓ seconds. Both cut points fall in quiet gaps. No retained narrator sample is normalized, faded or played at a different speed.

| Output time | Original recording time |
|---|---|
| 0–91.633333 s | Same time |
| 91.633333–123.666667 s | Output time + 2.333333 s |

`hicks-v3.js` maps the edited clock back to the existing source timeline, so later captions, vocabulary highlights, teaching animation and PHRASAL typing all advance together. The duplicate caption/title is skipped. The original 0.456125-second silent ending hold remains. [Audio edit and source map](audio-edit-v3.json).

## More audible sound design

[**SFX Kit by Wyzowl**](https://github.com/wyzowl/sfx-kit) supplies eleven selected **CC0-1.0** assets: three whoosh variants, coin drop, scissors, page turn, chalk drawing, pencil drawing/writing and keyboard letter/return. The files, their hashes, source revision and metadata are committed under `assets/sfx-kit/`; the CC0 text is under `licenses/`.

The kit's `sync.at` places each event at **visual moment − sync.at**. Each asset uses its specified `under_voiceover_db` rather than the previous heavy global duck. Short writing excerpts receive fades and level compensation after trimming. Keyboard peaks meet the actual frame on which each typed letter appears. Ten selected scene changes receive short whooshes; caption-only changes do not.

Gravel footsteps and the period-car engine/stall are synthesized separately, since the kit does not contain those actions. They have stronger audible transients and midrange detail for phone speakers. Coins, writing strokes and keys now use the kit assets over the quieter existing Foley. Existing material receives a restrained 6 dB lift; new effects are mixed by event rather than raising a continuous ambience bed.

Speech remains in front: effect RMS is limited below active speech, each asset ducks locally, and a final headroom guard changes **effects only**. The narrator's gain is unchanged. There are no musical stings, drones or background music. [Sound design, events and same-window level comparisons](sound-design-v3.json).

## Assembly and checks

[Latest manifest](revision-v3.json) records the edited blocks. Only the **70–97.666667-second** patch is rendered again. All **2,100 decoded pictures before 70 seconds** match v2, including its approved opening. The last **780 pictures** match original source time 100–126 seconds, shifted earlier by the removed sentence. Audio is assembled as continuous PCM and encoded to AAC once; source review-clip AAC is discarded before picture concatenation.

[Browser checks](layout-QC-hicks-v3.json) inspect all 830 patch frames, verify three new shots with visible motion, caption safe regions, 28 later caption starts, the direct transition after the English sentence, all ten shifted vocabulary highlights, final PHRASAL and deterministic seeking.

[Delivered-file QC](QC-revision-v3.json) checks full decoding, black intervals, duration/frame count, unchanged picture regions, exact retained narrator samples, waveform timing around edits and joins, encoded loudness/true peak, speech/effect separation, increased Foley levels and the kit assets' hashes/sync points. The delivered file measures **−13.33 LUFS / −1.67 dBTP**; all nineteen encoded waveform checks report zero sample lag. Selected encoded frames are inspected visually. No independent listening review was performed; audibility comparisons are waveform measurements, not a listening test.

Captions retain the existing script/ASR/pause alignment. Continuous-speech splits remain estimates rather than independently verified word-level timing. English examples appear in teaching headlines or on the board; bottom subtitles remain Persian.

## Rebuild

From the configured repository root:

```bash
bash films/olympic-1904-gouache/build-v3.sh
PLAYWRIGHT_CHROME=/usr/bin/chromium LEMO_ANGLE=swiftshader node films/olympic-1904-gouache/check-hicks-v3.mjs
/workspace/lemo-opuscar/.venv/bin/python films/olympic-1904-gouache/verify_revision_v3.py
```

Set `FILM_PYTHON` if the prepared Python environment path differs. The build uses the committed assets and later review videos, canonical voice master, Chromium and FFmpeg. It rebuilds missing v2 intermediates if required, makes a fresh edited voice/Foley base, applies the louder sound pass, renders the Hicks patch, and exports the full film plus an 18.9-second Hicks/transition preview. No image-generation API or transcription model is required.

`build-v2.sh` and `build.sh` retain the earlier versions with explicit `edit=v2` / `edit=original` renderer queries. `segments.json` retains the original thirteen review intervals and points to this latest revision. [Completed v2](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/main/video/olympic-1904-final-v2.mp4), [v2 QC](QC-revision-v2.json), v1 and earlier review files remain available. WAVs, raw renders, logs and temporary frame extracts remain ignored under `out/`.

## Style and provenance

The film adapts Lemo-Opuscar's **Welsh Valley Gouache**, Opuscar98 entry 14: opaque directional paint, pale-gold light, olive fields, coal/slate ridges and perspective roads. Painted assets, including the three new Hicks compositions, were generated for this project with the image-generation tool. Camera motion, dust, heat shimmer, ribbon/flag accents, wheels, text, chalk highlights and typing are rendered in Canvas/HTML. The scenes are illustrative, not archival reconstructions or exact portraits; motion is painterly rather than full anatomical character animation. User narration, existing font licenses and the renderer's MIT credits remain retained.
