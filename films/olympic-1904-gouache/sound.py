from pathlib import Path
import numpy as np,soundfile as sf
from scipy.signal import butter,sosfilt
p=Path(__file__).parent;sr=48000;N=10*sr;rng=np.random.default_rng(1904);mix=np.zeros((N,2));events=[]
def band(x,lo,hi):return sosfilt(butter(2,[lo,hi],btype='band',fs=sr,output='sos'),x)
def put(at,x,gain=1,pan=0):
 i=round(at*sr);x=x[:max(0,N-i)]*gain;mix[i:i+len(x),0]+=x*np.sqrt((1-pan)/2);mix[i:i+len(x),1]+=x*np.sqrt((1+pan)/2)
def foot(at,gain,pan):
 d=.115;t=np.arange(round(d*sr))/sr;x=band(rng.normal(size=len(t)),100,2700)*np.exp(-t*43)+np.sin(2*np.pi*92*t)*np.exp(-t*55)*.45;x=x/max(abs(x))*.24;put(at,x,gain,pan);events.append({'type':'dirt_footstep','at':round(at,4)})
# Soft outdoor air, no score and no synthetic speech.
t=np.arange(N)/sr;air=band(rng.normal(size=N),160,1500);air*=.006*(.6+.4*np.sin(t*.8)**2);air*=np.minimum(t/.18,1)*np.minimum((10-t)/.28,1);mix[:,0]+=air;mix[:,1]+=air*.93
for at in np.arange(.2,3,.392699):foot(float(at),.20,-.2)
# Main runner's foot contacts coincide with the second/fourth painted poses.
for at in np.arange(3.125,6,.25):foot(float(at),.70,float(np.sin(at)*.3))
for at in np.arange(6.15,9.9,.4):foot(float(at),.14,.25)
# One brief starter-pistol-like crack on the hard cut to the race, with a short tail.
t=np.arange(11040)/sr;x=band(rng.normal(size=len(t)),500,7200)*np.exp(-t*54);x+=.15*np.sin(2*np.pi*135*t)*np.exp(-t*25);x=x/max(abs(x))*.18;put(3,x);events.append({'type':'starter_crack','at':3})
mix*=np.minimum(np.arange(N)/sr/.04,1)[:,None]*np.minimum((N-np.arange(N))/sr/.18,1)[:,None];assert np.isfinite(mix).all();sf.write(p/'out/sound.wav',mix,sr,subtype='PCM_24')
import json;(p/'sound-events.json').write_text(json.dumps(events,indent=2));print('10 seconds, stereo 48kHz, sound effects only; peak',float(abs(mix).max()))
