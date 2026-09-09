# ANIMO-TS01 feedback to ARCHG01 migration seams

Status: `SOURCE_BOUND_TEMPORAL_FEEDBACK_NOT_ARCHITECTURE_ADMISSION`

This note translates the revision-53 temporal findings from ANIMO-TS01 into constraints that ARCHG01 migration seams must respect. It does not modify ARCHG01 authority, does not admit canonical TIME, and does not prescribe a new production scheduler.

## 1. Accepted/trial architecture is a semantic reconstruction, not a literal source mechanism

ARCH01 and ARCHG01 use immutable `AcceptedState` plus mutable `TrialState`. Revision 53 does not literally do this. The source stages the previous interval result arrays into the current/start arrays in `Init` at the beginning of the next timestep, then mutates those current/start arrays in `Addit` before rates and transport are evaluated.

A future transactional implementation can still use immutable accepted state, but source-equivalent behaviour requires an explicit working generation that sees same-step management and residue mutations before downstream process calculations. Treating every legacy read of `Con*`, `Os`, `Codiorm*`, `Copo`, and related arrays as a read of immutable pre-event accepted state would be wrong.

Required scheduler distinction:

- accepted interval-start snapshot;
- event-mutated working state for the same interval;
- provisional potential-pass result/scratch;
- actual end/result state;
- report observation after physical result completion.

## 2. Management is an ordered state transition, not an unordered event bag

The management seam in `ANIMO5_MIGRATION_SEAMS.md` must preserve two source facts.

First, management packet selection uses `(t0,t1]` through `Juda >= Tinead` and `Juda-St < Tinead`. Second, annual harvest/root-residue logic uses `[t0,t1)` through `Juda > Tiha` and `Juda-St <= Tiha`. These predicates are not interchangeable at exact interval endpoints.

Within one management row, material addition is applied before ploughing/mixing. The ploughing block includes the reservoir, so the newly added material can be redistributed in that same row. A normalized scheduler must therefore retain row order and intra-row action order unless a later behavioural qualification explicitly admits a change.

## 3. Hydrology exchange needs interval-generation identity, not only values

ARCHG01 already requires external hydrology exchange identity. TS01 adds a stricter temporal requirement: revision 53 advances the ANIMO interval clock before `Init`, stages start water coordinates, and then consumes the next hydrology record sequentially. The audited `Input_hydro` route does not provide a strong direct record-time equality assertion against the already advanced ANIMO time.

A future adapter should therefore bind, at minimum:

- accepted/start water coordinates for `t0`;
- proposed/end water coordinates and interval fluxes for `t1`;
- exact interval identity `[t0,t1]`;
- record sequence or synchronization token;
- geometry and owner identity.

Silent reuse of a stale or next-next hydrology frame must fail closed.

## 4. Potential pass is provisional and must not emit committed physical transfers

The revision-53 sequence contains a potential pass:

`Rates1 -> Transca(ANIMO-pot) -> Resp_miner(Itask=0) -> preliminary NH4 Transport -> aeration -> optional preliminary GHG`

followed by the actual pass:

`Rates2 -> Transca(MAIN-ANIMO) -> Resp_miner(Itask=1) -> actual NH4 Transport -> Denitr -> NO3 chain -> optional final GHG -> P`.

Potential result arrays and averages are overwritten or recomputed. A future typed-event journal must therefore distinguish provisional computational observations from accepted physical transfer events. Emitting physical ledger events during both passes would double count.

## 5. Some reads deliberately use older generation data

`Resp_miner` explicitly uses neighbouring `Conh` and `Copo` concentrations from the previous timestep when estimating immobilization availability. This is not a generic license to use stale data; it is a source-specific generation dependency.

A modern process interface therefore needs generation-aware inputs. Replacing these reads automatically with the latest same-step neighbour result would change the algorithm, even if that appears numerically cleaner.

This requirement should be visible in any future process-scheduler qualification fixture.

## 6. Generic transport and phosphorus are sequential in `Sqnu` order

Generic solute transport traverses `Sqnu` and propagates same-step average concentration from one solved layer to the next. Phosphorus does the same while coupling transport, sorption/desorption, precipitation/dissolution and uptake inside `Transgen/Transorp` per layer.

Consequences for migration seams:

- layer solves are not independently reorderable by assumption;
- naive whole-profile parallelization is not source-equivalent;
- phosphorus cannot be split into globally independent `transport`, `sorption`, and `precipitation` phases without qualification;
- any optimized scheduler must prove that it preserves the observed dependency graph or must enter an expected-difference qualification path.

