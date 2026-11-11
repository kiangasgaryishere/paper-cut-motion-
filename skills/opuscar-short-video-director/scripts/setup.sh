#!/usr/bin/env bash
# Read current upstream/environment instructions before running. No pulls/resets.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
TOOLS_DIR="$PWD/.opuscar-tools"
CHECK_ONLY=0
SKIP_DEPS=0
TIERS=(core)
while [ "$#" -gt 0 ]; do
  case "$1" in
    --tools-dir) [ "$#" -ge 2 ] && [ -n "$2" ] || { echo 'Missing --tools-dir value' >&2; exit 2; }; TOOLS_DIR=$2; shift 2 ;;
    --check-only) CHECK_ONLY=1; shift ;;
    --skip-deps) SKIP_DEPS=1; shift ;;
    --voice) TIERS+=(voice); shift ;;
    --music) TIERS+=(music); shift ;;
    -h|--help) echo 'setup.sh [--tools-dir PATH] [--check-only|--skip-deps] [--voice] [--music]'; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done
PYTHON_BIN=$(command -v python3 || command -v python || true)
[ -n "$PYTHON_BIN" ] || { echo 'Python 3.11+ is needed. Install it using your environment-supported method.' >&2; exit 2; }
"$PYTHON_BIN" -c 'import sys;sys.exit(sys.version_info<(3,11))' || { echo 'Python 3.11+ is needed.' >&2; exit 2; }
TOOLS_DIR=$("$PYTHON_BIN" -c 'import os,sys;print(os.path.abspath(os.path.expanduser(sys.argv[1])))' "$TOOLS_DIR")
LIB_DIR="$TOOLS_DIR/lemo-opuscar"
SFX_DIR="$TOOLS_DIR/sfx-kit"
if [ "$CHECK_ONLY" -eq 1 ]; then
  exec "$PYTHON_BIN" "$HERE/doctor.py" --lib-dir "$LIB_DIR" --sfx-dir "$SFX_DIR"
fi
for cmd in git node npm ffmpeg ffprobe; do
  command -v "$cmd" >/dev/null || { echo "Missing $cmd. Install it using the environment-supported method; this helper does not run administrator package managers." >&2; exit 2; }
done
node -e 'process.exit(Number(process.versions.node.split(".")[0])<20)' || { echo 'Node 20+ required; check current Opuscar requirements.' >&2; exit 2; }
mkdir -p "$TOOLS_DIR"
get_repo() {
  local dest=$1 remote=$2
  if [ -e "$dest" ]; then
    [ -d "$dest/.git" ] || [ -f "$dest/.git" ] || { echo "Existing non-repository path: $dest. Choose a different tools directory." >&2; exit 2; }
    [ -z "$(git -C "$dest" status --porcelain)" ] || { echo "Checkout has local changes: $dest. Reuse it with doctor.py or choose a fresh tools folder." >&2; exit 2; }
    echo "Reusing $dest without updating it."
  else
    git clone --depth 1 "$remote" "$dest"
  fi
}
get_repo "$LIB_DIR" https://github.com/lemomo-ai/lemo-opuscar.git
get_repo "$SFX_DIR" https://github.com/wyzowl/sfx-kit.git
[ -f "$LIB_DIR/AGENTS.md" ] && [ -f "$LIB_DIR/core/render/video.mjs" ] && [ -f "$SFX_DIR/GUIDE.md" ] && [ -f "$SFX_DIR/sounds.json" ] || { echo 'Unexpected repository layout; inspect the current upstream instructions.' >&2; exit 2; }
if [ "$SKIP_DEPS" -eq 0 ]; then
  [ "$(git -C "$LIB_DIR" config --get lemo.managed || true)" != true ] || { echo 'This upstream-managed checkout may auto-reset. This helper will not invoke that behavior; choose a fresh tools folder or reuse working tools with doctor.py.' >&2; exit 2; }
  [ -f "$LIB_DIR/plugin/skills/lemo-opuscar/scripts/setup.sh" ] || { echo 'Upstream setup entry point changed; inspect TECHNIQUE.md.' >&2; exit 2; }
  (cd "$LIB_DIR"; set -- deps
    for tier in "${TIERS[@]}"; do [ "$tier" = core ] || set -- "$@" "$tier"; done
    LEMO_OPUSCAR_HOME="$LIB_DIR" sh plugin/skills/lemo-opuscar/scripts/setup.sh "$@")
fi
echo "LIB=$LIB_DIR"
echo "SFX_KIT=$SFX_DIR"
git -C "$LIB_DIR" rev-parse HEAD
git -C "$SFX_DIR" rev-parse HEAD
if [ "$SKIP_DEPS" -eq 1 ]; then
  echo 'Fetch-only mode: dependencies and rendering still need validation.'
else
  "$PYTHON_BIN" "$HERE/doctor.py" --lib-dir "$LIB_DIR" --sfx-dir "$SFX_DIR"
fi
