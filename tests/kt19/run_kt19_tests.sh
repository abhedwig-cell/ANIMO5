#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$root"
python -m unittest tests.kt19.test_pinned_lwkm_file_provider
python -m unittest tests.test_legacy_unformatted
