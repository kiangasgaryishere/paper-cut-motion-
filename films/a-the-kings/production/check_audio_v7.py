from pathlib import Path
import json,numpy as np,soundfile as sf
p=Path('films/a-the-kings/production');v,sr=sf.read(p/'voice-v7.wav');fx,fs=sf.read(p/'sfx-v7.wav');mix,ms=sf.read(p/'mix-v7.wav');assert sr==fs==ms==48000
v=v[:len(mix)];v*=.84/max(.01,np.abs(v).max());voice=np.repeat(v[:,None],2,axis=1);pre=voice+fx;scale=min(1,.96/np.max(np.abs(pre)));err=float(np.max(np.abs(mix-pre*scale)));assert err<3e-7
rows=[]
for start in range(0,len(v)-4800,2400):
 a=v[start:start+4800];b=fx[start:start+4800];vr=np.sqrt(np.mean(a*a));fr=np.sqrt(np.mean(b*b))
 if vr>.04 and fr>.00005:rows.append(20*np.log10(vr/fr))
events=json.loads((p/'sound-events-v7.json').read_text());old=json.loads((p/'sound-events-v5.json').read_text());assert len(events)==len(old)+6
strokes=[e for e in events if any(x in e['type'] for x in ['underline','pencil','marker'])];assert len(strokes)==7
# The new speech treatment must not introduce any timeline shift.
source,_=sf.read(p/'voice.wav');source=source[:len(v)];from scipy.signal import correlate,correlation_lags
# A representative section; FFT correlation detects compressor/filter latency.
a=source[48000:480000];b=v[48000:480000];c=correlate(b,a,method='fft');lag=int(correlation_lags(len(b),len(a))[np.argmax(c)]);assert abs(lag)<=2
q=dict(events=len(events),learning_strokes=len(strokes),J_cuts=sum(e['edit']=='J' for e in events),L_cuts=sum(e['edit']=='L' for e in events),music='none',duration=len(v)/sr,voice_timing_shift_samples=lag,mix_reconstruction_max_error=err,speech_to_effect_dB={'minimum_100ms':float(min(rows)),'median_100ms':float(np.median(rows))},mix_peak_dBFS=float(20*np.log10(np.max(np.abs(mix)))),master_target_LUFS=-12,listening_review='not performed')
assert q['speech_to_effect_dB']['minimum_100ms']>12
(p/'audio-QC-v7.json').write_text(json.dumps(q,indent=2));print(json.dumps(q,indent=2))
