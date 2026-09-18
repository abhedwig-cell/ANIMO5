# ANIMO-HYDROQ01 Qualification Rationale

HYDROQ01 addresses the precise seam discovered by KT12. KT05 ends on the producer-input side of `Hydro_detailed`, while TCD-042 consumes resolved values that exist only after `Hydro_detailed` and `Modflux`.

The source mapping is pinned to the frozen revision-53 archive and exact file hashes. It shows that `Flab(1)` is recalculated inside `Hydro_detailed`, `Modflux` converts that resolved value to nonnegative `Flib(1)`, and `UBoundconc` then forms TCD-042 top-reservoir throughflow from `Flib(1)+Rurv`.

For the bounded no-ponding branch, revision-53 runoff resolution leaves `Rurv` at exact zero before the `Modflux` call. The candidate carrier therefore makes that zero explicit and fail-closed, rather than dropping the field.

The compiled contract does not calculate any of those values. It merely requires an upstream scientific execution to identify itself and supply the already-resolved values for one exact runtime interval.

A successful HYDROQ01 qualification therefore means:

`THE_POST_HYDRO_DETAILED_TCD042_HYDROLOGY_SEAM_IS_EXPLICITLY_TYPED_AND_SOURCE_MAPPED`

It does not mean:

`HYDRO_DETAILED_OR_MODFLUX_HAS_BEEN_MIGRATED_OR_QUALIFIED_FOR_NEW_RUNTIME_EXECUTION`.

That distinction remains mandatory for later composition.
