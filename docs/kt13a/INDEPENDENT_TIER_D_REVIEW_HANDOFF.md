# ANIMO-KT13A Independent Tier D Review Handoff

This handoff replaces the unremediated KT13 review target only after KT13A exact-head CI is green.

The candidate claim is:

`SELECTED_KT05_PACKET_PLUS_EXPLICIT_START_CHEMISTRY_AND_EXACT_SHARED_HETOP_CAN_DRIVE_ONE_BOUNDED_TCD042_INTERVAL_TO_ATOMIC_KT02_COMMIT`.

The reviewer must treat KT13A as a one-interval, selected-packet, nonproduction composition candidate. It is not a whole-model or provider-level claim.

The review must explicitly verify the cross-module geometry invariant introduced by KT13A: the `Hetop` used by the revision-53 hydrology execution and the `Hetop` used by TCD-042 science are exactly the same binary64 value. A tolerance is not acceptable here.

The reviewer must also verify transaction truth. Once KT02 has committed accepted state, the composition layer must not subsequently report a transactional failure merely because a diagnostic surface is unexpectedly unavailable.

Other mandatory axes are pinned in `integration/animo-kt13a/KT13A_INDEPENDENT_REVIEW_HANDOFF.json`, including the HYDROQ01-to-KT12 carrier mapping, Runinu continuation treatment, chemistry/hydrology ownership split, load-channel scope, dry-deposition exclusion and the unchanged B1/E1 TCD-042 admission envelope.

The following remain explicit nonclaims: canonical species-owner binding for the integer load channel, BOUNDARY parsing, chemistry-provider time provenance, first-call Runinu value, multi-interval continuation, canonical Runinu state, B2 historical equivalence, TB7, B4 and production.

A same-agent technical pass may be recorded only as `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`. It cannot satisfy the Tier D review gate.
