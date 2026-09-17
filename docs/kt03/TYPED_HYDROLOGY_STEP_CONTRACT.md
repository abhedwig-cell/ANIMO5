# ANIMO-KT03 Typed Hydrology-Step Contract

Status: `CANDIDATE_NONPRODUCTION_ADAPTER_CONTRACT`.

This contract refines the earlier KT03 boundary map after exact revision-53 source and frozen CranMais record inspection. It remains bounded to the current nonproduction adapter proof.

## 1. Boundary

The seam is:

`legacy SWATRE.UNF -> file adapter + Input_hydro-compatible normalization -> HydrologyStep -> Hydro_detailed`

The carrier represents values that are actually delivered out of `Input_hydro` toward the downstream detailed-hydrology responsibility. It does not preserve file-record order as an API and it does not contain ANIMO chemistry or process state.

The future in-memory SWAP5 provider, if later admitted, should produce the same normalized typed carrier rather than emulate `SWATRE.UNF` bytes.

## 2. CranMais frozen layout

For the pinned `CranMais/Input/Swatre.unf`:

- source SHA-256: `538827d517f7be4c060e2d62131e1942f8e0e76fdeae49dc0268486984cc9eaf`;
- SWAP3 textual header records: 5;
- `Hlpimp=1`;
- hydrology period: 1974 through 1982, producer time 0.0 through 365.0;
- layers: 22;
- horizons: 5;
- drainage systems: 0;
- dynamic timestep count: 3287;
- dynamic records per timestep: 8;
- `Tiwa` sequence: exact 1 through 3287 in the diagnostic parser;
- `St=1` for all 3287 records;
- no groundwater sentinel below -9.98 occurs in this frozen case;
- the initial producer-temperature record marks `Ioptte=0` for the legacy reader.

These are bounded byte-derived facts for this exact file, not a general SWAP3 grammar claim.

## 3. Typed physical/input fields

The first carrier uses layout identity:

`ANIMO41_SWAP3_HYDROLOGY_STEP_V1`

It contains:

### Identity and dimensions

- layout id;
- `Hlpimp` source-layout identity;
- layer count;
- drainage-system count;
- source-record-group SHA-256.

### Interval identity

- `Tiwa`;
- `St` as timestep duration.

### Surface, atmosphere and lower-boundary producer quantities

- `Prr`;
- `Prsn`;
- `Prirr`;
- `Evicpr`;
- `Evicirr`;
- `Evsn`;
- `Evso`;
- `Evpn`;
- `Evsoma`;
- `Evtrma`;
- `Runon`;
- `Ru`;
- `Walet` after the legacy groundwater-sentinel normalization when applicable;
- `Pnt`;
- `Snt`;
- `Wabaer`.

### Profile arrays

- `Sc(1:Nl)`;
- `Mofrt(1:Nl)`;
- `Flev(1:Nl)`;
- `Flab(1:Nl+1)`;
- `Fldr(1:Nudr,1:Nl)`.

### Optional delivered values

- `Sict` availability and value;
- soil-temperature availability and `Te(1:Nl)` when `Ioptte=1`.

Availability is explicit. Missing values are not represented by invented sentinels.

## 4. Records deliberately not exposed as typed carrier fields

Exact source inspection corrected one part of the earlier candidate map.

For SWAP3, `Input_hydro` also reads `Soco`, `Lai`, `Dpro`, `Hecr` and `Avdate`. In revision 53 these are local variables in `Input_hydro`; they are not output arguments and are not consumed by `Hydro_detailed`. When `Ioptte=0`, the per-layer producer-temperature record is read into local `SDum` and discarded.

The file adapter still validates those records for completeness and framing because they are part of the legacy stream grammar, but they are not part of the normalized typed output contract. Exposing them would incorrectly turn dead/local file grammar into a shared coupling API.

## 5. Normalization ownership

The legacy reader converts explicit REAL(4) file values through `Dble_trunc`. KT03 includes a diagnostic reimplementation only to test the adapter seam.

That reimplementation is `B1_DIAGNOSTIC_ADAPTER_PROBE_NOT_B2`. It does not establish independently recovered Intel compiler behaviour and must not be used to claim B2 historical equivalence.

The groundwater sentinel rule remains adapter-owned: raw `Walet < -9.98` requires an explicit ANIMO profile-bottom value. The adapter fails closed if the sentinel occurs but that normalization input is absent.

## 6. Material unresolved compatibility issue: Sict

The CranMais file has `Hlpimp=1`. In that branch the dynamic SWAP3 record contains 18 REAL(4) values and does not contain `sSict`.

Revision-53 `Input_hydro` nevertheless executes `Sict=Dble_trunc(sSict)` after both the `Hlpimp==11` and other branches. For `Hlpimp=1`, `sSict` has not been populated by the current timestep record. `Hydro_detailed` subsequently uses `(Sict-Sic)` in the SWAP3 top-boundary and whole-profile water-balance equations.

KT03 therefore represents interception storage as unavailable for this layout and refuses to claim downstream `Hydro_detailed` compatibility. It does not synthesize zero, reuse a previous value or infer an interception state.

This is recorded separately as `KT03-F01`. A scientific/source disposition is required before a fully defined typed packet can drive `Hydro_detailed` for this layout.

## 7. Runtime relation

The model-neutral KT02 runtime does not know this field schema. It owns only generic transaction/interval mechanics. The ANIMO adapter owns the hydrology payload and its validation.

This keeps the architecture boundary intentional:

- runtime mechanics are model-neutral;
- hydrology exchange payload is ANIMO/coupling-domain specific;
- scientific downstream transformation remains ANIMO-owned;
- timestep selection, retry scale and solver policy remain outside this carrier.

## 8. Qualification boundary

KT03 may positively qualify file-to-typed reconstruction for the fields that are actually defined in the frozen CranMais layout. It may not positively qualify full `Hydro_detailed` call equivalence while `Sict` remains undefined for `Hlpimp=1`.
