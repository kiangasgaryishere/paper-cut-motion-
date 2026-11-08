import json,re
from pathlib import Path
p=Path(__file__).parent
raw=(p/'data.js').read_text();art=json.loads(raw.split('const ART=')[1].split(';const SHOTS=')[0]);shots=json.loads((p/'scenes.json').read_text());cues=json.loads((p/'captions.json').read_text())
# Keep a recoverable source for repeated generation.
if not (p/'art-v1.json').exists():(p/'art-v1.json').write_text(json.dumps(art))
else:art=json.loads((p/'art-v1.json').read_text())
def label(x,y,t,size=90):return f'<text x="{x}" y="{y}" text-anchor="middle" fill="#242923" font-family="Latin" font-weight="700" font-size="{size}">{t}</text>'
def crown(x,y,s=.7):return f'<g transform="translate({x} {y}) scale({s})" filter="url(#s)"><path d="M-100 0L-125 -95L-52 -53L0 -125L52 -53L125 -95L100 0Z" fill="#bf873d" stroke="#5b4c32" stroke-width="5"/><rect x="-100" width="200" height="25" rx="7" fill="#c69954"/></g>'
art[0]+=label(290,790,'A',120)+label(790,790,'THE',98)
# An explanatory flag badge belongs to the layout, not to the historical army.
flag='<g data-context-flag="true" transform="translate(820 425) rotate(5)" filter="url(#s)"><rect width="150" height="100" fill="#faf6ec"/><path d="M75 0V100M0 50H150" stroke="#a23e35" stroke-width="22"/></g>'
for i in [1,2,3,4,5,6,7,8,10]:art[i]+=flag
# Three final compositions: contextual identification, a tangible exercise, a usable comment UI.
art[16]='''<defs><filter id="s" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="7" dy="12" stdDeviation="8" flood-opacity=".2"/></filter></defs>
<g filter="url(#s)"><path d="M180 1230V460H900V1230Z" fill="#d3c8b2"/><path d="M180 1230L300 1110H790L900 1230Z" fill="#b6a88e"/><rect x="420" y="590" width="340" height="430" fill="#a9bbb7" stroke="#f8f2e5" stroke-width="24"/><path d="M590 590V1020M420 805H760" stroke="#f8f2e5" stroke-width="18"/><path d="M420 1020H760L890 1225H270Z" fill="#f5e1a6" opacity=".45"/><path d="M120 1230H930V1285H120Z" fill="#927f60"/><path d="M200 1285V1400M850 1285V1400" stroke="#685b46" stroke-width="30"/></g>
<g filter="url(#s)" transform="rotate(-8 300 1130)"><rect x="200" y="1060" width="190" height="130" fill="#f5ecda"/><path d="M240 1090H350M240 1120H330M240 1150H340" stroke="#a59b84" stroke-width="5"/></g>
<g class="window-focus"><rect x="402" y="572" width="376" height="466" rx="8" fill="none" stroke="#bf873d" stroke-width="8"/></g>'''
art[17]='''<defs><filter id="s" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="7" dy="12" stdDeviation="8" flood-opacity=".2"/></filter></defs>
<g transform="rotate(5 540 920)" filter="url(#s)"><rect x="235" y="480" width="650" height="870" fill="#d7c4a2"/></g>
<g transform="rotate(-3 540 910)" filter="url(#s)"><rect x="200" y="450" width="650" height="870" fill="#faf5e9"/><path d="M240 510H810" stroke="#bf873d" stroke-width="10"/>
<circle cx="355" cy="740" r="100" fill="#e4ddcd"/><path d="M305 770L292 695L330 725L355 680L380 725L418 695L405 770Z" fill="#bf873d"/>
<rect x="575" y="640" width="170" height="200" fill="#a9bbb7" stroke="#d5cbb7" stroke-width="14"/><path d="M660 640V840M575 740H745" stroke="#f8f2e5" stroke-width="12"/>
<rect x="270" y="930" width="210" height="100" rx="8" fill="#e8dfcc"/><rect x="550" y="930" width="210" height="100" rx="8" fill="#e8dfcc"/>
<path d="M270 1150H770M270 1200H620" stroke="#d2c7b2" stroke-width="10"/></g>'''+label(375,1000,'A',65)+label(655,1000,'THE',65)+'''<g class="pen" transform="translate(795 1120) rotate(-32)" filter="url(#s)"><path d="M0 0V-390H24V0L12 38Z" fill="#943f36"/><path d="M0 0L12 38L24 0" fill="#c6ae86"/><path d="M8 25L12 38L16 25" fill="#242923"/></g>'''
art[18]='''<defs><filter id="s" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="7" dy="12" stdDeviation="8" flood-opacity=".2"/></filter></defs>
<g filter="url(#s)"><rect x="210" y="480" width="660" height="850" rx="40" fill="#f8f2e5"/><rect x="210" y="480" width="660" height="125" rx="40" fill="#d7c8ab"/><circle cx="265" cy="540" r="14" fill="#943f36"/><circle cx="310" cy="540" r="14" fill="#bf873d"/><circle cx="355" cy="540" r="14" fill="#82927b"/></g>
<g class="comment-bubble" filter="url(#s)"><path d="M280 760H800V1070H425L340 1140V1070H280Z" fill="#e9dfca"/></g>
<g class="comment-keyword">'''+label(540,965,'THE',138)+'''</g>
<g class="send-button"><circle cx="740" cy="1220" r="58" fill="#943f36"/><path d="M710 1200L770 1220L710 1240L725 1220Z" fill="#f8f2e5"/></g>
<g class="sent-check"><circle cx="740" cy="1220" r="58" fill="#5b6652"/><path d="M714 1220L734 1240L769 1199" fill="none" stroke="#f8f2e5" stroke-width="10" stroke-linecap="round"/></g>'''+crown(540,700,.55)
# Semantic header timing follows the revised scenes in data.js.
titles={0:'A یا THE؟',1:'انگلستان، هزار سال پیش',2:'تاج‌وتخت بدون وارث',4:'سه مدعی، یک تاج',5:'هارولد تاج‌گذاری می‌کند',6:'حمله از شمال',8:'ویلیام از راه می‌رسد',10:'پادشاه مشخص انگلستان',11:'یک پادشاه؛ هنوز نامشخص',12:'همان پادشاهِ مشخص',13:'ریشهٔ A: «یک»',14:'THE و اشاره',15:'شنونده می‌داند کدام',16:'حتی در اولین اشاره',17:'حالا نوبت تمرین توست',18:'THE رو کامنت کن'}
(p/'titles.json').write_text(json.dumps(titles,ensure_ascii=False,indent=2))
# Speech alignment replaces these timings later; this generator only owns artwork.
(p/'art-v2.json').write_text(json.dumps(art))
(p/'data.js').write_text('const ART='+json.dumps(art)+';const SHOTS='+json.dumps(shots)+';const CUES='+json.dumps(cues,ensure_ascii=False)+';const TITLES='+json.dumps(titles,ensure_ascii=False)+';')
