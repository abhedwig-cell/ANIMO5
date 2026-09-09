# ANIMO-PREP10 — Stable-DOM causal activation report

Status: `QUALIFIED_SOURCE_DEFECT_AND_CURRENT_GNU_CAUSAL_EFFECT_FOR_STABLE_DOM_AND_DON_HISTORICAL_NATIVE_AND_DOP_OPEN`.

## Starting point

The parent PREP10 checkpoint had already established two facts for the exact revision-53 bytes:

1. `SuStdiorma`, `SuStdiorni` and `SuStdiorpo` are read in their first assignments in the plough branch without a preceding explicit definition or reset;
2. the frozen CranMais testcase requests nine plough events, but its initial `>sdomin:` vectors are all zero and the unmodified frozen case is therefore numerically non-discriminating under the current GNU diagnostic build.

The remaining question was whether a controlled, explicitly non-B0 diagnostic input could make the missing event reset causally visible.

## Diagnostic input design

The frozen CranMais `Input/Initial.inp` member is pinned at SHA-256:

`8df3d78e830f344bc315d4dff2ae4c1ee4d6e959a07ba7d112e4105e6fbbb201`

`tools/make_prep10_causal_initial.py` creates deterministic descendants and refuses any other parent hash. It changes only compartment indices 1 and 2 of the three `>sdomin:` vectors.

Single-species probes used here are:

- DOM: `CoStdiorma(1:2) = 1.0E-2`, descendant SHA-256 `d66acd69d62c2cfded22d581048a25b365b81d9972aa1a3a31fd55047d712f04`;
- DON: `CoStdiorni(1:2) = 1.0E-3`, descendant SHA-256 `a3e1349bba096d769438e62635f9408046d858c611ebdf5decb498afd1f30455`;
- DOP negative control: `CoStdiorpo(1:2) = 1.0E-4`, descendant SHA-256 `e9b3024ee98536ef563ac7929ce2af082c4b5d54b71bf36e02441ef77f1846a3`.

These values satisfy the revision-53 input range check but are diagnostic activation values only. No physical representativeness is claimed.

CranMais has `PhosphorusCycle=0`, so the DOP vector is not an active runtime probe in this testcase. It is retained as a negative control.

## Observer result

The combined observer descendant was run with the existing observer-only Addit working-copy transform under GNU Fortran 14.2.0 and the existing diagnostic build contract including `-fno-automatic`.

At the first plough event the observer recorded:

- before: `SuStdiorma = 0`, `SuStdiorni = 0`;
- after: `SuStdiorma = 2.1670933665864016E-06`, `SuStdiorni = 2.1670933665864018E-07`.

Immediately before the second plough event it recorded exactly the same retained values:

- `SuStdiorma = 2.1670933665864016E-06`;
- `SuStdiorni = 2.1670933665864018E-07`.

This directly demonstrates inter-event carryover under the current GNU diagnostic storage contract. The missing reset is therefore not merely a theoretical source concern in this environment.

## Baseline versus reset counterfactual

The same diagnostic input descendants were run with:

- baseline diagnostic executable SHA-256 `0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`;
- reset-counterfactual executable SHA-256 `f3518bbca36989960fbe02785d64cca873d5e45494baa4e0c0a9a7c026a717db`.

The reset build sets the three stable-DOM plough accumulators to zero at the start of each plough event. It remains a diagnostic counterfactual, not an admitted correction.

Comparisons used only the already declared volatile timestamp and CPU metadata normalization. No numerical tolerance was used to turn differences into matches.

### DOM-only activation

Baseline and reset differ in 16 scientific output files after volatile-only normalization, including the final restart output, organic-matter and nitrogen balance outputs, discharge, mineral-N and nitrate outputs.

In the final `>sdomin:` restart vector:

- baseline sum: `6.136175457677E-05`;
- reset sum: `1.3633400418508182E-05`;
- baseline minus reset: `4.772835415826182E-05`;
- baseline/reset ratio: `4.500840046733142`.

### DON-only activation

The same 16 scientific output files are discriminating.

In the final stable-DON restart vector:

- baseline sum: `6.136069957677E-06`;
- reset sum: `1.3632378235187933E-06`;
- baseline minus reset: `4.7728321341582064E-06`;
- baseline/reset ratio: `4.501100139547595`.

### DOP negative control

After declared volatile-only normalization, baseline and reset scientific outputs match. This is expected because CranMais disables the phosphorus cycle. It must not be interpreted as evidence that `SuStdiorpo` is safe.

## Qualification conclusion

For the exact revision-53 source and a hash-pinned controlled descendant of the frozen CranMais input, the missing reset of the stable-DOM and stable-DON plough accumulators has a reproducible causal numerical effect under the current GNU diagnostic build contract.

The qualified statement is deliberately narrower than a historical-legacy defect admission:

- source-level use-before-definition is qualified for DOM, DON and DOP accumulators;
- current-GNU causal numerical activation is qualified for DOM and DON;
- DOP runtime causality remains open because the chosen testcase disables phosphorus;
- historical Intel manifestation remains open;
- the activation values are diagnostic and not a scientific reference scenario;
- no correction, corrected-legacy baseline or ANIMO5 migration is admitted.

## CI verification

GitHub Actions run `34303844330` at head `1adcb12443a9a113a4f2f8daec8a1ed29a0b1b56` completed successfully. Thirteen PREP10 unit tests passed, the audit JSON files validated, the transform tools compiled, and the existing GNU storage-semantics probe remained green.

The private/restricted B0 archives were not copied into GitHub Actions or public Git. The actual causal model runs were executed in the authoring environment against locally supplied exact B0 bytes and are identified by the hashes recorded in `integration/animo-prep/PREP10_STABLE_DOM_CAUSAL_ACTIVATION.json`.

## Next gate

The next correction step must be separate from this audit. A minimal event-reset patch can now be proposed as a corrected-legacy candidate, but it should only be admitted after conservation-ledger reconciliation and a dedicated qualification gate. A separate P-enabled diagnostic path is also required before the `SuStdiorpo` runtime effect can be closed.