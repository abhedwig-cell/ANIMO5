# ANIMO-B3D19 — TCD-038 GOV04 Tier-C Formal Disposition

Decision: `QUALIFIED_TIER_C_FORMAL_DISPOSITION_READY_FOR_SEPARATE_B3_ADMISSION_DECISION`.

This workunit records formal disposition only. It does **not** perform B3 admission, production patching, canonical STATE admission, TCD-039 composition, B4 opening, production migration, or central-regie integration.

## Authorities and live state

Authoring base: `ANIMO-RG05G@4551b6b4c3f987b1247571d59f8489b2f1a71ba6`.

Readiness: `ANIMO-B3B09@1b47d6b2e422463b557a48355ad8b4f5bed70ebc`.

Independent second-line review: `ANIMO-B3B09R@c6fcd47f4fb4c0277fa27860ee66dc83a449a038`, result `PASS`, workflow run `34528522077`, job `103043260093`.

GOV04: `1bbe4c211197590f346803106e45dca5faae79fc`; GOV03: `cbd262bdabe92923113b7326f2f42822ce9a971c`; B3Q01: `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`; canonical B3I03 register: `814ea660d367494432beb63ea78298d1f6cd73d7`.

Immediately before branch creation no `ANIMO-B3D19`, no later dedicated TCD-038 disposition/admission branch, and no RG05H aggregate were found. Issue #47 contains the independent PASS closeout and is closed `completed`.

## Scientific disposition

The independently reviewed lifecycle has one persistent coordinate for cumulative actual crop uptake. Accepted/current aliases are `Amplni_act` and, when phosphorus is active, `Amplpo_act`. Result/serialized aliases are `Rsamplni_act` and `Rsamplpo_act`.

The scientifically consistent initialization direction is:

`Rsampl*_act -> Ampl*_act`

before process execution. Frozen revision-53 instead can copy `Ampl*_act -> Rsampl*_act` after the existing threshold handling and thereby erase represented above-threshold imported actual uptake before the first process interval.

The bounded correction is limited to restoring `Amplni_act = Rsamplni_act` before the existing nitrogen threshold statement and restoring `Amplpo_act = Rsamplpo_act` within `Ipo.Eq.1` before the existing phosphorus threshold statement. The existing crop trigger, `1.0d-4` small-value rule and `Ipo.Eq.1` phosphorus guard remain unchanged.

The checkpoint representation is not redefined. The correction changes only restore semantics at the existing initialization surface. No new state, numerical policy, solver rule, tolerance, or precision rule is introduced. Potential uptake is outside scope and remains owned by TCD-039; no TCD-039 composition is permitted here.

## B3 class and GOV04 risk tier

B3 qualification class remains `B_LOCAL_ALGEBRA_INDEX_SPECIES`. The source correction is local and bounded even though its effect can propagate downstream through crop uptake and nutrient demand.

GOV04 risk tier remains `C` under the strictest-trigger-wins rule. Applicable Tier-C triggers are `RESTART_OR_COLD_START_DISCRIMINATION`, `INITIALIZATION_SEMANTICS`, and `CHECKPOINT_SEMANTICS`.

The required independent Tier-C second-line review has passed. No Tier-D trigger was found. GOV04 separation is retained: this formal disposition does not combine the subsequent B3 admission decision.

## Historical uncertainty

No qualified B2 authority for TCD-038 exists. GOV03 therefore remains authoritative for the historical-uncertainty route:

- `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`;
- `ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS`.

Historical revision-53 native manifestation remains exactly `UNKNOWN_WITHOUT_B2`. GNU diagnostic evidence is not historical B2 and this disposition makes no historical-fidelity claim.

## Expected-difference boundary

For applicable above-threshold imported state, accepted actual N/P uptake may now retain the serialized state rather than being erased before first process execution. Causally downstream crop uptake, nutrient demand, nutrient state, fluxes, balances and outputs may therefore differ.

This workunit does not qualify full-horizon difference magnitude, field prevalence, whole-model equivalence, or any arbitrary numerical tolerance. It does not change the crop trigger, small-value threshold, phosphorus applicability, potential-uptake semantics, checkpoint layout, solver/tolerance policy, precision policy, frozen B0 identity, or unrelated process behavior.

## Residual uncertainty and next gate

Residual uncertainty remains around historical Intel/native manifestation, the absence of a TCD-038-specific causally isolated full continuous-versus-split trajectory, full-horizon downstream magnitude, and the separate unresolved TCD-039 potential-uptake restart question.

Formal disposition:

`HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY`

Admission route:

`INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY`

Next allowed workunit after successful machine validation:

`SEPARATE_TIER_C_B3_ADMISSION_DECISION_FOR_TCD038`
