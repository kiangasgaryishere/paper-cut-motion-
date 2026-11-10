from pathlib import Path
import json,subprocess,re
p=Path('films/a-the-kings/production')
def measure(f):
 r=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(f),'-vn','-af','loudnorm=I=-12:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
 d=json.loads(re.findall(r'\{[^{}]+\}',r.stderr)[-1]);return {k:float(d[k]) for k in ['input_i','input_tp','input_lra']}
old=measure('video/a-the-kings-v6.mp4');new=measure('video/a-the-kings-v7.mp4');delta=new['input_i']-old['input_i']
assert -13<=new['input_i']<=-11 and new['input_tp']<=-1
assert 1.2<=delta<=3.0
q=json.loads((p/'audio-QC-v7.json').read_text());q.update(previous_encoded=old,final_encoded=new,loudness_increase_LU=round(delta,2));(p/'audio-QC-v7.json').write_text(json.dumps(q,indent=2));print(json.dumps(q,indent=2))
