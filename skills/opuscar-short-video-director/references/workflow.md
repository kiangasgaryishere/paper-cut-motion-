# Workflow and review gates

## 1. Intake and setup

Obtain the supplied script, inspect files, record collaboration preferences, and check/install the required tools early. Continue independent setup while waiting for nondependent answers. Do not begin final animation against a provisional voice track.

## 2. Analyze and lock content

Compare actual narration to the script. Log real duration, pauses, bilingual examples, pronunciation issues, unexpected extras and repeated lines. Transcription is evidence, not a replacement for the script; names and numbers need checking. Use overlapping transcription windows when an automatic segment fails.

Do not silently edit either source. Once authorized, create the approved script/narration version and a source map for intentional cuts. For TTS, keep the exact approved wording, check English examples/accent and get a real recording before final timing. Timing estimates may support planning only.

## 3. Treatment and art direction

Read the selected style's invariants. Consider original structural/treatment options without changing approved wording; choose a clear visual approach. Write `TREATMENT.md` before consulting demo story/code, except upstream material-gathering tools explicitly needed first. Never reskin a demo story as the user's film.

Write `ART_DIRECTION.md`: source style/prompt, palette, texture, light, typography, layout zones, identities, camera grammar, permitted transition families, audio palette and things to avoid. Choose one primary style. Explain any small, deliberate derivative.

## 4. Plan every shot and sound

Fill `timeline.json`, `STORYBOARD.md` and `SOUND_PLAN.md`. Each shot needs a start/end, composition, action, motion, incoming/outgoing connection, text and exact audio events. Plan recurring visual events every 3–4 seconds, including quiet teaching highlights. Asset availability/license and sync points are part of planning, not a late mix surprise.

Create 2–3 representative style frames with the intended drawing/rendering approach. Include the opening, a teaching/story beat and/or CTA. If generated artwork is part of the style, inspect it before animating; maintain a model sheet/asset bible. Do not imply an image-generation or speech tool exists unless available.

## 5. Consolidated review

Always complete the plan first. For key-checkpoint mode, present one compact package: short brief, style frames, timed storyboard and audio direction. Obtain approval once, then proceed. Close-review mode adds the agreed stages. Independent mode proceeds with disclosed assumptions and no artificial storyboard approval gate. A user can change modes later.

## 6. Production

Build deterministic animation from the locked timeline; integrate actual sound and caption cues. Produce an early hook preview for internal checking. Render the agreed windows/full film, mix continuously and verify the actual encoded output.

Ten-second mode is a review/render window, not a new film. Preserve world positions, continuous camera/ambience and canonical narrator across boundaries. Deliver 0–10, then 0–20, then 0–30, etc. Final part may be shorter. Track completed intervals and next start. A later “finish the whole video” instruction supersedes the old stop-every-ten-seconds workflow.

## 7. Revisions and delivery

Translate feedback into a change list and affected time ranges. Preserve approved material where possible. Update the shared timeline and all dependent assets/cues. A sound-only change does not justify rerendering picture. Do not repeatedly broaden tests after appropriate checks pass.

Run visual/audio/mobile/technical QC and a subtraction pass. Commit and push every completed project change/revision, including any requested preview, to the designated project repo. Verify the pushed artifact and return its commit-pinned video download automatically; PR merge is not required for review. In ten-second mode give the cumulative export. Follow repository-delivery.md for public/private access. Retain prior versions and a concise change log.
