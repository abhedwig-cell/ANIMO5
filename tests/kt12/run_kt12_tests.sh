#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
build="$(mktemp -d)"
trap 'rm -rf "$build"' EXIT
cd "$build"
gfortran -std=f2008 -Wall -Wextra -Werror -J . -I . \
  "$root/prototype/kt02/runtime/mod_transient_time.f90" \
  "$root/prototype/kt02/runtime/mod_transient_contracts.f90" \
  "$root/prototype/kt02/runtime/mod_transient_transactions.f90" \
  "$root/prototype/kt02/runtime/mod_transient_interval_runtime.f90" \
  "$root/prototype/kt12/mod_animo_tcd042_upper_boundary_client.f90" \
  "$root/tests/kt12/test_kt12_tcd042_client.f90" \
  -o test_kt12
./test_kt12
