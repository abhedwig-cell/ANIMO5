# ANIMO-GHG01 — GHGMais compatibility analysis

Status: `CONTROLLED_ONE_MISMATCH_DESCENDANT_CONFIRMS_STRUCTURAL_LINEAGE_BLOCK`

This document characterizes revision-53 parser incompatibilities without repairing the supplied testcase. The frozen `GHGMais` bytes remain B0 historical input evidence exactly as supplied. No derived testcase in this work unit is B0 or B2.

## 1. Evidence boundary

Frozen testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Frozen revision-53 source SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

The ordinary PREP diagnostic case adapter performs execution-environment adaptations only: path separator/case materialization, legacy unformatted-record framing conversion and the already documented GNU list-directed `PrintBalLabel` compatibility change. Those adaptations do not alter scientific inputs and remain `DIAGNOSTIC_NOT_REFERENCE`.

A scientific/input-schema compatibility descendant is a separate evidence class:

`COMPATIBILITY_DIAGNOSTIC_DESCENDANT`

It can characterize one parser mismatch at a time where possible. It cannot inherit B0 or B2 status from its parent.

## 2. Parent behaviour against revision 53

The runtime-adapted but scientifically unchanged GHGMais case reaches the revision-53 parser and stops with:

```text
STOP 1995
Error: label ">outGHG:" not found in file "Input/general.inp"
```

This is the first observed incompatibility, not evidence that it is the only incompatibility.

The frozen case already contains equivalent-looking GHG metadata under `MATERIAL.INP >defGHG:`:

```text
25. 298. 6 11 12 13 14 15 16
```

Its own comments identify these as CH4 and N2O CO2-equivalent conversion factors, the number of selected CO2 fractions and fraction numbers. Revision 53 expects the same semantic categories at `GENERAL.INP >outGHG:` but in a different location and record order.

## 3. Controlled descendant GHG01-CDD-001

Only one mismatch was changed.

The descendant appends to the execution-copy `GENERAL.INP`:

```text
>outGHG: --------------- GHG compatibility diagnostic metadata ----------------
6
11 12 13 14 15 16
25.0 298.0
```

Every numerical value is copied from the supplied `>defGHG:` block. The original `>defGHG:` block remains present. No `>orgcom:` section is added, no `>deffra:` row is rewritten and no new scientific parameter is invented.

Identity:

- frozen parent `GENERAL.INP`: `0210c9529ae90178412154aa40cf74b44872129a646ad933857650448220224f`;
- runtime-adapted `GENERAL.INP` before this scientific-schema transform: `a803ed49fdf16cb295924bbd3f52f3d5aea9cc58d0b3ac022101e53593753b66`;
- CDD-001 `GENERAL.INP`: `bf6c33dfab1c0c53dce3c79120be12a23c392dbf24dcc19336d62bb53236c8b0`.

Machine-readable transformation and run metadata are stored in:

`integration/animo-ghg/GHGMAIS_CDD001.json`

The local run-manifest SHA-256 recorded at execution time is:

`05a73c61cc436369e1692bd7eb576418e902636d7b9614bf62ab3371310a22b3`

That hash identifies the execution-time local diagnostic manifest, not the Git repository blob created later.

## 4. Result of CDD-001

CDD-001 passes the first `>outGHG:` requirement and then stops at the next independent revision-53 requirement:

```text
Error: label ">orgcom:" not found in file "Input/material.inp"
```

This confirms experimentally that the source/testcase mismatch is structural rather than a single missing label.

The result is strictly diagnostic:

- GHG main-process branch reached: `NO`;
- CH4 state mutation observed: `NO`;
- N2O state mutation observed: `NO`;
- GHG scientific output observed: `NO`;
- historical behaviour claim: `NOT_PERMITTED`.

## 5. Why no CDD-002 was created

A second automatic transform would no longer be a clean one-mismatch parser characterization.

Revision 53 requires `MATERIAL.INP >orgcom:` with one global `Cfracom`. GHGMais has no such block. Instead its `>deffra:` rows contain extra positional `RQ` and `cbfr` fields before `nifr`. Revision 53 does not read these positions. It expects:

```text
Frno, Recfav, Hufros, Ratio_rd_st, Asfa, Nifr, [Pofr]
```

Therefore reaching the next parser stage would require choosing a global carbon fraction and deciding how the GHGMais per-fraction `cbfr` and `RQ` semantics map to revision-53 state and reaction parameters. Those are scientific interpretations, not parser-neutral relocation operations.

Creating such a descendant without a source-native schema specification would violate the fail-closed rule. It could produce a runnable testcase while silently changing its physical meaning. That would be weaker evidence, not stronger evidence.

## 6. Supplied output-selection intent

The supplied `GENERAL.INP` clearly requests a GHG-active run through `GreenHouseGasOption=1`. Its `[GreenHouseGasses]` selection enables CO2 outputs and the N2O emission/state/production/reduction suite plus annual GHG output. The CH4-specific emission/state/production/oxidation output switches are set to zero.

This is useful lineage evidence about requested observability. It is not evidence that the case ever executed successfully with revision 53 or that CH4 was physically inactive. Output selection is not process activation.

## 7. Compatibility conclusion

The strongest admissible conclusion is:

`GHGMais` and revision 53 share substantial GHG vocabulary and later ANIMO 4.1-style configuration concepts, but the supplied testcase belongs to a different input-contract lineage. CDD-001 proves that moving only already-present GHG output metadata to the revision-53-required label exposes a second independent material-schema mismatch before any GHG physics executes.

The exact consuming source/executable lineage remains unresolved. Further transformation is blocked until an authoritative schema can explain `>defGHG:`, `>orgcom:`, `RQ`, `cbfr` and the changed `>deffra:` positional contract without inference.

Qualification:

- testcase artifact lineage: `B0_HISTORICAL_INPUT_EVIDENCE`;
- revision-53 behavioural testcase: `NOT_ADMITTED`;
- compatibility descendant: `DIAGNOSTIC_ONLY`;
- activated-process evidence from GHGMais descendants: `INSUFFICIENT_EVIDENCE`;
- historical reference: `REFERENCE_BLOCKED`.
