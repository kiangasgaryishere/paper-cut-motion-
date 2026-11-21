from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parents[1];r=json.loads((P/'out/events.json').read_text());a=json.loads((P/'analysis/audio.json').read_text())
(P/'timeline.json').write_text(json.dumps({'duration_seconds':71,'duration_frames':1704,'fps':24,'sample_rate':48000,'voice_source_samples':3350361,'voice_duration':a['duration'],'voice_edits':[],'tail_samples':57639,'caption_lead_seconds':.03,'captions':r['captions'],'shots':r['shots'],'meaningful_milestones':r['milestones'],'sound_events':r['events'],'drawing_source':'film.js'},ensure_ascii=False,indent=2)+'\n')
(P/'ANALYSIS.fa.md').write_text('''# بررسی اسکریپت و نریشن

- فایل اصلی69.7991875ثانیه و3,350,361نمونهٔ48kHz پس از دیکد دارد. خروجی71ثانیه است؛ فقط1.2008125ثانیه به انتها اضافه می‌شود.
- تمام متن و فایل MP3 کاربر نگه داشته شده‌اند؛ هیچ جمله‌ای حذف یا دوباره ساخته و سرعت هیچ بخشی عوض نشده است.
- ASR فارسی در دو پنجرهٔ شامل انگلیسی به تکرار بی‌معنا افتاد. متن آن پنجره‌ها مبنا قرار نگرفت؛ بازشناسی مستقل انگلیسی عبارت‌های فضایی‌ها، توییتر/ایکس، جام جهانی، مسیر رونالدو، پاپ، نامزدی جایزه و Rest in peace, legend را تأیید کرد. املای messy در خروجی خودکار، نام Messi در اسکریپت را تغییر نمی‌دهد.
- زمان‌بندی عبارت‌ها از مکث‌های واقعی و پنجره‌های بازشناسی با تکیه بر اسکریپت گرفته شده است. این روش زمان‌بندی واژه‌به‌واژهٔ اجباری یا ادعای شنیدن انسانی نیست.
- زیرنویس پایین فقط فارسی است؛ عبارت‌های انگلیسی محتوای میم روی حاشیهٔ عکس‌ها باقی می‌مانند. زیرنویس حدود30میلی‌ثانیه زودتر هدف‌گذاری شده، با تفکیک زمانی41.667میلی‌ثانیه در24fps؛ پایان هر زیرنویس پیش از شروع بعدی محدود شده است.
- پایان اسکریپت وابسته به عرضهٔ واقعی بازی است. کاربر تأیید کرد این ویدیو برای بعد از عرضهٔ تأییدشده ساخته شود. سایت رسمی در این محیط قابل دسترسی نبود؛ وضعیت عرضهٔ امروز مستقلاً تأیید نشده و تاریخی به ویدیو اضافه نشده است.
- ادعای نامزدی در اسکریپت به صورت یک میم عمومی نشان داده می‌شود؛ نام جایزه، سال یا پوستر رسمیِ تأییدنشده ساخته نشده است.
''')
(P/'CREDITS.md').write_text('''# Sources and rights

- Supplied script.md and ElevenLabs narration: original user material; script and assets/narration.mp3 retained byte-identical. No new voice service, clone, external transcription upload or paid TTS used.
- Primary style: Lemo Opuscar by Lemomo / LemoLab, Family Album Polaroids, Opuscar98 #56, https://lemomo-ai.github.io/lemo-opuscar/opuscar98/#no-56 . Official prompt checked against styleboard/opuscar98_styles.json; local library143f387ad774525dc9abc0ff05fb5f4bfbaa5f02. Official thumbnail inspected only, not claimed as an original shot or copied into the final film. Gallery code/story/mascot not reused. This style is a gallery entry, not an invented ready-made66-style renderer.
- Original artwork: four generated images, hosts.png, retirement.png, events-a.png, events-b.png. Retirement uses hosts.png as identity reference. These are original illustrative reconstructions, not official gameplay, licensed trailer excerpts, actual screenshots or documentary event photographs. Lucia/Jason are fictional GTA VI characters requested by user; GTA/Rockstar and game characters remain their respective owners' properties. No real public-figure portrait is used. Football and conclave are symbolic still lifes.
- Source original generated PNG files remain in /workspace/generated_images; project copies are retained for reproducibility. Contact-sheet quadrants are cropped only in Canvas for this video. New album/photo material rendering, camera and compositing are in film.js.
- Typography: Kalam Regular/Bold and Noto Sans Arabic reused from films/connected-speech-marker/fonts with OFL licenses in that project's licenses/Kalam-OFL.txt and Persian-Noto-font-license.txt. No proprietary Morabba file.
- SFX: Wyzowl sfx-kit, https://github.com/wyzowl/sfx-kit, CC0-1.0. Six actual files and license copied into assets/sfx; per-file hashes/source in manifest.json. No film/game score or copyrighted meme audio. Additional deterministic short UFO/bell/coastal texture synthesized in tools/mix.py.
- Rendering infrastructure uses existing Opuscar MIT core/render helpers. No new upstream style/demo code edited and no watermark or LemoLab sign-off on the user's movie.
''')
(P/'DECISIONS.md').write_text('''# Production decisions

- Current user supplied exact narration/script and explicitly allows selective meme humour and over-the-top moments; the complete source is authoritative.
- User confirmed intended publication is after actual confirmed release. Do not label this production as independent confirmation of release today; do not add an unsupported date or award name.
- Preserve full-production and independent-work preference, portrait1080×1920, raised Persian captions, no music and automatic scoped commit/push. No repeated approval gate.
- One analogue family-album look, with Vice City pastel cyan/magenta/violet environmental accents. Print saturation is restrained; the living-photo phase restores a little colour. No generic whiteboard/cut-paper replacement.
- Hero hosts hold a shared instant print; retirement repeats the same faces/clothes with a deliberately oversized pocket watch. Character identity uses referenced generation, not claims of an official screenshot. Static figures are not claimed as full body animation.
- Photographic UFO background alone gets horizontal panning smear. Stationary hosts use photographic depth/softness plus the camera and grade; avoid a rectangular sharp/blur mask around people.
- Public-event memes use symbolic objects rather than simulated news portraits. No fabricated footage, documentary labels or factual timestamps. One attempted real-football portrait generation was rejected by the image service; it was replaced with jersey/trophy still-life art, not another attempt to obtain the same blocked portrait.
- English meme content is legible on photo borders; Persian bottom subtitles translate spoken English. Separate content and caption channels. No full bilingual paragraphs, extra CTA or invented narrator lines.
- Subtraction pass: removed decorative tiny footer; separated award inset from nomination caption and moved host cameo away from papal label; retirement stamp is above faces. Restrained photo/stamp motion on selected punchlines.
- All speech stays on its source clock. Paper/camera-effect lead/tail carries transitions; no false claim that source narration was chopped into J/L cuts.
- No new dependency installs or music/voice tier required: existing Node/Chromium/FFmpeg/Python/ASR/SFX tooling works. CPU Canvas2D avoids the software-GPU bottleneck;24fps is native Opuscar cadence.
- Only this new film and its final MP4 are staged; cancelled Olympic v4 materials and earlier approved versions remain untouched.
''')
(P/'README.md').write_text('''# GTA VI meme retirement — Family Album Polaroids

71s portrait film from the exact supplied Persian/English script and narrator. Output: ../../video/gta6-family-album-v1.mp4. Intended for publication after actual release, as user confirmed. This is not a release-date verification. Original generated photographic illustration, not gameplay. Full supplied voice, Persian captions, selective meme humour; no music.

Preproduction: TREATMENT.md, STORYBOARD.md, ART_DIRECTION.md, SOUND_PLAN.md. Sources and limitations: CREDITS.md, ANALYSIS.fa.md, QC.json. File identities: assets/input-manifest.json. Caption track also exported as captions.fa.srt. Final pinned download recorded in DELIVERY.json after push/verification.

Rebuild from repository root, using installed project tools:

```bash
/workspace/lemo-opuscar/.venv/bin/python films/gta6-family-album/tools/prepare.py
PLAYWRIGHT_CHROME=/usr/bin/chromium LEMO_ANGLE=swiftshader node films/gta6-family-album/tools/check-film.mjs
/workspace/lemo-opuscar/.venv/bin/python films/gta6-family-album/tools/mix.py
PLAYWRIGHT_CHROME=/usr/bin/chromium LEMO_ANGLE=swiftshader node core/render/video.mjs films/gta6-family-album --fps 24 --workers 3 --size 1080x1920 --out films/gta6-family-album/out/picture.mp4
bash films/gta6-family-album/tools/export.sh
/workspace/lemo-opuscar/.venv/bin/python films/gta6-family-album/tools/verify.py
```

Node24, FFmpeg7, Chromium, Playwright, Python with numpy/scipy/soundfile/soxr/Pillow and local optional sherpa ASR are already available. Artwork is retained in assets, so regeneration/paid generation is not needed to render. Intermediates under out/stills are ignored. SFX WAV source assets are explicitly versioned with CC0 license; other intermediate WAVs remain local.
''')
assets=[]
for file,origin in [('hosts.png','exec-9277e1ec-bd63-4bc4-9ef2-38baf2310d08.png'),('events-a.png','exec-3dc9f42f-bd5b-47f8-a848-1f0bbe9ac8f7.png'),('events-b.png','exec-27404333-9ab9-4cfa-8ed0-5ff88db10bc2.png'),('retirement.png','exec-6173502f-1770-4c18-b310-00edb41ac0e5.png')]:
 d=(P/'assets'/file).read_bytes();assets.append({'file':'assets/'+file,'source':'generated artwork','original_generated_file':origin,'identity_reference':'assets/hosts.png' if file=='retirement.png' else None,'sha256':hashlib.sha256(d).hexdigest(),'bytes':len(d),'official_gameplay':False})
(P/'assets/artwork-manifest.json').write_text(json.dumps(assets,indent=2)+'\n')
print('project memory exported')
