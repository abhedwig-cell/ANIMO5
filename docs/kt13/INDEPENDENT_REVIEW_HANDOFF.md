# ANIMO-KT13 Independent Tier D Review Handoff

## Review target

Review the frozen KT13 composition package only after exact-head CI succeeds.

The candidate claim is:

`SELECTED_KT05_PACKET_PLUS_EXPLICIT_START_AND_CHEMISTRY_CONTEXT_CAN_DRIVE_ONE_BOUNDED_TCD042_INTERVAL_TO_ATOMIC_KT02_COMMIT`

This is not a production or whole-model claim.

## Required review axes

1. Verify KT06 is reused as the selected-packet time/binding authority and its semantics are not duplicated or widened.
2. Verify KT05 projection is byte-identical to the qualified implementation consumed by KT06.
3. Verify HYDROQ01, HYDROQ02 and HYDROEXEC01 implementation blobs match their frozen candidates.
4. Verify the detailed no-ponding hydrology path is the only hydrology science executed.
5. Verify call-entry `Runinu` remains explicit and no first-call or near-zero zeroing rule is invented.
6. Verify UBFORCE02 uses only the pinned wet/advective load formulas and dry deposition remains separate.
7. Verify chemistry remains separately owned from hydrology.
8. Verify KT12 runs only the exact admitted TCD-042 parent scope.
9. Verify KT02 is the sole owner of accepted-state publication.
10. Verify pre-commit failures leave the external accepted TCD-042 store unchanged.
11. Verify the end-to-end test includes a finite-positive E1 commit and a material `Runinu` continuation case.
12. Verify an invalid producer/runtime binding fails before science.
13. Verify an out-of-scope TCD-042 flux fails before external publication.
14. Verify no claim of multi-interval state ownership, provider integration, TB7, B4, Status A/AA or production is implied.

## Independence

Same-agent review is limited to:

`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`

and does not satisfy this Tier D review.

Any independent reviewer finding a material semantic issue must return the package for remediation and refreeze before admission.
