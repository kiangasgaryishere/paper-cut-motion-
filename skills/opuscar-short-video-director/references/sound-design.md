# Sound design is preproduction

## Plan and select before animation

For each shot identify the audible action, ambience, attention cue and any sound bridge. Record asset/source/license, visual sync frame, file sync offset, duration, gain, local speech duck, pan, fade/loop and purpose. “Add whoosh later” is not a sound plan.

Start with **SFX Kit by Wyzowl**: https://github.com/wyzowl/sfx-kit. Read its current `GUIDE.md`, `sounds.json`, `catalogue.md`, `analysis.json` if useful, and `LICENSE`. At the version inspected for this skill, its original synthesized WAVs are CC0, with 48 kHz/24-bit files and per-asset placement/level metadata. Verify the version/license, do not assume all future assets are identical.

Choose by actual action, material, length and intensity; check `use_for` and `avoid_for`. Available families include whooshes, coins, writing/chalk, keyboard, props, paper and applause. The kit is not assumed to contain footsteps, cars, food or every requested action. If absent, use an appropriate authorized source with a valid license or a credible original procedural model. Do not rename a random effect to claim it matches.

Copy only selected files/metadata into the project; record source commit and hashes. No need to bundle all 320 effects in every film.

## Sync precisely

**Timeline start = desired visual moment − `sync.at`.** It is not always the file start or peak. For rate changes, divide file times/sync offsets by the rate and respect `adapt.rate`. Choose a short sound for a short action. For trimmed writing or loops, use short fades/crossfades as documented; compensate a quiet excerpt if necessary and record it. Loops must not click or pulse unnaturally.

Examples:

- coin contact, scissor snip or apple bite: impact/crunch meets the actual action;
- chalk/pencil: sound runs while the stroke is drawn;
- keyboard: keys meet rendered character frames, Enter meets send/confirm;
- footsteps: match visible travel/cadence and surface, not all outdoor scenes;
- engine: a plausible period/material sound can pre-lap the car's arrival;
- applause: spatially and emotionally fits an audience or win, then fades;
- whoosh: supports a selected move/transition, not every title/caption change.

## Audible, sparse and speech-first

Do not bury effects through blanket heavy ducking. Do not solve audibility by raising continuous noise. Mix action stems separately from ambience. Use the kit's `under_voiceover_db` as a starting point and adjust after listening to the actual narrator and cropped asset. A brief effect may be roughly 8–14 dB below active speech as an initial audition range, not a universal rule. Timbre, frequency masking, material and action matter more than one RMS target.

Keep teaching pronunciation especially clear. Reduce competing 1–4 kHz energy, move a transition into a pause where possible, use local ducking, and protect peaks. Keep speaker priority without making important footsteps/coins/writing effectively inaudible. Avoid musical stings if music is disallowed. Silence is a valid cue.

Use a small palette with variants to avoid machine-gun repetition. Avoid stacking a whoosh, impact, chime, applause and new text on the same beat. J/L bridges can create continuity without more visual effects. Do not turn every sound into an attention alarm.

## Mix once across the full timeline

Master narration once, preserve its natural timing/gain across review windows, and keep voice/effects/music stems. Apply effects-only headroom control where possible. The final AAC encode is continuous; never concatenate per-part AAC streams as the master audio. Recheck sound events after sentence edits and caption/visual changes.

Start near −14 LUFS integrated for the final online-video mix and a true-peak ceiling no higher than −1 dBTP, leaving extra codec headroom when needed. These are useful defaults, not Instagram guarantees. Evaluate loudness on the encoded MP4, not only the WAV. Do not normalize each ten-second clip independently.

## Audition and evidence

Listen in context, on headphones and a small speaker/mono/mobile simulation when possible: can the effect be identified, does it meet the action, is the voice effortless, is it pleasant after several repetitions? Review apple/food, crowd, engine and sharp writing sounds carefully. Measure peaks/clipping, speech/effect balance and synchronization separately. Log actual listening conditions, or explicitly mark listening as not performed. Waveforms cannot certify naturalness or mobile audibility.
