# ANIMO-NQ02 — TCD-019 nonlinear phosphorus numerical reconstruction

Status: `SOURCE_BOUND_RECONSTRUCTION_AND_CAUSAL_NUMERICAL_QUALIFICATION_COMPLETED`.

## Scope and evidence boundary

This work unit treats TCD-019 only: nonlinear phosphate sorption numerical conservation and convergence policy. TCD-024, the slow-Langmuir wrong-index defect, remains a separate Class B interaction risk. No production source is changed. Every changed executable used here is a hashed B1 diagnostic descendant and is not B2.

## Pinned evidence

- frozen source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- frozen testcase archive SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- NQ01 authority selected by live ancestry/content comparison: `work/animo-nq01-numerical-qualification-architecture` at `e558dff12b127e0662cad62beea7527b42ad89ac`;
- NQ01 status: `QUALIFIED_NUMERICAL_QUALIFICATION_ARCHITECTURE_AWAITING_INDEPENDENT_REFERENCE_DATA`;
- TCD-019: Class E, `CONFIRMED_LEGACY_NUMERICAL_CONSERVATION_POLICY_DEFECT`, not admitted;
- TCD-024: Class B, `CONFIRMED_LEGACY_WRONG_INDEX_DEFECT_AND_LATENT_BOUNDS_RISK`, not admitted.

Both local B0 archives were re-hashed before diagnostic execution and matched the frozen identities above.

## Source-bound algorithm

`Transgen.for` calls the phosphorus transport/sorption route per layer and reconstructs the exact layer balance from the accepted aqueous concentration and the fast-sorbed, slow-sorbed and precipitated states. Its unfiltered conservation diagnostic is `Bapd-Batr`.

For `LWKM_gras_1040.2021.2045` the active configuration is:

- `Optcxfa = 2`, one fast Langmuir site;
- `Optcxsl = 3`, three slow Freundlich sites.

This activates TCD-019 but not the TCD-024 slow-Langmuir index path.

### Nonlinear unknowns and residual

`Transorp.for:C_unl` solves two coupled unknowns:

- `Rsc`, end-of-step aqueous concentration;
- `Avc`, average concentration over the step.

The Newton residual is

```text
F1 = Con*A1 + Hv2*A2 - Rsc
     + sum_i Fact_i * Difcxsl_i * A2

F2 = Con*B1 + Hv2*B2 - Avc
     + sum_i Fact_i * Difcxsl_i * B2
```

`A1,A2,B1,B2` come from `Detcoef` and depend on the fast-sorption storage coefficient `Avadco`. Slow sorption enters through `Difcxsl`, the adsorption/desorption rate choice and `Fact`. The Jacobian is assembled explicitly and includes `Avadcodc` from `Sorpfast`.

### Legacy convergence policy

Source constants are:

```text
Small   = 1e-4
Ccrit   = 1e-6
Maxiter = 20
```

Iterations 16 through 20 use running-average corrections rather than the current Newton correction and retain an `Avc_opt` associated with the smallest observed residual norm for fallback use.

The primary stopping test combines correction tests with signed residual comparisons `Vec(1) < 1e-3*Con` and `Vec(2) < 1e-3*Con`, not magnitude comparisons. Low-concentration `Ccrit` branches can also accept without the relative correction checks.

If Newton does not return, the routine enters a 50-iteration bisection-like scalar route with `abs(Df) < 1e-6` acceptance. `Recfso`, the slow-sorption adsorption/desorption rate selection, is inherited from the preceding Newton route rather than recomputed for every bisection trial. This is a source-bound fallback coupling risk, not separately admitted as a defect in NQ02.

## Constitutive conservation seam

For a Langmuir site

```text
S(C) = a*C/(1+b*C)
```

with `a = Parcxfa(2,I)*Parcxfa(3,I)/Rhbd`, the general `Sorpfast` branch represents storage through a finite secant. When `abs(Ct-Ct0) < 1e-6`, however, it substitutes the tangent

