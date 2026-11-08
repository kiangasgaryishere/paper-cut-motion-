import sherpa_onnx,soundfile as sf,json,time,numpy as np
from pathlib import Path
import os
HERE=Path(__file__).resolve().parent
FILM=HERE.parent
p=Path(os.environ.get('SHERPA_MODEL_DIR','/workspace/models/sherpa-onnx-whisper-small'))
r=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=str(p/'small-encoder.int8.onnx'),decoder=str(p/'small-decoder.int8.onnx'),tokens=str(p/'small-tokens.txt'),language='fa',num_threads=3,enable_segment_timestamps=True)
y,sr=sf.read(str(FILM/'voice.wav'),dtype='float32');out=[]
for a,b in [(0,15.8),(15.8,29.55),(29.55,44),(44,56.4),(56.4,65.3),(65.3,72.744)]:
 s=r.create_stream();s.accept_waveform(sr,np.pad(y[round(a*sr):round(b*sr)],(0,round(29*sr)-round((b-a)*sr))));r.decode_stream(s)
 print(a,b,s.result,flush=True)
 out.append(dict(offset=a,end=b,result=json.loads(str(s.result))))
 (HERE/'asr-segments.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
