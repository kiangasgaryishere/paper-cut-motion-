from pathlib import Path
import json,subprocess,hashlib,re,numpy as np,soundfile as sf
from scipy.signal import correlate,correlation_lags
p=Path(__file__).resolve().parent;root=p.parents[1];meta=json.loads((p/'segments.json').read_text());out=root/meta['assembly_output'];duration=meta['assembly_duration']
prior=[x for x in meta.get('assemblies',[]) if x['end']<duration and x.get('status')=='verified']
prefix=max(prior,key=lambda x:x['end']) if prior else dict(output=meta['parts'][0]['output'],end=meta['parts'][0]['end'])
prefix_seconds=prefix['end'];prefix_frames=round(prefix_seconds*30);prefix_samples=round(prefix_seconds*48000)
def probe(file):
 r=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(file)]));v=next(x for x in r['streams'] if x['codec_type']=='video');a=next(x for x in r['streams'] if x['codec_type']=='audio');return r,v,a
for part in meta['parts']:
 r,v,a=probe(root/part['output']);assert int(v['nb_frames'])==round((part['end']-part['start'])*30);assert abs(float(r['format']['duration'])-(part['end']-part['start']))<.01
r,v,a=probe(out);assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'30/1',round(duration*30));assert abs(float(r['format']['duration'])-duration)<.01;assert a['sample_rate']=='48000';assert abs(float(v['start_time']))<1e-5 and abs(float(a['start_time']))<1e-5
subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],capture_output=True,check=True)
b=subprocess.run(['ffmpeg','-hide_banner','-i',str(out),'-vf','blackdetect=d=0.1:pix_th=0.03','-an','-f','null','-'],capture_output=True,text=True,check=True);assert 'black_start:' not in b.stderr
# Every decoded picture frame in the approved first part must stay identical.
def first_frames_md5(file):
 text=subprocess.check_output(['ffmpeg','-v','error','-i',str(file),'-map','0:v:0','-frames:v',str(prefix_frames),'-f','framemd5','-'],text=True);return [x for x in text.splitlines() if x and not x.startswith('#')]
prefix_equal=first_frames_md5(root/prefix['output'])==first_frames_md5(out);assert prefix_equal
voice,sr=sf.read(p/'out/voice-master-v2.wav');expected=json.loads((p/'QC-part01-v2.json').read_text())['canonical_voice_master_sha256'];assert hashlib.sha256((p/'out/voice-master-v2.wav').read_bytes()).hexdigest()==expected
mix,_=sf.read(p/'out/assembled-mix.wav');assert len(mix)==round(duration*48000)
source_decoded_samples=len(voice);voice=np.pad(voice,(0,max(0,len(mix)-len(voice))))
fxparts=[]
for part in meta['parts']:
 fx,fs=sf.read(p/part['effects_wav']);assert fs==sr==48000;fxparts.append(fx)
fx=np.concatenate(fxparts);assert np.max(abs(mix-(voice[:len(mix),None]+fx)))<3e-7
old=np.concatenate([sf.read(p/part['mix_wav'])[0] for part in meta['parts'] if part['end']<=prefix_seconds]);assert np.array_equal(mix[:prefix_samples],old)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(out),'-vn','-c:a','pcm_f32le',str(p/'out/encoded-assembly.wav')],check=True);enc,_=sf.read(p/'out/encoded-assembly.wav');lags=[]
windows=[(1,2)]+[(x['start']-.6,1.2) for x in meta['parts'][1:]]+[(meta['parts'][-1]['start']+1,2),(meta['parts'][-1]['start']+4,2),(duration-2.5,2)]
for start,seconds in windows:
 j=round(start*sr);n=round(seconds*sr);x=mix[j:j+n].mean(axis=1);y=enc[j:j+n].mean(axis=1);c=correlate(y,x,method='fft');lag=int(correlation_lags(len(y),len(x))[np.argmax(c)]);assert abs(lag)<=2;lags.append(dict(start=start,duration=seconds,lag_samples=lag))
ratios=[]
for j in range(prefix_samples,len(mix)-4800,2400):
 vr=np.sqrt(np.mean(voice[j:j+4800]**2));fr=np.sqrt(np.mean(fx[j:j+4800]**2))
 if vr>.04 and fr>1e-6:ratios.append(float(20*np.log10(vr/fr)))
assert min(ratios)>15
m=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(out),'-vn','-af','loudnorm=I=-13:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);m=json.loads(re.findall(r'\{[^{}]+\}',m.stderr)[-1]);assert float(m['input_tp'])<=-1
from PIL import Image
last=meta['parts'][-1]['start'];times=([1,39,46.5,54,57.5,62.5,70.5,83,88,100.7,112,124.5] if duration>=126 else [1,prefix_seconds-1.5,last+2,last+4.8,min(last+7,duration-.4),duration-.3]);columns=4 if duration>=126 else len(times);rows=(len(times)+columns-1)//columns;board=Image.new('RGB',(columns*270,rows*480))
for i,t in enumerate(times):
 path=p/'out'/f'assembly-{t}.jpg';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(out),'-frames:v','1',str(path)],check=True);im=Image.open(path);im.thumbnail((270,480));board.paste(im,((i%columns)*270,(i//columns)*480))
board.save(p/f'preview-through-{duration:g}s.jpg',quality=92)
q=dict(duration=duration,fps=30,frames=round(duration*30),width=1080,height=1920,video=v['codec_name'],audio=a['codec_name'],audio_sample_rate=48000,video_start_time=float(v['start_time']),audio_start_time=float(a['start_time']),full_decode='passed',black_frames='none',approved_prefix_seconds=prefix_seconds,approved_prefix_frames=prefix_frames,approved_prefix_decoded_frames_identical=prefix_equal,approved_prefix_mix_samples_identical=True,canonical_voice_master_unchanged=True,audio_encoded_once=True,seams_at_seconds=[x['start'] for x in meta['parts'][1:]],seam_extra_audio_samples=0,encoded_mix_lag_checks=lags,narration_retimed=False,narration_boundary_fade=False,new_material_speech_over_effects_min_dB=round(min(ratios),2),new_material_speech_over_effects_median_dB=round(float(np.median(ratios)),2),encoded_LUFS=float(m['input_i']),encoded_true_peak_dBTP=float(m['input_tp']),source_decoded_duration=source_decoded_samples/sr,final_silent_padding_seconds=max(0,(len(mix)-source_decoded_samples)/sr),music='none',independent_listening_review='not performed',sha256=hashlib.sha256(out.read_bytes()).hexdigest(),bytes=out.stat().st_size)
(p/f'QC-through-{duration:g}s.json').write_text(json.dumps(q,indent=2));print(json.dumps(q,indent=2))
