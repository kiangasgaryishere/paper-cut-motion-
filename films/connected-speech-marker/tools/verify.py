"""Checks the encoded deliverable; does not claim subjective playback/listening."""
from pathlib import Path
import json,subprocess,hashlib,re
import numpy as np,soundfile as sf
from scipy.signal import correlate,correlation_lags
P=Path(__file__).resolve().parents[1];R=P.parents[1];O=P/'out';V=R/'video/connected-speech-marker-v1.mp4'
def run(args):return subprocess.run(args,capture_output=True,text=True,check=True)
meta=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(V)]).stdout)
v=next(s for s in meta['streams'] if s['codec_type']=='video');a=next(s for s in meta['streams'] if s['codec_type']=='audio')
assert(v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'24/1',1392)
assert a['sample_rate']=='48000' and a['codec_name']=='aac' and v['codec_name']=='h264'
assert abs(float(meta['format']['duration'])-58)<.05
assert abs(float(v['start_time']))<.001 and abs(float(a['start_time']))<.001
full=run(['ffmpeg','-v','error','-i',str(V),'-f','null','-']);assert not full.stderr,full.stderr
l=run(['ffmpeg','-hide_banner','-i',str(V),'-af','loudnorm=I=-14:TP=-1:LRA=7:print_format=json','-f','null','-']).stderr
loud=json.loads(l[l.rfind('{'):l.rfind('}')+1]);assert float(loud['input_tp'])<=-1
black=run(['ffmpeg','-hide_banner','-i',str(V),'-vf','blackdetect=d=0.1:pix_th=0.08','-an','-f','null','-']).stderr
black_intervals=[s for s in black.splitlines() if 'black_start:' in s];assert not black_intervals,black_intervals
run(['ffmpeg','-y','-v','error','-i',str(V),'-vn','-c:a','pcm_f32le',str(O/'decoded-aac.wav')])
x,sr=sf.read(O/'mix.wav');y,sr2=sf.read(O/'decoded-aac.wav');assert sr==sr2==48000
lags=[]
for t in [2.5,10,26.7,38.5,42.7,55.6]:
 i=round(t*sr);A=x[i:i+sr//2].mean(1);B=y[i:i+sr//2].mean(1);c=correlate(B,A,method='fft');lag=int(correlation_lags(len(B),len(A))[np.argmax(c)]);lags.append({'time':t,'lag_samples':lag});assert abs(lag)<=2,(t,lag)
t=json.loads((P/'timeline.json').read_text());assert t['shots'][0]['start_frame']==0 and t['shots'][-1]['end_frame']==1392
for s,u in zip(t['shots'],t['shots'][1:]):assert s['end_frame']==u['start_frame']
for c in t['captions']:
 assert not re.search('[A-Za-z]',c['text'].replace('LISTEN','')),c
 assert not(c['start_frame']<96 and c['end_frame']>51),'Captions reveal first hearing'
assert 'LISTEN' in t['captions'][-1]['text']
m=[e['frame'] for e in t['milestones']];gap=max(b-a for a,b in zip(m,m[1:]))/24;assert gap<=4
for page in range(1,11):
 e=[i for i in t['sound_events'] if i['page']==page and i['type'] in ['line','write']];red=[i for i in e if i['col']=='red'];other=[i for i in e if i['col']!='red'];assert min(i['t'] for i in red)>=max(i['t']+i['d'] for i in other)-.01
browser=json.loads((P/'analysis/production-browser-check.json').read_text());assert browser['deterministic_seek'] and not browser['errors']
report={'file':str(V.relative_to(R)),'sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'bytes':V.stat().st_size,'width':1080,'height':1920,'fps':24,'frame_count':1392,'duration':float(meta['format']['duration']),'audio_sample_rate':48000,'full_decode':'passed','black_intervals':black_intervals,'loudness':loud,'aac_alignment':lags,'caption_policy':'Persian except final LISTEN; first English hearing withheld','max_visual_milestone_gap_seconds':gap,'deterministic_seek':True,'listening_review':'not performed','real_time_full_playback':'not performed'}
(P/'analysis/production-output-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
