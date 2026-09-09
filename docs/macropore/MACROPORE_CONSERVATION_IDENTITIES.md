# Macropore conservation identities

Work unit: `ANIMO-MP01`

The identities below describe physical control volumes. They are not statements that the public revision-53 balance files implement those control volumes completely.

## 1. Sign and control-volume convention

For the isolated macropore control volume:

- positive external or matrix inflow is an input;
- positive macropore-to-matrix flow is an output;
- positive direct macropore drainage is an external output;
- storage is positive mass or water present in the macropore domains.

For a combined matrix + macropore control volume, matrix/macropore exchange is internal and must cancel.

## 2. Macropore water identity

For both macropore domains over one timestep:

`Delta S_mp = dt * (Q_mp,in - Q_mp,out)`

where revision 53 constructs conceptually:

`Q_mp,in = direct precipitation + routed runoff + matrix exfiltration`

and:

`Q_mp,out = macropore-to-matrix infiltration + Main Bypass drainage`

with:

`Delta S_mp = sum_d [SrWaMp(d) - SrWaMpOld(d)]`.

The exact specialized residual evaluated by `MAPOHYDRO` is equivalent to:

`MpDev = (FlMpInTo - FlMpOuTo) * St - sum_d(SrWaMp(d)-SrWaMpOld(d))`.

`MAPOHYDRO` warns when `abs(MpDev) >= 1e-5 m per timestep`.

That hard-coded warning threshold is legacy diagnostic behaviour. MP01 does not adopt it as an ANIMO5 acceptance tolerance.

## 3. Matrix/macropore water exchange identity

For each layer and domain, the source first interprets the sign of `FlMpOuIf`:

- negative `FlMpOuIf` becomes positive `FlMpInEf`, matrix -> macropore;
- nonnegative `FlMpOuIf` remains macropore -> matrix.

For a combined control volume:

`Q_matrix_to_mp - Q_mp_to_matrix`

must appear with the opposite sign in the matrix water equation. `MAPOHYDRO`, Task 2, modifies the matrix `Flou` and `Flid` terms accordingly.

Required invariant for migration:

`transfer_out(source) = transfer_in(destination)`

before any control-volume aggregation.

## 4. Main Bypass drainage partition

Revision 53 partitions domain-1 drainage into:

- `FlMpOuDrSo`, routed through soil;
- `FlMpOuDrMp`, direct macropore drainage.

with:

`FlMpOuDrMp = FlMpOuDr - FlMpOuDrSo`.

The complete macropore water control volume uses the full `FlMpOuDr` as outflow. A public combined-system ledger must not count `FlMpOuDrSo` twice, but it must count the direct component as an external output.

Domain 2 has no separate direct-drain input array in the revision-53 hydrological contract.

## 5. Macropore solute storage identity

For any transported dissolved quantity `X`:

`M_mp_old(X) = sum_d SrWaMpOld(d) * CoMpX(d)`

`M_mp_new(X) = sum_d SrWaMp(d) * RsCoMpX(d)`.

Applicable source states are:

- DOM: `CoMpDiorMa` / `RsCoMpDiorMa`;
- DON: `CoMpDiorNi` / `RsCoMpDiorNi`;
- DOP: `CoMpDiorPo` / `RsCoMpDiorPo`;
- NH4-N: `CoMpNh` / `RsCoMpNh`;
- NO3-N: `CoMpNi` / `RsCoMpNi`;
- PO4-P: `CoMpPo` / `RsCoMpPo`.

Units follow concentration times areic water storage and therefore produce areic mass.

## 6. Macropore solute balance

The species-generic `MAPOTRANSPORT` control volume is conceptually:

`surface input + matrix input + old storage = matrix output + direct drainage + new storage`.

Expanded:

`M_top + M_matrix_to_mp + M_mp_old = M_mp_to_matrix + M_direct_drain + M_mp_new`.

Vertical transport between virtual macropore compartments is internal and cancels over the profile.

The specialized routine explicitly forms old/new storage from water storage times accepted/result concentration and performs its own balance check.

## 7. Surface solute input

For precipitation-driven input, the kernel uses macropore precipitation flux multiplied by the corresponding precipitation concentration and timestep.

Runoff routed through the reservoir path contributes with the relevant top/reservoir concentration.

The exact species-specific boundary concentrations are supplied by the ordinary ANIMO transport orchestration. The generic macropore kernel does not own the scientific definition of those boundary concentrations.

## 8. Matrix exchange of solute

Matrix -> macropore mass transfer is constructed from matrix water flux and matrix concentration.

Macropore -> matrix mass transfer is constructed from the coupled average macropore concentration and water transfer to the matrix. The corresponding amount is also introduced into the matrix transport source/sink term.

For the combined matrix + macropore control volume:

`M_matrix_to_mp` and `M_mp_to_matrix`

are internal transfer events. They must not be counted as external gains/losses.

This is why a future typed-transfer ledger must carry both source and destination ownership rather than only a process label.

