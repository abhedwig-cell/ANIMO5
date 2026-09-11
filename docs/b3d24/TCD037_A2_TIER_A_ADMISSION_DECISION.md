# TCD-037-A2 GOV05 Tier-A atomic B3 admission decision

Work unit: `ANIMO-B3D24`

Target: `TCD-037-A2`

## Decision

Subject to exact-final-head CI, admit only canonical child atom `TCD-037-A2` with formal disposition:

`HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY`

and bounded decision:

`ADMIT_TCD037_A2_CH4_INDEX0_FORMATION_EMISSION_SPLIT_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_A_WAIVER`.

The parent `TCD-037` and siblings A1, A3 and A4 are not admitted by this decision. A1 retains its already-existing separate atomic admission.

## Scientific object

The admitted observer semantics are exactly:

`F_CH4 = sum(QPrCH4(1:Nl) * St)`

for the existing formation-side organic-matter dissimilation complement, and

`E_CH4 = (QEmCH4Dif + QEmCH4Ebl + QEmCH4Flw + QEmCH4Plt) * St`

for atmosphere-boundary CH4 emission.

The admitted reporting relations are:

`Delta Btom(CH4e) = 10000 * E_CH4 / Cfracom`

`Delta Btom(CO2e) = D_OM - 10000 * F_CH4 / Cfracom`

Only `Btom(CH4e)` and the existing formation-side `Btom(CO2e)` complement are within the expected-difference surface. No model-wide CO2-ledger closure is admitted or implied.

## Evidence and uncertainty

RUNTIMEQ03 establishes the source owners and the semantic collision. SYNQ03 independently qualifies synthetic causality and scope using exact-rational oracle arithmetic and exact binary64 dyadic cases. B3A06 re-evaluates the complete Tier-A predicate at readiness and its exact-final workflow run `34547418205` passes on `466718167b22a643b26ee5035a18514987b6e289`.

Evidence strength remains `B1_SYNTHETIC_NOT_B2`. The natural revision-53 active-GHG route remains `BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH`; no testcase translation was performed. Historical revision-53 executable behaviour remains `UNKNOWN`.

## GOV05 / Tier-A waiver

Current governance is `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`. GOV05 retains the GOV04 Tier-A waiver without weakening and reduces no scientific evidence gate.

B3D24 re-evaluates every retained Tier-A condition for the exact A2 admission object. All are PASS, including atomicity, exact source/accounting ownership, accounting relations, predeclared expected difference, state/flux non-interference, no numerical/solver/restart/state-semantic change, no composition, no unresolved A2 source-meaning ambiguity, validator/scope guard, independently qualified purpose-built synthetic activation, explicit UNKNOWN history and GOV03 route retention.

Therefore the final Tier-A waiver is granted for `CANONICAL_CHILD_ATOM:TCD-037-A2` only.

No independent second-line review is claimed. In the B3Q01-compatible disposition the review evidence is `INCOMPLETE / NOT_REVIEWED / independent=false`, while the review gate is `PASS / NOT_APPLICABLE` because the Tier-A waiver applies. This is an applicability statement, not an independence claim.

## Child-carrier binding

The B3Q02 formal carrier retains `TCD-037` only as top-level lineage and binds the actual decision to `CANONICAL_CHILD_ATOM:TCD-037-A2`. It does not admit the parent, reserve a new TCD, append the top-level register or authorize production migration.

## Hard boundaries

No production source or frozen B0 is modified. No A3/A4 admission, TCD-032..036 composition, canonical-register mutation, new top-level TCD, B4 authorization, production migration, historical-fidelity claim, B1-to-B2 promotion, testcase translation or whole-model CO2-ledger claim occurs.

## Central aggregation

Atomic admission authority is distinct from the latest aggregate snapshot. `ANIMO-RG05H` remains the pinned aggregate authority during this workunit. After B3D24 exact-final qualification, live aggregation cadence must be re-evaluated because other atomic admission work may be proceeding concurrently. This workunit itself does not create RG05I.
