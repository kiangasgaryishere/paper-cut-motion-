"""Verify the final encoded deliverable and its source timing."""
from pathlib import Path
import json, hashlib, subprocess
import numpy as np
from scipy.signal import correlate, butter, sosfilt
import soundfile as sf
p = Path(__file__).resolve().parents[1]
root = p.parents[1]
file = root/'video/carpet-comic-history-v1.mp4'
def run(*args):
    return subprocess.run(args, check=True, text=True, capture_output=True)
probe = json.loads(run('ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(file)).stdout)
v,a = probe['streams']
assert (v['width'],v['height'],v['codec_name'],v['pix_fmt'],v['avg_frame_rate'],v['nb_read_frames']) == (1080,1920,'h264','yuv420p','24/1','2232')
assert (a['codec_name'],a['channels'],a['sample_rate']) == ('aac',2,'48000')
assert abs(float(probe['format']['duration'])-93) < .01
assert (v['color_range'], v['color_space'], v['color_transfer'], v['color_primaries']) == ('tv','bt709','bt709','bt709')
log = run('ffmpeg','-hide_banner','-nostats','-xerror','-i',str(file),'-vf','blackdetect=d=0.08:pix_th=0.05','-af','loudnorm=I=-14:TP=-1:LRA=7:print_format=json','-f','null','-').stderr
assert 'black_start:' not in log
numbers = json.loads(log[log.rfind('{'):log.rfind('}')+1])
assert -15.5 <= float(numbers['input_i']) <= -12.5 and float(numbers['input_tp']) <= -1
run('ffmpeg','-v','error','-y','-i',str(file),'-vn','-ac','1','-c:a','pcm_f32le',str(p/'out/decoded.wav'))
encoded,_ = sf.read(p/'out/decoded.wav')
master,_ = sf.read(p/'out/mix.wav')
master = master.mean(axis=1)
run('ffmpeg','-v','error','-y','-i',str(p/'assets/narration.mp3'),'-af','highpass=f=65','-ar','48000','-c:a','pcm_f32le',str(p/'out/reference.wav'))
src,_ = sf.read(p/'out/reference.wav')
voice,_ = sf.read(p/'out/voice.wav')
assert len(voice) == len(src) == 4419555
anchors = []
for t in (1,9,18,28,36,43,52,62,72,83,89):
    i=t*48000
    def lag(track, ref):
        expected = ref[i:i+32000]
        region = track[i-256:i+32256]
        offset = np.argmax(correlate(region,expected,mode='valid',method='fft'))-256
        return int(offset), float(np.corrcoef(expected, track[i+offset:i+offset+len(expected)])[0,1])
    eo,ec = lag(encoded,master)
    so,sc = lag(voice,src)
    assert abs(eo)<=1 and ec>.97 and abs(so)<=4 and sc>.90,(t,eo,ec,so,sc)
    anchors.append(dict(seconds=t,aac_offset_samples=eo,voice_offset_samples=so))
plan=json.loads((p/'timeline.json').read_text())
assert all(x['end']<=y['start'] for x,y in zip(plan['captions'],plan['captions'][1:]))
data=file.read_bytes()
assert data.find(b'moov')<data.find(b'mdat')
report = dict(duration=93,frames=2232,width=1080,height=1920,fps=24,full_decode=True,black_intervals=[],source_samples=4419555,alignment=anchors,music=False,loudness_lufs=float(numbers['input_i']),true_peak_dbtp=float(numbers['input_tp']),caption_preflight=json.loads((p/'out/preflight.json').read_text()),bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
(p/'QC.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print({k:report[k] for k in ['duration','frames','loudness_lufs','true_peak_dbtp','bytes','sha256']})
