# ANIMO-ARCH07 coupled transaction qualification test specification

Status: `CANDIDATE_TEST_SPECIFICATION_ONLY`.

## Purpose

Adapter field conformance is insufficient if trial/accept/reject semantics can still corrupt coupled state. ARCH07 therefore reserves explicit coupled-runtime cases for the ARCH05 transaction boundary without defining the TIME policy that decides when those operations occur.

## Begin trial

A coupled trial fixture must bind before execution:

- `interval_id` and `trial_id`;
- ARCH06 `configuration_identity`, `physical_layout_id` and `exchange_binding_id`;
- geometry and schema identities;
- ANIMO accepted snapshot identity;
- producer accepted snapshot identities;
- exact immutable hydrology/crop frame IDs.

A stale or generation-mixed frame fails before process execution.

## Reject atomicity

The reject test is a destructive probe of trial-local data, not a no-op test. Before rejection the fixture should have:

- mutated ANIMO `TrialState`;
- trial-local scratch;
- one or more trial transfer events;
- realized crop uptake result where crop coupling is active.

After reject:

- ANIMO accepted state is unchanged;
- external accepted owner generations are unchanged;
- trial results are discarded;
- trial physical journal contributes nothing to committed physical ledgers;
- diagnostics may record that rejection occurred but remain nonphysical.

No numerical comparison tolerance is defined here. Exact rollback requirements for owned state must be established by the later implementation contract.

## Coupled accept barrier

The acceptance fixture must prove that no participant permanently advances before the logical group is admitted. The future TIME/orchestration contract may choose its own protocol, but the observable postcondition is one accepted interval with mutually corresponding owner generations.

ARCH07 therefore tests the atomic **contract boundary**, not a particular two-phase-commit algorithm.

## Retry

A retry creates a new `trial_id`. Producer frame contents are immutable. If frame content changes, its frame ID must also change. Reusing an identical immutable frame may be permitted only as an explicit same-frame binding, not by mutating a prior object.

The choice of revised `t1`, substep sequence or convergence criterion is outside ARCH07.

## Checkpoint owner split

A coupled checkpoint qualification case must prove ownership separation:

- ANIMO serializes only ANIMO-owned accepted persistent state and compatibility identities;
- hydrology owner checkpoints hydrology state;
- external crop owner checkpoints crop state;
- adapter/frame identities needed for compatibility are recorded, not foreign state duplicated into ANIMO.

This is a prerequisite specification for later split-run qualification, not current restart evidence.

## Split-run equivalence

ARCH07 reserves `T008` as a future behavioural comparison:

1. run an admitted coupled case continuously;
2. run the same case to an accepted boundary;
3. checkpoint every owner under its own contract;
4. restore the coupled system;
5. continue with the same admitted interval frames/forcing sequence;
6. compare accepted state, committed event journals and required outputs under the separately qualified numerical/reference comparison policy.

The case cannot pass today because canonical restart/TIME/reference comparison policies are not yet admitted.

## Rollback replay equivalence

`T009` similarly requires one rejected trial followed by replay from the unchanged accepted generation. The replay must be compared with a clean execution of that accepted interval. Rejected journal entries must have no physical contribution.

Again, ARCH07 defines the experiment and traceability requirements, not the numerical tolerance.
