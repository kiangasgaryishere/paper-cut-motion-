"""Master the ENTIRE narration once, before slicing any ten-second part."""
from pathlib import Path
import json,re,subprocess
p=Path(__file__).resolve().parent;out=p/'out';out.mkdir(exist_ok=True)
voice=p/'assets/narration.mp3';processed=out/'voice-presence.wav'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(voice),'-af','highpass=f=75,equalizer=f=2500:t=q:w=0.8:g=1.0,acompressor=threshold=0.18:ratio=1.5:attack=12:release=140:makeup=1.08','-ar','48000','-ac','1','-c:a','pcm_f32le',str(processed)],check=True)
base='loudnorm=I=-13:TP=-2.5:LRA=11'
r=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(processed),'-af',base+':print_format=json','-f','null','-'],capture_output=True,text=True,check=True);m=json.loads(re.findall(r'\{[^{}]+\}',r.stderr)[-1])
ln=base+f":measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
# Compensated limiter look-ahead retains the original time origin.
filters=ln+',aresample=192000,alimiter=limit=0.7499:attack=10:release=200:level=disabled:latency=1,aresample=48000'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(processed),'-af',filters,'-ar','48000','-ac','1','-c:a','pcm_s24le',str(out/'voice-master-v2.wav')],check=True)
(p/'alignment/voice-master-v2.json').write_text(json.dumps(dict(source='assets/narration.mp3',scope='whole recording, not each part',target_LUFS=-13,peak_ceiling_dBTP=-2.5,first_pass=m,retiming=False,sample_rate=48000,lookahead_latency_compensated=True),indent=2));print('Full narration mastered; no retiming or per-part fades.')
