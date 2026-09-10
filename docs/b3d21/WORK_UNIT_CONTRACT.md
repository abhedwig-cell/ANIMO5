# ANIMO-B3D21 — TCD-037-A1 CH4 Layer Formation Observer GOV04 Tier-A Atomic Admission Decision

Status at authoring: `ATOMIC_ADMISSION_DECISION_ONLY`

## Purpose

Make the bounded B3 disposition/admission decision for canonical child atom `TCD-037-A1` after `ANIMO-B3A05` qualified all GOV04 Tier-A waiver predicates at readiness scope.

This workunit must re-evaluate the complete Tier-A predicate against exact live/pinned authorities. If every predicate remains PASS, it may record the GOV04 independent-second-line-review waiver and admit only child `TCD-037-A1` under historical uncertainty.

## Exact starting point

`ANIMO-B3A05@5915333feed06e0c03280cb8fdfeff8dd1be9e9a`

B3A05 exact-final workflow:

`34538944794` — expected `completed/success` on the exact head above.

## Required authorities

- aggregate: `ANIMO-RG05H@3e4247928bb43f30def951fa8804560636affbef`
- canonical routing: `ANIMO-B3I07@54679c7555a963133dfd686648af334f479c5808`
- runtime semantics: `ANIMO-RUNTIMEQ03@a3e822f8e97fe1312a7dfa73601a49ae7375163e`
- independent synthetic activation: `ANIMO-SYNQ02@1975eda3586d79033be6af745994bb6181a825fc`
- SYNQ02 exact-final workflow: `34538344680` — expected `completed/success`
- synthetic evidence policy: `ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121`
- review governance: `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`
- historical uncertainty route: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`
- B3 disposition framework: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`
- child-atom carrier governance: `ANIMO-B3Q02@1db63b17cb5f48cbd8ae28116a2e716b4bdaadf3`

## Exact atomic claim

`TCD-037-A1` is limited to the active GHG layer CH4/CO2 formation-partition observer in `Outbal_calc`.

The accounting owner is:

`QPrCH4(Ln) * St`

for each active soil layer `Ln=1..Nl`.

The only admissible changed reporting surface is:

- `Bfom(CH4f)`
- `Bahu(CH4f)`
- `Bdom(CH4f)`
- `Bfom(CO2f)`
- `Bahu(CO2f)`
- `Bdom(CO2f)`

No physical state, process flux, restart/checkpoint state, solver state or numerical-policy quantity may change under this admission.

## Child-carrier rule

The formal disposition must use the additive B3Q02 `FORMAL_DISPOSITION` carrier. The embedded B3Q01 record uses `tcd_ids: ["TCD-037"]` as lineage only and binds the actual decision through exact scope:

`CANONICAL_CHILD_ATOM:TCD-037-A1`

Admission of A1 must not imply admission of parent `TCD-037` or siblings A2, A3 or A4.

## Historical uncertainty

No qualified B2 historical executable reference exists. Historical revision-53 behaviour remains exactly `UNKNOWN`. The only available route is:

`INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY`

SYNQ02 remains `B1_SYNTHETIC_NOT_B2` and is used only as independently qualified causal/coverage evidence under the GOV04 Tier-A synthetic-activation alternative.

## GOV04 Tier-A waiver

A separate independent second-line review may be omitted only if every GOV04 Tier-A condition remains PASS. The final waiver audit is part of B3D21. If any condition is false or unknown, this workunit must fail closed and must not admit A1.

When the waiver passes, the B3Q01 independent-review evidence block must use `result: NOT_REVIEWED`, must not claim independence, and the independent-review gate must be `PASS` with applicability `NOT_APPLICABLE` and an explicit GOV04 waiver reference.

## Hard boundaries

B3D21 must not:

- modify production source;
- modify frozen B0 source/testcases;
- admit parent `TCD-037`;
- admit A2, A3 or A4;
- compose A1 with any sibling or TCD-032..036;
- modify the canonical top-level TCD register;
- reserve a new top-level TCD;
- change B3Q01/B3Q02/GOV03/GOV04 governance artifacts;
- open B4;
- authorize production migration;
- create or update RG05I merely for this single atomic admission;
- claim historical fidelity or promote B1 synthetic evidence to B2.

## Allowed PASS result

If every gate remains qualified, the exact disposition is:

`HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY`

and the bounded decision is:

`ADMIT_TCD037_A1_CH4_LAYER_FORMATION_OBSERVER_WITH_HISTORICAL_UNCERTAINTY_GOV04_TIER_A_WAIVER`

The workunit stops after the exact-head atomic admission is qualified. Central aggregation remains governed by GOV04 batching.