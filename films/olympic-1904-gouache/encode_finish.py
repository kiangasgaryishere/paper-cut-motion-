"""Encode accurate frame windows from the one continuous 40–126 picture render."""
from pathlib import Path
import json,subprocess
p=Path(__file__).resolve().parent;root=p.parents[1];f=p/'segments.json';meta=json.loads(f.read_text());meta['parts']=[x for x in meta['parts'] if x['start']<40];source_n=round(meta['source_decoded_duration']*48000)
for index,a in enumerate(range(40,126,10),5):
 b=min(a+10,126);video=f'video/olympic-1904-part{index:02d}-v1.mp4';mix=f'out/part{index:02d}-mix-v1.wav';fx=f'out/part{index:02d}-sfx-v1.wav'
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a-40),'-i',str(p/'out/finish-picture-v1.mp4'),'-i',str(p/mix),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','slow','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-t',str(b-a),'-frames:v',str((b-a)*30),'-movflags','+faststart',str(root/video)],check=True)
 meta['parts'].append(dict(id=f'part{index:02d}',start=a,end=b,status='encoded',revision='v1',output=video,source_sample_start=a*48000,source_sample_end_exclusive=min(b*48000,source_n),timeline_sample_end_exclusive=b*48000,source_padding_samples=max(0,b*48000-source_n),video_frame_start=a*30,video_frame_end_exclusive=b*30,mix_wav=mix,effects_wav=fx));print('Encoded',a,b,flush=True)
meta.update(next_part_start=None,completion_requested=True,production_complete=False,assembly_output='video/olympic-1904-final-v1.mp4',assembly_duration=126,source_exhausted=True,final_silent_padding_seconds=126-meta['source_decoded_duration'])
f.write_text(json.dumps(meta,indent=2))
