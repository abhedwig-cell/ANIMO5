# ANIMO-TS01 event boundary semantics

Status: `SOURCE_BOUND_TEMPORAL_AUDIT`

The frozen revision-53 source uses several different temporal boundary predicates. They must not be normalized into one generic event convention without behavioural qualification.

Let `t0 = Juda-St` and `t1 = Juda` for the interval being processed.

## 1. Management events: `(t0,t1]`

The main program reads a management packet when:

```fortran
If(Juda.ge.Tinead .and. (Juda-St).lt.Tinead) Then
   Call Input_addit(...)
End If
```

Source: `Animo.for:460-465`.

Therefore a management event at time `E` is assigned to the interval for which:

` t0 < E <= t1 `

Consequences at exact boundaries:

- `E == t0`: not selected in this interval;
- `E == t1`: selected in this interval.

`Input_addit` reads all `Nuad` event rows for that event period and then advances `Adnr` and converts the next event time to the absolute simulation axis (`Input_addit.for:86-218`). The file-reader cursor is therefore continuation state in a broad behavioural sense even though it is not serialized by `INITIAL.OUT`.

## 2. Same-row management order: addition before ploughing

Inside `Addit`, each management row is processed sequentially (`Do I=1,Nuad`, `Addit.for:315`). Material is added first (`Addit.for:334-445`). Ploughing for that same row is then performed only afterward (`Addit.for:448+`).

Ploughing explicitly includes emptying the surface/addition reservoir. It sums the post-addition reservoir and layer state, records redistribution deltas, and redistributes the combined material through the selected plough depth.

Source semantics for a row with both `Qumt(I)>0` and `Pl(I)>0` are therefore:

`MATERIAL ADDITION -> PLOUGH/MIX`

A future event system that applies ploughing first, treats both actions as unordered, or moves ploughing to the next interval changes legacy behaviour.

## 3. Annual crop harvest/root-residue boundary: `[t0,t1)`

Annual crop harvest/root-residue handling in `Addit` uses:

```fortran
If (Juda.Gt.Tiha(Manper) .And. (Juda-St).Le.Tiha(Manper)) Then
   ...
End If
```

Source: `Addit.for:244-301`.

The harvest time `H` is therefore assigned to:

` t0 <= H < t1 `

This is the opposite endpoint convention from management additions:

| Event | Exact `t0` | Exact `t1` | Interval convention |
|---|---|---|---|
| management addition/plough packet | excluded | included | `(t0,t1]` |
| annual harvest/root-residue trigger | included | excluded | `[t0,t1)` |

This asymmetry is source evidence. TS01 does not assume it is intentional science, nor does it classify it as a defect without behavioural/theory evidence.

## 4. Crop transition semantics use both interval endpoints

`Init` evaluates crop identity twice:

```fortran
Kicrold = Kicr(detmanper(Tiso,Mamp,Juda-St))
Kicryn  = Kicr(detmanper(Tiso,Mamp,Juda))
```

Source: `Init.for:139-143`.

The same interval can therefore have a start crop identity and an end crop identity. Crop-state resets and grass initialization use combinations of `Kicrold`, `Kicryn`, harvest dates and the current interval boundary (`Init.for:157-181`; `Animo.for:299-323`).

A migrated scheduler cannot replace this with a single `crop_at_step` value without proving that all transition cases remain equivalent.

## 5. Year boundary semantics

At `Init`, the date is derived from the interval start:

```fortran
call GDATE(Juda-St, ...)
If(Juda-St<=Judami .or. (Month==1 .and. Day==1)) Then
   Stnu = 1
   ... annual deposition/current-year values ...
End If
```

Source: `Init.for:122-136`.

Thus annual-input/reset semantics are anchored to `t0`.

After all interval processing and output, the main program checks the interval end:

```fortran
call GDATE(Juda, ...)
If(Juda>=Judama .or. (Month==1 .and. Day==1)) Then
   call GDATE(Juda-St, ...)
   ... Outputgr_yr ...
End If
```

