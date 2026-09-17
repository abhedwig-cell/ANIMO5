# ANIMO-KT03 Typed Hydrology-Step Contract

Status: `CANDIDATE_NONPRODUCTION_ADAPTER_CONTRACT`.

This contract refines the KT03 boundary after exact revision-53 source inspection, two frozen supplied SWAP3 hydrology cases, and adversarial review. It remains bounded to the nonproduction adapter proof.

## 1. Boundary

The seam is:

`legacy SWATRE.UNF -> legacy file adapter + Input_hydro-compatible normalization -> HydrologyStep -> ANIMO hydrology adapter -> Hydro_detailed`

The normalized `HydrologyStep` is deliberately independent of legacy file framing. A future in-memory SWAP5 producer can create the same payload without pretending to be `SWATRE.UNF` and without inventing a legacy record hash.

Legacy file identity is retained separately as adapter evidence.

## 2. Responsibility split

### Normalized payload

`HydrologyStep` owns only the normalized producer hydrology data needed across the external hydrology boundary, plus explicit schema/unit identities and capability flags.

Schema identity:

`ANIMO_HYDROLOGY_STEP_V1`

Unit-contract identity:

`ANIMO_HYDROLOGY_UNITS_V1`

### Legacy provenance

`LegacyStepProvenance` separately records:

- `legacy_layout_id = ANIMO41_SWAP3_RECORD_LAYOUT_V1`;
- `Hlpimp` for the observed legacy layout;
- SHA-256 of the exact logical-record group from which the payload was reconstructed.

These fields are not part of `HydrologyStep`. This prevents file grammar from becoming a requirement of future in-memory coupling.

## 3. Frozen real-file envelopes

### CranMais, Hlpimp=1

Pinned hydrology SHA-256:

`538827d517f7be4c060e2d62131e1942f8e0e76fdeae49dc0268486984cc9eaf`

Observed bounded layout:

- SWAP3 textual header;
- `Hlpimp=1`;
- 22 layers;
- 5 horizons;
- 0 drainage systems;
- 3287 dynamic timesteps;
- 8 logical records per timestep;
- producer endpoint sequence 1 through 3287;
- producer step duration 1 day throughout;
- `Ioptte=0`;
- no groundwater sentinel below `-9.98`.

The Hlpimp=1 dynamic first record has 18 REAL(4) values and does not contain `sSict`.

### LWKM, Hlpimp=11

Pinned hydrology SHA-256:

`b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c`

Observed bounded layout:

- SWAP3 textual header;
- `Hlpimp=11`;
- 30 layers;
- 30 horizons;
- 5 drainage systems;
- 1800 dynamic timesteps;
- 13 logical records per timestep;
- producer step durations 8, 9, 10 and 11 days;
- exact decimal producer endpoint/duration chaining across all 1800 packets;
- `Ioptte=1`;
- no groundwater sentinel below `-9.98`;
- explicit `sSict` in all dynamic first records.

These facts are byte-derived for the named frozen files. They are not a general grammar claim for every historical SWAP3 producer variant.

## 4. Producer time versus runtime time

The normalized payload carries:

- `producer_endpoint_day`, reconstructed from legacy `Tiwa`;
- `producer_step_days`, reconstructed from legacy `St`.

These values are producer-coordinate metadata and downstream scientific input where required. They are **not** authoritative KT02 runtime time.

A later runtime adapter must map and validate the producer interval against the exact runtime interval before an ANIMO attempt is executed. The packet itself does not advance time, select a timestep, request subdivision or authorize retry.

This avoids creating two competing time owners.

## 5. Normalized fields and units

The supplied ANIMO 4.0 user's guide Table 10 documents the legacy SWATRE exchange units for the original field family. KT03 preserves those units rather than silently converting them.

| Typed field | Legacy meaning | Contract unit |
| --- | --- | --- |
| `producer_endpoint_day` | `Tiwa` producer endpoint coordinate | legacy Julian-day coordinate |
| `producer_step_days` | `St` producer interval duration | d |
| `prr`, `prsn`, `prirr` | precipitation, snow and irrigation fluxes | m d-1 |
| `evicpr`, `evicirr` | interception evaporation fluxes | m d-1 |
| `evsn`, `evso`, `evpn` | snow, soil and ponding evaporation | m d-1 |
| `evsoma`, `evtrma` | potential soil evaporation and transpiration | m d-1 |
| `runon`, `runoff` | surface runon and runoff | m d-1 |
| `groundwater_level` | `Walet` at interval end | m relative to soil surface, legacy convention |
| `ponding_end` | `Pnt` | m |
| `snow_storage_end` | `Snt` water equivalent | m |
| `water_balance_aeration` | `Wabaer` | m |
| `sc` | soil moisture pressure head | cm |
| `mofrt` | volumetric water content | m3 m-3 |
| `flev` | compartment transpiration flux | m d-1 |
| `flab` | vertical water flux | m d-1 |
| `fldr` | drainage-system flux | m d-1 |
| `interception_storage_end` | `Sict` when explicitly supplied | m |
| `soil_temperature` | `Te` when active | degC |

