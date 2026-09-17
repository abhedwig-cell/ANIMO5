#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BUILD="${ROOT}/.build-kt02"
rm -rf "${BUILD}"
mkdir -p "${BUILD}"
cd "${BUILD}"

gfortran -std=f2008 -Wall -Wextra -Werror \
  "${ROOT}/prototype/kt02/runtime/mod_transient_time.f90" \
  "${ROOT}/prototype/kt02/runtime/mod_transient_contracts.f90" \
  "${ROOT}/prototype/kt02/runtime/mod_transient_transactions.f90" \
  "${ROOT}/prototype/kt02/runtime/mod_transient_interval_runtime.f90" \
  "${ROOT}/prototype/kt02/runtime/mod_transient_persistence.f90" \
  "${ROOT}/prototype/kt02/runtime/mod_transient_worker_context.f90" \
  "${ROOT}/prototype/kt02/clients/mod_swap_like_client.f90" \
  "${ROOT}/prototype/kt02/clients/mod_animo_like_client.f90" \
  "${ROOT}/tests/kt02/test_kt02_dual_client.f90" \
  -o kt02_dual_client

./kt02_dual_client
python3 "${ROOT}/tests/kt02/test_kt02_structure.py"
