"""One continuous source-master clock; native marker foley, four actual movie screenings, no music added."""
from pathlib import Path
import subprocess,json
import numpy as np,soundfile as sf
from scipy.signal import butter,sosfilt
from scipy.ndimage import minimum_filter1d
P=Path(__file__).resolve().parents[1];O=P/'out';SR=48000;N=69*SR
subprocess.run(['ffmpeg','-y','-v','error','-i',str(P/'assets/narration.mp3'),'-af','highpass=f=75,acompressor=threshold=0.25:ratio=2:attack=8:release=110:makeup=1,loudnorm=I=-17:TP=-3:LRA=6,aresample=48000','-c:a','pcm_f32le',str(O/'voice.wav')],check=True)
subprocess.run(['ffmpeg','-y','-v','error','-i',str(P.parent/'connected-speech-marker/assets/mummy-real-clip.mp4'),'-vn','-ar','48000','-ac','2','-c:a','pcm_f32le',str(O/'clip.wav')],check=True)
vo,sr=sf.read(O/'voice.wav');clip,sc=sf.read(O/'clip.wav');assert sr==sc==SR and len(vo)==2976960
clip*=10**(-.5/20);f=144;clip[:f]*=np.linspace(0,1,f)[:,None];clip[-f:]*=np.linspace(1,0,f)[:,None];pad=np.zeros((114000,2));pad[:len(clip)]=clip
T=json.loads((P/'timeline.json').read_text());mix=np.zeros((N,2));voice_stem=np.zeros((N,2));movie_stem=np.zeros((N,2))
for s in T['segments']:
 a=round(s['start_frame']*2000);b=round(s['end_frame']*2000)
 if s['kind']=='voice':
  z=vo[round(s['source_start_frame']*2000):round(s['source_end_frame']*2000)];assert len(z)==b-a;voice_stem[a:b]=z[:,None]
 elif s['kind']=='movie':assert b-a==114000;movie_stem[a:b]=pad
fx=np.zeros((N,2),np.float32)
def band(x,a,b):return sosfilt(butter(2,[a,b],fs=SR,btype='bandpass',output='sos'),x)
def low(x,f):return sosfilt(butter(1,f,fs=SR,output='sos'),x)
def felt(d,v,seed):
 n=max(64,round(d*SR));r=np.random.default_rng(seed);x=band(r.standard_normal(n),550,min(5200,1700+v*.45));tooth=low(abs(r.standard_normal(n)),min(500,60+v*.02));tooth/=np.percentile(tooth,90)+1e-9;x*=.55+.45*np.clip(tooth,0,1.6);aa=min(n//3,288);bb=min(n//3,1200);en=np.ones(n);en[:aa]=np.linspace(0,1,aa);en[-bb:]=np.linspace(1,0,bb)**1.5;return x*en*np.clip(v/2500,.35,1)**.7

def place(z,t,gain,x=540):
 a=round(t*SR);z=z[:max(0,min(len(z),N-a))]*gain;pan=np.clip((x/1080-.5)*.65,-.35,.35)
 if len(z) and a>=0:fx[a:a+len(z)]+=z[:,None]*np.sqrt([(1-pan)/2,(1+pan)/2])
ev=json.loads((O/'events.json').read_text())['events']
for k,e in enumerate(ev):
 if e['type'] in ['line','write']:
  z=felt(e['d'],e['v'],k+42)
  if e['type']=='write':z*=.55+.45*abs(np.sin(2*np.pi*10*np.arange(len(z))/SR))
  place(z,e['t'],.12,e.get('x',540))
 else:
  n=round(e['d']*SR);r=np.random.default_rng(k);tt=np.arange(n)/SR;en=np.sin(np.pi*tt/e['d'])**1.7;z=band(r.standard_normal(n),400,3500)*en if e['type']=='peel' else low(r.standard_normal(n),900)*en;place(z,e['t'],.065)
for t in [2.375,9.25]:
 r=np.random.default_rng(round(t*100));tt=np.arange(round(.58*SR))/SR;place(band(r.standard_normal(len(tt)),500,2400)*np.sin(np.pi*tt/.58)**2,t,.06)
env=np.sqrt(np.maximum(0,low(voice_stem[:,0]**2,8)));fx*=np.clip(.065/(env+.018),.35,1)[:,None]
# Pronunciation example is deliberately quiet under Did you / Didja.
fx[round(38.25*SR):round(42.2*SR)]*=.2
for s in T['segments']:
 if s['kind']=='movie':fx[round(s['start_frame']*2000):round(s['end_frame']*2000)]=0
fx*=min(1,.15/(abs(fx).max()+1e-9));mix=voice_stem+movie_stem+fx
need=np.minimum(1,.87/(abs(mix).max(axis=1)+1e-9));mix*=minimum_filter1d(need,size=481,mode='nearest')[:,None]
sf.write(O/'mix.wav',mix,SR,subtype='PCM_24');sf.write(O/'voice-stem.wav',voice_stem,SR,subtype='PCM_24');sf.write(O/'movie-stem.wav',movie_stem,SR,subtype='PCM_24')
r={'duration':69,'samples':N,'source_voice_samples':len(vo),'clip_samples':len(clip),'screenings':4,'first_two_fullscreen':True,'replaced_source_quote_frames':[[298,333],[926,963]],'music':'none added; supplied movie audio retained','peak_dbfs':float(20*np.log10(abs(mix).max())),'narration_retained':'all samples except the two authorized English sample intervals','listening_review':'not performed'};(P/'analysis/mix-report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