```text
S'(Ct) = a/(1+b*Ct)^2.
```

The tangent is not the finite start/end storage change. `Detcoef` therefore solves an equation containing an approximate storage contribution while `Transgen` later checks conservation using the actual stored states. This explains how `R_eq` can be small while `R_cons` is systematically biased.

For an on-relation start state, Langmuir admits the cancellation-free exact secant

```text
[S(C)-S(C0)]/(C-C0)
  = a / ((1+b*C)*(1+b*C0))
```

and derivative

```text
-a*b / ((1+b*C)^2*(1+b*C0)).
```

For an actual start store not exactly equal to `S(C0)`, the diagnostic exact-storage formulation retains that mismatch explicitly. A scientifically material off-relation initialization remains TCD-014 and must not be hidden in TCD-019.

The fast Freundlich option contains an analogous small-delta tangent switch. NQ02 therefore treats this as a numerical-policy family, although the historical activation studied here is fast Langmuir.

## Solver-independent diagnostic residuals

NQ02 uses three separate quantities.

### `R_eq`

Independent re-evaluation of `F1,F2` at the accepted `Rsc,Avc`, outside the legacy stopping predicate. It measures how closely the accepted state solves the equation represented by the selected numerical formulation.

### `R_cons`

```text
R_cons = Bapd - Batr
```

before any warning filter. `Batr` uses actual start/end aqueous, fast-sorbed, slow-sorbed and precipitated states plus transfers. This is the layer conservation residual.

### `R_constitutive`

```text
R_constitutive = Rhbd * (Avadco*(Rsc-Con) - (fast_end-fast_start)).
```

It measures whether the storage term supplied to the nonlinear equation equals the actual fast-sorption state change.

These residuals are deliberately non-interchangeable. A small `R_eq` can coexist with biased `R_cons` when the represented constitutive equation is itself non-conservative.

## Source-bound causal result

The executed matrix confirms the earlier PREP01 localization and sharpens it:

- legacy LWKM cumulative `R_cons`: `-0.27254515116349 kg/ha P`;
- exact/cancellation-safe storage representation with legacy `Small`: `-0.0179739628387 kg/ha P` and `R_constitutive` reduced to the binary64 floor;
- tightening `Small` alone to `1e-8` with the legacy tangent leaves `-0.254894233228 kg/ha P`;
- exact storage plus nonlinear refinement reaches a stable region around `Small=1e-7` to `1e-8`, with cumulative `R_cons` about `-5e-7 kg/ha P`, before still tighter Newton thresholds begin to activate the separate fallback route.

The signed residual asymmetry was not materially activated in the primary LWKM experiment. It is a source risk, not part of the qualified causal claim.

## Numerical interpretation

TCD-019 has two distinct numerical contributions:

1. **formulation bias**: the small-delta tangent is not the exact finite conserved storage change. This dominates the systematic sign bias;
2. **nonlinear acceptance error**: once the storage formulation is made exact, the legacy Newton stopping policy controls the remaining equation and conservation residual. Excessive tightening cannot be assessed independently of the fallback policy because bisection begins to activate.

A threshold-free, cancellation-safe exact storage representation is therefore preferable to selecting a smaller arbitrary `|Delta C|` switch. A future solver policy must qualify Newton and fallback acceptance together.

## Boundary of this qualification

The route-level candidate is:

`EXACT_CONSERVATIVE_CONSTITUTIVE_STORAGE_REPRESENTATION_PLUS_QUALIFIED_NONLINEAR_AND_FALLBACK_POLICY`.

This is a `CONVERGENT_POLICY_CANDIDATE`, not an admitted change. NQ02 does not select `Small=1e-7`, `1e-8`, or any other production threshold. It does not define a global numerical tolerance. Multi-case natural coverage, independent B2 evidence where obtainable, independent numerical review and later B3 admission remain separate gates.

`TOLERANCE_NOT_YET_QUALIFIED`.
