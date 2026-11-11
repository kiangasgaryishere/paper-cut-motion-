"""Retain the canonical narrator; add sparse editorial sound bridges, no music."""
from pathlib import Path
import json,hashlib,numpy as np,soundfile as sf
from scipy.signal import butter,sosfilt
from scipy.ndimage import uniform_filter1d,minimum_filter1d
p=Path(__file__).resolve().parent;sr=48000;N=126*sr
meta=json.loads((p/'segments.json').read_text())
master=p/'out/voice-master-v2.wav';expected=json.loads((p/'QC-part01-v2.json').read_text())['canonical_voice_master_sha256']
assert hashlib.sha256(master.read_bytes()).hexdigest()==expected
raw,fs=sf.read(master);assert fs==sr;voice=np.pad(raw,(0,N-len(raw)))
original_fx=np.concatenate([sf.read(p/x['effects_wav'])[0] for x in meta['parts']]);assert original_fx.shape==(N,2)
extra=np.zeros_like(original_fx);rng=np.random.default_rng(19042026);events=[]
def band(x,lo,hi):return sosfilt(butter(2,[lo,hi],btype='band',fs=sr,output='sos'),x)
def put(at,x,pan=0,kind='stadium_clap'):
 j=round(at*sr);x=np.asarray(x)[:N-j];extra[j:j+len(x),0]+=x*np.sqrt((1-pan)/2);extra[j:j+len(x),1]+=x*np.sqrt((1+pan)/2)
 events.append(dict(type=kind,start=at,end=at+len(x)/sr,pan=pan))
def clap(gain=.04,d=.18):
 t=np.arange(round(sr*d))/sr;z=band(rng.normal(size=len(t)),500,5200)*np.exp(-t*28);return z/max(abs(z))*gain
def engine(d):
 t=np.arange(round(d*sr))/sr;z=band(rng.normal(size=len(t)),70,1200)*(.3+.7*np.sin(t*90)**8)+np.sin(2*np.pi*47*t)*.12
 return z/max(abs(z))*.035*np.minimum(t/.18,1)*np.minimum((d-t)/.18,1)
# J: the stadium is heard while the opening hook is still on screen.
# L: its last claps continue beneath the exhausted runners rather than stopping at the cut.
for at in np.arange(3.10,7.82,.19):
 gain=.032*(min(1,(at-3.0)/.6))*min(1,max(0,(7.98-at)/.75));put(float(at),clap(gain),float(rng.uniform(-.65,.65)))
# J: a period engine approaches before the car is visible (49.93 -> 50.733 s).
put(49.93,engine(1.10),-.22,'approaching_car_engine')
# L: stadium cheers trail across the officials' reveal, then die away.
for i,at in enumerate([69.32,69.58,69.84,70.10]):put(at,clap(.044*(1-i*.18)),(-1)**i*.4,'fred_applause_tail')
# L: Hicks's celebration gently bridges the story to the teaching board.
for i,at in enumerate([93.65,93.90,94.14,94.35]):put(at,clap(.040*(1-i*.18)),(-1)**i*.4,'hicks_applause_tail')
env=uniform_filter1d(abs(voice),size=2400);extra*=uniform_filter1d(np.where(env>.025,.28,.65),size=1600)[:,None]
fx=original_fx+extra;priority=np.ones(N)
for j in range(0,N-4800,2400):
 vr=np.sqrt(np.mean(voice[j:j+4800]**2));fr=np.sqrt(np.mean(fx[j:j+4800]**2))
 if vr>.025 and fr>0:priority[j:j+4800]=np.minimum(priority[j:j+4800],min(1,.15*vr/fr))
fx*=uniform_filter1d(minimum_filter1d(priority,size=1601),size=1600)[:,None]
mix=voice[:,None]+fx;assert np.isfinite(mix).all() and abs(mix).max()<.90
sf.write(p/'out/revision-v2-sfx.wav',fx,sr,subtype='PCM_24');sf.write(p/'out/revision-v2-mix.wav',mix,sr,subtype='PCM_24')
bridges=[
 dict(type='J',sound='Olympic narration',audio_start=3.416708,visual_cut=3.6,lead=3.6-3.416708),
 dict(type='J',sound='stadium applause',audio_start=3.10,visual_cut=3.6,lead=.5),
 dict(type='J',sound='18 nonfinishers narration',audio_start=7.142125,visual_cut=7.3,lead=7.3-7.142125),
 dict(type='L',sound='stadium applause',visual_cut=7.3,audio_end=7.84,tail=.54),
 dict(type='J',sound='approaching period engine',audio_start=49.93,visual_cut=50.7333333333,lead=.8033333333),
 dict(type='L',sound='Fred applause',visual_cut=69.6,audio_end=70.28,tail=.68),
 dict(type='L',sound='Hicks applause',visual_cut=93.9666666667,audio_end=94.53,tail=.5633333333),
]
(p/'sound-bridges-v2.json').write_text(json.dumps(dict(narration_retimed=False,music='none',bridges=bridges,added_events=events),indent=2))
print('Full 126-second v2 mix; canonical voice unchanged;',len(bridges),'editorial bridges, peak',abs(mix).max())
