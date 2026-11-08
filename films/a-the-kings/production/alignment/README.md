# Speech timing evidence

Native segment timestamps were extracted locally with sherpa-onnx 2.0.1 and the multilingual Whisper small INT8 model. Model source: https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2 (approximately 610 MiB compressed). The model archive is not committed.

Use a separate Python environment with `pip install -r requirements.txt`; set `SHERPA_MODEL_DIR` to the extracted model directory and run `python transcribe.py` after decoding the source narration to `../voice.wav` at 48 kHz. Audio is processed locally. The decoder limits tokens relative to input duration; clips are padded with silence to 29 seconds to avoid truncating Persian subword output. Original audio is not modified in the film.

`asr-segments.json` is raw recognizer evidence, with spelling errors. The supplied script determines display spelling. `../align_v2.py` records corrected phrase text and timing refinement against silence edges. This is phrase-level alignment, not a word-level forced alignment or a listening certification. Continuous-speech boundaries remain approximate.
