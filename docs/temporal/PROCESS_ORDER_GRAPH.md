# ANIMO-TS01 process order graph

Status: `SOURCE_BOUND_TEMPORAL_AUDIT`

This graph reconstructs revision-53 execution order from the frozen source. An arrow means `executes before / can feed`. It does not mean that the later process always consumes every earlier output.

## 1. Main execution graph

```text
PRE-LOOP
  Input1
    -> optional Input_SoilTemper
    -> optional Input_cropext
    -> Inicalc
    -> Input_Echo
    -> Outbal_write(Itask=1)
    -> Juda = Judami

TIMESTEP LOOP while Juda < Judama
  [advance Sttot, Stnu, Tiyr, Tito, Juda to interval end]
    -> Init
       | previous Rs* -> current/start arrays
       | first-step special initialization
       | crop/year boundary handling
       | reset current-step Ad* reporting deltas
    -> first-step-only Outbal_Init
    -> Input_hydro
    -> Hydro_Aggregated OR Hydro_detailed
    -> crop/residue preparation
       | Root_plant
       | OR Grassprd -> Root_grass
       | OR Root_extern
    -> event predicate
       | if Juda >= Tinead AND Juda-St < Tinead
       |    -> Input_addit
       -> Addit
          | continuous/root/crop residues
          | management material addition
          | same event row: addition -> ploughing/mixing
    -> UBoundconc
    -> crop demand/selectivity
       | Uptpar_Plant
       | OR Uptpar_Grass
       | OR Uptpar_extern
    -> temperature / Fracpoint
    -> POTENTIAL PROCESS PASS
       Rates1
       -> Transca('ANIMO-pot')
       -> Resp_miner(Itask=0)
       -> Transport(NH4, 'ANIMO-pot')
       -> Aeration_original OR Aeration_sonicg
       -> optional GHGasses(1)
    -> ACTUAL PROCESS PASS
       Rates2
       -> Transca('MAIN-ANIMO')
       -> Resp_miner(Itask=1)
       -> Transport(NH4, 'MAIN-ANIMO')
       -> Denitr
       -> optional grassup3
       -> Correction(1)
       -> Transport(NO3, 'MAIN-ANIMO')
       -> Correction(2)
       -> optional GHGasses(2)
       -> if P active: Transgen(P, 'MAIN-ANIMO')
    -> crop result-state integration
       | Upintg_Plant
       | OR Upintg_Grass
       | OR Upintg_Extern
    -> optional Outputgr
    -> Outbal_calc
    -> Outbal_write(Itask=2)
    -> Outsel
    -> year/final-boundary Outputgr_yr hook
  [next loop starts; next Init stages the Rs* just produced]

POST-LOOP
  Outbal_write(Itask=3)
  -> optional Output_InitPCl
  -> Output_Init
```

Primary source anchors: `Animo.for:225-1109`.

## 2. Interval semantics graph

For a normal non-first timestep, the state generations are:

```text
previous interval end result R(n)
          |
          | Init at beginning of loop n+1
          v
current/start representation C(n+1,t0)
          |
          | Addit / event and residue mutation
          v
mutated current-step working state W(n+1,t0+events)
          |
          | demand + potential process calculations
          v
provisional potential result/averages P(n+1)
          |
          | actual process calculations overwrite/recompute
          v
end-of-interval result R(n+1,t1)
          |
          +-> crop result integration
          +-> Outbal_calc / reports
          +-> Output_Init only if final interval
          |
          | next timestep Init, if another interval exists
          v
current/start representation C(n+2,t1)
```

The source does not contain an explicit end-of-step `commit(R -> C)`. Staging occurs at the next step's `Init`.

## 3. Flow-order subgraph for generic solute transport

`TRANSPORT.FOR` uses the hydrologically determined `Sqnu` sequence:

