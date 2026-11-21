from pathlib import Path
import json,subprocess,hashlib
import numpy as np,soundfile as sf,soxr
from scipy.signal import butter,sosfilt
from scipy.ndimage import minimum_filter1d
P=Path(__file__).resolve().parents[1];O=P/'out';O.mkdir(exist_ok=True);SR=48000;N=71*SR
E=json.loads((O/'events.json').read_text())['events'];rng=np.random.default_rng(5606)
def ff(args):return subprocess.run(['ffmpeg','-hide_banner','-nostats',*args],capture_output=True,text=True,check=True)
base='highpass=f=70,acompressor=threshold=0.14:ratio=2.5:attack=8:release=120:makeup=1.7'
a=ff(['-i',str(P/'assets/narration.mp3'),'-af',base+',loudnorm=I=-17:TP=-2.5:LRA=6:print_format=json','-f','null','-']).stderr
q=json.loads(a[a.rfind('{'):a.rfind('}')+1]);(O/'voice-firstpass.json').write_text(json.dumps(q,indent=2))
ln=f"loudnorm=I=-17:TP=-2.5:LRA=6:measured_I={q['input_i']}:measured_TP={q['input_tp']}:measured_LRA={q['input_lra']}:measured_thresh={q['input_thresh']}:offset={q['target_offset']}:linear=true"
ff(['-y','-i',str(P/'assets/narration.mp3'),'-af',base+','+ln+',aresample=48000','-c:a','pcm_f32le',str(O/'voice.wav')])
v,sr=sf.read(O/'voice.wav',dtype='float32');assert sr==SR and len(v)==3350361,(sr,len(v));voice=np.pad(v,(0,N-len(v)));fx=np.zeros((N,2),np.float32)
paths={'photo':'foley-paper-slide.wav','slide':'foley-paper-slide.wav','page':'props-page-turn.wav','shutter':'mechanical-shutter-light.wav','applause':'celebration-applause-small.wav','air':'whoosh-fast-soft.wav','stamp':'impact-light-firm.wav'}
cache={};manifest=[]
for n in set(paths.values()):
 p=P/'assets/sfx'/n;x,sr=sf.read(p,dtype='float32',always_2d=True);x=x.mean(axis=1);x=soxr.resample(x,sr,SR) if sr!=SR else x;cache[n]=x;manifest.append({'file':'assets/sfx/'+n,'source':'https://github.com/wyzowl/sfx-kit','license':'CC0-1.0','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'original_duration':len(x)/SR})
(P/'assets/sfx/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
def band(x,a,b):return sosfilt(butter(2,[a,b],fs=SR,btype='bandpass',output='sos'),x)
def low(x,f):return sosfilt(butter(2,f,fs=SR,output='sos'),x)
def synth(ty,d):
 n=round(d*SR);t=np.arange(n)/SR
 if ty=='bell':x=(np.sin(2*np.pi*740*t)+.32*np.sin(2*np.pi*1490*t))*np.exp(-t/ .18)
 elif ty=='ufo':f=1120+850*np.sin(np.pi*t/d);x=np.sin(2*np.pi*np.cumsum(f)/SR)*(.7+.3*np.sin(2*np.pi*17*t))*np.sin(np.pi*t/d)**1.4
 elif ty=='coast':x=low(rng.standard_normal(n),800)*.6+np.sin(2*np.pi*78*t)*.06;x*=np.sin(np.pi*t/d)**1.3
 else:x=band(rng.standard_normal(n),800,4500)*np.exp(-t/.012)
 return x.astype(np.float32)
def place(x,t,gain,pan):
 i=round(t*SR);x=x[:max(0,min(len(x),N-i))]*gain
 if len(x):fx[i:i+len(x)]+=x[:,None]*np.array([np.sqrt((1-pan)/2),np.sqrt((1+pan)/2)])
for k,e in enumerate(E):
 ty=e['type'];d=e['dur']
 if ty in paths:
  x=cache[paths[ty]].copy();active=np.where(abs(x)>.015*max(abs(x).max(),1e-9))[0];a=max(0,int(active[0])-.006*SR) if len(active) else 0;x=x[int(a):];x=x[:round(d*SR)]
 else:x=synth(ty,d)
 if not len(x):continue
 # RMS-normalize short foley, preserve dynamics and fade only effect tails.
 rms=np.sqrt(np.mean(x*x));x=x*(.18/(rms+1e-9));x*=min(1,.72/(abs(x).max()+1e-9));fade=min(len(x)//4,round(.045*SR));x[-fade:]*=np.linspace(1,0,fade)
 pan=[-.18,.12,0,.18][k%4];place(x,e['t'],e['gain']*(.6 if ty=='coast' else 1),pan)
# Smooth sidechain protects bilingual clauses without hiding every effect.
env=np.sqrt(np.maximum(0,low(voice.astype(float)**2,7)));duck=np.clip(.055/(env+.025),.38,1);fx*=duck[:,None]
fxpk=np.max(abs(fx),axis=1);fx*=minimum_filter1d(np.minimum(1,.22/(fxpk+1e-9)),size=241,mode='nearest')[:,None]
mix=voice[:,None]+fx;pk=np.max(abs(mix),axis=1);guard=minimum_filter1d(np.minimum(1,.80/(pk+1e-9)),size=481,mode='nearest');mix*=guard[:,None]
sf.write(O/'mix.wav',mix,SR,subtype='PCM_24');sf.write(O/'effects.wav',fx,SR,subtype='PCM_24')
report={'source_voice_samples':len(v),'duration':71,'tail_samples':N-len(v),'source_complete':True,'retimed':False,'music':False,'event_count':len(E),'peak_dbfs':float(20*np.log10(abs(mix).max()+1e-12)),'effects_peak_dbfs':float(20*np.log10(abs(fx).max()+1e-12)),'listening_review':False,'sfx_source':'Wyzowl SFX Kit CC0 + deterministic synthesized UFO/bell/coastal texture'}
(O/'mix-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
