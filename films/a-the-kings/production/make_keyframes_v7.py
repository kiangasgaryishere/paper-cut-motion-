from pathlib import Path
import json,subprocess
from PIL import Image,ImageDraw
p=Path('films/a-the-kings/production');out=p/'out/v7-keyframes';out.mkdir(exist_ok=True)
shots=json.loads((p/'scenes.json').read_text());times=[(s['start']+s['end'])/2 for s in shots]
for i,t in {0:3.7,9:37.2,13:54.3,14:61.0,15:66.0,16:71.0,17:74.0,18:78.3}.items():times[i]=t
ns=[round(t*30) for t in times];expr='+'.join('eq(n\\,'+str(n)+')' for n in ns)
subprocess.run(['ffmpeg','-v','error','-y','-i','video/a-the-kings-v7.mp4','-vf','select='+expr,'-fps_mode','vfr',str(out/'%02d.png')],check=True)
board=Image.new('RGB',(1350,2040),'#fff9f2');draw=ImageDraw.Draw(board)
for i,n in enumerate(ns):
 im=Image.open(out/f'{i+1:02d}.png');im.thumbnail((270,480));x=(i%5)*270;y=(i//5)*510;board.paste(im,(x,y));draw.text((x+8,y+487),f'{i+1:02d} | {n/30:.2f}s',fill='#14233f')
board.save(p/'keyframes-v7.jpg',quality=92)
