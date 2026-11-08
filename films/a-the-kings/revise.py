import json, re
from pathlib import Path
p=Path('films/a-the-kings')
scope={};exec((p/'boards.py').read_text().split('scenes=[]')[0],scope)
crownat,king=scope['crownat'],scope['king']
old=json.loads((p/'shots-v1.json').read_text());shots=[]
for s in old:
 if s['n']==12:
  a=dict(s,end=42,narration='اول گفتیم A KING؛ یعنی یه پادشاه، هنوز مشخص نکردیم کدوم.',visual='سه سیلوئت نامشخص؛ دایره انتخاب میان آنها می‌گردد.',action='کادر روی گزینه‌ها باز می‌شود؛ انتخاب نهایی انجام نمی‌شود.')
  b=dict(s,start=42,narration='ولی THE KING یعنی اون پادشاه مشخص!',visual='دو گزینه کنار می‌روند و ویلیامِ تاج‌دار واضح می‌ماند.',action='دایره انتخاب دور ویلیام ثابت می‌شود.')
  shots.extend([a,b])
 else:shots.append(s)
for i,s in enumerate(shots):
 s.update(n=i+1,voice_caption_onset_provisional=s['start'],visual_reveal_provisional=round(s['start']+.5,3),timing_status='provisional_not_speech_aligned',caption=s['narration'].replace('…',' '))
 s['caption_end_provisional']=s['end']
 s['on_screen_text']='subtitle_only'
 s['events_provisional']=[{'at':s['visual_reveal_provisional'],'action':s['action']}]
 if s['end']-s['start']>5:s['events_provisional'].append({'at':s['start']+3.5,'action':'همگرایی نگاه‌ها و روشن‌شدن تاج؛ تغییر معنادار در همان صحنه'})
