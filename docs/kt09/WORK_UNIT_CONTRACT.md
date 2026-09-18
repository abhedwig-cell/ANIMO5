# ANIMO-KT09 Work Unit Contract

Workunit: `ANIMO-KT09 — LWKM Representative Real-Packet Compiled KT05 Consumption`.

Execution discipline: `RECONCILE -> MATERIALIZE -> QUALIFY -> REVIEW -> CLOSE`.

## Purpose

KT09 strengthens the producer-to-compiled-boundary evidence without entering
the blocked KT06 runtime-semantics lane.

The bounded question is:

> Do representative complete real Hlpimp=11 LWKM packets, spanning all observed
> producer duration classes and positions across the 1800-packet sequence, pass
> the frozen KT05 compiled validator, projection and legacy-slice mapper without
> value loss or index-zero ownership leakage?

KT09 is evidence/tooling only. It changes no ANIMO science and no runtime
semantics.

## Authorities

- KT03:
  `ANIMO-KT03@c5d4c14fbd4ce77ed5ef369bb8ecaee0709ea3b8`;
- frozen KT05 implementation:
  `69dd607ba1efa28de3f83cc963526021352b3311`;
- KT07 closeout:
  `24dc3164c7832963d0b8931a8edf5155879a3f8d`;
- KT08 closeout:
  `281dc65cbaceaa61d31f9cb731b3c5a733ca5d57`.

KT06 is not consumed as qualified authority.

## Representative envelope

The eight anchors are exactly those frozen by KT08:

`0, 2, 5, 41, 449, 899, 1349, 1799`.

Together they cover:

- first and last producer packets;
- 8 d, 9 d, 10 d and 11 d producer durations;
- quarter, midpoint and three-quarter sequence positions;
- both zero and nonzero explicit interception storage endpoints.

Each fixture packet is the complete normalized KT03 `HydrologyStep`, not only
metadata.

The persisted bundle is compressed base64 solely to keep the repository
compact. Integrity tests independently pin both the compressed text and the
decompressed canonical JSON SHA-256.

## Qualification proof

Every representative packet must:

1. match its KT08 dynamic-group and typed-step identities;
2. reconstruct and validate as a frozen KT03 `HydrologyStep`;
3. for anchor 0, exactly match the qualified KT07 full first-packet fixture;
4. pass frozen KT05 explicit-state validation;
5. pass frozen KT05 external `Hydro_detailed` projection;
6. preserve every projected scalar and array exactly;
7. pass frozen KT05 legacy-slice mapping;
8. preserve ANIMO-owned index-zero legacy slices.

## Governance

KT09 changes no scientific process, accepted state, time ownership, restart,
retry, timestep selection, solver/numerical policy or production composition.

Same-agent review must be labelled
`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

No independent GOV04 scientific/runtime review is created by this workunit.
KT09 cannot satisfy or bypass the independent Tier C review required by KT06.

## Exclusions

No B2 historical compiler equivalence, no complete 1800-packet compiled proof,
no runtime/provider semantics, no Hlpimp=1 semantics, no `Hydro_detailed`
scientific execution, no ANIMO scientific admissibility, no production
migration, no B3/B4 admission and no Status A/AA.
