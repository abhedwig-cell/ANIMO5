# ANIMO-GHG01 — CH4 plant-mediated transport initialization audit

Status: `SOURCE_CONFIRMED_ACTIVE_CH4_PLANT_TRANSPORT_USE_BEFORE_DEFINITION_REFERENCE_UNEXERCISED`

This post-closeout audit isolates a source-level initialization defect in the active revision-53 methane route. It does not infer historical executable values, select a replacement expression, or admit a production correction.

Frozen source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Rechecked relevant source-file SHA-256:

- `ghg_ch4.for`: `00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98`.

## 1. Active source path

`GHG_Methane` is called from the active `GHGasses(1)` route when `IoptGHG>=1`. Plant-mediated transport is therefore part of the source-reachable GHG process path, not a dormant output-only branch.

The routine declares local integer `Ln` and local reals `Te50`, `Temat` and `fGrow`. Before the first assignment to `Ln` in the routine, revision 53 executes:

```text
Te50  = Te(Ln)
Temat = Tegr + 10.0
If (Te50.Lt.Temat) Then
   If (Te50.Gt.Tegr) Then
      fGrow = 4.0 * (1.0 - ((Temat-Te50)/(Temat-Tegr))**2.0)
   Else
      fGrow = 0.0
   Endif
Else
   fGrow = 4.0
Endif
```

Only afterwards does the first `Do Ln = ...` loop assign `Ln`.

The input parser documents `Tegr` as the temperature at which plant growth starts. The source then uses `fGrow` for every root-zone compartment in:

`K1plant(Ln) = Kpl * FvegCH4 * fRoot * fGrow`.

`K1plant` is passed to `GHGtransport` and later used to calculate both plant CH4 oxidation and plant-mediated CH4 emission.

## 2. Source-semantic finding

There is no source-defined value of local `Ln` before `Te(Ln)` is read.

Therefore the temperature selected for `Te50` is not defined by the Fortran source semantics at that point. Depending on compiler, storage and runtime state, the read can use an indeterminate index, a retained implementation-dependent value, or trigger a bounds/runtime failure under diagnostics.

The historical Intel local-storage contract is not sufficiently recovered to translate this source defect into a historical numerical value. Even if a particular compiler happens to retain a previous `Ln`, that retained value is not an explicit model-state or input contract.

Classification:

`SOURCE_CONFIRMED_USE_BEFORE_DEFINITION_IN_ACTIVE_CH4_PLANT_TRANSPORT_PATH_REFERENCE_UNEXERCISED`

Local reconciliation key:

`GHG01-LCL-CH4-PLANT-GROWTH-TEMPERATURE-INDEX`

## 3. Scientific impact boundary

The defect can affect the common growth multiplier applied to all root-zone plant-mediated CH4 transport coefficients in a call. Those coefficients participate in:

- plant-mediated CH4 extraction from the soil-gas/liquid system through `GHGtransport`;
- `QOxCH4Plt`, the fraction oxidised during plant transport;
- `QEmCH4Plt`, the plant-mediated atmospheric emission flux.

Thus the issue is potentially mass-transfer relevant, not only diagnostic/reporting relevant.

However, the intended temperature location represented by the local name `Te50` is not established by this source audit. No replacement such as `Te(1)`, a 50-cm interpolated temperature, or any other index is admitted without stronger ANIMO-specific theory or source-history evidence.

## 4. Qualification boundary and required closure

Before correction or B3 admission:

1. recover the detailed ANIMO GHG derivation or source history that defines the intended plant-growth temperature state;
2. obtain a revision-53-compatible activated GHG testcase;
3. instrument the first read of `Ln`, `Te50`, `fGrow`, `K1plant`, `QOxCH4Plt` and `QEmCH4Plt` under the qualified build contract;
4. use compiler/runtime diagnostics only as B1 causal evidence, not as historical B2 reference;
5. qualify any candidate correction against the intended scientific state definition, not merely against removal of an uninitialized read.

Historical runtime magnitude remains `REFERENCE_BLOCKED`.

No production migration or B3 admission is permitted from this finding alone.
