#!/usr/bin/env bash
set -euo pipefail

build_dir="$(mktemp -d)"
trap 'rm -rf "$build_dir"' EXIT

gfortran -std=f2008 -Wall -Wextra -Werror -fcheck=all \
  -J "$build_dir" \
  -o "$build_dir/test_kt05_explicit_adapter" \
  prototype/kt05/mod_animo_hydrology_adapter.f90 \
  tests/kt05/test_kt05_explicit_adapter.f90

"$build_dir/test_kt05_explicit_adapter"

python3 tests/kt05/test_kt05_structure.py
