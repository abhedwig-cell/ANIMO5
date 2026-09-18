#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$root"
build="$root/build/kt20"
rm -rf "$build"
mkdir -p "$build"

PYTHONPATH="$root" python tests/kt20/test_kt20_packet_frame.py

base64 -d reference/kt19/LWKM_FIRST_PACKET_POWERSTATION_B1.b64 > "$build/real_first_packet.bin"
PYTHONPATH="$root" python prototype/kt20/hydrology_packet_frame.py ci-frames   "$build/real_first_packet.bin" "$build"

gfortran -std=f2008 -Wall -Wextra -Werror -ffp-contract=off -fno-fast-math -J "$build" -I "$build"   prototype/kt02/runtime/mod_transient_time.f90   prototype/kt02/runtime/mod_transient_contracts.f90   prototype/kt02/runtime/mod_transient_transactions.f90   prototype/kt02/runtime/mod_transient_interval_runtime.f90   prototype/kt05/mod_animo_hydrology_adapter.f90   prototype/kt06/mod_animo_explicit_hydrology_runtime_binding.f90   prototype/kt11/mod_animo_multi_packet_hydrology_provider.f90   prototype/hydroq01/mod_animo_resolved_upper_hydrology_contract.f90   prototype/hydroq02/mod_animo_tcd042_runoff_load_context.f90   prototype/hydroexec01/mod_animo_bounded_no_ponding_upper_hydrology.f90   prototype/ubforce01/mod_animo_tcd042_upper_solute_load_contract.f90   prototype/ubforce02/mod_animo_tcd042_upper_solute_load_resolver.f90   prototype/boundq01/mod_animo_static_boundary_chemistry_adapter.f90   prototype/boundq02/mod_animo_static_boundary_year_binding.f90   prototype/boundq02b/mod_animo_immutable_static_boundary_frame.f90   prototype/kt12/mod_animo_tcd042_upper_boundary_client.f90   prototype/kt13/mod_animo_tcd042_bounded_composition.f90   prototype/kt14/mod_animo_tcd042_boundary_frame_composition.f90   prototype/stateq09/mod_animo_detailed_hydrology_origin_state.f90   prototype/stateq10/mod_animo_first_detailed_hydrology_origin.f90   prototype/stateq11/mod_animo_composite_accepted_continuation.f90   prototype/kt15/mod_animo_atomic_composite_application.f90   prototype/kt18/mod_animo_provider_backed_application.f90   prototype/kt20/mod_animo_kt20_hydrology_packet_frame.f90   tests/kt20/test_kt20_packet_bridge.f90   -o "$build/test_kt20"

"$build/test_kt20"

# Regression gates for both sides of the bridge.
bash tests/kt19/run_kt19_tests.sh
bash tests/kt18/run_kt18_tests.sh
