#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$root"
build="$(mktemp -d)"
trap 'rm -rf "$build"; rm -f tests/boundq01/fixtures/bad_option.inp tests/boundq01/fixtures/bad_range.inp' EXIT
gfortran -std=f2008 -Wall -Wextra -Werror \
  prototype/boundq01/mod_animo_static_boundary_chemistry_adapter.f90 \
  tests/boundq01/test_static_boundary_chemistry.f90 \
  -o "$build/test_boundq01"
"$build/test_boundq01"
