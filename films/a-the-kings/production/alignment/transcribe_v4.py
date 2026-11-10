import sherpa_onnx,soundfile as sf,json,numpy as np,re,os,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;FILM=HERE.parent;OUT=HERE/'v4';p=Path(os.environ.get('SHERPA_MODEL_DIR','/workspace/models/sherpa-onnx-whisper-small'))
r=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=str(p/'small-encoder.int8.onnx'),decoder=str(p/'small-decoder.int8.onnx'),tokens=str(p/'small-tokens.txt'),language='fa',num_threads=3,enable_segment_timestamps=True)
y,sr=sf.read(FILM/'voice.wav',dtype='float32');duration=len(y)/sr
OUT.mkdir(exist_ok=True)
if not (OUT/'silences.log').exists():
 with (OUT/'silences.log').open('w') as f:subprocess.run(['ffmpeg','-hide_banner','-i',str(FILM/'voice.wav'),'-af','silencedetect=noise=-34dB:d=0.16','-f','null','-'],stderr=f,stdout=subprocess.DEVNULL,check=True)
log=(OUT/'silences.log').read_text();pauses=[]
starts=re.findall(r'silence_start: ([\d.]+)',log);ends=re.findall(r'silence_end: ([\d.]+)',log)
for a,b in zip(starts,ends):
 a,b=float(a),float(b)
 if b-a>.25:pauses.append((a+b)/2)
bounds=[0]
while duration-bounds[-1]>15:
 a=bounds[-1];cand=[x for x in pauses if a+10<x<a+15];bounds.append(min(cand,key=lambda x:abs(x-a-13)) if cand else a+13)
bounds.append(duration);out=[]
for a,b in zip(bounds,bounds[1:]):
 z=y[round(a*sr):round(b*sr)];z=np.pad(z,(0,29*sr-len(z)));s=r.create_stream();s.accept_waveform(sr,z);r.decode_stream(s)
 out.append(dict(offset=a,end=b,result=json.loads(str(s.result))));print(a,b,s.result,flush=True)
 (OUT/'asr-segments.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print('COMPLETE',bounds,flush=True)
