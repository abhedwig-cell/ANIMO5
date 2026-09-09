# Class-A accounting-only corrected-legacy eight-case matrix

Status: `DIAGNOSTIC_EIGHT_CASE_NONINTERFERENCE_SUPPORTED_ACTIVE_CORRECTION_COVERAGE_STILL_LWKM_ONLY`.

## Purpose

TCD-017 and TCD-018 are candidate Class-A corrected-legacy changes because they repair balance accounting without intending to change process rates, transport equations or model state.

The earlier composition probe demonstrated this only for LWKM. This matrix repeats the experiment across all eight supplied cases that complete under the deterministic GNU diagnostic contract.

The result is diagnostic evidence only. It does not qualify a corrected legacy reference and it does not admit production migration.

## Clean probe build

A clean execution-only build was made from the deterministic GNU diagnostic source copy. It contains only:

1. TCD-017: include the already tracked top-reservoir organic-P redistribution loss `Addiorpotoppl` in the organic-P balance ledger;
2. TCD-018: expose `Sic/Sict` to `Outbal_calc`, accumulate interception-storage change over each balance period and include that store change in `Bawa(Ddev)`.

Temporary NO3/NH4/PO4 observer instrumentation used during archaeology was excluded from this clean build.

Baseline GNU diagnostic executable SHA-256:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

Clean Class-A diagnostic executable SHA-256:

`733dd2750e819cebe3c41b425a065ef899fe1d6929660d3ef3a24518022fd94e`

The frozen source archive itself was not modified.

## Runtime result

All eight compatible supplied cases reach the legacy successful-completion path:

| testcase | completion | common outputs | normalized equal | intended differences | unintended differences |
| --- | --- | ---: | ---: | ---: | ---: |
| CranGrass | SUCCESS | 31 | 31 | 0 | 0 |
| CranMais | SUCCESS | 23 | 23 | 0 | 0 |
| GrassPeat | SUCCESS | 60 | 60 | 0 | 0 |
| LWKM_gras_1040.2021.2045 | SUCCESS | 55 | 43 | 12 | 0 |
| Puitmijn_Cranendonck_60 | SUCCESS | 77 | 77 | 0 | 0 |
| RuurloGrass | SUCCESS | 72 | 72 | 0 | 0 |
| STONE_akk_0006.2001.2015 | SUCCESS | 45 | 45 | 0 | 0 |
| Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA | SUCCESS | 16 | 16 | 0 | 0 |

Totals:

```text
cases completed                         8 / 8
outputs compared                         379
exact after declared volatile normalization 367
intended ledger differences               12
unintended differences                      0
missing candidate outputs                   0
extra candidate outputs                     0
```

The only normalization permitted is the already persisted legacy comparator policy for run/file timestamps and elapsed CPU seconds. Scientific numbers are not tolerance-filtered.

## The twelve changed outputs

All twelve changes occur in LWKM and are exactly the output families expected from TCD-017 and TCD-018:

```text
ani_pGP.Bal
ani_pRP.Bal
ani_pTP.Bal
ani_waGP.Bal
ani_waRP.Bal
ani_waTP.Bal
bapoGP.Out
bapoRP.Out
bapoTP.Out
bawaGP.Out
bawaRP.Out
bawaTP.Out
```

No ordinary concentration, process, state, uptake, discharge or other balance output changes in the eight-case comparison.

Seven of eight cases produce an output tree identical to baseline after only declared volatile metadata normalization. This demonstrates that the two correction paths remain inactive or net-zero there and do not perturb unrelated behaviour.

## Active LWKM effect

In the clean Class-A LWKM execution:

- maximum absolute water period residual becomes approximately `2.07e-4 mm` instead of the characteristic `~0.0601 mm` interception-ledger offset;
- maximum absolute organic-P period residual becomes approximately `6.54e-7 kg/ha P` instead of the ploughing-related `~0.0494 kg/ha P` maximum;
- known non-Class-A defects, including the NO3 transport nonclosure and dynamic PO4 numerical-conservation seam, remain present because they are deliberately outside this composition.

This is important: the Class-A composition does not hide unrelated known defects.

## What this proves and does not prove

Supported for the supplied eight-case diagnostic scope:

`state/process trajectory noninterference = strongly supported`

because all output differences are confined to the intended balance surfaces.

Not yet supported:

- reference-qualified equivalence to historical Intel behaviour;
- active TCD-017 and TCD-018 coverage in multiple independent cases;
- all possible ploughing schedules, interception-state transitions, balance-profile configurations or hydrology modes;
- production admission of either correction.

Only LWKM activates a measurable correction in the current eight-case matrix. Therefore the next active-coverage test should be designed, not inferred from the seven no-effect cases.

## Admission consequence

The Class-A corrected-legacy candidate can now be described as:

`DIAGNOSTIC_ACCOUNTING_ONLY_NONINTERFERENCE_SUPPORTED_ACROSS_EIGHT_COMPATIBLE_CASES`

It must remain below `QUALIFIED_CORRECTED_LEGACY` until the historical reference gate is available and the same noninterference/ledger checks are repeated against that reference.
