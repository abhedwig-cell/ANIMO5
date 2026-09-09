# TCD-016 surface-state activation seam

Work unit: `ANIMO-SQ01`

Status: `SOURCE_BOUND_SHARED_SURFACE_ACTIVATION_SEAM_RECONSTRUCTED`

Production migration: `NOT_ADMITTED`

## 1. Purpose

This note refines the TCD-016 interpretation after a read-only reinspection of the frozen revision-53 source.

The important correction is that the effective `0.1 mm` layer-0 threshold is not merely local to `Transsub.for`. The same surface-water threshold is used by the hydrological preprocessing to decide whether the ponding compartment is active.

The frozen source and historical testcase are unchanged.

Frozen source SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

## 2. Hydrological activation of layer 0

### Detailed hydrology

`Hydro_detailed.for` defines ponding activation as:

```fortran
If((Pnt+Snt).Gt.1.0d-4 .Or. (Pn+Snla).Gt.1.0d-4) Then
   Flpn = 1
Else
   Flpn = 0
End If

Mofro(0) = Amax1(0.0,(Pn+Snla)  / He(0))
Mofrt(0) = Amax1(0.0,(Pnt+Snt) / He(0))
Mofr(0)  = 0.5 * (Mofro(0) + Mofrt(0))
```

Thus `Flpn` is the source-level ponding activation flag and `1.0d-4 m` is its activation threshold. This equals `0.1 mm` of surface water.

### Aggregated hydrology

`Hydro_aggregated.for` uses the same threshold:

```fortran
If(Pnt.Gt.1.0d-4 .Or. Pn.Gt.1.0d-4)Then
   Flpn = 1
Else
   Flpn = 0
End If

Mofro(0) = Amax1(0.0,Pn  / He(0))
Mofrt(0) = Amax1(0.0,Pnt / He(0))
```

The `0.1 mm` threshold is therefore shared by both hydrological input routes in the supplied archive.

## 3. Transport uses the same effective layer-0 threshold

`Transsub.for` uses:

```fortran
Factor = 1.0d0
If(Ln.eq.0)Factor = 1.0d2
```

and tests:

```fortran
Mt*Ld <= 1.0d-6*Factor
```

For layer 0 this is:

`1.0d-6 * 100 = 1.0d-4 m = 0.1 mm`.

The exact algebraic expression is local to `Transsub`, but its effective surface threshold is aligned with the hydrological ponding activation boundary.

This changes the interpretation of the seam. TCD-016 is not simply a transport solver encountering a tiny arbitrary concentration denominator. It occurs when the solute representation crosses the same threshold used to deactivate the surface-water compartment in hydrology.

## 4. The canonical event crosses this shared activation boundary

For `Puitmijn_Cranendonck_60`, `TITO=1490`, layer 0:

```text
Mto = 5.435585e-4 m3 m-3
Mt  = 1.628217e-5 m3 m-3
Ld  = 0.2 m
```

The start and end areic water storages are:

```text
Mto * Ld = 1.087117e-4 m = 0.1087117 mm
Mt  * Ld = 3.256434e-6 m = 0.003256434 mm
```

Therefore the timestep moves from just above the shared `0.1 mm` activation threshold to well below it.

This is best described as a **surface-state deactivation transition**.

At exactly this transition, `Transsub` can set the resulting aqueous concentration to zero while no alternate surface NH4 mass state receives the residual mass.

That strengthens the Class-C interpretation: the missing object is a conserved state owner across deactivation of the mobile surface-water representation.

## 5. The tiny-outflow threshold remains Transsub-specific

Within the wet-to-low-storage branch, `Transsub` exports the remaining mass through the leaving-water concentration only if:

```fortran
Fu > 1.0d-6 m d-1
```

This equals `0.001 mm d-1`.

For the captured event:

```text
Fu = 4.1184400265e-10 m d-1
   = 4.1184400265e-7 mm d-1
```

The export threshold is therefore about `2428` times larger than the observed leaving-water flux.

Unlike the `0.1 mm` surface activation boundary, SQ01 found no matching hydrological activation use of this `Fu` threshold. It remains a `Transsub`-local export/conditioning policy in the supplied archive.

No recovered ANIMO theory derives it as a physical solute-export threshold.

## 6. A separate 1 mm dry-deposition routing threshold exists

`UBoundconc.for` contains an additional surface-routing distinction:

```fortran
If(Flpn.Eq.0 .Or. (Pn+Snla).Lt.1.0d-3)Then
   ! dry deposition goes to first soil compartment
Else If(Flpn.Eq.1 .And. (Pn+Snla).Ge.1.0d-3)Then
   ! dry deposition goes to layer 0
End If
```

`1.0d-3 m = 1 mm`.

The ANIMO 4.0 technical description independently states that `UBOUNDCONC` selects layer 0 or layer 1 depending on ponding and that dry deposition is added to the first soil compartment in the no-ponding case.

The source therefore has at least two surface-state routing scales:

- `0.1 mm`: activation of the ponding compartment and effective layer-0 low-storage threshold;
- `1 mm`: dry-deposition routing between layer 0 and the first soil layer in `UBoundconc`.

For the canonical TCD-016 event the start storage is about `0.109 mm`, so it is above the `Flpn` activation threshold but below the `1 mm` dry-deposition routing threshold.

This is a genuine semantic seam worth preserving in the evidence model. SQ01 does **not** claim that it caused the observed mass loss, because the TCD-016 residual is already causally localized to the `Transsub` dry-down branch and no dry-deposition contribution is needed to reproduce it.

No new TCD is opened here solely from the existence of the `1 mm` routing threshold.

## 7. Consequence for atomization

The corrected division of responsibility is:

### TCD-016-C1

Owns the physical state question at surface-water deactivation:

- hydrology can deactivate the ponding representation at the shared `0.1 mm` boundary;
- finite NH4 mass may still remain;
- the legacy state model has no alternate conserved surface owner for that mass.

The existing `0.1 mm` threshold may be treated as a **legacy representation activation boundary** for reconstruction purposes. It is not yet qualified as a physical chemical phase boundary.

### TCD-016-E1

Owns numerical behavior around the admitted state transition:

- how concentration-based transport approaches the activation boundary;
- whether and where a numerical representation switch is required;
- treatment of the `Fu > 1e-6 m d-1` export policy;
- continuity, conditioning, timestep sensitivity and precision sensitivity.

E1 may not decide the mass destination.

## 8. Current disposition

The new source evidence strengthens, rather than relaxes, the original blocker:

`TCD016_SHARED_SURFACE_STATE_ACTIVATION_SEAM_CONFIRMED`

`PHYSICAL_CONTINUATION_OWNER_MISSING`

`0_1MM_BOUNDARY_PHYSICAL_DERIVATION_NOT_RECOVERED`

`FU_EXPORT_THRESHOLD_PHYSICAL_DERIVATION_NOT_RECOVERED`

`TCD-016-C1 = BLOCKED_INSUFFICIENT_ANIMO_SPECIFIC_PHASE_THEORY`

`TCD-016-E1 = BLOCKED_DEPENDS_ON_TCD016_C1`

`PRODUCTION_MIGRATION = NOT_ADMITTED`
