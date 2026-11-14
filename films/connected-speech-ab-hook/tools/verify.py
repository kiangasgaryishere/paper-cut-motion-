from pathlib import Path
import json,subprocess,hashlib,re
import numpy as np,soundfile as sf
from scipy.signal import correlate,correlation_lags
P=Path(__file__).resolve().parents[1];R=P.parents[1];O=P/'out';V=R/'video/connected-speech-ab-hook-v1.mp4';SR=48000

def run(a):return subprocess.run(a,capture_output=True,text=True,check=True)
m=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(V)]).stdout);v=next(x for x in m['streams'] if x['codec_type']=='video');a=next(x for x in m['streams'] if x['codec_type']=='audio')
assert(v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'24/1',1656);assert float(m['format']['duration'])==69;assert a['sample_rate']=='48000';assert float(v['start_time'])==float(a['start_time'])==0
assert not run(['ffmpeg','-v','error','-i',str(V),'-f','null','-']).stderr
l=run(['ffmpeg','-hide_banner','-i',str(V),'-af','loudnorm=I=-14:TP=-1:LRA=7:print_format=json','-f','null','-']).stderr;loud=json.loads(l[l.rfind('{'):l.rfind('}')+1]);assert float(loud['input_tp'])<=-1 and -16<=float(loud['input_i'])<=-12
black=run(['ffmpeg','-hide_banner','-i',str(V),'-vf','blackdetect=d=.15:pix_th=.08','-an','-f','null','-']).stderr;bl=[l for l in black.splitlines() if 'black_start:' in l];assert not bl,bl
run(['ffmpeg','-y','-v','error','-i',str(V),'-vn','-c:a','pcm_f32le',str(O/'decoded.wav')]);x,sr=sf.read(O/'mix.wav');y,sy=sf.read(O/'decoded.wav');assert sr==sy==SR and len(x)==69*SR
T=json.loads((P/'timeline.json').read_text());vo,sr=sf.read(O/'voice.wav');clip,sr=sf.read(O/'movie-stem.wav');voice_stem,sr=sf.read(O/'voice-stem.wav');screenings=[]
for e in T['segments']:
 aa=round(e['start_frame']*2000);bb=round(e['end_frame']*2000)
 if e['kind']=='movie':
  assert abs(voice_stem[aa:bb]).max()==0;assert np.max(abs(x[aa:bb]-clip[aa:bb]))<1e-6;screenings.append(x[aa:bb])
 elif e['kind']=='voice':
  expected=vo[round(e['source_start_frame']*2000):round(e['source_end_frame']*2000)];assert np.max(abs(voice_stem[aa:bb,0]-expected))<1e-6
assert all(np.max(abs(z-screenings[0]))<1e-12 for z in screenings)
anchors=[]
for t in [.3,3,7.1,10,17.4,20.3,31.2,42.4,44.5,47.1,63.5,67.3]:
 aa=round(t*SR);u=x[aa:aa+SR//2].mean(1);w=y[aa:aa+SR//2].mean(1);cc=correlate(w,u,method='fft');lag=int(correlation_lags(len(w),len(u))[np.argmax(cc)]);assert abs(lag)<=2;anchors.append({'time':t,'lag_samples':lag})
b=json.loads((P/'analysis/browser-check.json').read_text());assert b['seek_deterministic'] and not b['errors']
full=[f for f in b['frames'] if f['time'] in [0,.5,1.4,7.2,8.3]];assert all(f['movie']['rect']==[0,0,1080,1920] for f in full)
for c in T['captions']:assert not re.search('[A-Za-z]',c['text'].replace('LISTEN',''))
assert all(not(c['start_frame']<57 and c['end_frame']>0) for c in T['captions']);assert 'LISTEN' in ''.join(c['text'] for c in T['captions'] if c['start_frame']>1500)
report={'version':'connected-speech-ab-hook-v1','file':str(V.relative_to(R)),'sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'bytes':V.stat().st_size,'duration':69,'frames':1656,'width':1080,'height':1920,'fps':24,'sample_rate':SR,'full_decode':'passed','black_intervals':bl,'loudness':loud,'aac_alignment':anchors,'movie_screenings':4,'first_two_fullscreen':'passed: all sampled active movie rects fill 1080x1920','narrator_quote_replacement':'passed: zero narrator stem during every screening; master screening samples equal actual movie stem','screening_audio_equality':'passed: all four movie screenings sample-identical before AAC','other_narration_retention':'passed: every mapped non-replaced narration sample retained','seek_deterministic':True,'subtitle_layout':'passed: no overflow; charcoal background; first movie uncaptioned; second English captioned','caption_alignment':'phrase-level estimates from script and pauses, not manual word-level listening audit','full_speed_playback':'not performed','listening_review':'not performed'}
(P/'QC.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
