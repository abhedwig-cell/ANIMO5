# ANIMO-NQ01 First Reference Comparison Packet Contract

Status: `READY_AWAITING_INDEPENDENT_B2_DATA`.

## Purpose

This contract defines the minimum evidence packet that must exist around the first independent PREP02R B2-versus-B1 comparison.

The packet is deliberately distinct from numerical admission. A packet may be complete while its formatted-tree or structured comparison result is `DIFFERENT_FAIL_CLOSED`. Completeness means the evidence chain is present and traceable. It does not mean the compared implementations are equivalent.

The first packet is currently bound to `RuurloGrass` because PREP02R still identifies that case as the preferred first native reference exercise.

## Machine-readable contract

Schema:

`integration/animo-numerics/FIRST_REFERENCE_PACKET_SCHEMA.json`

Template:

`integration/animo-numerics/FIRST_REFERENCE_PACKET_TEMPLATE.json`

Validator:

`tools/validate_first_reference_packet.py`

Run:

```text
python tools/validate_first_reference_packet.py <packet.json> --json <validation.json>
```

A successful validator result means only:

`PACKET_COMPLETE`

It does not mean:

- B2 provenance is qualified by the validator;
- B1 and B2 are numerically equivalent;
- a non-exact difference is acceptable;
- B3 is established;
- production migration is admitted.

## Required frozen identities

The first packet must retain the frozen testbank identity:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

The corresponding B1 side must use the pinned GNU diagnostic executable identity:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

A different B1 executable creates a different diagnostic comparison and must not be silently substituted into the first packet.

## B2 evidence requirements

The packet records, at minimum:

- B2 evidence role;
- exact artifact SHA-256;
- PREP02R receipt manifest;
- lineage classification;
- explicit PREP02R permission to attempt native execution;
- ordinary native run manifest;
- raw output-tree manifest;
- native repeat-determinism classification or a reason why repeat execution was not possible.

The permitted B2 roles are:

- `B2_HISTORICAL_REFERENCE_CANDIDATE`;
- `B2_HISTORICAL_REFERENCE_QUALIFIED`.

A B1 artifact cannot be relabelled as B2 in the packet.

## Frozen input rule

The preferred first path requires:

`input_content_transformed = false`.

Filesystem staging, historical directory recreation or drive mapping may be recorded separately. Input content edits are not compatibility staging and invalidate the preferred frozen comparison packet until separately qualified.

The packet must identify both the complete staged input tree and the hydrology input identity or manifest.

## Ordinary output comparison

The packet always records the formatted/raw-tree comparison artifact and its decision.

Recognized decisions are:

- `MATCH_EXACT`;
- `MATCH_AFTER_DECLARED_VOLATILE_NORMALIZATION`;
- `DIFFERENT_FAIL_CLOSED`.

A fail-closed tree comparison does not make the packet incomplete. It becomes evidence that must be dispositioned.

## Observer and unrounded capture

Observer capture is optional at packet level because an ordinary B2 run may exist before an observer-capable historical build exists.

When observer capture is used, the packet requires:

- observer patch SHA-256;
- successful ordinary-output non-interference gate;
- B2 structured capture;
- B1 structured capture;
- structured comparison artifact and decision.

An observer packet cannot be complete if ordinary-output non-interference has not passed.

When no unrounded observer capture exists yet, the structured-comparison decision must remain:

`NOT_RUN_NO_UNROUNDED_CAPTURE`.

This records an evidence gap rather than pretending rounded report output is sufficient.

## Structured comparison outcomes

The packet may contain any genuine comparator result, including:

- `MATCH_EXACT_COMPARISON_EVIDENCE`;
- `MATCH_EXACT_B2_CANDIDATE_NOT_QUALIFIED`;
- `MATCH_SCIENTIFIC_RECORDS_REPRESENTATION_DIFFERS`;
- `DIFFERENT_FAIL_CLOSED`;
- `SCHEMA_OR_PROVENANCE_FAILURE`.

The packet validator checks that the result is recorded. It does not reinterpret or weaken it.

## Numerical-policy assertions

Every first-reference packet must explicitly state that:

- no global numerical tolerance was applied;
- no historical residual was used to derive a tolerance;
- rounded report output was not treated as an unrounded oracle;
- B1 was not classified as an independent reference;
- the packet itself did not qualify numerical equivalence;
- production migration was not admitted.

If any of these assertions is false, the NQ01 packet validator fails closed.

## B2 status and next action

The packet separately records whether the B2 artifact is still:

`CANDIDATE_NOT_QUALIFIED`

or has already become:

`PROVENANCE_QUALIFIED_REFERENCE`.

That status comes from PREP02R or its successor governance decision, not from the packet validator.

Every packet must also record a concrete next action, for example:

- classify remaining formatted differences;
- obtain observer-capable source/build lineage;
- investigate first state-trajectory divergence;
- perform numerical-policy qualification for a named discrepancy;
- retain exact-match evidence for later B3 reconciliation.

## Fail-closed distinction

Three statements must remain separate:

1. `PACKET_COMPLETE`: the required evidence chain is present.
2. `COMPARISON_MATCHES` or `DIFFERENT_FAIL_CLOSED`: what the comparator observed.
3. `QUALIFIED_NUMERICAL_EQUIVALENCE`: a later admission conclusion requiring actual B2 evidence and qualified acceptance criteria.

NQ01 currently establishes only the architecture for statements 1 and 2.

## Current boundary

Until PREP02R obtains independent B2 data:

`QUALIFIED_NUMERICAL_QUALIFICATION_ARCHITECTURE_AWAITING_INDEPENDENT_REFERENCE_DATA`

Numerical equivalence remains:

`NOT_QUALIFIED_NO_INDEPENDENT_B2_DATA`

Production migration remains:

`NOT_ADMITTED`.
