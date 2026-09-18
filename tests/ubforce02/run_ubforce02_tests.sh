#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
build="$(mktemp -d)"
trap 'rm -rf "$build"' EXIT
cd "$build"
gfortran -std=f2008 -Wall -Wextra -Werror -J . -I . \
  "$root/prototype/kt02/runtime/mod_transient_time.f90" \
  "$root/prototype/ubforce01/mod_animo_tcd042_upper_solute_load_contract.f90" \
  "$root/prototype/ubforce02/mod_animo_tcd042_upper_solute_load_resolver.f90" \
  "$root/tests/ubforce02/test_upper_solute_load_resolver.f90" \
  -o test_ubforce02
./test_ubforce02
