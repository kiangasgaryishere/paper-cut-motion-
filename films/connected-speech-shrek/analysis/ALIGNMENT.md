# Source analysis and timing

Script retained byte-for-byte from the supplied attachment. Local sherpa-onnx Whisper-small ASR was used for approximate phrase/scene identification. It is imperfect: e.g. padded silence causes hallucinated “I'm sorry” repetitions after the short Shrek file's real end, and Persian spellings are unreliable. Those are not film dialogue or caption authority. Only actual source duration, audible-energy intervals and supplied script text determine the edit.

Shrek1 source 0–2.5s is a quiet establishing lead. The hook uses 2.5s through the supplied file's end, including Donkey's first sentence and Shrek's response. The replay uses 2.5–3.875s, excluding Shrek's later spoken response. Shrek2 is retained in full; its ambient lead is used for the motivated narration L-cut. English captions track real dialogue intervals, omitting ambient annotations and ASR hallucinations. The source's full ending is retained.

New-voice pause 47.43–49.23s permits the trim of 47.5–48.875s without losing words. No narration words or pronunciation examples are removed. The Mummy voice examples contrasting “What are you” and “Whatcha” are educational readings in the new script and remain; actual film screenings have only movie speech. This supersedes the earlier edition's single-imitation replacement treatment for this new lesson structure.

The 16kHz ASR decode rounds duration to 69.48575s; the authoritative 48kHz full-quality decode has 3,335,314 samples, 69.485708333s. The two-sample rounding difference is reflected in the sample-based master map. It is not an audio edit.

No cross-attention word-alignment model or independent listening review is available/claimed. Caption timing is at phrase level; technical AAC lag checks establish export alignment, not subjective pronunciation accuracy.
