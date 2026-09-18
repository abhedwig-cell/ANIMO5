#!/usr/bin/env bash
set -euo pipefail

build_dir="$(mktemp -d)"
trap 'rm -rf "$build_dir"' EXIT

python3 tests/kt09/test_kt09_fixture_integrity.py
python3 tools/kt09_fixture_to_fortran.py   reference/kt09/LWKM_REPRESENTATIVE_ANCHOR_PACKETS.json.zlib.b64   "$build_dir/mod_kt09_real_lwkm_anchors.f90"

gfortran -std=f2008 -Wall -Wextra -Werror -fcheck=all   -J "$build_dir"   -o "$build_dir/test_kt09_real_anchor_projection"   prototype/kt05/mod_animo_hydrology_adapter.f90   "$build_dir/mod_kt09_real_lwkm_anchors.f90"   tests/kt09/test_kt09_real_anchor_projection.f90

"$build_dir/test_kt09_real_anchor_projection"
