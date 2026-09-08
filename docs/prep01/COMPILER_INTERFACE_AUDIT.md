# Compiler and legacy Fortran interface audit baseline

Status: `SOURCE_AUDIT_BASELINE_ESTABLISHED_NOT_YET_DEFECT_QUALIFIED`.

Compiler diagnostics and static scans are evidence for investigation. A warning is not automatically a scientific defect.

## Source-bound structural findings

The supplied 4.1.5 revision-53 candidate contains about 150 program units and relies predominantly on external subroutine/function interfaces rather than explicit module interfaces. `IMPLICIT NONE` is common, but explicit procedure interfaces are generally absent.

Very long formal argument lists are confirmed. Examples from the supplied source are:

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

These lists are not yet labelled `REDUNDANT_INTERFACE`: redundancy requires per-argument read/write/propagation and call-site analysis. Their size does establish a dedicated migration/audit risk.

## Preliminary audit matrix

| Audit item | PREP01 status | Classification |
| --- | --- | --- |
| implicit procedure interfaces | CONFIRMED_WIDESPREAD | SUSPICIOUS_LEGACY_CONSTRUCT |
| type mismatches | PARTIALLY_PROBED | NOT_ASSESSED |
| kind mismatches | PARTIALLY_PROBED | NOT_ASSESSED |
| scalar/array mismatches | PARTIALLY_PROBED | NOT_ASSESSED |
| shape inconsistencies | PARTIALLY_PROBED | NOT_ASSESSED |
| missing/incorrect intents | WIDESPREAD_ABSENCE_OF_INTENT_METADATA | DOCUMENTATION_GAP |
| unused arguments | NOT_ASSESSED_PER_ARGUMENT | NOT_ASSESSED |
| propagation-only arguments | NOT_ASSESSED_PER_ARGUMENT | NOT_ASSESSED |
| inconsistent call sites | PARTIALLY_PROBED | NOT_ASSESSED |
| aliasing | NOT_ASSESSED | NOT_ASSESSED |
| missing initialization | NOT_ASSESSED | NOT_ASSESSED |
| unclear argument semantics | CONFIRMED_RISK | DOCUMENTATION_GAP |
| unclear argument units | PARTLY_DOCUMENTED_IN_4_0_GUIDE | DOCUMENTATION_GAP |
| hidden side effects | CONFIRMED_RISK_FROM_FILE_IO_AND_SAVE_STATE | SUSPICIOUS_LEGACY_CONSTRUCT |
| COMMON blocks | NONE_FOUND_BY_STATIC_SCAN | NOT_ASSESSED_BEYOND_SCAN |
| saved mutable local state | PRESENT_IN_SELECTED_ROUTINES | SUSPICIOUS_LEGACY_CONSTRUCT |
| direct STOP in top-level logic | CONFIRMED | SUSPICIOUS_LEGACY_CONSTRUCT |
| direct file I/O in model program | CONFIRMED_WIDESPREAD | SUSPICIOUS_LEGACY_CONSTRUCT |

## Precision findings

The code uses default `REAL` heavily and also contains explicit `REAL(4)`, `REAL(8)` and `INTEGER(8)` usages. Precision is not centralized behind a single kind-policy module. The source also includes conversion/truncation utilities related to real-size handling.

Classification: `SUSPICIOUS_LEGACY_CONSTRUCT`, not a confirmed numerical defect. ANIMO5 precision must remain an explicit numerical policy and any conversion from legacy precision needs qualification evidence.

## Portability findings

Confirmed source/toolchain dependencies include case-insensitive include names, Intel `dfport/secnds`, `KINT`/`KIDNNT` behaviour and a GNU-incompatible output-list construct. See `GNU_COMPILER_PROBE.md`.

## Next audit step

PREP02 should produce an argument-semantics table for the highest-fanout routines before any interface shortening. For every argument, record owner, type/kind/shape, units, read/write role, persistence, call-chain propagation and whether it is scientifically meaningful or infrastructure-only.
