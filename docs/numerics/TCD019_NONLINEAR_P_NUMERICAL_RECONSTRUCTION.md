# TCD-019 nonlinear P numerical reconstruction

Status: `SOURCE_BOUND_RECONSTRUCTION_COMPLETE_B1_CAUSALITY_ONLY`.

This document reconstructs the revision-53 nonlinear phosphate transport and sorption path relevant to TCD-019. It does not admit a numerical change. All runtime experiments are B1 diagnostic evidence. The frozen source and frozen testbank are unchanged.

## Evidence identity

Frozen ANIMO 4.1.5 revision 53 source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Frozen testbank archive SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Natural diagnostic case:

`LWKM_gras_1040.2021.2045`

Deterministic case-manifest SHA-256, calculated over sorted relative path plus member SHA-256 pairs:

`2a5bfc4ffafc53cda50f03a74a16b5aa8e83efd8633b23e8efbc792ed1dc3338`

Frozen `CHEMPAR.INP` SHA-256 for this case:

`b591c59110ce33dfc0ff7ad55e57431b7335d9c4834b4a283a0c8d26ae275c3d`

Frozen source file SHA-256 values:

- `Transorp.for`: `65ab0f70ed7cc4f1c0012ca95bcdddeb5c26dd21b09df0ec61b7b269e51cd0ad`
- `Transgen.for`: `cd5efa76c1a4840b50901ee5015940b74c5fe4df79aca43d53a4a4cb77b9fecb`

NQ01 authority was resolved by ancestry and current content rather than branch naming. `work/animo-nq01-numerical-qualification-architecture` at `e558dff12b127e0662cad62beea7527b42ad89ac` is 33 commits ahead of the parallel `final`, `copy`, `ignore`, `stop` and `packet-temp` state at `438a8838731208d19f8fe158254054b9ac2f5b33`, with that older commit as merge base. NQ02 therefore starts from `e558dff...`.

B3Q01 authority used here is `work/animo-b3q01-scientific-admission-framework` at `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`. Its classification keeps TCD-019 as Class E and TCD-024 as a separate Class B defect.

## Natural process activation

The frozen LWKM case activates:

- fast sorption: `OPTCXFA=2`, Langmuir, one site;
- slow sorption: `OPTCXSL=3`, Freundlich, three sites.

It therefore activates the TCD-019 fast nonlinear Langmuir path while not activating TCD-024, which is specific to the slow-Langmuir path `OPTCXSL=2`. This makes LWKM useful for TCD-019 causal isolation.

## Governing numerical unknowns

`Conc_unl` calls `C_unl` to calculate two accepted concentrations for each layer and timestep:

- `Rsc`: phosphate concentration at the end of the time interval;
- `Avc`: average phosphate concentration over the time interval.

The legacy initial guess is fixed in source:

```text
Rsc = Con
Avc = Con
```

where `Con` is the concentration at the start of the local interval.

For a given current iterate, `C_unl` computes slow-sorption departure from equilibrium, calls `Sorpfast` for the fast storage coefficient, calls `Sorpslow` for equilibrium slow storage and derivatives, and calls `Detcoef` to obtain coefficients of the analytical concentration solution.

The Newton residual vector in revision 53 is structurally:

```text
r_R = Con*A1 + Hv2*A2 - Rsc
      + sum(Fact_i * Difcxsl_i * A2)

r_A = Con*B1 + Hv2*B2 - Avc
      + sum(Fact_i * Difcxsl_i * B2)
```

with the Jacobian augmented by derivatives of the analytical coefficients and slow-sorption terms. `A1`, `A2`, `B1` and `B2` depend on the storage coefficient returned by `Sorpfast`.

## Fast Langmuir relation and the TCD-019 seam

For one fast Langmuir site the constitutive sorbed amount per dry-soil mass can be written as

```text
S(C) = (M / rhbd) * b*C / (1 + b*C)
```

where revision-53 source maps `M` to `Parcxfa(2)` and `b` to `Parcxfa(3)`.

For ordinary concentration changes, `Sorpfast` uses an exact stored-state secant:

```text
Avadco = [S(C)-A0] / (C-C0)
```

where `A0` is the supplied start-of-step fast sorbed amount.

For `abs(C-C0) < 1e-6`, however, source lines 2309-2315 replace that finite storage change by the tangent at the final concentration:

```text
dS/dC at C = (M/rhbd) * b / (1+b*C)^2
```

while still setting the final sorbed state from the nonlinear Langmuir relation. The coefficient used inside the conservation solve is therefore not, in general, the finite storage change later represented by the accepted start and end states.

This is the primary TCD-019 causal seam.

For a constitutively consistent start state, the exact Langmuir secant has the cancellation-resistant identity

```text
[S(C)-S(C0)]/(C-C0)
  = (M/rhbd) * b / [(1+b*C)(1+b*C0)]
```

so no `abs(C-C0)` switch is mathematically required for Langmuir storage itself.

