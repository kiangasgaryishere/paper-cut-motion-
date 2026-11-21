from pathlib import Path
import sherpa_onnx,soundfile as sf,numpy as np,json,time
P=Path(__file__).resolve().parents[1];M=Path('/workspace/models/sherpa-onnx-whisper-small')
y,sr=sf.read(P/'analysis/out/source16.wav',dtype='float32');raw,sr48=sf.read(P/'analysis/out/source48.wav',dtype='float32')
# Explicitly retain source as authority; ASR is an imperfect bilingual audit only.
r=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=str(M/'small-encoder.int8.onnx'),decoder=str(M/'small-decoder.int8.onnx'),tokens=str(M/'small-tokens.txt'),language='fa',task='transcribe',num_threads=3,enable_segment_timestamps=True)
rows=[]
for a,b in [(0,15),(14,29),(28,43),(42,57),(56,len(y)/sr)]:
 t=time.time();s=r.create_stream();seg=y[round(a*sr):round(b*sr)];s.accept_waveform(sr,np.pad(seg,(0,29*sr-len(seg))));r.decode_stream(s);q=json.loads(str(s.result));rows.append({'offset':a,'end':b,'result':q});(P/'analysis/asr-source.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(a,b,round(time.time()-t,1),q['text'],flush=True)
# 10ms RMS pause candidates and exact decoded sample duration.
n=sr48//100;rms=np.sqrt(np.mean(raw[:len(raw)//n*n].reshape(-1,n)**2,axis=1));quiet=rms<.012;pauses=[];a=None
for i,v in enumerate(np.r_[quiet,False]):
 if v and a is None:a=i
 if not v and a is not None:
  if i-a>=12:pauses.append([a/100,i/100])
  a=None
meta={'duration':len(raw)/sr48,'samples':len(raw),'sample_rate':sr48,'source_complete':True,'retimed':False,'rms_pauses':pauses,'asr_limitations':'Local Whisper small; bilingual spelling and word timing are not authoritative.'};(P/'analysis/audio.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2));print(json.dumps(meta),flush=True)
