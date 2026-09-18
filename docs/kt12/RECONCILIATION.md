# ANIMO-KT12 Reconciliation

KT12 reconciles the admitted TCD-042 parent with the admitted nonproduction runtime lane.

The key finding is fail-closed: KT11 and KT05 carry inputs to `Hydro_detailed`, while TCD-042 consumes hydrology quantities that exist only after `Hydro_detailed` and `Modflux`.

Frozen revision-53 ordering is:

`typed producer forcing -> Hydro_detailed -> runoff/state reconciliation -> Modflux -> Flpn/Flib/Rurv -> UBoundconc(TCD-042)`.

For no-ponding TCD-042, revision-53 `Hydro_detailed` sets `Rurv=0`, but `Flab(1)` is recalculated inside `Hydro_detailed` before `Modflux` derives `Flib(1)=Max(0,Flab(1))`. The raw KT05 producer `flab(1)` is therefore not a qualified substitute for the resolved `Flib(1)`.

KT12 consequently implements the already admitted B1/E1 algebra only behind an explicit candidate resolved-hydrology carrier. This proves the scientific algebra can participate in KT02 transaction accept/reject semantics without putting average concentration into accepted physical state.

It does not establish the missing real hydrology producer for that carrier. Direct KT11 to TCD-042 composition remains blocked until a separate qualified post-Hydro_detailed output seam exists.
