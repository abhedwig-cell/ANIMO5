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
  "$root/prototype/ubforce01/mod_animo_tcd042_upper_solute_load_contract.f90" \
  "$root/prototype/ubforce02/mod_animo_tcd042_upper_solute_load_resolver.f90" \
  "$root/prototype/boundq01/mod_animo_static_boundary_chemistry_adapter.f90" \
  "$root/prototype/boundq02/mod_animo_static_boundary_year_binding.f90" \
  "$root/prototype/stateq09/mod_animo_detailed_hydrology_origin_state.f90" \
  "$root/prototype/stateq10/mod_animo_first_detailed_hydrology_origin.f90" \
  "$root/prototype/kt12/mod_animo_tcd042_upper_boundary_client.f90" \
  "$root/prototype/stateq11/mod_animo_composite_accepted_continuation.f90" \
  "$root/tests/stateq11/test_composite_accepted_continuation.f90" \
  -o test_stateq11
./test_stateq11
