#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$root"
PYTHONPATH="$root" python tests/kt21/test_lwkm_bounded_envelope.py
bash tests/kt19/run_kt19_tests.sh
