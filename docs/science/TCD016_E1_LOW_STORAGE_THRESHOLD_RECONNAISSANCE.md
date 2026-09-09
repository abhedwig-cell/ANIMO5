# TCD-016-E1 low-storage threshold reconnaissance

Work unit: `ANIMO-SQ01`

Child qualification record: `TCD-016-E1`

Status: `SOURCE_BOUND_NUMERICAL_POLICY_RECONNAISSANCE_COMPLETE_ADMISSION_BLOCKED_BY_C1`

Production migration: `NOT_ADMITTED`

## 1. Scope

This note isolates the numerical and representation policy in revision-53 `Transsub.for` that surrounds the historical semi-analytical solute-transport equation.

It does not propose a replacement threshold and does not admit a numerical correction.

`TCD-016-E1` remains dependent on `TCD-016-C1`, because a numerical transition policy cannot decide the physical destination of residual mass.

## 2. Frozen source identity

Archive:

`ANIMO_4.1.5.53(3).zip`

SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Read-only archive scan shows the TCD-016 low-storage threshold expressions occur in `Transsub.for`.

Relevant source history:

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

The low-storage handling is separate source logic executed before the ordinary coefficient solution is completed.

This distinction supports classification of the threshold issue as numerical/representation policy rather than phase theory.

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

### 4.2 Water-storage transition threshold

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

The factor of 100 is therefore not dimensionless in effect: it deliberately makes the surface-compartment representation switch at a water storage 100 times larger than the soil-layer threshold.

No recovered theory source in SQ01 derives `0.1 mm` as a physical surface-water phase boundary.

### 4.3 Tiny-outflow threshold

Inside the layer-0 wet-to-low-storage branch, residual mass is routed to the average outflow concentration only when:

```text
Fu > 1e-6 m d-1
```

This equals:

`0.001 mm d-1`.

No recovered ANIMO process theory in SQ01 defines this value as a physical solute-export threshold.

## 5. Captured TCD-016 event relative to the thresholds

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

The layer-0 threshold is:

```text
1e-4 m = 0.1 mm
```

So the event moves from only about `1.0871` times the threshold to about `0.03256` times the threshold within one timestep.

This confirms that the branch is triggered by a representational cutoff around a small but nonzero ponding storage, not by exact disappearance of water.

The observed leaving water flux is:

```text
Fu = 4.11844e-10 m d-1
   = 4.11844e-7 mm d-1
```

The export threshold `1e-6 m d-1` is about `2428` times larger than the observed `Fu`.

Therefore the source selects the branch that sets `Rsc=0` and, for the observed `Iflsol=2`, `Avc=0`, while a finite residual NH4 mass still exists.

## 6. Threshold occurrence audit

A read-only scan of the frozen archive found:

- `Factor = 1e2` for layer 0 only in `Transsub.for`;
- `Fu > 1e-6` only in `Transsub.for`;
- `1e-6*Factor` low-storage tests only in `Transsub.for`.

This establishes that the TCD-016 cutoff is a local transport-solver policy surface in the supplied archive.

It does not establish when or why the constants were introduced historically.

## 7. Why E1 cannot be solved by deleting the thresholds

Simply lowering or removing the water-storage threshold is not sufficient.

As water storage approaches zero, a concentration-only state becomes badly conditioned for finite mass. At exactly zero water, finite aqueous mass cannot be represented by concentration at all.

Likewise, applying the existing outflow formula for every positive `Fu` closes mass but can generate the already observed pathological concentration of order `3.37e4 kg N m-3`.

Therefore E1 is subordinate to C1:

- C1 decides where mass physically resides when aqueous representation is unavailable;
- E1 decides how and when the numerical representation transitions between admitted states without introducing discontinuous mass loss or pathological conditioning.

## 8. Required E1 qualification envelope after C1

Once C1 semantics are fixed, E1 should test at minimum a two-dimensional envelope around:

- surface water storage approaching zero from above;
- leaving water flux approaching zero from above and below any candidate numerical switch.

Required observations per case:

- total conserved NH4 mass;
- aqueous mass;
- continuation-phase mass;
- aqueous concentration;
- boundary export mass;
- transition count and direction;
- timestep sensitivity;
- floating-point precision sensitivity;
- restart equivalence on either side of the switch.

The acceptance criteria must be derived from the admitted state equations and conservation identity, not from the current `0.1 mm` or `0.001 mm d-1` values.

## 9. Current E1 disposition

Source reconnaissance supports:

`LOW_STORAGE_THRESHOLDS_ARE_LOCAL_REPRESENTATION_OR_NUMERICAL_POLICY_SURFACES`

It does not support:

`LEGACY_THRESHOLD_VALUES_ARE_PHYSICAL_CONSTANTS`.

No replacement values are proposed.

Current status remains:

`TCD-016-E1 = BLOCKED_DEPENDS_ON_TCD016_C1`

and:

`PRODUCTION_MIGRATION = NOT_ADMITTED`.
