"""Reuse v2 picture outside the Hicks patch; encode continuous edited audio once."""
from pathlib import Path
import json,subprocess
p=Path(__file__).resolve().parent;root=p.parents[1];meta=json.loads((p/'segments.json').read_text());revision=json.loads((p/'revision-v2.json').read_text())
sources=[(root/x['source'],x['start'],x['end'],x['start'],x['end']) for x in revision['picture_blocks'] if x['end']<=70]
sources.append((p/'out/hicks-delivery-v3.mp4',70,2930/30,70,100))
sources.extend((root/x['output'],x['start']-70/30,x['end']-70/30,x['start'],x['end']) for x in meta['parts'] if x['start']>=100)
entries=[];end=0
for i,(src,a,b,sa,sb) in enumerate(sources):
 assert abs(a-end)<.000001;end=b;dest=p/f'out/revision-v3-picture-{i:02d}.mp4'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-map','0:v:0','-an','-c:v','copy','-movflags','+faststart',str(dest)],check=True);entries.append((dest,b-a))
assert abs(end-3710/30)<.000001
listing=p/'out/revision-v3.ffconcat';listing.write_text('ffconcat version 1.0\n'+''.join(f"file '{src}'\nduration {d:.12f}\n" for src,d in entries))
output=root/'video/olympic-1904-final-v3.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listing),'-i',str(p/'out/revision-v3-mix.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-t',str(3710/30),'-movflags','+faststart',str(output)],check=True)
# Review the three new shots and the direct transition to the recap.
subprocess.run(['ffmpeg','-v','error','-y','-ss',str(2242/30),'-i',str(output),'-t',str(567/30),'-frames:v','567','-c:v','libx264','-crf','20','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(root/'video/olympic-1904-hicks-v3.mp4')],check=True)
manifest=dict(output='video/olympic-1904-final-v3.mp4',duration=3710/30,frames=3710,fps=30,
 picture_blocks=[dict(source=str(src.relative_to(root)),output_start=a,output_end=b,source_start=sa,source_end=sb) for src,a,b,sa,sb in sources],
 patch_output_start=70,patch_output_end=2930/30,three_new_source_shots=[dict(kind='close',start=2242/30,end=81),dict(kind='pov',start=81,end=2554/30),dict(kind='assisted',start=2554/30,end=2749/30)],
 removed_source_interval=[2749/30,2819/30],removed_frames=70,removed_samples=112000,audio_edit='audio-edit-v3.json',
 audio='out/revision-v3-mix.wav',effects='out/revision-v3-sfx.wav',voice='out/revision-v3-voice.wav',music='none',audio_encoded_once=True,narration_speed_changed=False,sound_design='sound-design-v3.json',sound_kit='SFX Kit by Wyzowl, CC0-1.0',
 review_output='video/olympic-1904-hicks-v3.mp4',review_start=2242/30,review_duration=567/30)
(p/'revision-v3.json').write_text(json.dumps(manifest,indent=2));print('Assembled v3: 3710 frames; repeated 70-frame sentence removed.')
