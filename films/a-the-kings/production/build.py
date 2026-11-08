import json,re,html,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter
p=Path(__file__).parent;root=p.parent
src=(root/'index.html').read_text();frames=json.loads(src.split('const frames=')[1].split(';window.DUR')[0]);shots=json.loads((root/'shots.json').read_text())
# Preserve the approved compositions; replace schematic busts with richer original cut-paper artwork.
scope={};exec((root/'boards.py').read_text().split('scenes=[]')[0],scope)
def portrait(x,y,col):
 beard='#74604c' if col!='#943f36' else '#51483d'
 details=''.join(f'<path d="M{u} -135q8 35 0 60" stroke="#e6dac6" opacity=".3" fill="none" stroke-width="2"/>' for u in range(-32,40,9))
 return f'''<g transform="translate({x} {y})" filter="url(#s)">
 <path d="M-135 205L-118 -18Q-90 -82 -48 -89L48 -89Q90 -82 118 -18L135 205Z" fill="{col}" stroke="#f2ebdd" stroke-width="12"/>
 <path d="M-50 -80L0 -20L50 -80L35 205H-35Z" fill="#c1ad7a" opacity=".8"/>
 <path d="M-110 -30L-70 160M110 -30L70 160M-70 30L-50 190M70 30L50 190" stroke="#1d2624" stroke-width="5" opacity=".2" fill="none"/>
 <path d="M-120 -3L-146 150L-97 172L-60 28M120 -3L146 150L97 172L60 28" fill="{col}" stroke="#e1d6c3" stroke-width="6"/>
 <ellipse cx="-123" cy="161" rx="23" ry="30" fill="#cbb38e"/><ellipse cx="123" cy="161" rx="23" ry="30" fill="#cbb38e"/>
 <path d="M-48 -100L-35 -55L0 -32L35 -55L48 -100" fill="#d1bb94"/>
 <ellipse cy="-153" rx="64" ry="82" fill="#d2bc98" stroke="#f2ebdd" stroke-width="7"/>
 <path d="M-66 -144Q-88 -249 8 -239Q81 -239 67 -143L48 -168L35 -208Q0 -180 -38 -201L-48 -161Z" fill="#494437"/>
 <path d="M-55 -140Q-25 -115 0 -129Q25 -115 55 -140L40 -77Q0 -53 -40 -77Z" fill="{beard}"/>
 {details}<path d="M-39 -158l25 -3M14 -161l25 3" stroke="#403f34" stroke-width="6" stroke-linecap="round"/>
 <circle cx="-25" cy="-150" r="3" fill="#242923"/><circle cx="25" cy="-150" r="3" fill="#242923"/>
 <path d="M0 -152l-7 23h13" fill="none" stroke="#997c59" stroke-width="3"/>
 <path d="M-20 -106Q0 -116 20 -106" fill="none" stroke="#c5ad8a" stroke-width="4"/>
 <path d="M-118 99L118 99" stroke="#443d2e" stroke-width="15"/>
 <rect x="-14" y="87" width="28" height="25" fill="#bd9350" stroke="#e2c58b" stroke-width="3"/>
 <path d="M90 108L65 230M72 136L104 143" stroke="#c2c1b6" stroke-width="9"/>
 </g>'''
clean=[]
for f in frames:
 f=re.sub(r'<foreignObject.*?</foreignObject>','',f,flags=re.S)
 f=f.replace('<rect width="1080" height="1920" filter="url(#paper)" opacity=".055"/>','')
 f=f.replace('<rect width="1080" height="1920" fill="#eae3d3"/>','')
 for x,y,col in re.findall(r'<g transform="translate\(([-\d]+) ([-\d]+)\)" filter="url\(#s\)"><path d="M-130 200.*?fill="(#[a-fA-F0-9]+)"',f):
  f=f.replace(scope['king'](x,y,col),portrait(x,y,col))
 f=f.replace('<svg viewBox="0 0 1080 1920" width="100%" height="100%">','').replace('</svg>','')
 clean.append(f)
