# Timing evidence and limits

The 62.02-second decoded recording was segmented from RMS pauses and compared to the supplied script using the locally installed sherpa-onnx Whisper-small model. Raw ASR is imperfect: some chunks fail its UTF-8 serializer; some hallucinate or omit material. The supplied script, not ASR spelling, is the text authority.

A token-timestamp pass was attempted, but the installed decoder lacks cross-attention outputs and explicitly reports that token timestamps are unavailable. That attempt was stopped after confirming the model limitation; no token-level timing claim is made. Caption cues are phrase-level estimates, with about 30 ms lead at known pause boundaries, not a manually verified word-level transcript. The two narrator-quote replacement boundaries were chosen inside measured pauses; every other narration sample is preserved exactly by the master edit map.
