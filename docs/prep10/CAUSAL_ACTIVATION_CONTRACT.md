# ANIMO-PREP10 — Stable-DOM causal activation gate

Parent checkpoint: `d728496cd72ba1a2e20a5f0cd731b3800b72f4a6` on `work/animo-prep10-stable-dom-plough-accumulators`.

Branch: `work/animo-prep10-stable-dom-causal-activation`.

## Purpose

This continuation tests whether the already qualified revision-53 source-level use-before-definition of `SuStdiorma`, `SuStdiorni` and `SuStdiorpo` can be made numerically discriminating by a controlled diagnostic descendant of the frozen CranMais input.

The experiment is diagnostic only. It does not modify B0, does not create a reference output, does not admit corrected legacy, and does not admit ANIMO5 production migration.

## Frozen identities

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank archive SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- CranMais frozen `Input/Initial.inp` SHA-256: `8df3d78e830f344bc315d4dff2ae4c1ee4d6e959a07ba7d112e4105e6fbbb201`

## Controlled diagnostic descendants

The only intended scientific-input changes are to the `>sdomin:` vectors at compartment indices 1 and 2. Three single-species probes are defined:

- DOM probe: `CoStdiorma(1:2) = 1.0E-2`, DON and DOP unchanged at zero;
- DON probe: `CoStdiorni(1:2) = 1.0E-3`, DOM and DOP unchanged at zero;
- DOP negative-control probe: `CoStdiorpo(1:2) = 1.0E-4`, DOM and DON unchanged at zero.

All values are within the revision-53 input validator range `[0,10]`. These values are chosen to activate the code path, not as a calibrated or physically representative CranMais state.

CranMais has `PhosphorusCycle=0`; therefore the DOP probe is a negative control for this testcase and cannot qualify the `SuStdiorpo` runtime effect.

## Execution contract

Use the existing GNU diagnostic build contract, including `-fno-automatic`. Compare:

1. unmodified diagnostic source behavior;
2. observer-only `Addit.for` working-copy transform;
3. reset counterfactual that assigns the stable-DOM plough accumulators to zero at the start of every plough event.

The reset build is a diagnostic counterfactual only. It is not a correction admission.

Comparisons must normalize only the previously declared volatile timestamp and CPU metadata. No numerical tolerance may convert a difference into a match.

## Qualification rule

The DOM or DON source defect is dynamically causally activated under the current GNU diagnostic contract only if all of the following hold:

- the frozen parent input identity is verified before transformation;
- the transform is deterministic and hash-recorded;
- both baseline and reset-counterfactual runs complete through the established CranMais diagnostic path;
- observer output demonstrates accumulator carryover between plough events;
- baseline and reset-counterfactual scientific outputs differ after declared volatile-only normalization;
- the same frozen-input case without the activating transform remains non-discriminating, as already established by the parent PREP10 checkpoint.

The historical Intel runtime effect remains open until a provenance-qualified native reference becomes available.