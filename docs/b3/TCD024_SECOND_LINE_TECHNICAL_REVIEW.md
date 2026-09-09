# TCD-024 second-line technical review

Work unit: `ANIMO-B3B03R`

Target: `TCD-024`

Candidate reviewed: `work/animo-b3b03-tcd024-slow-langmuir-index-readiness` at `446f57f3aeff6e7db56ce473f0724bdb58cad94f`.

## Disposition

Technical result:

`PASS_TCD024_ATOMIC_CLASS_B_READINESS_TECHNICALLY_RECONFIRMED`

Governance result:

`UNRESOLVED_NOT_ADMITTED_INDEPENDENT_SECOND_LINE_AND_VALID_ADMISSION_ROUTE_STILL_REQUIRED`

This workunit does not claim the B3Q01 independent-second-line gate. It is executed from the same ChatGPT authoring context as ANIMO-B3B03. Re-reading pinned authorities and rerunning fail-closed checks can strengthen the technical record, but cannot create genuine reviewer independence.

## 1. Reviewed atomic claim

The reviewed claim remains one local index correction in frozen revision-53 `Transorp.for`, `Conc_unl`.

Legacy expression:

```fortran
Yy = One + Parcxsl(3,I) * Avc
```

Candidate atomic expression:

```fortran
Yy = One + Parcxsl(3,J) * Avc
```

`I` is the nonlinear trial counter, `J` is the slow-sorption-site counter. The outer trial domain is `1..20`; the site domain is bounded by `Ncxsl` and `Macx=3`. No numerical-policy or constitutive-model change is part of this review.

Result: `PASS`.

## 2. Frozen and canonical identity review

ANIMO-B3B03 pins the frozen B0 source ZIP to:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

and the supplied testbank ZIP to:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

The frozen `ANIMO_4.1.5.53/Transorp.for` member is pinned to:

`65ab0f70ed7cc4f1c0012ca95bcdddeb5c26dd21b09df0ec61b7b269e51cd0ad`.

The canonical TCD register blob used by B3B03 is:

`224acc350fde69d3c4aebed8628c0f945e0b3367`.

Its TCD-024 entry classifies the defect as:

`CONFIRMED_LEGACY_WRONG_INDEX_DEFECT_AND_LATENT_BOUNDS_RISK`.

Result: `PASS`.

## 3. Class-B causal identity

B3Q01 defines Class B for local algebra/index/species defects whose intended operation can be identified without changing state representation, physics or numerical policy.

TCD-024 satisfies that narrow form:

- the surrounding slow-site update is site-local;
- `Recf(J)`, equilibrium storage and site state are site-indexed;
- only the Langmuir affinity inside the kinetic exponent is selected with trial counter `I`;
- replacing `I` with `J` restores the same site's own parameter binding.

The latent out-of-bounds observation is separate support for the same index defect. It does not create a second correction mechanism.

Result: `PASS`.

## 4. Independent synthetic oracle review

SYNQ01 pins two applicable TCD-024 oracles:

- `SYNQ-O006`: per-site slow-Langmuir relaxation;
- `SYNQ-O007`: exact index-domain safety.

The active B3B03 microcase uses deliberately unequal site affinities `K = 2, 40, 600`, so the wrong selector cannot remain hidden by equal parameters. Re-evaluation at 80-digit Decimal precision produces distinct site-2 and site-3 states for the site-correct and wrong-`K1` selectors.

The index-domain oracle is exact: trial counter `I=1..20` is not a valid site selector for a three-site array, and the first invalid trial-domain value is `I=4`.

B3B03 also retained a small representation inconsistency in shorter numerical strings published by SYNQ01: three displayed values differ by one unit in the last displayed decimal from a fresh 80-digit re-evaluation. B3B03 correctly refused to turn that into a tolerance. The equation and exact discriminator remain the scientific evidence; the shortened strings are provenance only.

Result: `PASS_WITH_RECORDED_SYNQ01_DISPLAY_REPRESENTATION_ISSUE`.

## 5. Unrounded state and transfer evidence

The B3B03 active fixture stores full Decimal state values and transfer rates for each of three sites. The wrong-selector mutant is identical at site 1 by construction and different at sites 2 and 3.

The affected surface is therefore directly visible in unrounded slow-site P state and site-local slow-sorption transfer, rather than inferred only from formatted balance files.

Result: `PASS`.

## 6. Multi-site conservation identity

For the isolated internal transfer control volume consisting of dissolved P plus all slow-sorption sites, with no external source or sink during the isolated transfer:

```text
Delta P_solution + sum_j(Delta P_slow,j) = 0
```

B3B03 evaluates the solution counter-transfer as the exact negative of total slow-site storage gain. The identity closes exactly in Decimal arithmetic without a tolerance. The summed transfer rates also equal total site storage gain divided by `dt`.

This qualifies the local transfer identity only. It does not claim that every nonlinear phosphorus seam is resolved.

Result: `PASS`.

## 7. Active and inactive controls

