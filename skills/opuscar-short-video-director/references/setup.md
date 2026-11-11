# Environment and Opuscar setup

## Inspect first

Respect the host's filesystem, installation, network and credential rules. Read available environment guidance. Reuse working tools; never replace a user's environment or update repositories silently. Do not hardcode `/workspace`, a particular virtualenv, provider or OS package manager.

Read current upstream documentation at setup time. Sources and commands can change; the helper is a convenience, not an authority over the repository.

1. Locate a user-selected/existing Lemo checkout, or clone https://github.com/lemomo-ai/lemo-opuscar into a dedicated tools directory. Record commit/version.
2. Read `AGENTS.md`, `DIRECTOR.md`, `TECHNIQUE.md`, `core/README.md`, setup script and selected style specification. Inspect saved user styles too.
3. Current core installation entry point from the library root is `sh plugin/skills/lemo-opuscar/scripts/setup.sh deps`. It handles Node packages, headless browser and Python core dependencies. Review it before running: some upstream-managed checkouts auto-update/reset. Do not execute that behavior on a user's dirty/shared worktree.
4. Install style-specific packages into the film's private environment. Install voice/transcription or music tiers only when actually needed and authorized; supplied narration does not require installing every TTS provider. Persian and mixed-language transcription may need a compatible multilingual tool.
5. Obtain SFX Kit from https://github.com/wyzowl/sfx-kit. Read `GUIDE.md`, `sounds.json`, `catalogue.md` and `LICENSE`. Record revision. Select only needed assets into the project and save provenance/sync metadata.
6. Check Git, Node/npm, supported Python, FFmpeg/ffprobe, Chromium, fonts, media decoding and disk space. At the source version inspected for this skill, Node 20+, Python 3.11+ and FFmpeg 7+ are expected. Recheck current requirements.
7. Render a tiny smoke frame/clip using the actual project/style and test its export audio path before expensive production. A passing dependency report alone does not prove a working renderer.

## Helpers

```bash
python3 scripts/doctor.py --lib-dir /path/to/lemo-opuscar --sfx-dir /path/to/sfx-kit
bash scripts/setup.sh --tools-dir /path/to/project-tools
```

The setup helper clones only missing directories, refuses unsafe existing checkouts, and never pulls/resets. It installs only Opuscar's core tier unless `--voice` / `--music` is explicitly passed. `--skip-deps` fetches/checks only; `--check-only` changes nothing. Missing system tools are reported with the next step; install using the actual environment's supported method and existing authorization.

No external repositories, media, models or credentials are bundled with the skill. Setup needs permitted network access. If offline, use valid existing sources and explain any real limitation; do not pretend a download succeeded.

## Renderer contract

Follow the current core documentation. The usual page contract is deterministic `window.render(t)`, positive `window.DUR`, and `window.READY` after fonts/images load; `window.EV` and `window.TEXTS` can support sound events/readability checks. Avoid random/time/state dependencies. Run the library's tools from its root with an absolute project path:

```bash
cd "$LIB"
node core/render/still.mjs "$PROJECT" 1.5
node core/render/video.mjs "$PROJECT" --fps 30 --size 1080x1920 --out "$PROJECT/out/picture.mp4"
```

Verify flags against the checked-out tool before using them. A `start/end` query only works when the project's own renderer implements it; it is not a universal Opuscar trim command. Use `$LIB` for library scripts, self-host project assets/fonts, and keep production outside upstream `core/` and `styles/`.
