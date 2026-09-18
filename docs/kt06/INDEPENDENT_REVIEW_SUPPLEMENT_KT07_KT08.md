# ANIMO-KT06 Independent Review Supplement — KT07 / KT08 Producer Evidence

This supplement is review support only.

It does **not** change the frozen KT06 implementation/remediation target:

`fc818917a46408d55cd7f03e2fa8257534683907`

and it does not change the KT06 candidate claim, risk tier, qualification state
or required independent-review outcome.

## Why this supplement exists

At the time the KT06 implementation was frozen, its real-producer contact was
bounded to first-interval metadata while most `hydrology_step_t` values used
by the compiled KT06 probe test were synthetic finite values.

Two later evidence/tooling workunits strengthened that producer-side evidence
without modifying KT06 runtime semantics.

### KT07

`ANIMO-KT07 — LWKM Full Explicit Hydrology Packet Derived Fixture`

Qualified evidence head:

`2d469e0a00071b73207112222199eef82c96a961`

Closeout:

`24dc3164c7832963d0b8931a8edf5155879a3f8d`

Exact qualified-head CI:

`35288769233 -> SUCCESS`

Closeout CI:

`35288927837 -> SUCCESS`

KT07 establishes, at B1 derived-evidence level, that the complete first real
LWKM Hlpimp=11 normalized hydrology packet passes the frozen KT05 compiled
validator, projection and legacy-slice mapper.

Its exact verdict is:

`QUALIFIED_B1_DERIVED_FULL_LWKM_EXPLICIT_HYDROLOGY_PACKET_FIXTURE_AND_COMPILED_KT05_PROJECTION_NO_B2_OR_RUNTIME_OR_SCIENTIFIC_EQUIVALENCE`

This supports the independent reviewer when assessing whether the KT06
`hydrology_step_t -> KT05 projection` contact is merely synthetic. It does
not make KT07 part of the frozen KT06 implementation and does not prove KT06
runtime semantics.

### KT08

`ANIMO-KT08 — LWKM Full Explicit Hydrology Producer Sequence Evidence`

Qualified evidence head:

`6927d8f66bd5948797b163880a869ecc0be4c391`

Closeout:

`281dc65cbaceaa61d31f9cb731b3c5a733ca5d57`

Exact qualified-head CI:

`35291286873 -> SUCCESS`

Closeout CI:

`35291383064 -> SUCCESS`

KT08 establishes, at B1 derived-evidence level, a complete cryptographically
pinned 1800-packet Hlpimp=11 LWKM producer sequence with:

- first producer origin: 0 d;
- final endpoint: 18263 d;
- no normalized producer-coordinate chain discontinuities;
- durations 8 d, 9 d, 10 d and 11 d with counts 37, 13, 1400 and 350;
- explicit interception state in all packets;
- soil-temperature payload in all packets.

Its exact verdict is:

`QUALIFIED_B1_FULL_LWKM_EXPLICIT_HYDROLOGY_PRODUCER_SEQUENCE_IDENTITY_AND_TEMPORAL_ENVELOPE_NO_RUNTIME_PROVIDER_OR_B2_EQUIVALENCE`

KT08 is producer evidence only. It deliberately does not define packet
selection, forcing lifetime, retry identity, interval subdivision, calendar
mapping or publication policy.

## How the independent reviewer should use this evidence

KT07 and KT08 may be used to narrow question 8 in the original handoff:

- the frozen KT06 compiled probe still uses mostly synthetic packet values;
- however, the frozen KT05 boundary has now been exercised with a complete real
  first LWKM packet;
- and the full real producer sequence has now been independently summarized and
  pinned at B1 level.

The reviewer should therefore distinguish two questions:

1. **producer/contact evidence:** is the typed KT03/KT05 packet boundary grounded
   sufficiently in real supplied producer data for this nonproduction claim?
2. **runtime semantics:** does KT06 bind such a packet to KT02 correctly without
   changing time authority, accepted-state ownership or publication semantics?

Only the first question is strengthened by KT07/KT08. The second still requires
the genuinely independent Tier C review of KT06 itself.

## Explicit non-effects

This supplement does not:

- alter the frozen KT06 target;
- consume KT07 or KT08 as implementation dependencies;
- qualify a multi-packet forcing provider;
- qualify retry-aware packet identity;
- qualify calendar conversion;
- qualify subday/fractional mapping;
- qualify Hlpimp=1 semantics;
- execute `Hydro_detailed`;
- establish ANIMO scientific admissibility;
- promote KT06 to qualified, admitted, B3/B4, Status A or Status AA.

The required independent result remains one of:

- `PASS_CLAIM_UNCHANGED`;
- `PASS_WITH_NON_SEMANTIC_REMEDIATION`;
- `REOPEN_RUNTIME_SEMANTIC_CLAIM`;
- `NEGATIVE_DISPOSITION_REQUIRED`.