```text
K = 1-Flpn
  -> Ln = Sqnu(K)
  -> solve layer Ln with Transsub
  -> write Avco(Ln), Rsco(Ln), Rscx(Ln)
  -> Cob(Ln+1) = Avco(Ln)
  -> Coo(Ln)   = Avco(Ln)
  -> K = K+1
  -> next Sqnu layer
```

Source: `TRANSPORT.FOR:129-210`.

Consequence: the average concentration produced in one layer during the same interval can become the incoming concentration for the next layer. The graph is therefore sequential and direction-dependent. `Sqnu` order is part of the numerical/temporal semantics.

## 4. Phosphorus subgraph

Phosphorus is not executed as separate global `transport -> sorption -> precipitation` phases. `Transgen` traverses the `Sqnu` layer order and calls `Transorp` per soil layer:

```text
Transgen
  -> Ln = Sqnu(K)
  -> gather current Copo / Amcxfa / Amcxsl / Ampopr
  -> Transorp(
       transport,
       equilibrium sorption,
       non-equilibrium sorption,
       precipitation/dissolution,
       crop-uptake sink,
       process source/sink)
  -> write Rscopo / Rsamcxfa / Rsamcxsl / Rsampopr
  -> Avcopo(Ln) becomes neighbour input
  -> next layer
```

Source: `Transgen.for:212-294`.

Any architecture that schedules sorption/desorption as an independently reorderable whole-profile process would therefore not match the literal source algorithm.

## 5. Organic transformation and immobilization subgraph

`Resp_miner` has an internal per-layer, at-most-two-pass loop:

```text
for Ln in Sqnu order
  iter = 1
  -> calculate organic transformations / Tomnni / Tomnpo
  -> if immobilization requires mineral N or P
       estimate available mineral nutrient
       using current layer plus incoming neighbour concentrations
       NOTE: neighbour Conh/Copo are explicitly previous-timestep values
       -> possibly reduce assimilation factor
  -> iter = iter + 1
  -> if actual pass and shortage remains, second calculation
```

Source: `resp_miner.for:173-190,1076-1153,1229-1232`.

The potential invocation terminates this loop early (`If(pot) iter = iter + 1`, `resp_miner.for:1230`).

## 6. Nitrogen dependency chain

```text
post-management current NH4/NO3 state
  -> Uptpar_* determines uptake selectivity
  -> Rates1 / potential Resp_miner
  -> preliminary NH4 Transport
  -> aeration / oxygen limitation
  -> Rates2
  -> actual Resp_miner produces NH4 source/sink terms
  -> actual NH4 Transport produces Avconh
  -> Denitr uses Avconh and Rekinh to construct nitrification contribution to Rekoni
  -> optional grassup3 modifies NO3 uptake/source terms
  -> Correction(1) snapshots Rekoni
  -> NO3 Transport
  -> Correction(2) adjusts denitrification bookkeeping for changed Rekoni
  -> crop-state Upintg_* records realized uptake from Avconh/Avconi
```

The source therefore establishes these ordering dependencies:

- actual NH4 transport precedes the NO3 nitrification contribution;
- NO3 transport follows the final `Rekoni` construction;
- plant-side uptake integration follows the transport step that already applied the soil-side uptake sink.

## 7. Management-event graph

Management events use the predicate:

```text
Juda >= Tinead  AND  Juda-St < Tinead
```

Source: `Animo.for:460`.

So an event at `E` is assigned to the interval `(t0,t1]`.

When selected:

```text
Input_addit
  -> read Nuad and event rows
  -> advance management file cursor / Adnr / next Tinead
  -> Addit
       -> material addition mutates current state
       -> if PL(I)>0: ploughing/mixing runs after that addition
  -> UBoundconc
  -> all subsequent process-rate and transport calculations
```

Source: `Input_addit.for:53-218`; `Addit.for:313-448+`.

## 8. Harvest and crop-boundary graph

Annual crop harvest/root-residue handling in `Addit` uses:

```text
Juda > Tiha  AND  Juda-St <= Tiha
```

Source: `Addit.for:244-301`.

