# ANIMO-KT19 Qualification Rationale

KT08 already proves the identity and temporal envelope of all 1800 packets in the exact LWKM producer file. KT11 already proves an in-memory immutable multi-packet provider. RG08 identifies the remaining external-provider engineering gap: reproducibly turning the actual supplied file into that typed packet responsibility.

KT19 closes that gap without placing legacy file grammar in the kernel.

The adapter is source-pinned twice. It first checks the full file SHA-256. It then reconstructs every normalized packet and recomputes the three independent KT08 aggregate sequence identities. A file with the right framing but the wrong content cannot pass by matching only a header or packet count.

Packet selection is read-only and exact whole-day. Runtime calendar identity and producer-day offset remain explicit. The returned Python `HydrologyStep` is frozen and contains tuples, so downstream code cannot mutate provider-owned forcing in place.

The full B0 source remains external. This is intentional. GitHub CI therefore cannot replay the entire 2.3 MB source. CI instead exercises the exact adapter on a B1-derived first-packet raw-byte fixture and verifies all pinned constants against KT08. A separate external replay record confirms that the exact KT19 provider blob successfully materialized the project-uploaded full source and reproduced every KT08 aggregate and anchor identity.

The evidence still remains below B2: it does not reconstruct the historical compiler/executable route.

Positive qualification should therefore be interpreted as a bounded external adapter result, not as production input admission.
