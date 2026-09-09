# ANIMO5 final temporal revalidation of the consolidated candidate architecture

Work unit: `ANIMO-ARCHG02`

Status: `CANDIDATE_ARCHITECTURE_TEMPORAL_REVALIDATION_NOT_CANONICAL_ADMISSION`.

## 1. Purpose and evidence pins

ARCHG01 consolidated ARCH01 through ARCH07 into a coherent candidate architecture but deliberately deferred process ordering, accepted-versus-mutated reads, retry/reject policy, coupled temporal acceptance and calendar/time representation.

Those deferrals can now be re-evaluated against completed evidence:

- ARCHG01 base: `work/animo-archg01-candidate-architecture-consolidation@5cef7969ee921acd2044521cc7636d388aa02efe`;
- TS01: `work/animo-ts01-temporal-semantics@ed12a678cfba19ce851eb2f380e6da3f49203fe4`;
- TIME01: `work/animo-time01-generic-time-transaction-contract@246128dd14732173a6f27c15c923970d50c14e2a`;
- RG02 G5 governance context: `work/animo-rg02-g5-independent-stream-attachment@b289174f4378dcbfcfea9c0d77d0665b3b6c2603`.

The result is an overlay on ARCHG01. The historical ARCHG01 documents are not silently rewritten.

## 2. Revalidation verdict

The consolidated candidate architecture remains internally coherent after final TS01/TIME01 evidence, **provided that its lifecycle objects are understood as a modern abstraction rather than a literal description of revision-53 storage mechanics**.

Two ARCHG01 ideas are explicitly contradicted as literal legacy mechanisms:

1. revision 53 does not keep its current/start arrays immutable for the whole interval, because `Addit` mutates them before downstream processes read them;
2. revision 53 does not execute one literal atomic end-of-step commit, because ordinary result-to-current staging occurs in the next `Init`, while the final interval serializes result state directly.

Neither observation invalidates the candidate `AcceptedState -> TrialState -> accept/reject` architecture. It changes the compatibility requirement: a modern immutable accepted snapshot must expose trial generations that reproduce the legacy visibility and generation dependencies exactly where source equivalence is required.

The candidate architecture therefore survives revalidation with temporal refinement, not by claiming that legacy already implemented transactions.

## 3. Canonical state-generation views required by the candidate scheduler

ARCHG02 adopts the TIME01 candidate generation vocabulary as an architecture-facing requirement:

- accepted/start snapshot at `t0`;
- same-interval event-mutated trial state;
- provisional potential-pass state/rates;
- actual end/result state;
- explicitly previous-step neighbour view where the legacy algorithm requires it;
- same-trial upstream derived view for ordered transport;
- reporting/diagnostic continuation as nonphysical observer state.

A process API that exposes only `accepted` and `latest` is insufficient. It would permit two known source-equivalence errors:

- replacing `Resp_miner` previous-step neighbour reads with newly computed same-step neighbour values;
- hiding same-step management additions from processes that revision 53 runs after `Addit`.

This refinement is architecture-significant because generation identity becomes part of process seam contracts, even though the underlying legacy arrays are not copied literally.

## 4. Process scheduling is now constrained, not globally free

ARCHG01 previously deferred process ordering. TS01 now supplies a source-bound partial order and TIME01 converts it into a candidate scheduler contract.

At minimum, compatibility scheduling must preserve these dependency classes:

`management/residue mutation -> demand/selectivity -> potential pass -> aeration -> actual pass -> actual NH4 transport -> denitrification/NO3 source -> NO3 transport -> P solve -> crop result integration -> balance observation -> reporting`.

Additional noncommutative constraints include:

- same-row material addition before ploughing;
- management event classification with `t0 < E <= t1`;
- annual harvest/root-residue classification with `t0 <= H < t1`;
- provisional potential results cannot emit committed physical transfer events;
- generic solute transport follows `Sqnu` and propagates same-trial upstream averages;
- P transport and phase processes remain coupled per layer;
- crop soil-side removal and later crop-state gain are one physical transfer identity;
- report rollover/reset is not a physical commit.

A future scheduler may use a different internal organization only if it proves that these dependencies remain equivalent or obtains a separately admitted difference. ARCHG02 does not declare any reorder scientifically irrelevant.

## 5. Accept, reject and retry are now candidate policy, not legacy reconstruction

TIME01 fills an architecture hole that ARCHG01 intentionally left open.

The candidate policy now separates:

- `interval_id` for a fixed proposed `[t0,t1]` interval and its semantic bindings;
- `trial_id` for one execution attempt;
- accepted generation identity for the immutable starting snapshot;
- immutable external frame identity.

A retry receives a fresh `trial_id`. A changed `t1` is a new interval and requires new interval/frame binding. Rejection discards trial state, scratch and uncommitted physical events without changing accepted owner generations. Coupled acceptance requires a logical barrier so ANIMO and participating external owners advance corresponding accepted generations together.

These rules are **candidate architecture policy**. They are not claimed to be present in revision 53 and are not canonical TIME admission. No runtime scheduler/reject/retry implementation has yet qualified them.

## 6. External exchange after temporal revalidation

ARCH05/ARCH07 remain compatible with TS01/TIME01 if every external frame is bound before process execution to:

- `t0` and `t1`;
- interval identity;
- producer accepted generation;
- ANIMO accepted generation/trial binding;
- geometry and layout identity;
- configuration/exchange/schema identity;
- immutable frame identity.

