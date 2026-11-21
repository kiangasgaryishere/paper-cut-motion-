from pathlib import Path
import subprocess,json,hashlib
import numpy as np,soundfile as sf
from scipy.signal import correlate,butter,sosfilt
P=Path(__file__).resolve().parents[1];R=P.parents[1];O=P/'out';V=R/'video/gta6-family-album-v1.mp4'
def run(a):return subprocess.run(a,capture_output=True,text=True,check=True)
p=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(V)]).stdout);v=next(x for x in p['streams'] if x['codec_type']=='video');a=next(x for x in p['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'],v['avg_frame_rate'],v['codec_name'],v['pix_fmt'],int(v['nb_read_frames']))==(1080,1920,'24/1','h264','yuv420p',1704)
assert (v['color_range'],v['color_space'],v['color_transfer'],v['color_primaries'])==('tv','bt709','bt709','bt709')
assert (a['codec_name'],a['sample_rate'],a['channels'])==('aac','48000',2)
assert abs(float(p['format']['duration'])-71)<.01
run(['ffmpeg','-v','error','-i',str(V),'-f','null','-'])
x=run(['ffmpeg','-hide_banner','-nostats','-i',str(V),'-af','loudnorm=I=-14:TP=-1:LRA=7:print_format=json','-f','null','-']).stderr;loud=json.loads(x[x.rfind('{'):x.rfind('}')+1]);assert -15.5<=float(loud['input_i'])<=-12.5 and float(loud['input_tp'])<=-1,loud
black=run(['ffmpeg','-hide_banner','-nostats','-i',str(V),'-vf','blackdetect=d=0.08:pix_th=0.05','-an','-f','null','-']).stderr;blacklines=[x for x in black.splitlines() if 'black_start:' in x];assert not blacklines,blacklines
run(['ffmpeg','-v','error','-y','-i',str(V),'-vn','-ac','1','-ar','48000','-c:a','pcm_f32le',str(O/'encoded-audio.wav')])
enc,sr=sf.read(O/'encoded-audio.wav',dtype='float32');master,sr=sf.read(O/'mix.wav',dtype='float32');master=master.mean(axis=1)
anchors=[]
for t in [1,14,22,29,37,46,54,60,65,68]:
 i=t*48000;n=round(.7*48000);pad=512;ref=master[i:i+n].astype(float);r=correlate(enc[i-pad:i+n+pad].astype(float),ref,mode='valid',method='fft');offset=int(r.argmax())-pad;corr=float(np.corrcoef(ref,enc[i+offset:i+offset+n])[0,1]);assert abs(offset)<=1 and corr>.97,(t,offset,corr);anchors.append({'time':t,'encoded_offset_samples':offset,'correlation':corr})
source,sr=sf.read(P/'analysis/out/source48.wav',dtype='float32');vo,sr=sf.read(O/'voice.wav',dtype='float32');assert len(source)==len(vo)==3350361
# Compare timing after matching the known 70Hz mastering high-pass. Raw correlation
# otherwise confuses the EQ phase response with an editorial shift (up to19samples here).
raw_source=source.copy();source=sosfilt(butter(2,70,fs=48000,btype='highpass',output='sos'),source)
source_align=[]
for t in [1,14,22,29,37,46,54,60,65,68]:
 i=t*48000;n=round(.7*48000);pad=512;r=correlate(vo[i-pad:i+n+pad],source[i:i+n],mode='valid',method='fft');offset=int(r.argmax())-pad;corr=float(np.corrcoef(vo[i+offset:i+offset+n],source[i:i+n])[0,1]);assert abs(offset)<=2 and corr>.94,(t,offset,corr);raw_r=correlate(vo[i-pad:i+n+pad],raw_source[i:i+n],mode='valid',method='fft');raw_offset=int(raw_r.argmax())-pad;source_align.append({'time':t,'master_offset_samples_after_matching_highpass':offset,'correlation':corr,'raw_phase_comparison_offset_samples':raw_offset})
pre=json.loads((O/'preflight.json').read_text());assert pre['deterministic_seek'] and pre['no_caption_overlap'] and pre['no_latin_captions'] and pre['max_meaningful_event_gap']<=4
# Exact uploaded source bytes remain intact; safe to reproduce and audit without rewriting.
for f in json.loads((P/'assets/input-manifest.json').read_text()):assert hashlib.sha256((P/f['path']).read_bytes()).hexdigest()==f['sha256']
data=V.read_bytes();assert len(data)<100_000_000 and data.find(b'moov')<data.find(b'mdat')
qc={'video':str(V.relative_to(R)),'duration':71,'frames':1704,'resolution':[1080,1920],'fps':24,'pixel_format':'yuv420p','color_range':'tv','color_space':'bt709','primaries':'bt709','transfer':'bt709','codecs':['h264','aac'],'sample_rate':48000,'channels':2,'complete_file_decode':True,'faststart':True,'black_intervals':blacklines,'loudness':loud,'source_voice_samples':3350361,'source_retained_complete':True,'retiming':False,'tail_samples':57639,'source_voice_alignment':source_align,'source_alignment_method':'Compare after matching known mastering high-pass; unfiltered EQ-phase offsets recorded separately.','encoded_audio_alignment':anchors,'preflight':pre,'music':False,'supplied_source_hashes_match':True,'artwork':'original generated illustrative snapshots, not gameplay/news photos','publication_condition':'after actual confirmed release, as user expressly requested; not independent current-release verification','style_frames_inspected':[.7,6.4,12,15.7,22.8,31.4,40.3,43.3,48.2,56.6,60.8,65.9,69.4],'full_speed_watched':False,'perceptual_listening_review':False,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
(P/'QC.json').write_text(json.dumps(qc,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:qc[k] for k in ['duration','frames','bytes','sha256','loudness']},indent=2))
