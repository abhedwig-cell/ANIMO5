# ANIMO-TS01 restart and acceptance semantics

Status: `SOURCE_BOUND_TEMPORAL_AUDIT`

This document distinguishes three things that must not be conflated:

1. what revision-53 source actually does between timesteps;
2. what its `INITIAL.OUT` restart-style file serializes;
3. what ARCH01/02/03/ARCHG01 propose for a future transaction/checkpoint architecture.

## 1. Revision-53 acceptance is implicit and delayed

Revision 53 has paired current/start and result/end representations for many physical states. Examples are `Conh/Rsconh`, `Coni/Rsconi`, `Copo/Rscopo`, `Os/Rsos`, `Amcxfa/Rsamcxfa` and crop `Ampl*/Rsampl*` fields.

On ordinary timesteps, `Init` copies prior `Rs*` values into current/start arrays (`Init.for:322-400,487-571`). This copy occurs after the main clock has already been advanced to the new interval end (`Animo.for:232-264`).

The source therefore has a recognizable generation transition:

`previous end result -> current start representation`

but no explicit `accept()` call at the end of the producing interval. The equivalent staging occurs at the beginning of the next interval.

## 2. Current/start state is not immutable during a legacy step

After `Init`, `Addit` directly mutates current/start arrays before rate calculations and transport. Fertilizer/manure, residues and ploughing can update `Conh`, `Coni`, `Copo`, organic pools and dissolved-organic concentrations (`Addit.for:313-445,448+`).

Consequently, the revision-53 current/start representation has two temporal meanings inside one interval:

- immediately after `Init`: beginning state carried from the previous result;
- after `Addit`: beginning state plus current-interval event/residue mutations.

Later routines such as `Uptpar_*`, `Rates*`, `Resp_miner` and transport read the post-event form.

This directly contradicts a literal reading that legacy has an immutable accepted state throughout one trial. A modern immutable `AcceptedState` can still be a better design, but emulation must reproduce which processes see same-step management mutations.

## 3. Result arrays have provisional and final meanings

`Rs*` does not always mean a committed final state.

During the potential pass, `Transca('ANIMO-pot')` and preliminary NH4 `Transport` write provisional result/average fields. The actual pass later overwrites/recomputes the corresponding results. Only after `Rates2`, actual transformation/transport, the N chain, P chain and crop integration are complete do the `Rs*` fields represent the interval's end result.

Therefore a future implementation must distinguish:

- provisional solver/process results;
- final trial result;
- accepted continuation state.

Using only the `Rs` naming convention is insufficient.

## 4. Mixed-generation reads exist by source design

The most explicit example is `Resp_miner`. During N or P immobilization shortage estimation it uses neighbouring `Conh` and `Copo` values. Source comments state that the incoming neighbour concentration is from the previous timestep (`resp_miner.for:1076-1087,1141-1153`).

In contrast, generic transport propagates same-step `Avco` values from one layer to the next in `Sqnu` order (`TRANSPORT.FOR:183-187`).

Revision 53 therefore deliberately combines:

- previous/start neighbour values in one subcalculation;
- same-step sequential neighbour values in another.

A modern state API must make these generations explicit. Replacing every read with `latest trial state` would not be source-equivalent.

## 5. Final interval acceptance differs from middle intervals

For a middle interval, the just-produced result is staged into current/start state by the next call to `Init`.

For the final interval, the loop exits and there is no next `Init`. Instead, after final balance closeout, `Output_Init` writes the final result fields directly (`Animo.for:1081-1109`).

Thus the source has no single physical instruction that can be called `commit` for all steps. Continuation semantics must be inferred from dataflow:

- middle interval: final `Rs*` becomes continuation state through next `Init`;
- final interval: final `Rs*` is treated as the authoritative end state for restart-style output.

## 6. What `Output_Init` serializes

`Output_Init` writes a subset of final end/result state:

- `Mofrt` moisture (`Output_Init.for:81`);
- top and profile NH4/NO3 result concentrations (`84-87`);
- exudate, humus and fresh-organic result pools (`90-101`);
- labile DOM/DON and stable DOM/DON/DOP result fields (`104-110`);
- crop root/shoot/N result state and P when active (`113-120`);
- PO4, fast/slow sorption-site state, precipitated P and DOP when P is active (`126-134`);
- system CH4-C and N2O-N result state when GHG is active (`155-166`).

Macropore restart sections are commented out (`Output_Init.for:137-153`).

`Output_Init` also contains a side effect: if `Rsamplpo_act < 0`, it overwrites that physical result with zero before writing (`Output_Init.for:115-117`). Thus serialization is not strictly read-only in revision 53.

## 7. What `INITIAL.OUT` does not establish

The source and public guide support the historical purpose that `INITIAL.OUT` can be used as initialization input for another simulation. They do not establish strong restart equivalence.

In particular, the file does not serialize all of the following continuation-relevant or potentially continuation-relevant information:

