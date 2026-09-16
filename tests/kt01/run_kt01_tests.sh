#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BUILD="${ROOT}/.kt01-build"
rm -rf "$BUILD"
mkdir -p "$BUILD"
cd "$BUILD"

FC="${FC:-gfortran}"
FFLAGS="${FFLAGS:--std=f2008 -ffree-line-length-none -Wall -Wextra -Werror -fcheck=all -fbacktrace}"

"$FC" $FFLAGS -c \
  "$ROOT/prototype/kt01/mod_animo_time_coordinate.f90" \
  "$ROOT/prototype/kt01/mod_animo_runtime_contracts.f90" \
  "$ROOT/prototype/kt01/mod_animo_kernel_transactions.f90" \
  "$ROOT/prototype/kt01/mod_animo_committed_persistence.f90" \
  "$ROOT/prototype/kt01/mod_animo_worker_context.f90" \
  "$ROOT/prototype/kt01/mod_animo_interval_runtime.f90"

"$FC" $FFLAGS -o test_kt01_runtime \
  mod_animo_time_coordinate.o \
  mod_animo_runtime_contracts.o \
  mod_animo_kernel_transactions.o \
  mod_animo_committed_persistence.o \
  mod_animo_worker_context.o \
  mod_animo_interval_runtime.o \
  "$ROOT/tests/kt01/test_kt01_runtime.f90"

./test_kt01_runtime

"$FC" $FFLAGS -o test_kt01_identity_envelope \
  mod_animo_time_coordinate.o \
  mod_animo_runtime_contracts.o \
  mod_animo_kernel_transactions.o \
  mod_animo_committed_persistence.o \
  mod_animo_worker_context.o \
  "$ROOT/tests/kt01/test_kt01_identity_envelope.f90"

./test_kt01_identity_envelope
cd "$ROOT"
python3 tests/kt01/test_kt01_structure.py
rm -rf "$BUILD"
