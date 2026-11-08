from pathlib import Path
import sys,json,numpy as np,soundfile as sf
from scipy.ndimage import maximum_filter1d,uniform_filter1d
sys.path.insert(0,'core/audio');import sfx
p=Path('films/a-the-kings/production');voice,sr=sf.read(p/'voice.wav');assert sr==48000
length=round(72.744*sr);voice=np.pad(voice,(0,max(0,length-len(voice))))[:length]
# Keep the recording's timing; only a uniform gain and final loudness normalization are applied.
voice=voice*(.78/max(.01,np.abs(voice).max()));fx=np.zeros((length,2),dtype=np.float32)
shots=json.loads((p/'scenes.json').read_text());events=[]
for i,s in enumerate(shots):
 t=s['start']+.5
 if i in [9,11,12,13,14,15,16]:continue
 if i in [5,10]:x=sfx.clack(.75)*.4;at=t+.65
 elif i in [6,8]:x=sfx.whoosh(.5)*.18;at=t
 elif i in [1,7,17]:x=sfx.whoosh(.3)*.17;at=t+.1
 else:x=sfx.click(.8)*.14;at=t+.2
 sfx.add(fx,x,at,gain=1,pan=(i%3-1)*.25);events.append(dict(t=at,scene=i+1,type='paper/contact'))
# Reduce the sound effects beneath active speech, preserving every word.
env=uniform_filter1d(np.abs(voice),size=2400);duck=np.where(env>.025,.38,.75)
fx*=duck[:,None];out=np.repeat(voice[:,None],2,axis=1)+fx
peak=np.abs(out).max()
if peak>.96:out*=.96/peak
assert np.isfinite(out).all()
sf.write(p/'sfx.wav',fx,sr,subtype='PCM_24');sf.write(p/'mix.wav',out,sr,subtype='PCM_24')
(p/'sound-events.json').write_text(json.dumps(events,indent=2))
print('Mixed original voice +',len(events),'procedural SFX, no music;',len(out)/sr,'seconds; peak',np.abs(out).max())
