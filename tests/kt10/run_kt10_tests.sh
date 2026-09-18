#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BUILD="${ROOT}/.build-kt10"
rm -rf "${BUILD}"
mkdir -p "${BUILD}"
cd "${BUILD}"

expected_kt06_blob="9a24ea833291f761d2fa76ca4cc9fee28436c614"
actual_kt06_blob="$(git -C "${ROOT}" hash-object prototype/kt06/mod_animo_explicit_hydrology_runtime_binding.f90)"
if [[ "${actual_kt06_blob}" != "${expected_kt06_blob}" ]]; then
  echo "Frozen KT06 implementation blob changed: ${actual_kt06_blob}" >&2
  exit 1
fi

gfortran -std=f2008 -Wall -Wextra -Werror -fcheck=all \
  "${ROOT}/prototype/kt02/runtime/mod_transient_time.f90" \
  "${ROOT}/prototype/kt02/runtime/mod_transient_contracts.f90" \
  "${ROOT}/prototype/kt02/runtime/mod_transient_transactions.f90" \
  "${ROOT}/prototype/kt02/runtime/mod_transient_interval_runtime.f90" \
  "${ROOT}/prototype/kt05/mod_animo_hydrology_adapter.f90" \
  "${ROOT}/prototype/kt06/mod_animo_explicit_hydrology_runtime_binding.f90" \
  "${ROOT}/tests/kt10/test_kt10_kt06_adversarial_boundaries.f90" \
  -o kt10_kt06_adversarial_boundaries

./kt10_kt06_adversarial_boundaries
