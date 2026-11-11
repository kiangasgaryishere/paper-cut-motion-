"""Exact source interval [30,40), using the already approved full voice master."""
from pathlib import Path
import json,hashlib,numpy as np,soundfile as sf
from scipy.signal import butter,sosfilt
from scipy.ndimage import uniform_filter1d,minimum_filter1d
p=Path(__file__).resolve().parent;sr=48000;N=10*sr
master=p/'out/voice-master-v2.wav';expected=json.loads((p/'QC-part01-v2.json').read_text())['canonical_voice_master_sha256'];assert hashlib.sha256(master.read_bytes()).hexdigest()==expected,'Canonical voice changed; do not reset gain between parts.'
full,fs=sf.read(master);assert fs==sr and len(full)>=40*sr;voice=full[30*sr:40*sr];fx=np.zeros((N,2));events=[];rng=np.random.default_rng(190404)
def band(x,lo,hi):return sosfilt(butter(2,[lo,hi],btype='band',fs=sr,output='sos'),x)
def emit(name,x,absolute,gain=1,pan=0):
 i=round((absolute-30)*sr);x=np.asarray(x)[:max(0,N-i)]*gain;fx[i:i+len(x),0]+=x*np.sqrt((1-pan)/2);fx[i:i+len(x),1]+=x*np.sqrt((1+pan)/2);events.append(dict(type=name,absolute_start=absolute,absolute_end=absolute+len(x)/sr,gain=gain,pan=pan))
def cloth(d=.3):
 t=np.arange(round(d*sr))/sr;z=band(rng.normal(size=len(t)),450,3800)*np.sin(np.pi*t/d)**2;return z/max(abs(z))*.06
def crunch():
 d=.27;t=np.arange(round(d*sr))/sr;z=band(rng.normal(size=len(t)),700,6800)*np.exp(-t*13)*(.2+.8*np.sin(t*108)**4);return z/max(abs(z))*.12
def settle():
 d=.30;t=np.arange(round(d*sr))/sr;z=band(rng.normal(size=len(t)),100,1700)*np.exp(-t*15);return z/max(abs(z))*.06
def grumble():
 d=.55;t=np.arange(round(d*sr))/sr;z=band(rng.normal(size=len(t)),75,240)*(np.sin(np.pi*t/d)**2)*(.6+.4*np.sin(t*29));return z/max(abs(z))*.045
t=np.arange(N)/sr;air=band(rng.normal(size=N),160,1500)*.0025;fx[:,0]+=air;fx[:,1]+=air*.93
emit('finished_hem_cloth',cloth(.25),30.40,gain=.6)
emit('orchard_leaves_pre_lap',cloth(.55),32.28,gain=.6,pan=-.4)
emit('spoiled_apple_bite',crunch(),34.18,gain=.8,pan=-.15)
emit('soft_stomach_grumble',grumble(),35.15,gain=.65)
emit('grass_settle',settle(),36.25,gain=.75,pan=-.25)
emit('resting_shirt_rustle',cloth(.35),36.50,gain=.6)
emit('leaf_gust',cloth(.5),37.70,gain=.5,pan=-.4)
emit('lie_down_cloth_accent',cloth(.3),38.50,gain=.5)
env=uniform_filter1d(abs(voice),size=2400);duck=uniform_filter1d(np.where(env>.025,.28,.65),size=1600);fx*=duck[:,None]
priority=np.ones(N)
for j in range(0,N-4800,2400):
 vr=np.sqrt(np.mean(voice[j:j+4800]**2));fr=np.sqrt(np.mean(fx[j:j+4800]**2))
 if vr>.025 and fr>0:priority[j:j+4800]=np.minimum(priority[j:j+4800],min(1,.16*vr/fr))
fx*=uniform_filter1d(minimum_filter1d(priority,size=1601),size=1600)[:,None]
# Fade effects at the segment edges, never the continuous narrator.
fx*=np.minimum(np.arange(N)/sr/.025,1)[:,None]*np.minimum((N-np.arange(N))/sr/.10,1)[:,None]
mix=voice[:,None]+fx;assert np.isfinite(mix).all() and abs(mix).max()<.9
sf.write(p/'out/part04-sfx-v1.wav',fx,sr,subtype='PCM_24');sf.write(p/'out/part04-mix-v1.wav',mix,sr,subtype='PCM_24');(p/'sound-events-part04-v1.json').write_text(json.dumps(events,indent=2));print(len(events),'effects; source [30,40), unchanged voice gain; no music.')
