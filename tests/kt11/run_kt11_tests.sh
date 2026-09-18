#!/usr/bin/env bash
set -euo pipefail

test "$(git hash-object prototype/kt06/mod_animo_explicit_hydrology_runtime_binding.f90)" = "9a24ea833291f761d2fa76ca4cc9fee28436c614"
test "$(git hash-object prototype/kt05/mod_animo_hydrology_adapter.f90)" = "9ed1d6d3e91d9f5522f8c2a49a5e19eed1d82a9a"
test "$(git hash-object prototype/kt02/runtime/mod_transient_interval_runtime.f90)" = "ac8eed3b7385daad3cb7c926bd7dab9d99e0a888"
test "$(git hash-object prototype/kt02/runtime/mod_transient_transactions.f90)" = "182164ca4bf4a890d98f9c89366764e5d818b10c"

python3 tests/kt11/test_kt11_upstream_evidence.py

build_dir="$(mktemp -d)"
trap 'rm -rf "$build_dir"' EXIT

python3 tools/kt11_materialize_kt09_anchors.py   reference/kt11/LWKM_REPRESENTATIVE_ANCHOR_PACKETS_KT09.json.zlib.b64   "$build_dir/mod_kt09_real_lwkm_anchors.f90"

gfortran -std=f2008 -Wall -Wextra -Werror -fcheck=all   -J "$build_dir"   -o "$build_dir/test_kt11_multi_packet_hydrology_provider"   prototype/kt02/runtime/mod_transient_time.f90   prototype/kt02/runtime/mod_transient_contracts.f90   prototype/kt02/runtime/mod_transient_transactions.f90   prototype/kt02/runtime/mod_transient_interval_runtime.f90   prototype/kt05/mod_animo_hydrology_adapter.f90   prototype/kt06/mod_animo_explicit_hydrology_runtime_binding.f90   "$build_dir/mod_kt09_real_lwkm_anchors.f90"   prototype/kt11/mod_animo_multi_packet_hydrology_provider.f90   tests/kt11/test_kt11_multi_packet_hydrology_provider.f90

"$build_dir/test_kt11_multi_packet_hydrology_provider"
