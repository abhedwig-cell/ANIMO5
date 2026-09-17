# ANIMO-KT03 Typed Hydrology-Step Contract

Status: `CANDIDATE_NONPRODUCTION_ADAPTER_CONTRACT`.

This contract refines the KT03 boundary after exact revision-53 source inspection and two frozen supplied SWAP3 hydrology cases. It remains bounded to the nonproduction adapter proof.

## 1. Boundary

The seam is:

`legacy SWATRE.UNF -> file adapter + Input_hydro-compatible normalization -> HydrologyStep -> Hydro_detailed`

The carrier represents values that are actually delivered out of `Input_hydro` toward the downstream detailed-hydrology responsibility. It does not preserve file-record order as an API and it does not contain ANIMO chemistry or process state.

A future in-memory SWAP5 provider, if later admitted, should produce the same normalized typed carrier rather than emulate `SWATRE.UNF` bytes.

## 2. Frozen real-file envelopes

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
- `Tiwa=1..3287`;
- `St=1` throughout;
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
- variable `St` values 8, 9, 10 and 11 days;
- exact decimal interval-chain continuity across all 1800 packets;
- `Ioptte=1`;
- no groundwater sentinel below `-9.98`;
- explicit `sSict` in all dynamic first records.

These facts are byte-derived for the named frozen files. They are not a general claim for every historical SWAP3 producer variant.

## 3. Typed physical/input fields

The carrier uses layout identity:

`ANIMO41_SWAP3_HYDROLOGY_STEP_V1`

It contains the following responsibility groups.

### Identity and dimensions

- layout id;
- `Hlpimp` source-layout identity;
- layer count;
- drainage-system count;
- source-record-group SHA-256.

### Interval identity

- `Tiwa`;
- `St` as producer timestep duration.

The carrier records interval identity but does not select the timestep and does not own retry/subdivision policy.

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

### Capability-dependent delivered values

- `Sict` availability and value;
- soil-temperature availability and `Te(1:Nl)` when `Ioptte=1`.

Availability is explicit. Missing values are not represented by invented sentinels or inferred state.

## 4. Records deliberately not exposed as typed carrier fields

For SWAP3, `Input_hydro` also reads `Soco`, `Lai`, `Dpro`, `Hecr` and `Avdate`. In revision 53 these are local variables in `Input_hydro`; they are not output arguments and are not consumed by `Hydro_detailed`. When `Ioptte=0`, the per-layer producer-temperature record is read into local `SDum` and discarded.

The file adapter validates these records for completeness and framing because they remain part of the legacy stream grammar. They are not part of the normalized typed output contract. Exposing them would incorrectly turn local file grammar into a shared coupling API.

## 5. Normalization ownership

The legacy reader converts explicit REAL(4) file values through `Dble_trunc`. KT03 includes a diagnostic reimplementation only to test the adapter seam.

That reimplementation is classified:

`B1_DIAGNOSTIC_ADAPTER_PROBE_NOT_B2`

It does not establish independently recovered Intel compiler behaviour and must not be used to claim B2 historical equivalence.

The groundwater sentinel rule remains adapter-owned: raw `Walet < -9.98` requires an explicit ANIMO profile-bottom value. The adapter fails closed if the sentinel occurs but that normalization input is absent.

## 6. Hlpimp capability distinction

### Hlpimp=11

The producer record explicitly contains `sSict`. The typed packet therefore marks interception-storage endpoint availability as true and can construct the complete file-derived `Hydro_detailed` boundary for the bounded LWKM case.

All 1800 frozen LWKM packets satisfy that completeness gate.

### Hlpimp=1

The producer record does not contain `sSict`. Revision-53 `Input_hydro` nevertheless executes `Sict=Dble_trunc(sSict)` after the layout branch, while `Hydro_detailed` consumes `(Sict-Sic)`.

KT03 marks interception-storage endpoint availability as false for this layout and refuses the complete `Hydro_detailed` projection. It does not synthesize zero, carry a previous value or infer interception storage.

This source/layout gap is recorded as `KT03-F01` and requires a separate scientific/source disposition before full Hlpimp=1 downstream support can be claimed.

The typed contract therefore models a real capability distinction rather than hiding the legacy ambiguity.

## 7. Downstream projection

`hydro_detailed_boundary()` provides only the file-derived subset that the unchanged legacy `Hydro_detailed` call consumes. It requires the packet to be complete for that responsibility.

The projection does not include values that are supplied independently from ANIMO geometry/state or other model responsibilities. In particular, it does not redefine ANIMO state ownership and it does not make the adapter owner of downstream water-balance semantics.

## 8. Runtime relation

The model-neutral KT02 runtime does not know this field schema. It owns generic transaction and interval mechanics only. The ANIMO adapter owns hydrology payload validation and the mapping to ANIMO's external hydrology boundary.

The separation remains:

- runtime mechanics are model-neutral;
- hydrology exchange payload is ANIMO/coupling-domain specific;
- scientific downstream transformation remains ANIMO-owned;
- timestep selection, retry scale and solver policy remain outside this carrier;
- legacy file framing remains an adapter responsibility, not a runtime responsibility.

## 9. Qualification boundary

KT03 can qualify file-to-typed reconstruction for both observed frozen layouts and the complete file-derived downstream projection for the Hlpimp=11 LWKM envelope.

KT03 cannot qualify full Hlpimp=1 downstream compatibility while `Sict` remains undefined there. It also does not establish B2 historical numerical equivalence, production migration, joint SWAP5-ANIMO timestep acceptance or a production shared runtime library.
