#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 maet.py install "$@"
python3 maet.py doctor
