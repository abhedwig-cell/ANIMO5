# ANIMO-NQ02 — TCD-019 nonlinear phosphorus numerical reconstruction

Status: `SOURCE_BOUND_RECONSTRUCTION_PERSISTED_DIAGNOSTIC_MATRIX_NOT_YET_EXECUTED`.

## Scope and evidence boundary

This work unit qualifies TCD-019 only: nonlinear phosphate sorption numerical conservation and convergence policy. TCD-024, the slow-Langmuir wrong-index defect, is treated only as a separate interaction risk and is not merged into the TCD-019 correction claim.

No production source is changed. Any executable or source descendant used later is B1 diagnostic evidence only.

## Pinned evidence

- Frozen source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`.
- Frozen testcase archive SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.
- Authoritative NQ01 branch for this work unit: `work/animo-nq01-numerical-qualification-architecture`.
- Authoritative NQ01 head at NQ02 start: `e558dff12b127e0662cad62beea7527b42ad89ac`.
- NQ01 status: `QUALIFIED_NUMERICAL_QUALIFICATION_ARCHITECTURE_AWAITING_INDEPENDENT_REFERENCE_DATA`.
- TCD-019 B3Q01 class: `E`, `ATOMIC_NUMERICAL_POLICY_CLAIM`, not admitted.
- TCD-024 B3Q01 class: `B`, `ATOMIC_LOCAL_INDEX_CLAIM`, not admitted.

The local source and testbank artifacts were re-hashed before source inspection and matched the two frozen B0 hashes above.

## Source-bound algorithm

### Process entry

`Transgen.for` calls `Transorp` once per mineral-P layer. `Transgen` then reconstructs the layer transport plus storage balance from the solved aqueous concentration, fast sorption, slow sorption and precipitated-P states. Its diagnostic residual is `Bapd-Batr`.

For the supplied `LWKM_gras_1040.2021.2045` case, `CHEMPAR.INP` activates:

- `Optcxfa = 2`: fast Langmuir sorption;
- `Ncxfa = 1`;
- `Optcxsl = 3`: slow Freundlich sorption;
- `Ncxsl = 3`.

Therefore the known LWKM TCD-019 signal activates the fast-Langmuir small-delta path, while the TCD-024 slow-Langmuir wrong-index path is not active in this historical case.

### Unknowns and nonlinear system

`C_unl` solves two coupled unknowns:

- `Rsc`: concentration at end of the timestep;
- `Avc`: average concentration during the timestep.

It starts with `Rsc = Con` and `Avc = Con`, then uses Newton updates for at most 20 iterations. The Newton residual vector is:

```text
F1 = Con*A1 + Hv2*A2 - Rsc
     + sum_i Fact_i * Difcxsl_i * A2

F2 = Con*B1 + Hv2*B2 - Avc
     + sum_i Fact_i * Difcxsl_i * B2
```

where `A1,A2,B1,B2` are the analytical conservation-equation coefficients returned by `Detcoef`. They depend on the fast-sorption storage coefficient `Avadco`. Slow sorption enters through `Difcxsl`, the adsorption/desorption rate choice and `Fact`.

The Jacobian is assembled explicitly from `Coefdc`, `Eqcxsldc`, the Langmuir slow-sorption rate dependence where active, and the derivative `Avadcodc` supplied by `Sorpfast`.

### Newton stopping and late-iteration policy

Source constants are:

```text
Small   = 1e-4
Ccrit   = 1e-6
Maxiter = 20
```

For iterations 16 through 20, the routine no longer applies the current Newton correction directly. It accumulates corrections and subtracts their running average. It also stores the `Avc` associated with the smallest observed `abs(Vec(1))+abs(Vec(2))` for use as a later bisection initial estimate.

The primary convergence test combines relative corrections and one-sided residual comparisons. In source form the residual checks use `Vec(1) < 1e-3*Con` and `Vec(2) < 1e-3*Con`, not absolute residuals. Negative residuals therefore satisfy these terms regardless of magnitude. This is a source-bound asymmetry that must be measured separately from the `Small` threshold itself.

Additional branches accept low `Rsc` values through `Ccrit` without requiring the relative correction tests.

### Fallback

If Newton does not return, `C_unl` switches to a 50-iteration bisection-like scalar solve. The scalar residual is `Df = Lhs-Rhs`. Acceptance uses `abs(Df) < 1e-6`.

The fallback relation enforces:

```text
Ctry = 2*Ctrya - Con
```

and evaluates aqueous storage, fast sorption and slow-sorption terms directly. However, the adsorption/desorption rate array `Recfso` is inherited from the preceding Newton loop rather than recomputed inside each bisection trial. This is a separate control-path property to capture in NQ02. It is not yet classified as a defect.

## Fast-sorption constitutive seam

`Sorpfast` implements three fast-sorption models.

### Linear

The storage coefficient is exact and constant.

### Langmuir

For a site with

```text
S(C) = a*C/(1+b*C)
```

where `a = Parcxfa(2,I)*Parcxfa(3,I)/Rhbd`, the general branch uses the finite storage change:

```text
Avadco contribution = (S(Ct)-Ampocxfa(I))/(Ct-Ct0)
```

For `abs(Ct-Ct0) < 1e-6`, the source replaces that finite change with the tangent at `Ct`:

```text
S'(Ct) = a/(1+b*Ct)^2
```

The tangent is not equal to the secant for finite `Ct-Ct0`. Because `Detcoef` uses `Avadco` as storage capacity while the final state contains `S(Ct)`, the nonlinear solve can satisfy its approximate equation while the exact start/end storage accounting does not close.

When the start store is on the constitutive relation, the exact Langmuir secant has a cancellation-free form:

```text
[S(C)-S(C0)]/(C-C0)
  = a / ((1+b*C)*(1+b*C0))
