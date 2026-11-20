"""Source-timed voice + native Whiteboard foley. Never trims or retimes speech."""
from pathlib import Path
import subprocess,json,runpy
import numpy as np
import soundfile as sf
from scipy.signal import butter,sosfilt
from scipy.ndimage import minimum_filter1d
P=Path(__file__).resolve().parents[1];O=P/'out';O.mkdir(exist_ok=True);SR=48000;N=76*SR
fxlib=runpy.run_path(str(P/'tools/native-foley.py'))
def ff(args):return subprocess.run(['ffmpeg','-hide_banner','-nostats',*args],capture_output=True,text=True,check=True)
base='highpass=f=70,acompressor=threshold=0.12:ratio=3:attack=8:release=120:makeup=2'
# Mono target -17 gives approximately -14 LUFS after identical center voice goes to stereo.
a=ff(['-i',str(P/'assets/narration.mp3'),'-af',base+',loudnorm=I=-17:TP=-2:LRA=6:print_format=json','-f','null','-']).stderr
q=json.loads(a[a.rfind('{'):a.rfind('}')+1]);(O/'voice-firstpass.json').write_text(json.dumps(q,indent=2))
ln=f"loudnorm=I=-17:TP=-2:LRA=6:measured_I={q['input_i']}:measured_TP={q['input_tp']}:measured_LRA={q['input_lra']}:measured_thresh={q['input_thresh']}:offset={q['target_offset']}:linear=true"
ff(['-y','-i',str(P/'assets/narration.mp3'),'-af',base+','+ln+',aresample=48000','-c:a','pcm_f32le',str(O/'voice.wav')])
v,sr=sf.read(O/'voice.wav',dtype='float32');assert sr==SR and len(v)==3604000,(sr,len(v))
voice=np.pad(v,(0,N-len(v)));fx=np.zeros((N,2),np.float32)
E=json.loads((O/'events.json').read_text());keys=E['camera']
def camera(t):
 for a,b in zip(keys,keys[1:]):
  if a['t']<=t<=b['t']:
   u=(t-a['t'])/(b['t']-a['t']);u=u*u*(3-2*u)
   return {k:a[k]+(b[k]-a[k])*u for k in ['x','y','z']}
 return keys[0] if t<keys[0]['t'] else keys[-1]
def place(x,t,gain,pan=0):
 i=round(t*SR);x=np.asarray(x,np.float32)
 if i<0:x=x[-i:];i=0
 x=x[:max(0,min(len(x),N-i))]*gain
 if len(x):fx[i:i+len(x)]+=x[:,None]*np.array([np.sqrt((1-pan)/2),np.sqrt((1+pan)/2)])
for e in E['events']:
 ty=e['type'];t=e['t'];c=camera(t);x=e.get('x',c['x']);y=e.get('y',c['y']);sx=540+(x-c['x'])*c['z'];sy=960+(y-c['y'])*c['z'];on=-80<sx<1160 and -100<sy<1460
 pan=float(np.clip((sx/1080-.5)*.9,-.6,.6));gain=.38 if on else .10
 if ty in ('write','stroke','dash'):
  snd=fxlib['marker'](e['dur'],e['len'],ty,{'coal':'black','coral':'orange'}.get(e['pen'],e['pen']),c['z']);place(snd,t,gain*(.8 if ty=='write' else 1),pan)
 elif ty=='tap':place(fxlib['tap'](c['z']),t,gain*.7,pan)
 elif ty=='erase':place(fxlib['eraser'](e['dur']),t,.28,0)
 elif ty=='cap':place(fxlib['cap_pop'](),t,.09,.15)
 elif ty=='magnet':place(fxlib['magnet'](),t,.22,pan)
for t in [5.7,19.2,31.2,42.9,53.9,66.5,69.4]:place(fxlib['whoosh'](.55,.35),t,.20)
# A smooth speech sidechain and effects-only peak guard keep the supplied voice intelligible.
def low(x,f):return sosfilt(butter(2,f,fs=SR,output='sos'),x)
env=np.sqrt(np.maximum(0,low(voice.astype(float)**2,6)));duck=np.clip(.035/(env+.015),.28,1);fx*=duck[:,None]
fx*=min(1,.15/(np.max(np.abs(fx))+1e-9))
mix=voice[:,None]+fx
pk=np.max(abs(mix),axis=1);gain=minimum_filter1d(np.minimum(1,.82/(pk+1e-9)),size=481,mode='nearest');mix*=gain[:,None]
sf.write(O/'effects.wav',fx,SR,subtype='PCM_24');sf.write(O/'mix.wav',mix,SR,subtype='PCM_24')
report={'sample_rate':SR,'duration':76,'source_voice_samples':len(v),'tail_samples':N-len(v),'voice_complete':True,'retiming':False,'music':False,'events':len(E['events']),'effects_peak_dbfs':float(20*np.log10(np.max(abs(fx))+1e-12)),'mix_peak_dbfs':float(20*np.log10(np.max(abs(mix))+1e-12)),'min_safety_gain_db':float(20*np.log10(gain.min())),'listening_review':'not performed; objective measurements and source timing only'}
(O/'mix-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
