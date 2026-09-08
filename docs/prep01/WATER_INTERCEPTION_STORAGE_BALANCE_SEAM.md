# Water-balance interception-storage omission

Status: `CONFIRMED_LEGACY_BALANCE_INTERFACE_STATE_OMISSION`.

This note records PREP01 diagnostic evidence against the supplied revision-53 source and the deterministic LWKM execution. The frozen source, hydrology payload and testcase are unchanged.

## Observed envelope

The largest deterministic diagnostic water-balance period deviation occurs in the LWKM total-profile balance for the period ending in output year 2008:

`Bawa(Ddev) = -0.0601 mm`.

Because ANIMO consumes a complete external hydrologic water balance, the first hypothesis was that this deviation was inherited from the supplied SWAP/SWATRE hydrology payload. Source instrumentation shows that hypothesis is wrong.

## Whole-profile hydrology check

`Hydro_detailed.for` computes its own whole-profile water-balance deviation `Badev`. For the exact balance period corresponding to the `-0.0601 mm` output, summing all 36 hydrologic-step `Badev` values gives:

`-5.2640587582358e-5 mm`.

The largest single-step whole-profile deviation is only about `2.14e-4 mm`.

The external hydrology plus the adjustments made by `Hydro_detailed` therefore closes several orders of magnitude more tightly than the annual `Bawa(Ddev)` value. The `-0.0601 mm` is not inherited hydrology nonclosure.

## Missing state term

For detailed hydrology with interception/snow semantics (`Iopthyvs=1`), `Hydro_detailed.for` explicitly includes canopy/interception storage change in its full balance:

```text
... - (Sict-Sic) - (Pnt-Pn) - (Snt-Snla) ...
```

where `Sic` and `Sict` are initial and final interception water storage for a hydrologic step.

For the same annual balance period, diagnostic logging gives:

- first `Sic = 6.0e-5 m`;
- final `Sict = 0.0 m`;
- telescoping `Sict-Sic = -6.0e-5 m = -0.0600 mm`;
- inter-step storage discontinuity sum = `0.0 mm`.

Thus the missing interception-storage change is a real, continuous state transition, not a logging artefact.

## `Outbal_calc` interface omission

`Outbal_calc.for` constructs `Bawa(Ddev)` from precipitation, irrigation, runon/inundation, interception/snow/pond/soil evaporation, runoff, drainage, bottom fluxes and storage changes for:

- snow (`Stsn_b/e`);
- ponding (`Stpn_b/e`);
- soil moisture (`Stsm_b/e`).

It does not contain an interception-storage term. More fundamentally, `Sic` and `Sict` are not arguments of `Outbal_calc`, so the routine cannot close the detailed-hydrology control volume when canopy interception storage differs between balance-period endpoints.

Numerically:

```text
annual interception storage change  = -0.0600000000000 mm
sum Hydro_detailed Badev             = -0.0000526405876 mm
combined                             = -0.0600526405876 mm
formatted Bawa(Ddev)                 = -0.0601 mm
```

The observed annual deviation is therefore explained to output precision by the omitted interception storage plus the much smaller underlying hydrology residual.

Classification: `CONFIRMED_LEGACY_BALANCE_INTERFACE_STATE_OMISSION`.

This is not evidence that water mass disappeared from the externally supplied hydrology. It is a mismatch between the state covered by `Hydro_detailed` and the state exposed to the legacy `Outbal_calc` water ledger.

## Architectural consequence

ANIMO5 should not maintain a water or solute ledger whose control-volume state is a manually selected subset of the hydrology state. The coupling contract should expose all storage terms that can change across an accepted timestep, including interception and snow/canopy stores when those processes are active.

Qualification should require:

1. explicit ownership of every water store in the coupled control volume;
2. beginning/end storage for each active store;
3. exact cancellation of internal transfers;
4. independent comparison of imported hydrology closure and ANIMO's own ledger closure;
5. no promotion of this `0.0601 mm` residual to an acceptance tolerance.

A corrected-legacy implementation would need an explicit interception-storage input to the balance routine, or an equivalent conservative ledger interface. That correction is not admitted by PREP01.
