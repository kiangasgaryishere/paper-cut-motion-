from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parents[1]
rows=[
(.14,3.86,'یکی از افسانه‌ای‌ترین میم‌های اینترنت بالاخره مُرد!'),
(5.27,7.81,'فکر کنم بگم، خودت می‌فهمی منظورم چیه.'),
(8.62,10.7,'بریم چندتا از بهتریناشو ببینیم؛'),(10.99,13.6,'آخریش دیگه واقعاً یه چیز دیگه‌ست!'),
(14.16,16.55,'حتی فضایی‌ها هم قبل از جی‌تی‌ای شش رسیدن!'),(16.92,19.83,'حتی فضایی‌ها هم زودتر از جی‌تی‌ای شش رسیدن!'),
(20.4,23.62,'حتی توییتر هم قبل از جی‌تی‌ای شش، ایکس شد!'),(23.95,26.21,'توییتر کلاً هویتش عوض شد!'),
(26.81,30.01,'مسی هم قبل از جی‌تی‌ای شش جام جهانی رو برد!'),(30.33,32.52,'مسی بالاخره جام جهانی رو برد!'),
(33.05,35.33,'رونالدو از منچستریونایتد رفت…'),(35.61,36.69,'به النصر پیوست…'),(36.91,38.47,'و حتی به تهران هم اومد!'),(38.86,41.75,'رونالدو تو این مدت یه زندگی کامل کرد!'),
(42.2,44.32,'همهٔ این‌ها قبل از جی‌تی‌ای شش!'),(44.77,47.5,'حتی پاپ جدید هم قبل از جی‌تی‌ای شش اومد!'),(47.77,49.34,'حتی پاپ هم عوض شد!'),
(49.81,51.77,'ولی آخری از همه عجیب‌تره…'),(52.27,55.07,'خود جی‌تی‌ای شش هم نامزد جایزه شد…'),(55.38,57.13,'قبل از اینکه جی‌تی‌ای شش بیاد!'),
(57.47,59.6,'یعنی خود جی‌تی‌ای شش هم قبل از جی‌تی‌ای شش'),(59.6,61.67,'نامزد جایزه شد!'),
(62.2,64.23,'ولی بالاخره انتظار تموم شد…'),(64.84,67.36,'و این میم افسانه‌ای هم بازنشسته شد.'),(68.18,69.25,'در آرامش بخواب، افسانه.')]
caps=[{'start':max(0,round(a-.03,3)),'end':round(b+.05,3),'text':s} for a,b,s in rows]
for a,b in zip(caps,caps[1:]):a['end']=min(a['end'],b['start'])
(P/'captions.json').write_text(json.dumps(caps,ensure_ascii=False,indent=2)+'\n')
def srt(t):
 m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'
(P/'captions.fa.srt').write_text('\n\n'.join(f"{i+1}\n{srt(c['start'])} --> {srt(c['end'])}\n{c['text']}" for i,c in enumerate(caps))+'\n')
inputs=[]
for path,name in [('script.md','script.md'),('assets/narration.mp3','ElevenLabs_2026-11-21T10_48_34_Daniel - Steady Broadcaster_pre_s56_sim75_v4.mp3')]:
 b=(P/path).read_bytes();inputs.append({'path':path,'original_name':name,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'retained_complete':True})
(P/'assets/input-manifest.json').write_text(json.dumps(inputs,indent=2)+'\n')
p=P/'brief.json';b=json.loads(p.read_text());b.update(status='preproduction-in-progress',script_supplied=True,narration_supplied=True,footage_approach='Original generated photographic illustrations; no official gameplay or news-photo claims',publication_condition='User confirmed on2026-11-21: publish only after actual confirmed release; not independent verification of current release',humour='selective meme beats and user-authorized over-the-top moments',characters=['Lucia Caminos','Jason Duval'],source_voice_duration=3350361/48000,output_duration=71,fps=24,narration_retimed=False,music=False);b['not_started']=['full_render'];p.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
print('prepared',len(caps),'Persian subtitle phrases')
