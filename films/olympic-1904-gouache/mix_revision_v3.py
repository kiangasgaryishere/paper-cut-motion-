"""Remove only the repeated sentence; keep source voice samples at their natural speed."""
from pathlib import Path
import json,hashlib,numpy as np,soundfile as sf
from scipy.signal import butter,sosfilt
from scipy.ndimage import uniform_filter1d,minimum_filter1d
p=Path(__file__).resolve().parent;sr=48000;a=2749*1600;b=2819*1600;N=3710*1600
master=p/'out/voice-master-v2.wav';expected=json.loads((p/'QC-part01-v2.json').read_text())['canonical_voice_master_sha256'];assert hashlib.sha256(master.read_bytes()).hexdigest()==expected
raw,fs=sf.read(master);assert fs==sr;full=np.pad(raw,(0,126*sr-len(raw)))
voice=np.concatenate([full[:a],full[b:]]);original,fs=sf.read(p/'out/revision-v2-sfx.wav');assert fs==sr
fx=np.concatenate([original[:a],original[b:]]);assert len(fx)==len(voice)==N
# Both cuts sit in detected quiet gaps, not in the spoken English or next sentence.
quiet=[float(np.sqrt(np.mean(full[j-240:j+240]**2))) for j in [a,b]];assert max(quiet)<.001
# Fade only ambience/Foley near the splice; retained narration samples are untouched.
f=480;fx[a-f:a]*=np.linspace(1,0,f)[:,None];fx[a:a+f]*=np.linspace(0,1,f)[:,None]
rng=np.random.default_rng(1904003);extra=np.zeros_like(fx);events=[]
for i,at in enumerate([91.30,91.52,91.74,91.96]):
 t=np.arange(8640)/sr;z=sosfilt(butter(2,[500,5200],btype='band',fs=sr,output='sos'),rng.normal(size=len(t)))*np.exp(-t*28)
 z=z/max(abs(z))*.026*(1-i*.18);j=round(at*sr);pan=(-1)**i*.35;extra[j:j+len(z),0]+=z*np.sqrt((1-pan)/2);extra[j:j+len(z),1]+=z*np.sqrt((1+pan)/2);events.append(dict(type='finish_applause_L_cut',edited_start=at,edited_end=at+.18))
env=uniform_filter1d(abs(voice),size=2400);extra*=uniform_filter1d(np.where(env>.025,.28,.65),size=1600)[:,None];fx+=extra
priority=np.ones(N)
for j in range(0,N-4800,2400):
 vr=np.sqrt(np.mean(voice[j:j+4800]**2));fr=np.sqrt(np.mean(fx[j:j+4800]**2))
 if vr>.025 and fr>0:priority[j:j+4800]=np.minimum(priority[j:j+4800],min(1,.15*vr/fr))
fx*=uniform_filter1d(minimum_filter1d(priority,size=1601),size=1600)[:,None]
mix=voice[:,None]+fx;assert np.isfinite(mix).all() and abs(mix).max()<.9
for name,data in [('voice',voice),('sfx',fx),('mix',mix)]:sf.write(p/f'out/revision-v3-{name}.wav',data,sr,subtype='PCM_24')
report=dict(source_master_sha256=expected,removed_sentence='و بالاخره قهرمان شد! (the repeated sentence after They kept him going)',removed_source_start=a/sr,removed_source_end=b/sr,removed_source_samples=b-a,removed_video_frames=70,removed_duration=(b-a)/sr,duration=N/sr,output_samples=N,splice_quiet_RMS=quiet,narration_speed_changed=False,retained_voice_samples_unchanged=True,ambience_splice_fade_ms=10,added_sound_events=events,music='none',source_map=[dict(output_start=0,output_end=a/sr,source_start=0,source_end=a/sr),dict(output_start=a/sr,output_end=N/sr,source_start=b/sr,source_end=126)])
(p/'audio-edit-v3.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
