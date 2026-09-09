# ANIMO-PREP10 — Stable-DOM plough accumulator audit

Status: `QUALIFIED_GNU_DIAGNOSTIC_CAUSAL_ACCUMULATOR_CARRYOVER_CONFIRMED_CONTROLLED_INPUT_DESCENDANTS_HISTORICAL_INTEL_OPEN`.

## Purpose

PREP10 follows the revision-53 stable dissolved-organic matter ploughing path in `Addit.for`, with particular attention to whether event-local redistribution accumulators are defined and reset before each management event.

Frozen source and supplied testcase bytes remain immutable. No production correction is admitted.

## Frozen identity

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

## Qualified source-level finding

The exact frozen source archive was scanned with `tools/audit_stable_dom_plough_accumulators.py`. The audit hash-pins the archive before inspecting `ANIMO_4.1.5.53/Addit.for`.

`Addit.for` declares scalar local accumulators:

```fortran
Real :: SuStdiorma, SuStdiorni, SuStdiorpo
```

The plough branch begins at source line 449. Within that branch the first assignments to the three accumulators are self-reading assignments:

- `SuStdiorma`: line 475;
- `SuStdiorni`: line 477;
- `SuStdiorpo`: line 479.

No explicit definition or zero assignment occurs before those first self-reads, and no explicit zero assignment for these three scalars was found elsewhere in the file. The exact `Addit.for` member is 35,615 bytes with SHA-256 `e3cf8f427e9a4b3743742039c89aae57864cb7268893e45797c7a17427dc8f5d`.

The source-level classification remains:

`CONFIRMED_SOURCE_LEVEL_USE_BEFORE_DEFINITION`

## Frozen testcase behavior is non-discriminating

The frozen CranMais testcase contains nine explicit plough requests, but its `>sdomin:` block is entirely zero initially. The exact initial member SHA-256 is `8df3d78e830f344bc315d4dff2ae4c1ee4d6e959a07ba7d112e4105e6fbbb201`.

An observer-only GNU diagnostic was then run across the frozen testbank. Four successful frozen cases actually reached the plough branch:

- CranMais: 9 events;
- LWKM_gras_1040.2021.2045: 4 events;
- STONE_akk_0006.2001.2015: 15 events;
- Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA: 3 events.

Across all 31 observed frozen-case events, `SuStdiorma`, `SuStdiorni` and `SuStdiorpo` were zero immediately before and after the accumulation loop. The observer produced no scientific or structural output difference after normalization of only declared volatile timestamps and elapsed CPU text. An explicit event-reset counterfactual likewise produced no scientific or structural difference for those frozen inputs.

Therefore the supplied frozen testbank is **non-discriminating** for this defect under the current GNU diagnostic environment. That is evidence of dormancy for those concrete frozen runs, not evidence that the source defect is harmless.

Machine-readable frozen-case evidence is in:

`integration/animo-prep/PREP10_GNU_STABLE_DOM_OBSERVER_MATRIX.json`

## GNU diagnostic-contract storage semantics

The existing GNU diagnostic build contract includes `-fno-automatic`. `tools/probe_prep10_local_storage_semantics.py` reproduces the relevant local self-read pattern independently of ANIMO.

GitHub Actions run `34302300827` demonstrated that under the diagnostic flag contract a synthetic local value persists across calls as `1.0`, `2.0`, `3.0`. With the additional diagnostic observer `-finit-real=snan`, the first undefined read becomes `NaN` rather than acquiring a physical interpretation.

This proves only the GNU diagnostic storage behavior of the synthetic pattern. It does not establish historical Intel behavior.

## Controlled causal activation

Because the frozen cases were non-discriminating, PREP10 created controlled B0-derived diagnostic input descendants. These descendants are not B0 and are not asserted to be realistic field states. They exist only to activate the code path causally.

`tools/make_prep10_sdomin_activation.py` is fail-closed. It verifies an explicit parent SHA-256, requires the selected original `>sdomin:` tokens to be zero, changes only specified tokens, preserves byte length, writes a new descendant, and records a transform manifest.

The diagnostic activation values used were:

- stable DOM: `1.000000E-04`;
- stable DON: `1.000000E-05`;
- stable DOP: `1.000000E-06`;
- indices `0,1,2` only.

No scientific realism or acceptance tolerance is attached to these amplitudes.

### CranMais C/N activation

Parent:

`ANIMO_testbank/CranMais/Input/Initial.inp`

Parent SHA-256:

`8df3d78e830f344bc315d4dff2ae4c1ee4d6e959a07ba7d112e4105e6fbbb201`

Controlled descendant SHA-256:

`a5acb3333207d0ed65814abf4d9b097bd752830cbf27f212aface3f1810f25f2`

CranMais has the phosphorus cycle disabled. Under the observer build, event 1 starts with all three accumulators at zero. After event 1:

