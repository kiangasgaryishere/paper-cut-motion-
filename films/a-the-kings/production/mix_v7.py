from pathlib import Path
import sys,json,numpy as np,soundfile as sf
from scipy.ndimage import uniform_filter1d,minimum_filter1d
sys.path.insert(0,'core/audio');import sfx
p=Path('films/a-the-kings/production');meta=json.loads((p/'meta-v4.json').read_text());shots=json.loads((p/'scenes.json').read_text());v,sr=sf.read(p/'voice-v7.wav');assert sr==48000
N=round(meta['trim_end']*sr);v=np.pad(v,(0,max(0,N-len(v))))[:N];v*=.84/max(.01,np.abs(v).max());fx=np.zeros((N,2),np.float32);events=[]
def emit(name,x,at,gain=1,pan=0,kind='sync',cut=None):
 x=np.asarray(x,dtype=np.float32);assert np.isfinite(x).all();sfx.add(fx,x,at,gain,pan);events.append(dict(type=name,start=round(at,6),end=round(min(N/sr,at+len(x)/sr),6),gain=gain,pan=pan,edit=kind,cut=cut))
def paper(d=.6):
 tt=sfx.t_(d);x=sfx.bp(sfx.noise(d),700,6700)*(np.sin(np.pi*tt/d)**2)*(.3+.7*np.sin(tt*91)**4);return sfx.norm(x)*.13
def sail(d=.85):
 tt=sfx.t_(d);return sfx.norm(sfx.bp(sfx.noise(d),180,2400)*(np.sin(np.pi*tt/d)**1.5))*.10
def march(d=2.8):
 x=np.zeros(round(d*sr))
 for k,at in enumerate(np.arange(.05,d-.16,.24)):
  y=sfx.thump(.18,85+(k%3)*14)[:round(.09*sr)]+sfx.clack(.6+(k%3)*.1,.12)[:round(.09*sr)];j=round(at*sr);x[j:j+len(y)]+=y
 tt=sfx.t_(d);air=sfx.norm(sfx.bp(sfx.noise(d),120,900))*.025*np.sin(np.pi*tt/d)**2
 return sfx.norm(x)*.11+air
def charge(d=.75):
 tt=sfx.t_(d);phase=2*np.pi*np.cumsum(110+45*np.sin(np.pi*tt/d))/sr;glot=np.tanh(2*np.sin(phase));breath=sfx.bp(sfx.noise(d),500,3200);return sfx.norm((sfx.bp(glot,300,1800)+breath*.4)*np.sin(np.pi*tt/d)**1.7)*.085
def metal(d=.8):
 tt=sfx.t_(d);x=sum(a*np.sin(2*np.pi*f*tt)*np.exp(-tt/tau) for a,f,tau in [(1,1350,.15),(.55,2167,.3),(.25,3310,.4)]);return sfx.norm(x)*.10

def breath_fall(d=.43):
 tt=sfx.t_(d);phase=2*np.pi*np.cumsum(130-70*tt/d)/sr;voice=sfx.bp(np.tanh(2.5*np.sin(phase)),220,1600);air=sfx.bp(sfx.noise(d),400,2600);return sfx.norm((voice*.6+air*.45)*np.sin(np.pi*tt/d)**1.7)*.09

def game_over():
 d=.62;z=np.zeros(round(d*sr));
 for at,f,dur in [(0,440,.13),(.16,330,.13),(.32,220,.24)]:
  tt=sfx.t_(dur);env=np.minimum(tt/.005,1)*np.minimum((dur-tt)/.025,1);w=np.sign(np.sin(2*np.pi*f*tt))*.8+np.sin(2*np.pi*f*.5*tt)*.2;j=round(at*sr);z[j:j+len(w)]+=w*env
 return sfx.lp(z,2100)*.09

def type_key(pitch):
 x=sfx.click(pitch,.065);x[:min(len(x),400)]+=sfx.hp(sfx.noise(min(len(x),400)/sr),3500)*.006;return x

def pencil(d=.45):
 tt=sfx.t_(d)
 grain=sfx.bp(sfx.noise(d),1100,6800)
 pressure=(.38+.62*np.sin(tt*57+.6*np.sin(tt*19))**2)
 envelope=np.minimum(tt/.018,1)*np.minimum((d-tt)/.035,1)
 return sfx.norm(grain*pressure*envelope)*.22

