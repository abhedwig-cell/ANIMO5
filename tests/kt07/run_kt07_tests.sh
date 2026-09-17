#!/usr/bin/env bash
set -euo pipefail

build_dir="$(mktemp -d)"
trap 'rm -rf "$build_dir"' EXIT

python3 tests/kt07/test_kt07_fixture_integrity.py
python3 tools/kt07_fixture_to_fortran.py   reference/kt07/LWKM_FIRST_EXPLICIT_HYDROLOGY_STEP.json   "$build_dir/mod_kt07_real_lwkm_fixture.f90"

gfortran -std=f2008 -Wall -Wextra -Werror -fcheck=all   -J "$build_dir"   -o "$build_dir/test_kt07_real_packet_projection"   prototype/kt05/mod_animo_hydrology_adapter.f90   "$build_dir/mod_kt07_real_lwkm_fixture.f90"   tests/kt07/test_kt07_real_packet_projection.f90

"$build_dir/test_kt07_real_packet_projection"
