# ANIMO-TS01 legacy timestep lifecycle

Status: `SOURCE_BOUND_TEMPORAL_AUDIT`

Authority for ordering claims in this document is the frozen ANIMO 4.1.5 revision-53 source archive with SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`. The ANIMO 4.0 user guide is supporting historical documentation only and is not revision-53 implementation authority.

## 1. Central finding

Revision 53 does not implement an explicit transaction object, but it does contain a strong implicit distinction between start/current arrays and result/end arrays. The distinction is temporally important and is not equivalent to the candidate ARCH01 transaction model.

The main legacy pattern is:

1. advance the model clock to the end of the interval;
2. at the start of the computation for that interval, copy the previous interval's `Rs*` result arrays into current/start arrays in `Init`;
3. read the new hydrological interval;
4. mutate several current/start arrays in place for crop residues, management additions and ploughing;
5. calculate potential and then actual process rates;
6. solve transport and transformations into new `Rs*` result arrays;
7. integrate crop state, balances and outputs from those results;
8. only at the beginning of the next timestep are those results copied into the current/start arrays.

The final simulated interval is a special boundary: there is no following `Init` call. `Output_Init` serializes the final `Rs*` result arrays directly.

This means that a future accepted/trial design can be cleaner than the source, but it cannot assume that all revision-53 equations read one immutable beginning-of-step snapshot. Some routines intentionally read state already mutated inside the current interval, and some availability calculations explicitly read previous-step neighbour concentrations.

## 2. Pre-loop lifecycle

`Animo.for` performs the following relevant sequence before the timestep loop:

| Order | Call | Temporal role | Source |
|---:|---|---|---|
| 1 | `Input1` | read static configuration, initial state, management metadata and hydrology metadata | `Animo.for:80` |
| 2 | `Input_SoilTemper` when selected | load external soil-temperature data | `Animo.for:129` |
| 3 | `Input_cropext` when external crop is selected | load crop forcing | `Animo.for:134` |
| 4 | `Inicalc` | derive initial quantities and initialize model-side structures | `Animo.for:143` |
| 5 | `Input_Echo` | reporting/diagnostic echo | `Animo.for:174` |
| 6 | `Outbal_write(Itask=1)` | initialize balance output structures/files | `Animo.for:195` |
| 7 | set `Juda=Judami` | establish loop start | `Animo.for:221` |

The timestep loop is `Do While (Juda<Judama)` at `Animo.for:225`.

## 3. The interval clock is advanced before process execution

At the top of every loop iteration, counters are incremented first. For variable hydrology, the next record is peeked to obtain `St`, then backspaced. `Tiyr`, `Tito` and `Juda` are advanced before `Init` is called (`Animo.for:232-246`).

Therefore, within most of the timestep body:

- `Juda` denotes the interval end;
- `Juda-St` denotes the interval start;
- `Tito` has already been advanced by `St`;
- date-dependent logic must be audited for whether it uses `Juda` or `Juda-St`.

This is not merely a naming issue. Event predicates in revision 53 deliberately use different endpoint conventions.

## 4. State staging in `Init`

`Init` is called at `Animo.for:264` under the comment `UPDATE STATE VARIABLES (RESULT FROM PREVIOUS STEP)`.

### 4.1 Non-first timestep

For later timesteps, `Init` copies prior result/end values into current/start values, including:

- surface/top solutes: `Rsconhtop -> Conhtop`, `Rsconitop -> Conitop`, `Rscodiormatop -> Codiormatop`, with corresponding P fields (`Init.for:324-337`);
- hydrological start coordinates: `Mofrt -> Mofro`, `Snt -> Snla`, `Sict -> Sic`, `Pnt -> Pn`, `Walet -> Wale` (`Init.for:339-350`);
- NH4/adsorbed NH4: `Rsconh -> Conh`, `Rscxnh -> Cxnh` (`Init.for:352-355`);
- NO3: `Rsconi -> Coni` (`Init.for:357-359`);
- labile and stable DOM/DON/DOP (`Init.for:361-371`);
- fresh organic matter, humus and exudate pools (`Init.for:373-380`);
- PO4, precipitated P and fast/slow sorption-site state (`Init.for:383-400`);
- GHG dissolved/result concentrations when active (`Init.for:487-495`);
- macropore result concentrations and prior water storage when active (`Init.for:501-532`);
- crop state result fields into current crop fields (`Init.for:555-571`).

This is the closest source equivalent of acceptance. It occurs at the beginning of the next loop iteration, not as an explicit atomic commit at the end of the producing interval.

### 4.2 First timestep

The first timestep follows a different path (`Init.for:185-321`). Input initial-state arrays remain the current/start state, while several result fields are deliberately initialized or zeroed for checking. The first timestep therefore cannot be treated as an ordinary `previous result -> current` transition.

`Outbal_Init` is called only for the first simulated interval at `Animo.for:336`, after `Init` and before hydrology and management for that interval. Beginning-storage semantics are therefore tied to the initial/current state before same-step additions.

### 4.3 Management reporting reset

At the end of `Init`, `Nuad` and the per-step `Ad*` management/redistribution reporting arrays are reset. The source comment states that these are initial values used by `OUTBAL` at the start of the timestep before additions are executed in `ADDIT` (`Init.for:574-590`). These are reporting accumulators, not accepted physical stores.

## 5. Hydrology frame

After state staging, the dynamic hydrology record is read in `Input_hydro` (`Animo.for:360`). Detailed or aggregated hydrology is then derived (`Animo.for:372,382`).

For detailed hydrology, the record supplies end-of-interval values such as `Mofrt`, `Walet`, `Pnt` and fluxes, while `Mofro`, `Wale` and `Pn` represent the carried start state. `Hydro_detailed` therefore constructs the water-quality interval from a start/end hydrological pair.

A source scan of `Input_hydro.for` finds record reads and hydrological sanity handling but no explicit per-record equality assertion that `Tiwa` equals the already advanced ANIMO `Juda/Tito` timestamp. Temporal alignment is therefore sequence-coupled to the hydrology file. This is an `UNRESOLVED_ALIGNMENT_GUARD` seam, not evidence that supplied files are misaligned.

## 6. Residues, management and ploughing occur before chemical process rates

The sequence is:

1. root/crop production and residue preparation through `Root_plant`, `Grassprd`, `Root_grass` or `Root_extern` (`Animo.for:405-448`);
2. if a management event time is crossed, `Input_addit` reads that event packet (`Animo.for:460-465`);
3. `Addit` is always called (`Animo.for:468`);
4. `UBoundconc` updates the upper-boundary/surface-reservoir concentration state (`Animo.for:502`).

`Addit` does not merely stage transfers in scratch. It mutates current/start arrays such as `Conh`, `Coni`, `Copo`, `Os` and dissolved-organic concentrations directly before later rate and transport routines read them (`Addit.for:342-445`).

Within one management row, material addition is executed first. If `Pl(I)>0`, ploughing then mixes the resulting state and empties the reservoir (`Addit.for:448` onward). Consequently, an event row containing both an addition and ploughing has source semantics `ADD THEN PLOUGH`, not two unordered management actions.

`UBoundconc` runs after these mutations. Material newly placed in the virtual top reservoir is therefore eligible for the same interval's surface-reservoir/boundary update according to the active hydrology.

## 7. Crop demand before transformation, crop-state integration after transport

Crop uptake parameters are calculated after management and boundary update:

- `Uptpar_Plant` at `Animo.for:525`;
- `Uptpar_Grass` at `Animo.for:535`;
- `Uptpar_extern` at `Animo.for:544`.

These routines determine demand/selectivity parameters before organic transformation and mineral-N transport.

Actual nutrient uptake from soil is already a sink inside the transport equations. For generic solutes `TRANSPORT.FOR:225` includes `Se(Ln)*Flev(Ln)` in the outgoing mass term. The `Upintg_*` routines later integrate the corresponding realized nutrient uptake into crop result state using the step-average concentrations:

- `Upintg_Plant` at `Animo.for:914`;
- `Upintg_Grass` at `Animo.for:927`;
- `Upintg_Extern` at `Animo.for:938`.

Thus `Upintg_*` must not be reinterpreted as a second soil uptake operation. It is the plant-side state integration of a sink that has already participated in transport.

## 8. Potential pass before actual pass

Revision 53 contains a real two-stage biochemical sequence.

### 8.1 Potential pass

1. temperature and fraction setup (`Animo.for:554-566`);
2. `Rates1`, explicitly commented as potential rates without oxygen-status limitation (`Animo.for:572`);
3. `Transca('ANIMO-pot')`, potential labile DOM transport/transformation (`Animo.for:591`);
4. `Resp_miner(Itask=0)`, potential organic transformation/respiration demand (`Animo.for:616`);
5. preliminary `Transport('AMMONIUM','ANIMO-pot')` to obtain an NH4 average relevant to oxygen demand (`Animo.for:652`);
6. `Aeration_original` or `Aeration_sonicg` (`Animo.for:668,692`);
7. preliminary GHG calculation when enabled (`Animo.for:706`).

Potential-pass result/average arrays are provisional. Several are overwritten by the main pass. They are not accepted continuation state.

### 8.2 Actual pass

1. `Rates2`, actual rates with oxygen status (`Animo.for:726`);
2. `Transca('MAIN-ANIMO')` (`Animo.for:738`);
3. `Resp_miner(Itask=1)` (`Animo.for:764`);
4. actual NH4 `Transport` (`Animo.for:812`);
5. `Denitr` constructs the NO3 zero-order term from denitrification plus nitrification based on actual step-average NH4 (`Animo.for:828`; `Denitr.for:61-66`);
6. optional grass diffusive uptake adjustment (`Animo.for:837`);
7. `Correction(1)`, actual NO3 `Transport`, then `Correction(2)` (`Animo.for:843-862`);
8. final GHG calculation (`Animo.for:868`);
9. phosphorus `Transgen` (`Animo.for:891`).

The potential and actual calls are therefore not interchangeable duplicate computations. Their ordering is part of the revision-53 temporal contract.

## 9. Internal iterations and sequential layer ordering

### 9.1 Immobilization availability loop

`Resp_miner` traverses layers in `Sqnu` flow order and contains a maximum two-pass loop for N/P immobilization availability (`resp_miner.for:173-190,1229-1232`). When mineralization is negative, the routine may reduce assimilation after estimating available mineral N/P.

For that availability estimate, comments explicitly identify neighbouring NH4 and P concentrations as being from the previous timestep. NH4 uses `Conh(Ln-1)`/`Conh(Ln+1)` (`resp_miner.for:1076-1087`), and P uses `Copo(Ln-1)`/`Copo(Ln+1)` (`resp_miner.for:1141-1153`). This is an intentional stale/current mixture in the source algorithm and must not be silently replaced by same-step neighbour results.

### 9.2 Sequential solute transport

`TRANSPORT.FOR` traverses compartments in `Sqnu` order (`TRANSPORT.FOR:129-210`). After solving a layer it assigns the same-step average concentration to `Cob(Ln+1)` and `Coo(Ln)` (`TRANSPORT.FOR:183-187`). A downstream layer can therefore consume an upstream layer's same-step average concentration.

This makes the layer traversal order scientifically observable. A parallel or reordered implementation requires a separate equivalence argument; it is not source-equivalent by construction.

### 9.3 Phosphorus transport and phase exchange are coupled per layer

`Transgen` also traverses in `Sqnu` order (`Transgen.for:212-218`). For soil layers it calls `Transorp`, which solves P transport with fast/slow sorption and precipitation/dissolution terms for that layer (`Transgen.for:264-272`), then propagates `Avcopo` to neighbouring layers (`Transgen.for:289-294`).

Revision 53 therefore does not expose a simple global ordering of `all sorption` versus `all transport`. Those processes are coupled inside the layer solve.

## 10. Balances and output observe the completed interval

After crop result-state integration, `Outbal_calc` is called (`Animo.for:987`). It accumulates balance terms from the interval's state changes, fluxes, process rates, management delta arrays and step-average concentrations.

`Outbal_write(Itask=2)` follows (`Animo.for:1035`). When a reporting boundary is reached, it writes and resets balance accumulators. For example, water ending storages become the next reporting period's beginning storages and flux terms are zeroed (`Outbal_write.for:827-842`). Organic-matter ledgers use the same reporting-period pattern (`Outbal_write.for:1035-1057`). This reset does not modify the physical chemistry state.

`Outsel` then writes selected state/rate output (`Animo.for:1043`). The annual grass-output hook occurs after that, using the end timestamp to detect a boundary and `Juda-St` to identify the interval being closed (`Animo.for:1069-1072`).

`Outbal_calc` itself detects user balance periods using a half-step crossing test `Tiyr-0.5*St < T <= Tiyr+0.5*St` (`Outbal_calc.for:199-225`). This reporting boundary is distinct from management-event boundary predicates.

## 11. End-of-run and restart-style state

After the loop:

1. `Outbal_write(Itask=3)` closes final balance output (`Animo.for:1086`);
2. optional P-class state is output (`Animo.for:1094`);
3. `Output_Init` serializes final state (`Animo.for:1099`).

`Output_Init` writes final `Rs*` result fields for mineral N, organic pools, labile/stable DOM, crop state, mineral-P phase/site state and, when active, GHG system state (`Output_Init.for:81-165`). Macropore serialization is commented out (`Output_Init.for:137-153`).

A notable side effect occurs at `Output_Init.for:115-117`: negative `Rsamplpo_act` is overwritten with zero before writing. Therefore the revision-53 restart serializer is not a strictly read-only observer of final result state.

The generated `INITIAL.OUT` does not by itself prove exact continuation sufficiency. It does not serialize all temporal cursors, management-reader position, reporting accumulators or all externally owned hydrological coordinates. Split-run equivalence therefore remains a behavioural qualification question.

## 12. Source-bound accepted, provisional and derived semantics

The least misleading mapping of revision-53 source is:

| Source concept | Meaning in revision 53 | Architecture analogy, not source terminology |
|---|---|---|
| current/start arrays such as `Conh`, `Coni`, `Copo`, `Os`, `Mofro` immediately after `Init` | prior accepted/result state staged for the new interval | accepted-state snapshot |
| those same arrays after `Addit` | current-interval state already mutated by events/residues | mutable trial working state |
| `Rs*` arrays during potential pass | provisional results, often overwritten | trial scratch/provisional state |
| `Rs*` arrays after actual process solves | end-of-interval result state | candidate next state |
| `Av*`, `Rek*`, transformation/rate arrays | interval averages/rates/scratch | derived/trial scratch |
| balance arrays | reporting continuation, not physical stores | diagnostic continuation state |
| next call to `Init` | copies prior end result into current/start representation | delayed acceptance/staging boundary |

Revision 53 therefore supports the scientific need for explicit temporal generations, but it does not implement the ARCH01 rule that accepted state remains immutable during the whole trial.

## 13. Qualification boundary

This lifecycle is source-bound preparatory evidence. No claim is made that the order is scientifically optimal. No process has been reordered. No B2 historical executable reference is available in TS01. Any future implementation that changes event predicates, flow-order traversal, potential/actual staging, same-step management visibility, or previous-step neighbour reads must be treated as a behavioural change until independently qualified.
