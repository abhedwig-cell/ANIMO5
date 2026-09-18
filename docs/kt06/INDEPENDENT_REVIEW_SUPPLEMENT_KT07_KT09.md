# ANIMO-KT06 Independent Review Supplement — KT07 through KT09 Producer Evidence

This supplement supersedes the earlier KT07/KT08-only review supplement.

It is review support only. It does **not** change the frozen KT06
implementation/remediation target:

`fc818917a46408d55cd7f03e2fa8257534683907`

and it does not change the KT06 candidate claim, risk tier, qualification state
or required independent-review outcome.

## Why this supplement exists

At frozen KT06, real-producer contact was bounded to first-interval metadata
while most compiled probe packet values were synthetic finite values.

Three later evidence/tooling workunits strengthened only the producer/contact
side of that evidence without changing KT06 runtime semantics.

### KT07 — complete first real packet through frozen KT05

Qualified evidence head:

`2d469e0a00071b73207112222199eef82c96a961`

Closeout:

`24dc3164c7832963d0b8931a8edf5155879a3f8d`

Qualification CI:

`35288769233 -> SUCCESS`

KT07 established at B1 level that the complete first real LWKM Hlpimp=11
normalized hydrology packet passes the frozen KT05 compiled validator,
projection and legacy-slice mapper.

### KT08 — complete 1800-packet producer-sequence identity

Qualified evidence head:

`6927d8f66bd5948797b163880a869ecc0be4c391`

Closeout:

`281dc65cbaceaa61d31f9cb731b3c5a733ca5d57`

Qualification CI:

`35291286873 -> SUCCESS`

KT08 established at B1 level the complete ordered 1800-packet producer
sequence, including a gap-free normalized producer-coordinate envelope from
origin 0 d to endpoint 18263 d and observed durations 8, 9, 10 and 11 d.

KT08 deliberately did not define packet selection, forcing lifetime, retry
identity, interval subdivision, calendar mapping or publication policy.

### KT09 — representative complete real packets through frozen KT05

Qualified evidence head:

`e54fc115fabb58da5e79fad33e1359717a5ed19c`

Closeout:

`249066b7c07d505ba9a72a5aa199401a4349b0da`

Qualification CI:

`35293001679 -> SUCCESS`

Closeout CI:

`35293114491 -> SUCCESS`

KT09 extended the compiled KT05 contact from one real packet to eight complete
real-derived packets at source indices:

`0, 2, 5, 41, 449, 899, 1349, 1799`.

Those anchors span all four observed duration classes, first/final packets,
intermediate sequence positions and both zero and nonzero explicit
interception-storage endpoints.

Every representative packet passed the frozen KT05 validator, external
projection and legacy-slice mapper with exact preservation of projected B1
fixture values and index-zero ownership.

The exact KT09 verdict is:

`QUALIFIED_B1_REPRESENTATIVE_REAL_LWKM_PACKETS_COMPILED_THROUGH_FROZEN_KT05_NO_COMPLETE_SEQUENCE_OR_RUNTIME_OR_B2_EQUIVALENCE`

## How the independent reviewer should use KT07-KT09

The producer/contact limitation of frozen KT06 is now narrower than it was when
KT06 was authored:

- KT07 proves one complete real packet through the compiled boundary;
- KT08 pins the complete real producer sequence and temporal envelope;
- KT09 proves representative complete real packets from across that sequence
  through the compiled boundary.

This materially strengthens evidence that the KT03/KT05 typed packet boundary
is grounded in supplied real producer data.

It does **not** answer the Tier C runtime questions. The independent reviewer
must still decide whether KT06 correctly preserves:

- KT02 as sole accepted-time and publication authority;
- forcing outside accepted continuation state;
- fail-closed producer/runtime interval matching;
- atomic nonpublication on failed private intervals;
- bounded calendar/offset semantics;
- absence of hidden retry, forcing-lifecycle or timestep-policy assumptions.

## Explicit non-effects

KT07-KT09 do not become implementation dependencies of frozen KT06 and do not:

- alter the frozen target or candidate claim;
- qualify a multi-packet forcing provider;
- qualify retry-aware packet identity;
- qualify interval subdivision;
- qualify calendar conversion or subday mapping;
- qualify Hlpimp=1 semantics;
- execute `Hydro_detailed` science;
- establish ANIMO scientific admissibility;
- establish B2 historical compiler/executable equivalence;
- promote KT06 to qualified, admitted, B3/B4, Status A or Status AA.

The required independent result remains one of:

- `PASS_CLAIM_UNCHANGED`;
- `PASS_WITH_NON_SEMANTIC_REMEDIATION`;
- `REOPEN_RUNTIME_SEMANTIC_CLAIM`;
- `NEGATIVE_DISPOSITION_REQUIRED`.
