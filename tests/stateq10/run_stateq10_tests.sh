#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
build="$(mktemp -d)"
trap 'rm -rf "$build"' EXIT
cd "$build"
gfortran -std=f2008 -Wall -Wextra -Werror -ffp-contract=off -fno-fast-math \
  "$root/prototype/stateq10/mod_animo_first_detailed_hydrology_origin.f90" \
  "$root/tests/stateq10/test_first_detailed_hydrology_origin.f90" \
  -o test_stateq10
./test_stateq10
