#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
build="$(mktemp -d)"
trap 'rm -rf "$build"' EXIT
cd "$build"
gfortran -std=f2008 -Wall -Wextra -Werror -ffp-contract=off -fno-fast-math \
  "$root/prototype/stateq09/mod_animo_detailed_hydrology_origin_state.f90" \
  "$root/tests/stateq09/test_detailed_hydrology_origin_state.f90" \
  -o test_stateq09
./test_stateq09
