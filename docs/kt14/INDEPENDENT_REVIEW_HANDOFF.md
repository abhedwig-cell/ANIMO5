# ANIMO-KT14 Independent Tier D Review Handoff

Review the exact frozen KT14 package after exact-head CI.

Candidate claim:

`A_SELF_VALIDATING_BOUNDQ02_CHEMISTRY_FRAME_BOUND_TO_EXACT_T0_T1_CAN_DRIVE_THE_REMEDIATED_KT13A_ONE_INTERVAL_TCD042_TRANSACTION_WITHOUT_STALE_FRAME_OR_DRY_DEPOSITION_LEAKAGE`.

Required review axes:

1. BOUNDQ02 frame validation occurs before any KT13A science.
2. Frame origin and endpoint identities are exact TIME02 identities.
3. Mutated forcing provenance is rejected before science.
4. KT14 passes only `boundary_frame%chemistry` into the wet/advective TCD-042 path.
5. Dry deposition remains visible but does not enter `Load1...Load6`.
6. BOUNDQ02 and KT13A frozen implementation blobs match their qualified upstream candidates.
7. The imported BOUNDQ01 no-P fixture is byte-identical to the pinned upstream fixture.
8. The repaired positive case uses exact binary64 oracles consistent with the source chemistry instead of an assumed direction of concentration change.
9. KT02 remains the sole accepted science-state publication authority.
10. A stale or invalid frame leaves the accepted TCD-042 store unchanged.
11. Boundary year cursor publication is not claimed atomic with science.
12. Multi-interval continuation, Runinu first-call resolution, canonical cursor state, B4 and production remain out of scope.

Same-agent assurance remains only:

`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

A material finding requires remediation and a new immutable review target.
