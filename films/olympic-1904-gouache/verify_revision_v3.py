"""Check actual delivered pictures, edited narrator samples and audible Foley mix."""
from pathlib import Path
import json,subprocess,hashlib,re,numpy as np,soundfile as sf
from scipy.signal import correlate,correlation_lags
from PIL import Image
p=Path(__file__).resolve().parent;root=p.parents[1];out=root/'video/olympic-1904-final-v3.mp4';duration=3710/30;sr=48000
def probe(file):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(file)]))
pr=probe(out);v=next(s for s in pr['streams'] if s['codec_type']=='video');a=next(s for s in pr['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'30/1',3710)
assert abs(float(pr['format']['duration'])-duration)<.002 and a['sample_rate']=='48000'
assert abs(float(v['start_time']))<1e-5 and abs(float(a['start_time']))<1e-5
subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],capture_output=True,check=True)
b=subprocess.run(['ffmpeg','-hide_banner','-i',str(out),'-vf','blackdetect=d=0.1:pix_th=0.03','-an','-f','null','-'],capture_output=True,text=True,check=True);assert 'black_start:' not in b.stderr
def hashes(file,start,frames):
 data=subprocess.check_output(['ffmpeg','-v','error','-ss',str(start),'-i',str(file),'-map','0:v:0','-frames:v',str(frames),'-f','framemd5','-'],text=True)
 return [line.split(',')[-1].strip() for line in data.splitlines() if line and not line.startswith('#')]
old=root/'video/olympic-1904-final-v2.mp4'
x=hashes(old,0,2100);y=hashes(out,0,2100);assert len(x)==len(y)==2100 and x==y
x=hashes(old,100,780);y=hashes(out,2930/30,780);assert len(x)==len(y)==780 and x==y
master=p/'out/voice-master-v2.wav';expected=json.loads((p/'QC-part01-v2.json').read_text())['canonical_voice_master_sha256'];assert hashlib.sha256(master.read_bytes()).hexdigest()==expected
raw,_=sf.read(master);original_samples=len(raw);full=np.pad(raw,(0,126*sr-len(raw)));expected_voice=np.concatenate([full[:2749*1600],full[2819*1600:]])
voice,fs=sf.read(p/'out/revision-v3-voice.wav');assert fs==sr and np.array_equal(voice,expected_voice)
mix,fs=sf.read(p/'out/revision-v3-mix.wav');fx,_=sf.read(p/'out/revision-v3-sfx.wav');assert fs==sr and len(mix)==3710*1600
assert np.max(abs(mix-(voice[:,None]+fx)))<3e-7
subprocess.run(['ffmpeg','-v','error','-y','-i',str(out),'-vn','-c:a','pcm_f32le',str(p/'out/encoded-revision-v3.wav')],check=True);enc,_=sf.read(p/'out/encoded-revision-v3.wav');lags=[]
for center in [1,3.6,7.3,10,20,30,40,49.93,60,69.6,74.7333333333,81,85.1333333333,90.6,2749/30,2930/30,110,119.5,123]:
 j=round((center-.3)*sr);n=round(.6*sr);x=mix[j:j+n].mean(axis=1);y=enc[j:j+n].mean(axis=1)
 c=correlate(y,x,method='fft');lag=int(correlation_lags(len(y),len(x))[np.argmax(c)]);assert abs(lag)<=2;lags.append(dict(center=center,lag_samples=lag))
ratios=[]
for j in range(0,len(mix)-4800,2400):
 vr=np.sqrt(np.mean(voice[j:j+4800]**2));fr=np.sqrt(np.mean(fx[j:j+4800]**2))
 if vr>.04 and fr>1e-6:ratios.append(float(20*np.log10(vr/fr)))
assert min(ratios)>5.5
r=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(out),'-vn','-af','loudnorm=I=-13:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
loud=json.loads(re.findall(r'\{[^{}]+\}',r.stderr)[-1]);assert float(loud['input_tp'])<=-1
sound=json.loads((p/'sound-design-v3.json').read_text());assert all(c['gain_vs_v2_dB']>6 for c in sound['audibility_comparisons'])
kit=p/'assets/sfx-kit';km=json.loads((kit/'manifest.json').read_text());assert km['license']=='CC0-1.0'
for s in km['sounds']:assert hashlib.sha256((kit/(s['id']+'.wav')).read_bytes()).hexdigest()==s['sha256']
synced=[e for e in sound['events'] if e['origin']=='SFX Kit CC0'];assert all(abs(e['edited_start']+e['sync_at']-e['visual_moment'])<=1/sr for e in synced)
sheet=Image.new('RGB',(1080,960))
for i,t in enumerate([75.4,78.5,81.5,83.5,86.5,90.6,91.8,121.8]):
 dest=p/f'out/v3-encoded-{t}.jpg';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(out),'-frames:v','1',str(dest)],check=True)
 im=Image.open(dest);im.thumbnail((270,480));sheet.paste(im,((i%4)*270,(i//4)*480))
sheet.save(p/'preview-hicks-v3.jpg',quality=92)
review=probe(root/'video/olympic-1904-hicks-v3.mp4');rv=next(s for s in review['streams'] if s['codec_type']=='video');assert int(rv['nb_frames'])==567 and abs(float(review['format']['duration'])-18.9)<.002
q=dict(duration=duration,width=1080,height=1920,fps=30,frames=3710,full_decode='passed',black_intervals='none',video_start_time=float(v['start_time']),audio_start_time=float(a['start_time']),
 unchanged_prefix_seconds=70,unchanged_prefix_decoded_frames=2100,unchanged_tail_source_start=100,unchanged_tail_output_start=2930/30,unchanged_tail_decoded_frames=780,
 canonical_master_unchanged=True,retained_narrator_samples_unchanged=True,narration_speed_changed=False,removed_sentence='و بالاخره قهرمان شد! (second occurrence after They kept him going)',removed_source_interval=[2749/30,2819/30],removed_samples=112000,removed_frames=70,
 edited_narration_duration=(original_samples-112000)/sr,final_silent_padding_seconds=(126*sr-original_samples)/sr,
 encoded_mix_lag_checks=lags,speech_over_effects_min_dB=round(min(ratios),2),speech_over_effects_median_dB=round(float(np.median(ratios)),2),encoded_LUFS=float(loud['input_i']),encoded_true_peak_dBTP=float(loud['input_tp']),
 sfx_kit_license=km['license'],sfx_kit_asset_hashes_verified=len(km['sounds']),sfx_kit_sync_points_checked=len(synced),transition_whooshes=sum('whoosh' in e['id'] for e in synced),audibility_comparisons=sound['audibility_comparisons'],music='none',audio_encoded_once=True,independent_listening_review='not performed',review_duration=18.9,review_frames=567,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),bytes=out.stat().st_size)
(p/'QC-revision-v3.json').write_text(json.dumps(q,indent=2));print(json.dumps(q,indent=2))
manifest=json.loads((p/'revision-v3.json').read_text());manifest.update(status='verified',sha256=q['sha256']);(p/'revision-v3.json').write_text(json.dumps(manifest,indent=2))
