#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
build="$(mktemp -d)"
trap 'rm -rf "$build"' EXIT
cd "$build"
gfortran -std=f2008 -Wall -Wextra -Werror -J . -I . \
  "$root/prototype/kt02/runtime/mod_transient_time.f90" \
  "$root/prototype/hydroq02/mod_animo_tcd042_runoff_load_context.f90" \
  "$root/tests/hydroq02/test_runoff_load_context.f90" \
  -o test_hydroq02
./test_hydroq02