- main step counters and interval cursor such as `Sttot`, `Stnu`, `Juda/Tito` as a transaction identity;
- management-file reader cursor `Adnr` and the already consumed event-record position;
- current `Tinead` as a serialized schedule cursor;
- balance/report accumulators needed for identical mid-period output continuation;
- all detailed hydrology-owner state such as snow, ponding, interception and groundwater coordination state;
- active macropore state;
- all crop demand/deficit/cumulative variables that may influence future demand, depending on crop mode;
- an explicit configuration/schema/geometry identity binding the state to the interpretation used to restore it.

Some of these can potentially be reconstructed from static input and the requested restart date. TS01 does not assume reconstructability is exact until a split-run test proves it.

## 8. Restart acceptance classification

The source-bound classification is:

| Item | Revision-53 classification | Basis |
|---|---|---|
| current arrays immediately after ordinary `Init` | `READ_ACCEPTED` analogue | prior `Rs*` has been staged |
| current arrays after `Addit` | `READ_MUTATED_CURRENT_STEP` | same-step events have changed them |
| potential-pass `Rs*/Av*` | provisional/trial scratch | overwritten by main pass |
| actual-pass final `Rs*` | candidate next/end state | next `Init` or final serializer consumes it |
| `Init` result-to-current copy | `COPY_TO_ACCEPTED` analogue | creates next start representation |
| balance arrays | diagnostic/report continuation | do not own physical stores |
| `Output_Init` | `RESTART_SERIALIZE`, with one state-changing guard | writes selected final result state |

## 9. ARCH01 reconciliation

Authoritative live ARCH01 head audited: `24f57d8daab828f88446a79bd6a276f2925c828b`.

| ARCH01 assumption/design statement | TS01 disposition | Source-bound reason |
|---|---|---|
| legacy contains meaningful old/start versus result/end state generations | `CONFIRMED` | widespread `current <- Rs*` staging in `Init` |
| future derived values should declare which snapshot generated them | `CONFIRMED` as a need | source contains both stale previous-step and same-step derived reads |
| accepted state is immutable throughout a trial | `CONTRADICTED` as a description of legacy | `Addit` mutates current/start arrays before later processes read them |
| a process does not independently commit partial state | `CONTRADICTED` as literal legacy mechanism, `SUPPORTED_AS_FUTURE_DESIGN` | legacy routines progressively write result arrays and current arrays; there is no transaction object |
| one atomic end-of-step commit maps TrialState to AcceptedState | `CONTRADICTED` as literal legacy mechanism | ordinary staging happens in the next `Init`; final step serializes `Rs*` directly |
| potential/rate scratch should not be checkpoint state | `PARTIALLY_SUPPORTED` | potential results are overwritten, but behavioural restart sufficiency still needs testing |
| typed transfer journal represents physical transfers once | `UNRESOLVED_BY_LEGACY_SOURCE` | revision 53 uses distributed state mutation and reporting ledgers rather than one journal |

The contradiction labels do not reject ARCH01 as a candidate architecture. They identify where an adapter/process schedule must reproduce legacy visibility/order despite using a cleaner transaction model.

## 10. ARCH02 reconciliation

Authoritative live ARCH02 head audited: `a079d93c965f6073586c55ee4b3544dd8873b723`.

| ARCH02 statement | TS01 disposition | Reason |
|---|---|---|
| portable checkpoint should be made only at an accepted boundary | `PARTIALLY_SUPPORTED` | legacy only emits restart-style state after final interval, but has no explicit acceptance object |
| uncommitted potential/trial scratch should not be serialized | `CONFIRMED` for observed potential fields | `Output_Init` writes final result families, not potential rate scratch |
| reporting accumulators are separate from physical state | `CONFIRMED` | `Outbal_write` resets them without changing chemistry state |
| site-resolved P state belongs in restart state | `CONFIRMED` | `Output_Init` writes `Rsamcxfa/Rsamcxsl` site arrays |
| macropore state cannot be assumed restartable | `CONFIRMED` | corresponding serializer block is commented out |
| existing restart payload is sufficient for exact continuation | `UNRESOLVED`, and not claimed as qualified by ARCH02 | no B2 split-run evidence; temporal/event/diagnostic cursors are incomplete |
| hydrology/crop external owner synchronization must match accepted time | `PARTIALLY_SUPPORTED_AS_REQUIREMENT` | source depends on synchronized hydrology/crop data but does not encode modern owner tokens |

## 11. ARCH03 reconciliation

Authoritative live ARCH03 head audited: `bc27bd7cf0c8148b38768315d2fa54014f5a6cf9`.

