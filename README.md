# A / THE — Paper-cut motion reel

A 19-scene vertical film explaining English articles through the 1066 succession story, with the supplied Persian narration, Persian/English captions and procedural sound effects. **No background music.**

[Download the video (MP4)](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/main/video/a-the-kings-v1-review.mp4)

[View the 19-frame storyboard](films/a-the-kings/STORYBOARD-v2-19-frames.jpg) · [Director’s plan (Persian)](films/a-the-kings/DIRECTORS-PLAN.fa.md)

## Version status

This is the **first motion review**, not a publication-ready master. Caption timing is an editorial estimate and has not been verified against the spoken words. The intended voice/caption lead is 0.5 seconds before the related visual reveal. The artwork is original vector paper illustration, not archival photo collage. Source narration is included unchanged; mastering adjusts its level.

The delivered MP4 is 1080×1920, 24 fps, 72.75 seconds, H.264/AAC. Full decoding and black-frame checks passed. Final measured loudness: −14.2 LUFS; true peak −1.4 dBFS. See [QC](films/a-the-kings/production/QC.json) and [review notes](films/a-the-kings/production/REVIEW.fa.md).

## Run and rebuild

Prerequisites: Node 20+, Python 3.11+, FFmpeg 7+ (with ffprobe), and Chromium. On Linux the default browser path is `/usr/bin/chromium`; set `PLAYWRIGHT_CHROME` to another installed browser if required. `LEMO_ANGLE=swiftshader` uses software rendering.

```bash
bash setup.sh
bash films/a-the-kings/production/build.sh
```

The build writes `video/a-the-kings-v1-review.mp4`. Run from an existing checkout; a separate Git worktree is unnecessary. Rendering can take several minutes. Dependencies and intermediate WAV/frame files are ignored; the finished MP4 is tracked for direct download.

`production/index.html` and `data.js` contain the current motion and artwork. `captions.json` contains the provisional bilingual cues; `mix.py` builds the sound mix. Earlier storyboard generators and boards are retained as design history; do not run them over the current motion page. The prepared production files rebuild without regenerating the storyboard.

## Credits

Shared renderer and SFX adapted from [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar), revision `143f387ad774525dc9abc0ff05fb5f4bfbaa5f02`, MIT. Copyright and font licenses are in `licenses/`. User-supplied script and narration remain project materials; no license for redistribution of those materials is granted by the toolkit license. No API credentials are required for rendering or procedural SFX.
