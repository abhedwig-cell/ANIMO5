# ANIMO5 ARCHG01 TS01 closeout revalidation

Work unit: `ANIMO-ARCHG01`

Status: `TS01_CLOSEOUT_REVALIDATED_SOURCE_BOUND_CONSTRAINTS_INTEGRATED_TIME_POLICY_NOT_ADMITTED`

TS01 is now qualified as source-bound preparatory evidence at live head `ed12a678cfba19ce851eb2f380e6da3f49203fe4`, with decision `QUALIFIED_SOURCE_BOUND_TEMPORAL_SEMANTICS_PREPARATORY_EVIDENCE`.

This document supersedes the earlier provisional TS01 handoff written while TS01 was still in progress.

## 1. Revalidation outcome

The consolidated candidate object model remains valid. TS01 does not require a mega-state, a different state owner model, or removal of `AcceptedState`, `TrialState`, `TransferEvent`, `ExternalExchange`, `MassLedger`, `RestartSnapshot`, `DiagnosticsView` or `LegacyInputAdapter`.

It does require stronger temporal contracts around those types.

The revalidation result is:

- no candidate type is invalidated;
- `AcceptedState` remains a valid modern immutable lifecycle role, but it is not a literal legacy mechanism;
- `TrialState` must represent same-step event mutation before later process reads;
- process seams must declare read generation explicitly;
- `StepContext` must bind source-compatible event timing and ordering constraints without pretending that one universal endpoint convention exists;
- potential-pass results remain provisional/scratch semantics;
- restart compatibility remains structurally designed but behaviourally unqualified;
- arbitrary layer reordering or parallelization remains unadmitted;
- no canonical TIME/retry/reject implementation is admitted.

## 2. Legacy acceptance mapping

Revision 53 stages previous end results into current/start arrays at the next step's `Init`. The modern architecture proposes a logical accepted boundary after the completed actual result.

The candidate mapping remains possible:

```text
legacy final actual result R(n,t1)
        -> source-authoritative end generation
modern completed TrialState(n,t1)
        -> logical accept
        -> AcceptedState(n+1,t1)
legacy next Init
        -> stages R(n,t1) into current/start representation
```

This mapping is structurally coherent because TS01 finds a real old/start versus result/end generation split. It is not yet behaviourally qualified because first-step handling, final-step serialization, event cursors, crop/year boundaries, reporting continuation and external-owner synchronization can affect split-run equivalence.

Disposition: architecture survives; reference/TIME qualification remains required.

## 3. Same-step management and read visibility

TS01 confirms that `Addit` mutates current/start chemistry before `UBoundconc`, crop demand, potential processing and actual processing.

The modern seam therefore must execute management/residue application inside the trial before downstream readers that depend on it. The physical transfer must be represented once. A legacy mutation plus a second typed-transfer application would double apply the material.

Disposition: resolved architecturally by mutable `TrialState` plus one physical `TransferEvent`; source order is binding unless separately qualified.

## 4. Event boundaries

TS01 qualifies source-bound differences that cannot be collapsed by architecture:

- management addition/plough packet: `(t0,t1]`;
- annual harvest/root-residue trigger: `[t0,t1)`;
- balance-report dates: half-step crossing logic;
- same management row: addition before ploughing.

`StepContext` may carry an immutable schedule/event view, but event classes must retain their own qualified boundary rule and ordering relation.

Disposition: resolved as a preservation contract. Any normalization change requires expected-difference/reference evidence.

## 5. Process read generations

A future process seam must be able to distinguish at least:

1. beginning accepted state;
2. post-management trial state;
3. provisional potential-pass result;
4. actual same-step result;
5. explicitly previous-step neighbour state;
6. same-step upstream average propagated in `Sqnu` order;
7. immutable external-owner observation.

This is the most important refinement produced by TS01. A generic `latest_state` read contract is not sufficient for source-equivalent migration.

Disposition: resolved at architecture-contract level, still unimplemented.

## 6. Potential and actual passes

Potential `Rates1`, `Transca`, `Resp_miner` and preliminary NH4 results precede aeration and the actual pass. They may be overwritten.

The candidate architecture therefore keeps potential values in trial scratch or explicitly provisional trial fields. They do not emit committed physical transfers by default. Diagnostic observation is allowed but remains nonphysical.

Disposition: resolved architecturally. Any changed numerical formulation is NQ/B3 work.

## 7. Layer traversal and stale/current mixtures

TS01 confirms that generic transport and phosphorus traverse `Sqnu` in source-observable order, while `Resp_miner` contains explicit previous-step neighbour reads for availability calculations.

The architecture does not authorize changing either behaviour. Parallel execution is allowed only if a future implementation proves equivalence under the applicable numerical/scientific/reference policy.

Disposition: source order/read generation now known; production optimization remains unadmitted.

## 8. Crop uptake

The soil-side nutrient sink occurs in transport and plant-side `Upintg_*` later integrates realized uptake into crop state.

The typed-transfer model therefore represents one nutrient transfer from soil to crop. Plant-side integration is the sink's receiving-state effect, not a second soil removal.

Disposition: resolved architecturally.

## 9. Restart and serialization

TS01 confirms that final `Rs*` result fields are the relevant end generation, but `INITIAL.OUT` is not evidence for complete transaction/checkpoint equivalence.

Important gaps include management/event cursor state, reporting continuation, external-owner synchronization, macropore continuation and other mode-dependent continuation variables. `Output_Init` also contains a state-changing phosphorus clamp before serialization.

The canonical `RestartSnapshot` therefore remains read-only over accepted canonical state. A legacy restart adapter may reproduce serializer transformations only as explicit compatibility behaviour and only after qualification.

Disposition: structure resolved, behavioural split-run equivalence requires reference evidence.

## 10. Retry, rejection and topology transitions

TS01 does not find a generic legacy trial rejection/rollback mechanism, a mid-step portable checkpoint, or a qualified runtime feature-topology transition policy.

These are future orchestration capabilities, not source behaviours that architecture may infer.

Disposition: not production-ready. Separate TIME/transition contracts are required.

## 11. Conflict-register closeout mapping

The temporal conflicts are reclassified as follows:

| Conflict | Post-TS01 disposition |
|---|---|
| delayed staging versus atomic commit | `REQUIRES_REFERENCE` |
| same-step management visibility | `RESOLVED_ARCHITECTURAL` |
| heterogeneous event endpoints | `RESOLVED_ARCHITECTURAL` with reference gate for any change |
| potential versus actual pass | `RESOLVED_ARCHITECTURAL` with NQ/B3 gate for reformulation |
| sequential `Sqnu` propagation | `NOT_PRODUCTION_READY` for reordering; source contract known |
| previous-step neighbour reads | `RESOLVED_ARCHITECTURAL` as explicit read-generation requirement |
| first-step asymmetry | `RESOLVED_ARCHITECTURAL` as separate initialization boundary |
| restart cursor/report omissions | `REQUIRES_REFERENCE` |
| runtime feature/topology transition | `NOT_PRODUCTION_READY` |

No temporal finding invalidates the core candidate architecture.

## 12. Final boundary

TS01 is preparatory source-bound qualification, not B2 historical reference, B3 admission, canonical TIME implementation, or production migration authorization.

ARCHG01 therefore remains:

`QUALIFIED_CONSOLIDATED_CANDIDATE_ARCHITECTURE_PRODUCTION_IMPLEMENTATION_NOT_ADMITTED`
