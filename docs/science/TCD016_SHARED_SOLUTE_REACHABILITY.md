# TCD-016 shared solute reachability and scope guard

Work unit: `ANIMO-SQ01`

Status: `SOURCE_BOUND_SHARED_REPRESENTATION_REACHABILITY_RECONSTRUCTED_NO_NEW_TCD_ADMITTED`

Production migration: `NOT_ADMITTED`

## 1. Purpose

TCD-016 is an observed NH4 surface-layer dry-down conservation failure. The revision-53 source, however, routes several dissolved substances through the same layer-0 transport representation and the same `Transsub` low-storage transition.

This note answers a narrower question:

> Which substances are structurally able to encounter the TCD-016 representation seam, and which of those have actually been shown to exhibit the same mass-loss defect?

The distinction is mandatory. Shared code reachability is not equivalent to an observed discrepancy and does not by itself justify a new TCD.

Frozen source archive:

`ANIMO_4.1.5.53(3).zip`

SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

The archive was re-hashed before this continuation audit and was not modified.

## 2. Two-step surface deactivation lifecycle

The shared `0.1 mm` surface boundary has an important temporal consequence.

`Hydro_detailed.for` sets `Flpn=1` when either old or new ponding-plus-snow storage exceeds `1e-4 m`. `Hydro_aggregated.for` uses the same old-or-new rule for ponding storage.

Therefore a timestep that crosses from above to below `0.1 mm` still has:

`Flpn = 1`.

`TRANSPORT.FOR` and `Transgen.for` then use:

`K1 = 1 - Flpn`.

So layer 0 remains in the transport sequence during the crossing timestep.

At the start of the following timestep, `Init.for` promotes the resulting states:

- `Pn = Pnt`;
- `Mofro(Ln) = Mofrt(Ln)`;
- `Conh = Rsconh`;
- `Coni = Rsconi`;
- soluble-organic result concentrations to their accepted states;
- `Copo = Rscopo`.

If old and new surface water are then both below `0.1 mm`, hydrology sets `Flpn=0` and layer 0 is omitted from the normal solute transport sequence.

This means the crossing timestep is the legacy state machine's only explicit opportunity to move residual layer-0 solute into another persistent state before the ponding compartment becomes inactive.

For the canonical NH4 event, `Transsub` instead sets the resulting aqueous concentration to zero and no continuation owner receives the mass.

## 3. Generic `Transsub` branch reachability

For layer 0, `Transsub` uses an effective storage threshold of:

`1e-6 * 100 = 1e-4 m = 0.1 mm`.

The canonical TCD-016 hydrology is:

- `Mto*Ld = 1.087117e-4 m = 0.1087117 mm`;
- `Mt*Ld = 3.256434e-6 m = 0.003256434 mm`;
- `Fu = 4.1184400265397315e-10 m d-1`.

Thus the wet-to-low-storage branch is entered.

For a layer-0 substance with zero first-order disappearance and zero root/selectivity term, the difference between `HV1` and `HV` is only:

`Fu/Ld = 2.059220013269866e-9 d-1`.

`Transsub` defines `Small = 1e-8`. Therefore this case is classified as `Iflsol=2`.

In the wet-to-low-storage branch, because `Fu <= 1e-6 m d-1`, the routine sets:

```fortran
rsc = 0.0
...
if (Iflsol.eq.2) avc = 0.0d0
return
```

This control-flow result does not depend on the substance name. A conservative layer-0 solute with finite starting mass can therefore encounter the same zero-result representation loss under the same hydrological transition.

This is a structural reachability statement. It does not claim that every substance has the same reaction terms or that the supplied historical testbank naturally realizes the same event for every substance.

## 4. Substance route matrix

### 4.1 NH4-N

Main route:

`Animo -> Transport('AMMONIUM') -> Transsub`.

Layer 0 is included whenever `Flpn=1`.

Evidence level:

`OBSERVED_AND_REPRODUCED_DEFECT`.

The canonical `Puitmijn_Cranendonck_60` event establishes actual mass loss of:

`1.3880242022597072e-5 kg N m-2 = 0.13880242022597072 kg N ha-1`.

This remains the only substance for which SQ01 currently makes a historical TCD-016 defect claim.

### 4.2 Mineral phosphorus / orthophosphate

Main route:

`Animo -> Transgen('PHOSPHORUS')`.

For `Ln=0`, `Transgen` bypasses the soil sorption/precipitation routine and calls `Transsub` directly with:

- zero layer-0 root/selectivity term;
- zero first-order rate term;
- zero zero-order process term;
- zero bulk-density/sorption contribution.

Consequently, under the canonical TCD-016 hydrology, the same `Iflsol=2` low-storage control flow is structurally reachable for a finite layer-0 phosphate concentration.

Evidence level:

`SOURCE_CONFIRMED_STRUCTURAL_REACHABILITY_NOT_HISTORICALLY_ACTIVATED_IN_SQ01`.

No new PO4 TCD is opened by SQ01. In particular this finding must remain separate from:

- `TCD-019`, nonlinear phosphorus sorption numerical conservation;
- `TCD-024`, slow-Langmuir site indexing.

Those concern soil phosphorus process/numerical behaviour, whereas this note concerns surface aqueous-state deactivation.

### 4.3 NO3-N

Main route:

`Animo -> Transport('NITRATE') -> Transsub`.

