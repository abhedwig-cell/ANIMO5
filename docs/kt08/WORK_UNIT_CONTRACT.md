# ANIMO-KT08 Work Unit Contract

Workunit: `ANIMO-KT08 — LWKM Full Explicit Hydrology Producer Sequence Evidence`.

Execution discipline: `RECONCILE -> ACQUIRE/MATERIALIZE -> QUALIFY -> REVIEW -> CLOSE`.

## Purpose

KT08 strengthens real-producer evidence without crossing the open KT06 runtime
semantics gate.

The bounded question is:

> Does the complete pinned LWKM Hlpimp=11 producer file define a finite,
> explicit-state, gap-free sequence of normalized KT03 hydrology packets, and
> can that complete sequence be cryptographically summarized so later coupling
> work can verify that it is using the same producer envelope?

KT08 is evidence/tooling only. It does not define how a runtime should consume,
retry, split, cache, select or publish multiple packets.

## Authorities

- KT03 authority:
  `ANIMO-KT03@c5d4c14fbd4ce77ed5ef369bb8ecaee0709ea3b8`;
- KT05 closeout:
  `3319e57adbf6036a86684f8e26d9559454c07b82`;
- KT07 closeout:
  `24dc3164c7832963d0b8931a8edf5155879a3f8d`;
- pinned LWKM `SWATRE.UNF` SHA-256:
  `b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c`.

KT06 is not consumed as qualified authority.

## Evidence boundary

The raw B0 producer file is not added to the repository. The committed
`reference/kt08/LWKM_SEQUENCE_SUMMARY.json` is B1 derived evidence.

The source materializer must parse every dynamic packet through the frozen KT03
adapter, invoke `HydrologyStep.validate()`, require complete
`Hydro_detailed` projection capability, and fail closed on any temporal chain
discontinuity.

Three aggregate SHA-256 identities compactly commit to the complete sequence:

1. the ordered list of all 1800 normalized typed-step digests;
2. the ordered list of all 1800 dynamic logical-record-group digests;
3. the ordered tuples of packet index, normalized endpoint, normalized
   duration, dynamic-group digest and typed-step digest.

Representative anchors are persisted for all four observed producer durations
and for positions across the sequence.

## Expected bounded producer facts

For this exact file only:

- Hlpimp=11;
- 30 layers;
- 30 horizons;
- 5 drainage systems;
- soil temperature present;
- 1800 packets;
- first producer interval origin 0 d;
- final endpoint 18263 d;
- no packet-chain gaps or overlaps after frozen KT03 diagnostic normalization;
- durations are 8, 9, 10 and 11 d with counts 37, 13, 1400 and 350;
- every packet has explicit interception storage;
- every packet has soil-temperature payload.

These are file-derived facts, not a generic producer grammar or runtime policy.

## Governance

KT08 changes no scientific state, runtime branching, checkpoint/restart
semantics, numerical policy, solver policy, accepted-state ownership or
production source.

Same-agent adversarial review is required and must remain labelled
`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

KT08 cannot satisfy or bypass the genuinely independent GOV04 Tier C review
still required by KT06.

## Exclusions

No B2 historical compiler equivalence, no Hlpimp=1 semantics, no generic
calendar conversion, no multi-packet forcing-provider design, no retry or
timestep-selection semantics, no `Hydro_detailed` execution, no ANIMO
scientific admissibility, no KT02/KT06 qualification, no production migration,
no B3/B4 admission and no Status A/AA claim.
