"""Append all manifest parts, preserving picture packets and encoding audio once."""
from pathlib import Path
import json,subprocess,numpy as np,soundfile as sf
p=Path(__file__).resolve().parent;root=p.parents[1];meta=json.loads((p/'segments.json').read_text());parts=sorted(meta['parts'],key=lambda x:x['start']);buffers=[];previous=0;paths=[]
for part in parts:
 assert part['start']==previous,('Gap/overlap',part);previous=part['end'];wav,sr=sf.read(p/part['mix_wav']);assert sr==48000 and len(wav)==round((part['end']-part['start'])*sr)
 video=root/part['output'];assert video.is_file();buffers.append(wav)
 # Remove each review clip's AAC stream before the concat demuxer sees it.
 # AAC encoder priming can otherwise shift copied video by ~21 ms.
 picture=p/'out'/(part['id']+'-picture-only.mp4')
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(video),'-map','0:v:0','-an','-c:v','copy','-movflags','+faststart',str(picture)],check=True)
 paths.append((picture,part['end']-part['start']))
joined=np.concatenate(buffers,axis=0);assert len(joined)==round(previous*48000);sf.write(p/'out/assembled-mix.wav',joined,48000,subtype='PCM_24')
# The prefix PCM is retained bit-for-bit; only the final AAC encode sees a boundary.
check,_=sf.read(p/'out/assembled-mix.wav');assert np.array_equal(check[:len(buffers[0])],buffers[0])
def quote(path):return str(path).replace("'","'\\''")
listing=p/'out/concat-parts.ffconcat';listing.write_text('ffconcat version 1.0\n'+''.join("file '"+quote(path)+"'\nduration "+str(d)+'\n' for path,d in paths))
output=root/meta['assembly_output'];subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listing),'-i',str(p/'out/assembled-mix.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-t',str(previous),'-movflags','+faststart',str(output)],check=True)
meta['assemblies']=[dict(output=meta['assembly_output'],start=0,end=previous,frames=round(previous*30),audio_encoded_once=True,picture_stream_copied=True,parts=[x['id'] for x in parts])];(p/'segments.json').write_text(json.dumps(meta,indent=2));print('Assembled',previous,'seconds:',output)
