# ANIMO-KT09 Qualification Report

## Disposition

KT09 qualifies representative B1 real-producer packet consumption through the
frozen KT05 compiled explicit hydrology boundary.

Exact verdict:

`QUALIFIED_B1_REPRESENTATIVE_REAL_LWKM_PACKETS_COMPILED_THROUGH_FROZEN_KT05_NO_COMPLETE_SEQUENCE_OR_RUNTIME_OR_B2_EQUIVALENCE`

Frozen qualified head:

`e54fc115fabb58da5e79fad33e1359717a5ed19c`

Exact-head GitHub Actions run:

`35293001679 -> SUCCESS`

## Qualified source envelope

Pinned source SHA-256:

`b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c`

Producer envelope:

- model header `V7.3.3.3`;
- Hlpimp=11;
- 30 layers;
- 30 horizons;
- 5 drainage systems;
- soil-temperature payload present.

## Qualified representative packets

Eight complete normalized producer packets are persisted for source indices:

`0, 2, 5, 41, 449, 899, 1349, 1799`.

The set spans all producer durations observed in KT08:

- 8 d;
- 9 d;
- 10 d;
- 11 d.

It also spans the first and final packet and intermediate sequence positions,
and includes nonzero explicit interception storage.

## Qualified identities

Canonical decompressed fixture SHA-256:

`fcb306cb4661139be0bc425db8fd4ff3d1d8d696a1a485c22dd6c67f5bb662b2`

Persisted compressed fixture text SHA-256:

`bb28e4f8ce0a23dfad497c4c52c4916fd6c30b322ad66b326db09d7d88f2ea13`

Every packet's typed-step digest and dynamic logical-record-group digest is
cross-checked against closed KT08 sequence evidence. The first packet is also
checked for exact normalized payload parity with the closed KT07 fixture.

## Qualified compiled proof

For every representative packet, the frozen KT05 implementation at

`69dd607ba1efa28de3f83cc963526021352b3311`

successfully:

1. validates the complete explicit `hydrology_step_t`;
2. projects the exact file-derived `Hydro_detailed` external subset;
3. preserves all projected scalar values;
4. preserves all projected arrays;
5. maps producer arrays into the legacy 1:N slices;
6. preserves ANIMO-owned index-zero legacy slices.

This strengthens the KT07 one-packet compiled proof across the real producer
sequence without claiming exhaustive compiled consumption of all 1800 packets.

## Evidence strength

Evidence class:

`B1_DERIVED_FROM_PINNED_B0_PRODUCER_NOT_B2`

KT09 does not qualify historical compiler behaviour. It consumes the frozen
KT03 diagnostic normalization exactly as already classified.

## Relationship to KT06

KT09 is separate producer/contact evidence. It neither modifies nor qualifies
KT06 runtime semantics.

The KT06 frozen review target remains:

`fc818917a46408d55cd7f03e2fa8257534683907`

and still requires genuinely independent GOV04 Tier C review.

KT09 can be shown to that reviewer as stronger evidence that the KT03/KT05
typed boundary is exercised with multiple complete real-derived packets. It
cannot be used as authority for time mapping, retry identity, packet selection,
forcing lifecycle or publication semantics.

## Review evidence

Same-agent assurance:

`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`

Final result:

`SELF_REVIEW_PASS_B1_REPRESENTATIVE_COMPILED_CONSUMPTION_TOOLING_ONLY`

No material finding remains open.

## Explicit nonclaims

KT09 does not qualify:

- complete compiled KT05 consumption of all 1800 producer packets;
- B2 historical compiler/executable equivalence;
- Hlpimp=1 or Hlpimp=2 semantics;
- `Hydro_detailed` scientific execution or numerical equivalence;
- ANIMO scientific admissibility;
- KT02 or KT06 runtime integration;
- a multi-packet forcing provider;
- retry or timestep-selection policy;
- generic calendar mapping;
- SWAP5 production coupling;
- production migration;
- B3/B4 admission;
- Status A or Status AA.

## Handoff

KT09 is closed as reusable representative B1 compiled-boundary evidence.

The main runtime lane remains blocked only at the KT06 genuinely independent
Tier C review boundary.
