from pathlib import Path
import json,subprocess,hashlib,re,numpy as np,soundfile as sf
from scipy.signal import correlate,correlation_lags
p=Path(__file__).resolve().parent;f=p.parents[1]/'video/olympic-1904-part01-v2.mp4'
r=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]));v=next(x for x in r['streams'] if x['codec_type']=='video');a=next(x for x in r['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'30/1',300);assert abs(float(r['format']['duration'])-10)<.01;assert a['sample_rate']=='48000'
subprocess.run(['ffmpeg','-v','error','-i',str(f),'-f','null','-'],capture_output=True,check=True)
b=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-vf','blackdetect=d=0.1:pix_th=0.03','-an','-f','null','-'],capture_output=True,text=True,check=True);assert 'black_start:' not in b.stderr
subprocess.run(['ffmpeg','-v','error','-y','-i',str(f),'-vn','-c:a','pcm_f32le',str(p/'out/encoded-part01.wav')],check=True)
encoded,sr=sf.read(p/'out/encoded-part01.wav');mix,fs=sf.read(p/'out/part01-mix-v2.wav');voice,vs=sf.read(p/'out/voice-master-v2.wav');fx,_=sf.read(p/'out/part01-sfx-v2.wav');assert sr==fs==vs==48000 and len(mix)==480000
voice=voice[:len(mix)];assert np.max(np.abs(mix-(voice[:,None]+fx)))<3e-7
# Cross-correlate the encoded output with its exact master timeline in three windows.
lags=[]
for start in [1,4,7]:
 j=start*sr;x=mix[j:j+2*sr].mean(axis=1);y=encoded[j:j+2*sr].mean(axis=1);c=correlate(y,x,method='fft');lag=int(correlation_lags(len(y),len(x))[np.argmax(c)]);assert abs(lag)<=2;lags.append(dict(start=start,lag_samples=lag))
# The canonical voice master must also retain the source's original time origin.
processed,_=sf.read(p/'out/voice-presence.wav');source_lags=[]
for start in [1,4,7]:
 j=start*sr;x=processed[j:j+2*sr];y=voice[j:j+2*sr];c=correlate(y,x,method='fft');lag=int(correlation_lags(len(y),len(x))[np.argmax(c)]);assert abs(lag)<=2;source_lags.append(dict(start=start,lag_samples=lag))
ratios=[]
for j in range(0,len(voice)-4800,2400):
 vr=np.sqrt(np.mean(voice[j:j+4800]**2));fr=np.sqrt(np.mean(fx[j:j+4800]**2))
 if vr>.04 and fr>1e-6:ratios.append(float(20*np.log10(vr/fr)))
assert min(ratios)>15
m=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(f),'-vn','-af','loudnorm=I=-13:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);m=json.loads(re.findall(r'\{[^{}]+\}',m.stderr)[-1]);assert float(m['input_tp'])<=-1
for t in [1,4.5,8.5]:subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(f),'-frames:v','1',str(p/'out'/f'encoded-v2-{t}.jpg')],check=True)
from PIL import Image
board=Image.new('RGB',(810,480))
for i,t in enumerate([1,4.5,8.5]):
 im=Image.open(p/'out'/f'encoded-v2-{t}.jpg');im.thumbnail((270,480));board.paste(im,(i*270,0))
board.save(p/'preview-part01-v2.jpg',quality=92)
q=dict(duration=10,fps=30,frames=300,width=1080,height=1920,video=v['codec_name'],audio=a['codec_name'],sample_rate=48000,full_decode='passed',black_frames='none',narration='uploaded running.mp3, original absolute interval [0,10)',narration_retimed=False,narration_boundary_fade=False,encoded_mix_lag_checks=lags,master_source_lag_checks=source_lags,speech_over_effects_min_dB=round(min(ratios),2),speech_over_effects_median_dB=round(float(np.median(ratios)),2),encoded_LUFS=float(m['input_i']),encoded_true_peak_dBTP=float(m['input_tp']),music='none',independent_listening_review='not performed',motion_check='motion-layout-QC-v2.json',source_mp3_sha256=hashlib.sha256((p/'assets/narration.mp3').read_bytes()).hexdigest(),canonical_voice_master_sha256=hashlib.sha256((p/'out/voice-master-v2.wav').read_bytes()).hexdigest(),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size)
(p/'QC-part01-v2.json').write_text(json.dumps(q,indent=2));print(json.dumps(q,indent=2))