# The complete supplied script is preserved in caption text. Boundaries remain editorial estimates.
pairs=[
[('می‌دونی چرا توی انگلیسی','Do you know why, in English,'),('یه‌جا A میاریم، یه‌جا THE؟','we sometimes use A, and sometimes THE?')],
[('برای جواب، بریم به انگلستانِ هزار سال پیش!','For the answer, let’s visit England a thousand years ago!')],
[('سال ۱۰۶۶، پادشاه انگلستان','In 1066, the king of England'),('بدون وارث از دنیا می‌ره.','dies without an heir.')],
[('حالا انگلستان به یه پادشاه احتیاج داره:','Now England needs a king:'),('England needs a king.','England needs a king.')],
[('ولی مشکل اینجاست که سه نفر','But there’s a problem: three men'),('تاج‌وتخت رو برای خودشون می‌خوان!','each want the throne!')],
[('اول هارولد تاج‌گذاری می‌کنه.','First, Harold is crowned.')],
[('اما پادشاه نروژ حمله می‌کنه!','But the king of Norway invades!')],
[('هارولد شکستش می‌ده،','Harold defeats him,'),('ولی هنوز نفس راحت نکشیده که','but before he can catch his breath,')],
[('ویلیام با یه لشکر دیگه از راه می‌رسه!','William arrives with another army!')],
[('این بار هارولد کشته می‌شه','This time, Harold is killed'),('و ویلیام می‌شه:','and William becomes:')],
[('The king of England!','The king of England!')],
[('حالا دقت کردی؟ اول گفتیم A KING؛','Notice? First we said A KING:'),('یعنی یه پادشاه، هنوز مشخص نکردیم کدوم.','a king—we haven’t specified which one.')],
[('ولی THE KING یعنی اون پادشاه مشخص!','But THE KING means that particular king!')],
[('و جالبه که ریشهٔ این تفاوت','Interestingly, the roots of this distinction'),('به انگلیسی قدیم برمی‌گرده!','go back to Old English!'),('A از کلمهٔ ĀN به معنی «یک» اومده.','A comes from ĀN, meaning “one.”')],
[('اما THE از خانوادهٔ کلمهٔ اشارهٔ that؛','THE belongs to the demonstrative family, like “that”:'),('چیزی شبیه «اون» و «همون» خودمون!','something like “that one” or “the very one.”')],
[('پس فرق اصلی چیه؟','So what’s the key difference?'),('وقتی شنونده می‌تونه بفهمه دقیقاً کدوم چیز رو می‌گی،','When your listener can identify exactly which thing you mean,'),('معمولاً THE میاریم؛','we usually use THE;')],
[('حتی اگه قبلاً اسمش رو نشنیده باشه!','even if it hasn’t been mentioned before!')],
[('برای تمرین این تفاوت،','To practise this distinction,'),('یه چالش تصویری و یه ورک‌شیت کاربردی آماده کردیم.','we’ve prepared a visual challenge and a practical worksheet.')],
[('فقط THE رو کامنت کن','Just comment THE'),('تا برات بفرستیم!','and we’ll send them to you!')]
]
cues=[]
for i,(s,ps) in enumerate(zip(shots,pairs)):
 weights=[max(3,len(a.split())) for a,b in ps];total=sum(weights);at=s['start']
 for (fa,en),w in zip(ps,weights):
  end=at+(s['end']-s['start'])*w/total
  cues.append(dict(t0=round(at,4),t1=round(end,4),text=fa,en=en,scene=i,timing='estimated_unverified'))
  at=end
(p/'captions.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2))
(p/'scenes.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2))
rng=np.random.default_rng(1066);a=rng.normal(0,2.7,(960,540));rgb=np.stack([234+a,227+a,211+a],axis=2).clip(0,255).astype('uint8');Image.fromarray(rgb).save(p/'paper.jpg',quality=94)
# Offline font copies; Noto Arabic and DejaVu are already installed and redistributable.
import shutil
shutil.copy('/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf',p/'Arabic.ttf')
shutil.copy('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',p/'Latin.ttf')
data='const ART='+json.dumps(clean)+';const SHOTS='+json.dumps(shots)+';const CUES='+json.dumps(cues,ensure_ascii=False)+';'
(p/'data.js').write_text(data)
print(len(clean),'scenes;',len(cues),'bilingual caption cues (provisional)')
