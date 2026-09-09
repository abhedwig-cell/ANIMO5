# Water-balance interception-storage omission

Status: `CONFIRMED_LEGACY_BALANCE_INTERFACE_STATE_OMISSION_CAUSALLY_CORRECTED_IN_DIAGNOSTIC_LEDGER_PROBE`.

This note records PREP01 diagnostic evidence against the supplied revision-53 source and the deterministic LWKM execution. The frozen source, hydrology payload and testcase are unchanged.

## Observed envelope

The largest deterministic diagnostic water-balance period deviation occurs in `LWKM_gras_1040.2021.2045/bawaTP.Out`, for the period ending in output year 2008:

`Bawa(Ddev) = -0.0601 mm`.

The total-profile annual series contains a distinctive pattern of approximately `+0.06` and `-0.06 mm` residuals in selected years, while many intervening periods close near `1e-4 mm` or better. Examples are 1993 `+0.0600`, 1996 `-0.0600`, 1997 `+0.0598`, 1998 `-0.0598`, 2002 `-0.0600`, 2004 `+0.0600`, 2008 `-0.0601` and 2014 `-0.0599 mm`.

Because ANIMO consumes an external hydrologic water balance, the first hypothesis was that this deviation was inherited from the supplied SWAP/SWATRE hydrology payload. Source instrumentation shows that hypothesis is wrong.

## Whole-profile hydrology check

`Hydro_detailed.for` computes its own whole-profile water-balance deviation `Badev`. For the exact balance period corresponding to the 2008 `-0.0601 mm` output, summing all hydrologic-step `Badev` values gives:

`-5.2640587582358e-5 mm`.

The external hydrology plus the adjustments made by `Hydro_detailed` therefore closes orders of magnitude more tightly than the annual `Bawa(Ddev)` value. The `-0.0601 mm` is not inherited hydrology nonclosure.

## Missing state term

For detailed hydrology with interception/snow semantics (`Iopthyvs=1`), `Hydro_detailed.for` explicitly includes canopy/interception storage change in its full balance:

```text
... - (Sict-Sic) - (Pnt-Pn) - (Snt-Snla) ...
```

where `Sic` and `Sict` are initial and final interception water storage for a hydrologic step.

`Outbal_calc.for` constructs `Bawa(Ddev)` from precipitation, irrigation, runon/inundation, interception/snow/pond/soil evaporation, runoff, drainage, bottom fluxes and storage changes for snow, ponding and soil moisture. It does not contain an interception-storage term. More fundamentally, `Sic` and `Sict` are not arguments of `Outbal_calc`.

For 2008:

```text
sum Hydro_detailed Badev              = -0.0000526405876 mm
initial interception storage Sic      = +0.0600000000000 mm
final interception storage Sict       =  0.0000000000000 mm
interception storage change           = -0.0600000000000 mm
combined                              = -0.0600526405876 mm
formatted Bawa(Ddev)                  = -0.0601 mm
```

The observed annual deviation is therefore explained to output precision by the omitted interception storage plus the much smaller underlying hydrology residual.

## Full-run annual reconciliation

Source-consistent instrumentation was extended over all 25 annual total-profile balance periods. For every period the following identity reproduces the legacy `BAWADV` to formatted-output precision:

```text
legacy Outbal residual
  = sum(Hydro_detailed Badev over the period)
  + (final interception storage - initial interception storage)
```

Selected examples:

| year | interception change (mm) | accumulated `Hydro_detailed` `Badev` (mm) | legacy `BAWADV` (mm) |
| --- | ---: | ---: | ---: |
| 1993 | `+0.060000` | `+5.79e-7` | `+0.0600` |
| 1996 | `-0.060000` | `+8.70e-6` | `-0.0600` |
| 2004 | `+0.060000` | `-2.66e-6` | `+0.0600` |
| 2008 | `-0.060000` | `-5.26e-5` | `-0.0601` |
| 2014 | `-0.060000` | `+5.57e-5` | `-0.0599` |

This repeated sign- and magnitude-matching pattern makes a chance numerical association implausible.

## Causal ledger-only probe

A temporary diagnostic copy extended `Outbal_calc` with an interception-storage ledger accumulator. For every top-of-profile balance period it accumulated:

```fortran
(Sict-Sic) * 1000
```

and subtracted the accumulated storage change when `Bawa(Ddev,Ly)` was finalized, resetting the accumulator with the existing balance-period reset semantics. No hydrologic state, flux, forcing, soil-water equation or testcase input was changed.

The characteristic `~0.06 mm` residuals disappear. Selected total-profile period residuals become:

- 1993: `+5.79e-7 mm`;
- 1996: `+8.70e-6 mm`;
- 1997: `-1.73e-4 mm`;
- 1998: `+1.83e-4 mm`;
- 2002: `+6.21e-6 mm`;
- 2004: `-2.66e-6 mm`;
- 2008: `-5.26e-5 mm`;
- 2014: `+5.57e-5 mm`.

The largest total-profile period residual after the probe is about `2.07e-4 mm`, on the same scale as the accumulated internal detailed-hydrology residual.

Classification: `CONFIRMED_LEGACY_BALANCE_INTERFACE_STATE_OMISSION`.

This is not evidence that water mass disappeared from the externally supplied hydrology. It is a mismatch between the state covered by `Hydro_detailed` and the state exposed to the legacy `Outbal_calc` water ledger.

## Architectural consequence

ANIMO5 should not maintain a water or solute ledger whose control-volume state is a manually selected subset of the hydrology state. The coupling contract should expose all storage terms that can change across an accepted timestep, including interception and snow/canopy stores when those processes are active.

Qualification should require:

1. explicit ownership of every water store in the coupled control volume;
2. beginning/end storage for each active store;
3. exact cancellation of internal transfers;
4. independent comparison of imported hydrology closure and ANIMO's own ledger closure;
5. balance-period reset and continuation coverage;
6. no promotion of the raw `0.0601 mm` residual to an acceptance tolerance.

A corrected-legacy implementation needs an explicit interception-storage contribution to the balance routine or an equivalent conservative ledger interface. That correction is not admitted by PREP01.
