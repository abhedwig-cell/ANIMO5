# ANIMO-KT01 Review 1 Addendum

Reviewed immutable authoring head: `fc4df11c467bcd26951a3e7b168e5bf9c676b94b`

Review mode: `SINGLE_AGENT_ADVERSARIAL_REVIEW`

Assurance: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`

This addendum extends Review 1 after reconstructing the transfer-event boundary and applying GOV05 Tier-C restart/persistence requirements. It does not supersede or weaken `docs/kt01/REVIEW.md`. Review 1 remains a fail-closed review.

## KT01-R1-F02 — material transfer representation defect

`TransferEvent` represents direction through `source_id -> sink_id`. ARCH01 requires the corresponding amount to be non-negative. At the reviewed head, `append_transfer_event` validates identifiers and capacity but accepts negative `amount` values.

A negative amount would therefore encode direction twice, once in the endpoints and once in the sign. That is outside the qualified typed-transfer contract.

Required remediation:

- reject `amount < 0` at the event-construction boundary;
- add an executable negative control proving no journal mutation occurs when a negative event is offered.

## KT01-R1-F03 — Tier-C restart evidence gap

KT01 exercises checkpoint export/restore semantics. Under GOV05 Tier C, a checkpoint round-trip alone is insufficient: split-run/restart evidence is required when restart semantics are in scope.

The reviewed test matrix demonstrates identity-preserving restore, but it does not compare an uninterrupted synthetic continuation against the equivalent continuation split at an accepted checkpoint and restored before the second segment.

Required remediation:

- add a synthetic split-run/restart continuation test;
- compare exact final accepted time, generation and synthetic physical storage;
- compare separately published committed-event history for the complete continuation after the Review-1 event-ledger ownership remediation;
- use exact comparison only; do not introduce a scientific tolerance.

## Interaction with KT01-R1-F01

Review 1 already requires committed event history to be removed from physical `AcceptedState` and `AcceptedCheckpoint`, published as a separate ledger, accumulated across internal accepted substeps, and withheld together with physical state on incomplete/failed outer intervals. That remediation also closes the previously implicit multi-substep event-history-loss path.

## Addendum verdict

`REMEDIATION_REQUIRED_AUTHORING_HEAD_NOT_QUALIFIED`

The bounded remediation set is now:

1. `KT01-R1-F01`: separate event-ledger ownership and atomic outer publication;
2. `KT01-R1-F02`: enforce non-negative directed transfer amounts;
3. `KT01-R1-F03`: add exact split-run/restart continuation evidence.

Any substantive remediation creates a new immutable authoring head and requires exact-head CI plus a restarted full applicable GOV05 adversarial review. No production, B3, B4, canonical-TIME, historical-B2 or shared-library authority is granted.
