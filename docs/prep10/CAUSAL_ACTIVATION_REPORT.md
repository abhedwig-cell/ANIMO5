# ANIMO-PREP10 — Stable-DOM/DON/DOP causal activation report

Status: `QUALIFIED_SOURCE_DEFECT_AND_CURRENT_GNU_CAUSAL_EFFECT_FOR_STABLE_DOM_DON_AND_DOP_HISTORICAL_NATIVE_OPEN`.

## Starting point

The exact revision-53 `Addit.for` source has already been qualified as reading `SuStdiorma`, `SuStdiorni` and `SuStdiorpo` in their first plough-branch assignments without an explicit preceding definition or event reset.

The unmodified frozen testbank remains non-discriminating for this defect under the current GNU diagnostic build because the successful frozen plough cases begin with zero stable-DOM/DON/DOP activation. Controlled diagnostic descendants were therefore used. They are not B0 and are not scientific reference cases.

## CranMais DOM and DON activation

Frozen CranMais `Input/Initial.inp` SHA-256:

`8df3d78e830f344bc315d4dff2ae4c1ee4d6e959a07ba7d112e4105e6fbbb201`

`tools/make_prep10_causal_initial.py` creates deterministic descendants and rejects any different parent hash. The single-species probes used were:

- DOM: `CoStdiorma(1:2) = 1.0E-2`, descendant SHA-256 `d66acd69d62c2cfded22d581048a25b365b81d9972aa1a3a31fd55047d712f04`;
- DON: `CoStdiorni(1:2) = 1.0E-3`, descendant SHA-256 `a3e1349bba096d769438e62635f9408046d858c611ebdf5decb498afd1f30455`.

CranMais has `PhosphorusCycle=0`, so its DOP-only descendant remains a useful negative control but cannot exercise `SuStdiorpo`.

### Observer carryover

Under GNU Fortran 14.2.0 with the existing diagnostic contract including `-fno-automatic`, the first CranMais plough event left:

- `SuStdiorma = 2.1670933665864016E-06`;
- `SuStdiorni = 2.1670933665864018E-07`.

Exactly those values were present immediately before the second plough event. The observer build itself produced no scientific output differences relative to the baseline after declared volatile-only normalization.

### Event-reset counterfactual

A diagnostic counterfactual resets the three stable-DOM plough accumulators to zero at the start of each plough event. It is not an admitted correction.

For DOM-only activation, baseline and reset differ in 16 scientific output files. In the final stable-DOM restart vector:

- baseline sum: `6.136175457677E-05`;
- reset sum: `1.3633400418508182E-05`;
- baseline minus reset: `4.772835415826182E-05`;
- baseline/reset ratio: `4.500840046733142`.

For DON-only activation, the same 16 scientific output files are discriminating. In the final stable-DON restart vector:

- baseline sum: `6.136069957677E-06`;
- reset sum: `1.3632378235187933E-06`;
- baseline minus reset: `4.7728321341582064E-06`;
- baseline/reset ratio: `4.501100139547595`.

No numerical tolerance was used to convert a difference into a match.

## Phosphorus-enabled stable-DOP activation

To close the current-GNU DOP gate without changing the frozen CranMais phosphorus switch, PREP10 uses the already provenance-pinned frozen testcase `LWKM_gras_1040.2021.2045`.

Relevant frozen identities are:

- `input/INITIAL.INP`: SHA-256 `0e6bb1d30c46c3aa8c7dcd077c06845afebcb6bd8b576c0df24e037382dfa483`;
- `input/GENERAL.INP`: SHA-256 `e511f8a222f2e12959683429fb31008a420856aa476e578a1fe2e6b525914120`;
- `input/Management.inp`: SHA-256 `bbfa83721eaaa7deb23d4d09f7f263964ba842a917ef6d4d58454e56f7309493`.

This testcase has `PhosphorusCycle=1`. The successful current-GNU run observes four plough events.

`tools/make_prep10_lwkm_p_causal_initial.py` accepts only the exact frozen LWKM initial-state parent. It changes only `CoStdiorpo` indices 1 and 2 from zero to `1.0E-4`. The resulting diagnostic descendant SHA-256 is:

`1efe16d5e8c3e685ad22168132da4ffa789c4f982e8c178640a97fff14fd4e48`

The activation value is selected for causal observability only. No physical calibration claim is made.

### DOP observer carryover

At the first LWKM plough event:

- before: `SuStdiorpo = 0`;
- after: `SuStdiorpo = 3.0585643629036948E-12`.

Immediately before the second plough event:

- `SuStdiorpo = 3.0585643629036948E-12`.

The later observed values remain carried between events as well. The observer run was scientifically non-interfering: of 55 generated output files, 47 were raw-equal and 8 became equal after declared volatile-only normalization, with zero scientific differences.

### DOP baseline versus event reset

Baseline and event-reset runs both completed through the established GNU diagnostic path. After declared volatile-only normalization, 11 generated scientific files differ:

- `ani_pGP.Bal`;
- `ani_pRP.Bal`;
- `ani_pTP.Bal`;
- `bapoGP.Out`;
- `bapoRP.Out`;
- `bapoTP.Out`;
- `discharge.out`;
- `initial.out`;
- `transfopGP.Out`;
- `transfopRP.Out`;
- `transfopTP.Out`.

In the final stable-DOP restart vector:

- baseline sum: `1.7192446562370895E-08`;
- reset sum: `1.7191897420234135E-08`;
- baseline minus reset: `5.491421367604038E-13`;
- baseline/reset ratio: `1.000031941915621`;
- maximum absolute layer difference: `1.5200000000006317E-13`.

The DOP numerical effect is much smaller than the deliberately stronger CranMais DOM/DON activation, but it is reproducible, survives volatile-only normalization, and is directionally tied to the event-reset counterfactual.

## Qualification conclusion

The current-GNU causal gate is now closed for all three accumulator species:

- source-level use-before-definition: qualified for `SuStdiorma`, `SuStdiorni`, `SuStdiorpo`;
- current GNU causal effect: qualified for stable DOM, stable DON and stable DOP;
- observer-only transform noninterference: qualified for the exercised diagnostic paths;
- historical Intel manifestation: still open;
- physical representativeness of activation values: not claimed;
- diagnostic outputs: not reference outputs;
- reset counterfactual: not a corrected-legacy admission;
- B0 source and testcase bytes: unchanged.

Machine-readable evidence is split between:

- `integration/animo-prep/PREP10_STABLE_DOM_CAUSAL_ACTIVATION.json` for CranMais DOM/DON;
- `integration/animo-prep/PREP10_STABLE_DOP_CAUSAL_ACTIVATION.json` for phosphorus-enabled LWKM DOP;
- `integration/animo-prep/ANIMO-PREP10_STATUS.json` for the workunit decision.

## CI and evidence boundary

Public GitHub Actions validates the source scanners, deterministic input-transform tools, machine-readable JSON and synthetic GNU local-storage probe. Restricted/private B0 archives are intentionally not uploaded to public CI. The actual causal model runs were executed in the authoring environment against locally supplied exact B0 bytes and are hash-bound in the machine-readable evidence.

## Next gate

PREP10 should not silently turn this diagnosis into a production fix. The next meaningful step is a separate corrected-legacy candidate workunit for the minimal event reset, with exact source-descendant identity, frozen-testbank noninterference checks, causal-descendant convergence to the qualified reset counterfactual, conservation-ledger reconciliation, and an explicit no-reference/no-migration boundary until the historical-reference gate is resolved.