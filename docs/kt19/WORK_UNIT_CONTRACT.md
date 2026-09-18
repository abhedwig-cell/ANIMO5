# ANIMO-KT19 Work Unit Contract

Workunit: `ANIMO-KT19 - Pinned LWKM PowerStation File to Immutable Hydrology Provider Qualification`.

Execution discipline: `RECONCILE -> MATERIALIZE PINNED SOURCE -> IMPLEMENT ADAPTER -> QUALIFY -> REVIEW -> CLOSE/HANDOFF`.

## Purpose

KT19 materializes the external-provider boundary identified by RG08.

It connects the exact supplied LWKM `SWATRE.UNF` byte source to an immutable typed packet provider without putting file I/O, record framing or source-byte ownership into the ANIMO kernel or accepted application state.

KT19 does not change KT11 central admission and does not connect this Python adapter directly to production.

## Program and evidence authority

Current program rebaseline:

`ANIMO-RG08@14109956b62376d0d0ab681e8c641c9e71d110bd`

Exact-final RG08 CI:

`35401743469 -> SUCCESS`

Producer-sequence evidence:

`ANIMO-KT08` with pinned source SHA-256:

`b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c`

and 1800-packet typed sequence identity:

`c17319d5a014d498335ed6d6736d0f10adffc4dc30fd3722b220e77dc2eaa5e4`.

Central runtime authorities remain unchanged:

- `ANIMO-KT06-A1@56384db4107aed484218363e26dbb7be7f51e8de`;
- `ANIMO-KT11-A1@50731bf118deb8ef1029f220a40b39a99240e480`.

## Reproducible source materialization

The project-supplied testbank archive is present outside the repository:

`ANIMO_testbank.zip`

SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Member:

`ANIMO_testbank/LWKM_gras_1040.2021.2045/input/SWATRE.UNF`

Member SHA-256:

`b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c`

Member size:

`2388124` bytes.

The full B0 producer source is intentionally NOT committed to Git.

## Implementation

KT19 adds:

`prototype/kt19/pinned_lwkm_file_provider.py`

The exact authoring implementation blob initially exercised against the external source is:

`9aa42bc124f7795d760e649163149447a07a4324`.

The provider:

1. verifies the full source SHA-256 before parsing;
2. reuses the existing PowerStation framing parser;
3. reuses the KT03 SWAP3 static and dynamic packet normalization contract;
4. requires the exact observed LWKM static envelope: Hlpimp=11, 30 layers, 30 horizons, 5 drainage systems and active temperature payload;
5. materializes all 1800 immutable `HydrologyStep` packets;
6. checks producer-chain continuity and exact whole-day integer metadata;
7. recomputes all three KT08 aggregate sequence identities and fails closed on any mismatch;
8. indexes packets by exact `(producer_endpoint_day, producer_step_days)`;
9. selects through an explicit runtime calendar identity and producer-day offset;
10. returns frozen typed packet values, not mutable file/parser state.

No source record position, file handle, retry state or accepted model state is exposed downstream.

## Real-source replay evidence

The exact project-uploaded source was replayed outside CI.

Observed:

- 23417 logical records;
- 23417 physical blocks;
- 1800 packets;
- all three KT08 aggregate sequence hashes matched exactly;
- all eight KT08 anchor packet typed digests matched through runtime-style interval selection.

Evidence is persisted in:

`integration/animo-kt19/KT19_EXTERNAL_SOURCE_REPLAY.json`.

This full-file replay is reproducible by anyone holding the pinned source bytes, but is not CI-self-contained because governance intentionally keeps B0 producer bytes out of Git.

## CI evidence

CI uses a small B1-derived real-source byte fixture:

`reference/kt19/LWKM_FIRST_PACKET_POWERSTATION_B1.b64`

It contains the exact original source prefix through the first complete packet group plus a synthetic PowerStation trailer.

It is not B0.

CI verifies:

- the fixture hash and framing;
- the full first real packet through KT03 normalization;
- exact first typed-packet digest;
- immutable provider selection semantics;
- calendar mismatch rejection;
- missing-interval rejection;
- non-integer runtime coordinate rejection;
- discontinuous-provider rejection;
- full pinned-provider rejection when the source hash is not the exact B0 file;
- KT19 constants against the persisted KT08 sequence authority.

## Evidence class and claim

KT19 is nonproduction external-provider runtime work.

A positive qualification may establish only:

`PINNED_LWKM_POWERSTATION_BYTES_CAN_BE_FAIL_CLOSED_MATERIALIZED_AS_THE_EXACT_KT08_TYPED_PACKET_SEQUENCE_AND_SELECTED_AS_IMMUTABLE_EXACT_WHOLE_DAY_FORCING`.

It does not establish B2 historical executable equivalence.

## Governance

Candidate risk tier:

`GOV04 Tier C external forcing/runtime adapter`.

Same-agent review may provide only:

`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Genuine independent Tier C review remains required before any central provider admission.

## Hard boundaries

No raw B0 source committed to Git.
No production source change.
No kernel file I/O.
No accepted-state file ownership.
No scientific process change.
No Hydro_detailed execution.
No retry/timestep policy.
No subday support.
No generic source layout outside the pinned LWKM Hlpimp=11 file.
No KT11 central-authority mutation.
No B2 claim.
No B3 mutation.
No TB7.
No B4.
No production.
No Status A or Status AA.
