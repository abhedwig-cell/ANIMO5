# ANIMO5 ARCHG01 to TS01 handoff and revalidation contract

Work unit: `ANIMO-ARCHG01`

Status: `CANDIDATE_ARCHITECTURE_TEMPORAL_HANDOFF_TS01_IN_PROGRESS`

This note is a follow-up hardening pass on the consolidated candidate architecture. It reads the live ANIMO-TS01 source-bound audit at head `5bd1bdd3012adec63679e72077a243ae95ccc01f`. TS01 itself still reports `decision = IN_PROGRESS`, so none of its unfinished findings are promoted here to a qualified TIME contract. They are used only to test whether ARCHG01 has made assumptions that the source audit already contradicts.

## 1. Result of the provisional compatibility check

The core ARCH01-ARCH07 object separation survives the source-bound temporal audit, but only under a stricter interpretation than a generic immutable-start-state timestep.

The candidate architecture may keep:

- one immutable `AcceptedState` generation;
- a mutable `TrialState`;
- trial-local scratch and provisional calculations;
- typed physical transfer events;
- one logical accept/reject boundary;
- observer-only ledgers and diagnostics;
- accepted-boundary restart snapshots.

However, it may not infer that every legacy process reads only the immutable beginning-of-step state. TS01 shows that revision 53 deliberately mixes several generations and order-sensitive values inside one interval. The future process contract must state which generation each read comes from.

Therefore ARCHG01 remains a coherent candidate architecture, but production implementation is still blocked by the TIME/TS01 gate.

## 2. Accepted state and delayed legacy staging

Revision 53 does not execute an explicit end-of-step commit. For ordinary timesteps, the previous `Rs*` result arrays become the next current/start arrays only when the following `Init` call executes. The final interval is different because `Output_Init` serializes the final `Rs*` result generation directly.

ARCHG01's atomic commit is therefore an abstraction, not a literal description of the legacy source.

It can be admitted only if a later TIME qualification establishes that the following mapping is behaviourally safe:

```text
legacy completed actual result R(n,t1)
        ~= candidate TrialState result at t1
candidate logical accept at t1
        -> next AcceptedState
legacy next-step Init staging
        ~= candidate begin_trial state construction plus explicitly scheduled boundary actions
```

The equivalence condition is not just equality of chemistry fields. It must preserve:

- final-interval output generation;
- first-step special initialization;
- crop/year boundary actions performed in `Init`;
- management/reporting cursor semantics;
- any process that intentionally reads old versus already-mutated state.

Until TS01 closes and this mapping is reviewed, `AcceptedState` and `TrialState` are qualified architecture roles only, not an admitted source-equivalent TIME implementation.

## 3. Same-step management belongs in TrialState

TS01 shows that `Addit` mutates the current/start arrays before `UBoundconc`, uptake demand, the potential pass and the actual pass. A future architecture must therefore model material application and ploughing as mutations/events inside the current trial, before the later processes that consume their consequences.

The safe candidate mapping is:

1. `AcceptedState` remains immutable;
2. begin the trial by constructing `TrialState` from accepted physical state;
3. apply the scheduled management/residue actions to `TrialState` once;
4. emit the corresponding physical `TransferEvent` legs once;
5. later process kernels read the required post-event trial state where the source does;
6. reject discards both the state mutation and the event journal;
7. accept promotes the completed result generation.

Retaining legacy `Addit` mutation while also adding a typed event producer would double-apply material and is forbidden at a migration seam.

## 4. Event scheduling cannot use one universal endpoint rule

TS01 has already established three distinct source-bound conventions:

- management addition/plough packets: `(t0,t1]`;
- annual harvest/root-residue trigger: `[t0,t1)`;
- selected balance dates: a half-step crossing rule.

ARCHG01 therefore refines `StepContext`: it may bind an immutable event/schedule view, but it must not normalize all event sources to one endpoint convention unless a later behavioural/scientific qualification explicitly admits that change.

The same management row also has a strict internal order: addition before ploughing/mixing. A future generic event collection must preserve an ordering relation or a compound-event identity. Treating both actions as unordered events is not source-equivalent.

## 5. Potential pass is provisional state, not committed physics

Revision 53 performs a potential biochemical pass before aeration and a later actual pass. Potential `Rs*`/average results can be overwritten by the actual calculation.

In the candidate type model:

