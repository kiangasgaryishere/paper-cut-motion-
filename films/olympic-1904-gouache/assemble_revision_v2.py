"""Copy revised opening and unchanged later picture packets; encode full audio once."""
from pathlib import Path
import json,subprocess
p=Path(__file__).resolve().parent;root=p.parents[1];meta=json.loads((p/'segments.json').read_text())
source=[(p/'out/opening-delivery-v2.mp4',0,20)]+[(root/x['output'],x['start'],x['end']) for x in meta['parts'] if x['start']>=20]
entries=[]
for i,(src,a,b) in enumerate(source):
 dest=p/f'out/revision-v2-picture-{i:02d}.mp4'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-map','0:v:0','-an','-c:v','copy','-movflags','+faststart',str(dest)],check=True)
 entries.append((dest,a,b))
listing=p/'out/revision-v2.ffconcat'
listing.write_text('ffconcat version 1.0\n'+''.join(f"file '{dest}'\nduration {b-a}\n" for dest,a,b in entries))
output=root/'video/olympic-1904-final-v2.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listing),'-i',str(p/'out/revision-v2-mix.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-t','126','-movflags','+faststart',str(output)],check=True)
# A small ten-second review file lets the user compare the important opening quickly.
subprocess.run(['ffmpeg','-v','error','-y','-i',str(p/'out/opening-delivery-v2.mp4'),'-i',str(p/'out/revision-v2-mix.wav'),'-map','0:v:0','-map','1:a:0','-t','10','-frames:v','300','-c:v','libx264','-crf','20','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(root/'video/olympic-1904-opening-v2.mp4')],check=True)
manifest=dict(output='video/olympic-1904-final-v2.mp4',duration=126,fps=30,frames=3780,
 picture_blocks=[dict(source=str(src.relative_to(root)),start=a,end=b) for src,a,b in source],
 original_picture_unchanged_from=20,audio='out/revision-v2-mix.wav',effects='out/revision-v2-sfx.wav',
 voice='out/voice-master-v2.wav',narration_retimed=False,music='none',sound_bridges='sound-bridges-v2.json',
 opening_visual_cuts=[3.6,7.3,10.4],historical_note='No modern Olympic rings; the emblem postdates 1904.')
(p/'revision-v2.json').write_text(json.dumps(manifest,indent=2));print('Assembled full v2 and ten-second opening preview.')
