from pathlib import Path
import sherpa_onnx,soundfile as sf,numpy as np,json,time
P=Path(__file__).resolve().parents[1];M=Path('/workspace/models/sherpa-onnx-whisper-small');y,sr=sf.read(P/'analysis/out/source16.wav',dtype='float32')
r=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=str(M/'small-encoder.int8.onnx'),decoder=str(M/'small-decoder.int8.onnx'),tokens=str(M/'small-tokens.txt'),language='en',task='transcribe',num_threads=3,enable_segment_timestamps=True)
audit=[]
for a,b in [(14.16,16.65),(20.4,23.7),(26.81,30.1),(33.05,38.6),(42.2,47.6),(52.27,57.25),(68.0,69.79)]:
 s=r.create_stream();s.accept_waveform(sr,np.pad(y[round(a*sr):round(b*sr)],(0,round(29*sr)-round((b-a)*sr))));r.decode_stream(s);q=json.loads(str(s.result));audit.append({'offset':a,'end':b,'result':q});(P/'analysis/asr-english.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2));print(a,b,q['text'],flush=True)
