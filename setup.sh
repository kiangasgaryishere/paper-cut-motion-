#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
npm ci --no-audit --no-fund
if [ ! -x .venv/bin/python ]; then python3 -m venv .venv; fi
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
