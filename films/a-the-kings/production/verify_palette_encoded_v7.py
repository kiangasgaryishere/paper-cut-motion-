from pathlib import Path
import json,subprocess,numpy as np
from PIL import Image
p=Path('films/a-the-kings/production');m=json.loads((p/'out/v7-palette-reference/manifest.json').read_text());out=p/'out/v7-palette-encoded';out.mkdir(exist_ok=True);expr='+'.join('eq(n\\,'+str(x['n'])+')' for x in m)
subprocess.run(['ffmpeg','-v','error','-y','-i','video/a-the-kings-v7.mp4','-vf','select='+expr,'-fps_mode','vfr',str(out/'%02d.png')],check=True)
rows=[]
for i,x in enumerate(m,1):
 a=np.array(Image.open(x['file']).convert('RGB')).astype(float);b=np.array(Image.open(out/f'{i:02d}.png').convert('RGB')).astype(float);err=float(np.abs(a-b).mean());assert err<5,(x['n'],err);rows.append(dict(frame=x['n'],mean_pixel_error=round(err,3)))

q=dict(encoded_palette_frames=rows);(p/"encoded-palette-QC-v7.json").write_text(json.dumps(q,indent=2));print("Palette frames verified:",len(rows))
