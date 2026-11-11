# Opuscar Short Video Director

Version **1.1.0**. A reusable agent skill for short-video production from an existing script, specializing in educational storytelling for language learners. [راهنمای فارسی](README.fa.md).

## Install and invoke

Extract the ZIP and place the `opuscar-short-video-director` directory in your agent's supported skills directory. For Codex personal skills, this is normally `~/.agents/skills/`. Keep `SKILL.md` directly inside that folder. Other agents have their own installation paths; importing a ZIP is supported only where the host offers it.

Example: “Use `$opuscar-short-video-director` with this supplied script. Make an Instagram Reel; ask how involved I want to be, then plan the storyboard, direction and audio.”

The skill is not automatically registered by downloading it. It needs an agent with file/shell access, a working rendering environment, and any media-generation/transcription capabilities the chosen project requires. No API key, cloud account, model weights, video, font or sound library is bundled. Do not claim unavailable capabilities are installed.

## Automatic repository saving and video downloads

Every completed meaningful project change/revision is committed and pushed to the designated project repo, including requested previews. No repeated “commit/push” instruction is needed. Downloads point to the exact pushed video commit; ten-second reviews use the cumulative movie. Task-branch previews do not require PR merge. Private repos stay private and use authenticated downloads. See [repository delivery](references/repository-delivery.md).

## Sources

- Primary library: https://github.com/lemomo-ai/lemo-opuscar
- Style gallery: https://lemomo-ai.github.io/lemo-opuscar/
- Opuscar98 style showcase: https://lemomo-ai.github.io/lemo-opuscar/opuscar98/#styles
- Sound selection and timing: https://github.com/wyzowl/sfx-kit

The instructions are an independent workflow built around these sources. They do not redistribute upstream code or media. Third-party tools and assets retain their own licenses. Script authorship and project materials remain with their owners.

## Helpers

Run helpers only after reading `SKILL.md` and environment-specific rules. Use an absolute tools/project path and quote paths with spaces.

```bash
# Read-only readiness report; no downloads or installs.
python3 scripts/doctor.py --lib-dir /path/to/lemo-opuscar --sfx-dir /path/to/sfx-kit

# Clone missing libraries and install the upstream core tier, after reading it.
bash scripts/setup.sh --tools-dir /path/to/project-tools

# Require an existing UTF-8 script; do not overwrite an existing project.
python3 scripts/init_project.py --project /path/to/my-film --script-file /path/to/script.md

# Run after filling the plan; an untouched template intentionally fails readiness.
python3 scripts/validate_plan.py /path/to/my-film

# After the agent commits/pushes a real video: check its remote version and public download.
python3 scripts/video_link.py --repo /path/to/repo --file video/my-film-v003.mp4 --visibility public --verify-download

# Standard-library helper/packaging checks, no downloads or media generation.
python3 scripts/selftest.py
```

`setup.sh --check-only` is read-only. `--skip-deps` only clones/checks the libraries. `--voice` or `--music` install optional upstream tiers only when explicitly needed/authorized; there is no default music installation. Existing repositories are never reset, pulled or automatically updated. Setup stops on a dirty checkout or an upstream-managed auto-reset configuration; use a fresh tools folder or reuse working tools with `doctor.py`.

System Git, Node/npm, Python, FFmpeg/ffprobe and browser OS dependencies may need platform-specific installation. The setup helper reports missing prerequisites rather than silently invoking administrator package managers. An agent may install them when authorized and supported by its environment. Optional providers/transcription models must be configured separately.

`validate_plan.py` checks JSON timing/coverage/readiness, not whether a film is beautiful, audible or factually correct. It deliberately does not install dependencies, render video, listen, infer licensing or certify Instagram compatibility. Real production checks are in `references/quality.md`.

## Project memory

Templates keep decisions out of repeated chat questions. `brief.json` records audience, delivery, collaboration and audio/text policy. `timeline.json` stores frame-based shots/captions and sample-based narration source mapping, visual milestones and sound sync events. Markdown sheets explain creative decisions and review status. `QC.json` distinguishes technical checks from actual watching/listening.

Historical details from the original production are not hardcoded: no mandatory gouache/paper-cut style, Persian subtitle language, English flags, championship story, comment keyword, audio provider or public GitHub delivery. Those are project choices.

The video-link helper is read-only except for network requests. It never commits, pushes or merges. For private repositories, omit `--verify-download` and use an authorized browser/connector to verify the authenticated URL. It rejects uncommitted files and Git LFS pointers.

## License

Original instructions, templates and helper scripts in this package are licensed under MIT; see [LICENSE](LICENSE). Upstream repositories are linked, not included.
