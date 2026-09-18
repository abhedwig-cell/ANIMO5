# ANIMO-KT19 Independent Tier C Review Handoff

The independent review target is the frozen KT19 adapter package after exact-final CI.

Review the candidate claim:

`PINNED_LWKM_POWERSTATION_BYTES_CAN_BE_FAIL_CLOSED_MATERIALIZED_AS_THE_EXACT_KT08_TYPED_PACKET_SEQUENCE_AND_SELECTED_AS_IMMUTABLE_EXACT_WHOLE_DAY_FORCING`.

The reviewer should verify at minimum:

1. the exact B0 member SHA-256 is checked before parsing;
2. the raw B0 bytes are not committed to Git;
3. the PowerStation parser and KT03 normalization are reused rather than silently redefined in KT19;
4. all 1800 packets are required, not a subset;
5. all three KT08 aggregate identities are recomputed and required;
6. producer-chain discontinuity and duplicate interval identity fail closed;
7. packet selection uses explicit calendar identity and producer-day offset;
8. returned forcing is immutable;
9. the B1 first-packet fixture is correctly classified as derived evidence, not B0;
10. the external full-source replay evidence is not misrepresented as CI-self-contained or B2;
11. no KT11 central admission, science, B3, B4 or production authority is created;
12. any mismatch in source hash, static envelope or sequence identity prevents provider construction.

Same-agent review in the authoring context is not independent assurance.