Active synthetic control:

- `Optcxsl=2`;
- three unequal slow-Langmuir sites;
- target equation activated;
- wrong selector discriminated for sites 2 and 3.

Inactive site control:

- selected adsorption and desorption rates both zero;
- `qnew=qold` exactly;
- transfer rate `0` exactly;
- site result invariant to the affinity selector.

Inactive constitutive-route control:

- supplied LWKM uses `Optcxsl=3` Freundlich slow sorption;
- PREP05's TCD-024-only diagnostic comparison reports 55 model outputs and zero normalized differences on that route.

Result: `PASS`.

## 8. Natural activation limitation

All six supplied frozen active-P cases use `OPTCXSL=3`. None naturally activates the slow-Langmuir `Optcxsl=2` branch.

Therefore:

```text
natural_positive_activation = NOT_AVAILABLE_IN_SUPPLIED_FROZEN_TESTBANK
historical_prevalence = UNKNOWN
```

The synthetic active fixture is valid causal and coverage evidence. It is not historical B2 evidence and cannot establish prevalence.

Result: `PASS_LIMITATION_RETAINED`.

## 9. TCD-019 separation and NQ02 pinning

B3B03 pins NQ02 interaction evidence to the exact authority:

- branch `work/animo-nq02-tcd019-nonlinear-p-qualification`;
- head `40a41089020f78ee1d5181b8afc7bdb511af3193`;
- interaction blob `9ca37e90115faab9604a3f3051a8246b5e3a0813`.

That evidence explicitly keeps:

- TCD-019 as Class E numerical policy;
- TCD-024 as Class B wrong index;
- the combined diagnostic unadmitted.

A similarly named NQ02 development branch contains a different later/alternate interaction characterization. B3B03 does not silently float to that branch. The exact pinned NQ02 authority above governs this readiness record.

The TCD-024 claim remains valid without changing TCD-019. No solver stopping rule, secant/tangent policy, `Small`, clipping threshold or fallback policy is admitted here.

Result: `PASS`.

## 10. Expected-difference and non-interference review

The predeclared direct expected differences are limited to:

- site-J kinetic factor;
- site-J slow-sorbed P state;
- corresponding slow-sorption P transfer;
- downstream P state, balance, restart and report quantities receiving that transfer.

Expected unchanged surfaces include:

- branch and option selection;
- trial/site loop ordering;
- TCD-019 policy;
- solver tolerances and stopping rules;
- linear and Freundlich slow-sorption routes;
- inactive zero-rate sites;
- hydrology;
- unrelated C/N families outside existing P coupling;
- production and frozen source bytes.

PREP05's full synthetic TCD-024-only diagnostic changed a narrow P-centred output set and left inspected ordinary N/OM output families unchanged. The supplied Freundlich negative-control route is output-identical under declared metadata normalization.

This supports the atomic expected-difference surface. It does not justify a global claim that every P-coupled output is otherwise numerically identical under all possible slow-Langmuir runs.

Result: `PASS_WITH_SCOPE_BOUNDARY_RETAINED`.

## 11. Live validation state of ANIMO-B3B03

The final B3B03 workflow run is:

`34382965948`

on head:

`446f57f3aeff6e7db56ce473f0724bdb58cad94f`.

The run completed successfully. Both the exact readiness validator and the atomic scope guard passed.

Result: `PASS`.

## 12. Admission route review

The pinned PREP02R status remains:

`BLOCKED_HISTORICAL_REFERENCE_ARTIFACT_NOT_YET_OBTAINED`

with:

- `reference_qualified=false`;
- `external_request_sent=false`.

GOV02 requires completed reasonable B2 acquisition closure before the historical-uncertainty route can open. That condition is not met.

Therefore neither route is currently available for TCD-024:

```text
NORMAL_B2_AVAILABLE = false
INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY = false
```

Result: `FAIL_PENDING_NO_VALID_ADMISSION_ROUTE`.

## 13. Reviewer-independence gate

This review is technically separate in branch identity but not genuinely independent in reviewer identity. It is produced from the same ChatGPT authoring context that produced ANIMO-B3B03.

B3Q01 requires independent second-line review separate from correction authoring. That requirement cannot be truthfully certified here.

Result: `FAIL_NOT_INDEPENDENT`.

## Final decision

The technical Class-B readiness claim survives second-pass scrutiny:

`PASS_TCD024_ATOMIC_CLASS_B_READINESS_TECHNICALLY_RECONFIRMED`

No new technical correction mechanism was introduced and no TCD-019 numerical policy was modified.

B3 admission remains fail-closed because:

1. no valid admission route is open;
2. genuine independent second-line review is still missing;
3. historical prevalence remains `UNKNOWN`;
4. no natural positive slow-Langmuir activation exists in the supplied frozen testbank.

Final governance disposition:

`UNRESOLVED_NOT_ADMITTED_INDEPENDENT_SECOND_LINE_AND_VALID_ADMISSION_ROUTE_STILL_REQUIRED`
