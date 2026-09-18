#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
build="$(mktemp -d)"
trap 'rm -rf "$build"' EXIT
cd "$build"
gfortran -std=f2008 -Wall -Wextra -Werror -J . -I . \
  "$root/prototype/kt02/runtime/mod_transient_time.f90" \
  "$root/prototype/hydroq01/mod_animo_resolved_upper_hydrology_contract.f90" \
  "$root/tests/hydroq01/test_resolved_upper_hydrology_contract.f90" \
  -o test_hydroq01
./test_hydroq01
