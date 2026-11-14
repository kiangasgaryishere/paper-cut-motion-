# Connected Speech — new-hook A/B edition

A separate production based on the newly supplied `script.md` and `Honey.mp3`, keeping the approved Lemo Marker on Paper identity. **69 seconds, 1080×1920, 24fps, AAC stereo 48kHz.** Earlier videos and covers are preserved.

The opening movie and the replay after the guessing prompt fill the entire vertical frame with a subject-aware crop. Each leaves through an aspect-preserving match move into the paper diagram. The third utterance (“Rick said”) uses the actual supplied movie picture/audio. The script's final listening replay also uses the movie. Neither narrator imitation remains.

Twelve original pages are specific to this script: subtitle dependence, familiar words, sound linking/reduction, Connected Speech, Did you/Didja, recognition, five audio conversations, transcript/worksheet and LISTEN comment CTA. White Persian captions use charcoal panels. The first listening test is uncaptioned; the second has English text. The final test withholds its English answer. No added music; film's supplied audio retained and native paper/marker foley protects speech.

`timeline.json` contains the shared output frame clock and explicit source/output edit map. Source voice is 62.02s decoded. Only two authorized English narrator sample windows are replaced; all other samples are retained with no speed changes. Two additional movie screenings and the longer replacements bring the total to 69s, including a short ending hold. Phrase caption timing uses the supplied script and source pauses; ASR evidence is imperfect and contains documented failures. No independent real-time listening or word-level transcription review is claimed.

## Build

Existing Chromium, FFmpeg, Node/playwright-core and the configured Opuscar Python (NumPy, SciPy, SoundFile) are reused. The native engine, fonts and glyphs are shared with `../connected-speech-marker`; do not move this folder alone without those dependencies.

```bash
bash films/connected-speech-ab-hook/tools/build.sh
```

The supplied movie source is the previously authorized `../connected-speech-marker/assets/mummy-real-clip.mp4`. Generated full-resolution JPEG frames and temporary WAV/render files stay in ignored out/. Only final MP4 and review evidence are published.

See STORYBOARD.md, brief.json, CREDITS.md, analysis/ and QC.json for actual direction and validation. Output: `video/connected-speech-ab-hook-v1.mp4`.
