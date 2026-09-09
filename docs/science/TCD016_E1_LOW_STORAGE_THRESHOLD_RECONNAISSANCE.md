# TCD-016-E1 low-storage threshold reconnaissance

Work unit: `ANIMO-SQ01`

Child qualification record: `TCD-016-E1`

Status: `SOURCE_BOUND_NUMERICAL_AND_SHARED_REPRESENTATION_POLICY_RECONNAISSANCE_COMPLETE_ADMISSION_BLOCKED_BY_C1`

Production migration: `NOT_ADMITTED`

## 1. Scope

This note isolates the numerical and representation policy in revision-53 `Transsub.for` around the historical semi-analytical solute-transport equation and reconciles it with the surface-water activation logic in the hydrological preprocessing.

It does not propose a replacement threshold and does not admit a numerical correction.

`TCD-016-E1` remains dependent on `TCD-016-C1`, because a numerical transition policy cannot decide the physical destination of residual mass.

## 2. Frozen source identity

Archive:

`ANIMO_4.1.5.53(3).zip`

SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Relevant `Transsub.for` source history:

- `$Id: Transsub.for 34 2013-03-11 10:17:47Z renau001 $`
- `$HeadURL: .../tags/animo4.1.4/Transsub.for $`
- history comments: 2003 release ANIMO4.0, 2011 release ANIMO4.1.

These are lineage markers, not scientific derivations of the thresholds.

## 3. Underlying equation versus guard policy

`Transsub` documents the differential equation:

```text
dc(t)/dt
+ HV1 / (MTO + RHBD*SOCF + HV*t) * c(t)
= HV2 / (MTO + RHBD*SOCF + HV*t)
```

The historical ANIMO 3.5 Report 144 numerical theory describes the same family of semi-analytical concentration equations and coefficient functions. Revision-53 `Detcoef` uses corresponding power, logarithmic and exponential forms.

The low-storage handling is additional source logic around that mathematical formulation.

A new source reconciliation shows that one part of this handling, the effective layer-0 `0.1 mm` storage threshold, is aligned with the hydrological ponding-activation boundary. It should therefore not be described as merely a local `Transsub` numerical cutoff.

## 4. Threshold family

### 4.1 General small-value constants

`Transsub` defines:

```text
Small   = 1e-8
Vsmall  = 1e-12
Vvsmall = 1e-20
```

`Small` is used to classify `HV` and `HV1` as numerically zero and therefore select one of five analytical solution forms.

These constants are plainly part of numerical branch selection.

### 4.2 Water-storage transition threshold in Transsub

The wet-to-low-storage branch is triggered by:

```text
Mt*Ld <= 1e-6*Factor
and
Mto*Ld > 1e-6*Factor
```

with:

```text
Factor = 1
Factor = 100 for Ln = 0
```

Because `Mt` and `Mto` are volumetric moisture contents and `Ld` is layer thickness, `Mt*Ld` and `Mto*Ld` have the dimension of areic water storage, metres of water.

Therefore the effective thresholds are:

- ordinary layers: `1e-6 m water = 0.001 mm water`;
- layer 0: `1e-4 m water = 0.1 mm water`.

### 4.3 Shared hydrological surface-activation threshold

`Hydro_detailed.for` sets `Flpn=1` when either old or new ponding plus snow storage exceeds `1.0d-4 m`; otherwise `Flpn=0`.

`Hydro_aggregated.for` uses the same `1.0d-4 m` threshold for old or new ponding.

Thus the effective layer-0 threshold in `Transsub` is aligned with the hydrological surface-water activation boundary:

`1.0d-4 m = 0.1 mm`.

The exact expression `1e-6*Factor` occurs in `Transsub`, but the effective `0.1 mm` boundary is a shared hydrology/transport representation convention in the supplied source.

No recovered ANIMO theory in SQ01 derives `0.1 mm` as a physical chemical phase boundary.

### 4.4 Tiny-outflow threshold

Inside the layer-0 wet-to-low-storage branch, residual mass is routed to the average outflow concentration only when:

```text
Fu > 1e-6 m d-1
```

This equals:

`0.001 mm d-1`.

A read-only archive scan found this TCD-016 `Fu` condition only in `Transsub.for`. No recovered ANIMO process theory in SQ01 defines it as a physical solute-export threshold.

## 5. Captured TCD-016 event relative to the shared activation boundary

For `Puitmijn_Cranendonck_60`, `TITO=1490`, layer 0:

```text
Mto = 5.435585e-4 m3 m-3
Mt  = 1.628217e-5 m3 m-3
Ld  = 0.2 m
Fu  = 4.1184400265397315e-10 m d-1
```

The areic water storages are:

```text
Mto*Ld = 1.087117e-4 m = 0.1087117 mm
Mt*Ld  = 3.256434e-6 m = 0.003256434 mm
```

