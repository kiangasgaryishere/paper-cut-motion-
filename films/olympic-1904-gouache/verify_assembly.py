from pathlib import Path
import json,subprocess,hashlib,re,numpy as np,soundfile as sf
from scipy.signal import correlate,correlation_lags
p=Path(__file__).resolve().parent;root=p.parents[1];meta=json.loads((p/'segments.json').read_text());out=root/meta['assembly_output'];duration=meta['assembly_duration']
def probe(file):
 r=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(file)]));v=next(x for x in r['streams'] if x['codec_type']=='video');a=next(x for x in r['streams'] if x['codec_type']=='audio');return r,v,a
for part in meta['parts']:
 r,v,a=probe(root/part['output']);assert int(v['nb_frames'])==round((part['end']-part['start'])*30);assert abs(float(r['format']['duration'])-(part['end']-part['start']))<.01
r,v,a=probe(out);assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'30/1',600);assert abs(float(r['format']['duration'])-20)<.01;assert a['sample_rate']=='48000';assert abs(float(v['start_time']))<1e-5 and abs(float(a['start_time']))<1e-5
subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],capture_output=True,check=True)
b=subprocess.run(['ffmpeg','-hide_banner','-i',str(out),'-vf','blackdetect=d=0.1:pix_th=0.03','-an','-f','null','-'],capture_output=True,text=True,check=True);assert 'black_start:' not in b.stderr
# Every decoded picture frame in the approved first part must stay identical.
def first_frames_md5(file):
 text=subprocess.check_output(['ffmpeg','-v','error','-i',str(file),'-map','0:v:0','-frames:v','300','-f','framemd5','-'],text=True);return [x for x in text.splitlines() if x and not x.startswith('#')]
prefix_equal=first_frames_md5(root/meta['parts'][0]['output'])==first_frames_md5(out);assert prefix_equal
voice,sr=sf.read(p/'out/voice-master-v2.wav');expected=json.loads((p/'QC-part01-v2.json').read_text())['canonical_voice_master_sha256'];assert hashlib.sha256((p/'out/voice-master-v2.wav').read_bytes()).hexdigest()==expected
mix,_=sf.read(p/'out/assembled-mix.wav');assert len(mix)==960000
fxparts=[]
for part in meta['parts']:
 fx,fs=sf.read(p/part['effects_wav']);assert fs==sr==48000;fxparts.append(fx)
fx=np.concatenate(fxparts);assert np.max(abs(mix-(voice[:len(mix),None]+fx)))<3e-7
old,_=sf.read(p/'out/part01-mix-v2.wav');assert np.array_equal(mix[:480000],old)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(out),'-vn','-c:a','pcm_f32le',str(p/'out/encoded-assembly.wav')],check=True);enc,_=sf.read(p/'out/encoded-assembly.wav');lags=[]
for start,seconds in [(1,2),(8,2),(9.4,1.2),(11,2),(14,2),(17.5,2)]:
 j=round(start*sr);n=round(seconds*sr);x=mix[j:j+n].mean(axis=1);y=enc[j:j+n].mean(axis=1);c=correlate(y,x,method='fft');lag=int(correlation_lags(len(y),len(x))[np.argmax(c)]);assert abs(lag)<=2;lags.append(dict(start=start,duration=seconds,lag_samples=lag))
ratios=[]
for j in range(480000,len(mix)-4800,2400):
 vr=np.sqrt(np.mean(voice[j:j+4800]**2));fr=np.sqrt(np.mean(fx[j:j+4800]**2))
 if vr>.04 and fr>1e-6:ratios.append(float(20*np.log10(vr/fr)))
assert min(ratios)>15
m=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(out),'-vn','-af','loudnorm=I=-13:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);m=json.loads(re.findall(r'\{[^{}]+\}',m.stderr)[-1]);assert float(m['input_tp'])<=-1
from PIL import Image
board=Image.new('RGB',(1350,480));times=[1,8.5,11.8,14.8,19.1]
for i,t in enumerate(times):
 path=p/'out'/f'assembly-{t}.jpg';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(out),'-frames:v','1',str(path)],check=True);im=Image.open(path);im.thumbnail((270,480));board.paste(im,(i*270,0))
board.save(p/'preview-through-20s.jpg',quality=92)
q=dict(duration=20,fps=30,frames=600,width=1080,height=1920,video=v['codec_name'],audio=a['codec_name'],audio_sample_rate=48000,video_start_time=float(v['start_time']),audio_start_time=float(a['start_time']),full_decode='passed',black_frames='none',approved_first_300_decoded_frames_identical=prefix_equal,first_480000_mix_samples_identical=True,canonical_voice_master_unchanged=True,audio_encoded_once=True,seam_at_seconds=10,seam_extra_audio_samples=0,encoded_mix_lag_checks=lags,narration_retimed=False,narration_boundary_fade=False,part02_speech_over_effects_min_dB=round(min(ratios),2),part02_speech_over_effects_median_dB=round(float(np.median(ratios)),2),encoded_LUFS=float(m['input_i']),encoded_true_peak_dBTP=float(m['input_tp']),music='none',independent_listening_review='not performed',sha256=hashlib.sha256(out.read_bytes()).hexdigest(),bytes=out.stat().st_size)
(p/'QC-through-20s.json').write_text(json.dumps(q,indent=2));print(json.dumps(q,indent=2))