This is particularly important for hydrology because TS01 found that legacy `Input_hydro` relies on sequential record consumption rather than an explicit timestamp equality assertion at each read. The modern adapter must therefore make synchronization stronger and explicit rather than reproducing implicit record-order coupling.

Stronger identity validation is an architecture safety property. It does not authorize changed hydrological physics or a production adapter.

## 7. Restart and checkpoint revalidation

ARCH02's accepted-boundary checkpoint model remains coherent, with three refinements from TS01/TIME01:

1. final legacy restart material is drawn from final result generation because no following `Init` occurs;
2. management/event cursor and reporting continuation cannot be assumed irrelevant merely because `INITIAL.OUT` omits them;
3. a future checkpoint writer must be side-effect free even though legacy `Output_Init` contains at least one clamp side effect.

The candidate rule remains: a portable physical checkpoint is created only from accepted state, while diagnostic continuation is a separate optional payload and external owners restore their own state.

What remains unqualified is strong continuous-versus-split behavioural equivalence. That requires independent B2/reference evidence and cannot be replaced by structural checkpoint sufficiency.

## 8. ARCHG01 conflict dispositions after TS01/TIME01

The main ARCHG01 conflicts change as follows.

- `ARCHG-C04` topology change inside a trial: no longer wholly unspecified. TIME01 candidate policy fails closed on mid-trial topology changes unless a separate transition contract exists. This is candidate policy, not canonical admission.
- `ARCHG-C05` accepted versus already-mutated trial reads: source constraint now resolved by TS01 and represented through explicit TIME01 generation views.
- `ARCHG-C09` numerical closure tolerance: unchanged. NQ01/NQ02 remain independent owners and no architecture tolerance is introduced.
- `ARCHG-C11` restart qualification: unchanged as a reference blocker. Candidate structure is not B2 split-run evidence.
- `ARCHG-C06` GHG and `ARCHG-C07` macropores: temporal framework can be represented, but feature-scientific admission remains blocked by GHG01/MP01 and B3 governance.

The full machine-readable dispositions are in `integration/animo-architecture/ARCHG02_TEMPORAL_REVALIDATION_MATRIX.csv`.

## 9. Migration seam readiness after revalidation

Temporal uncertainty is reduced for several seams, but production readiness does not cross a gate.

### Hydrology exchange

The interval/frame identity and coupled accept/reject contract are now candidate-specified. Remaining blockers include canonical TIME, concrete adapter runtime qualification, coordinated restart and macropore extension when active.

### Mineral N

Management visibility, potential/actual separation, NH4-to-NO3 ordering, mixed-generation reads and `Sqnu` dependencies are now source-bound constraints. TCD-015, TCD-016, runtime event production, canonical STATE/TIME and applicable NQ/B3 gates remain.

### Phosphorus

TS01 fixes the source-equivalence schedule around `Sqnu` and per-layer transport/phase coupling. Architecture still cannot choose TCD-014, TCD-019, TCD-024 or TCD-029 dispositions.

### Crop and management

Event endpoints, add-before-plough ordering, one-transfer uptake identity and candidate coupled transaction semantics are explicit. Concrete adapters, B2 continuation and discrepancy-specific B3 remain open.

### GHG and macropores

The temporal transaction shell is representable, but this does not qualify feature science. GHG01/MP01 restrictions remain unchanged.

The full seam matrix is `integration/animo-architecture/ARCHG02_MIGRATION_SEAM_READINESS.csv`.

## 10. What is resolved and what is not

### Resolved as source-bound compatibility constraints

- process partial order relevant to revision-53 equivalence;
- same-step management visibility;
- management versus harvest endpoint rules;
- previous-step versus same-step neighbour generation distinctions;
- `Sqnu` traversal dependencies;
- per-layer P coupling;
- provisional versus actual state/event distinction;
- reporting boundary versus physical acceptance distinction;
- final result-generation serialization requirement.

### Specified as candidate policy but still noncanonical

- immutable accepted snapshot with explicit trial generations;
- interval/trial identity separation;
- reject atomicity;
- retry identity;
- coupled logical commit barrier;
- explicit external-frame binding;
- accepted-boundary portable checkpoint;
- prohibition of uncontracted topology change inside a trial.

### Still open

- independently trusted B2 reference and split-run equivalence;
- runtime scheduler/reject/retry/coupled evidence;
- concrete canonical time coordinate/calendar encoding and representable range;
- canonical STATE and TIME gate admission;
- numerical tolerance and nonlinear policy admission;
- discrepancy-specific B3 scientific decisions;
- GHG and macropore feature admission;
- MASS, EX, B4 and production gates.

## 11. Revalidation decision

No final TS01/TIME01 result requires abandoning the ARCHG01 object graph. The object graph is retained with a stricter interpretation:

`AcceptedState` is a modern immutable owner snapshot, while source-equivalent process execution occurs through explicit trial-generation views and a constrained scheduler. Atomic accept/reject is a future transaction policy, not a claim about legacy implementation.

The appropriate ARCHG02 candidate decision is:

`QUALIFIED_CANDIDATE_ARCHITECTURE_REVALIDATED_AGAINST_FINAL_TS01_TIME01_PRODUCTION_NOT_ADMITTED`.

This decision does not admit canonical TIME, B3, B4 or production migration.