| ARCH03 statement | TS01 disposition | Reason |
|---|---|---|
| MassLedger/reporting is observer, not physical-state owner | `CONFIRMED` | `Outbal_calc` runs after physical calculations; `Outbal_write` resets reports independently |
| beginning/end storage and transfers must refer to one explicit interval | `CONFIRMED` as a migration requirement | legacy mixes state generations and delays reporting accumulation until interval end |
| one future typed event journal can replace parallel physical booking | `UNRESOLVED_BY_LEGACY_SOURCE` | source has no such journal; PREP06 establishes conservation identities, not runtime event emission |
| report resets are not physical commits | `CONFIRMED` | reset modifies `B*` arrays only |
| initialization projection needs a separate nonclosure channel | `PARTIALLY_SUPPORTED` | first-step and initial-balance path is distinct; scientific admission of specific projection defects remains B3/TCD work |

## 12. ARCHG01 reconciliation

Live ARCHG01 appeared during TS01 execution and is authoritative at `92812896b6a91b422fcbd9bf5e843da5cfc0f278`. Its own status explicitly defers global accepted time boundary, process ordering, accepted-versus-mutated trial reads, substep/retry policy and calendar/time representation to TS01.

TS01 dispositions for those deferred assumptions are:

| ARCHG01 deferred item | TS01 result |
|---|---|
| global accepted time boundary | `PARTIALLY_SUPPORTED`: source equivalent is staged at next-step `Init`; final step uses result directly |
| process ordering | `CONFIRMED_SOURCE_SEQUENCE`: reconstructed in `PROCESS_ORDER_GRAPH.md`; no reordering admitted |
| accepted-versus-mutated-trial reads per process | `CONFIRMED_MIXED`: `Init` state is then mutated by `Addit`; later reads are post-event; specific `Resp_miner` neighbours remain previous-step |
| substep policy | `PARTIALLY_SUPPORTED`: source has process-internal iterations and layer-order traversal, but no generic retry/rollback transaction |
| retry / accept-reject | `UNRESOLVED`: no general trial rejection/rollback mechanism observed in main legacy route |
| mid-step checkpoint | `UNRESOLVED/NOT_PRESENT`: legacy `Output_Init` is end-of-run only |
| runtime feature/topology transition | `UNRESOLVED`: not qualified by TS01 |
| calendar/time representation | `PARTIALLY_SUPPORTED`: source uses `Juda`, `Juda-St`, `Tiyr`, `Tito` with event-specific endpoint predicates; future canonical representation remains architecture work |

ARCHG01's immutable `AcceptedState` and mutable `TrialState` remain viable candidate types, but TS01 adds a hard compatibility requirement: the trial schedule must preserve the legacy distinction between reads from the initial accepted snapshot, reads after same-step management mutation, same-step sequential neighbour averages, and explicitly previous-step neighbour concentrations.

## 13. Restart test specifications

No synthetic test is B2 historical evidence. The following are qualification specifications for later implementation:

### R1. Continuous versus split run at a clean non-event boundary

Run a multi-step case continuously and split after a timestep with no management/year/report boundary. Restore from a checkpoint candidate and compare continuation-critical state, event sequence and outputs. Exact comparison policy must follow NQ01/B2 evidence when available.

### R2. Split immediately before and after a management event

Verify that the event is neither replayed nor skipped and that `Input_addit` cursor semantics are reconstructed exactly.

### R3. Split around crop transition/harvest

Verify `Kicrold`, `Kicryn`, harvest residue, accumulated crop uptake and crop-state resets.

### R4. Split at year boundary

Verify annual deposition/current-year parameters, `Stnu`, crop annual bookkeeping and annual-output closeout.

### R5. Split inside a balance reporting period

Two separate assertions are required:

- physical continuation equivalence;
- diagnostic/report continuation equivalence.

The second requires either serialized diagnostic continuation state or a deliberate restriction to report boundaries.

### R6. Accepted-state generation sentinel

Instrument a non-production diagnostic build to snapshot:

- immediately after `Init`;
- after `Addit`;
- after potential pass;
- after actual N/P processing;
- after `Upintg_*`;
- after `Outbal_calc`.

The sentinel should prove that only the expected state families change at each boundary. This is source diagnostic evidence, not B2.

### R7. Previous-step neighbour sentinel

Construct a synthetic two/three-layer immobilization case with sharply distinct previous-step neighbour concentrations and verify that `Resp_miner` availability uses `Conh/Copo` previous-step neighbours rather than new `Rs/Av` neighbour values.

### R8. Final serializer purity check

Detect the `Rsamplpo_act < 0` branch and assert that any future checkpoint writer does not silently mutate canonical physical state. If legacy numerical equivalence requires reproducing the clamp in restart material, it must be represented as an explicit compatibility transformation, not a serializer side effect.

## 14. Qualification boundary

TS01 does not qualify exact split-run equivalence because no independent B2 historical executable reference is currently available. It also does not declare `INITIAL.OUT` inadequate for all practical legacy workflows. The narrower source-bound conclusion is that `INITIAL.OUT` is not sufficient evidence for strong transaction/checkpoint equivalence, and several temporal/event/diagnostic continuation quantities lie outside the serialized payload.
