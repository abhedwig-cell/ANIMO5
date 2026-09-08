# Legacy execution recovery evidence

Status: `STRUCTURAL_EXECUTION_RECOVERED_NUMERICAL_REFERENCE_NOT_QUALIFIED`.

This document records PREP01 execution-recovery work against the supplied ANIMO 4.1.5 revision-53 source and the frozen RuurloGrass testcase. No frozen source file was modified.

## 1. Legacy hydrology record framing

The RuurloGrass `SWATRE.UNF` file is not directly readable by GNU Fortran's default unformatted sequential runtime. Byte-level inspection establishes an observed framing for this case:

- file header byte: `0x4b`;
- each logical record: one-byte payload length, payload bytes, same one-byte trailing length;
- file trailer byte: `0x82`.

For RuurloGrass:

- source SHA-256: `36d8dbeee7a46c769026c7441ea607160a715768571ba3e048b32ee2ace74d13`;
- source size: 888148 bytes;
- logical records: 11691;
- observed payload lengths: 8, 12, 20, 24, 40, 80 and 84 bytes;
- first payload decodes exactly as `(1980, 1985, 1.0, 120.0, 1.0)`, matching the old-SWAP header read in `input1.for`.

`tools/convert_legacy_unformatted.py` rewrites record framing only. Payload bytes are copied unchanged. The converted Ruurlo file is 958292 bytes with SHA-256 `b5fc15f51074ba9e4131e0616b4348e31d523d0a8e874be6055bcd614de4de5c`.

The converter deliberately fails closed for high-bit/extended markers. `GHGMais/Input/result.bun` contains such a marker and is not admitted yet.

## 2. Confirmed `Dble_trunc` return-kind defect

The supplied `Function.for` defines `Dble_trunc` with a `REAL(8)` function result. Active callers, including `input1.for`, `Input_hydro.for` and `Animo.inc`, declare `Dble_trunc` as default `REAL`.

This is a source-level return-kind mismatch across an implicit procedure interface.

Under GNU Fortran the consequence is directly observable. The Ruurlo hydrology header contains `STimahy=120.0`, but the caller receives `Timahy=0.0` through the mismatched function result and terminates with `STOP 1111` because the ANIMO and hydrology periods no longer agree.

A diagnostic copy in which the function result is made consistent with the caller declaration passes that gate. The frozen source remains unchanged.

PREP01 classification: `CONFIRMED_DEFECT` for interface/type correctness. Scientific/numerical impact under the historical Intel build still requires reference evidence before a corrected legacy baseline is admitted.

## 3. Compiler-dependent local-state retention in `Outbal_write`

A GNU diagnostic run reaches the end of the Ruurlo simulation after the hydrology framing and `Dble_trunc` compatibility issues are bypassed, but initially fails at the final balance-description write. `Outbal_write` initializes local character format strings in the `Itask=1` path and reuses them in the later `Itask=3` path without an explicit `SAVE` declaration.

Adding `SAVE` only in a diagnostic copy permits the run to finish. This is currently classified `SUSPICIOUS_LEGACY_CONSTRUCT`, not yet `CONFIRMED_DEFECT`, because the exact historical Intel project flags are unavailable and could have imposed static local storage.

## 4. First completed diagnostic run

With three execution-only compatibility measures outside the frozen source:

1. GNU-oriented record-framing conversion of `SWATRE.UNF` with payload bytes unchanged;
2. a diagnostic correction of the `Dble_trunc` result-kind mismatch;
3. diagnostic persistence of the `Outbal_write` local format strings;

the supplied RuurloGrass case reaches:

`Successful completion of simulation`

and produces the expected broad classes of legacy outputs and mass-balance files.

This run is **not** a scientific reference result.

The run reports IEEE invalid/divide-by-zero/overflow/denormal exceptions and contains 7788 message lines with `NaN`. `OXYDEM` fails to converge from the first simulated timestep, with `NaN` values in aerated fractions and oxygen-demand diagnostics. Therefore none of these output files may be promoted to `FROZEN_LEGACY`, `CORRECTED_LEGACY_REFERENCE`, RR or QG expected values.

## 5. Current interpretation

Execution recovery has moved from a file-format blocker to a numerical/reference blocker.

Established facts:

- the Ruurlo binary hydrology payload can be preserved exactly while converting only record framing;
- the supplied source contains a confirmed implicit-interface result-kind mismatch in `Dble_trunc`;
- a full control-flow run is possible under GNU with explicit diagnostic compatibility adaptations;
- that run is numerically invalid and cannot serve as behavioural truth.

Still unresolved:

- exact historical Intel compiler/project flags;
- whether `Dble_trunc` produced materially different behaviour in the historical qualified executable;
- source of the first `OXYDEM` NaN and whether it is a legacy numerical defect, an uninitialized-state/compiler-semantics dependency, or a consequence of another interface mismatch;
- byte/reference outputs from a trusted native ANIMO 4.1.5 revision-53 executable;
- extended record framing used by the GHGMais `result.bun` case.

## Gate

PREP01 must remain fail-closed. Structural program completion is not equivalent to a reproducible scientific legacy reference.
