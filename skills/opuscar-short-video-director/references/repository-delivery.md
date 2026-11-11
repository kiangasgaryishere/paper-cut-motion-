# Automatic saving and one-click video delivery

## Default contract

The user's selected project repo is the home of the work. Commit and push **each completed meaningful change**: environment/skill setup, approved plan/assets, a rendered review increment, a completed revision, and final delivery. Include a requested downloadable preview in its completed revision. Do not commit each keystroke or intermediate render frame. Do not batch several finished user requests into an unsaved end-of-session change.

Discover repo, remote, working branch and visibility from the attached context/connector/Git when possible. Record them once in `brief.delivery`. If no repo or write access is available, ask only for the missing destination/access; continue independent work and explain the actual push blocker. Never invent a successful push. The user need not repeat “commit and push” after every revision.

## Scoped Git procedure

1. Inspect current branch and status. Keep unrelated user changes and cancelled work out of the commit. Work in the current authorized task branch or an isolated branch/worktree when needed; never push changes into the upstream Lemo/SFX libraries.
2. Finish the change and appropriate checks. Save required scripts, plans, selected licensed assets and the video export. Ignore dependencies, caches, raw renders, model weights and credentials. Do not automatically publish private source media absent authorization for those materials.
3. Stage explicit project paths, review the staged diff, and create a descriptive commit. Push to the selected task branch. Do not use force push, reset others' work, disable branch protections or merge without authorization. Resolve ordinary issues inside the authorized scope; report a genuine access/conflict blocker.
4. Verify the actual remote branch has the video commit. Record version, commit, duration/resolution, artifact path and SHA-256. Distinguish local commit success from push success.
5. Build a link to the exact pushed video version and check it. Return it immediately for that completed review/delivery. Do not require the user to browse folders, find a commit, click through a PR or ask for a link.

Pushing a task branch is enough for a commit-pinned download; a PR need not be merged to review the video. If a PR is part of the environment, keep it current, but do not make merging a routine preview step. A missing auth token should be configured in the environment, never pasted in chat or embedded in URLs.

## Video files and version names

Default output folder: `video/`. Use a clear project-specific version, e.g. `video/my-film-v003.mp4`, `video/my-film-through-030s-v003.mp4` or `video/my-film-preview-v003.mp4`. Preserve earlier reviewed versions or stable commit links. A new export should not silently replace the link the user is currently reviewing.

Track the real MP4 directly when it fits the host's file limits. A Git LFS pointer is not the video; never give a raw pointer link as a download. If the video exceeds current repository limits, keep the required quality and use a repo-associated supported artifact/asset method within existing authorization, such as an appropriate release asset, or explain the concrete limitation. Do not quietly downscale, split the final into unusable fragments, make a private repo public, or publish a release merely to evade a permission boundary.

## Public GitHub links

Use the **full video commit SHA**, not `main` or a moving branch:

```text
https://raw.githubusercontent.com/OWNER/REPO/VIDEO_COMMIT/video/my-film-v003.mp4
```

URL-encode path components (spaces, non-ASCII names) and preserve `/`. Download with the environment's allowed tools and compare to the local file SHA-256. Verify it is video bytes, not HTML, an authentication page, a 404 response or an LFS pointer. Do not put tokens in the URL. A browser may play an MP4 first; the same video URL can be saved/downloaded.

## Private GitHub links

Keep the repo private and give the user's authenticated file download URL:

```text
https://github.com/OWNER/REPO/blob/VIDEO_COMMIT/video/my-film-v003.mp4?raw=true
```

Briefly say “Open while signed into the GitHub account with access.” An authorized connector may verify/download the actual bytes. An anonymous raw URL returning 404 is not proof that a private video is missing. Do not claim anonymous accessibility or publish private media elsewhere without authorization. Public sharing is a separate user choice.

## Helper and delivery record

```bash
python3 scripts/video_link.py --repo /path/to/repo --file video/my-film-v003.mp4 --visibility public --verify-download
```

The helper rejects an uncommitted/modified artifact, checks the remote branch tip with `git ls-remote`, creates a commit-pinned link, and optionally checks a public download hash. `--branch` selects an explicitly authorized branch if needed. Private validation needs the authenticated environment separately. The helper performs no commit, push, merge or credential setup.

Record the result in `QC.json` and `DECISIONS.md`. If saving that record creates a later metadata-only commit, its video link should still point to the verified earlier video commit; do not create an endless self-referential commit/hash loop. These records are included in the next appropriate save.

## User-facing response

Keep it easy: one sentence about the change, then **Download preview** or **Download full video**, plus the relevant duration/version if useful. Include the cumulative video link in ten-second mode. Do not substitute a source ZIP, repository homepage, local workspace path or PR link for the requested MP4. If push/download verification failed, state the real status and provide an available temporary local delivery without pretending it came from GitHub.
