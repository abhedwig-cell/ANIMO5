# ANIMO-KT05 External Slice Indexing Contract

KT05 represents only producer-derived normalized hydrology data. Several revision-53 `Hydro_detailed` arrays have a legacy lower bound of zero, while `Input_hydro` fills the external producer data beginning at index 1.

The mapping is therefore explicit:

| Normalized KT03/KT05 field | Legacy target slice |
| --- | --- |
| `mofrt(1:Nl)` | `Mofrt(1:Nl)` |
| `flev(1:Nl)` | `Flev(1:Nl)` |
| `flab(1:Nl+1)` | `Flab(1:Nl+1)` |
| `fldr(1:Nudr,1:Nl)` | `Fldr(1:Nudr,1:Nl)` |

Legacy index-zero entries are **not producer data** in this contract. KT05 does not overwrite them.

The helper `apply_projection_to_legacy_slices` exists only to qualify this indexing boundary. It copies the normalized external slices into caller-owned legacy-shaped arrays and preserves index zero. It does not call `Hydro_detailed`, initialize ANIMO state, partition runoff, compute `Dif`, adjust `Evso`, execute macropore logic or call `Modflux`.

The mapping is tested with sentinel values at index zero. Any future wrapper that constructs a full legacy call frame must provide the ANIMO-owned index-zero/state values separately and must not infer them from the hydrology packet.
