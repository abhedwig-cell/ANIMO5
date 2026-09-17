#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BUILD="${ROOT}/.build-kt05"
rm -rf "${BUILD}"
mkdir -p "${BUILD}"
cd "${BUILD}"

gfortran -std=f2008 -Wall -Wextra -Werror \\
  "${ROOT}/prototype/kt02/runtime/mod_transient_time.f90" \\
  "${ROOT}/prototype/kt02/runtime/mod_transient_contracts.f90" \\
  "${ROOT}/prototype/kt02/runtime/mod_transient_transactions.f90" \\
  "${ROOT}/prototype/kt02/runtime/mod_transient_interval_runtime.f90" \\
  "${ROOT}/prototype/kt05/mod_animo_explicit_hydrology_runtime_adapter.f90" \\
  "${ROOT}/tests/kt05/test_kt05_explicit_runtime_adapter.f90" \\
  -o kt05_explicit_runtime_adapter

./kt05_explicit_runtime_adapter