- potential-pass intermediate results belong to trial scratch or explicitly labeled provisional trial values;
- they cannot become committed `TransferEvent` records merely because a legacy routine writes result-shaped arrays;
- physical event emission belongs to the actual admitted transfer-producing path;
- diagnostic capture of the potential pass is allowed but remains nonphysical.

This is important for MassLedger. If potential and actual passes both entered the physical journal, the ledger would double count transformations that revision 53 treats as provisional then actual.

## 6. Layer order is not a performance-only choice

TS01 shows that generic transport and phosphorus processing traverse the hydrologically determined `Sqnu` order and can pass same-step average concentrations to the next layer. `Resp_miner` additionally uses previous-timestep neighbour concentrations in availability checks.

Consequences for the candidate migration seams:

- a process seam may not promise arbitrary layer parallelism from the architecture alone;
- `AcceptedState` versus `TrialState` read provenance must be expressible per field/process;
- a solver that replaces previous-step neighbour values with same-step neighbour values changes temporal/numerical semantics;
- a reordered or parallel layer algorithm requires NQ/B3 equivalence evidence, not only unit tests and conservation closure.

ARCHG01 therefore treats physical state ownership and execution scheduling as separate concerns. The ownership model is compatible with sequential execution, but it does not authorize reordering.

## 7. Crop uptake must remain one physical transfer

TS01 confirms that soil-side crop uptake is already applied as a sink in transport, while `Upintg_*` later integrates the corresponding realized uptake into crop result state.

The typed-transfer mapping must represent this as one physical nutrient transfer with two state effects inside the same accepted transaction:

```text
soil nutrient store -> crop nutrient store
```

For an external crop owner, the sink is still emitted once by ANIMO's trial and the external owner consumes the accepted result under the coupled commit barrier. `Upintg_*`-like plant-side bookkeeping may not be modeled as a second soil sink.

## 8. Restart has a new explicit architecture hazard

The provisional TS01 audit identifies two facts that strengthen ARCH02/ARCHG01's caution around legacy restart files.

First, `INITIAL.OUT` omits continuation context such as the management-reader cursor, reporting accumulators and complete coordinated external-owner state. Second, `Output_Init` is not fully read-only: it clamps negative `Rsamplpo_act` to zero before writing.

Therefore:

- canonical `RestartSnapshot` creation must remain read-only over accepted physical state;
- `INITIAL.OUT` cannot be treated as the canonical checkpoint schema;
- importing/exporting a legacy restart file needs a separate compatibility adapter/qualification path;
- any clamp or other legacy serializer transformation must be explicit evidence, not a hidden checkpoint side effect;
- split-run equivalence remains a reference/behavioural qualification problem.

ARCHG01 deliberately does not add the legacy serializer side effect to the modern checkpoint contract.

## 9. Required TS01 answers before ARCHG01 can be revalidated

ARCHG01 requests the following outputs from the completed temporal audit:

1. exact interval lifecycle and the semantic point at which a completed result may be considered accepted;
2. per-process read generation: pre-event accepted, post-event current/trial, provisional result, actual result, previous-step neighbour, same-step upstream average;
3. complete event endpoint and ordering rules, including crop/year transitions;
4. whether any physical state mutation occurs after the candidate logical commit point but before the next interval begins;
5. which provisional passes must never enter the committed transfer journal;
6. exact temporal role of `Sqnu` order and any other source-observable iteration sequence;
7. final-state and restart generation semantics, including `Output_Init` transformations;
8. continuation-critical cursors or scheduling metadata not represented by the chemical state arrays;
9. whether rejected/retried trials are a new ANIMO5 orchestration capability rather than a source behaviour to preserve;
10. which source ordering facts are historical implementation details versus scientifically/numerically constrained behaviour requiring B3/NQ evidence to change.

## 10. Revalidation rule

When TS01 closes, ARCHG01 must be rechecked before canonical STATE/TIME admission.

The recheck must classify every temporal dependency in `ARCHG01_CONFLICT_REGISTER.csv` as one of:

- resolved without changing the candidate object model;
- requires refinement of `StepContext` or process seam contracts;
- requires a B3 expected-difference/admission record;
- requires NQ numerical equivalence qualification;
- requires reference/split-run evidence;
- invalidates part of the current candidate architecture.

No TS01 closeout may be treated as an automatic production migration authorization.
