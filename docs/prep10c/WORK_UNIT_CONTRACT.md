# ANIMO-PREP10C — Stable-DOM/DON/DOP plough event-reset corrected-legacy candidate

Status: `CANDIDATE_IMPLEMENTATION_AND_QUALIFICATION_IN_PROGRESS_NOT_ADMITTED`.

## Parent and scope

Parent branch: `work/animo-prep10-stable-dom-causal-activation`

Parent commit: `0a174fcee84865f027abab3dde491470c7a04afa`

This workunit follows the qualified PREP10 finding that revision-53 `Addit.for` reads `SuStdiorma`, `SuStdiorni` and `SuStdiorpo` before an explicit event-local definition and that the missing event reset has a reproducible causal numerical effect for stable DOM, DON and DOP under the current GNU diagnostic contract.

PREP10C creates and qualifies a minimal corrected-legacy **candidate** only. It does not admit corrected legacy, B3 or ANIMO5 production behaviour.

## Frozen identities

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank archive SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- frozen `ANIMO_4.1.5.53/Addit.for` SHA-256: `e3cf8f427e9a4b3743742039c89aae57864cb7268893e45797c7a17427dc8f5d`
- qualified diagnostic reset-counterfactual `Addit.for` SHA-256: `a1993aa2d22c8f2c13fc169e78f9121587c8f14a122ef7d3f757cc24a58a54ae`

Raw frozen artifacts remain outside public Git and must not be modified.

## Proposed atomic correction

At the start of each `Pl(I) > 0` event, before the stable-DOM/DON/DOP accumulation loop:

```fortran
SuStdiorma = 0.0
SuStdiorni = 0.0
If (Ipo.Eq.1) SuStdiorpo = 0.0
```

No governing equation, state definition, tolerance, precision policy, process order or public interface is intentionally changed.

The candidate is therefore provisionally treated as B3Q01 **Class B: local algebra/index/species correction**, specifically removal of stale event-local accumulator carryover that otherwise duplicates prior-event material in a later redistribution. Classification is not admission.

## Required evidence before candidate closeout

PREP10C must fail closed unless it records:

1. exact source-descendant identity and deterministic transform recipe;
2. proof that the candidate source transform is byte-identical to the already qualified PREP10 event-reset counterfactual for `Addit.for`;
3. current-GNU frozen-testbank non-interference across every case that can complete under the established diagnostic compatibility contract, with the known GHGMais lineage mismatch kept explicit;
4. causal-descendant convergence for the PREP10 DOM, DON and DOP activation cases;
5. conservation/redistribution reasoning for the plough operation and evidence that the reset removes stale cross-event mass rather than creating or deleting intended event mass;
6. exact changed and unchanged surfaces;
7. no use of arbitrary numerical tolerance to declare equivalence;
8. explicit historical-native/B2 status;
9. explicit independent-review gate status;
10. explicit non-admission until the applicable B3Q01 route is satisfied.

## Admission boundary

The B3Q01 framework requires more than a causal fix. PREP10C may finish as a qualified candidate while `corrected_legacy_admitted = false`.

Until a provenance-qualified B2 reference is available, or the documented historical-uncertainty route is legitimately opened after exhausted acquisition effort and independent second-line review, the B3 disposition remains fail-closed. A successful candidate test matrix must not be interpreted as B3 admission or B4 migration approval.