This assigns a harvest time to `[t0,t1)`, not to the management event convention `(t0,t1]`. The difference is observable at exact interval endpoints and must be preserved or explicitly qualified.

`Init` separately derives:

- `Kicrold = Kicr(detmanper(..., Juda-St))`;
- `Kicryn  = Kicr(detmanper(..., Juda))`.

Source: `Init.for:139-143`.

Thus a single interval may deliberately carry both start-of-interval and end-of-interval crop identities.

## 9. Balance lifecycle graph

```text
Init
  -> reset Nuad and Ad* per-step management reporting deltas
Addit
  -> mutate physical/current state
  -> fill Ad* deltas for addition/redistribution
process/transport routines
  -> produce Rs*, Av*, Rek*, transfer totals
Upintg_*
  -> finish crop result state
Outbal_calc
  -> accumulate physical interval observations into reporting arrays
  -> determine whether report period closes
Outbal_write(Itask=2)
  -> when period closes: write report
  -> copy report ending storage to next report beginning storage
  -> reset report-period flux/process accumulators
Outsel
  -> write selected state/rate output
```

This confirms that balance reset is a reporting transaction, not a physical state acceptance boundary.

## 10. Restart boundary graph

```text
last actual process step
  -> final Rs* result state
  -> Outbal_calc / Outbal_write / Outsel
  -> loop exits
  -> Outbal_write(Itask=3)
  -> Output_Init
       writes selected final Rs* and Mofrt
       may clamp Rsamplpo_act < 0 to zero
       does not serialize all temporal/reporting/external-owner state
```

There is no final `Init` before `Output_Init`. Therefore `INITIAL.OUT` represents selected result/end fields, not a serialized image of the ordinary post-`Init` current/start representation.

## 11. Event hooks and loop/iteration inventory

| Hook/loop | Frequency | Ordering significance |
|---|---|---|
| main `Do While (Juda<Judama)` | one per hydrological interval | top-level temporal schedule |
| hydrology record peek for variable `St` | before `Init` | determines interval end before state staging |
| management event predicate | once per interval | selects `(t0,t1]` event packet |
| `Addit: Do I=1,Nuad` | all event rows in packet, source order | each row is applied sequentially; plough follows that row's addition |
| `Resp_miner: Do While iter<=2` | per layer, actual immobilization path | availability-dependent second calculation |
| generic `Transport` Sqnu loop | per species call | same-step upstream/downstream coupling |
| `Transgen` Sqnu loop | P active | same-step P transport/phase coupling |
| `Aeration_original -> Oxydem` | original aeration option | internal oxygen solution/iteration seam; delegated to aeration routine |
| balance-period crossing | after physical interval | report-period write/reset only |
| annual grass-output hook | after all interval output | closes year using end boundary and prior interval date |

## 12. Order dependencies that TS01 treats as non-reorderable without evidence

The following are source-observed dependencies, not recommendations:

1. previous `Rs*` staging occurs before the current hydrology record is consumed;
2. residues and management are visible to uptake demand and all subsequent chemical processing in the same interval;
3. same-row fertilization precedes ploughing;
4. top-reservoir additions precede `UBoundconc`, allowing same-interval boundary processing;
5. crop demand/selectivity precedes transformations and transport;
6. potential rates/respiration/NH4 transport precede aeration, which precedes actual rates;
7. actual organic transformations precede actual NH4 transport;
8. actual NH4 average concentration feeds later nitrification/NO3 source construction;
9. NO3 transport follows denitrification and correction setup;
10. P is solved after the mineral-N chain and is internally transport/phase coupled per layer;
11. crop result-state integration follows the soil transport sinks;
12. mass-balance accumulation follows all physical result updates;
13. report-period reset follows balance accumulation;
14. final restart-style serialization occurs only after the last reporting phase.

TS01 does not claim that every one of these dependencies is physically necessary in a different model formulation. It establishes that changing them is not source-equivalent by assumption.
