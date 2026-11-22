"""Mix source narration and paper/fabric foley at the picture cue times."""
import json
from pathlib import Path
import subprocess
import numpy as np
from scipy.signal import butter, sosfilt, resample_poly
from scipy.ndimage import maximum_filter1d
import soundfile as sf

project = Path(__file__).resolve().parents[1]
out = project / 'out'
rate = 48000
samples = rate * 93
source = project / 'assets/narration.mp3'
def ffmpeg(*args):
    return subprocess.run(['ffmpeg','-hide_banner','-nostats',*args],
                          check=True, capture_output=True, text=True).stderr

base = 'highpass=f=65,acompressor=threshold=0.15:ratio=2:attack=8:release=130'
meter = ffmpeg('-i',str(source),'-af',base+',loudnorm=I=-17:TP=-2.5:LRA=7:print_format=json','-f','null','-')
measured = json.loads(meter[meter.rfind('{'):meter.rfind('}')+1])
norm = 'loudnorm=I=-17:TP=-2.5:LRA=7:linear=true'
for key in ('I','TP','LRA','thresh'):
    norm += f':measured_{key}={measured["input_"+key.lower()]}'
norm += ':offset='+measured['target_offset']
ffmpeg('-y','-i',str(source),'-af',base+','+norm+',aresample=48000',
       '-c:a','pcm_f32le',str(out/'voice.wav'))
voice, sr = sf.read(out/'voice.wav',dtype='float32')
assert sr == rate and len(voice) == 4419555
voice = np.pad(voice,(0,samples-len(voice)))
fx = np.zeros((samples,2),np.float32)
timeline = json.loads((project/'timeline.json').read_text())
sounds = {'page':'props-page-turn','fabric':'foley-fabric-touch',
          'card':'foley-card-touch','slide':'foley-paper-slide'}
def apply(cue, kind, gain, pan):
    audio, sr = sf.read(project/f'assets/sfx/{sounds[kind]}.wav',always_2d=True)
    x = audio.mean(axis=1)
    if sr != rate:
        import math
        gcd = math.gcd(sr,rate)
        x = resample_poly(x,rate//gcd,sr//gcd)
    active = np.flatnonzero(np.abs(x)>.02*np.max(np.abs(x)))
    x = x[max(0,active[0]-240):][:int(.52*rate)]
    length = min(1920,len(x)//4)
    x[-length:] *= np.linspace(1,0,length)
    x *= gain/(np.max(np.abs(x))+1e-9)
    i = round(cue*rate)
    fx[i:i+len(x)] += x[:,None]*np.sqrt([(1-pan)/2,(1+pan)/2])

for n,shot in enumerate(timeline['shots'][1:],1):
    if n%4==0 or shot['kind'] in ('compare','choice','cta'):
        apply(shot['start']-.11,'page',.15,.05)
    elif shot['kind'] in ('loom','swatch','rug'):
        apply(shot['start']+.22,'fabric',.105,-.16)
    else:
        apply(shot['start']-.07,'slide',.12,.19)
for t in [1.62,42.44,43.09,43.74,46.24,70.38,71,89.71]:
    apply(t,'card',.18,.02)
envelope = np.sqrt(np.maximum(0,sosfilt(butter(2,7,fs=rate,output='sos'),voice**2)))
fx *= np.clip(.06/(envelope+.028),.42,1)[:,None]
mix = voice[:,None]+fx
peak = maximum_filter1d(np.max(np.abs(mix),axis=1),size=245)
mix *= np.minimum(1,.80/(peak+1e-9))[:,None]
sf.write(out/'mix.wav',mix,rate,subtype='PCM_24')
print('Source kept: 4,419,555 samples. Mixed 93 seconds, no score.')
