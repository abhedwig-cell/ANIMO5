#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$root"
build="$(mktemp -d)"
trap 'rm -rf "$build"' EXIT
gfortran -std=f2008 -Wall -Wextra -Werror -ffp-contract=off -fno-fast-math -J "$build" -I "$build" \
  prototype/kt02/runtime/mod_transient_time.f90 \
  prototype/ubforce01/mod_animo_tcd042_upper_solute_load_contract.f90 \
  prototype/ubforce02/mod_animo_tcd042_upper_solute_load_resolver.f90 \
  prototype/boundq01/mod_animo_static_boundary_chemistry_adapter.f90 \
  prototype/boundq02/mod_animo_static_boundary_year_binding.f90 \
  tests/boundq02/test_static_boundary_year_binding.f90 \
  -o "$build/test_boundq02"
"$build/test_boundq02"