# Remove the old plan's text instructions from the current visual specification.
replacements={1:'دو کارت تصویری بدون نوشته؛ تاج میان دو امکان حرکت می‌کند.',2:'برگه آرشیوی بدون نوشته به تالار تخت باز می‌شود.',4:'نقشه و جایگاه خالی شاه؛ یک سیلوئت ناشناس ظاهر می‌شود.',8:'نشان مهاجم از نقشه کنار می‌رود و نشان هارولد به جنوب حرکت می‌کند؛ مهر تصویری بدون نوشته.',11:'تاج بر سر ویلیام؛ رقبا از عمق صحنه کنار می‌روند.',14:'یک مهره از میان چند مهره جدا می‌شود؛ ریشه واژه فقط در زیرنویس.',15:'دست کاغذی به تاج مشخص اشاره می‌کند؛ توضیح واژه فقط در زیرنویس.',16:'دو شخصیت به یک تاج نگاه می‌کنند؛ خطوط نگاه در یک نقطه همگرا می‌شوند.',17:'اتاقی با تنها یک پنجره؛ نور توجه را به پنجره می‌برد، بدون برچسب.',18:'برگه تمرین تصویری بدون تیتر و نوشته؛ جای پاسخ‌ها و اشکال مشخص‌اند.',19:'حباب کامنت بی‌نوشته و تاج کوچک؛ THE فقط در زیرنویس.'}
for n,v in replacements.items():shots[n-1]['visual']=v
(p/'shots.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2))
base='''<defs><filter id="s" x="-50%" y="-50%" width="200%" height="200%"><feDropShadow dx="8" dy="14" stdDeviation="9" flood-color="#342c20" flood-opacity=".23"/></filter><filter id="paper"><feTurbulence type="fractalNoise" baseFrequency=".45" numOctaves="3" seed="4"/><feColorMatrix type="saturate" values="0"/></filter></defs><rect width="1080" height="1920" fill="#eae3d3"/><rect width="1080" height="1920" filter="url(#paper)" opacity=".055"/>'''
mapshape='<path d="M480 490L640 540L590 690L700 820L630 990L730 1140L580 1240L340 1200L430 1020L390 860L480 700Z" fill="#969985" stroke="#f6f0e4" stroke-width="20" filter="url(#s)"/>'
throne='<g filter="url(#s)"><path d="M310 1120V650Q540 420 770 650V1120Z" fill="#82715a"/><path d="M360 1060V690Q540 500 720 690V1060Z" fill="#4e5146"/><rect x="300" y="1030" width="480" height="75" fill="#ae9874"/></g>'
def paper(x,y,w=230,h=300,rot=0):return f'<g transform="translate({x} {y}) rotate({rot})" filter="url(#s)"><rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" fill="#f6f0e4"/></g>'
def ship(x,y):return f'<g transform="translate({x} {y})" filter="url(#s)"><path d="M-140 0H140L85 65H-85Z" fill="#685842"/><path d="M0 -230V0M10 -220V-25H150Z" fill="#e9ddc2" stroke="#685842" stroke-width="8"/></g>'
def ring(x,y,r=100):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#bf873d" stroke-width="10"/>'
body=[
 paper(290,760)+paper(790,760)+crownat(540,1030,1.4),
 paper(540,840,640,830,-8)+mapshape,
 throne+crownat(540,1030,.8),
 mapshape+king(540,1000,'#a7a18e'),
 crownat(540,490)+king(240,950,'#5b6652')+king(540,1120,'#68767d')+king(840,950,'#943f36'),
 king(540,980,'#5b6652')+crownat(540,760,.65),
 mapshape+ship(760,580)+'<path d="M760 650Q650 650 550 790" fill="none" stroke="#68767d" stroke-width="12" stroke-dasharray="16 12"/>',
 mapshape+'<path d="M540 740Q440 940 610 1150" fill="none" stroke="#5b6652" stroke-width="12" stroke-dasharray="16 12"/>'+ring(540,740,65),
 ship(320,750)+king(740,1050,'#943f36'),
 '<g opacity=".4" transform="rotate(-12 400 1000)">'+king(400,1000,'#5b6652')+'</g>'+crownat(720,1100,.8),
 king(540,980,'#943f36')+crownat(540,760,.65),
 king(260,1050,'#a7a18e')+king(540,1050,'#a7a18e')+king(820,1050,'#a7a18e')+ring(540,910,130),
 '<g opacity=".15">'+king(240,1050,'#a7a18e')+king(840,1050,'#a7a18e')+'</g>'+king(540,1000,'#943f36')+crownat(540,780,.65)+ring(540,900,175),
 paper(540,870,620,600)+'<g fill="#a7a18e"><circle cx="360" cy="1050" r="32"/><circle cx="470" cy="1050" r="32"/><circle cx="580" cy="1050" r="32"/></g><circle cx="700" cy="800" r="58" fill="#bf873d"/>',
 crownat(720,830)+ '<path d="M250 1060L370 990L480 850Q515 820 520 850L470 950L600 930L670 990L630 1100L440 1190L300 1190Z" fill="#c9b99b" stroke="#f6f0e4" stroke-width="12" filter="url(#s)"/>',
 king(220,1070,'#5b6652')+king(860,1070,'#68767d')+crownat(540,780,.8)+'<path d="M260 890L475 740M820 890L605 740" fill="none" stroke="#bf873d" stroke-width="5" stroke-dasharray="10 12"/>',
 '<path d="M180 1230V460H900V1230Z" fill="#d8cfba"/><rect x="470" y="640" width="280" height="380" fill="#b7c5be" stroke="#f6f0e4" stroke-width="24"/><path d="M610 640V1020M470 830H750" stroke="#f6f0e4" stroke-width="18"/><path d="M470 1020L750 1020L900 1230H300Z" fill="#f6f0e4" opacity=".6"/>',
 paper(540,880,670,900,-5)+ring(400,700,65)+ring(680,700,65)+'<rect x="320" y="940" width="430" height="120" fill="none" stroke="#a59b84" stroke-width="5"/>',
 crownat(540,650,.8)+'<path d="M210 830H870V1100H420L300 1190V1100H210Z" fill="#f6f0e4" filter="url(#s)"/><circle cx="450" cy="970" r="17" fill="#bf873d"/><circle cx="540" cy="970" r="17" fill="#bf873d"/><circle cx="630" cy="970" r="17" fill="#bf873d"/>'
]
# Captions here are short editorial placeholders, not a timed transcript.
caps=['چرا یه‌جا A و یه‌جا THE؟','بریم به انگلستانِ هزار سال پیش','سال ۱۰۶۶، پادشاه بدون وارث از دنیا می‌ره','England needs a king.','سه نفر تاج‌وتخت رو می‌خوان!','اول هارولد تاج‌گذاری می‌کنه','اما پادشاه نروژ حمله می‌کنه!','هارولد شکستش می‌ده، ولی هنوز…','ویلیام با یه لشکر دیگه از راه می‌رسه!','این بار هارولد کشته می‌شه','The king of England!','A KING؛ هنوز مشخص نکردیم کدوم','THE KING؛ اون پادشاه مشخص','A از ĀN به معنی «یک» اومده','THE از خانوادهٔ کلمه‌های اشاره است','شنونده می‌فهمه دقیقاً کدوم رو می‌گی','حتی اگه قبلاً اسمش رو نشنیده باشه','یه چالش تصویری و ورک‌شیت آماده کردیم','فقط THE رو کامنت کن']
frames=[]
for i,(b,cap) in enumerate(zip(body,caps)):
 cap=re.sub(r'[A-Za-zĀā]+(?:[ .]+[A-Za-zĀā]+)*',lambda m: '<bdi dir="ltr">'+m.group(0)+'</bdi>',cap)
 subtitle=f'<foreignObject x="110" y="1440" width="790" height="260"><div xmlns="http://www.w3.org/1999/xhtml" dir="rtl" style="font:48px Noto Sans Arabic, sans-serif;color:#f6f0e4;background:#242923;padding:22px 30px;border-radius:12px;text-align:center;line-height:1.8">{cap}</div></foreignObject>'
 frames.append('<svg viewBox="0 0 1080 1920" width="100%" height="100%">'+base+b+subtitle+'</svg>')
(p/'index.html').write_text('<!doctype html><meta charset="utf-8"><style>html,body{margin:0;width:100%;height:100%;overflow:hidden}#frame{height:100%;width:100%}</style><div id="frame"></div><script>const frames='+json.dumps(frames,ensure_ascii=False)+';window.DUR=19;window.render=t=>document.getElementById("frame").innerHTML=frames[Math.min(18,Math.floor(t))];window.render(0);document.fonts.ready.then(()=>window.READY=true);</script>')
