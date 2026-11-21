# GTA VI meme retirement — Family Album Polaroids

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
