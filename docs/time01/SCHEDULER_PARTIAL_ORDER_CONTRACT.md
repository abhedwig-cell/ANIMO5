# ANIMO-TIME01 scheduler partial-order contract

Status: `CANDIDATE_CONTRACT_ONLY`.

## 1. Principle

TIME01 permits a future scheduler to replace the monolithic revision-53 call sequence only if all source-observed temporal/data dependencies are preserved or later deliberately superseded by admitted evidence.

A scheduler implementation MAY execute independent work concurrently. It SHALL NOT infer independence merely because routines write different arrays.

## 2. Boundary model

The candidate scheduler uses named boundaries rather than Fortran routine ownership. The minimum source-equivalence sequence is:

`B00_ACCEPTED_START`

`-> B10_INTERVAL_BOUND`

`-> B20_EXTERNAL_HYDROLOGY_BOUND`

`-> B30_RESIDUE_AND_MANAGEMENT_APPLIED`

`-> B40_BOUNDARY_AND_CROP_DEMAND_READY`

`-> B50_POTENTIAL_PASS_COMPLETE`

`-> B60_AERATION_READY`

`-> B70_ACTUAL_ORGANIC_AND_NH4_COMPLETE`

`-> B80_NO3_COMPLETE`

`-> B90_P_COMPLETE`

`-> B100_CROP_INTEGRATED`

`-> B110_PHYSICAL_TRIAL_COMPLETE`

`-> B120_BALANCE_OBSERVED`

`-> B130_REPORTING_DONE`

`-> B140_TRIAL_READY_FOR_DECISION`

`-> ACCEPT or REJECT`

These are logical boundaries, not a required function decomposition.

## 3. Accepted-start staging

`B00_ACCEPTED_START` binds the immutable accepted generation at `t0`.

Legacy source physically copies prior `Rs*` results into current/start arrays during the next `Init`. A modern scheduler need not make that copy if its state representation is immutable/persistent, but every process that source reads from the ordinary current/start generation must receive the semantically equivalent `G_ACCEPTED_START` view unless same-step mutation has already occurred.

The first simulation interval is an initialization special case and is not an ordinary accepted-start transition.

## 4. Interval and external-frame binding

Before physical process mutation:

1. bind exact `t0`, `t1`, calendar and `interval_id`;
2. create a fresh `trial_id`;
3. bind configuration/layout identities;
4. bind hydrology and external crop frames where active;
5. validate producer accepted generations and geometry;
6. reject before mutation on any mismatch.

The legacy sequential `Input_hydro` read is therefore replaced by an explicit frame boundary, not treated as evidence that record order is sufficient identity.

## 5. Residue and management block

Within the event block the following constraints apply:

- annual harvest/root-residue event membership uses `t0 <= H < t1` in source-equivalence mode;
- management packet event membership uses `t0 < E <= t1`;
- residue/material application mutates trial state before later chemistry reads it;
- within one management row, material addition precedes ploughing/mixing;
- ploughing sees the post-addition surface/reservoir state;
- event selection and event application are trial-local until accept.

After `B30_RESIDUE_AND_MANAGEMENT_APPLIED`, later source-equivalent processes that historically see post-management state read `G_MUTATED_EVENT`, not `G_ACCEPTED_START`.

## 6. Boundary concentration and crop-demand preparation

Upper-boundary chemistry and crop uptake demand/selectivity are prepared after the management/residue block and before potential/actual chemistry.

The scheduler SHALL retain crop start/end identity where both are required by legacy transition logic. A single opaque `crop_at_step` value is insufficient for source-equivalence.

## 7. Potential pass

The potential chain preserves the source dependency:

`potential rates -> potential transformations -> potential Resp_miner -> preliminary NH4 transport -> aeration-related preparation`

Potential results are `G_PROVISIONAL`.

They MAY be traced diagnostically but SHALL NOT emit committed physical transfer events or become accepted state.

## 8. Actual N/organic chain

The minimum actual dependency chain is:

`actual rates`

`-> actual organic transformations`

`-> actual Resp_miner`

`-> actual NH4 transport`

`-> denitrification/NO3 source construction`

`-> first correction/bookkeeping boundary`

`-> actual NO3 transport`

`-> second correction/bookkeeping boundary`

This order is not declared scientifically optimal. It is the source-equivalence baseline.

### Previous-neighbour exception

`Resp_miner` nutrient-availability logic has an explicit `PREVIOUS_ACCEPTED_NEIGHBOR` dependency. Where that path is active, neighbour `Conh/Copo` reads must come from the accepted/start generation required by source, even though other current-layer state is being updated in the trial.