The supplied 4.0 guide predates the revision-53 Hlpimp=11 `sSict` record extension. The metre dimension for `Sict` is also consistent with the admitted TCD-018 accounting relation, where `Sict-Sic` is a water-storage change converted from metres to millimetres for the reporting ledger. This does not resolve the Hlpimp=1 missing-value problem.

Future producers must convert to this unit contract before creating the payload. They must not rely on field-name similarity alone.

## 6. Fields deliberately excluded from the normalized payload

For SWAP3, `Input_hydro` also reads `Soco`, `Lai`, `Dpro`, `Hecr` and `Avdate`. In revision 53 these are local variables in `Input_hydro`; they are not output arguments and are not consumed by `Hydro_detailed`. When `Ioptte=0`, the per-layer producer-temperature record is read into local `SDum` and discarded.

The legacy file adapter validates these records for framing and completeness because they remain part of the input grammar. They are not promoted into the cross-model payload.

Likewise, `Hlpimp` and source-record SHA-256 remain adapter provenance rather than physical forcing.

## 7. Normalization ownership

The legacy reader converts explicit REAL(4) file values through `Dble_trunc`. KT03 includes a diagnostic reimplementation only to exercise the adapter seam.

Evidence class:

`B1_DIAGNOSTIC_ADAPTER_PROBE_NOT_B2`

This does not establish independently recovered Intel compiler behaviour and must not be used to claim B2 historical numerical equivalence.

The groundwater sentinel rule remains file-adapter owned: raw `Walet < -9.98` requires an explicit ANIMO profile-bottom value. The adapter fails closed if that normalization input is absent.

## 8. Hlpimp capability distinction

### Hlpimp=11

The legacy producer record explicitly contains `sSict`. The normalized payload marks interception-storage endpoint availability as true. All 1800 frozen LWKM packets can therefore construct the complete **file-derived subset** of the current `Hydro_detailed` call surface.

This is a structural projection claim, not scientific equivalence of `Hydro_detailed` execution.

### Hlpimp=1

The legacy producer record does not contain `sSict`. Revision-53 `Input_hydro` nevertheless assigns `Sict` from `sSict`, while `Hydro_detailed` consumes `(Sict-Sic)`.

KT03 marks interception-storage endpoint availability as false and refuses the complete file-derived `Hydro_detailed` projection. It does not synthesize zero, carry a previous value or infer interception storage.

This remains `KT03-F01` and requires a separate scientific/source disposition before full Hlpimp=1 downstream support can be claimed.

## 9. Downstream projection

`hydro_detailed_boundary()` projects only the external file-derived values consumed by the unchanged legacy `Hydro_detailed` responsibility. It does not supply ANIMO-owned geometry, accepted state, macropore state, diagnostics or derived state.

The projection therefore does not redefine ANIMO state ownership and does not make the adapter owner of downstream water-balance semantics.

## 10. Runtime relation

The model-neutral KT02 runtime does not know this field schema or any legacy file grammar. It owns generic transaction and interval mechanics only.

The intended composition is:

`KT02 exact interval authority -> ANIMO runtime adapter validates producer interval -> HydrologyStep forcing -> ANIMO scientific attempt -> KT02 commit/reject`

The separation remains:

- runtime mechanics are model-neutral;
- hydrology exchange payload is domain-specific;
- scientific downstream transformation remains ANIMO-owned;
- timestep selection, retry scale and solver policy remain outside this payload;
- legacy file framing and Hlpimp remain adapter provenance;
- a future SWAP5 in-memory provider need only satisfy the normalized schema and unit contract.

## 11. Qualification boundary

KT03 may qualify:

- reconstruction from the two named frozen legacy layouts into the normalized file-independent payload;
- separation of legacy provenance from physical forcing;
- explicit producer-time metadata without making it runtime authority;
- explicit unit-contract identity;
- complete file-derived `Hydro_detailed` projection for the bounded Hlpimp=11 LWKM envelope;
- fail-closed incomplete projection for Hlpimp=1.

KT03 does not establish B2 historical numerical equivalence, corrected Hlpimp=1 semantics, production migration, joint SWAP5-ANIMO timestep acceptance or a production shared runtime library.