# Selective accents, rather than one repeated whoosh on every edit.
for at,pitch in [(meta['hook_a_at'],1),(meta['hook_the_at'],.85)]:emit('paper_card_accent',sfx.click(pitch,.05),at)
cut=shots[1]['start'];emit('paper_unfold_pre_lap',paper(.78),cut-.30,kind='J',cut=cut)
emit('empty_throne_wood',sfx.clack(.6,.055),shots[2]['start']+.32)
emit('claimants_three_cards',paper(.38),shots[4]['start']+.15,gain=.6)
emit('coronation_metal',metal(.65),shots[5]['start']+.38)
cut=shots[6]['start'];emit('norway_sail_before_picture',sail(.95),cut-.36,pan=.35,kind='J',cut=cut)
emit('norway_attack_rush',march(2.75),cut-.12,pan=.25)
emit('short_attack_cry',charge(),cut+.24,gain=.8,pan=.15)
# Battle sound survives the picture cut to Harold's victory.
cut=shots[7]['start'];emit('battle_tail_to_victory',metal(.9),cut-.18,pan=-.2,kind='L',cut=cut)
emit('shield_falls',sfx.clack(.65,.075),cut+1.05,pan=.25)
cut=shots[8]['start'];emit('william_army_pre_lap',march(1.6),cut-.38,pan=-.3,kind='J',cut=cut)
emit('william_sail',sail(.6),cut+.12,pan=-.2)
# Near-silence around the death turn, followed by three short, distinct actions.
cut=shots[9]['start'];emit('harold_short_fall_breath',breath_fall(),cut+.55)
emit('harold_ground_impact',sfx.thump(.13,75),cut+.97)
emit('single_game_over_effect',game_over(),cut+1.12)
emit('new_king_crown',metal(.62),shots[10]['start']+.38)
# Grammar section gets room to breathe. One book sound crosses into the next graphic.
cut=shots[14]['start'];emit('old_book_page_tail',paper(.76),cut-.24,gain=.65,kind='L',cut=cut)
emit('worksheet_pencil',pencil(.45),73.195708,gain=.8)
cut=shots[18]['start'];emit('comment_interface_pre_lap',paper(.42),cut-.25,gain=.25,kind='J',cut=cut)
for k,at in enumerate([meta['comment_keyword_at']+i*.13 for i in range(3)]):emit('cta_key_'+str(k+1),type_key(1.15-k*.08),at)
emit('comment_send',sfx.pop(.035)[:round(.12*sr)],shots[18]['start']+1.4)
# Audible pencil/marker strokes match the new explanatory paths, not scene cuts.
for name,at,d in [('a_comparison_underline',41.739875,.45),('the_comparison_underline',46.3745,.45),('an_to_a_pencil_arrow',meta['a_root_at'],.45),('the_family_pencil_branch',57.535042,.55),('identified_crown_marker',65.345333,.45),('shared_window_marker',70.227833,.45)]:
 emit(name,pencil(d),at,gain=.85)
# Smooth speech-aware ducking keeps nonverbal effects beneath the narrator.
env=uniform_filter1d(np.abs(v),size=2400);duck=uniform_filter1d(np.where(env>.025,.30,.75),size=1600);fx*=duck[:,None]
# Limit effects over overlapping speech windows; expand gain reduction before
# smoothing so a loud effect in a pause cannot mask the next syllable.
priority=np.ones(N,dtype=np.float32)
for j in range(0,N-4800,2400):
 vr=np.sqrt(np.mean(v[j:j+4800]**2));fr=np.sqrt(np.mean(fx[j:j+4800]**2))
 if vr>.025 and fr>0:
  priority[j:j+4800]=np.minimum(priority[j:j+4800],min(1,.19*vr/fr))
priority=uniform_filter1d(minimum_filter1d(priority,size=1601),size=1600)
fx*=priority[:,None]
out=np.repeat(v[:,None],2,axis=1)+fx
if np.abs(out).max()>.96:out*=.96/np.abs(out).max()
assert np.isfinite(out).all();sf.write(p/'sfx-v7.wav',fx,sr,subtype='PCM_24');sf.write(p/'mix-v7.wav',out,sr,subtype='PCM_24');(p/'sound-events-v7.json').write_text(json.dumps(events,indent=2))
for e in events:
 if e['edit']=='J':assert e['start']<e['cut']<e['end']
 if e['edit']=='L':assert e['start']<e['cut']<e['end']
print(len(events),'sound events;',sum(e['edit']=='J' for e in events),'J cuts;',sum(e['edit']=='L' for e in events),'L cuts;',len(out)/sr,'seconds; no music.')
