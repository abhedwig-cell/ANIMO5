#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$root"
build="$(mktemp -d)"
trap 'rm -rf "$build"' EXIT
gfortran -std=f2008 -Wall -Wextra -Werror -ffp-contract=off -fno-fast-math -J "$build" -I "$build" \
  prototype/kt02/runtime/mod_transient_time.f90 \
  prototype/kt02/runtime/mod_transient_contracts.f90 \
  prototype/kt02/runtime/mod_transient_transactions.f90 \
  prototype/kt02/runtime/mod_transient_interval_runtime.f90 \
  prototype/kt05/mod_animo_hydrology_adapter.f90 \
  prototype/kt06/mod_animo_explicit_hydrology_runtime_binding.f90 \
  prototype/hydroq01/mod_animo_resolved_upper_hydrology_contract.f90 \
  prototype/hydroq02/mod_animo_tcd042_runoff_load_context.f90 \
  prototype/hydroexec01/mod_animo_bounded_no_ponding_upper_hydrology.f90 \
  prototype/ubforce01/mod_animo_tcd042_upper_solute_load_contract.f90 \
  prototype/ubforce02/mod_animo_tcd042_upper_solute_load_resolver.f90 \
  prototype/boundq01/mod_animo_static_boundary_chemistry_adapter.f90 \
  prototype/boundq02/mod_animo_static_boundary_year_binding.f90 \
  prototype/kt12/mod_animo_tcd042_upper_boundary_client.f90 \
  prototype/kt13/mod_animo_tcd042_bounded_composition.f90 \
  prototype/kt14/mod_animo_tcd042_boundary_frame_composition.f90 \
  tests/kt14/test_kt14_boundary_frame_composition.f90 \
  -o "$build/test_kt14"
"$build/test_kt14"
