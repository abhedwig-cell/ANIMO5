# ANIMO-KT12 Reconciliation

KT12 reconciles the admitted TCD-042 parent with the admitted nonproduction runtime lane.

The key finding is fail-closed: KT11 and KT05 carry inputs to `Hydro_detailed`, while TCD-042 consumes hydrology quantities that exist only after `Hydro_detailed` and `Modflux`.

Frozen revision-53 ordering is:

`typed producer forcing -> Hydro_detailed -> runoff/state reconciliation -> Modflux -> Flpn/Flib/Rurv -> UBoundconc(TCD-042)`.

For no-ponding TCD-042, revision-53 `Hydro_detailed` sets `Rurv=0`, but `Flab(1)` is recalculated inside `Hydro_detailed` before `Modflux` derives `Flib(1)=Max(0,Flab(1))`. The raw KT05 producer `flab(1)` is therefore not a qualified substitute for the resolved `Flib(1)`.

KT12 consequently implements the already admitted B1/E1 algebra only behind an explicit candidate resolved-hydrology carrier. This proves the scientific algebra can participate in KT02 transaction accept/reject semantics without putting average concentration into accepted physical state.

It does not establish the missing real hydrology producer for that carrier. Direct KT11 to TCD-042 composition remains blocked until a separate qualified post-Hydro_detailed output seam exists.

## Separate upper-boundary solute-load forcing seam

A second boundary is also explicit in frozen revision-53 `UBoundconc`. The `Load1...Load6` terms are not hydrology-only values. They combine hydrological quantities such as precipitation, irrigation, runon, run-in and `Rupr` with species-specific concentration forcings.

KT11 supplies hydrology packets only. It does not qualify precipitation chemistry, irrigation chemistry, runon chemistry or the already-composed solute `Load` consumed by TCD-042.

KT12 therefore treats `load_rate` as an explicitly supplied already-resolved process forcing. It does not derive it from KT11 and does not claim that the hydrology lane alone is sufficient for a complete TCD-042 execution.

The future end-to-end composition consequently needs two separately owned input surfaces before the TCD-042 client: a qualified post-`Hydro_detailed` resolved hydrology seam and a qualified upper-boundary solute-load forcing seam.
