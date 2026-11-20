# Whiteboard readiness — technical check

User selected https://lemomo-ai.github.io/lemo-opuscar/styles/whiteboard/ for the next Reel and requested readiness before supplying content. This is a technical smoke check, not a storyboard or a user film.

The gallery page returned HTTP proxy 403, so the official upstream STYLE.md was retrieved from raw.githubusercontent.com. It is byte-identical to the existing local whiteboard STYLE.md. Style invariants reviewed: one glossy dry-erase board, live single-line writing, floating markers without hands, moving magnets/eraser, camera travelling across one board, meaningful limited ink colours and stroke-aligned foley. The previous paper texture/peel grammar does not carry over.

Existing Node 24, FFmpeg 7, Chromium, Playwright and Opuscar Python core dependencies passed dependency discovery. SFX Kit is already present. Installed only the style's missing Architects Daughter font via its official pinned font script; EMS Tech single-line paths were already available. No voice/music tier or paid service was installed or invoked.

The MIT native engine and general helpers are vendored here with a small 1080×1920 viewport adaptation (screen dimensions, camera centre, ink buffer and gloss fill). Stroke geometry, handwriting, props, board and material rendering remain native. Font metadata retains EMS Tech's authorship/OFL information; Architects Daughter OFL and upstream MIT are included. Existing Persian font is shared from the prior project for joined Persian captions, an explicit localization adaptation.

`smoke.js` draws only READY, an arrow and a circle with native floating markers, gloss, ghost ink, camera movement and a Persian caption. The 3-second test uses no narration/music. This confirms rendering, not final creative direction or listening quality. User's established defaults persist: Instagram portrait, stronger purposeful blue/red, raised Persian captions, speech-priority effects, no added music, automatic scoped commits/pushes and version-specific downloadable video delivery after actual production.

Rebuild from repo root:

```bash
PLAYWRIGHT_CHROME=/usr/bin/chromium LEMO_ANGLE=swiftshader node core/render/video.mjs setup/whiteboard-readiness --fps 24 --workers 1 --size 1080x1920 --out setup/whiteboard-readiness/smoke.mp4
```

Next required input: supplied final script. Also send narration and any clips/images/references to use. Topic-specific board layout, learning flow, footage decisions and sound plan follow content analysis; no demo story is reused.
