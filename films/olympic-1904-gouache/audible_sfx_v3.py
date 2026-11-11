"""Audible event-led Foley using CC0 SFX Kit sync points and per-asset speech ducking."""
from pathlib import Path
import json,numpy as np,soundfile as sf
from scipy.signal import butter,sosfilt
from scipy.ndimage import uniform_filter1d,minimum_filter1d
p=Path(__file__).resolve().parent;sr=48000;N=3710*1600;cut_a=2749/30;cut_b=2819/30;removed=70/30
voice,fs=sf.read(p/'out/revision-v3-voice.wav');base,fs2=sf.read(p/'out/revision-v3-sfx.wav');assert fs==fs2==sr and len(voice)==len(base)==N
kit=p/'assets/sfx-kit';catalog={s['id']:s for s in json.loads((kit/'manifest.json').read_text())['sounds']}
fx=base*2;events=[];rng=np.random.default_rng(19040333)
env=uniform_filter1d(abs(voice),size=2400);speech=uniform_filter1d((env>.025).astype(float),size=2400)
def edit_time(source):
 assert not cut_a<=source<cut_b
 return source-removed if source>=cut_b else source
def band(x,lo,hi):return sosfilt(butter(2,[lo,hi],btype='band',fs=sr,output='sos'),x)
def place(name,data,start,duck_db=-2,gain_db=0,visual=None,origin='procedural',sync=0):
 x=np.asarray(data);x=np.repeat(x[:,None],2,axis=1) if x.ndim==1 else x
 j=round(start*sr);trim=max(0,-j);j=max(j,0);x=x[trim:trim+max(0,N-j)]*10**(gain_db/20)
 duck=10**(duck_db/20);x*=((1-speech[j:j+len(x)])+speech[j:j+len(x)]*duck)[:,None]
 fx[j:j+len(x)]+=x;events.append(dict(id=name,edited_start=j/sr,edited_end=(j+len(x))/sr,visual_moment=visual,sync_at=sync,under_voiceover_db=duck_db,gain_db=gain_db,origin=origin))
