# Sound plan v1 — proposed, no mix rendered

Source: assets/narration.mp3, uploaded mommy.mp3. Complete decoded length: 57.19625 s. Keep all words and the supplied English excerpt. No TTS/provider/extra actor voice required. Source integrated loudness -16.71 LUFS / measured true peak +2 dBTP; master the full recording once with appropriate headroom and a true-peak guard, preserving natural speed/timing. Never normalize per scene.

## Selected sound grammar

| Event | Source/method | Placement and character | Voice protection |
|---|---|---|---|
| Every marker pen-down | Native Marker on Paper `demo/mix.py` felt(d,v,seed,bright), tok and tsk algorithms; MIT | Export actual line/write/hatch durations, lengths/speeds and screen positions from the final drawing timeline. Color markers slightly duller; mild screen-position pan. | Locally reduce against speech; audible above silence, never a constant noisy bed. |
| Handwritten English | Native felt function, syllabic/glyph envelope | Begins at actual letter stroke; pauses with pen lifts, stable source seed. | Almost absent during source English pronunciation so the phonetic example is not masked. |
| Page peel | Native peel_sound, corner crackle then slide | Matches the exact corner lift/fold/slide duration. | No hard digital pop; short, not loud over a new instruction. |
| Push-through | Native air(d,seed), low filtered air | Match the accelerating push and stop on the incoming match frame. | Brief, soft; not a bright stock whoosh. |
| Optional recorded-style fallback | SFX Kit writing-marker-draw, writing-marker-write, foley-paper-slide, props-page-turn; CC0 | Available locally and inspected in the catalogue. Use asset sync.at if selected; trim/fade to actual action. | Native procedural marker is preferred for line-by-line sync; do not layer both unnecessarily. |
| LISTEN | Marker writing + final red stroke | Six letters written, then one underline; no keyboard because no keyboard is pictured. | Voice remains primary; silence after completed underline. |

## Protected intervals

- Approx. 1.85–4.25 s: the existing English film phrase. No added pronunciation, no overlapping music/bright marker squeak. Do not reveal its text on the first hearing.
- Approx. 26–30 s: Did you / Didja explanation. Fine word intervals will be refined from the original waveform; place marker emphasis between pronunciation targets where possible.
- Two short paper/reading breathing spaces come from real pauses and the native page transitions. Do not fabricate narrator gaps.

## Planning status

Visual transition moments are in timeline.json/REVIEW.fa.md. Individual pen-down sound events depend on the approved final drawing animation, so exact asset/sample events and final mix remain production work, not completed QC. Do not claim these sounds have been auditioned or mixed already.

Target final output: around -14 LUFS, true peak <= -1 dBTP with AAC margin; measure the encoded MP4. Listen in context if playback tools allow. Preserve clear, identifiable marker/paper cues without masking teaching. No background music, chalk, typing, coins, engine or unrelated effects.
