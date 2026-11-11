# A / THE — Paper-cut motion reel

A 19-scene vertical film explaining English articles through the 1066 succession story, with the supplied Persian narration, Persian-only captions and procedural sound effects. **No background music.**

[Download the video (MP4)](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/main/video/a-the-kings-v7.mp4)

[View the revised keyframes](films/a-the-kings/production/keyframes-v7.jpg) · [Director’s plan (Persian)](films/a-the-kings/DIRECTORS-PLAN.fa.md)

## Version status

This is the **seventh motion version**. Phrase timing now uses Whisper speech segments refined against pauses in the recording, replacing the first version’s estimated scene table. Captions lead their detected phrase onset by approximately 23–53 ms at 30 fps. Visual changes follow narration rather than a fixed 0.5-second delay. Some continuous-speech boundaries remain approximate; independent listening review has not been performed. The artwork is original vector paper illustration, not archival photo collage. The user-approved 79.1-second narration prefix is included without retiming; extra unscripted speech after the CTA was removed by approval, and mastering adjusts its level.

The delivered MP4 is 1080×1920, 30 fps, 79.1 seconds, H.264/AAC. Full decoding and black-frame checks passed. See [version 7 review notes](films/a-the-kings/production/REVIEW-v7.fa.md) and [QC](films/a-the-kings/production/QC-v7.json). The first version remains in `video/a-the-kings-v1-review.mp4` for comparison.

## Run and rebuild

Prerequisites: Node 20+, Python 3.11+, FFmpeg 7+ (with ffprobe), and Chromium. On Linux the default browser path is `/usr/bin/chromium`; set `PLAYWRIGHT_CHROME` to another installed browser if required. `LEMO_ANGLE=swiftshader` uses software rendering.

```bash
bash setup.sh
bash films/a-the-kings/production/build.sh
```

The build writes `video/a-the-kings-v7.mp4`. Run from an existing checkout; a separate Git worktree is unnecessary. Rendering can take several minutes. Dependencies and intermediate WAV/frame files are ignored; the finished MP4 is tracked for direct download.

`production/index.html` and `data.js` contain the current motion and artwork. `captions.json` contains the speech-anchored Persian-only cues; `mix_v7.py` builds the sound mix. Earlier storyboard generators and boards are retained as design history; do not run them over the current motion page. The prepared production files rebuild without regenerating the storyboard.

## Credits

Shared renderer and SFX adapted from [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar), revision `143f387ad774525dc9abc0ff05fb5f4bfbaa5f02`, MIT. Copyright and font licenses are in `licenses/`. User-supplied script and narration remain project materials; no license for redistribution of those materials is granted by the toolkit license. No API credentials are required for rendering or procedural SFX.

## Version 2 changes

A/THE labels on the opening paper cards; selected Persian headlines; contextual England flag badges; redesigned final three scenes including THE inside the comment box; three additional effects (paper fold, pencil writing, comment send). No music was added. See the alignment folder for model provenance and timing limitations.

## Version 3 visual corrections

England’s flag now appears in only two scenes. Norway’s flag is mounted on the invading ship. Harold’s victory and death have explicit staged actions. Old English is shown as a manuscript with ān → A, and THE is explained with a demonstrative-family diagram and a separate THAT branch. Two contact effects accompany the new actions; narration and caption timing are unchanged.

## Version 4 — new recording and opening

The new script and voiceover have been aligned again. The user approved removing speech after the script CTA; the approved recording ends at 79.1 seconds. The published narration source omits that extra tail, with its decoded prefix checked sample-for-sample against the original input. The opening king is seated on his throne holding A and THE cards, with speech-led accents. Headlines and artwork now occupy separate reserved zones. The English subtitle row is removed and English utterances receive Persian captions. England’s public-domain Natural Earth outline is filled with the St George cross, clipped to the country boundary. The 8-second hook preview is in `video/previews/`.

## Version 5 — sound bridges and varied edits

Four J-cut sound pre-laps and two L-cut tails bridge selected picture edits while narration and Persian captions retain their timing. Distinct battle, sail, fall and one brief game-over effect replace repeated transition sounds. THE types in three synchronized steps in the final comment box. No background score was added. The sound-event map and edit checks are in [sound-events-v5.json](films/a-the-kings/production/sound-events-v5.json) and [edit-QC-v6.json](films/a-the-kings/production/edit-QC-v6.json).

## Version 6 — narrative color palette

The opening uses bright cream, an ivory A card and a burgundy THE card with white lettering. History uses warm paper; invasion and battle use slate navy; Harold’s death uses warm charcoal. The grammar section returns to cream, and the CTA repeats burgundy in the comment box. Text color adapts to dark backgrounds. The original speech, Persian captions and v5 sound design retain their timing. Computed palette contrast and hook checks are in [palette-QC-v6.json](films/a-the-kings/production/palette-QC-v6.json).

## Version 7 — clearer narration and stronger color

Narration receives gentle presence EQ and compression without retiming. Mastering targets −12 LUFS with a true-peak guard below −1 dBTP. The encoded file measures −12.51 LUFS / −1.46 dBTP, 1.51 LU louder than v6. Speech-aware ducking and an overlapping-window effect limiter keep narration above the effects. Seven pencil/marker sounds follow animated learning strokes; 30 sound events retain the four J-cuts and two L-cuts. No music is added.

Warm cream, gold, teal, navy, plum and pale blue distinguish the story beats. More saturated costumes preserve each character’s color identity. See [audio measurements](films/a-the-kings/production/audio-QC-v7.json), [palette checks](films/a-the-kings/production/palette-QC-v7.json) and [stroke synchronization checks](films/a-the-kings/production/learning-QC-v7.json). Independent listening review has not been performed.

## Completed film: 1904 Olympic marathon — v2

[Download the complete 2:06 gouache film](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/main/video/olympic-1904-final-v2.mp4) · [Revised first ten seconds](https://raw.githubusercontent.com/kiangasgaryishere/paper-cut-motion-/main/video/olympic-1904-opening-v2.mp4) · [Project and validation](films/olympic-1904-gouache/README.md)

The opening now has two distinct animated shots for the 1904 Olympic venue and eighteen exhausted nonfinishers, plus short J-cut/L-cut sound bridges. The full narration, Persian subtitles, Fred Lorz car story, Thomas Hicks finish, English recap and PHRASAL comment prompt remain complete. Narration takes priority over effects; no background music. Every picture from twenty seconds onward is preserved, and earlier versions remain available.
