"""Verify the encoded real-footage edition and exact replacement/insert boundaries."""
from pathlib import Path
import json,hashlib,subprocess,io
import numpy as np,soundfile as sf
from scipy.signal import correlate,correlation_lags
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parents[1];R=P.parents[1];O=P/'out';A=P/'real-footage';V=R/'video/connected-speech-real-footage-v1.mp4';SR=48000

def run(args):return subprocess.run(args,capture_output=True,text=True,check=True)
m=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(V)]).stdout);v=next(s for s in m['streams'] if s['codec_type']=='video');a=next(s for s in m['streams'] if s['codec_type']=='audio');assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'24/1',1449);assert abs(float(m['format']['duration'])-60.375)<.01;assert a['sample_rate']=='48000';assert float(a['start_time'])==float(v['start_time'])==0
assert not run(['ffmpeg','-v','error','-i',str(V),'-f','null','-']).stderr
l=run(['ffmpeg','-hide_banner','-i',str(V),'-af','loudnorm=I=-14:TP=-1:LRA=7:print_format=json','-f','null','-']).stderr;loud=json.loads(l[l.rfind('{'):l.rfind('}')+1]);assert float(loud['input_tp'])<=-1
run(['ffmpeg','-y','-v','error','-i',str(V),'-vn','-c:a','pcm_f32le',str(O/'real-decoded.wav')]);x,sr=sf.read(O/'real-mix.wav');y,sy=sf.read(O/'real-decoded.wav');assert sr==sy==SR
n=114000;i=90000;j=288000;assert np.max(abs(x[i:i+n]-x[j:j+n]))<1e-12
base,sr=sf.read(O/'mix.wav');assert np.max(abs(x[j+n:]-base[j:]))<1e-6 # exact downstream shift, no narration editing
clip,sr=sf.read(O/'real-clip-audio.wav');clip*=10**(-.5/20);f=144;clip[:f]*=np.linspace(0,1,f)[:,None];clip[-f:]*=np.linspace(1,0,f)[:,None];assert np.max(abs(x[i:i+len(clip)]-clip))<1e-6 # no residual narrator voice
anchors=[]
for t in [2.1,3.2,6.2,7.3,8.6,29.1,44.6,58.1]:
 k=round(t*SR);u=x[k:k+SR//2].mean(1);w=y[k:k+SR//2].mean(1);cor=correlate(w,u,method='fft');lag=int(correlation_lags(len(w),len(u))[np.argmax(cor)]);assert abs(lag)<=2;anchors.append({'t':t,'lag_samples':lag})
# First screening is free of Persian captions as well as English answer text.
t=json.loads((P/'timeline.json').read_text());assert not any(c['start_frame']<102 and c['end_frame']>45 for c in t['captions'])
black=run(['ffmpeg','-hide_banner','-i',str(V),'-vf','blackdetect=d=.1:pix_th=.08','-an','-f','null','-']).stderr;assert not any('black_start:' in l for l in black.splitlines())
# Inspectable encoded stills include both screenings and downstream teaching/CTA.
times=[.8,2.7,5,6.8,8.6,12.6,26.9,34.3,43.5,49.8,59.9];sheet=Image.new('RGB',(1080,3*515),'#dedbd6');d=ImageDraw.Draw(sheet)
for n,t in enumerate(times):
 raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(V),'-frames:v','1','-vf','scale=270:480','-f','image2pipe','-vcodec','mjpeg','-']);im=Image.open(io.BytesIO(raw));xx=n%4*270;yy=n//4*515;sheet.paste(im,(xx,yy+25));d.text((xx+8,yy+6),str(t)+'s',fill='black')
sheet.save(A/'contact-sheet.jpg',quality=94)
report={'file':str(V.relative_to(R)),'sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'bytes':V.stat().st_size,'duration':60.375,'frames':1449,'fps':24,'width':1080,'height':1920,'sample_rate':SR,'full_decode':'passed','black_intervals':[],'loudness':loud,'aac_alignment':anchors,'first_screening_subtitles':False,'second_screening_subtitle':'Honey, what you doing?','narrator_quote_replaced':'passed: PCM exactly matches supplied clip audio, no voice mixed underneath','screening_audio_equality':'passed: two screenings sample-identical before AAC','downstream_shift':'passed: source mix from 6.0s onward retained sample-identical after 57-frame insert','caption_contrast':{'foreground':'#FFFFFF','background':'#1B1C20'},'listening_review':'not performed','real_time_full_playback':'not performed'}
(A/'QC.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
