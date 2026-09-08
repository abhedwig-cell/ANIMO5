# PO4 recurring numerical-conservation seam in `Transorp`

Status: `SOURCE_BOUND_NUMERICAL_CONSERVATION_POLICY_DEFECT_CAUSALLY_LOCALIZED`.

This note records diagnostic evidence only. The frozen source and frozen LWKM testcase remain unchanged.

## Observed residual

For `LWKM_gras_1040.2021.2045`, the deterministic diagnostic run shows a recurring inorganic-P balance drift. Instrumented `Transgen` evidence demonstrates that the cumulative `Bapp` deviation is generated inside the PO4 transport/sorption solve rather than in `Outbal_calc` bookkeeping.

Across 27,000 measured layer/timestep checks:

- cumulative `sum(BAPD-BATR) = -0.27254515116349 kg/ha P`;
- largest local absolute residual = `5.011328758918021e-4 kg/ha P`;
- negative local residuals = 24,379;
- positive local residuals = 2,621.

The individual errors are far below the legacy local warning threshold, but their strong sign bias accumulates over the simulation.

## Source mechanism 1: tangent substituted for exact secant

`Transorp.for`, subroutine `Sorpfast`, uses a nonlinear Langmuir fast-sorption relation. In the general branch it uses the exact change in sorbed mass through the secant slope:

```fortran
Dum = (Rsampocxfa(I)-Ampocxfa(I))/(Ct-Ct0)
```

For `abs(Ct-Ct0) < 1e-6`, however, it replaces the secant by the local derivative at the final concentration `Ct`:

```fortran
Avadco = Avadco + A / (1 + b*Ct)**2
```

with `A = Parcxfa(2,I)*Parcxfa(3,I)/Rhbd` and `b = Parcxfa(3,I)`.

For nonlinear Langmuir sorption this tangent is not identical to the finite storage change divided by `Ct-Ct0`. The conservation equation therefore uses an approximate fast-sorption storage coefficient while the later `Transgen` mass check uses the actual start/end sorbed amounts.

A temporary diagnostic source probe reduced only this `1e-6` switch threshold to `1e-12`, forcing the exact stored-state secant over essentially all ordinary small concentration changes. No testcase input or frozen source was changed.

Result:

- cumulative `Transgen` residual: `-0.27254515116349` -> `-0.017973962837645 kg/ha P`;
- reduction in the dominant drift: about 93.4 percent.

This establishes the small-delta tangent substitution as the dominant source of the systematic PO4 sign bias in this case.

## Source mechanism 2: nonlinear solver stopping policy

`C_unl` uses `Small = 1e-4` in its Newton convergence policy. A separate diagnostic probe tightened only this value to `1e-8`.

By itself that changes the cumulative residual from approximately:

`-0.2725451512` to `-0.2548942332 kg/ha P`.

The convergence tolerance is therefore not the main cause, but it leaves a material residual after the constitutive approximation is removed.

## Combined causal probe

Combining:

1. the exact stored-state Langmuir secant for small `Ct-Ct0` changes by lowering the tangent-switch threshold from `1e-6` to `1e-12`; and
2. `C_unl` Newton `Small` from `1e-4` to `1e-8`;

produces:

- cumulative `sum(BAPD-BATR) = +9.6337434306e-6 kg/ha P`;
- largest local absolute residual = `1.0140786787e-5 kg/ha P`;
- largest GP period residual in `bappGP.Out` approximately `1.02e-5 kg/ha P`;
- final cumulative GP deviation approximately `9.89e-6 kg/ha P`;
- local residual sign distribution becomes nearly symmetric: 13,243 positive versus 13,752 negative.

Relative to the baseline cumulative absolute drift, the combined diagnostic reduction is `99.9964653%`, a factor of about 28,291.

This is strong causal evidence that the observed recurring LWKM PO4 drift is a numerical-conservation policy artefact, not a missing external P ledger term.

## Stable conservative formulation

For the Langmuir function

```text
S(C) = a*C/(1+b*C)
```

the exact secant between `C0` and `C` can be written without subtractive cancellation as:

```text
[S(C)-S(C0)]/(C-C0) = a / [(1+b*C)(1+b*C0)]
```

where in this source `a = Parcxfa(2,I)*Parcxfa(3,I)/Rhbd`.

This provides a route to a mass-consistent constitutive linearization without relying on an arbitrary `|C-C0|` threshold. When the stored initial fast-sorption amount is intentionally inconsistent with the sorption relation, that inconsistency belongs to the separate TCD-014 initialization contract and must be accounted explicitly rather than hidden in the secant formula.

## Classification

`CONFIRMED_LEGACY_NUMERICAL_CONSERVATION_POLICY_DEFECT`

The term *defect* here is specific: the numerical policy knowingly substitutes a tangent approximation for an exactly representable nonlinear storage change and combines it with a convergence tolerance that permits systematic accumulated mass drift. This is not evidence that the Langmuir physics itself is wrong.

## Not accounting-only

Unlike TCD-017 and TCD-018, this correction changes solved concentrations and therefore downstream trajectories. In a comparison of the baseline Class-A diagnostic run with the combined PO4 numerical probe, multiple P outputs and some coupled N/output surfaces changed. It must not be admitted under the accounting-only Class-A route.

## Qualification consequence

ANIMO5 should require constitutive updates used inside a conserved transport equation to be conservative by construction wherever practical. Solver tolerance then controls nonlinear-equation accuracy, not whether a constitutive storage change is booked consistently.

A corrected-legacy candidate must separately qualify:

1. exact local P mass closure;
2. concentration and sorption trajectories;
3. interaction with precipitation and slow sorption;
4. coupled downstream N/OM effects;
5. behaviour for all fast-sorption options, especially Langmuir and Freundlich;
6. initialization cases where the supplied store is not exactly on the constitutive relation;
7. historical native-reference parity before calling any changed trajectory an admitted correction.

The raw `~0.273 kg/ha P` legacy cumulative drift must not be converted into a numerical acceptance tolerance.
