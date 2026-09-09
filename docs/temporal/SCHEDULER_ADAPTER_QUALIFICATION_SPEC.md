# ANIMO-TS01 scheduler and adapter temporal qualification specification

Status: `POST_CLOSE_SOURCE_BOUND_QUALIFICATION_SPECIFICATION`.

This specification converts the qualified TS01 source reconstruction into testable constraints for a future ANIMO5 process scheduler, hydrology/crop adapter and transaction orchestrator. It does not define a production scheduler, a canonical TIME contract, a retry algorithm or a scientific reordering policy.

The source authority remains the frozen ANIMO 4.1.5 revision-53 archive with SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`. ARCH01/02/03/07 and ARCHG01 are candidate architecture inputs only. Where this document adds future transactional requirements, they are labelled as architecture-contract tests rather than claims about literal legacy mechanics.

## 1. Why a scheduler qualification layer is required

TS01 found that revision 53 cannot be represented faithfully by a generic unordered list of process equations. The legacy route contains observable temporal distinctions between:

- previous interval result state;
- current/start state immediately after `Init`;
- current state after same-step management and residue mutation;
- provisional potential-pass result and averages;
- final actual-pass result;
- same-step upstream average concentrations propagated in `Sqnu` order;
- explicitly previous-timestep neighbour concentrations used by `Resp_miner`;
- reporting accumulators observed only after physical mutation.

A future clean `AcceptedState` / `TrialState` implementation is therefore admissible only if its scheduler reproduces these visibility rules, or if a later scientific/reference qualification explicitly admits a difference.

## 2. Candidate scheduler boundaries

The following names are qualification boundaries, not required production API names.

| Boundary | Source analogue | Required semantic effect |
|---|---|---|
| `B00_INTERVAL_ADVANCE` | main-loop clock update | bind proposed interval end before ordinary state staging |
| `B10_STAGE_START` | `Init` | expose prior final result as new start generation; execute first-step special path when applicable |
| `B20_BIND_HYDROLOGY` | `Input_hydro` + hydrology derivation | bind current interval hydrology and preserve start/end water-coordinate distinction |
| `B30_APPLY_PREPROCESS_EVENTS` | residue preparation + `Input_addit` + `Addit` + `UBoundconc` | make same-step event mutations visible to all later demand/reaction/transport calculations |
| `B40_EXECUTE_PROCESS_CHAIN` | demand, potential pass, aeration, actual N/P chain | preserve source-observed process and layer ordering plus mixed-generation reads |
| `B50_FINALIZE_PHYSICAL_RESULT` | `Upintg_*` after transport/process results | complete soil/crop result generation before physical balance observation |
| `B60_OBSERVE_AND_REPORT` | `Outbal_calc`, `Outbal_write`, `Outsel` | observe completed interval; report reset must not act as physical commit |
| `B70_FINAL_SERIALIZE` | post-loop `Output_Init` | serialize final result generation when the run ends; do not substitute stale start/current generation |

A future implementation may have more internal boundaries. It may not collapse boundaries in a way that changes source-observed visibility without separate qualification.

## 3. Generation labels for qualification traces

Qualification instrumentation should use explicit generation labels even if production types later use different names:

- `G_ACCEPTED_START`: beginning state immediately after ordinary result-to-start staging, or qualified initial state on the first interval;
- `G_MUTATED_EVENT`: start state after residues, management additions and ploughing for the current interval;
- `G_PROVISIONAL`: potential-pass result/rates/averages that may be overwritten;
- `G_ACTUAL_RESULT`: actual current-interval end result;
- `G_SAME_STEP_DERIVED`: same-step derived values such as upstream `Av*` propagated along `Sqnu`;
- `G_PREVIOUS_NEIGHBOR`: explicitly previous-step neighbour concentration used by immobilization availability logic;
- `G_REPORT_ONLY`: observer and report-period continuation state.

The central negative requirement is that there is no universal `latest_state` read rule. A scheduler/state API that silently substitutes the newest available value for all reads is incompatible with the source reconstruction.

## 4. Event scheduling contract

Event type must carry its own boundary rule.

### Management packet

Legacy predicate: `t0 < E <= t1`.

An exact-`t0` management event belongs to the previous interval, while exact-`t1` belongs to the current interval. The management cursor advances when the packet is read. A restart protocol must therefore prove that an event is neither replayed nor skipped.

### Annual harvest/root residue

Legacy predicate: `t0 <= H < t1`.

This is deliberately not normalized to the management convention. TS01 does not infer whether the asymmetry is scientifically intentional, but it is source-observed behaviour.

### Same-row action order

For one management row, material addition precedes ploughing. Ploughing includes the post-addition reservoir. Splitting a row into independent events is admissible only if the scheduler preserves this order and common row identity.

### Crop and year transitions

The scheduler must preserve distinct start and end crop identities where legacy uses both `Kicrold` and `Kicryn`. Year closeout occurs after a step ending on the boundary, while new-year initialization logic executes at the following step start.

## 5. Process-chain contract

The qualification target for the normal active route is the following source-order partial order:

```text
post-event current state
  -> crop demand/selectivity
  -> Rates1
  -> potential Transca
  -> potential Resp_miner
  -> preliminary NH4 Transport
  -> aeration
  -> optional preliminary GHG
  -> Rates2
  -> actual Transca
  -> actual Resp_miner
  -> actual NH4 Transport
  -> Denitr
  -> optional grass adjustment
  -> Correction(1)
  -> actual NO3 Transport
  -> Correction(2)
  -> optional final GHG
  -> phosphorus Transgen/Transorp
  -> crop Upintg
  -> balance observation
