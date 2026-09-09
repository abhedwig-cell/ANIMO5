# ANIMO-MASSQ01 work-unit contract

Status: `QUALIFIED_MASSLEDGER_OBSERVER_PROJECTION_B1_NONREFERENCE_MASS_GATE_NOT_ADMITTED`.

Purpose: build and qualify an observer-only MassLedger projection above the existing B1 diagnostic execution surface. The projection reconstructs conserved storage and boundary/source transfers from source-bound state and transfer identities; legacy balance accumulators are comparison/report evidence only and never authoritative physical storage.

Base authority: `work/animo-rg02-g5-independent-stream-attachment@5c278152eacc33660f1c5870c7d419b8041b20a9`.

Pinned evidence inputs:

- PREP06 `work/animo-prep06-conserved-state-ledger@9b1f1ea51c24fb82823290193651830dc61ea3c8`;
- ARCH03 `work/animo-arch03-mass-ledger-observer@bc27bd7cf0c8148b38768315d2fa54014f5a6cf9`;
- ARCHG01 `work/animo-archg01-candidate-architecture-consolidation@981de99811806da362244440502218a84754157b`;
- ARCHG02 `work/animo-archg02-temporal-revalidation@db8183802631902f41aa5bec518a3c2e63e03ab7`;
- TQ01 `work/animo-tq01-testcase-qualification@5c43ee16df37a0a1357614fdec527f25e5ca8c16`;
- MP02 and GHG01 are read live and pinned before their evidence is used.

Frozen runtime artifacts remain unchanged:

- source archive SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

Hard invariants:

1. observer code may read physical state and process-transfer variables but may not mutate physical state;
2. no legacy balance accumulator is an authoritative storage owner;
3. no known discrepancy is corrected to force closure;
4. raw residuals are preserved without an invented closure tolerance;
5. B1 observer evidence is never promoted to B2 reference evidence;
6. synthetic macropore evidence remains explicitly synthetic B1;
7. GHG coverage may remain incomplete where the source/input/reference contract is unresolved.

Required residual classes:

- `EXPECTED_KNOWN_TCD`;
- `LEGACY_REPORTING_ONLY_DIFFERENCE`;
- `OBSERVER_CLOSURE_PASS`;
- `UNEXPLAINED_RESIDUAL`.

A new unexplained residual is a MASSQ01-local finding only. This workunit has no authority to allocate a canonical TCD identifier.

Target success status: `QUALIFIED_MASSLEDGER_OBSERVER_PROJECTION_B1_NONREFERENCE_MASS_GATE_NOT_ADMITTED`.

Closeout: the target success status was reached for the B1 nonreference observer projection after quantity-specific transaction-boundary qualification, eight-case runtime execution, observer-on/off non-interference comparison, known-TCD visibility checks, synthetic MP02 mapping and explicit GHG coverage limitation. The closeout does not admit a canonical MASS implementation or corrected legacy reference.

Production migration, B3 admission and canonical MASS admission remain outside scope.