```

with derivative with respect to `C`:

```text
-a*b / ((1+b*C)^2*(1+b*C0))
```

This removes the need for a numerical switch threshold. It is only a TCD-019 candidate when the start store is constitutively consistent. If `Ampocxfa != S(C0)`, the difference belongs to the separate TCD-014 initialization/state-consistency contract and must not be silently discarded.

### Freundlich

The same `abs(Ct-Ct0) < 1e-6` tangent substitution exists for the fast Freundlich option. NQ02 therefore treats the policy family as broader than one Langmuir expression, although the current TCD-019 historical signal is Langmuir-active.

## Reference-quality residuals

NQ02 will not use a legacy warning threshold as an acceptance rule. It defines three distinct diagnostic residuals.

### R_eq: nonlinear equation residual

Evaluate the accepted state with the governing `C_unl` equations independently of the solver stopping test. Record both components `F1,F2` and a dimensioned norm. The norm is evidence, not an admission tolerance.

### R_cons: exact layer P conservation residual

Use the `Transgen` identity before its warning filter:

```text
R_cons = Bapd - Batr
```

where `Batr` contains actual start/end aqueous, fast-sorbed, slow-sorbed and precipitated storage changes plus transport, and `Bapd` is the process production term. Capture the unfiltered signed value for every layer/timestep.

### R_constitutive: represented versus actual fast-storage change

For each fast-sorption site:

```text
R_constitutive = Rhbd * ( Avadco*(Rsc-Con)
                          - (Rsampocxfa-Ampocxfa) )
```

with the exact source units retained in capture metadata. This directly measures whether the storage coefficient used by the solve represents the actual fast-sorption state change. For the small-delta tangent path it should expose the constitutive conservation defect independently of whole-layer fluxes.

These residuals must be kept separate. A smaller `R_cons` does not prove that `R_eq` is converged, and a small `R_eq` for an approximate constitutive equation does not prove exact storage conservation.

## Existing B1 causal evidence

Existing PREP01 B1 evidence for LWKM reports:

- baseline cumulative `sum(BAPD-BATR) = -0.27254515116349 kg/ha P` over 27,000 layer/timestep checks;
- lowering only the fast-sorption small-delta switch from `1e-6` to `1e-12` reduced the cumulative residual to `-0.017973962837645 kg/ha P`;
- tightening only `C_unl Small` from `1e-4` to `1e-8` changed the cumulative residual to about `-0.2548942332 kg/ha P`;
- combining those two probes produced about `+9.63e-6 kg/ha P` cumulative residual.

This is strong causal localization, but it is not a convergence study and it does not qualify either numerical threshold. In particular, `1e-12` and `1e-8` remain diagnostic probe values, not candidate production tolerances.

## Immediate qualification questions

NQ02 must now establish whether:

1. exact constitutive storage representation removes the systematic residual without depending on a switch threshold;
2. the accepted aqueous and sorbed trajectories stabilize under monotone solver refinement;
3. the one-sided residual stopping test changes the apparent convergence envelope;
4. fallback use or late-iteration averaging materially affects accepted states;
5. precision changes scale the residual or leave a formulation-dominated floor;
6. time-step refinement changes the inferred policy candidate;
7. TCD-024 correction composes independently when slow Langmuir is activated.

Until those are answered, `TOLERANCE_NOT_YET_QUALIFIED` applies.
