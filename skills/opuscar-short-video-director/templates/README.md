# Template contract

Initialize into a new project with `scripts/init_project.py`. The agent fills these files from source material and decisions; the user does not fill forms. The untouched templates intentionally fail production-readiness checks.

## Timeline JSON

- `fps`, `sample_rate`, `duration_frames`: positive integers; intervals are half-open.
- `shots`: ordered, contiguous records covering the whole film, each with `id`, `start_frame`, `end_frame`, `visual`, `action`, `camera` (object or description), `transition_out` and `sound_direction`. “Silence” is a valid explicit sound direction.
- `milestones`: `{frame, event}` for meaningful within-shot changes. Shot starts also count. No default gap beyond four seconds; preserve reading time through small changes rather than excessive cutting.
- `captions`: `{start_frame, end_frame, text}`. Language policy comes from `brief.text.captions`. Target-language teaching text belongs in the shot/teaching layer, not automatically in translated bottom captions.
- `teaching_highlights`: `{start_frame, end_frame, target, description}` for synchronized examples/emphasis.
- `sound_events`: `{id, moment_frame, sync_at, start_seconds, duration_seconds, source, asset, license, purpose, under_voiceover_db}`. Start is `moment_frame/fps - sync_at`. If that is negative, set actual `start_seconds` to zero and `trim_start_seconds` to the removed prefix. For `source: procedural`, use `method` instead of an asset/license. Rates must already be reflected in sync/duration values; record the rate separately.
- `source_map`: records `{kind, output_start_sample, output_end_sample, source_start_sample, source_end_sample}` covering the full output audio. `kind: source` preserves equal sample lengths at unchanged speed; `kind: silence` has a `reason` instead of source offsets. Required if narration is planned. Use the actual decoded narrator sample count in the brief. No narration: explicitly set `required: false`, `status: not-required`.
- `approved_audio_edits`: source removals as `{source_start_sample, source_end_sample, approval, reason}`. Include a record for omitted opening/tail audio too. Nonempty approval records refer to an actual instruction/delegation; never invent approval to pass a validator.

The helper checks readiness, logical ranges, reading-layer policy and source-map consistency. It does not verify the truth of a supplied approval string, pronunciation, asset rights, real media duration, visual quality or listening. Check those separately.

## Brief gates

Set `mode_confirmed` and `participation_confirmed` only from actual user choices. Mark plan sections `ready` when complete. Review status is `approved` for close/key-checkpoint modes, or `delegated` for independent mode. Include a decision reference. A key-checkpoint default is not automatic approval.

Style invariants and at least two actual frame files must be recorded. Narration status must be `provided` with a real file/decoded count or explicitly `not-required`. Caption language must be resolved, even for silent/caption-free projects (`none`).
