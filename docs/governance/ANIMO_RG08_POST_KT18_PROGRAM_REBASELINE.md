# ANIMO-RG08 Post-KT18 Program Rebaseline

RG08 records the state after two further bounded runtime advances beyond RG07.

KT17 now provides real SHA-256 integrity checking for the bounded accepted checkpoint, including recomputed configuration, payload and manifest digests. It binds an externally supplied expected build identity and fixed source/testbank/documentation identities, while explicitly not claiming executable self-attestation or runtime rehashing of source artifacts.

KT18 now connects the admitted KT11 exact multi-packet provider to the bounded KT15A accepted application. Packet selection is read-only, returns a copy, is independent of storage order and remains revalidated by downstream KT06 against the immutable application configuration. Two provider-backed application intervals and negative atomicity cases are executable and green.

Neither advance is admission. Central admitted runtime authority remains KT06-A1 plus KT11-A1.

The current serial gate is no longer lack of a basic bounded application mechanism. It is genuine independent review followed by explicit per-candidate disposition/admission. RG08 therefore persists a frozen review-routing bundle but does not perform or simulate independent review.

The next external-provider engineering step is also now clear. KT08 already proves the complete pinned LWKM producer sequence identity for 1800 packets from a source file with SHA-256 `b48c6aaa...`, but the raw B0 producer file is intentionally not committed to the repository. A real-file or stream adapter can proceed only as a separate nonproduction workunit with reproducible access to that pinned source. The adapter must not turn local source availability into an unreviewed production or B2 claim.

Scientific closure remains independent: TCD-016, TCD-034 and TCD-040 are still unadmitted. Therefore B3, TB7, B4 and production remain closed and the programme denominator remains unqualified.