def asset(name,moment,duration=None,gain_db=2):
 s=catalog[name];x,fs=sf.read(kit/(name+'.wav'));assert fs==sr
 if duration is not None and len(x)>round(duration*sr):
  x=x[:round(duration*sr)].copy();f=min(round(.025*sr),len(x)//4);x[:f]*=np.linspace(0,1,f)[:,None] if x.ndim==2 else np.linspace(0,1,f);x[-f:]*=np.linspace(1,0,f)[:,None] if x.ndim==2 else np.linspace(1,0,f)
 if duration is not None and name.startswith('writing-'):
  x*=.035/max(float(np.sqrt(np.mean(x**2))),1e-9)
  x*=min(1,.32/max(float(np.max(abs(x))),1e-9))
 place(name,x,moment-s['sync']['at'],s['under_voiceover_db'],gain_db,moment,'SFX Kit CC0',s['sync']['at'])
def foot():
 t=np.arange(6000)/sr;z=band(rng.normal(size=len(t)),130,2600)*np.exp(-t*40)+np.sin(2*np.pi*110*t)*np.exp(-t*48)*.3
 z*=.045/np.sqrt(np.mean(z**2));return z
# Directional gravel footfalls: audible in the running shots, not under every scene.
for at in np.arange(.125,7.28,.25):place('running_gravel',foot(),float(at),-2,visual=float(at))
for at in np.arange(58.95,69.35,.28):place('running_gravel',foot(),float(at),-2,visual=float(at))
for at in [77.4,78.25,79.1,80.0]:place('weary_footstep',foot(),at,-3,gain_db=-3,visual=at)
for at in np.arange(85.35,89.4,.48):place('assisted_footstep',foot(),float(at),-3,gain_db=-2,visual=float(at))
# Audible brass-era motor with midrange combustion texture for phone speakers.
d=56.90-49.93;t=np.arange(round(d*sr))/sr;pulse=.22+.78*np.sin(t*90)**8
z=band(rng.normal(size=len(t)),90,1600)*pulse+sum(np.sin(2*np.pi*f*t)*amp for f,amp in [(47,.12),(94,.08),(188,.04)])
z*=np.minimum(t/.2,1)*np.minimum((d-t)/.15,1);z*=.045/np.sqrt(np.mean(z**2));place('period_car_engine',z,49.93,-2,visual=50.7333333333)
for at in [57.0,57.13,57.29]:
 t=np.arange(5280)/sr;z=band(rng.normal(size=len(t)),100,1700)*np.exp(-t*32);z=z/max(abs(z))*.14;place('engine_stall',z,at,-2,visual=at)
for at in [13.95,14.35,14.75,16.15,16.75,17.35]:asset('money-coin-drop',at)
for at in [26.55,27.2,27.85,28.4,28.85,29.05]:asset('props-scissors',at,gain_db=1)
# Ten selected scene changes: different sizes rather than a whoosh on every caption.
for source,name in [(3.6,'whoosh-fast-medium'),(7.3,'whoosh-fast-soft'),(13.7,'whoosh-medium-soft'),(26.2,'whoosh-fast-medium'),(42.7,'whoosh-medium-soft'),(58.7333333333,'whoosh-fast-soft'),(2242/30,'whoosh-medium-soft'),(81,'whoosh-fast-soft'),(2554/30,'whoosh-fast-medium')]:asset(name,edit_time(source),gain_db=1)
asset('whoosh-fast-medium',cut_a,gain_db=1)
data=json.loads((p/'finish-data.json').read_text())
for i,v in enumerate(data['vocab']):asset('writing-chalk-draw' if i%2==0 else 'writing-pencil-draw',edit_time(v['start']),duration=.25,gain_db=3)
asset('writing-pencil-write',edit_time(110.6),duration=.65,gain_db=3)
asset('props-page-turn',edit_time(115.83),gain_db=1)
asset('writing-pencil-draw',edit_time(119.25),duration=.45,gain_db=3)
for i in range(7):asset('keyboard-letter-firm',np.ceil(edit_time(data['typing_start']+i*.085)*30-.00001)/30,gain_db=2)
asset('keyboard-return-firm',np.ceil(edit_time(123.25)*30-.00001)/30,gain_db=2)
# Voice stays ahead: at most half its RMS in active 100 ms windows (-6 dB).
priority=np.ones(N)
for j in range(0,N-4800,2400):
 vr=np.sqrt(np.mean(voice[j:j+4800]**2));fr=np.sqrt(np.mean(fx[j:j+4800]**2))
 if vr>.025 and fr>0:priority[j:j+4800]=np.minimum(priority[j:j+4800],min(1,.50*vr/fr))
fx*=uniform_filter1d(minimum_filter1d(priority,size=1201),size=1200)[:,None]
# Peak protection changes effects only; narrator gain and timing remain untouched.
headroom=np.maximum(.82-abs(voice),.001);ceiling=np.minimum(1,headroom/np.maximum(np.max(abs(fx),axis=1),1e-9))
fx*=minimum_filter1d(ceiling,size=97)[:,None];mix=voice[:,None]+fx
assert np.isfinite(mix).all() and abs(mix).max()<=.820001
sf.write(p/'out/revision-v3-sfx.wav',fx,sr,subtype='PCM_24');sf.write(p/'out/revision-v3-mix.wav',mix,sr,subtype='PCM_24')
# Same absolute 150 ms windows, comparing effects before and after this sound pass.
old,_=sf.read(p/'out/revision-v2-sfx.wav');comparisons=[]
for source,name in [(1.125,'running'),(13.95,'coins'),(53.0,'engine'),(95.4,'chalk'),(119.25,'pencil'),(121.8,'typing')]:
 j=round(edit_time(source)*sr);k=round(source*sr);n=7200;rms_new=float(np.sqrt(np.mean(fx[j:j+n]**2)));rms_old=float(np.sqrt(np.mean(old[k:k+n]**2)));comparisons.append(dict(type=name,source_time=source,edited_time=edit_time(source),effects_RMS_dBFS=round(20*np.log10(max(rms_new,1e-12)),2),gain_vs_v2_dB=round(20*np.log10(rms_new/max(rms_old,1e-12)),2)))
report=dict(kit_source='https://github.com/wyzowl/sfx-kit',license='CC0-1.0',kit_manifest='assets/sfx-kit/manifest.json',placement='visual_moment - sync.at',music='none',narrator_gain_changed=False,maximum_mix_sample_peak=float(abs(mix).max()),old_Foley_gain_dB=6.0206,trimmed_writing_RMS_target_dBFS=-29.12,procedural_footstep_RMS_target_dBFS=-26.94,active_speech_effects_RMS_ceiling_dB=-6.0206,events=events,audibility_comparisons=comparisons)
(p/'sound-design-v3.json').write_text(json.dumps(report,indent=2));print(json.dumps(dict(events=len(events),comparisons=comparisons,peak=report['maximum_mix_sample_peak']),indent=2))