## Important TCD-014 boundary

The exact constitutive secant above assumes that the represented start store lies on `S(C0)`. The frozen LWKM run has a small first-step inconsistency between the supplied initial fast store and the constitutive relation. The maximum bulk offset captured at the first step is `8.757228792122262e-08`; after the first 30 layer calls it falls to approximately machine-level representation noise, with maximum absolute offset about `1.11e-16`.

This is not folded into TCD-019. It is the separate TCD-014 initialization/state-projection seam. A formula of the form

```text
[S(C)-A0]/(C-C0)
```

is algebraically exact for the represented store, but becomes ill-conditioned when a tiny `A0-S(C0)` offset is divided by a tiny concentration change. NQ02 tested that formulation as a counterexample and found systematic fallback to bisection and severe instability. TCD-019 must therefore not silently solve TCD-014 by embedding an initial-state discrepancy into a near-zero secant.

## Legacy nonlinear convergence policy

`C_unl` uses:

- Newton iteration cap: 20;
- `Small = 1e-4` for relative correction tests;
- `Ccrit = 1e-6` for a low-concentration branch;
- averaging of cumulative Newton corrections during the last five iterations;
- retention of an `Avc_opt` state with the smallest recorded `abs(Vec(1))+abs(Vec(2))` during that late-iteration region;
- negative-state return to the caller for interval reduction unless this is the last allowed interval reduction;
- bisection fallback on the final attempt or after Newton exhaustion.

The normal Newton acceptance expression is also sign-asymmetric. It tests

```text
Vec(1) < 1e-3*Con
Vec(2) < 1e-3*Con
```

rather than the absolute residuals. The relative correction terms do use absolute values. A negative residual is therefore not bounded by the residual part of this criterion in the same way as a positive residual. NQ02 does not replace this criterion, but it is part of the legacy numerical policy that future admission must address explicitly rather than merely tightening `Small`.

The bisection path has a separate fixed acceptance condition `abs(Df) < 1e-6` and a cap of 50 iterations. Thus revision 53 has more than one nonlinear acceptance threshold and more than one solver path.

## Reference-quality diagnostic residual

NQ02 separates the legacy Newton bookkeeping from an exact constitutive local conservation residual. For the accepted `Rsc` and `Avc`, the diagnostic evaluator reconstructs the discretized local P conservation equation using:

- the accepted aqueous concentrations;
- exact fast-sorption storage from the constitutive relation, not the small-delta tangent coefficient;
- source-consistent slow equilibrium storage;
- source kinetic factors for the slow sites;
- source water/storage coefficients and local timestep.

The reported scalar residual is `F = LHS - RHS`. It is a conservation-equation residual, not the legacy warning metric and not the printed balance rounding. It is also not claimed to be a complete norm of the two-component Newton vector. It is deliberately an independent check of whether the accepted state satisfies the conserved local P equation when nonlinear storage is evaluated exactly.

For the natural LWKM case, where slow sorption is Freundlich, this residual is not confounded by the separate slow-Langmuir implementation seams discussed in the interaction document.

Baseline over 27,000 layer/timestep calls:

- maximum absolute exact-equation residual: `1.0007604587941588e-06` in the local equation units;
- mean absolute residual: `1.9857497039147934e-08`;
- cumulative physical P conservation residual: `-0.27254515116348993 kg/ha`;
- largest local P conservation residual: `5.011328758918021e-4 kg/ha`.

## Independent high-precision decomposition

Using the captured unrounded accepted states and effective layer-specific Langmuir parameters, NQ02 independently evaluated at 80 decimal digits the exact finite storage change minus the storage change represented by the legacy tangent branch.

Across 25,923 calls in which the legacy small-delta tangent branch is active:

- summed exact-minus-tangent mismatch: `+0.2546290594721548 kg/ha`;
- summed absolute mismatch: the same value, showing a one-sided bias in this case;
- largest local mismatch: `0.0005011328758797566 kg/ha`;
- the same calculation in binary64 gives `0.2546290594721141 kg/ha`;
- 80-digit minus binary64 aggregate difference is about `4.07e-14 kg/ha`.

The dominant TCD-019 drift is therefore not explained by ordinary binary64 roundoff. It is a formulation/linearization policy effect at the canonical diagnostic precision.

## Reconstruction decision

The source reconstruction supports:

`LEGACY_NUMERICAL_POLICY_NONCONVERGENT_OR_BIASED`

The word `biased` is important. The legacy Newton solve often satisfies its own stopping rule, but the accepted solution exhibits a strongly signed conservation error because the nonlinear fast storage represented inside the solve is not the exact finite storage change. Tightening the nonlinear correction tolerance alone does not remove that mechanism.

A threshold-free, constitutively exact Langmuir secant is mathematically available and is studied separately as a numerical-policy candidate. It is not admitted here, and it has an explicit TCD-014 initialization boundary.

`TOLERANCE_NOT_YET_QUALIFIED`