- `SuStdiorma = 2.167093371709238E-08`;
- `SuStdiorni = 2.167093371709237E-09`;
- `SuStdiorpo = 0`.

Immediately before event 2, the C and N values are still exactly those event-1 accumulated values. The values continue to be carried through the remaining events.

The observer remained non-intrusive for the compared generated outputs: 23 generated files, 18 raw-equal and 5 equal after declared volatile normalization, with zero scientific or structural differences.

The explicit event-reset counterfactual **did** discriminate. Relative to the baseline diagnostic, 12 generated files contained scientific or structural differences:

- `Output/initial.out`;
- `banhMP.Out`;
- `banhTP.Out`;
- `baniMP.Out`;
- `baniTP.Out`;
- `banoMP.Out`;
- `banoTP.Out`;
- `baomMP.Out`;
- `baomTP.Out`;
- `discharge.out`;
- `miner-N.out`;
- `nitrate.out`.

Four additional balance files differed only in signed-zero formatting and are kept separate from the scientific/structural difference count.

### Phosphorus-enabled Zuiderzeeland activation

A second controlled descendant used the phosphorus-enabled case `Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA` so that the conditional `SuStdiorpo` branch was exercised.

Parent initial member SHA-256:

`f47dcbc7905f1d9d4b8b36def6e993e5f5ab31ebfd419b57a758e1f63c3e3937`

Controlled descendant SHA-256:

`7dddf3a6b5724866dc3dd06bf6a64941db15f4ccc0fd9abfa1c79490156a0550`

After the first observed plough event:

- `SuStdiorma = 1.3089539571491048E-07`;
- `SuStdiorni = 1.3089539571491032E-08`;
- `SuStdiorpo = 1.3089539571491044E-09`.

Immediately before event 2, all three values remain present. This independently demonstrates carryover of the conditional phosphorus accumulator under a phosphorus-enabled configuration.

The observer again remained non-intrusive for the compared generated outputs. The event-reset counterfactual produced scientific or structural differences in eight generated files, including N/P/organic-matter balance outputs, `bapoTP.Out`, `discharge.out` and `initial.out`. Two other balance files differed only by signed-zero formatting.

Machine-readable controlled-activation evidence is in:

`integration/animo-prep/PREP10_STABLE_DOM_CAUSAL_ACTIVATION_MATRIX.json`

## Qualified interpretation

For the current GNU diagnostic contract, PREP10 can now distinguish three statements that must not be collapsed:

1. **Source fact:** all three stable-DOM plough accumulators are self-read before explicit definition and are not reset per event.
2. **Frozen-testbank observation:** the supplied successful plough-active frozen cases happen to keep the three observed accumulators at zero, so those runs do not expose the defect numerically.
3. **Controlled causality:** when nonzero stable DOM/DON/DOP is introduced only in explicit B0-derived diagnostic descendants, the first event creates nonzero accumulator values, those values remain present before later plough events, and resetting the accumulators changes generated model outputs. The phosphorus-enabled descendant confirms the conditional P path as well.

The current qualification is therefore:

`QUALIFIED_GNU_DIAGNOSTIC_CAUSAL_ACCUMULATOR_CARRYOVER_CONFIRMED_CONTROLLED_INPUT_DESCENDANTS_HISTORICAL_INTEL_OPEN`

This is B1-style diagnostic causality evidence. It is not B2 historical-reference evidence and does not by itself admit an event reset as corrected legacy.

## Verification boundary

The diagnostic executables used in the controlled experiment reproduce the already persisted identities:

- baseline executable SHA-256: `0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`;
- observer executable SHA-256: `d179aba23e0a0ef90b118437c2817a0c3a0ec6f227be555598ba393c31d7a501`;
- event-reset counterfactual executable SHA-256: `f3518bbca36989960fbe02785d64cca873d5e45494baa4e0c0a9a7c026a717db`.

All controlled baseline, observer and event-reset runs completed successfully using the legacy `STOP 100` normal-completion contract. Raw source and raw testbank archives were not added to Git.

The repository CI validates the audit tools, transform tools and machine-readable evidence, but CI does not contain the restricted B0 archives and therefore does not rerun the controlled ANIMO executions themselves.

## What remains open

PREP10 does **not** yet establish:

- how the historical Intel Visual Fortran executable manifested the undefined locals;
- whether an independently provenance-qualified historical executable exhibits the same carryover;
- whether the diagnostic activation amplitudes represent realistic scientific states;
- a scientific acceptance tolerance or an admissible correction policy;
- corrected-legacy, B3 or ANIMO5 production admission.

The next scientific/governance step is no longer to prove GNU causality. That is now done. The next step is to disposition the defect through the separate corrected-legacy/B3 admission framework and, if a provenance-qualified historical native reference becomes available, determine its historical manifestation independently.
