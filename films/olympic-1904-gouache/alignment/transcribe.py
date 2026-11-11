from pathlib import Path
import json,numpy as np,soundfile as sf,sherpa_onnx
p=Path(__file__).resolve().parent.parent;model=Path('/workspace/models/sherpa-onnx-whisper-small')
r=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=str(model/'small-encoder.int8.onnx'),decoder=str(model/'small-decoder.int8.onnx'),tokens=str(model/'small-tokens.txt'),language='fa',num_threads=3,enable_segment_timestamps=True)
y,sr=sf.read(p/'out/voice-asr.wav',dtype='float32');s=r.create_stream();s.accept_waveform(sr,np.pad(y,(0,max(0,29*sr-len(y)))));r.decode_stream(s);result=json.loads(str(s.result));(p/'alignment/asr-first18.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
