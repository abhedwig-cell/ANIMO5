# ANIMO-ARCH02 — Restart & Checkpoint Sufficiency Architecture

Status: `CANDIDATE_ARCHITECTURE_DESIGN_ONLY`.

## Purpose

Derive a restart/checkpoint sufficiency contract from the qualified candidate ownership model in ANIMO-ARCH01 and the source-bound conserved-state evidence in ANIMO-PREP06.

This workunit does not admit canonical STATE or TIME semantics and does not implement production code.

## Exact parent

ARCH01 closeout:

`24f57d8daab828f88446a79bd6a276f2925c828b`

ARCH01 decision:

`QUALIFIED_CANDIDATE_STATE_OWNERSHIP_AND_TYPED_TRANSFER_ARCHITECTURE_DESIGN`

Frozen evidence identities remain unchanged:

- source ZIP SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- ANIMO 4.0 User's Guide SHA-256 `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`.

## Questions

ARCH02 must determine, for every ARCH01 candidate field family:

1. whether it is required in a physical restart payload;
2. whether it must instead be supplied by an external owner at restart;
3. whether it is derived and must be recomputed;
4. whether it is step-local and must never be checkpointed;
5. whether it is diagnostic continuation state rather than physical model state;
6. whether its inclusion is conditional on a feature or ownership mode;
7. whether checkpointing is legal only at an accepted transaction boundary.

## Hard rules

- No frozen legacy source change.
- No testcase change.
- No physics change.
- No numerical-policy change.
- No corrected-legacy admission.
- No production implementation.
- No canonical STATE or TIME gate admission.
- Checkpoints are defined at accepted transaction boundaries only. Trial state and uncommitted transfer journals are not portable continuation state in this candidate design.
- Diagnostic continuation state must not be confused with physical model state.

## Required outputs

- `docs/arch02/RESTART_CHECKPOINT_MODEL.md`
- `docs/arch02/DIAGNOSTIC_CONTINUATION_MODEL.md`
- `integration/animo-architecture/ARCH02_RESTART_POLICY.csv`
- `integration/animo-architecture/ARCH02_CONSISTENCY_TEST.json`
- `tools/audit_arch02_restart_policy.py`
- `integration/animo-architecture/ANIMO-ARCH02_STATUS.json`

## Qualification ceiling

At most:

`QUALIFIED_CANDIDATE_RESTART_AND_CHECKPOINT_SUFFICIENCY_ARCHITECTURE`

with:

- `canonical_state_gate_admitted=false`
- `canonical_time_gate_admitted=false`
- `reference_qualified=false`
- `production_migration_admitted=false`

`persist early, test second` applies.
