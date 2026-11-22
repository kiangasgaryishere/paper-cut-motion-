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

# (Cue time, material, gain, pan). Landings use the contact frame.
cues = [
    (.13,'fabric',.22,-.10), (1.70,'card',.25,.08),
    (4.17,'slide',.17,.06), (5.69,'fabric',.22,.14),
    (6.72,'page',.22,0), (8.05,'slide',.17,.10),
    (11.08,'slide',.155,-.14), (12.03,'slide',.155,.14), (12.98,'slide',.155,-.14),
    (14.33,'slide',.13,.15), (17.38,'fabric',.16,-.10),
    (20.95,'card',.17,.1), (24.18,'card',.20,.03), (24.87,'card',.18,.03), (25.56,'card',.18,.03),
    (27.7,'fabric',.17,.18), (31.36,'card',.17,.18),
    (34.93,'card',.15,-.17), (35.61,'card',.15,.15),
    (37.87,'slide',.18,.05), (39.42,'card',.18,.20),
    (40.02,'card',.16,.06), (42.41,'card',.19,-.20),
    (42.83,'card',.19,.20), (45.4,'slide',.19,-.12),
    (45.57,'card',.17,-.08), (47.88,'page',.20,0),
    (49.29,'slide',.16,.04), (51.44,'fabric',.15,.13),
    (54.56,'slide',.17,-.13), (55.26,'slide',.17,.13), (56.41,'page',.20,0),
    (57.72,'slide',.17,0), (59.76,'card',.16,.12),
    (62.12,'fabric',.15,.10), (64.53,'card',.17,.13),
    (66.82,'slide',.17,.10), (69.99,'card',.18,-.15),
    (70.80,'card',.18,0), (71.58,'card',.17,.15),
    (73.85,'fabric',.17,.10), (74.88,'page',.18,.05), (75.82,'card',.13,.04), (77.09,'slide',.15,0),
    (81.01,'card',.18,0), (83.62,'page',.17,-.08), (85.01,'card',.14,.18),
    (87.36,'card',.16,0), (89.78,'card',.25,0)
]
for cue, kind, gain, pan in cues:
    apply(cue,kind,gain,pan)
envelope = np.sqrt(np.maximum(0,sosfilt(butter(2,7,fs=rate,output='sos'),voice**2)))
fx *= np.clip(.06/(envelope+.028),.42,1)[:,None]
mix = voice[:,None]+fx
peak = maximum_filter1d(np.max(np.abs(mix),axis=1),size=245)
mix *= np.minimum(1,.80/(peak+1e-9))[:,None]
sf.write(out/'mix-v3.wav',mix,rate,subtype='PCM_24')
print('Source kept: 4,419,555 samples. Mixed 93 seconds, no score.')
