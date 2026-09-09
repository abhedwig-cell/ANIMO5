# ANIMO-ARCH01 — Conserved State Ownership & Typed Transfer Architecture

Status: `CANDIDATE_ARCHITECTURE_DESIGN_ONLY_NOT_CANONICAL_ADMISSION`.

## Purpose

Translate the qualified ANIMO-PREP06 conserved-state and transfer-ledger evidence into an explicit candidate ANIMO5 ownership architecture. This workunit designs contracts and machine-readable architecture artefacts only. It does not implement production state, process physics, numerical policy, corrected legacy behaviour, or migration admission.

## Evidence parent

Exact starting commit:

`9b1f1ea51c24fb82823290193651830dc61ea3c8`

from `work/animo-prep06-conserved-state-ledger`.

PREP06 qualification at that parent remains:

`QUALIFIED_CONSERVED_STATE_AND_TRANSFER_LEDGER_PREPARATORY_EVIDENCE`.

Frozen evidence identities remain:

- ANIMO 4.1.5 revision-53 source SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- ANIMO 4.0 User's Guide SHA-256 `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`.

## Dependency boundary

The programme migration DAG places canonical state ownership after a qualified migration baseline. That gate is not yet satisfied because PREP02 historical or independently trusted reference qualification remains blocked.

ARCH01 therefore produces a **candidate architecture**, not the canonical admitted STATE gate. Nothing in this workunit may be used to claim that `QM -> STATE` has been passed.

## Design goals

1. Give every continuation-critical physical store one explicit owner.
2. Separate persistent state from derived state, scratch, forcing, parameters, diagnostics and reporting accumulators.
3. Represent accepted and trial/result state explicitly so checkpoint, commit and rollback semantics can be implemented later without hidden mutation.
4. Define typed transfer events with explicit quantity, species, source compartment, sink compartment, control-volume classification and sign convention.
5. Make internal transfer cancellation structural rather than dependent on parallel hand-maintained balance arrays.
6. Generate beginning/end storage views from the same state ownership registry.
7. Keep crop, soil matrix, surface reservoir, macropore and gas compartments explicit where PREP06 evidence requires them.
8. Preserve unresolved scientific boundaries, especially elemental-C/GHG reconciliation, macropore public-ledger coverage and dormant parser-visible state.
9. Permit scalable per-column layouts and optional feature state without prescribing a programming language or concrete memory layout yet.

## Hard exclusions

- no frozen legacy source changes;
- no testcase changes;
- no physics changes;
- no numerical-policy changes;
- no corrected-legacy patch;
- no production implementation;
- no reference qualification;
- no production migration admission;
- no silent conversion of unresolved PREP06 evidence into architecture truth.

## Required outputs

- `docs/arch01/STATE_OWNERSHIP_MODEL.md`;
- `docs/arch01/TYPED_TRANSFER_CONTRACT.md`;
- `docs/arch01/TRANSACTION_STATE_MODEL.md`;
- `integration/animo-architecture/ARCH01_STATE_OWNERSHIP.csv`;
- `integration/animo-architecture/ARCH01_TRANSFER_TYPES.csv`;
- `integration/animo-architecture/ANIMO-ARCH01_STATUS.json`;
- a fail-closed architecture consistency audit and test evidence.

## Qualification ceiling

Maximum decision:

`QUALIFIED_CANDIDATE_STATE_OWNERSHIP_AND_TYPED_TRANSFER_ARCHITECTURE_DESIGN`

with all of the following remaining false:

- `canonical_state_gate_admitted`;
- `reference_qualified`;
- `production_implemented`;
- `production_migration_admitted`.

`persist early, test second` applies.
