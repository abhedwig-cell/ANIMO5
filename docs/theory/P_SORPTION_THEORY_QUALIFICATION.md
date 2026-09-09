# Revision-53 phosphorus sorption and precipitation theory qualification

Decision: `QUALIFIED_INHERITED_P_SORPTION_THEORY_WITH_REV53_OPTION_AND_DEFECT_GAPS`

Production migration: `NOT_ADMITTED`

## 1. Evidence boundary

The supplied ANIMO 4.0 User's Guide is unusually strong evidence for the phosphorus constitutive interface because it explicitly documents equilibrium sorption, non-equilibrium sorption and precipitation options in `CHEMPAR.INP`.

For revision 53, that guide is used as `AUTHORITATIVE_INHERITED_ANIMO40_THEORY`, not as an automatic authority for every later branch, solver tolerance or generalized option.

Public WUR phosphorus descriptions independently support the physical separation between:

- a fast reversible adsorption process;
- a slower time-dependent fixation/diffusion process;
- precipitation/dissolution controlled by the phosphate concentration relative to an equilibrium or threshold level.

These public descriptions are supportive process evidence. They do not establish the exact revision-53 numerical implementation.

## 2. Fast equilibrium sorption

### ANIMO 4.0 authority

The 4.0 guide documents the following equilibrium-sorption options:

- linear;
- Langmuir;
- Freundlich.

It also states that ANIMO 4.0 operationally permits only:

- `OPTCXFA = 2`, Langmuir;
- `NCXFA = 1`, one equilibrium site.

The inherited fast-Langmuir process is therefore independently documented.

Reconciliation state for this core:

`THEORY_CONFIRMED`

### Revision-53 source

`Transorp.for` retains the fast constitutive family. For Langmuir, the source computes equilibrium sorbed amount from a maximum sorption amount and affinity coefficient with the standard saturating form represented by `Parcxfa(2,site)` and `Parcxfa(3,site)`.

The exact revision-53 support for additional fast constitutive options or multiple sites is not proven by the 4.0 operational contract. Those generalized paths remain:

`IMPLEMENTATION_DERIVED_NOT_INDEPENDENT_THEORY`

until a 4.1.x change document or equivalent version-specific authority is recovered.

### TCD-019 is a numerical-policy issue, not a theory replacement

PREP01 TCD-019 found that the revision-53 nonlinear transport/sorption path can use a local Langmuir tangent rather than the exact finite storage change for very small concentration increments and uses a comparatively loose nonlinear stopping criterion in `C_unl`.

This does not show that Langmuir sorption itself is the wrong scientific model. It shows that the numerical realization of a conserved nonlinear storage relation requires separate qualification.

TH01 therefore keeps:

`TCD-019 = NUMERICAL_POLICY_CHANGE_REQUIRES_SEPARATE_QUALIFICATION`

rather than reclassifying it as a physics change.

## 3. Slow non-equilibrium sorption

### ANIMO 4.0 authority

The 4.0 guide explicitly documents all three non-equilibrium sorption options:

- `OPTCXSL = 1`: linear;
- `OPTCXSL = 2`: Langmuir;
- `OPTCXSL = 3`: Freundlich.

It permits one to three non-equilibrium sites and supplies separate first-order adsorption and desorption rate constants per site/horizon.

This is important for revision-53 interpretation. Slow Langmuir is not a source-only post-4.0 invention. It is a documented inherited ANIMO option.

### Physical interpretation

Later public WUR descriptions of ANIMO phosphorus behavior predominantly describe the calibrated slow process as a time-dependent Freundlich-type fixation/diffusion relation with multiple components, while fast adsorption is described as reversible Langmuir sorption.

This later emphasis strengthens the theory basis for the standard Freundlich slow-fixation route. It does not invalidate the documented optional slow-Langmuir route.

The correct evidence split is therefore:

- slow Freundlich: inherited theory is strong and later public descriptions are consistent with its physical role;
- slow Langmuir: inherited option authority is strong, but the exact revision-53 kinetic integration still requires source/version reconciliation.

## 4. Slow Freundlich

Reconciliation state:

`THEORY_CONFIRMED`

The source computes the site equilibrium target for the Freundlich branch from the site-specific coefficient and exponent and relaxes the non-equilibrium store using site-specific rate coefficients.

The supplied phosphorus cases exercise `OPTCXSL = 3`, which gives this route meaningful B1 coverage. That coverage remains diagnostic rather than historical B2 evidence.

B3 implication:

`THEORY_READY_BEHAVIOURAL_REFERENCE_STILL_REQUIRED`

The scientific process can be judged against inherited theory, but exact historical trajectories and admissible tolerances still require B2/B3 reconciliation.

## 5. Slow Langmuir and TCD-024

Reconciliation state:

`THEORY_CODE_CONFLICT`

### Intended site semantics

The 4.0 input contract establishes that non-equilibrium sorption can contain multiple sites and that each site has its own constitutive parameters and adsorption/desorption rates.

In the revision-53 source, the slow-Langmuir equilibrium target is likewise site-indexed. The surrounding algorithm uses site index `J` for:

- equilibrium amount;
- adsorption/desorption rate;
- current and result sorbed amount.

