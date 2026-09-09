# ANIMO-STATEQ01 checkpoint projection purity qualification

Status: `QUALIFICATION_HARNESS_PERSISTED_EXECUTION_OPEN`

Canonical STATE admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## Scope

This addendum targets two remaining restricted-core readiness tests:

- `RC-R8`: final-interval checkpoint serializer observational purity;
- `RC-R9`: report-period split physical-only continuation.

It is qualification-only and does not replace `INITIAL.OUT`, `Output_Init` or any production serializer.

## Candidate contract

A checkpoint is projected only from an already accepted boundary. The projection may contain:

- accepted-boundary identity and compatible layout/configuration identity;
- canonical physical owner state;
- admitted continuation state required for future behaviour.

Report-period accumulators are diagnostic continuation. They are not physical state owners and must not change the physical checkpoint payload.

The candidate projection therefore receives report accumulators as context but deliberately excludes them from the physical+continuation checkpoint view.

## TS01 final-step consequence

TS01 distinguishes final result generation from physical interval execution. STATEQ01 therefore requires checkpoint projection to be observational with respect to the already accepted boundary.

The qualification harness accepts a `final_result_generation` context flag but does not allow it to change the projected physical or continuation state. This directly prevents a final-output code path from redefining checkpoint state merely because a run is ending.

This is intentionally different from treating legacy `Output_Init` as a canonical checkpoint writer. STATEQ01 has already rejected that assumption because of known clamp/omission concerns.

## RC-R8 sentinel

The executable sentinel checks:

- no mutation of physical state input;
- no mutation of continuation-state input;
- no mutation of report accumulator input;
- repeated projection is idempotent;
- final-result context does not alter the checkpoint view;
- returned payloads own copies rather than aliases back into accepted state.

## RC-R9 sentinel

The same harness changes report-period values while holding accepted physical and continuation state fixed. The physical checkpoint payload must remain exactly unchanged and contain no report accumulator fields.

A pass is only synthetic observer/projection evidence. It does not yet prove that a full revision-53 split run across a report boundary is behaviourally identical when diagnostic continuation is dropped. That real split test remains open.

## Files

Harness:

`tools/stateq01/checkpoint_projection_purity_harness.py`

Tests:

`tests/stateq01/test_checkpoint_projection_purity_harness.py`
