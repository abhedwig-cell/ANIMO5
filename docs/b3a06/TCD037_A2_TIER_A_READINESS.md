# TCD-037-A2 Tier-A admission readiness

Work unit: `ANIMO-B3A06`

Target: `TCD-037-A2`

## Decision

`TCD-037-A2` satisfies the Tier-A waiver predicate at readiness scope, subject to this workunit's exact-final-head CI remaining green.

Current review governance at closeout is `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`, whose exact-head workflow `34546470484` passed. GOV05 explicitly retains the GOV04 Tier-A waiver without weakening. Therefore the technical Tier-A predicate evaluated here is still the full GOV04 predicate, now consumed through GOV05 as current governance.

This is **not** scientific admission and does not grant the final Tier-A waiver. A later atomic admission decision must re-evaluate all applicable predicates on the then-current authorities and exact evidence pins.

## Atomic claim

A2 separates two different accepted-timestep CH4 observer quantities that legacy index 0 overloads:

- formation total: `F_CH4 = sum(QPrCH4(1:Nl) * St)`;
- atmosphere-boundary emission total: `E_CH4 = (QEmCH4Dif + QEmCH4Ebl + QEmCH4Flw + QEmCH4Plt) * St`.

They have different source ownership and may differ physically within one timestep because CH4 storage and oxidation lie between production and atmospheric transfer.

The only allowed reporting effects are:

- `Btom(CH4e)` from `E_CH4`;
- `Btom(CO2e)` only as the existing formation-side dissimilation complement from `F_CH4`.

No model-wide CO2-ledger closure is claimed.

## Exact accounting relations

The qualified source-shaped consumer relations are:

`Delta Btom(CH4e) = 10000 * E_CH4 / Cfracom`

`Delta Btom(CO2e) = D_OM - 10000 * F_CH4 / Cfracom`

where `D_OM` is the ordinary organic-matter dissimilation amount already owned by the balance calculation.

`ANIMO-SYNQ03` independently qualified the causal split with an exact-rational oracle. In the divergent case, formation and emission are deliberately unequal. In `FORMATION_ONLY`, formation is held fixed while emission is zero; the CO2e complement stays identical and CH4e changes. In `EMISSION_ONLY`, emission is held fixed while formation is zero; CH4e stays identical and CO2e changes. The equal-total control shows that numerical equality of the two amounts does not collapse their semantic ownership.

The synthetic evidence uses exact binary64-representable dyadic values and no empirical tolerance.

## Evidence strength and historical boundary

Synthetic evidence remains `B1_SYNTHETIC_NOT_B2`.

Natural active-GHG revision-53 coverage remains `BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH`. No testcase translation was performed.

Historical revision-53 executable behaviour remains exactly `UNKNOWN`. GOV03's historical-uncertainty route remains the only available route if A2 is later admitted.

## Tier-A predicate under GOV05

GOV05 retains the GOV04 Tier-A waiver without weakening and keeps `STRICTEST_APPLICABLE_RISK_TRIGGER_WINS`. At readiness scope all strengthened Tier-A conditions are PASS:

- exact source seam pinned;
- physical and accounting ownership unambiguous;
- atomic claim;
- exact accounting relations stated and satisfied;
- expected-difference contract pinned before B3A06 qualification;
- physical-state non-interference demonstrated;
- process-flux non-interference demonstrated;
- no numerical-policy change;
- no solver or tolerance change;
- no restart, initialization or state semantic change;
- no composition;
- no unresolved scientific or source-meaning ambiguity at A2 scope;
- reproducible validator available;
- scope guard available;
- natural activation unavailable for a documented lineage reason and purpose-built synthetic activation independently qualified for causality and scope;
- historical behaviour retained as `UNKNOWN` without B2;
- GOV03 route conditions retained;
- no production source, canonical register, B4 object or finalized governance snapshot modified.

The readiness record therefore reports `TIER_A_WAIVER_PREDICATE_PASS_AT_READINESS`.

B3A06 itself does not grant the final waiver. It also does not claim that an independent second-line review occurred. Under GOV05 Tier A, no separate review phase is required only because every retained GOV04 Tier-A waiver predicate passes. This is an applicability decision, not an independence claim.

## B3Q01 child binding

The finalized B3Q01 top-level schema is not changed. A later child disposition may use the parent lineage binding:

`tcd_ids: ["TCD-037"]`

while the exact canonical child identity remains `TCD-037-A2` in the child-scoped record/disposition carrier. No parent or sibling admission is implied.

## Governance transition consumed

At B3A06 branch creation, GOV05 was not yet qualified. Before closeout it advanced to `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904` and exact-head run `34546470484` succeeded. B3A06 therefore consumes GOV05 as current governance rather than freezing the earlier start-of-work observation.

The transition does not change the A2 scientific gates: GOV05 states that scientific evidence gates are not reduced and Tier A continues to use the full GOV04 waiver predicate.

## Hard boundaries

B3A06 performs no admission, grants no final waiver, changes no production source, changes no frozen B0 material, changes no canonical TCD register, reserves no new top-level TCD, admits no parent or sibling atom, composes no TCD-032..036 discrepancy, opens no B4, authorizes no production migration, updates no aggregate snapshot, claims no historical fidelity, promotes no B1 evidence to B2, translates no testcase and closes no full carbon ledger.

## Next workunit if qualified

`ANIMO-B3D22 — TCD-037-A2 CH4 Index-0 Formation/Emission Split Tier-A Atomic Admission Decision`
