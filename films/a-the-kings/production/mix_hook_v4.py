from pathlib import Path
import sys,numpy as np,soundfile as sf
sys.path.insert(0,'core/audio');import sfx
p=Path('films/a-the-kings/production');v,sr=sf.read(p/'voice.wav');v=v[:8*sr];v*=.78/max(.01,np.abs(v).max());b=np.repeat(v[:,None],2,axis=1)
for at,x,gain in [(2.062,sfx.click(1.0),.045),(3.4,sfx.click(.85),.045),(4.91725,sfx.whoosh(.28),.035)]:sfx.add(b,x,at,gain=gain)
assert np.isfinite(b).all();sf.write(p/'hook-v4-mix.wav',b,sr,subtype='PCM_24')
