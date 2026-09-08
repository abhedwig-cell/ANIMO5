# Compiler and legacy Fortran interface audit baseline

Status: `SOURCE_AUDIT_BASELINE_BUILD_CONTRACT_DEPENDENCIES_CONFIRMED`.

Compiler diagnostics and static scans are evidence for investigation. A warning is not automatically a scientific defect, and a failure under the wrong compiler-default semantics is not evidence of a legacy scientific defect.

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

These lists are not labelled `REDUNDANT_INTERFACE`. Redundancy requires per-argument read/write/propagation and call-site analysis. A long list can be architecturally poor without containing scientifically redundant data.

## `Dble_trunc`: corrected classification

The earlier PREP01 GNU probe used four-byte default `REAL`. Under that build:

- `Function.for` defined `Dble_trunc` as `REAL(8)`;
- active callers declared the external function as default `REAL`;
- the implicit procedure interface therefore behaved as a return-kind mismatch;
- Ruurlo hydrology end time was corrupted and the run stopped at `STOP 1111`.

That was initially classified as a confirmed legacy interface defect. This classification was too strong.

Source inspection shows a broader precision pattern:

- hydrology staging variables use explicit `REAL(4)`;
- `Dble_trunc` explicitly converts to `REAL(8)`;
- caller-side state is widely declared as default `REAL`;
- transport code contains comments and constructs consistent with conversion from four-byte external forcing to an eight-byte internal default-real model.

When GNU is built with eight-byte default `REAL`, while retaining eight-byte `DOUBLE PRECISION` through `-fdefault-double-8`, the apparent `Dble_trunc` result mismatch disappears and eight testcases execute without the earlier NaNs.

Current classification:

`BUILD_CONTRACT_DEPENDENCY`

The source is still fragile because procedure result kinds are not protected by explicit interfaces and correctness depends on compiler-default kind policy. But PREP01 no longer calls `Dble_trunc` a demonstrated defect in the historical ANIMO executable.

## Local storage duration

`Outbal_write` initializes local character format strings in an `Itask=1` invocation and reuses them during a later `Itask=3` invocation without explicit `SAVE`.

With ordinary automatic local storage the GNU diagnostic run reaches final output and fails because those values are no longer valid. With `-fno-automatic`, no source `SAVE` patch is required and the routine behaves deterministically.

Classification:

`BUILD_CONTRACT_DEPENDENCY`

Again, the source is non-portable because required storage duration is implicit. Exact historical Intel project semantics remain to be recovered or independently qualified.

## Preliminary audit matrix

| Audit item | PREP01 status | Classification |
| --- | --- | --- |
| implicit procedure interfaces | CONFIRMED_WIDESPREAD | SUSPICIOUS_LEGACY_CONSTRUCT |
| result-kind dependence on compiler defaults | CONFIRMED | BUILD_CONTRACT_DEPENDENCY |
| other kind mismatches | PARTIALLY_PROBED | NOT_ASSESSED |
| scalar/array mismatches | PARTIALLY_PROBED | NOT_ASSESSED |
| shape inconsistencies | PARTIALLY_PROBED | NOT_ASSESSED |
| missing/incorrect intents | WIDESPREAD_ABSENCE_OF_INTENT_METADATA | DOCUMENTATION_GAP |
| unused arguments | NOT_ASSESSED_PER_ARGUMENT | NOT_ASSESSED |
| propagation-only arguments | NOT_ASSESSED_PER_ARGUMENT | NOT_ASSESSED |
| inconsistent call sites | PARTIALLY_PROBED | NOT_ASSESSED |
| aliasing | NOT_ASSESSED | NOT_ASSESSED |
| missing initialization | NOT_CONFIRMED_AS_CURRENT_BLOCKER | NOT_ASSESSED |
| unclear argument semantics | CONFIRMED_RISK | DOCUMENTATION_GAP |
| unclear argument units | PARTLY_DOCUMENTED_IN_4_0_GUIDE | DOCUMENTATION_GAP |
| hidden side effects | CONFIRMED_RISK_FROM_FILE_IO_AND_LOCAL_STATE | SUSPICIOUS_LEGACY_CONSTRUCT |
| COMMON blocks | NONE_FOUND_BY_STATIC_SCAN | NOT_ASSESSED_BEYOND_SCAN |
| saved/static mutable local state | BUILD_SEMANTICS_MATERIAL | BUILD_CONTRACT_DEPENDENCY |
| direct STOP in top-level logic | CONFIRMED | SUSPICIOUS_LEGACY_CONSTRUCT |
| direct file I/O in model program | CONFIRMED_WIDESPREAD | SUSPICIOUS_LEGACY_CONSTRUCT |

## Precision findings

The code uses default `REAL` heavily and also contains explicit `REAL(4)`, `REAL(8)` and `INTEGER(8)` usages. Precision is not centralized behind a single kind-policy module.

The paired GNU probes demonstrate that default kind selection is part of the behavioural build contract. Precision modernization therefore cannot be treated as a mechanical declaration cleanup.

ANIMO5 precision remains an explicit numerical policy. No mixed-precision migration is admitted by PREP01.

## Portability findings

Confirmed source/toolchain dependencies include:

- case-insensitive include names;
- Intel `dfport/secnds`;
- `KINT`/`KIDNNT` behaviour;
- compiler/runtime-dependent binary unformatted records;
- one GNU-incompatible output-list construct;
- eight-byte default-real semantics in the current evidence-derived diagnostic contract;
- static local storage semantics in the current evidence-derived diagnostic contract.

`tools/build_gnu_diagnostic.py` records these dependencies as an explicit, source-hash-bound diagnostic recipe. It does not claim historical equivalence.

## Next interface-audit step

The next useful interface work is no longer NaN chasing. It is semantic audit of the largest interfaces and systematic external-function result crosschecking.

For every large-routine argument, record:

- owner;
- type, kind and shape;
- units;
- read, write or read/write role;
- continuation-state relevance;
- call-chain propagation;
- whether it is scientifically meaningful, I/O/configuration-only, diagnostics-only, scratch, or redundant.

Only after that evidence exists may argument lists be shortened or grouped into coherent data structures.
