"""Build the real-footage edition from the native real=1 render.
Two verbatim clip screenings; actor audio replaces synthesized English quote.
"""
from pathlib import Path
import json,subprocess
import numpy as np,soundfile as sf
P=Path(__file__).resolve().parents[1];R=P.parents[1];O=P/'out';A=P/'real-footage';SR=48000;D=57/24;INSERT=6.;FIRST=45/24
O.mkdir(exist_ok=True);A.mkdir(exist_ok=True)
def ff(*args):subprocess.run(['ffmpeg','-y','-v','error',*map(str,args)],check=True)
# Keep the original entire supplied clip's decoded audio. It is already close to voice loudness.
ff('-i',P/'assets/mummy-real-clip.mp4','-vn','-ar',SR,'-ac',2,'-c:a','pcm_f32le',O/'real-clip-audio.wav')
clip,sr=sf.read(O/'real-clip-audio.wav');assert sr==SR and len(clip)<=round(D*SR)
clip*=10**(-.5/20) # measured source TP -1.62 dBTP, leave AAC headroom
pad=np.zeros((round(D*SR),2));pad[:len(clip)]=clip
# Very short ramps only at recording edges; keep every source sample and natural interior pauses.
f=round(.003*SR);pad[:f]*=np.linspace(0,1,f)[:,None];tail=min(len(clip),len(pad));pad[tail-f:tail]*=np.linspace(1,0,f)[:,None]
base,sr=sf.read(O/'mix.wav');assert sr==SR and len(base)==58*SR
voice,voice_sr=sf.read(O/'voice.wav');assert voice_sr==SR
base[:round(FIRST*SR)]=voice[:round(FIRST*SR),None]*10**(-2/20) # Remove obsolete figure-drawing foley from the intro.
base[round(FIRST*SR):round((FIRST+D)*SR)]=pad # complete replacement, never mix narrator quote underneath
at=round(INSERT*SR);mix=np.concatenate([base[:at],pad,base[at:]])
assert len(mix)==round((58+D)*SR)
sf.write(O/'real-mix.wav',mix,SR,subtype='PCM_24')
# Patch picture on the original source clock, then insert the captioned replay in that same edit map.
# 57 replay frames preserve 56 supplied frames at 24fps with a short held last frame.
filtergraph=(
 '[1:v]fps=24,scale=960:408:flags=lanczos,setsar=1,split=2[c1][c2];'
 '[c1]tpad=start_mode=clone:start_duration=1.875:stop_mode=clone:stop_duration=6.75,trim=end_frame=162,setpts=PTS-STARTPTS[first];'
 '[0:v][first]overlay=60:646:eof_action=pass:enable=\'lt(t,6.75)\'[base];'
 '[base]split=2[b1][b2];[b1]trim=start_frame=0:end_frame=144,setpts=PTS-STARTPTS[before];'
 '[b2]trim=start_frame=144:end_frame=1392,setpts=PTS-STARTPTS[after];'
 '[c2]tpad=stop_mode=clone:stop_duration=1,trim=end_frame=57,setpts=PTS-STARTPTS[reclip];'
 '[2:v]fps=24,trim=end_frame=57,setpts=PTS-STARTPTS[paper];'
 '[paper][reclip]overlay=60:646:shortest=1[replay];'
 '[before][replay][after]concat=n=3:v=1:a=0,format=yuv420p[v]'
)
ff('-filter_complex_threads',2,'-i',O/'real-base.mp4','-i',P/'assets/mummy-real-clip.mp4','-loop',1,'-framerate',24,'-i',O/'real-replay-background.png','-i',O/'real-mix.wav','-filter_complex',filtergraph,'-map','[v]','-map','3:a:0','-c:v','libx264','-preset','medium','-threads',4,'-crf',16,'-c:a','aac','-b:a','256k','-ar',SR,'-t',58+D,'-movflags','+faststart',R/'video/connected-speech-real-footage-v1.mp4')
metadata={
 'version':'real-footage-v1','duration_frames':1449,'fps':24,'duration_seconds':58+D,'sample_rate':SR,
 'source_clip':'assets/mummy-real-clip.mp4','transcript':'Honey, what you doing?',
 'first_screening':{'start_frame':45,'end_frame':102,'start_seconds':FIRST,'end_seconds':FIRST+D,'subtitles':False,'audio':'supplied clip only; narrator quote and existing foley completely replaced'},
 'second_screening':{'start_frame':144,'end_frame':201,'start_seconds':6,'end_seconds':6+D,'subtitles':'English: Honey, what you doing?','audio':'same supplied clip audio'},
 'edit_map':[{'kind':'base','source_start_frame':0,'source_end_frame':144,'output_start_frame':0,'output_end_frame':144},{'kind':'clip_replay','clip_start_frame':0,'output_start_frame':144,'output_end_frame':201},{'kind':'base','source_start_frame':144,'source_end_frame':1392,'output_start_frame':201,'output_end_frame':1449}],
 'removed_narrator_quote_source_interval':[FIRST,FIRST+D],
 'clip_decoded_samples':len(clip),'clip_audio_padding_samples':len(pad)-len(clip),'music':'none added; supplied movie audio retained',
 'captions':'white on charcoal; Persian for lesson, English for replay and teaching examples, final LISTEN retained',
 'voice_after_insert_shift_frames':57,'original_illustrated_video_preserved':True
}
(A/'timeline.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n');print(json.dumps(metadata,ensure_ascii=False,indent=2))