The shared surface activation boundary is:

```text
1e-4 m = 0.1 mm
```

So the event moves from only about `1.0871` times the threshold to about `0.03256` times the threshold within one timestep.

This is not merely a solver approaching exact zero water. It is a transition across the source-defined surface-state activation boundary.

The observed leaving water flux is:

```text
Fu = 4.11844e-10 m d-1
   = 4.11844e-7 mm d-1
```

The export threshold `1e-6 m d-1` is about `2428` times larger than the observed `Fu`.

Therefore the source deactivates the layer-0 aqueous representation at the same scale used by hydrology while the transport-specific export guard refuses to assign the residual mass to the tiny leaving-water flux. `Rsc` becomes zero and, for the observed `Iflsol=2`, `Avc` also becomes zero.

## 6. Ancillary 1 mm dry-deposition routing threshold

`UBoundconc.for` contains a separate routing boundary:

```text
Flpn = 0 OR (Pn+Snla) < 1e-3 m
```

routes dry NH4/NO3 deposition to the first soil compartment, whereas:

```text
Flpn = 1 AND (Pn+Snla) >= 1e-3 m
```

routes dry deposition to layer 0.

This equals `1 mm`, ten times the `Flpn` activation threshold.

The supplied ANIMO 4.0 technical description independently states that `UBOUNDCONC` chooses the upper-boundary concentration for layer 0 or layer 1 depending on ponding and that dry deposition is added to layer 1 in the no-ponding case.

For the canonical TCD-016 event the start surface storage is about `0.109 mm`, so it lies above the shared `0.1 mm` activation boundary but below the `1 mm` dry-deposition routing boundary.

This is an additional surface-routing semantic seam. SQ01 does not claim it caused the observed TCD-016 mass loss, and no new TCD is opened from this fact alone.

## 7. Corrected policy interpretation

The threshold family must now be separated into three roles:

1. **Analytical small-value constants** such as `Small=1e-8`: local numerical branch selection.
2. **Shared `0.1 mm` surface activation boundary**: hydrology/transport representation policy controlling whether the ponding compartment is active/representable.
3. **`Fu > 0.001 mm d-1` export threshold**: `Transsub`-local policy deciding whether residual mass can be forced through the leaving-water concentration in the low-storage branch.

The shared `0.1 mm` boundary is source-defined behaviour and must be preserved as historical evidence. Its physical derivation is not established.

The `Fu` threshold remains a local numerical/export policy with no recovered physical derivation.

## 8. Why E1 cannot be solved by deleting either threshold

Simply lowering or removing the water-storage threshold is not sufficient.

As water storage approaches zero, a concentration-only state becomes badly conditioned for finite mass. At exactly zero water, finite aqueous mass cannot be represented by concentration at all.

Likewise, applying the existing outflow formula for every positive `Fu` closes mass but can generate the already observed pathological concentration of order `3.37e4 kg N m-3`.

Therefore E1 is subordinate to C1:

- C1 decides what owns conserved mass when the source deactivates the aqueous surface representation;
- E1 decides how the numerical transport representation behaves approaching, crossing and leaving that admitted state boundary.

The existence of a shared legacy activation boundary strengthens C1 rather than removing it.

## 9. Required E1 qualification envelope after C1

Once C1 semantics are fixed, E1 should test at minimum a two-dimensional envelope around:

- surface water storage below, at and above the shared `0.1 mm` legacy activation boundary;
- leaving water flux below, at and above any candidate export/conditioning switch, including the legacy `0.001 mm d-1` value as historical evidence rather than an acceptance target.

Required observations per case:

- total conserved NH4 mass;
- aqueous mass;
- continuation-phase mass;
- aqueous concentration;
- boundary export mass;
- surface activation state;
- transition count and direction;
- timestep sensitivity;
- floating-point precision sensitivity;
- restart equivalence on either side of the switch.

The acceptance criteria must be derived from the admitted state equations and conservation identity, not from defective historical residuals.

## 10. Current E1 disposition

Source reconnaissance now supports:

`0_1MM_LOW_STORAGE_BOUNDARY_IS_SHARED_SURFACE_REPRESENTATION_ACTIVATION_POLICY`

and:

`FU_EXPORT_THRESHOLD_REMAINS_TRANSSUB_LOCAL_NUMERICAL_OR_EXPORT_POLICY`.

It does not support:

`LEGACY_THRESHOLD_VALUES_ARE_PHYSICAL_CHEMICAL_CONSTANTS`.

No replacement values are proposed.

Current status remains:

`TCD-016-E1 = BLOCKED_DEPENDS_ON_TCD016_C1`

and:

`PRODUCTION_MIGRATION = NOT_ADMITTED`.
