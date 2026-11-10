import json,math,re
from pathlib import Path
p=Path(__file__).parent
# New recording: native ASR phrase timing refined against recording pauses.
items=[
(0,1.757458,'می‌دونی چرا توی انگلیسی…',0),
(2.062,2.663042,'«یه پادشاه»…',0),
(2.960625,4.1845,'یا «اون پادشاه»؟',0),
(4.91725,6.196833,'برای فهمیدن تفاوتشون،',1),
(6.380458,10.242208,'بریم سراغ یکی از جنجالی‌ترین دعواهای تاج‌وتخت تاریخ انگلستان!',1),
(10.857958,12.37225,'سال ۱۰۶۶،',2),
(12.659333,15.134625,'پادشاه انگلستان بدون وارث از دنیا می‌ره.',2),
(15.773042,17.752417,'حالا انگلستان به یه پادشاه نیاز داره:',3),
(18.427875,20.176958,'انگلستان به یک پادشاه نیاز دارد.',3),
(21.1785,24.327583,'ولی مشکل اینجاست که سه نفر اون تاج رو برای خودشون می‌خوان!',4),
(25.022792,26.503625,'اول هارولد تاج‌گذاری می‌کنه.',5),
(27.039792,28.880667,'اما پادشاه نروژ حمله می‌کنه!',6),
(29.546208,30.6751875,'هارولد شکستش می‌ده،',7),
(30.6751875,32.6751875,'ولی هنوز نفس راحت نکشیده که',7),
(32.6751875,34.760542,'ویلیام با یه لشکر دیگه از راه می‌رسه!',8),
(35.411292,37.979,'این بار هارولد کشته می‌شه و ویلیام می‌شه:',9),
(38.24225,39.361208,'پادشاهِ انگلستان!',10),
(40.353125,41.174208,'حالا دقت کردی؟',11),
(41.619875,42.837583,'اول گفتیم «یه پادشاه»؛',11),
(43.128083,44.073125,'یعنی یه پادشاه،',11),
(44.383,45.589417,'هنوز مشخص نکردیم کدوم.',11),
(46.2245,48.873708,'ولی «اون پادشاه» یعنی پادشاه مشخص!',12),
(49.797542,52.903,'و جالبه که ریشهٔ این تفاوت به انگلیسی قدیم برمی‌گرده!',13),
(53.605917,56.307958,'«اِی» از واژهٔ «آن» به معنی «یک» اومده.',13),
(56.885042,59.941542,'اما حرف تعریفِ معیّن از خانوادهٔ واژه‌های اشاره است؛',14),
(60.309542,62.229542,'چیزی شبیه «اون» و «همون» خودمون!',14),
(63.060917,64.363167,'پس فرق اصلی چیه؟',15),
(65.165333,68.159958,'وقتی شنونده می‌تونه بفهمه دقیقاً کدوم چیز رو می‌گی،',15),
(68.409542,69.666833,'معمولاً حرف تعریفِ معیّن میاریم؛',15),
(69.927833,71.558958,'حتی اگه قبلاً اسمش رو نشنیده باشه!',16),
(72.195708,76.522625,'برای تمرین این تفاوت، یه چالش تصویری و یه ورک‌شیت کاربردی آماده کردیم.',17),
(76.941208,78.863792,'فقط همین کلمه رو کامنت کن تا برات بفرستیم!',18)]
cues=[]
for a,b,t,i in items:
 start=max(0,math.floor((a-.02)*30)/30);cues.append(dict(t0=start,t1=b+.06,text=t,en='',scene=i,speech_onset=a,speech_end=b,timing_method='New recording: ASR phrase + pause refinement; continuous boundaries approximate'))
for a,b in zip(cues,cues[1:]):a['t1']=min(a['t1'],b['t0'])
shots=json.loads((p/'scenes.json').read_text());titles=json.loads((p/'titles.json').read_text());starts=[next(a for a,b,t,k in items if k==i) for i in range(19)]
meta=dict(source_duration=90.456,decoded_duration=90.4,render_duration=79.1,trim_end=79.1,tail_decision='trim_after_script_cta_user_approved',script_content_end=78.863792,a_root_at=53.605917,the_point_at=60.309542,comment_keyword_at=77.3225,hook_a_at=2.062,hook_the_at=3.4)
# User approved removing the extra tail. Cut at 79.1 s inside the pause after the script CTA.
for i,s in enumerate(shots):
 s['start']=starts[i];s['end']=starts[i+1] if i<18 else meta['render_duration'];s['timing_status']='new_audio_phrase_anchored_v4'
titles.update({'0':'A KING یا THE KING؟','1':'دعوای تاج‌وتخت انگلستان'})
art=json.loads((p/'art-v4.json').read_text())
(p/'captions.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2));(p/'scenes.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2));(p/'titles.json').write_text(json.dumps(titles,ensure_ascii=False,indent=2));(p/'meta-v4.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
(p/'data.js').write_text('const ART='+json.dumps(art)+';const SHOTS='+json.dumps(shots)+';const CUES='+json.dumps(cues,ensure_ascii=False)+';const TITLES='+json.dumps(titles,ensure_ascii=False)+';const META='+json.dumps(meta)+';')
assert all(not re.search('[A-Za-z]',c['text']) for c in cues)
print(len(cues),'Persian-only cues; new audio; user-approved ending at 79.1 seconds.')
