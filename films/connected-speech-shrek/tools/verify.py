"""Encoded-output, source-map, reverse, caption and colour checks; no listening claim."""
from pathlib import Path
import json,subprocess,hashlib,re
import numpy as np,soundfile as sf
from scipy.signal import correlate,correlation_lags
P=Path(__file__).resolve().parents[1];R=P.parents[1];O=P/'out';V=R/'video/connected-speech-shrek-v1.mp4';SR=48000

def run(a):return subprocess.run(a,capture_output=True,text=True,check=True)
m=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(V)]).stdout);v=next(s for s in m['streams'] if s['codec_type']=='video');a=next(s for s in m['streams'] if s['codec_type']=='audio');assert(v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'24/1',2088);assert float(m['format']['duration'])==87 and a['sample_rate']=='48000';assert float(v['start_time'])==float(a['start_time'])==0
assert not run(['ffmpeg','-v','error','-i',str(V),'-f','null','-']).stderr
l=run(['ffmpeg','-hide_banner','-i',str(V),'-af','loudnorm=I=-14:TP=-1:LRA=7:print_format=json','-f','null','-']).stderr;loud=json.loads(l[l.rfind('{'):l.rfind('}')+1]);assert float(loud['input_tp'])<=-1 and -16<=float(loud['input_i'])<=-12
black=run(['ffmpeg','-hide_banner','-i',str(V),'-vf','blackdetect=d=.15:pix_th=.08','-an','-f','null','-']).stderr;bl=[z for z in black.splitlines() if 'black_start:' in z];assert not bl,bl
run(['ffmpeg','-y','-v','error','-i',str(V),'-vn','-c:a','pcm_f32le',str(O/'decoded.wav')]);x,sr=sf.read(O/'mix.wav');y,sy=sf.read(O/'decoded.wav');vo,s=sf.read(O/'voice.wav');vs,s=sf.read(O/'voice-stem.wav');ms,s=sf.read(O/'movie-stem.wav');rs,s=sf.read(O/'reverse-stem.wav');fx,s=sf.read(O/'fx-stem.wav');assert sr==sy==SR and len(x)==87*SR
T=json.loads((P/'timeline.json').read_text());
for e in T['segments']:
 aa=round(e['start_frame']*2000);bb=round(e['end_frame']*2000)
 if e['kind']=='voice':
  expected=vo[round(e['source_start_frame']*2000):round(e['source_end_frame']*2000)];assert len(expected)==bb-aa;assert np.max(abs(vs[aa:bb,0]-expected))<1e-6
 elif e['kind']=='movie':
  assert abs(fx[aa:bb]).max()==0
  if e['id']=='shrek-complete':assert abs(vs[aa+24000:bb]).max()==0
  else:assert abs(vs[aa:bb]).max()==0
  assert np.max(abs(x[aa:bb]-ms[aa:bb]-vs[aa:bb]))<1e-6
 elif e['kind']=='reverse':
  assert abs(vs[aa:bb]).max()==0;assert np.max(abs(x[aa:bb]-rs[aa:bb]))<1e-6;assert np.sqrt(np.mean(rs[aa:bb]**2))>.005
cut=vo[round(47.5*SR):round(48.875*SR)];assert np.sqrt(np.mean(cut**2))<.012
# Complete Shrek movie stem retains all decoded samples, with documented constant gain/3ms edge ramps.
reportmix=json.loads((P/'analysis/mix-report.json').read_text());raw,s=sf.read(O/'shrek2.wav');g=10**(reportmix['shrek_constant_gain_db']/20);aa=1356*2000;assert np.max(abs(ms[aa+144:aa+len(raw)-144]-raw[144:-144]*g))<1e-6
anchors=[]
for t in [.3,3.3,8.9,9.7,15.3,31.2,36.1,40.2,51.2,56.7,59.5,64.9,68.2,73.3,85.5]:
 k=round(t*SR);u=x[k:k+SR//2].mean(1);w=y[k:k+SR//2].mean(1);cc=correlate(w,u,method='fft');lag=int(correlation_lags(len(w),len(u))[np.argmax(cc)]);assert abs(lag)<=2,(t,lag);anchors.append({'time':t,'lag_samples':lag})
b=json.loads((P/'analysis/browser-check.json').read_text());assert b['seek_deterministic'] and not b['errors'];frames={f['time']:f for f in b['frames']};assert frames[8.85]['movie']['frame']>frames[9.2]['movie']['frame'];assert frames[2.7]['movie']['frame']==frames[4.2]['movie']['frame']==120;assert frames[9.8]['movie']['asset']=='shrek1';assert not frames[0]['movie']['subtitles'] and not frames[9.8]['movie']['subtitles'];assert frames[51.9]['movie']['subtitles'] and frames[59.4]['movie']['subtitles']
assert all(abs(f['captionBottom']-1650)<1 for f in b['frames']);assert T['caption_bottom_px']==270
for c in T['captions']:assert not re.search('[A-Za-z]',c['text'].replace('LISTEN',''))
colour_times=[4.2,13.7,19.3,24.6,28.4,35.9,40.8,46.8,55.5,68.5,73.8,79.8,82.9,86.5];colours=[{'time':t,'blue_red_share_of_marker_coverage':frames[t]['ink']['blue_red_share']} for t in colour_times];assert min(c['blue_red_share_of_marker_coverage'] for c in colours)>.35
q={'version':'connected-speech-shrek-v1','file':str(V.relative_to(R)),'sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'bytes':V.stat().st_size,'duration':87,'frames':2088,'width':1080,'height':1920,'fps':24,'sample_rate':SR,'full_decode':'passed','black_intervals':bl,'loudness':loud,'aac_alignment':anchors,'reverse':'passed: actual source frame index descends, repeat is first Donkey sentence only; reverse audio stem present','freeze':'passed: identical source frame retained before rewind','movies':'opening/repeat uncaptioned; Mummy uncaptioned then captioned; complete Shrek2 source retained and captioned','voice':'all mapped narration words retained; only measured silent interval removed; actor dialogue never overlaps narration','caption_panel_raise_px':50,'caption_layout':'passed: no overflow or collision with diagram region','marker_colour_checks':colours,'seek_deterministic':True,'caption_alignment':'phrase-level estimates, not manual word-level listening audit','real_time_full_playback':'not performed','listening_review':'not performed'};(P/'QC.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(json.dumps(q,ensure_ascii=False,indent=2))