### Source conflict

`Conc_unl` has an outer nonlinear trial loop indexed by `I` and an inner slow-site loop indexed by `J`. In one Langmuir kinetic exponent it accesses:

`Parcxsl(3,I)`

instead of the site-specific:

`Parcxsl(3,J)`.

The conflict is stronger than a naming suspicion because:

1. `I` is a solver trial counter, not a sorption-site identifier;
2. the inherited multiple-site theory requires site-specific parameters;
3. the neighboring slow-site calculations use `J` consistently;
4. `Parcxsl` has only the declared site dimension while `I` can range much farther;
5. PREP05's isolated `I -> J` probe produces large coherent phosphorus changes and removes more than 99.5 percent of the synthetic nonclosure;
6. the same correction is diagnostically inert on the supplied Freundlich route.

TCD-024 is therefore scientifically interpretable as a parameter-binding conflict with the documented site model.

This still does not admit the correction to B3. Historical behavior for `OPTCXSL=2` is not independently available and no supplied native testcase exercises it.

B3 implication:

`BLOCKED_TCD024_AND_HISTORICAL_REFERENCE`

Required corrected-legacy qualification must use unequal slow-Langmuir site parameters, unrounded site states, explicit bounds/index diagnostics and non-interference checks for the linear and Freundlich routes.

## 6. Precipitation and dissolution

### Inherited instantaneous route

The 4.0 guide documents:

- `OPTPR = 0`: instantaneous precipitation;
- `OPTPR = 1`: first-order kinetic precipitation;

and explicitly states that ANIMO 4.0 operationally allows only the instantaneous route.

The guide also documents the phosphate threshold or buffer concentration above which precipitation occurs.

Reconciliation for the inherited instantaneous process:

`THEORY_CONFIRMED`

### Revision-53 kinetic route

Revision 53 retains a first-order kinetic option. TH01 has not located a version-specific source that independently establishes when this route became operational, its intended calibration domain or whether its exact time integration matches the introducing formulation.

Classification:

`CODE_DEFINED_THEORY_UNCONFIRMED`

for the kinetic extension beyond the documented 4.0 operational route.

## 7. Initial-state coupling

The physical mineral-P state is not only dissolved PO4. It includes solution concentration, fast sorption, slow sorption and precipitated P. The 4.0 guide already documents this coupled initial state.

PREP01 TCD-014 showed that revision 53 can accept small per-layer inconsistencies between supplied dissolved and sorbed initial state and then project those states through the sorption calculation, producing a deterministic first-step profile residual.

The theory implication is clear:

- the coupled P state is conserved as a whole;
- initialization policy must specify whether inconsistent independently supplied stores are rejected, preserved or reconciled;
- the revision-53 threshold/tolerance policy is not defined by the 4.0 scientific theory alone.

This remains a B3 initialization-policy issue, not a reason to redefine the physical stores.

## 8. P-class forcing is adjacent but not sorption theory

Revision-53 `PClassOption`, `PClassYearSwitch`, `PClass` and `ChoosePClass` select class-indexed crop uptake and crop-loss forcing. The source identifies an `EMW2012` context but the current theory evidence does not define the scientific meaning of the classes or thresholds.

Classification:

`IMPLEMENTATION_DERIVED_NOT_INDEPENDENT_THEORY`

Reconciliation state:

`CODE_DEFINED_THEORY_UNCONFIRMED`

This policy can alter phosphorus trajectories but must not be folded into the sorption constitutive theory.

## 9. B3 assessment

| phosphorus surface | theory evidence | reconciliation | B3 readiness |
| --- | --- | --- | --- |
| Fast one-site Langmuir | strong ANIMO 4.0 authority | `THEORY_CONFIRMED` | theory-ready; TCD-019 numerical qualification remains |
| Additional fast options/sites | source-defined beyond documented 4.0 operational scope | `CODE_DEFINED_THEORY_UNCONFIRMED` | blocked on 4.1.x provenance |
| Slow Freundlich | strong inherited option plus later public process consistency | `THEORY_CONFIRMED` | theory-ready; B2/B3 behavior still required |
| Slow Langmuir | explicit inherited option | `THEORY_CODE_CONFLICT` because of TCD-024 | blocked until corrected-legacy and B2 qualification |
| Instantaneous precipitation | strong inherited authority | `THEORY_CONFIRMED` | theory-ready; historical behavior still to qualify |
| Kinetic precipitation | source-visible but 4.0 non-operational | `CODE_DEFINED_THEORY_UNCONFIRMED` | blocked on version-specific authority |
| P-class forcing | source-defined later policy | `CODE_DEFINED_THEORY_UNCONFIRMED` | blocked on independent scientific provenance |

## 10. Qualification decision

TH01 can defend the inherited ANIMO phosphorus constitutive theory substantially better than the GHG or macropore extensions.

It cannot defend all revision-53 phosphorus options as a single fully qualified theory surface.

Decision:

`QUALIFIED_INHERITED_P_SORPTION_THEORY_WITH_REV53_OPTION_AND_DEFECT_GAPS`

No frozen source, testcase, physical equation or numerical policy was changed by this qualification.
