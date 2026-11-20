"""Verify actual encoded movie, sample alignment, captions and delivery-size constraints."""
from pathlib import Path
import json,subprocess,hashlib
import numpy as np
import soundfile as sf
from scipy.signal import correlate
P=Path(__file__).resolve().parents[1];root=P.parents[1];O=P/'out';V=root/'video/rahnama-five-whiteboard-v1.mp4'
def run(a):return subprocess.run(a,capture_output=True,text=True,check=True)
p=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(V)]).stdout)
v=next(s for s in p['streams'] if s['codec_type']=='video');a=next(s for s in p['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['avg_frame_rate'],v['codec_name'],v['pix_fmt'],int(v['nb_read_frames']))==(1080,1920,'24/1','h264','yuv420p',1824),v
assert (a['codec_name'],a['sample_rate'],a['channels'])==('aac','48000',2)
assert abs(float(p['format']['duration'])-76)<.01
run(['ffmpeg','-v','error','-i',str(V),'-f','null','-'])
l=run(['ffmpeg','-hide_banner','-nostats','-i',str(V),'-af','loudnorm=I=-14:TP=-1:LRA=7:print_format=json','-f','null','-']).stderr
loud=json.loads(l[l.rfind('{'):l.rfind('}')+1]);assert float(loud['input_tp'])<=-1,loud
assert -15.5<=float(loud['input_i'])<=-12.5,loud
black=run(['ffmpeg','-hide_banner','-nostats','-i',str(V),'-vf','blackdetect=d=0.08:pix_th=0.05','-an','-f','null','-']).stderr
blacklines=[x for x in black.splitlines() if 'black_start:' in x];assert not blacklines,blacklines
run(['ffmpeg','-v','error','-y','-i',str(V),'-vn','-ac','1','-ar','48000','-c:a','pcm_f32le',str(O/'encoded-audio.wav')])
enc,sr=sf.read(O/'encoded-audio.wav',dtype='float32');master,sr=sf.read(O/'mix.wav',dtype='float32');master=master.mean(axis=1)
anchors=[]
for t in [1,14,27,40,53,65,73]:
 i=t*48000;n=48000;pad=512;ref=master[i:i+n].astype(float);q=enc[i-pad:i+n+pad].astype(float);r=correlate(q,ref,mode='valid',method='fft');offset=int(r.argmax())-pad
 seg=enc[i+offset:i+offset+n];corr=float(np.corrcoef(ref,seg)[0,1]);assert abs(offset)<=1 and corr>.97,(t,offset,corr)
 anchors.append({'time':t,'aac_offset_samples':offset,'correlation':corr})
# Compare mastered VO to the original decode, confirming no drift at representative phrase anchors.
source,sr=sf.read(P/'analysis/out/source48.wav',dtype='float32');vo,sr=sf.read(O/'voice.wav',dtype='float32');assert len(source)==len(vo)==3604000
source_align=[]
for t in [1,14,27,40,53,65,73]:
 i=t*48000;n=48000;pad=512;r=correlate(vo[i-pad:i+n+pad],source[i:i+n],mode='valid',method='fft');offset=int(r.argmax())-pad
 assert abs(offset)<=8,(t,offset);source_align.append({'time':t,'master_offset_samples':offset})
pre=json.loads((O/'preflight.json').read_text());assert not pre['invalid_events'] and pre['deterministic_seek'] and pre['no_latin_captions']
caps=json.loads((P/'captions.json').read_text());assert len(caps)==30 and 'برنامه' in caps[-1]['text']
assert V.stat().st_size<100_000_000
with V.open('rb') as f:data=f.read()
assert data.find(b'moov')<data.find(b'mdat'),'faststart missing'
qc={'video':str(V.relative_to(root)),'duration':76,'frames':1824,'resolution':[1080,1920],'fps':24,'codecs':['h264','aac'],'sample_rate':48000,'channels':2,'complete_file_decode':True,'black_intervals':blacklines,'faststart':True,'loudness':loud,'encoded_audio_alignment':anchors,'source_voice_alignment':source_align,'source_voice_samples':len(source),'voice_speed_unchanged':True,'voice_tail_samples':44000,'caption_count':len(caps),'caption_layout_preflight':pre,'visual_stills_reviewed':[0.8,4.9,18.7,30.5,42.6,53.6,66.2,68.8,74.5],'full_speed_watched':False,'perceptual_audio_listening_review':False,'font':'Noto Sans Arabic fallback, not Morabba','music':False,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
(P/'QC.json').write_text(json.dumps(qc,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:qc[k] for k in ['duration','frames','loudness','bytes','sha256']},indent=2))
