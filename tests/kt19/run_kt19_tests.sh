#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$root"
python tests/kt19/test_pinned_lwkm_file_provider.py
python tests/test_legacy_unformatted.py
