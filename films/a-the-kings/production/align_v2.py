import json,re,math
from pathlib import Path
p=Path(__file__).parent
# Onsets below follow native Whisper segments, refined against observed pauses in the recording.
# Continuous speech boundaries retain the model timestamp; they are not word-level forced alignment.
items=[
(.225167,3.121208,'می‌دونی چرا توی انگلیسی یه‌جا A میاریم، یه‌جا THE؟','Why do we sometimes use A, and sometimes THE?',0),
(3.751458,6.5895,'برای جواب، بریم به انگلستانِ هزار سال پیش!','For the answer, let’s visit England a thousand years ago!',1),
(7.050875,11.09725,'سال ۱۰۶۶، پادشاه انگلستان بدون وارث از دنیا می‌ره.','In 1066, the king of England dies without an heir.',2),
(11.490833,13.410417,'حالا انگلستان به یه پادشاه احتیاج داره:','Now England needs a king:',3),
(13.839833,15.422708,'England needs a king.','England needs a king.',3),
(16.18625,19.320708,'ولی مشکل اینجاست که سه نفر تاج‌وتخت رو برای خودشون می‌خوان!','But three men each want the throne!',4),
(19.81125,21.53875,'اول هارولد تاج‌گذاری می‌کنه.','First, Harold is crowned.',5),
(21.864208,23.739958,'اما پادشاه نروژ حمله می‌کنه!','But the king of Norway invades!',6),
(24.103875,25.10,'هارولد شکستش می‌ده،','Harold defeats him,',7),
(25.10,27.0,'ولی هنوز نفس راحت نکشیده که','but before he can catch his breath,',7),
(27.0,29.338958,'ویلیام با یه لشکر دیگه از راه می‌رسه!','William arrives with another army!',8),
(29.755917,32.398458,'این بار هارولد کشته می‌شه و ویلیام می‌شه:','This time, Harold is killed, and William becomes:',9),
(32.702792,33.989542,'The king of England!','The king of England!',10),
(34.531958,35.423125,'حالا دقت کردی؟','Notice what happened?',11),
(35.697375,37.355708,'اول گفتیم A KING؛','First, we said A KING:',11),
(37.57625,38.611792,'یعنی یه پادشاه،','a king—',11),
(38.800625,40.102667,'هنوز مشخص نکردیم کدوم.','we haven’t specified which one.',11),
(40.533292,43.737792,'ولی THE KING یعنی اون پادشاه مشخص!','But THE KING means that particular king!',12),
(44.17875,47.668625,'و جالبه که ریشهٔ این تفاوت به انگلیسی قدیم برمی‌گرده!','The roots of this distinction go back to Old English!',13),
(48.103875,50.664917,'A از کلمهٔ ĀN به معنی «یک» اومده.','A comes from ĀN, meaning “one.”',13),
(51.084417,53.717042,'اما THE از خانوادهٔ کلمهٔ اشارهٔ that؛','THE belongs to the demonstrative family, like “that”:',14),
(53.947542,56.074125,'چیزی شبیه «اون» و «همون» خودمون!','something like “that one” or “the very one.”',14),
(56.775958,57.712375,'پس فرق اصلی چیه؟','So what’s the key difference?',15),
(58.017042,61.68,'وقتی شنونده می‌تونه بفهمه دقیقاً کدوم چیز رو می‌گی،','When your listener can identify exactly which thing you mean,',15),
(61.68,62.965542,'معمولاً THE میاریم؛','we usually use THE;',15),
(63.356917,65.137208,'حتی اگه قبلاً اسمش رو نشنیده باشه!','even if it hasn’t been mentioned before!',16),
(65.468583,69.995583,'برای تمرین این تفاوت، یه چالش تصویری و یه ورک‌شیت کاربردی آماده کردیم.','To practise, we’ve prepared a visual challenge and a practical worksheet.',17),
(70.323,72.392208,'فقط THE رو کامنت کن تا برات بفرستیم!','Just comment THE and we’ll send them to you!',18),
]
cues=[]
for a,b,fa,en,scene in items:
 # Snap before onset, not after it: 20–53 ms lead at 30 fps.
 t0=max(0,math.floor((a-.020)*30)/30)
 cues.append(dict(t0=round(t0,6),t1=round(b+.06,6),text=fa,en=en,scene=scene,speech_onset=a,speech_end=b,lead_ms=round((a-t0)*1000,2),timing_method='Whisper native segments + silence-edge refinement; continuous boundaries approximate'))
for x,y in zip(cues,cues[1:]):x['t1']=min(x['t1'],y['t0'])
shots=json.loads((p/'scenes.json').read_text());starts=[next(x[0] for x in items if x[4]==i) for i in range(19)]
for i,s in enumerate(shots):
 s['start']=starts[i] if i else 0;s['end']=starts[i+1] if i<18 else 72.766666667
 s['timing_status']='speech_anchored_v2';s['visual_reveal']=s['start'];s['on_screen_text']='captions + selected headlines; A/THE on first cards; THE in comment box'
 for k in list(s):
  if 'provisional' in k:s.pop(k)
 s['action']=s['visual']
 s['sound_policy']='Original voice unchanged; foley at visual events; no music.'
(p/'captions.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2))
(p/'scenes.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2))
art=json.loads((p/'art-v2.json').read_text());titles=json.loads((p/'titles.json').read_text())
(p/'data.js').write_text('const ART='+json.dumps(art)+';const SHOTS='+json.dumps(shots)+';const CUES='+json.dumps(cues,ensure_ascii=False)+';const TITLES='+json.dumps(titles,ensure_ascii=False)+';')
(p/'captions-en.json').write_text(json.dumps([dict(t0=c['t0'],t1=c['t1'],text=c['en']) for c in cues],ensure_ascii=False,indent=2))
print('captions',len(cues),'scene onsets',starts,'lead ms',min(c['lead_ms'] for c in cues),max(c['lead_ms'] for c in cues))
