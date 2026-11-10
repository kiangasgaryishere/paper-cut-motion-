import json,subprocess,concurrent.futures
from pathlib import Path
p=Path('films/a-the-kings/production');m=json.loads((p/'out/v5-patches/manifest.json').read_text())
def encode(e):
 out=Path(e['path']+'.mp4');subprocess.run(['ffmpeg','-v','error','-y','-framerate','30','-i',e['path']+'/%04d.jpg','-frames:v',str(e['frames']),'-c:v','libx264','-threads','2','-preset','fast','-crf','14','-pix_fmt','yuv420p',str(out)],check=True);return str(out)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:clips=list(ex.map(encode,m))
args=['ffmpeg','-v','error','-y','-i',str(p/'out/picture-v4.mp4')]
for f in clips:args+=['-i',f]
filters=[];last='0:v'
for i,e in enumerate(m,1):
 lo,hi=e['start_frame'],e['end_frame'];filters.append(f'[{i}:v]setpts=PTS-STARTPTS+({lo}/30-0.00001)/TB[p{i}]');filters.append(f"[{last}][p{i}]overlay=enable='gte(t,{lo/30-.00002})*lt(t,{hi/30-.00002})':eof_action=repeat[v{i}]");last=f'v{i}'
args+=['-filter_complex_threads','2','-filter_complex',';'.join(filters),'-map',f'[{last}]','-an','-frames:v','2373','-c:v','libx264','-threads','3','-preset','medium','-crf','14','-pix_fmt','yuv420p',str(p/'out/picture-v5.mp4')]
subprocess.run(args,check=True);print('Reused v4 picture; replaced',sum(e['frames'] for e in m),'frames in',len(m),'revised sections.')
