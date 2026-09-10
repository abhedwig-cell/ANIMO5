# TCD-037-A1 CH4 layer-formation observer — GOV04 Tier-A atomic admission decision

Work unit: `ANIMO-B3D21`

Decision:

`ADMIT_TCD037_A1_CH4_LAYER_FORMATION_OBSERVER_WITH_HISTORICAL_UNCERTAINTY_GOV04_TIER_A_WAIVER`

Disposition:

`HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY`

## 1. Decision object

This decision applies only to canonical child atom `TCD-037-A1` under top-level lineage parent `TCD-037`.

The atom is the layer CH4 formation observer input in the active GHG CH4/CO2 formation-partition path. Its source-owned accepted-timestep amount is:

`QPrCH4(Ln) * St`

The parent TCD remains compound. Admission of A1 does not admit parent `TCD-037`, A2, A3, A4, or any other GHG discrepancy.

## 2. Authority recheck

B3D21 starts from exact qualified readiness authority:

`ANIMO-B3A05@5915333feed06e0c03280cb8fdfeff8dd1be9e9a`

with exact-final workflow `34538944794 = completed/success`.

The admission also binds:

- `ANIMO-RG05H@3e4247928bb43f30def951fa8804560636affbef`;
- `ANIMO-B3I07@54679c7555a963133dfd686648af334f479c5808`;
- `ANIMO-RUNTIMEQ03@a3e822f8e97fe1312a7dfa73601a49ae7375163e`;
- `ANIMO-SYNQ02@1975eda3586d79033be6af745994bb6181a825fc`, exact-final workflow `34538344680 = completed/success`;
- `ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121`;
- `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`;
- `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`;
- `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- `ANIMO-B3Q02@1db63b17cb5f48cbd8ae28116a2e716b4bdaadf3`.

No later B3D21 or RG05I authority existed at branch start.

## 3. Why the strictest GOV04 tier is A

The previously compound parent contained unresolved observer ownership and index-0 semantic collisions. B3I07 separated those claims. At A1 scope there is no remaining restart, initialization, persistent-state, checkpoint, numerical-policy, solver, tolerance, exact-zero, singular-domain, composition or production-bound trigger.

A1 changes only a bounded accounting/reporting observer. Its physical producer `QPrCH4` is not redefined and its trajectory is not changed. Consequently no Tier B, Tier C or Tier D trigger is applicable to this atomic object.

## 4. Final Tier-A waiver decision

B3D21 re-evaluates all GOV04 Tier-A waiver conditions rather than inheriting the B3A05 conclusion automatically. The machine-readable waiver audit records every condition as PASS.

The critical activation condition is satisfied through the GOV04 alternative route: the absence of a reasonably available natural active-GHG revision-53 case is documented, and SYNQ02 is a purpose-built activation independently qualified for causality and scope. Its evidence strength remains B1 synthetic; it is never promoted to B2.

Therefore a separate independent second-line review is waived for this exact atom. In B3Q01-compatible representation:

- the independent-review evidence result is `NOT_REVIEWED`;
- no independence is claimed;
- the independent-review gate is `PASS / NOT_APPLICABLE`;
- the gate cites GOV04 and the exact B3D21 waiver audit.

The waiver is invalid outside `CANONICAL_CHILD_ATOM:TCD-037-A1` and becomes invalid if any source pin, claim, scope or evidence identity changes.

## 5. Historical uncertainty route

No qualified B2 historical executable reference exists. GOV03 has closed the reasonable acquisition route and made the G6U historical-uncertainty route eligible subject to claim-scoped B3 requirements.

Historical revision-53 behaviour therefore remains exactly:

`UNKNOWN`

The admission does not claim that the historical executable used `QPrCH4(Ln)*St`, nor does it claim equivalence to an unavailable historical executable. The scientific basis is the source-qualified accounting ownership plus the exact independently cross-checked accounting identity.

## 6. Exact accounting identity

For each active non-degenerate layer:

`M_CH4 = 10000 * QPrCH4(Ln) * St / Cfracom`

`Btot = Ffom + Fahu + Fdom`

`CH4_i = F_i / Btot * M_CH4`

`CO2_i = F_i - CH4_i`

with exact identities:

`sum_i(CH4_i) = M_CH4`

and

`sum_i(CH4_i + CO2_i) = Btot`.

SYNQ02 independently checks these with exact rational arithmetic and deterministic O0/O2 execution for the qualified synthetic values.

## 7. Expected difference and non-interference

The admitted scientific change surface is exactly six observer fields:

- `Bfom(CH4f)`;
- `Bahu(CH4f)`;
- `Bdom(CH4f)`;
- `Bfom(CO2f)`;
- `Bahu(CO2f)`;
- `Bdom(CO2f)`.

No change is admitted for physical model state, GHG process fluxes, restart/checkpoint state, solver state, tolerances, numerical policy, unrelated observers, A2/A3/A4, or TCD-032..036.

This is a scientific B3 admission object only. There is still no production implementation in scope.

## 8. Child carrier

B3D21 uses B3Q02 `FORMAL_DISPOSITION` mode. The embedded B3Q01 disposition retains:

`tcd_ids = ["TCD-037"]`

only as lineage. Its actual atomic target is bound by:

`decision_scope = CANONICAL_CHILD_ATOM:TCD-037-A1`

The carrier records `atom_admitted=true` while `parent_admitted=false`, with no canonical-register append, no new top-level TCD and no production migration.

## 9. Admission result

All claim-scoped B3 gates PASS, including the GOV04-waived independent-review applicability gate. B3D21 therefore admits `TCD-037-A1` into B3 under historical uncertainty.

This admission is authoritative from the qualified atomic B3D21 record. It need not wait for the next aggregate snapshot. GOV04 batching still applies: this single admission does not by itself justify RG05I because canonical routing, B3 completeness, B4 eligibility and production eligibility are unchanged.

## 10. Boundaries after admission

After this decision:

- `TCD-037-A1 = ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY`;
- parent `TCD-037 = NOT_ADMITTED_AS_A_COMPOUND_PARENT`;
- A2, A3 and A4 remain not admitted;
- historical revision-53 behaviour remains `UNKNOWN`;
- no B4 gate opens;
- no production migration is authorized;
- no production source is changed;
- no cross-TCD composition is qualified.

The next sibling work must be selected independently from live A2 evidence and routing; A1 admission must not be used as a shortcut for A2/A3/A4.