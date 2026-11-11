"""Exact source interval [20,30), using the already approved full voice master."""
from pathlib import Path
import json,hashlib,numpy as np,soundfile as sf
from scipy.signal import butter,sosfilt
from scipy.ndimage import uniform_filter1d,minimum_filter1d
p=Path(__file__).resolve().parent;sr=48000;N=10*sr
master=p/'out/voice-master-v2.wav';expected=json.loads((p/'QC-part01-v2.json').read_text())['canonical_voice_master_sha256'];assert hashlib.sha256(master.read_bytes()).hexdigest()==expected,'Canonical voice changed; do not reset gain between parts.'
full,fs=sf.read(master);assert fs==sr and len(full)>=30*sr;voice=full[20*sr:30*sr];fx=np.zeros((N,2));events=[];rng=np.random.default_rng(190403)
def band(x,lo,hi):return sosfilt(butter(2,[lo,hi],btype='band',fs=sr,output='sos'),x)
def emit(name,x,absolute,gain=1,pan=0):
 i=round((absolute-20)*sr);x=np.asarray(x)[:max(0,N-i)]*gain;fx[i:i+len(x),0]+=x*np.sqrt((1-pan)/2);fx[i:i+len(x),1]+=x*np.sqrt((1+pan)/2);events.append(dict(type=name,absolute_start=absolute,absolute_end=absolute+len(x)/sr,gain=gain,pan=pan))
def cloth(d=.3):
 t=np.arange(round(d*sr))/sr;z=band(rng.normal(size=len(t)),450,3800)*np.sin(np.pi*t/d)**2;return z/max(abs(z))*.06
def snip():
 t=np.arange(round(.105*sr))/sr;n=band(rng.normal(size=len(t)),1600,7500)*np.exp(-t*60);metal=np.sin(2*np.pi*2350*t)*np.exp(-t*85)*.12;z=n+metal;return z/max(abs(z))*.12
def drop():
 t=np.arange(round(.18*sr))/sr;z=band(rng.normal(size=len(t)),100,1100)*np.exp(-t*26);return z/max(abs(z))*.055
t=np.arange(N)/sr;air=band(rng.normal(size=N),160,1500)*.0025;fx[:,0]+=air;fx[:,1]+=air*.93
emit('long_clothes_rustle',cloth(.35),20.4,gain=.75)
emit('showed_up_clothes_accent',cloth(.24),725/30,gain=.55)
emit('tailoring_cloth_pre_lap',cloth(.45),26.02,gain=.65,pan=-.25)
for k,at in enumerate([26.55,27.2,27.85,28.4,28.85,29.05]):emit('scissor_snip_'+str(k+1),snip(),at,gain=.78,pan=-.15)
for k,at in enumerate([28.9,29.1]):emit('cut_fabric_flap_'+str(k+1),cloth(.25),at,gain=.65,pan=.1+k*.25)
for k,at in enumerate([29.5,29.7]):emit('cloth_lands_'+str(k+1),drop(),at,gain=.65,pan=.1+k*.25)
env=uniform_filter1d(abs(voice),size=2400);duck=uniform_filter1d(np.where(env>.025,.28,.65),size=1600);fx*=duck[:,None]
priority=np.ones(N)
for j in range(0,N-4800,2400):
 vr=np.sqrt(np.mean(voice[j:j+4800]**2));fr=np.sqrt(np.mean(fx[j:j+4800]**2))
 if vr>.025 and fr>0:priority[j:j+4800]=np.minimum(priority[j:j+4800],min(1,.16*vr/fr))
fx*=uniform_filter1d(minimum_filter1d(priority,size=1601),size=1600)[:,None]
# Fade effects at the segment edges, never the continuous narrator.
fx*=np.minimum(np.arange(N)/sr/.025,1)[:,None]*np.minimum((N-np.arange(N))/sr/.10,1)[:,None]
mix=voice[:,None]+fx;assert np.isfinite(mix).all() and abs(mix).max()<.9
sf.write(p/'out/part03-sfx-v1.wav',fx,sr,subtype='PCM_24');sf.write(p/'out/part03-mix-v1.wav',mix,sr,subtype='PCM_24');(p/'sound-events-part03-v1.json').write_text(json.dumps(events,indent=2));print(len(events),'effects; source [20,30), unchanged voice gain; no music.')