Layer 0 is structurally included when `Flpn=1` and nitrate has no adsorbed layer-0 state in the `Transport` call.

However nitrate reaction coefficients can be modified by the aeration/denitrification route, including at the active surface index. Those coefficients affect the `Transsub` analytical-solution class and therefore the exact wet-to-low-storage result.

Evidence level:

`SHARED_SEAM_REACHABLE_EXACT_DELETION_NOT_ESTABLISHED`.

SQ01 therefore does not claim that nitrate necessarily reproduces the NH4 defect under the historical event.

This finding is separate from `TCD-015`, which concerns a negative-concentration transport algebra defect.

### 4.4 Soluble organic matter, soluble organic N and soluble organic P

`Transca.for` calls `Transport` for:

- `Sol.Org.Mat`;
- `Sol.Org.Nit`;
- `Sol.Org.Pho` when phosphorus is active.

These routes can include layer 0 when `Flpn=1` and therefore reach `Transsub`.

But a separate source-initialization seam prevents SQ01 from asserting identical low-storage behaviour without further qualification: several soil-derived reaction/sorption arrays are populated explicitly for `Ln=1..Nl`, while `Transca` constructs layer-0 calls using those shared arrays. This continuation audit does not classify that initialization issue or infer its runtime value.

Evidence level:

`SHARED_TRANSSUB_REACHABILITY_REQUIRES_SEPARATE_LAYER0_PARAMETER_INITIALIZATION_AUDIT`.

No DOM/DON/DOP discrepancy is created here.

### 4.5 GHG gases and other transport systems

CH4 and N2O use the GHG transport subsystem, not the `Transport/Transgen -> Transsub` layer-0 route qualified here.

Macropore water/solute transport also has its own `MapoTransport/MPTRANSP` state and transfer semantics even though it can interact with the main transport equation.

Evidence level:

`OUT_OF_TCD016_SHARED_TRANSSUB_SCOPE`.

No inference is made from TCD-016 to those subsystems.

## 5. Reachability is broader than the admitted discrepancy

The source evidence supports two statements simultaneously:

1. the missing state-owner problem is architecturally a surface-aqueous representation issue rather than an NH4-specific algebraic feature;
2. only NH4 currently has a qualified natural diagnostic demonstrating actual TCD-016 mass deletion.

Therefore the parent discrepancy remains:

`TCD-016 = NH4 surface-layer dry-down mass conservation`.

The wider finding is recorded as a **shared representation hazard**, not as a widened discrepancy identity.

A separate substance-specific TCD should only be opened when at least one of the following exists:

- a natural historical case showing nonclosure or incorrect state transition;
- a source-bound algebraic proof that is independent of unresolved species-specific reaction/state semantics;
- an explicit governance decision to create a generic surface-state discrepancy parent with separately qualified children.

SQ01 does not make that governance decision.

## 6. Historical origin search for the `0.1 mm` convention

The frozen files show the convention already present in the ANIMO 4.0/4.1 lineage markers:

- `Hydro_detailed.for`: ANIMO4.0 release history, SVN tag lineage `animo4.1.4`;
- `Hydro_aggregated.for`: same;
- `Transsub.for`: same, later SVN revision number but no explanatory history entry for the threshold.

The public WUR record for Alterra Report 983 confirms that it is the 2005 ANIMO4.0 process-description report. The WUR ANIMO product page also identifies Report 983 as the process-description reference and Report 224 as the user's guide.

Public indexing and the supplied user guide establish ponding-layer and surface-reservoir semantics, but SQ01 still has not recovered a derivation of `0.1 mm` as a physical chemical threshold or a rationale for the separate `Fu > 1e-6 m d-1` export test.

The direct eDepot target for Report 983 remained inaccessible to the available retrieval path during this continuation audit. Therefore no negative claim is made about text that was not inspected.

Current historical-origin status:

`0_1MM_CONVENTION_PRESENT_IN_ANIMO40_LINEAGE_BUT_ORIGIN_OR_PHYSICAL_DERIVATION_NOT_RECOVERED`.

## 7. Consequences for C1 and E1

### C1

C1 should define a surface continuation owner generically enough that its architecture does not hard-code NH4-specific storage mechanics unless theory requires that.

Scientific admission remains species-specific where chemistry differs. A common state topology does not imply common rewetting kinetics, reactions or phase identity across NH4, NO3, DOM and phosphate.

### E1

E1 should eventually qualify the numerical representation switch against at least:

- NH4, because the natural defect is established;
- a nonreactive synthetic conservative tracer or equivalent equation probe, to isolate representation policy;
- phosphorus layer 0, because the current source structurally supplies a zero-reaction direct `Transsub` path there.

That future qualification remains blocked until C1 fixes the physical state semantics.

## 8. Disposition

The continuation audit supports:

`TCD016_IS_AN_OBSERVED_NH4_INSTANCE_OF_A_SHARED_SURFACE_AQUEOUS_REPRESENTATION_HAZARD`.

It does **not** support:

`ALL_SOLUTES_HAVE_CONFIRMED_TCD016_MASS_LOSS`.

It also does not merge this seam with TCD-015, TCD-019, TCD-023 or TCD-024.

Current parent status remains:

`BLOCKED_TCD016_INSUFFICIENT_THEORY_FOR_CORRECTED_LEGACY_ADMISSION`.

Production migration remains:

`NOT_ADMITTED`.
