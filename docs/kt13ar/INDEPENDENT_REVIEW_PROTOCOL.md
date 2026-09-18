# ANIMO-KT13AR Independent Tier D Review Protocol

This branch is only a review scaffold. It was prepared by the authoring context and therefore contains no independent scientific verdict.

The immutable review target is:

`ANIMO-KT13A@df2310cc69e3fe16187ba2235843222f8acfb726`

Its exact-head GitHub Actions run is:

`35370974894 -> success`

The frozen substantive composition is:

`95dead10d7e017b7f46b2ce3f85704df134bb0e0`

with composition-module blob:

`6e2e4c73e9b43f5d1bda58dc9387a56be8b2e2b1`.

## Independence gate

The reviewer must be genuinely independent of the authoring context under GOV04 Tier D. Reusing this authoring context, or merely opening a different branch in it, does not satisfy independence.

The current state must therefore remain:

`AWAITING_GENUINELY_INDEPENDENT_TIER_D_REVIEW`

until a different review context performs the review.

## Review question

Determine whether the following bounded composition claim is supported by the pinned implementation and evidence:

`SELECTED_KT05_PACKET_PLUS_EXPLICIT_START_CHEMISTRY_AND_EXACT_SHARED_HETOP_CAN_DRIVE_ONE_BOUNDED_TCD042_INTERVAL_TO_ATOMIC_KT02_COMMIT`.

No broader claim is under review.

## Mandatory checks

The independent review must inspect, not merely trust, the authoring assertions. At minimum it must verify all machine-readable axes in `integration/animo-kt13ar/ANIMO-KT13AR_STATUS.json`.

Particular attention is required for the prior material finding KT13A-F01. The reviewer must verify that the remediated composition enforces exact binary64 identity between HYDROEXEC01 `start_context%he_top` and the `hetop` consumed by KT12, and that mismatches fail before scientific execution without mutating accepted state.

The reviewer must also verify transaction truth: KT02 remains the sole accepted-state publisher and a post-commit diagnostic problem cannot be reported as if the transaction itself had failed.

The manual HYDROQ01 V1 to KT12 V0 projection must be checked field by field for the admitted TCD-042 forcing coordinates. This mapping is not automatically trusted merely because the relevant fields have the same names.

## Required nonclaims

A PASS cannot imply any of the following:

- canonical load-channel to species-owner binding;
- BOUNDARY parser qualification;
- chemistry-provider time provenance;
- a historical first-call `Runinu` value;
- multi-interval continuation;
- canonical `Runinu` checkpoint/state admission;
- B2 historical equivalence;
- TB7, B4 or production authorization.

## Outcome recording

The reviewer may record only `PASS`, `FAIL` or `INCOMPLETE`.

A PASS requires every review axis to be PASS and no unresolved material finding.

FAIL and INCOMPLETE remain valid closed review outcomes and must not be rewritten into PASS by the authoring context.

This review does not itself admit the composition. A separate post-review composition admission/qualification decision remains required.
