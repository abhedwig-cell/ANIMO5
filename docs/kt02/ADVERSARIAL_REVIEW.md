# ANIMO-KT02 Adversarial Review

Review mode: `same-agent / not genuinely independent`.

Assurance label: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Reviewed executable head: `5a6c990f04f44837812ee15e7827688ff495c7ac`.

Exact-head GitHub Actions run: `35278096937`, conclusion `SUCCESS`.

This review is deliberately stricter than the compile/test gate. A green synthetic proof is not sufficient evidence that the proposed authority boundary is safe to reuse.

## Findings

### KT02-R1, HIGH: accepted and trial authority is externally mutable/forgeable

`accepted_store_t`, `trial_state_t` and `trial_result_t` currently expose their components publicly through `mod_transient_contracts`. A caller can therefore directly mutate accepted payload/time/generation or construct candidate provenance without going through `begin_trial` and `commit_trial`.

That contradicts the intended architectural claim that the shared substrate owns authority transitions. The current tests prove cooperative use, not enforcement of the boundary.

Disposition: `MUST_REMEDIATE_BEFORE_QUALIFICATION`.

Required remediation: make accepted/trial/result provenance opaque, add explicit initialization/snapshot/result-construction accessors, and retain only a named trusted reconstruction boundary for persistence restore.

### KT02-R2, MEDIUM: target-bound responsibility is overstated in the candidate contract

The candidate contract says commit checks that an endpoint does not exceed the active requested target. The current `commit_trial` primitive has no active interval target argument. The bound is correctly enforced by `run_interval` before `begin_trial`, but not by standalone commit.

This is not an observed runtime defect in the tested interval path, but it is a theory/code ownership mismatch.

Disposition: `MUST_RECONCILE_BEFORE_QUALIFICATION`.

Required remediation: state explicitly that endpoint-to-target admissibility belongs to interval orchestration, while transaction commit itself requires exact accepted origin and strictly forward endpoint progress.

### KT02-R3, MEDIUM: client object authority is not yet explicitly constrained

The abstract `transient_client_t` is `intent(inout)` and may retain internal data between attempts. That is necessary for diagnostics, workspace and test policy state, but the contract does not yet explicitly forbid a client object from retaining authoritative physical continuation state outside `accepted_store_t`.

If a future adapter did so, rollback could appear correct while hidden model state leaked across rejected attempts.

Disposition: `MUST_RECONCILE_BEFORE_QUALIFICATION`.

Required remediation: define the client object as non-authoritative execution context. Persistent physical continuation must be represented only by the accepted payload. Any warm-start or cache retained in the client must be disposable or proven not to affect scientific identity across reject/retry.

### KT02-R4, LOW: ANIMO-like proof client uses unchecked total addition

The ANIMO-like synthetic conservation check computes `store_a + store_b` in `int64` without an overflow guard. Current test values are small and the issue is in proof-client code, not the shared core, but the client advertises nonnegative `int64` stores generally.

Disposition: `REMEDIATE_OR_BOUND_EXPLICITLY_BEFORE_QUALIFICATION`.

### KT02-R5, BOUNDARY: exact shared time is not SWAP5 production authority

The prototype uses the bounded exact TIME02-style representation proven in KT01. Current SWAP5 production runtime still has REAL-valued time contracts in the frozen reusable source. Therefore KT02 can qualify a shared prototype time contract only. It cannot claim that current SWAP5 production has adopted that representation.

Disposition: `ACCEPTED_EXPLICIT_BOUNDARY`.

### KT02-R6, BOUNDARY: generic atomic sidecar/event publication is not yet proven

KT01 demonstrated atomic physical-state plus ANIMO-like committed event-ledger publication. The current KT02 core intentionally narrows the shared surface and does not yet include a generic sidecar/event ledger. This avoids forcing ANIMO transfer semantics into every model, but means KT02 must not claim generic multi-product atomic publication beyond the accepted physical payload.

Disposition: `ACCEPTED_EXPLICIT_BOUNDARY`; future optional sidecar hook requires a separate proof if needed.

## Review verdict before remediation

`NOT_YET_QUALIFIABLE`.

The dual-client concept is supported, and the exact-head tests are useful evidence, but R1 is material to the claimed authority boundary. R2 through R4 must also be reconciled. No production or admission action is permitted from this review state.