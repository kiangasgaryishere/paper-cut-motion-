"""One continuous new Foley mix [40,126), sliced after processing for review parts."""
from pathlib import Path
import json,hashlib,numpy as np,soundfile as sf
from scipy.signal import butter,sosfilt
from scipy.ndimage import uniform_filter1d,minimum_filter1d
p=Path(__file__).resolve().parent;sr=48000;start=40;end=126;N=(end-start)*sr
master=p/'out/voice-master-v2.wav';expected=json.loads((p/'QC-part01-v2.json').read_text())['canonical_voice_master_sha256'];assert hashlib.sha256(master.read_bytes()).hexdigest()==expected
full,fs=sf.read(master);assert fs==sr;voice=np.pad(full,(0,max(0,end*sr-len(full))))[start*sr:end*sr];fx=np.zeros((N,2));events=[];rng=np.random.default_rng(1904126)
def band(x,lo,hi):return sosfilt(butter(2,[lo,hi],btype='band',fs=sr,output='sos'),x)
def emit(name,x,at,gain=1,pan=0):
 i=round((at-start)*sr);x=np.asarray(x)[:max(0,N-i)]*gain;fx[i:i+len(x),0]+=x*np.sqrt((1-pan)/2);fx[i:i+len(x),1]+=x*np.sqrt((1+pan)/2);events.append(dict(type=name,absolute_start=round(at,6),absolute_end=round(at+len(x)/sr,6),gain=gain,pan=pan))
def paper(d=.35):
 t=np.arange(round(d*sr))/sr;z=band(rng.normal(size=len(t)),500,4200)*np.sin(np.pi*t/d)**2;return z/max(abs(z))*.07
def foot():
 t=np.arange(round(.12*sr))/sr;z=band(rng.normal(size=len(t)),120,2500)*np.exp(-t*40)+np.sin(2*np.pi*95*t)*np.exp(-t*55)*.2;return z/max(abs(z))*.10
def engine(d):
 t=np.arange(round(d*sr))/sr;z=band(rng.normal(size=len(t)),70,1400)*(.25+.75*np.sin(t*90)**8);z+=np.sin(2*np.pi*47*t)*.12;env=np.minimum(t/.15,1)*np.minimum((d-t)/.20,1);return z/max(abs(z))*.035*env
def chalk(d=.23):
 t=np.arange(round(d*sr))/sr;z=band(rng.normal(size=len(t)),1200,6500)*np.sin(np.pi*t/d)**2*(.3+.7*np.sin(t*83)**2);return z/max(abs(z))*.09
def tap():
 t=np.arange(round(.07*sr))/sr;z=band(rng.normal(size=len(t)),1800,7000)*np.exp(-t*90)+np.sin(2*np.pi*1700*t)*np.exp(-t*130)*.10;return z/max(abs(z))*.08
def clap():
 t=np.arange(round(.16*sr))/sr;z=band(rng.normal(size=len(t)),500,6500)*np.exp(-t*25);return z/max(abs(z))*.07
# Outdoor air is ambience only; no music/drone or long tonal effects.
d=54;t=np.arange(d*sr)/sr;air=band(rng.normal(size=len(t)),160,1300)*.002;emit('outdoor_air',air,40)
emit('new_runner_clothes',paper(),42.70,.55)
for at in [45.15,46.5]:emit('cramped_leg_cloth',paper(.22),at,.5)
emit('car_engine_pre_lap',engine(6.55),50.55,.7)
for k,at in enumerate([57.0,57.13,57.29]):emit('engine_stall_'+str(k+1),engine(.11),at,.9)
emit('stalled_car_clunk',foot(),57.48,.7)
emit('car_exit_cloth',paper(.32),58.70,.7)
for at in np.arange(58.95,69.35,.28):emit('running_footstep',foot(),float(at),.36,pan=.15)
for at in [67.7,68.08,68.45,68.82]:emit('spectator_clap',clap(),at,.55,pan=-.3)
emit('official_clipboard',paper(.4),69.55,.75)
emit('truth_revealed_paper',paper(.25),73.29,.6)
for at in [77.4,78.25,79.1,80.0]:emit('weary_step',foot(),at,.32)
# No musical suspense bed during the hallucination: speech carries this turn.
for at in np.arange(85.35,89.4,.48):emit('assisted_finish_step',foot(),float(at),.4)
emit('finish_ribbon_cloth',paper(.45),88.75,.8)
for at in [91.8,92.05,92.32,92.6]:emit('winner_applause',clap(),at,.7)
data=json.loads((p/'finish-data.json').read_text())
for v in data['vocab']:emit('chalk_'+v['en'].lower().replace(' ','_'),chalk(),v['start'],.7)
emit('lesson_combination_chalk',chalk(.35),110.6,.75)
emit('worksheet_page',paper(.55),115.83,.7)
emit('practice_pencil',chalk(.4),119.25,.6)
for i in range(7):emit('cta_key_'+str(i+1),tap(),data['typing_start']+i*.085,.7)
emit('comment_send',tap(),123.25,.8)
env=uniform_filter1d(abs(voice),size=2400);fx*=uniform_filter1d(np.where(env>.025,.28,.65),size=1600)[:,None]
priority=np.ones(N)
for j in range(0,N-4800,2400):
 vr=np.sqrt(np.mean(voice[j:j+4800]**2));fr=np.sqrt(np.mean(fx[j:j+4800]**2))
 if vr>.025 and fr>0:priority[j:j+4800]=np.minimum(priority[j:j+4800],min(1,.16*vr/fr))
fx*=uniform_filter1d(minimum_filter1d(priority,size=1601),size=1600)[:,None];fx*=np.minimum(np.arange(N)/sr/.025,1)[:,None]*np.minimum((N-np.arange(N))/sr/.1,1)[:,None]
mix=voice[:,None]+fx;assert np.isfinite(mix).all() and abs(mix).max()<.9
for index,a in enumerate(range(40,126,10),5):
 b=min(a+10,126);j=(a-40)*sr;k=(b-40)*sr;sf.write(p/f'out/part{index:02d}-mix-v1.wav',mix[j:k],sr,subtype='PCM_24');sf.write(p/f'out/part{index:02d}-sfx-v1.wav',fx[j:k],sr,subtype='PCM_24')
(p/'sound-events-finish.json').write_text(json.dumps(events,indent=2));print(len(events),'nonmusical effects; canonical voice preserved, final tail silence',end-len(full)/sr,'seconds.')
