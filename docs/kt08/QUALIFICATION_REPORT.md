# ANIMO-KT08 Qualification Report

## Disposition

KT08 qualifies a bounded B1 evidence object for the complete ordered
explicit-state hydrology sequence in the pinned LWKM Hlpimp=11 producer file.

Exact verdict:

`QUALIFIED_B1_FULL_LWKM_EXPLICIT_HYDROLOGY_PRODUCER_SEQUENCE_IDENTITY_AND_TEMPORAL_ENVELOPE_NO_RUNTIME_PROVIDER_OR_B2_EQUIVALENCE`

Frozen evidence/tooling head:

`6927d8f66bd5948797b163880a869ecc0be4c391`

Exact-head GitHub Actions run:

`35291286873 -> SUCCESS`

## Qualified source envelope

Pinned source:

`LWKM_gras_1040.2021.2045/input/SWATRE.UNF`

SHA-256:

`b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c`

Observed frozen producer properties:

- model header `V7.3.3.3`;
- Hlpimp=11;
- 30 layers;
- 30 horizons;
- 5 drainage systems;
- soil-temperature payload active.

## Qualified sequence facts

For this exact producer file and frozen KT03 diagnostic normalization:

- packet count: 1800;
- first interval origin: 0 d;
- first endpoint: 10 d;
- final endpoint: 18263 d;
- sum of all producer durations: 18263 d;
- chain discontinuities: 0;
- unique endpoints: 1800;
- explicit interception state: present in all packets;
- soil-temperature payload: present in all packets.

Duration histogram:

- 8 d: 37;
- 9 d: 13;
- 10 d: 1400;
- 11 d: 350.

Interception-storage endpoint summary:

- minimum: 0 m;
- maximum: 0.0002 m;
- nonzero packets: 652.

## Aggregate sequence identity

All 1800 normalized packets are compactly pinned through:

- typed-step sequence SHA-256:
  `c17319d5a014d498335ed6d6736d0f10adffc4dc30fd3722b220e77dc2eaa5e4`;
- dynamic-group sequence SHA-256:
  `40664a5fa73a980ad00b044bbce543b571b0e9302356f4b889dae2802deb2e34`;
- temporal-and-digest record sequence SHA-256:
  `eb14311a997129df4ae590ea1c72baecadcc2991ec0c3e8e313ed4ba3720ddc1`.

These aggregate identities allow later work to verify that a producer-sequence
artifact is exactly the one qualified here without committing the raw legacy
file or all packet payloads.

## Qualified tooling

KT08 includes a raw-source rematerializer which, when supplied the pinned B0
file, reconstructs every packet through the frozen KT03 parser, validates every
normalized packet, requires explicit-state downstream projection capability,
checks producer-coordinate continuity, and fails closed against the frozen
sequence identities and envelope.

CI verifies the persisted B1 summary and reruns the existing KT03, KT05 and
KT07 qualification tests. The raw B0 source is intentionally not stored in the
repository, so CI does not constitute independent raw-byte replay.

## Evidence strength

Evidence class:

`B1_DERIVED_FROM_PINNED_B0_PRODUCER_NOT_B2`

KT08 does not change the evidence strength of KT03
`legacy_dble_trunc_diagnostic`. Historical compiler behaviour remains outside
this claim.

## Relationship to runtime work

KT08 supplies stronger producer-side evidence for future coupling work, but it
does not define or qualify a multi-packet forcing provider.

In particular, a future runtime design must still independently decide and
qualify packet identity across retries, interval subdivision, packet selection,
calendar relation, cache lifetime and publication semantics.

KT06 remains:

`NOT_YET_QUALIFIED_UNDER_GOV04_TIER_C`

pending genuinely independent review of its frozen runtime-binding target.

## Review evidence

Same-agent assurance:

`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`

Final result:

`SELF_REVIEW_PASS_B1_FULL_SEQUENCE_EVIDENCE_TOOLING_ONLY`

KT08-R1 is closed and no material finding remains open.

## Explicit nonclaims

KT08 does not qualify:

- B2 historical compiler/executable equivalence;
- Hlpimp=1 or Hlpimp=2 semantics;
- producer grammar outside the pinned LWKM source;
- generic calendar mapping;
- KT02 or KT06 runtime semantics;
- a multi-packet forcing provider;
- retry or timestep-selection policy;
- `Hydro_detailed` execution or numerical equivalence;
- ANIMO scientific admissibility;
- SWAP5 production coupling;
- production migration;
- B3/B4 admission;
- Status A or Status AA.

## Handoff

KT08 is closed as reusable pinned B1 producer-sequence evidence.

The main runtime lane remains at the KT06 genuinely independent Tier C review
boundary. KT08 may be consumed by a later forcing-provider design only as
producer evidence, never as authority for runtime policy.
