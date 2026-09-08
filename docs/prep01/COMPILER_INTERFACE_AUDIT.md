# Compiler and legacy Fortran interface audit baseline

Status: `SOURCE_AUDIT_BASELINE_WITH_CONFIRMED_INTERFACE_DEFECT`.

Compiler diagnostics and static scans are evidence for investigation. A warning is not automatically a scientific defect.

## Source-bound structural findings

The supplied 4.1.5 revision-53 candidate contains about 150 program units and relies predominantly on external subroutine/function interfaces rather than explicit module interfaces. `IMPLICIT NONE` is common, but explicit procedure interfaces are generally absent.

Very long formal argument lists are confirmed.

| Routine | Formal arguments | PREP01 classification |
| --- | ---: | --- |
| `Input1` | 352 | SUSPICIOUS_LEGACY_CONSTRUCT |
| `Outbal_calc` | 246 | SUSPICIOUS_LEGACY_CONSTRUCT |
| `Inicalc` | 198 | SUSPICIOUS_LEGACY_CONSTRUCT |
| `Init` | 194 | SUSPICIOUS_LEGACY_CONSTRUCT |
| `Input_Echo` | 155 | SUSPICIOUS_LEGACY_CONSTRUCT |
| `Outsel` | 143 | SUSPICIOUS_LEGACY_CONSTRUCT |
| `Addit` | 140 | SUSPICIOUS_LEGACY_CONSTRUCT |
| `Resp_miner` | 133 | SUSPICIOUS_LEGACY_CONSTRUCT |

These lists are not yet labelled `REDUNDANT_INTERFACE`: redundancy requires per-argument read/write/propagation and call-site analysis.

## Confirmed result-kind mismatch: `Dble_trunc`

`Function.for` defines `Dble_trunc` with a `REAL(8)` function result. Active callers declare it as default `REAL`, including `input1.for`, `Input_hydro.for` and `Animo.inc`. Because the function is called through implicit interfaces, the mismatch is not prevented by the source structure.

GNU execution supplies direct behavioural evidence of the mismatch: the frozen Ruurlo hydrology record contains end time `120.0`, while the caller obtains `0.0`, causing the simulation-period gate to terminate with `STOP 1111`. A diagnostic copy with a caller-consistent result kind passes this gate.

Classification: `CONFIRMED_DEFECT` for Fortran interface/type correctness. Whether the historical Intel executable masked, exposed or numerically depended on this mismatch remains a qualification question and must not be guessed.

## Preliminary audit matrix

| Audit item | PREP01 status | Classification |
| --- | --- | --- |
| implicit procedure interfaces | CONFIRMED_WIDESPREAD | SUSPICIOUS_LEGACY_CONSTRUCT |
| type/result-kind mismatches | CONFIRMED_AT_DBLE_TRUNC; MORE_NOT_ASSESSED | CONFIRMED_DEFECT |
| other kind mismatches | PARTIALLY_PROBED | NOT_ASSESSED |
| scalar/array mismatches | PARTIALLY_PROBED | NOT_ASSESSED |
| shape inconsistencies | PARTIALLY_PROBED | NOT_ASSESSED |
| missing/incorrect intents | WIDESPREAD_ABSENCE_OF_INTENT_METADATA | DOCUMENTATION_GAP |
| unused arguments | NOT_ASSESSED_PER_ARGUMENT | NOT_ASSESSED |
| propagation-only arguments | NOT_ASSESSED_PER_ARGUMENT | NOT_ASSESSED |
| inconsistent call sites | PARTIALLY_PROBED | NOT_ASSESSED |
| aliasing | NOT_ASSESSED | NOT_ASSESSED |
| missing initialization | ACTIVE_INVESTIGATION_AFTER_DIAGNOSTIC_NAN_RUN | NOT_ASSESSED |
| unclear argument semantics | CONFIRMED_RISK | DOCUMENTATION_GAP |
| unclear argument units | PARTLY_DOCUMENTED_IN_4_0_GUIDE | DOCUMENTATION_GAP |
| hidden side effects | CONFIRMED_RISK_FROM_FILE_IO_AND_LOCAL_STATE | SUSPICIOUS_LEGACY_CONSTRUCT |
| COMMON blocks | NONE_FOUND_BY_STATIC_SCAN | NOT_ASSESSED_BEYOND_SCAN |
| saved mutable local state | PRESENT_IN_SELECTED_ROUTINES | SUSPICIOUS_LEGACY_CONSTRUCT |
| implicit local-state persistence assumptions | CONFIRMED_IN_OUTBAL_WRITE_PATTERN | SUSPICIOUS_LEGACY_CONSTRUCT |
| direct STOP in top-level logic | CONFIRMED | SUSPICIOUS_LEGACY_CONSTRUCT |
| direct file I/O in model program | CONFIRMED_WIDESPREAD | SUSPICIOUS_LEGACY_CONSTRUCT |

## Precision findings

The code uses default `REAL` heavily and also contains explicit `REAL(4)`, `REAL(8)` and `INTEGER(8)` usages. Precision is not centralized behind a single kind-policy module. The `Dble_trunc` mismatch shows why precision and interface kinds cannot be treated as cosmetic modernization.

ANIMO5 precision remains an explicit numerical policy. No mixed-precision migration is admitted by PREP01.

## Portability findings

Confirmed source/toolchain dependencies include case-insensitive include names, Intel `dfport/secnds`, `KINT`/`KIDNNT` behaviour, compiler/runtime-dependent binary unformatted records and a GNU-incompatible output-list construct. The legacy `Outbal_write` routine also reuses local format strings across separate invocations without explicit `SAVE`, which is compiler/project-setting dependent.

## Next audit step

1. localize the first source of the diagnostic `OXYDEM` NaN before accepting any GNU-run numerical result;
2. inventory all external function return declarations against definitions;
3. produce an argument-semantics table for highest-fanout routines before any interface shortening.

For every large-routine argument, record owner, type/kind/shape, units, read/write role, persistence, call-chain propagation and whether it is scientifically meaningful or infrastructure-only.