## 7. Crop uptake is one physical transfer with split timing

Crop demand/selectivity is computed after management and before transformations/transport. Soil-side nutrient removal is applied in transport. Plant-side state gain is integrated later by `Upintg_*` using interval-average concentrations and realized uptake.

A future crop seam should represent this as one soil-to-crop physical transfer whose two legacy bookkeeping moments are reconciled, not as two independent transfers. Otherwise the migration can remove nutrient from soil and then record a second physical transfer when plant state is updated.

For external crop ownership, the same rule applies across the owner boundary: one realized uptake event, with explicit accepted interval identity.

## 8. Balance and report reset are observers, not transaction commits

`Outbal_calc` runs after physical result state and crop integration. `Outbal_write` can then write and reset report-period accumulators and roll ending storage into the next report-period beginning-storage fields.

This boundary must not be reused as a physical state commit boundary. ARCH03 observer semantics are source-supported here. Diagnostic continuation may still be needed for mid-report-period restart equivalence, but it remains separate from physical continuation state.

## 9. Legacy restart output does not define canonical restart sufficiency

The final interval has no following ordinary `Init`. `Output_Init` serializes selected final `Rs*` result fields directly. It also has source-observed limitations: several temporal/reporting/external-owner continuation quantities are omitted, the macropore serialization block is commented, and `Rsamplpo_act` is clamped before writing.

Therefore:

- `INITIAL.OUT` is evidence for selected end/result state families;
- it is not proof of serializer purity;
- it is not proof of split-run behavioural equivalence;
- it is not a sufficient basis for canonical `RestartSnapshot` admission.

ARCH02's accepted-boundary checkpoint concept remains a candidate design until behavioural split-run evidence exists.

## 10. Minimum scheduler qualification sentinels

Before a production process scheduler can claim revision-53 temporal equivalence, it should demonstrate at least:

1. exact endpoint management sentinel for `t0`, interior, and `t1` under `(t0,t1]`;
2. exact endpoint harvest sentinel under `[t0,t1)`;
3. same-row fertilizer plus ploughing add-then-mix sentinel;
4. same-step reservoir addition visible to `UBoundconc` and later processing;
5. potential-pass events excluded from committed physical transfer totals;
6. `Resp_miner` previous-step neighbour-generation sentinel;
7. `Sqnu` direction/order sentinel for generic solute transport;
8. `Sqnu` coupled phosphorus transport/phase sentinel;
9. single physical crop-uptake transfer across soil removal and plant integration;
10. balance/report reset shown not to alter physical continuation state;
11. continuous versus split-run test at a clean accepted boundary once independent reference evidence exists;
12. split-run tests immediately before and after management, crop and year boundaries.

Synthetic sentinels can qualify causal implementation behaviour but remain non-B2 evidence.

## 11. Disposition for ARCHG01 seams

| ARCHG01 seam | TS01 disposition |
|---|---|
| Hydrology exchange | `PARTIALLY_SUPPORTED`: value ownership is coherent; exact interval synchronization remains a TIME/adaptor requirement |
| Mineral nitrogen | `SOURCE_ORDER_CONSTRAINED`: potential/actual pass, NH4-before-NO3 chain, previous-step neighbour reads and Sqnu traversal must be represented |
| Phosphorus | `SOURCE_ORDER_CONSTRAINED`: per-layer transport/phase coupling and site-resolved state identity must be preserved |
| Organic matter | `SOURCE_ORDER_CONSTRAINED`: potential versus actual transformation and immobilization recalculation semantics matter |
| Crop | `PARTIALLY_SUPPORTED`: owner model is coherent; realized uptake must remain one transfer despite split legacy timing |
| Management | `SOURCE_ORDER_CONSTRAINED`: endpoint predicates, row order and add-before-plough are observable semantics |
| Dissolved organic matter | `SOURCE_ORDER_CONSTRAINED`: same-step transport propagation and post-management visibility apply |
| GHG | `UNRESOLVED_FEATURE_THEORY_BOUND`: only reachable source placement is mapped; scientific and testcase qualification remain open |
| Macropores | `UNRESOLVED_FEATURE_BOUND`: temporal placement can be source-read but active-path behavioural qualification is absent |

## Qualification boundary

This feedback closes no B3 discrepancy, numerical-policy issue, feature admission, historical reference gap, or canonical TIME gate. It only makes the source-observed temporal constraints explicit at the architecture migration seams so that later implementation cannot silently reinterpret process order as an implementation detail.
