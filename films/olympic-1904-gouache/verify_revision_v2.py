"""Validate delivered v2 picture preservation, timing, narration and encoded levels."""
from pathlib import Path
import json,subprocess,hashlib,re,numpy as np,soundfile as sf
from scipy.signal import correlate,correlation_lags
from PIL import Image
p=Path(__file__).resolve().parent;root=p.parents[1];out=root/'video/olympic-1904-final-v2.mp4'
def probe(file):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(file)]))
pr=probe(out);v=next(s for s in pr['streams'] if s['codec_type']=='video');a=next(s for s in pr['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'30/1',3780)
assert abs(float(pr['format']['duration'])-126)<.001 and a['sample_rate']=='48000'
assert abs(float(v['start_time']))<1e-5 and abs(float(a['start_time']))<1e-5
subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],capture_output=True,check=True)
b=subprocess.run(['ffmpeg','-hide_banner','-i',str(out),'-vf','blackdetect=d=0.1:pix_th=0.03','-an','-f','null','-'],capture_output=True,text=True,check=True);assert 'black_start:' not in b.stderr
def hashes(file):
 data=subprocess.check_output(['ffmpeg','-v','error','-ss','20','-i',str(file),'-map','0:v:0','-f','framemd5','-'],text=True)
 return [line.split(',')[-1].strip() for line in data.splitlines() if line and not line.startswith('#')]
old=hashes(root/'video/olympic-1904-final-v1.mp4');new=hashes(out);assert len(old)==len(new)==3180 and old==new
voice,sr=sf.read(p/'out/voice-master-v2.wav');source_samples=len(voice);expected=json.loads((p/'QC-part01-v2.json').read_text())['canonical_voice_master_sha256']
assert hashlib.sha256((p/'out/voice-master-v2.wav').read_bytes()).hexdigest()==expected
voice=np.pad(voice,(0,126*sr-len(voice)));mix,fs=sf.read(p/'out/revision-v2-mix.wav');fx,_=sf.read(p/'out/revision-v2-sfx.wav')
assert fs==sr==48000 and len(mix)==126*sr and max(abs(mix-(voice[:,None]+fx)).ravel())<3e-7
subprocess.run(['ffmpeg','-v','error','-y','-i',str(out),'-vn','-c:a','pcm_f32le',str(p/'out/encoded-revision-v2.wav')],check=True)
enc,_=sf.read(p/'out/encoded-revision-v2.wav');lags=[]
for center in [1,3.6,7.3,10,20,30,40,49.93,50.733333333,60,69.6,80,90,93.9666666667,100,110,120,124.5]:
 j=round((center-.4)*sr);n=round(.8*sr);x=mix[j:j+n].mean(axis=1);y=enc[j:j+n].mean(axis=1)
 c=correlate(y,x,method='fft');lag=int(correlation_lags(len(y),len(x))[np.argmax(c)]);assert abs(lag)<=2;lags.append(dict(center=center,lag_samples=lag))
ratios=[]
for j in range(0,len(mix)-4800,2400):
 vr=np.sqrt(np.mean(voice[j:j+4800]**2));fr=np.sqrt(np.mean(fx[j:j+4800]**2))
 if vr>.04 and fr>1e-6:ratios.append(float(20*np.log10(vr/fr)))
assert min(ratios)>16
r=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(out),'-vn','-af','loudnorm=I=-13:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
loud=json.loads(re.findall(r'\{[^{}]+\}',r.stderr)[-1]);assert float(loud['input_tp'])<=-1
sheet=Image.new('RGB',(1080,960))
for i,t in enumerate([1,4.4,6.4,8.6,10.2,50,69.8,94.2]):
 dest=p/f'out/v2-encoded-{t}.jpg';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(out),'-frames:v','1',str(dest)],check=True)
 im=Image.open(dest);im.thumbnail((270,480));sheet.paste(im,((i%4)*270,(i//4)*480))
sheet.save(p/'preview-revision-v2.jpg',quality=92)
preview=probe(root/'video/olympic-1904-opening-v2.mp4');pv=next(s for s in preview['streams'] if s['codec_type']=='video')
assert abs(float(preview['format']['duration'])-10)<.001 and int(pv['nb_frames'])==300
q=dict(duration=126,width=1080,height=1920,fps=30,frames=3780,full_decode='passed',black_intervals='none',
 video_start_time=float(v['start_time']),audio_start_time=float(a['start_time']),
 original_decoded_picture_identical_from=20,original_identical_frames=3180,canonical_narration_unchanged=True,
 narration_retimed=False,source_decoded_duration=source_samples/sr,final_silent_padding_seconds=126-source_samples/sr,
 encoded_mix_lag_checks=lags,speech_over_effects_min_dB=round(min(ratios),2),speech_over_effects_median_dB=round(float(np.median(ratios)),2),
 encoded_LUFS=float(loud['input_i']),encoded_true_peak_dBTP=float(loud['input_tp']),
 opening_visual_cuts=[3.6,7.3,10.4],music='none',audio_encoded_once=True,
 independent_listening_review='not performed',opening_preview_duration=10,opening_preview_frames=300,
 sha256=hashlib.sha256(out.read_bytes()).hexdigest(),bytes=out.stat().st_size)
(p/'QC-revision-v2.json').write_text(json.dumps(q,indent=2));print(json.dumps(q,indent=2))
manifest=json.loads((p/'revision-v2.json').read_text());manifest.update(status='verified',sha256=q['sha256']);(p/'revision-v2.json').write_text(json.dumps(manifest,indent=2))
