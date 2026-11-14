"""Sample-accurate new-source master, freeze/rewind, actual supplied movie audio, no added score."""
from pathlib import Path
import subprocess,json
import numpy as np,soundfile as sf
from scipy.signal import butter,sosfilt
from scipy.ndimage import minimum_filter1d
P=Path(__file__).resolve().parents[1];O=P/'out';SR=48000;N=87*SR

def ff(*a):subprocess.run(['ffmpeg','-y','-v','error',*map(str,a)],check=True)
ff('-i',P/'assets/narration.mp3','-af','highpass=f=75,acompressor=threshold=0.25:ratio=2:attack=8:release=110:makeup=1,loudnorm=I=-17:TP=-3:LRA=6,aresample=48000','-c:a','pcm_f32le',O/'voice.wav')
movies={}
for name,src in [('shrek1',P/'assets/shrek1.mp4'),('shrek2',P/'assets/shrek2.mp4'),('mummy',P.parent/'connected-speech-marker/assets/mummy-real-clip.mp4')]:
 ff('-i',src,'-vn','-ar',SR,'-ac',2,'-c:a','pcm_f32le',O/f'{name}.wav');movies[name]=sf.read(O/f'{name}.wav')[0]
# Match clip speech to a clear level using constant gain and actual sample peak headroom.
sh=movies['shrek2'];active=sh[round(2.68*SR):round(3.78*SR)];gsh=min(.115/(np.sqrt(np.mean(active**2))+1e-9),.78/(abs(sh).max()+1e-9));movies['shrek1']*=gsh;movies['shrek2']*=gsh;movies['mummy']*=10**(-.5/20)
vo,sr=sf.read(O/'voice.wav');assert sr==SR and len(vo)==3335314
T=json.loads((P/'timeline.json').read_text());voice=np.zeros((N,2));movie=np.zeros((N,2));fx=np.zeros((N,2));reverse=np.zeros((N,2))
for e in T['segments']:
 a=round(e['start_frame']*2000);b=round(e['end_frame']*2000)
 if e['kind']=='voice':
  z=vo[round(e['source_start_frame']*2000):round(e['source_end_frame']*2000)];assert len(z)==b-a;voice[a:b]+=z[:,None]
 elif e['kind']=='movie':
  src=movies[e['asset']];aa=e['source_start_frame']*2000;bb=e['source_end_frame']*2000;z=src[aa:min(bb,len(src))];pad=np.zeros((b-a,2));pad[:len(z)]=z;f=144;pad[:f]*=np.linspace(0,1,f)[:,None];end=len(z);pad[end-f:end]*=np.linspace(1,0,f)[:,None];movie[a:b]+=pad
 elif e['kind']=='reverse':
  src=movies['shrek1'][60*2000:121*2000][::-1];tt=np.linspace(0,len(src)-1,b-a);z=np.stack([np.interp(tt,np.arange(len(src)),src[:,ch]) for ch in range(2)],1);z/=abs(z).max()+1e-9;z*=.15*np.sin(np.linspace(0,np.pi,len(z)))[:,None]**.8;reverse[a:b]=z

def band(x,a,b):return sosfilt(butter(2,[a,b],fs=SR,btype='bandpass',output='sos'),x)
def low(x,f):return sosfilt(butter(1,f,fs=SR,output='sos'),x)
def felt(d,v,seed):
 n=max(64,round(d*SR));r=np.random.default_rng(seed);x=band(r.standard_normal(n),550,min(5200,1700+v*.45));tooth=low(abs(r.standard_normal(n)),min(500,60+v*.02));tooth/=np.percentile(tooth,90)+1e-9;x*=.55+.45*np.clip(tooth,0,1.6);a=min(n//3,288);b=min(n//3,1200);en=np.ones(n);en[:a]=np.linspace(0,1,a);en[-b:]=np.linspace(1,0,b)**1.5;return x*en*np.clip(v/2500,.35,1)**.7

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
  n=round(e['d']*SR);r=np.random.default_rng(k);tt=np.arange(n)/SR;en=np.sin(np.pi*tt/e['d'])**1.7;z=band(r.standard_normal(n),400,3500)*en;place(z,e['t'],.06)
for t in [67/24,795/24,1278/24]:
 r=np.random.default_rng(round(t*100));tt=np.arange(round(.58*SR))/SR;place(band(r.standard_normal(len(tt)),500,2400)*np.sin(np.pi*tt/.58)**2,t,.05)
env=np.sqrt(np.maximum(0,low(voice[:,0]**2,8)));fx*=np.clip(.065/(env+.018),.35,1)[:,None]
# Quiet material sounds under the explicit full/reduced-form pronunciation comparisons.
fx[round(35.1*SR):round(41*SR)]*=.22
for e in T['segments']:
 if e['kind'] in ['movie','hold','reverse']:fx[round(e['start_frame']*2000):round(e['end_frame']*2000)]=0
fx*=min(1,.15/(abs(fx).max()+1e-9));mix=voice+movie+reverse+fx
# One smooth look-ahead safety pass across the entire master, never per-page normalization.
need=np.minimum(1,.85/(abs(mix).max(axis=1)+1e-9));lim=minimum_filter1d(need,size=481,mode='nearest');mix*=lim[:,None]
for name,z in [('mix',mix),('voice-stem',voice),('movie-stem',movie),('reverse-stem',reverse),('fx-stem',fx)]:sf.write(O/f'{name}.wav',z,SR,subtype='PCM_24')
r={'duration':87,'samples':N,'source_voice_samples':len(vo),'shrek_constant_gain_db':float(20*np.log10(gsh)),'silent_source_cut_seconds':[47.5,48.875],'word_removals':False,'voice_retiming':False,'full_scene_voice_overlap':'final Shrek first 0.5s ambient lead only; actor dialogue starts after voice ends','rewind_frames':[211,225],'first_donkey_repeat_source_frames':[60,93],'music':'none added; film soundtrack retained','peak_dbfs':float(20*np.log10(abs(mix).max())),'safety_limiter_minimum_gain':float(lim.min()),'listening_review':'not performed'};(P/'analysis/mix-report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
