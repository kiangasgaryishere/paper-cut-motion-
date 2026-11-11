# Quality gate and subtraction pass

## Before production

- Supplied script and narration policy are resolved; no invented dialogue.
- Actual narration is locked if planned. Script/audio discrepancies have a recorded decision.
- Opuscar style/source and any derivative are clear; tool smoke render/export passes.
- User participation and ten-second/full mode are recorded.
- Timed storyboard, shot/camera direction, text, B-roll and sound assets/sync points are defined.
- Representative real style frames exist and the selected review gate is satisfied.
- Visual milestones leave no unexplained gap beyond four seconds; teaching remains readable.

## Visual review

Inspect a contact sheet across the film, closer strips around key actions/cuts, and actual playback where available. Check hook and first 5–6 seconds deliberately. Check the last three shots and CTA just as carefully.

Check changing scale/angle/action rather than repeated crops; focal hierarchy; character/prop/light continuity; road geometry, motion direction, foot contact, occlusion and parallax; maps/flags/historical accuracy; image/heading separation; bilingual shaping, contrast and mobile-safe text; correct final comment keyword. B-roll must explain or contextualize something.

## Sound and timing

Check actual voice/script match, word/caption timing, teaching highlights and all edited joins. Verify effects against actions, material and period. Listen for excessive whooshes, repeated identical footfalls, synthetic noise, sharp writing, surprising engine/food/crowd levels and an overbusy opening. Key effects must be audible; speech and pronunciation remain easy to follow.

Measure decoded output loudness/true peak/clipping and relevant stem levels. Confirm no AAC priming shift, gap, repeated syllable or per-part level reset. For a cut, prove the intended interval is removed and following cues are shifted together. State whether listening/playback was actually possible.

## Technical output

Check final codec, dimensions, frame rate, frame count, duration, audio sample rate, stream start times and full decoding. Detect black/blank intervals, broken fonts/assets and unwanted silent gaps. A fade or intentional silence is not automatically an error; record it. Copy-only revisions can use packet/frame equality to establish unchanged picture, plus a new audio decode/timing check.

Useful FFmpeg/ffprobe checks include stream metadata, full decode, `blackdetect`, loudness/true-peak analysis and waveform cross-correlation around joins. Use the current tools and actual project files; do not claim these checks ran merely because commands are documented.

Check that the completed change and requested preview/final MP4 were committed and pushed to the intended repo/branch. Verify the actual remote video commit, a link pinned to that commit, and the downloaded bytes/hash where access permits. A Git LFS pointer or permission page is not a video download. For private repos, record authentication requirements and only claim checks actually performed. PR merge is not required to deliver a pushed preview. Instagram processing may change quality; local export QC is not proof of a successful platform upload.

## Subtraction pass

For every prominent cut/move/effect/text layer ask: what does it add? Remove or simplify one without a clear narrative/learning purpose. Watch for simultaneous competition: dramatic motion + big text + hard whoosh + impact. Prefer a clean cut or silence when sufficient. Preserve breathing space around pronunciation, comparison and the ending.

## Honest handoff

Record each check in `QC.json` as passed, failed, not performed or not applicable, with evidence. Do not set all checks to passed from a template. A failed required check must be fixed or clearly reported as a material limitation. Never claim the video is proven “viral”, “fully listened to”, “perfectly synchronized” or “Instagram certified” without corresponding evidence.

After appropriate checks pass, deliver; do not repeat expensive tests without a changed file, new failure or unresolved concern.
