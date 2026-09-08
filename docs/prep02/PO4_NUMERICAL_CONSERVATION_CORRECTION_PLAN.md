# ANIMO-PREP02 — PO4 numerical-conservation correction gate

Status: `PLANNED_CLASS_E_NUMERICAL_POLICY_CORRECTION_REFERENCE_REQUIRED`.

## Scope

This work item covers TCD-019 only: recurring inorganic-P mass drift caused by the interaction of nonlinear fast-sorption linearization and nonlinear solver stopping policy in `Transorp`.

It does not cover:

- TCD-014 initialization-state consistency;
- TCD-017 organic-P balance bookkeeping;
- general precision modernization;
- GHG or macropore qualification.

## Semantic class

TCD-019 is **Class E: numerical constitutive-conservation correction**.

It is not Class A accounting-only because changing the sorption solve changes concentrations and therefore downstream coupled trajectories. It is not a physics-model replacement either: the intended Langmuir constitutive relation is retained. The correction changes how that constitutive relation is represented inside a conserved nonlinear transport solve.

Expected properties:

```text
physics_relation_unchanged = true
numerical_policy_changed = true
state_trajectory_may_change = true
mass_conservation_should_improve = true
reference_qualification_required = true
```

## Frozen behaviour that must first be reference-qualified

For the LWKM case the frozen revision-53 behaviour must reproduce:

- recurring `Transgen` PO4 local residuals;
- cumulative local residual around `-0.2725451512 kg/ha P` over the investigated diagnostic run;
- strong negative sign bias of local residuals;
- no corresponding large local legacy warning because individual events remain below the absolute warning floor.

These values remain diagnostic until a historical or independently admitted reference executable reproduces them.

## Candidate correction family

The corrected-legacy implementation should not simply lower tolerances until the observed residual disappears.

Preferred structure:

1. use a mass-consistent finite storage change for nonlinear fast sorption;
2. avoid subtractive cancellation for small concentration changes through an analytically stable secant where possible;
3. treat intentionally inconsistent start stores as an initialization-contract issue rather than forcing them onto the constitutive curve invisibly;
4. define nonlinear solver convergence independently from ledger closure;
5. expose both nonlinear residual and mass residual in diagnostics.

For Langmuir sorption

```text
S(C) = a*C/(1+b*C)
```

the exact constitutive secant can be evaluated stably as

```text
[S(C)-S(C0)]/(C-C0) = a / [(1+b*C)(1+b*C0)]
```

when the start store is on the constitutive relation. The derivative of this secant with respect to `C` can also be written analytically for Newton iteration.

If the persisted start store is not on the constitutive relation, the corrected implementation must use the actual conserved start mass or book an explicit initialization adjustment. TCD-014 owns that policy decision.

## Diagnostic causal evidence already available

Baseline LWKM `Transgen` local balance accumulation:

`-0.27254515116349 kg/ha P`.

Probe A, remove almost all use of the small-delta tangent approximation by lowering the switch from `1e-6` to `1e-12`:

`-0.017973962837645 kg/ha P`.

Probe B, tighten only `C_unl` Newton `Small` from `1e-4` to `1e-8`:

`-0.25489423322790 kg/ha P`.

Combined A+B:

`+9.6337434306e-6 kg/ha P`.

Absolute drift reduction:

`99.9964653%`.

The combined probe changes multiple ordinary P outputs and some coupled output surfaces, so it cannot be admitted as an observer or reporting-only correction.

## Admission gates

### E-G1 — native frozen reproduction

Require a qualified frozen reference for an affected P case. The reference must capture unrounded mass terms or equivalent observer evidence.

### E-G2 — local constitutive identity

For each supported fast-sorption model:

- linear;
- Langmuir;
- Freundlich;

prove that the storage change used by the transport equation matches the actual beginning/end conserved storage to the admitted floating-point policy.

No arbitrary small-`dC` branch may introduce a systematic mass term.

### E-G3 — nonlinear convergence separation

Persist independently:

- nonlinear equation residual;
- mass residual;
- iteration count;
- fallback/bisection use;
- constitutive branch used.

A nonlinear convergence tolerance cannot serve implicitly as the mass-conservation tolerance.

### E-G4 — trajectory qualification

Because state trajectories change, compare corrected versus frozen reference for:

- aqueous PO4 concentration;
- fast sorbed P;
- slow sorbed P;
- precipitated P;
- boundary P fluxes;
- plant uptake where active;
- downstream coupled N/OM quantities that respond to P-state changes;
- period and cumulative P balances.

Differences must be explained by the admitted correction, not hidden under one global tolerance.

### E-G5 — initialization interaction

Run both:

- constitutively consistent initial stores;
- deliberately inconsistent but accepted legacy `INPO=1` stores.

The latter must exercise TCD-014 policy explicitly. TCD-019 must not silently redefine which initial quantity is authoritative.

### E-G6 — whole-case and cross-case regression

At least one P-rich test case is insufficient. The correction must be exercised against all available compatible P cases and dedicated synthetic constitutive tests spanning concentration ranges and sorption curvature.

## Exit discipline

Possible exit:

`QUALIFIED_CORRECTED_LEGACY_PO4_CONSERVATIVE_NUMERICAL_POLICY`

only after frozen reference qualification plus the gates above.

Until then:

```text
implemented_in_production = false
corrected_legacy_admitted = false
ANIMO5_process_migration_admitted = false
```
