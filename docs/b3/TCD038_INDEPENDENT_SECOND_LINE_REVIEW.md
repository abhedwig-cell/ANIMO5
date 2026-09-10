# ANIMO-B3B09R - Independent Second-Line Review of TCD-038

Decision: `PASS`.

This is GOV04 Tier-C independent second-line review evidence only. It is not B3 admission, canonical STATE admission, composition, B4 authorization, production migration, or central-regie integration.

## Live pre-write reconciliation

The clean review branch was rechecked immediately before writing and was still exactly at `ANIMO-B3B09@1b47d6b2e422463b557a48355ad8b4f5bed70ebc`. Issue #47 had no review comments. No later dedicated TCD-038 branch, issue, evidence workunit, or review was found.

Current aggregate authority is `ANIMO-RG05G@4551b6b4c3f987b1247571d59f8489b2f1a71ba6`. RG05G admits TCD-030, TCD-023 and TCD-028 only. It neither admits nor changes TCD-038.

The handoff readiness workflow was independently rechecked: run `34524511092`, job `103029989632`, head `1b47d6b2e422463b557a48355ad8b4f5bed70ebc`, conclusion `success`. This establishes readiness-package integrity only, not the second-line scientific conclusion.

## Independent source and lifecycle reconstruction

Frozen B0 remains source SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566` and testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

The source-bound restart inventory and PREP10 evidence establish one lifecycle coordinate, with accepted/current aliases `Amplni_act` and conditional `Amplpo_act`, and result/serialized aliases `Rsamplni_act` and conditional `Rsamplpo_act`. `input1.for` reads the result-side aliases from `>orgpla:`. Ordinary `Init.for` restores result-side state into accepted state. Uptake integration advances result-side state from accepted state. `Output_Init.for` writes the result-side actual uptake back to `>orgpla:`.

The only direction consistent with that lifecycle is therefore:

`Rsampl*_act -> Ampl*_act`

at initialization before process execution.

The frozen `Inicalc.for` seam instead applies the existing threshold and then copies `Ampl*_act -> Rsampl*_act` without first restoring an above-threshold serialized value. PREP10's source-bound diagnostic evidence naturally reaches this seam in four unmodified cases and observes nonzero input actual N/P uptake becoming zero immediately after `Inicalc`. A minimal diagnostic direction probe preserves the supplied values. This is causal B1/source-bound diagnostic evidence, not B2.

## Scope and semantics

The bounded candidate identity is only the missing read-to-accepted assignment before the existing logic. The existing crop trigger remains `Kicr(1).Ne.6 .Or. (Kicr(1).Eq.6 .And. Ioptcu.Eq.1)`. The existing `1.0d-4` small-value rule remains unchanged. P remains guarded by `Ipo.Eq.1`.

The `>orgpla:` representation is shared by ordinary initialization and serialized continuation, with no separate restart discriminator on this path. The candidate therefore changes restore semantics, not representation. Zero and sub-threshold input behavior remains unchanged. On the applicable path, represented above-threshold cumulative actual uptake is preserved rather than erased.

TCD-039 is fully excluded. It concerns potential uptake state that has no restart representation. This review adds no potential-uptake field, changes no checkpoint layout, and does not claim that TCD-038 alone establishes complete crop restart continuity.

## GOV04 classification

B3 qualification class remains `B_LOCAL_ALGEBRA_INDEX_SPECIES`, because the bounded correction is a local assignment-direction correction and adds no state representation, physics model, numerical policy, solver rule, tolerance, or precision rule.

GOV04 risk tier is nevertheless `C`. Under `STRICTEST_APPLICABLE_RISK_TRIGGER_WINS`, restart/cold-start discrimination, initialization semantics and checkpoint/restore semantics are Tier-C triggers. A Tier-B review route would therefore be invalid.

## STATE evidence and later routing

STATEQ01 is retained as state/route context only. It is not promoted to a causally isolated TCD-038 split-run proof.

The later live STATEQ02 closeout is `cb7c23524df6560e65a5bdc1ed19e0b6e3bd46c6`. It strengthens restricted-core exact split-run evidence, but its profile explicitly excludes the external crop surface and unresolved internal crop restart state. It therefore neither proves nor contradicts TCD-038. B3I04 preserves that boundary and performs no new admission.

Later B3I05 and B3I06 routing concerns TCD-042/upper-boundary hazards and does not supersede TCD-038. No material contradictory or superseding TCD-038 evidence was found.

## Expected difference and non-interference

The first expected difference is exact and local: for an applicable above-threshold imported state, accepted `Ampl*_act` retains the represented input instead of being erased before first process execution. Causally downstream crop uptake, nutrient demand and dependent nutrient states, fluxes or outputs may consequently differ.

No field-scale magnitude, whole-trajectory equivalence, prevalence estimate or tolerance is inferred. PREP10's downstream diagnostic differences demonstrate material reach beyond accounting, but they are not acceptance tolerances.

The review changes no production source, frozen B0, canonical TCD register, canonical STATE object, central aggregate, numerical policy, solver, tolerance, or checkpoint representation. It does not open B4 or production migration.

## Evidence-strength boundary

PREP10 remains `DIAGNOSTIC_NOT_REFERENCE_PLUS_SOURCE_BOUND`. PREP12 is a provenance-preserving rehome and adds no scientific strength. STATEQ01 and STATEQ02 are not promoted beyond their qualified scopes. No qualified B2 authority for TCD-038 was found, and GNU diagnostic execution is not treated as historical B2.

Therefore historical revision-53 native behavior remains exactly:

`UNKNOWN_WITHOUT_B2`.

Residual uncertainty remains around historical native manifestation, a TCD-038-specific causally isolated full split-run trajectory, and full-horizon downstream magnitude.

## Second-line disposition

All claim-scoped Tier-C review questions pass without requiring TCD-039 composition, new state representation, numerical-policy change, solver/tolerance change, checkpoint-layout change, evidence promotion, or a stronger historical claim.

Final second-line result:

`PASS_INDEPENDENT_REVIEW_EVIDENCE_ONLY_NO_B3_ADMISSION`

A separate Tier-C disposition/admission decision is still required if central regie chooses to proceed.