A scheduler that passes same-step neighbour result state everywhere is non-equivalent unless separately qualified.

### Internal recalc

The source permits one recalculation of the immobilization shortage path. This process-local iteration remains inside one trial and does not create an accept/reject boundary.

## 9. Generic solute transport ordering

For legacy-equivalence mode, generic solute transport traverses the hydrological `Sqnu` order. Same-step `Av*` from an upstream processed layer can feed the next layer.

This is `SAME_TRIAL_UPSTREAM` dependency, not a generic previous-state dependency.

A future parallel solver may replace this only after a separate numerical/scientific qualification demonstrates equivalence for the admitted scope.

## 10. Phosphorus ordering

The P path retains two requirements:

- layers are processed in `Sqnu` order where the source does so;
- transport and sorption/desorption/precipitation phase updates are coupled per layer in the source-equivalence path.

A schedule `all P transport for all layers -> all sorption for all layers` is not admitted by TIME01.

## 11. Crop uptake integration

Soil-side nutrient uptake is consumed in the transport/process path. Plant/crop state is integrated later.

TIME01 therefore requires one transfer identity per realized soil-to-crop nutrient movement. The later crop integration is the receiving-state update for that same physical transfer, not a second soil sink.

Where crop is externally owned, the external result/event contract must preserve the same one-transfer rule.

## 12. Optional GHG and macropore nodes

GHG process nodes may only be scheduled when their feature/input/scientific contracts are admitted. TS01 reconstructs only the observed position of reachable preliminary/final GHG calls; TIME01 does not claim complete GHG temporal qualification.

Macropore transport/storage nodes similarly remain gated by the separate macropore qualification and TCD-025 resolution. Their absence from the active partial order must fail closed if the configuration claims an admitted active macropore topology.

## 13. Physical-complete boundary

`B110_PHYSICAL_TRIAL_COMPLETE` is reached only after all active physical result state and trial-local physical transfer events for the interval are complete.

This boundary is the earliest candidate point for conservation/numerical acceptance evaluation. It is not automatically acceptance.

## 14. Balance and reporting observers

`B120_BALANCE_OBSERVED` observes candidate physical state/transfers.

`B130_REPORTING_DONE` may close/reset report accumulators.

Neither boundary mutates accepted physical owner state or commits a trial.

If a trial is ultimately rejected, any diagnostics from that attempt remain explicitly nonphysical and must be distinguishable from accepted-run reporting.

## 15. Trial-ready decision

`B140_TRIAL_READY_FOR_DECISION` means:

- active process schedule completed;
- required structural checks completed;
- required numerical/conservation checks have produced their decision inputs;
- no participant has committed yet.

The coupled orchestration layer may now accept or reject under the transaction policy.

## 16. Required dependency declaration types

Every process/scheduler node must declare zero or more of:

- `ACCEPTED_START_READ`
- `POST_EVENT_TRIAL_READ`
- `PREVIOUS_ACCEPTED_NEIGHBOR`
- `SAME_TRIAL_UPSTREAM`
- `PROVISIONAL_READ`
- `ACTUAL_TRIAL_READ`
- `EXTERNAL_FRAME_READ`
- `REPORT_ONLY_READ`

and one result class:

- `TRIAL_STATE_MUTATION`
- `TRIAL_PHYSICAL_EVENT`
- `PROVISIONAL_SCRATCH`
- `DIAGNOSTIC_OBSERVATION`
- `NO_PHYSICAL_EFFECT`

An undeclared mixed-generation dependency is a qualification failure.

## 17. Fail-closed reorder cases

At minimum the scheduler qualification must detect:

- management after demand/rates;
- plough before same-row addition;
- potential pass physical journal commit;
- actual NO3 path before actual NH4 dependency is available;
- `Resp_miner` previous-neighbour read replaced by latest same-step neighbour state;
- generic transport violating `Sqnu` dependency;
- global P phase split violating per-layer coupling;
- crop receiving integration treated as a second soil removal;
- balance/report boundary used as commit;
- final serialization/accepted checkpoint from stale pre-result generation.

## 18. Relationship to TS01 sentinel matrix

All 26 TS01 scheduler sentinels remain qualification requirements. TIME01 maps them in `TIME01_REQUIREMENT_COVERAGE.csv` and does not downgrade the five B2-dependent restart/reference cases to static evidence.

## 19. Qualification boundary

This partial-order contract says what a candidate scheduler must preserve. It does not provide runtime scheduler evidence, performance claims, parallel-safety qualification or canonical TIME admission.