```

This is not a claim that every arrow is scientifically necessary in every conceivable reformulation. It is the source-equivalence baseline. Reordering needs evidence.

## 6. Potential versus actual pass

Potential-pass result arrays are provisional. A future transfer journal must not publish potential-pass mass transfers as committed physical events when the actual pass later overwrites/recomputes the result.

Qualification therefore requires two separate checks:

1. potential values are visible where source later routines require them, notably aeration/limitation calculations;
2. only the actual accepted interval contributes physical transfer events and end-state mass accounting.

If a diagnostic trace records potential fluxes, they must be typed as nonphysical/provisional observations.

## 7. Mixed-generation immobilization reads

`Resp_miner` explicitly uses previous-timestep neighbouring `Conh`/`Copo` concentrations for availability estimation and can recalculate once after shortage detection.

A migrated process kernel must be able to request `G_PREVIOUS_NEIGHBOR` independently of mutable trial state. This is a hard source-compatibility requirement. Replacing those reads with same-step neighbour `Rs*` or `Av*` values changes the algorithm even when equations are otherwise unchanged.

## 8. Layer scheduling contract

Generic solute transport and phosphorus processing follow `Sqnu` flow order. Same-step average concentration from one solved layer can feed the next layer.

Therefore:

- layer processing for these routines is direction-dependent;
- unordered parallel layer execution is not source-equivalent by assumption;
- a parallel implementation would require an algorithmic reformulation plus numerical/scientific qualification;
- qualification traces must record the actual `Sqnu` order and the generation of neighbour inputs.

For phosphorus there is an additional constraint: transport, sorption/desorption and precipitation/dissolution are coupled inside the per-layer `Transgen/Transorp` solve. A scheduler must not split them into globally reorderable whole-profile phases merely for architectural cleanliness.

## 9. Uptake transfer contract

Legacy soil-side nutrient uptake is applied inside transport. Plant-side N/P gain is integrated later by `Upintg_*` using the same interval averages and selectivity terms.

A future typed-event design must represent this as one soil-to-crop physical transfer with two state-side effects, not as two independent physical sinks/sources. A qualification harness should reconcile:

`soil nutrient loss == crop nutrient gain`

for the shared realized uptake event, subject to separately admitted numerical/reference comparison policy.

## 10. Balance and report boundary contract

`Outbal_calc` observes the completed physical interval. `Outbal_write` may write and reset report-period accumulators afterward.

Required negative tests:

- report-period reset cannot advance physical generation;
- report beginning-storage rollover cannot overwrite model physical state;
- a physical transaction cannot be considered accepted merely because a report period closed;
- a rejected future trial may create diagnostics, but may not contribute physical amounts to committed ledgers.

The final point is an ARCH01/03/07 transaction requirement, not a literal legacy retry mechanism.

## 11. Hydrology adapter temporal contract

Revision 53 consumes hydrology records sequentially and combines staged start coordinates with new end-of-interval hydrology. TS01 did not find a direct per-record assertion that incoming `Tiwa` equals the already advanced ANIMO interval timestamp.

A future adapter should therefore be stricter than the legacy file seam:

- bind explicit `t0`, `t1`, accepted generation and geometry identity;
- reject stale, skipped, duplicate or generation-mixed frames;
- preserve distinct start and proposed/end storage coordinates;
- normalize producer signs only at the adapter boundary;
- do not infer time alignment merely from record order.

This stricter validation is an architecture safety contract. It is not evidence that revision 53 performed the same checks.

## 12. Crop adapter temporal contract

Where crop state is externally owned, the adapter must bind start/end crop identity, demand and realized uptake to the same interval generation. It must preserve source-observed ordering:

`same-step management -> demand/selectivity -> soil uptake during transport -> plant/crop integration`.

Residue, harvest and grazing events require explicit event identity. They must not be inferred after the fact from crop-state deltas if doing so loses source event ordering or endpoint semantics.

## 13. Restart and split-run qualification

Strong split-run equivalence is not qualified today. The minimum future behavioural suite must include:

- clean non-event split;
- split immediately before and after a management event;
- crop transition/harvest split;
- year-boundary split;
- mid-report-period split with physical and diagnostic continuation checked separately;
- accepted-generation sentinel at `Init`, post-`Addit`, post-potential, post-actual, post-`Upintg` and post-balance boundaries;
- management cursor/event replay check;
- final serializer purity/compatibility transformation check.

These experiments require independently trustworthy B2/reference evidence before they can establish historical behavioural equivalence.

## 14. Evidence tiers

Every scheduler/adaptor test must declare one of these evidence tiers:

- `SOURCE_STATIC`: checks immutable revision-53 source anchors/order only;
- `SYNTHETIC_CAUSAL`: executes a diagnostic or synthetic case to expose causality; never B2 by itself;
- `ARCH_CONTRACT`: checks candidate ANIMO5 transaction/adapter invariants not claimed as legacy behaviour;
- `REFERENCE_BEHAVIOR`: compares with independently trustworthy historical/reference behaviour;
- `SCIENTIFIC_ADMISSION`: establishes that an intentional behavioural difference is scientifically admitted.

A PASS at one tier cannot be silently promoted to another.

## 15. Fail-closed admission rules

A future scheduler/adaptor qualification fails if any of the following is true:

1. event endpoint semantics are not explicit per event class;
2. same-row add-before-plough order is not preserved;
3. same-step management mutation is invisible to downstream demand/reaction/transport;
4. potential-pass physical transfers can reach committed ledgers;
5. `Resp_miner` previous-neighbour reads are replaced by generic latest-state reads without admitted difference;
6. `Sqnu` ordering is absent, unstable or ignored where same-step neighbour propagation occurs;
7. P transport and phase processes are globally reordered without admitted qualification;
8. soil and crop uptake sides can be booked as two independent physical events;
9. report reset can mutate/accept physical state;
10. restart can replay/skip management events or lose required crop/year continuation;
11. final checkpoint state is taken from a stale start generation;
12. hydrology/crop frames can be bound without explicit interval/generation identity;
13. a test marked `SOURCE_STATIC` or `SYNTHETIC_CAUSAL` is presented as B2 historical evidence;
14. a scheduler difference is accepted merely because outputs look close under an unqualified tolerance.

## 16. Relationship to ARCH07

ARCH07 already defines adapter field and coupled transaction test structure, including immutable frame identities, reject atomicity, checkpoint ownership split, split-run reservation and rollback/replay reservation. TS01 adds the missing temporal predicates and process visibility constraints.

ARCH07 tests should eventually import the TS01 sentinel IDs from `integration/animo-temporal/TS01_SCHEDULER_SENTINELS.csv` rather than restating temporal assumptions independently. This prevents the adapter layer from accidentally defining a second time model.

## 17. Qualification boundary

This specification is a post-close consequence of the qualified TS01 source audit. It does not change the TS01 decision, does not admit canonical TIME, does not qualify a production process scheduler, and does not change any revision-53 source or testcase.
