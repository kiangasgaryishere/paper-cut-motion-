"""Narrator-first mix of exact absolute samples [0,480000)."""
from pathlib import Path
import json,numpy as np,soundfile as sf
from scipy.signal import butter,sosfilt
from scipy.ndimage import uniform_filter1d,minimum_filter1d
p=Path(__file__).resolve().parent;sr=48000;N=10*sr
full,fs=sf.read(p/'out/voice-master-v2.wav');assert fs==sr and len(full)>=N
voice=full[:N];rng=np.random.default_rng(1904);fx=np.zeros((N,2));events=[]
def band(x,lo,hi):return sosfilt(butter(2,[lo,hi],btype='band',fs=sr,output='sos'),x)
def put(at,x,gain=1,pan=0,kind='footstep'):
 i=round(at*sr);x=x[:max(0,N-i)]*gain;fx[i:i+len(x),0]+=x*np.sqrt((1-pan)/2);fx[i:i+len(x),1]+=x*np.sqrt((1+pan)/2);events.append(dict(type=kind,at=round(at,6),gain=gain))
def foot(at,gain,pan):
 t=np.arange(round(.115*sr))/sr;x=band(rng.normal(size=len(t)),100,2700)*np.exp(-t*43)+np.sin(2*np.pi*92*t)*np.exp(-t*55)*.45;x=x/max(abs(x))*.16;put(at,x,gain,pan)
# Faint outdoor air; never a music bed.
t=np.arange(N)/sr;air=band(rng.normal(size=N),160,1500)*.004*(.6+.4*np.sin(t*.8)**2);fx[:,0]+=air;fx[:,1]+=air*.93
for at in np.arange(.125,10,.25):foot(float(at),.18 if at<101/30 else .36,float(np.sin(at*.6)*.25))
# One restrained starting crack as the marathon shot appears, below the voice.
t=np.arange(11040)/sr;x=band(rng.normal(size=len(t)),500,7200)*np.exp(-t*54)+.15*np.sin(2*np.pi*135*t)*np.exp(-t*25);x=x/max(abs(x))*.07;put(176/30,x,kind='soft_starter_crack')
env=uniform_filter1d(abs(voice),size=2400);duck=uniform_filter1d(np.where(env>.025,.28,.65),size=1600);fx*=duck[:,None]
priority=np.ones(N)
for j in range(0,N-4800,2400):
 vr=np.sqrt(np.mean(voice[j:j+4800]**2));fr=np.sqrt(np.mean(fx[j:j+4800]**2))
 if vr>.025 and fr>0:priority[j:j+4800]=np.minimum(priority[j:j+4800],min(1,.16*vr/fr))
fx*=uniform_filter1d(minimum_filter1d(priority,size=1601),size=1600)[:,None]
# Fade effects only. Narration is never faded/repeated at a ten-second boundary.
fx*=np.minimum(np.arange(N)/sr/.025,1)[:,None]*np.minimum((N-np.arange(N))/sr/.10,1)[:,None]
mix=np.repeat(voice[:,None],2,axis=1)+fx;assert np.isfinite(mix).all() and abs(mix).max()<.90
sf.write(p/'out/part01-sfx-v2.wav',fx,sr,subtype='PCM_24');sf.write(p/'out/part01-mix-v2.wav',mix,sr,subtype='PCM_24');(p/'sound-events-part01-v2.json').write_text(json.dumps(events,indent=2))
meta=json.loads((p/'segments.json').read_text());meta['source_decoded_duration']=len(full)/sr;meta['parts'][0]['source_sample_start']=0;meta['parts'][0]['source_sample_end_exclusive']=N;meta['parts'][0]['video_frame_start']=0;meta['parts'][0]['video_frame_end_exclusive']=300;(p/'segments.json').write_text(json.dumps(meta,indent=2))
print('First 480000 narration samples mixed, with voice priority; no music. Peak:',float(abs(mix).max()))
