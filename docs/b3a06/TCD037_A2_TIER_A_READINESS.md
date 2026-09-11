# TCD-037-A2 Tier-A admission readiness

Work unit: `ANIMO-B3A06`

Target: `TCD-037-A2`

## Decision

`TCD-037-A2` satisfies the Tier-A waiver predicate at readiness scope, subject to exact-final-head CI. Current review governance is `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`; its exact-head run `34546470484` passed. GOV05 explicitly retains the GOV04 Tier-A waiver without weakening and does not reduce scientific gates.

This is **not** scientific admission and does not grant the final Tier-A waiver. A later atomic admission decision must re-evaluate all applicable predicates on then-current authorities and evidence pins.

## Atomic claim

A2 separates two different accepted-timestep CH4 observer quantities that legacy index 0 overloads:

- `F_CH4 = sum(QPrCH4(1:Nl) * St)` — formation total;
- `E_CH4 = (QEmCH4Dif + QEmCH4Ebl + QEmCH4Flw + QEmCH4Plt) * St` — atmosphere-boundary emission total.

The only allowed reporting effects are `Btom(CH4e)` from `E_CH4` and `Btom(CO2e)` only as the existing formation-side dissimilation complement from `F_CH4`. No model-wide CO2-ledger closure is claimed.

## Exact accounting relations

`Delta Btom(CH4e) = 10000 * E_CH4 / Cfracom`

`Delta Btom(CO2e) = D_OM - 10000 * F_CH4 / Cfracom`

SYNQ03 independently qualified the causal split with an exact-rational oracle. The divergent, formation-only and emission-only controls discriminate the two owners; the equal-total control proves numerical coincidence does not imply semantic identity; rate-time equivalence and inactive controls bound the regression surface. Synthetic evidence uses exact binary64-representable dyadic values and no empirical tolerance.

## Evidence boundary

Evidence remains `B1_SYNTHETIC_NOT_B2`. Natural active-GHG revision-53 coverage remains `BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH`; no testcase translation was performed. Historical revision-53 executable behaviour remains `UNKNOWN`. GOV03's historical-uncertainty route remains the only available route if A2 is later admitted.

## Tier-A predicate under GOV05

GOV05 retains the complete GOV04 Tier-A waiver predicate and `STRICTEST_APPLICABLE_RISK_TRIGGER_WINS`. At readiness scope all required conditions are PASS: exact source seam; unambiguous ownership; atomicity; exact accounting relations; predeclared expected-difference contract; state and process-flux non-interference; no numerical, solver, tolerance, restart, initialization or state-semantic change; no composition; no unresolved A2 source-meaning ambiguity; reproducible validator and scope guard; independently qualified synthetic activation because natural activation is unavailable; historical behaviour held UNKNOWN; GOV03 route retained; and no production/register/B4/finalized-governance mutation.

B3A06 does not claim an independent second-line review occurred. For Tier A, no separate review phase is required because every retained waiver predicate passes. This is an applicability decision, not an independence claim.

## B3Q01 child binding

The finalized top-level schema remains unchanged. A later child disposition may use `tcd_ids: ["TCD-037"]` as parent lineage while the exact child identity remains `TCD-037-A2`. No parent or sibling admission is implied.

## Identifier collision checks

During closeout, `ANIMO-B3D22` was found allocated to the TCD-031 Tier-C formal-disposition lane. A subsequent live check found `ANIMO-B3D23` allocated to the TCD-031 GOV05 Tier-C admission lane. `ANIMO-B3D24` had no branch or open issue at the last check. B3A06 does not reserve B3D24; the later admission lane must recheck it live and use the next free identifier if necessary.

## Hard boundaries

No admission, final waiver, production-source change, frozen-B0 change, canonical-register change, new top-level TCD, parent/sibling admission, TCD-032..036 composition, B4, production migration, aggregate update, historical-fidelity claim, B1-to-B2 promotion, testcase translation or full carbon-ledger closure.

## Next workunit if qualified

Candidate after current collision checks:

`ANIMO-B3D24 — TCD-037-A2 CH4 Index-0 Formation/Emission Split Tier-A Atomic Admission Decision`