Source: `Animo.for:1069-1072`.

Thus a step ending exactly on 1 January closes annual output after physical processing, while the following `Init` sees 1 January at its start and activates new-year start semantics. The two hooks occur on opposite sides of the boundary.

## 6. Balance-period boundaries are a third convention

`Outbal_calc` determines report-period closure after physical state calculation. For specified balance dates it uses:

```fortran
If (Tiyr-0.5*St.Lt.T .And. Tiyr+0.5*St.Ge.T) Then
   Optout(Ly)=1
End If
```

Source: `Outbal_calc.for:199-225`.

This is a half-step crossing rule around the current `Tiyr`, not the management or harvest endpoint rule. Once the period is selected, `Outbal_write(Itask=2)` writes the report, moves ending report storage to beginning storage for the next report period, and zeros period flux/process accumulators.

These report resets do not accept or change physical chemistry state.

## 7. Initialization boundary

The first loop iteration is special:

1. initial state was constructed by `Input1`/`Inicalc` before the loop;
2. the main clock is advanced to the first interval end;
3. `Init` takes its first-step branch rather than copying a previous `Rs*` state;
4. `Outbal_Init` captures beginning-storage semantics before current-step hydrology and management (`Animo.for:336`);
5. `Init` zeroes the current-step management reporting deltas before `Addit`.

This means a synthetic one-step case must distinguish initialization projection from first runtime transfer. The first interval is not evidence for an ordinary restart/continuation transition.

## 8. Restart boundary

Revision 53 writes `INITIAL.OUT` only after the simulation loop. It does not checkpoint during the ordinary timestep body.

The end-of-run sequence is:

`last physical interval -> balance/output -> loop exit -> Outbal_write(Itask=3) -> Output_Init`.

Because there is no following `Init`, final `Rs*` arrays are serialized directly. The restart-style output is therefore taken from the end/result generation, whereas ordinary inter-step continuation first passes through the next `Init` staging operation.

No source evidence establishes that an arbitrary split at this boundary is strongly equivalent to an uninterrupted run. Temporal cursors, management-reader position, report accumulators and coordinated external hydrology state are not all represented in `INITIAL.OUT`.

## 9. First and last timestep asymmetry

| Aspect | First timestep | Ordinary middle timestep | Last timestep |
|---|---|---|---|
| current/start state | initial input/projection | copied from prior `Rs*` in `Init` | copied from prior `Rs*` in `Init` |
| result arrays entering step | special initialized/zeroed values | previous results then reset/reused as needed | previous results then reset/reused as needed |
| beginning balance | `Outbal_Init` explicit | prior report period state | prior report period state |
| following acceptance copy | yes, if a second step exists | yes | no |
| restart-style serialization | no | no | `Output_Init` from final `Rs*` |

Tests that only inspect middle timesteps do not cover first/last boundary semantics.

## 10. Temporal conservation mapping to PREP06

PREP06 identifies physical transfers independently of their reporting implementation. TS01 adds when those transfers are generated, applied and observed.

