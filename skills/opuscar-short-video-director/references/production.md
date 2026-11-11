# One timeline, reliable production

## File and timing model

Use a project-local `brief.json` plus `timeline.json`. Store video events in integer frames and narrator positions in integer samples. Default 30 fps / 48,000 Hz means exactly 1,600 samples per frame. Other frame rates need rational mapping; do not repeatedly round local segment times.

Derive render windows, shots, captions, sound events and teaching highlights from this source. The Markdown storyboard and cue sheet are human-readable views of the same decisions. Record the source/audio hash, style/library commits, asset provenance, plan baseline and approvals.

The schema is a production contract, not a required rendering engine. A Canvas/HTML/three.js Opuscar project can load exported data; helpers must not silently maintain a second, divergent timing file.

## Rendering

Follow the selected style and current Opuscar core. Use deterministic `render(t)` and seeded randomness; no accumulated state, `Date.now()`, live network fonts or frame-order dependence. Wait for fonts/images to decode before READY. Verify seeking backward and isolated-frame rendering. Carry world geometry through one camera transform; preserve floor contact, occlusion and depth scaling.

Generate or source assets to fit the planned shot, not the reverse. Inspect anatomy, transparency, safe areas, historical details, repeated identities and text artifacts. Keep typography in code where practical, especially RTL/bilingual examples and comment keywords. Match texture/grain and avoid excessive compression-destroying animated grain.

## Narration, subtitles and teaching

Retain an original recording and one full mastered narrator. Do not alter speed or normalize by review part. Compare ASR against the approved script, check pronunciation and align to actual pauses/words. Correct transcription errors from evidence; flag spoken discrepancies.

Caption speech normally at its onset; an optional **20–50 ms lead** can be chosen and auditioned. Never impose a half-second caption lead or delay. J/L-cuts adjust picture/contextual audio, not the caption's relationship to the narrator. English examples and translated bottom captions can be separate layers, but caption language policy is explicit in the brief.

Readability needs actual mobile-scale review, not only a bounding box. Shape Arabic/Persian correctly with a supporting font, set RTL/LTR per element and check digits/punctuation. Avoid long stacked text, tiny translations, title/subject collisions and subtitle/UI overlap.

## Ten-second assembly

Render `[0,10)`, `[10,20)`, etc. from the global timeline. A cut may cross a window boundary; do not force a new shot at every ten seconds. Slice the canonical PCM at exact sample boundaries. No narrator boundary fades, repeat syllables or padding between parts.

For each cumulative export, concatenate picture streams with accurate timestamps when compatible; strip per-part AAC before concatenation to avoid encoder priming offsets. Build full PCM voice/effects once, then encode final AAC once. Re-encode incompatible picture blocks deliberately rather than assuming stream-copy is safe. Verify duration/frame count and audio lag around every join. Keep old versions and next-start metadata.

## Revisions and edit maps

Use stable shot/cue IDs. For a sound-only update, copy the verified picture stream and remux a new continuous audio encode. For a local picture update, rerender the smallest correct region and preserve unaffected streams/frames when feasible.

When removing a sentence, first confirm authorization, then select quiet boundaries that preserve adjacent words. Store source intervals and corresponding output intervals. Recompute later picture, captions, sound, vocabulary highlights and CTA from that map. Keep pitch/speed unchanged unless requested. Do not fix sync by arbitrarily shifting only the subtitles.

Use versioned outputs and a concise changelog. Do not overwrite a previous approved deliverable without a recoverable version. Stop or change scope when the user cancels; do not publish abandoned edits.

## Delivery

Default MP4: 1080×1920, square pixels, 30 fps, H.264/yuv420p, AAC 48 kHz and fast start, usually Rec.709 with consistent color handling. Choose bitrate/CRF for clarity of texture and text; do not inflate a low-resolution render to claim quality. Export from source-quality assets and preserve a master where needed.

Commit and push each completed meaningful project change to the user's designated repo automatically; use references/repository-delivery.md. Record the actual remote commit and give a direct, commit-pinned MP4 download for every completed review/requested preview/final export. Keep private repos private, and do not require PR merge for a preview. A ZIP/source package can include manifests/build instructions/selected licensed assets, but not credentials, caches, external repositories or model weights. Verify downloaded video bytes/checksum where access permits. Never replace the MP4 link with a source-folder or PR link.
