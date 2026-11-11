"""Exact source interval [10,20), using the already approved full voice master."""
from pathlib import Path
import json,hashlib,numpy as np,soundfile as sf
from scipy.signal import butter,sosfilt
from scipy.ndimage import uniform_filter1d,minimum_filter1d
p=Path(__file__).resolve().parent;sr=48000;N=10*sr
master=p/'out/voice-master-v2.wav';expected=json.loads((p/'QC-part01-v2.json').read_text())['canonical_voice_master_sha256'];assert hashlib.sha256(master.read_bytes()).hexdigest()==expected,'Canonical voice changed; do not reset gain between parts.'
full,fs=sf.read(master);assert fs==sr and len(full)>=20*sr;voice=full[10*sr:20*sr];fx=np.zeros((N,2));events=[];rng=np.random.default_rng(190402)
def band(x,lo,hi):return sosfilt(butter(2,[lo,hi],btype='band',fs=sr,output='sos'),x)
def emit(name,x,absolute,gain=1,pan=0):
 i=round((absolute-10)*sr);x=np.asarray(x)[:max(0,N-i)]*gain;fx[i:i+len(x),0]+=x*np.sqrt((1-pan)/2);fx[i:i+len(x),1]+=x*np.sqrt((1+pan)/2);events.append(dict(type=name,absolute_start=absolute,absolute_end=absolute+len(x)/sr,gain=gain,pan=pan))
def clink(pitch=1):
 t=np.arange(round(.22*sr))/sr;z=sum(a*np.sin(2*np.pi*f*pitch*t)*np.exp(-t/tau) for a,f,tau in [(1,1890,.025),(.5,3025,.041),(.22,4720,.052)]);z+=band(rng.normal(size=len(t)),1800,7000)*np.exp(-t*100)*.12;return z/max(abs(z))*.13
def cloth(d=.3):
 t=np.arange(round(d*sr))/sr;z=band(rng.normal(size=len(t)),450,3800)*np.sin(np.pi*t/d)**2;return z/max(abs(z))*.06
# Outdoor air follows the actual outdoor shots, then gives way to the table.
t=np.arange(N)/sr;air=band(rng.normal(size=N),160,1500)*.003;air*=np.where(t<5.966667,1,0);fx[:,0]+=air;fx[:,1]+=air*.93
emit('portrait_cloth',cloth(),10.40,gain=.6)
# A small J-cut: dock rope precedes the harbor picture by 0.18 seconds.
emit('dock_rope_pre_lap',cloth(.55),13.52,gain=.6,pan=.35)
for k,at in enumerate([13.95,14.35,14.75]):emit('travel_fund_coin_'+str(k+1),clink(.95+k*.06),at,gain=.75,pan=.25)
# A brief dry dice/table rattle, followed by three coins leaving the frame.
z=np.zeros(round(.34*sr))
for at in [.00,.06,.14,.23]:
 d=.065;tt=np.arange(round(d*sr))/sr;x=band(rng.normal(size=len(tt)),400,4500)*np.exp(-tt*65);x=x/max(abs(x))*.05;j=round(at*sr);z[j:j+len(x)]+=x
emit('dice_table_rattle',z,479/30,gain=.75,pan=-.3)
for k,at in enumerate([16.15,16.75,17.35]):emit('lost_coin_'+str(k+1),clink(1.03-k*.08),at,gain=.85,pan=.3+k*.15)
emit('empty_purse_leather',cloth(.35),18.05,gain=.6)
env=uniform_filter1d(abs(voice),size=2400);duck=uniform_filter1d(np.where(env>.025,.28,.65),size=1600);fx*=duck[:,None]
priority=np.ones(N)
for j in range(0,N-4800,2400):
 vr=np.sqrt(np.mean(voice[j:j+4800]**2));fr=np.sqrt(np.mean(fx[j:j+4800]**2))
 if vr>.025 and fr>0:priority[j:j+4800]=np.minimum(priority[j:j+4800],min(1,.16*vr/fr))
fx*=uniform_filter1d(minimum_filter1d(priority,size=1601),size=1600)[:,None]
# Fade effects at the segment edges, never the continuous narrator.
fx*=np.minimum(np.arange(N)/sr/.025,1)[:,None]*np.minimum((N-np.arange(N))/sr/.10,1)[:,None]
mix=voice[:,None]+fx;assert np.isfinite(mix).all() and abs(mix).max()<.9
sf.write(p/'out/part02-sfx-v1.wav',fx,sr,subtype='PCM_24');sf.write(p/'out/part02-mix-v1.wav',mix,sr,subtype='PCM_24');(p/'sound-events-part02-v1.json').write_text(json.dumps(events,indent=2));print(len(events),'effects; source [10,20), unchanged voice gain; no music.')