## 9. Direct-drain solute loss

For domain 1:

`M_direct_drain(X) = sum_layer FlMpOuDrMp(layer) * AvCoMpX(1) * St`

subject to the routine's timestep concentration evaluation.

This is external mass export from the matrix + macropore soil control volume.

The specialized `MAPOTRANSPORT` balance includes it. The public/main ledger integration is incomplete, which is the core of `TCD-025`.

## 10. Species identities

The same structural identity applies separately to:

- organic matter carried as labile DOM mass;
- N carried as DON;
- N carried as NH4-N;
- N carried as NO3-N;
- P carried as DOP;
- P carried as PO4-P.

There is no basis for allowing one species family to omit macropore storage or direct drainage merely because another family reports it.

## 11. Causal water diagnostics

MP01 directly compiled and executed the frozen `MAPOHYDRO.FOR` routine.

| Case | Inflow m | Outflow m | Storage change m | Residual m |
| --- | ---: | ---: | ---: | ---: |
| storage only | 0 | 0 | 0 | 0 |
| matrix exchange | 0.002 | 0.002 | 0 | 0 |
| direct drainage | 0 | 0.005 | -0.005 | 0 |
| precipitation to storage | 0.005 | 0 | 0.004999999999999999 | 8.67e-19 |

No `MAPOHYDRO` water-balance warning was emitted.

Classification:

`B1_CAUSALLY_EXERCISED_SPECIALIZED_WATER_CONSERVATION`.

## 12. Causal solute diagnostics

MP01 directly compiled and executed the frozen `MPTRANSP` kernel in `MAPOTRANSPORT.FOR`.

| Case | Old store | Inputs | Matrix out | Direct drain | New store | Residual |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| storage only | 0.020 | 0 | 0 | 0 | 0.020 | 0 |
| Internal Catchment exchange | 0.020 | 0.002 matrix | 0.003812692469220182 | 0 | 0.01818730753077982 | -3.47e-18 |
| Main Bypass direct drain | 0.020 | 0 | 0 | 0.010 | 0.010 | 0 |
| surface input to storage | 0 | 0.015 top | 0 | 0 | 0.015 | 0 |
| surface input plus matrix transfer | 0.010 | 0.006 top | 0.0023746150615596364 | 0 | 0.013625384938440364 | 0 |

No `MAPOTRANSPORT` balance warning was emitted.

Classification:

`B1_CAUSALLY_EXERCISED_SHARED_SOLUTE_KERNEL_CONSERVATION`.

The kernel is generic. The individual DOM/DON/DOP/NH4/NO3/PO4 orchestration call sites are source-supported, but MP01 did not execute six separate full ANIMO active-path cases.

## 13. Negative control

The active `GENERAL.INP` selected by `animo.ini` for each of the nine supplied B0 cases has:

`MacroPoreOption=0`.

This confirms TQ01's `natural_macropore_active_cases=0` result.

The supplied cases can therefore support only non-activation/non-interference statements for macropores. They cannot establish historical active-path conservation.

## 14. Persistent restart identity

A split-run conservation identity requires the restart representation to serialize every physical state needed at the split boundary.

For macropores, at minimum this includes:

- hydrological macropore water state supplied by the hydrological forcing/restart;
- macropore dissolved-solute concentrations for all active species.

`Init.for` supports in-memory promotion. However, `Output_Init.for` has the macropore `>MPnitr:`, `>MPorgs:` and `>MPphos:` write block commented out and its macropore arguments are removed/commented from the call surface.

Therefore:

`INITIAL.out(t_split)` is not a complete persistent representation of the active macropore solute state.

Classification:

`SOURCE_CONFIRMED_PERSISTENT_RESTART_INCOMPLETE_FOR_MACROPORE_SOLUTES`.

No continuous-versus-split active macropore B1 test is claimed.

## 15. Main-ledger identity required for TCD-025

For a public whole soil profile that includes macropores, the correct observer identity must contain:

`Delta S_matrix + Delta S_macropore = external inputs - external outputs + reactions/management terms`

with matrix/macropore exchange cancelled internally.

The observer must include:

- beginning macropore water and solute storage;
- ending macropore water and solute storage;
- direct macropore drainage as external export;
- no duplicate count of exchange or drainage routed back through soil.

Revision-53 `Outbal_calc` does not satisfy that complete identity. This is not a defect in the specialized local `MAPOHYDRO`/`MAPOTRANSPORT` closure demonstrated above. It is a mismatch between physical subsystem ownership and the public/main observer control volume.

## 16. Numerical-policy boundary

The tiny residuals observed in the controlled probes demonstrate algebraic/numerical closure for those selected values and compiler policy. They do not establish a general tolerance.

MP01 therefore does not convert `3.47e-18`, `8.67e-19`, or the legacy warning thresholds into acceptance criteria for ANIMO5.

Any future numerical tolerance belongs in a separate numerical qualification decision.
