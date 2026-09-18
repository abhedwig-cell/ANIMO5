#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
build="$(mktemp -d)"
trap 'rm -rf "$build"' EXIT
cd "$build"
gfortran -std=f2008 -Wall -Wextra -Werror -ffp-contract=off -fno-fast-math -J . -I . \
  "$root/prototype/kt02/runtime/mod_transient_time.f90" \
  "$root/prototype/kt02/runtime/mod_transient_contracts.f90" \
  "$root/prototype/kt02/runtime/mod_transient_transactions.f90" \
  "$root/prototype/kt02/runtime/mod_transient_interval_runtime.f90" \
  "$root/prototype/kt05/mod_animo_hydrology_adapter.f90" \
  "$root/prototype/kt06/mod_animo_explicit_hydrology_runtime_binding.f90" \
  "$root/prototype/hydroq01/mod_animo_resolved_upper_hydrology_contract.f90" \
  "$root/prototype/hydroq02/mod_animo_tcd042_runoff_load_context.f90" \
  "$root/prototype/hydroexec01/mod_animo_bounded_no_ponding_upper_hydrology.f90" \
  "$root/prototype/ubforce01/mod_animo_tcd042_upper_solute_load_contract.f90" \
  "$root/prototype/ubforce02/mod_animo_tcd042_upper_solute_load_resolver.f90" \
  "$root/prototype/kt12/mod_animo_tcd042_upper_boundary_client.f90" \
  "$root/prototype/kt13/mod_animo_tcd042_bounded_composition.f90" \
  "$root/tests/kt13/test_kt13_bounded_composition.f90" \
  -o test_kt13
./test_kt13
