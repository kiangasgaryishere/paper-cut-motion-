from pathlib import Path
import json, runpy
import numpy as np
from PIL import Image,ImageDraw,ImageFont,features
from scipy.ndimage import label,find_objects
P=Path(__file__).resolve().parents[1]; root=P.parents[1]
# Load only thinning/tracing helpers; avoid the older project's main().
src=(root/'films/connected-speech-marker/tools/upstream-skeleton.py').read_text()
src=src.replace('elif strokes:\n            strokes[-1].extend(path)\n        else:\n            strokes.append(path)', 'else:\n            strokes.append(path)')
# Helpers share globals, including NB and rdp.
G=dict(np=np);exec(src[src.index('def thin('):src.index('def main(')],G)
f=ImageFont.truetype(str(root/'films/connected-speech-marker/fonts/Persian.ttf'),180)
out={}
for key,s in [('hook','ثبت‌نام نکن!'),('cta','برنامه'),('brand','رهنما')]:
 im=Image.new('L',(2400,500));d=ImageDraw.Draw(im);d.text((20,0),s,font=f,fill=255,direction='rtl')
 b=im.getbbox();im=im.crop(b);a=np.array(im)>110
 paths=[]
 labels,count=label(a,structure=np.ones((3,3)))
 for i,sl in enumerate(find_objects(labels)):
  mask=labels[sl]==i+1;y0,x0=sl[0].start,sl[1].start
  if max(mask.shape)<40:
   yy,xx=np.nonzero(mask);xx=float(xx.mean()+x0);yy=float(yy.mean()+y0);paths.append([(xx-1.5,yy),(xx+1.5,yy)])
  else:
   paths.extend([[(x+x0,y+y0) for x,y in path] for path in G['trace'](G['thin'](mask))])
 out[key]={'w':im.width,'h':im.height,'paths':[G['rdp'](p if len(p)>1 else [p[0],(p[0][0]+.4,p[0][1]+.4)],1.0) for p in paths]}
(P/'assets/persian-strokes.json').write_text(json.dumps(out,default=int))
print('RAQM',features.check('raqm'),[(k,len(v['paths'])) for k,v in out.items()])
# Captions from the supplied script, phrase timing anchored to measured source pauses.
rows=[
(0,1.94,'کلاس زبان ثبت‌نام نکن،'),(2.07,4.33,'اگه قراره این ۵ تا چیز رو از دست بدی!'),(4.63,5.81,'مخصوصاً آخری!'),
(6.21,8.09,'اول، فقط تعیین سطح؟'),(8.44,10.25,'اینکه بگن سطحت چیه'),(10.25,12,'و برو بشین تو فلان ترم که کاری نداره!'),(12.43,14.29,'تو رهنما، براساس نیازت'),(14.53,15.98,'یه نقشهٔ راه یادگیری می‌چینیم؛'),(16.36,19.03,'با برنامهٔ ترمی و هفتگی مخصوص خودت.'),
(19.61,22.56,'دوم، همون محتوای تکراری برای همه؟'),(22.95,25.38,'هر هفته محتوای مخصوص خودت رو می‌گیری؛'),(25.78,27.81,'فیلم، پادکست، بازی و تمرین‌هایی'),(27.95,31.18,'که برای نیازهای تو انتخاب یا طراحی شدن.'),
(31.67,34.62,'سوم، گرامر بخون، تمرین حل کن؟'),(34.92,37.39,'اینجا گرامر رو توی بازی استفاده می‌کنی،'),(37.74,39.7,'توی بحث بقیه رو قانع می‌کنی،'),(39.93,41,'نقش بازی می‌کنی'),(41.2,42.78,'و با زبان مسئله حل می‌کنی.'),
(43.34,46.01,'چهارم، یادگیری فقط توی کلاس؟'),(46.25,47.87,'بیرون کلاس هم تمرین می‌کنی،'),(48.01,48.95,'سؤال می‌پرسی'),(49.14,50.8,'و روی کارهات بازخورد می‌گیری.'),(51.19,54.03,'حتی می‌تونی توی یک ترم از چند مدرس یاد بگیری.'),
(54.42,57.03,'پنجم، این یکی رو احتمالاً نشنیدی!'),(57.46,60.53,'تمرین‌ها، اشتباهات و پیشرفتت ثبت می‌شن.'),(60.97,63.59,'چند نفر از تیم آموزشی با هم بررسی‌شون می‌کنن'),(63.85,66.67,'تا برنامهٔ هفتهٔ بعدت دقیق‌تر طراحی بشه.'),
(67,69.79,'این چیزیه که داریم تو آکادمی رهنما اجرا می‌کنیم.'),(70.17,72.97,'اگه می‌خوای ببینی برنامهٔ مخصوص خودت چه شکلیه،'),(73.21,75.09,'کلمهٔ «برنامه» رو کامنت کن!')]
caps=[{'start':max(0,round(a-.03,3)),'end':round(b+.05,3),'text':s} for a,b,s in rows]
for a,b in zip(caps,caps[1:]):a['end']=min(a['end'],b['start'])
(P/'captions.json').write_text(json.dumps(caps,ensure_ascii=False,indent=2))
