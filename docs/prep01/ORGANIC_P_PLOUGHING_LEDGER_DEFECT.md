# Organic-P ploughing redistribution balance-bookkeeping defect

Status: `CONFIRMED_LEGACY_BALANCE_BOOKKEEPING_DEFECT_STATE_PHYSICS_UNCHANGED`.

This note records diagnostic evidence against the supplied ANIMO 4.1.5 revision-53 source and the deterministic LWKM testcase. The frozen source and frozen testcase remain unchanged.

## 1. Observed residual envelope

The largest organic-P balance-period deviation in the deterministic diagnostic envelope occurs in `LWKM_gras_1040.2021.2045`, `bapoGP.Out`, year 1998:

`+0.0494 kg/ha P`.

The same balance profile shows other isolated nonzero annual residuals:

- 1997: `+0.0441 kg/ha P`;
- 1998: `+0.0494 kg/ha P`;
- 2007: `+0.0251 kg/ha P`;
- 2008: `+0.0352 kg/ha P`.

The cumulative deviation consequently reaches approximately `+0.154 kg/ha P`.

In contrast, an instrumented `TRANSPORT` run for 1998 gives a summed organic-P `BAPD-BATR` of only about `1.45e-7 kg/ha P`. The large annual residual is therefore not a transport nonclosure.

## 2. Source-level redistribution contract

`Addit.for` handles ploughing as an internal redistribution. When `Pl(I)>0`, the surface reservoir is emptied and its material is mixed into the ploughing layers.

For dissolved organic P (DOP), `Addit.for` explicitly records the surface-reservoir removal as:

```fortran
If (Ipo.Eq.1) Addiorpotoppl(I) = - Sudiorpo
```

and records layer-wise organic-P changes in `Addiorpopl(I,Ln)`.

For each investigated ploughing event, the top-reservoir term plus the layer redistribution terms sums to zero to floating-point roundoff. The physical/state redistribution itself is therefore conservative in this bookkeeping representation.

Examples from source-consistent instrumentation:

### 1997 event

```text
Addiorpotoppl * Z = -0.044113049197064061 kg/ha P
sum layer Addiorpopl * Z = +0.04411304919706420 kg/ha P
net = about 1.4e-16 kg/ha P
```

### 1998 event

```text
Addiorpotoppl * Z = -0.049376586649567941 kg/ha P
sum layer Addiorpopl * Z = +0.049376586649567955 kg/ha P
net = about 1.4e-17 kg/ha P
```

The same zero-sum pattern occurs for the later 2007 and 2008 ploughing events.

## 3. Missing balance-bookkeeping term in `Outbal_calc`

`Outbal_calc.for` books the ploughing redistribution into the balance array `Redi`.

For N, the top-reservoir terms are explicitly included:

```fortran
If(Ln.Eq.0)Then
  Banh(Redi,Ly) = Banh(Redi,Ly) + Adnhtoppl(I)   *Z
  Bani(Redi,Ly) = Bani(Redi,Ly) + Adnitoppl(I)   *Z
  Bano(Redi,Ly) = Bano(Redi,Ly) + Addiornitoppl(I)*Z
End If
```

For P, the analogous block includes the inorganic-P top term:

```fortran
If (Ln.Eq.0) Then
  Bapp(Redi,Ly) = Bapp(Redi,Ly) + Adpotoppl(I)*Z
End If
```

but **does not include** the corresponding organic-P term:

```fortran
Bapo(Redi,Ly) = Bapo(Redi,Ly) + Addiorpotoppl(I)*Z
```

Layer-wise organic-P redistribution terms are nevertheless included later through `Addiorpopl(I,Ln)`. As a result, `Bapo(Redi,Ly)` receives the positive mass added to the plough layers without the equal negative removal from the surface reservoir.

The annual balance residual therefore equals the omitted top-reservoir term with opposite sign.

## 4. Causal accounting-only probe

A temporary diagnostic source copy added exactly one missing bookkeeping statement in the `Ln==0` ploughing block:

```fortran
Bapo(Redi,Ly) = Bapo(Redi,Ly) + Addiorpotoppl(I)*Z
```

No process state, transport equation, reaction rate, input, hydrology or redistribution calculation was changed.

Results for `bapoGP.Out`:

| year | frozen-source diagnostic residual | accounting-probe residual |
| --- | ---: | ---: |
| 1997 | `+4.41e-2 kg/ha P` | `+5.07e-13 kg/ha P` |
| 1998 | `+4.94e-2 kg/ha P` | `+4.61e-10 kg/ha P` |
| 2007 | `+2.51e-2 kg/ha P` | no material residual |
| 2008 | `+3.52e-2 kg/ha P` | no material residual |

Across the corrected diagnostic series no annual organic-P residual exceeds `1e-4 kg/ha P`; the largest observed period residual is approximately `4.06e-8 kg/ha P`.

This causally confirms that the large isolated organic-P residuals are produced by missing balance bookkeeping, not by organic-P transport or redistribution physics.

## 5. Classification

`CONFIRMED_LEGACY_BALANCE_BOOKKEEPING_DEFECT`

The defect affects:

- `Bapo(Redi,Ly)`;
- `Bapo(Ddev,Ly)`;
- cumulative organic-P balance deviation output;
- any qualification logic that interprets those legacy balance residuals.

The evidence does **not** show that the underlying ploughing redistribution state update loses organic P. The state redistribution in `Addit.for` is conservative for the investigated events.

This distinction matters. A corrected-legacy patch can likely repair the balance ledger without changing physical state trajectories, but equivalence must still be checked against a qualified reference executable and all affected output contracts.

## 6. ANIMO5 consequence

ANIMO5 should not maintain process balance accounting through loosely coupled parallel arrays whose individual terms can be omitted silently. Ploughing/tillage redistribution should be represented as explicit internal transfers in a mass ledger, with the donor and receiver sides generated from the same transaction.

Qualification should require:

1. internal redistribution sums to zero for every conserved element over a closed profile;
2. surface-reservoir removal and soil-layer additions are paired in one ledger transaction;
3. process state and diagnostic balance accounting are reconciled independently;
4. a balance-output bug cannot be mistaken for a physical process defect;
5. corrected-legacy output changes are documented even when state trajectories remain unchanged.

No production correction is admitted by PREP01. The frozen legacy behaviour remains evidence; the one-line accounting correction belongs in a separately qualified corrected-legacy workunit.
