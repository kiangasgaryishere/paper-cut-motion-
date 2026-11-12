"""Deterministic native felt-marker foley, no music; source narration is never cut or retimed.
Felt/tap/paper algorithms adapted from Lemo marker-paper/demo/mix.py (MIT).
Run with the Opuscar Python environment after tools/check-film.mjs exports out/events.json.
"""
from pathlib import Path
import json, subprocess
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt
P=Path(__file__).resolve().parents[1]; O=P/'out'; O.mkdir(exist_ok=True)
SR=48000; N=58*SR
chain='highpass=f=75,acompressor=threshold=0.25:ratio=2.0:attack=8:release=110:makeup=1,loudnorm=I=-14:TP=-2:LRA=6:measured_I=-18.63:measured_TP=-1.69:measured_LRA=3.30:measured_thresh=-29.22:offset=1.33:linear=false,aresample=48000'
subprocess.run(['ffmpeg','-y','-v','error','-i',str(P/'assets/narration.mp3'),'-af',chain,'-c:a','pcm_f32le',str(O/'voice.wav')],check=True)
vo,sr=sf.read(O/'voice.wav',dtype='float32'); assert sr==SR and len(vo)==2745420,(sr,len(vo))
voice=np.zeros(N,np.float32);voice[:len(vo)]=vo
fx=np.zeros((N,2),np.float32)
def band(x,a,b):return sosfilt(butter(2,[a,b],fs=SR,btype='bandpass',output='sos'),x)
def low(x,f):return sosfilt(butter(1,f,fs=SR,output='sos'),x)
def felt(d,v,seed):
 n=max(64,round(d*SR));r=np.random.default_rng(seed);x=band(r.standard_normal(n),550,min(5200,1700+v*.45));tooth=low(abs(r.standard_normal(n)),min(500,60+v*.02));tooth/=np.percentile(tooth,90)+1e-9;x*=.55+.45*np.clip(tooth,0,1.6)
 a=min(n//3,288);b=min(n//3,1200);env=np.ones(n);env[:a]=np.linspace(0,1,a);env[-b:]=np.linspace(1,0,b)**1.5
 return x*env*np.clip(v/2500,.35,1)**.7

def tap(seed):
 r=np.random.default_rng(seed);t=np.arange(2400)/SR
 return np.sin(2*np.pi*210*t)*np.exp(-t/.009)*.6+band(r.standard_normal(len(t)),900,3200)*np.exp(-t/.003)*.5

def place(x,t,gain,pan=0):
 i=round(t*SR); x=x[:max(0,min(len(x),N-i))]*gain
 if len(x) and i>=0: fx[i:i+len(x)]+=x[:,None]*np.array([np.sqrt((1-pan)/2),np.sqrt((1+pan)/2)])

events=json.loads((O/'events.json').read_text())['events']
for k,e in enumerate(events):
 t=e['t'];d=e['d'];r=np.random.default_rng(900+k)
 if e['type'] in ['line','write']:
  x=felt(d,e['v'],k+42)
  if e['type']=='write':x*=.55+.45*abs(np.sin(2*np.pi*10*np.arange(len(x))/SR))
  pan=np.clip((e['x']/1080-.5)*.65,-.35,.35);place(x,t,.13,pan);place(tap(k),t,.04,pan)
 else:
  n=round(d*SR);tt=np.arange(n)/SR;en=np.sin(np.pi*np.clip(tt/d,0,1))**1.7
  if e['type']=='peel':x=band(r.standard_normal(n),400,3500)*en;gain=.10
  else:x=low(r.standard_normal(n),900)*en;gain=.11
  place(x,t,gain,.12)
# RMS-guided smooth sidechain preserves material sound while protecting intelligibility.
env=np.sqrt(np.maximum(0,low(voice.astype(float)**2,8)));duck=np.clip(.065/(env+.018),.35,1)
fx*=duck[:,None]
# Original English first hearing and fast-speech pronunciation are learning-critical.
for a,b,gain in [(2.12,3.98,0),(26.45,30.6,.22)]:
 i,j=round(a*SR),round(b*SR);mask=np.ones(N);mask[i:j]=gain;fade=round(.06*SR);mask[max(0,i-fade):i]=np.linspace(1,gain,min(fade,i));mask[j:j+fade]=np.linspace(gain,1,fade);fx*=mask[:,None]
# Cap only effects; narration is mastered once across the complete recording.
peak=np.max(np.abs(fx));fx*=min(1,.18/(peak+1e-9))
mix=voice[:,None]+fx
# Smooth safety limiting only the occasional combined peak; no scene-level gain resets.
peak=np.max(np.abs(mix),axis=1)
need=np.minimum(1,.84/(peak+1e-9))
# Offline lookahead maximum attenuation; small number of transient peaks makes this cheap.
from scipy.ndimage import minimum_filter1d
gain=minimum_filter1d(need,size=481,mode='nearest');mix*=gain[:,None]
mix *= 10**(-2/20) # Stereo loudness calibration: measured final mix ~-14 LUFS.
sf.write(O/'mix.wav',mix,SR,subtype='PCM_24');sf.write(O/'effects.wav',fx,SR,subtype='PCM_24')
report={'sample_rate':SR,'duration':58,'source_voice_samples':len(vo),'silence_tail_samples':N-len(vo),'source_retained_complete':True,'retiming':False,'music':False,'effects_events':len(events),'voice_peak_dbfs':float(20*np.log10(np.max(abs(vo))+1e-12)),'mix_peak_dbfs':float(20*np.log10(np.max(abs(mix))+1e-12)),'protected_english_interval':[2.12,3.98],'pronunciation_effect_gain':.22,'listening_review':'not performed'}
(O/'mix-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
