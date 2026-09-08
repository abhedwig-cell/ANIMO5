# Water-balance omission of canopy interception storage

Status: `CONFIRMED_LEGACY_BALANCE_BOOKKEEPING_DEFECT_HYDROLOGY_STATE_REMAINS_CONSERVATIVE`.

This note records PREP01 diagnostic evidence against the supplied ANIMO 4.1.5 revision-53 source and deterministic LWKM testcase. The frozen source and testcase are unchanged.

## 1. Observed water-balance pattern

The deterministic balance envelope reports a maximum absolute water-balance period deviation of approximately `0.0601 mm` in `LWKM_gras_1040.2021.2045/bawaTP.Out`, year 2008.

The full-profile annual series contains a distinctive pattern of approximately `+0.06` and `-0.06 mm` residuals in selected years, while many intervening years close near `1e-4 mm` or better.

Examples:

- 1993: `+0.0600 mm`;
- 1996: `-0.0600 mm`;
- 1997: `+0.0598 mm`;
- 1998: `-0.0598 mm`;
- 2002: `-0.0600 mm`;
- 2004: `+0.0600 mm`;
- 2008: `-0.0601 mm`;
- 2014: `-0.0599 mm`.

This pattern is not consistent with random floating-point drift.

## 2. `Hydro_detailed` contains an interception-storage state

The detailed-hydrology route carries old and new canopy/interception water storage as `Sic` and `Sict`.

`Hydro_detailed.for` explicitly includes this storage change in its whole-profile water balance:

```fortran
Badev = ... -(Sict-Sic) -(Pnt-Pn) -(Snt-Snla)
```

for `Iopthyvs=1`.

It also uses `(Sict-Sic)/St` when reconciling the upper-boundary water flux. Thus interception storage is already part of the detailed-hydrology state and internal conservation check.

The supplied 4.0 User's Guide describes a complete soil-water-crop water balance including precipitation, irrigation, runon, snow, interception evaporation, soil/pond evaporation, transpiration, runoff, lower-boundary flow and drainage. The public `BAWA` output contract reports interception evaporation but has no record-1 term for interception storage.

## 3. `Outbal_calc` omits the storage change

`Outbal_calc.for` computes end storage for:

- ponding: `Stpn_e`;
- snow: `Stsn_e`;
- soil moisture: `Stsm_e`.

Its full-profile `Bawa(Ddev,Ly)` then subtracts the changes in those three stores, but it does not receive or account for `Sic`/`Sict`.

Therefore, when canopy interception storage differs between the beginning and end of a balance period, the public water-balance residual contains that storage change even though the detailed hydrology itself accounts for it.

## 4. Exact annual reconciliation

A source-consistent diagnostic build emitted, for every detailed-hydrology step:

- `Tito`;
- `St`;
- raw whole-profile `Badev`;
- `Sic`;
- `Sict`.

For every annual TP balance period in the 1991-2015 LWKM run, the following identity reproduces the legacy `BAWADV` to the precision of the formatted output:

```text
legacy Outbal residual
  = sum(Hydro_detailed Badev over period)
  + (final interception storage - initial interception storage)
```

with metres converted to millimetres.

### 2008 example

```text
sum Hydro_detailed Badev = -5.264058758e-05 mm
initial Sic              =  0.060000000000 mm
final Sict               =  0.000000000000 mm
interception delta       = -0.060000000000 mm
predicted Outbal residual= -0.060052640588 mm
formatted legacy BAWADV  = -0.0601 mm
```

The large apparent water-balance error is therefore almost exactly the unbooked loss of `0.06 mm` from canopy interception storage during that annual balance period.

Other years show the same behaviour. For example:

- 1993 interception delta `+0.060000 mm`, raw hydrology deviation `+5.79e-7 mm`, legacy output `+0.0600 mm`;
- 1996 interception delta `-0.060000 mm`, raw hydrology deviation `+8.70e-6 mm`, legacy output `-0.0600 mm`;
- 2004 interception delta `+0.060000 mm`, raw hydrology deviation `-2.66e-6 mm`, legacy output `+0.0600 mm`;
- 2014 interception delta `-0.060000 mm`, raw hydrology deviation `+5.57e-5 mm`, legacy output `-0.0599 mm`.

## 5. Causal ledger-only probe

A temporary diagnostic copy extended `Outbal_calc` with an interception-storage ledger accumulator. For each top-of-profile balance it accumulated:

```fortran
(Sict-Sic) * 1000
```

through the balance period and subtracted the accumulated storage change when `Bawa(Ddev,Ly)` was finalized. No hydrologic state, flux, forcing, soil-water calculation or process equation was changed.

The characteristic `~0.06 mm` residuals disappear.

For TP, selected results become:

- 1993: `+5.79e-7 mm`;
- 1996: `+8.70e-6 mm`;
- 1997: `-1.73e-4 mm`;
- 1998: `+1.83e-4 mm`;
- 2002: `+6.21e-6 mm`;
- 2004: `-2.66e-6 mm`;
- 2008: `-5.26e-5 mm`;
- 2014: `+5.57e-5 mm`.

The largest TP period deviation after the probe is approximately `2.07e-4 mm`, matching the scale of the accumulated internal `Hydro_detailed` residual rather than the omitted canopy-store change.

Across the other LWKM balance profiles the corrected diagnostic residuals likewise remain near the internal hydrology residual scale.

## 6. Classification

`CONFIRMED_LEGACY_BALANCE_BOOKKEEPING_DEFECT`

The defect affects the public ANIMO water-balance ledger and cumulative deviation when detailed hydrology carries nonzero interception storage across a balance-period boundary.

The evidence does **not** demonstrate loss of water from the hydrologic state. `Hydro_detailed` already includes `Sic/Sict` in its internal whole-profile conservation equation and its raw residual remains very small.

This is therefore a reporting/ledger omission, not a demonstrated SWAP/ANIMO hydrology-state defect.

## 7. Qualification consequence

The legacy `0.0601 mm` maximum must not be used as a water-conservation acceptance threshold. It contains a deterministic omitted state term.

A corrected-legacy water ledger should explicitly include every storage compartment that participates in the selected boundary system, including interception storage when detailed hydrology provides it.

ANIMO5 should represent conserved water stores and boundary fluxes through an explicit ledger contract rather than a fixed set of partially parallel output arrays. At minimum qualification must distinguish:

1. state conservation inside the hydrology adapter;
2. transfer of hydrology state into ANIMO;
3. balance-reporting completeness;
4. balance-period reset/continuation semantics;
5. output-format rounding from unrounded internal residuals.

No production correction is admitted by PREP01. The correction belongs in separately qualified corrected-legacy work.