| PREP06 identity / transfer family | Generated or selected | Applied to physical state | Accumulated/reported | Temporal hazard |
|---|---|---|---|---|
| `ID-MATERIAL-ADDITION` | management packet selected before `Addit` | immediately in `Addit`, before rates | `Ad*` deltas consumed later by `Outbal_calc` | double booking if event journal and legacy `Ad*` both treated as physical |
| `ID-REDISTRIBUTION` | same management row | after same-row addition in `Addit` | redistribution deltas later in `Outbal_calc` | order reversal changes mixed composition; TCD-017 is reporting-side omission, not permission to move state mutation |
| `ID-CROP-RESIDUE/HARVEST/GRAZING` | crop/residue logic before management chemistry | current state is mutated in `Addit` | balance observation later | harvest endpoint rule differs from management rule |
| `ID-ORG-TRANSFORM` | potential then actual rate construction | actual `Transca`/`Resp_miner` writes `Rs*` and source terms | `Outbal_calc` after all processes | provisional pass must not be committed or counted twice |
| `ID-N-MINERALIZATION` | `Resp_miner(Itask=1)` | represented in organic result state plus NH4 source/sink terms consumed by NH4 transport | balance later | availability correction uses previous-step neighbour state |
| `ID-NITRIFICATION` | final contribution constructed after actual NH4 average exists | enters later NO3 transport through `Rekoni` | balance/GHG after NO3 path | moving nitrification before actual NH4 changes dependency |
| `ID-DENITRIFICATION` | aeration computes potential/limitation, `Denitr` assembles NO3 term | consumed by NO3 transport | later balance/GHG | source/rate bookkeeping spans multiple routines |
| `ID-P-SORPTION` | inside per-layer `Transgen/Transorp` | coupled with P transport/phase update | balance after P solve | cannot be safely split into globally reorderable phases by assumption |
| `ID-SOLUTE-LAYER/PROFILE` | flux/source terms available before solver | `Transport`/`Transgen` solve sequentially in `Sqnu` order | `Toin/Toou`, `Av*`, `Rs*` observed by balances | same-step upstream average feeds downstream layer |
| `ID-CROP-N/P` | selectivity before transport | soil-side uptake sink inside transport | plant-side result gain later in `Upintg_*`; balance after | implementing both as separate sinks would double-remove nutrient |
| `ID-DRYDOWN` | transport solver detects vanishing/negative solution state | guard can overwrite concentrations/results | balance only sees resulting state/flux terms | TCD-016 can miss mass because no continuation state/explicit export exists |
| `ID-REPORT-ACCUM` | contribution exists after physical process | no physical state application | `Outbal_calc` and detailed reporting arrays | reporting reset/write timing must not be confused with physical commit |

## 11. Double-count and missed-event risks

TS01 identifies the following migration risks without changing the source:

1. **crop uptake double application**: soil uptake is already a sink in transport; `Upintg_*` is the plant-side state gain;
2. **management double application**: a typed future event plus retained legacy `Addit` mutation would apply the same material twice;
3. **plough/add reorder**: converting one row to independent events can reverse source order;
4. **endpoint duplication or omission**: using one universal event predicate would move exact-boundary management or harvest events;
5. **provisional-pass double count**: potential `Transca`/NH4 results are overwritten and must not enter committed transfer totals as physical events;
6. **report-reset-as-commit error**: `Outbal_write` resets observation state after reporting but does not define physical acceptance;
7. **restart event replay**: `INITIAL.OUT` alone does not serialize the management-file cursor. Reinitializing management input at a split point can replay or skip an event unless the continuation protocol resolves the cursor from absolute time exactly as legacy does;
8. **year-boundary shift**: moving annual resets to `t1` rather than the next step's `t0` can change annual forcing/crop bookkeeping;
9. **final-state generation error**: serializing current/start arrays after the last step would be stale because legacy writes final `Rs*` directly.

## 12. Source-bound event tests to implement later

These specifications are safe as synthetic causal tests, but they are not B2 evidence:

- management event exactly at `t0`, inside interval, and exactly at `t1`;
- annual harvest exactly at `t0`, inside interval, and exactly at `t1`;
- one event row with both fertilizer addition and `PL>0`, checking add-then-mix state;
- virtual-reservoir fertilization with nonzero same-step hydrology, checking whether new material participates in `UBoundconc` that interval;
- crop transition spanning one timestep, recording `Kicrold` and `Kicryn` use;
- interval ending on 1 January, checking annual closeout followed by next-step new-year initialization;
- balance date centered within a multi-day step, checking the half-step report crossing rule;
- first-step and final-step sentinels to verify special `Init` and final `Output_Init` generations.

Acceptance for these tests is exact source-order/event selection, not an invented scientific tolerance.
