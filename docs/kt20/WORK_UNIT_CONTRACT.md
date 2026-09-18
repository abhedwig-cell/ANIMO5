# ANIMO-KT20 Work Unit Contract

Workunit: `ANIMO-KT20 - KT19 Pinned Provider Packet to KT18 Accepted-Application Bridge Qualification`.

Execution discipline: `RECONCILE -> MATERIALIZE -> BRIDGE -> QUALIFY -> REVIEW -> CLOSE/HANDOFF`.

## Purpose

KT20 closes the language/runtime seam between the qualified KT19 pinned real-file provider and the qualified KT18 provider-backed accepted application without changing either central KT11 provider semantics or the KT15A application model.

The bridge is deliberately bounded and nonproduction:

`KT19 immutable HydrologyStep -> exact adapter packet frame -> Fortran hydrology_step_t -> KT11 provider -> KT18 accepted application`.

## Current program authority

`ANIMO-RG08@14109956b62376d0d0ab681e8c641c9e71d110bd`

Exact-final RG08 CI:

`35401743469 -> SUCCESS`.

Upstream provider candidate:

`ANIMO-KT19@6245aad4aca962cb2a63d0394bb7f2baa686457d`

Upstream application candidate:

`ANIMO-KT18@42d8837f85acd0c4c9e29b323d8b2cb1bfdd4d72`.

Central provider authority remains:

`ANIMO-KT11-A1@50731bf118deb8ef1029f220a40b39a99240e480`.

## Adapter frame

KT20 introduces:

`ANIMO_KT20_HYDROLOGY_PACKET_FRAME_V1`

with role:

`NONPRODUCTION_ADAPTER_INTERCHANGE_NOT_CANONICAL_FORCING_ABI`.

The frame exists solely to move one already normalized immutable KT19 packet across the Python/Fortran qualification seam without decimal-format loss.

It is not a production protocol and not a canonical external-forcing ABI.

The frame records:

- frame schema and role;
- KT03 typed-step SHA-256 as provenance;
- hydrology schema and unit-contract identity;
- layer and drainage dimensions;
- every scalar as its exact IEEE binary64 hexadecimal identity;
- interception and temperature capability flags;
- every vector/matrix value in contract order;
- an explicit terminal marker.

The Python side exports and reparses the frame and recomputes the KT03 typed-step digest.

The Fortran side reconstructs every REAL64 through exact bit identity and then calls the existing KT05 validator.

Fortran does not independently recompute the Python JSON typed-step SHA-256. The digest is therefore provenance at this seam, while exact field identity is qualified by Python roundtrip plus cross-language bit reconstruction.

## Real-source evidence

CI uses only the existing B1-derived first-packet PowerStation fixture from KT19.

That fixture preserves the exact original source bytes for the first LWKM packet group and has expected typed packet identity:

`eeeb862839cce8111535fae86220d8574240804b9f6f029f7ec8e07ceb65da1c`.

The decoded real packet is used to initialize the Fortran KT11 provider and is selected by KT18 for the exact runtime interval.

The first real LWKM packet is NOT inside the currently admitted bounded TCD-042 application envelope. KT20 therefore expects that real-source packet to reach the application and then fail closed before publication.

That negative result is part of the qualification, not a defect.

## Positive bridge control

A separate synthetic packet uses the identical frame materialization and Fortran decoder but contains a bounded small forcing that is already inside the qualified TCD-042 application envelope.

It must commit through:

`frame -> Fortran packet -> KT11 -> KT18 -> KT15A atomic application`.

This positive control establishes bridge mechanics without misrepresenting synthetic forcing as historical evidence.

## Atomicity

For the real-source B1 packet:

- KT20 frame decoding must succeed;
- KT11 provider initialization and exact selection must succeed;
- KT18 must report that the provider packet was selected;
- the bounded scientific application must reject the packet if outside its current admitted envelope;
- accepted application generation, time and science state must remain unchanged.

For the synthetic control:

- the same bridge path must lead to one accepted application generation.

## Full pinned source boundary

KT19 already records successful external replay of all 1800 packets from the exact pinned B0 file.

KT20 does not commit that B0 file to Git and does not require it for CI.

A holder of the pinned source can use the KT20 `pinned-select` exporter to materialize any exact selected packet after KT19 performs the full source SHA-256 and sequence-identity validation.

This is reproducible external materialization, not CI-contained B0 custody.

## Governance

Candidate tier:

`GOV04 Tier D external-provider/application composition`.

Same-agent review provides only:

`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Genuine independent Tier D review remains required before any admission.

## Hard boundaries

No raw B0 source committed.
No production protocol.
No canonical forcing ABI.
No KT11 central authority mutation.
No science change.
No TCD-042 scope widening.
No claim that the first real packet is scientifically admitted.
No B2 claim.
No B3 mutation.
No TB7.
No B4.
No production.
No Status A or AA.
