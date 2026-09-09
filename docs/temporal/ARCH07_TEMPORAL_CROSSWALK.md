# ANIMO-TS01 to ARCH07 temporal qualification crosswalk

Status: `POST_CLOSE_RECONCILIATION_EVIDENCE`.

This crosswalk checks whether the candidate ARCH07 adapter qualification suite already covers the temporal constraints reconstructed by TS01. It does not edit or supersede ARCH07. ARCH07 remains authoritative for its own candidate adapter test specification at head `7e6f7bcb492cd36bf7a852235e93b796a6d2a8f6`.

## 1. Main result

ARCH07 covers the future transaction identity, rollback, commit barrier, checkpoint-owner separation and reference split-run framework well. It also covers realized crop uptake linkage and hydrology frame generation identity.

It does **not** attempt to qualify most source-internal temporal semantics. That is appropriate, but it means a future implementation cannot treat ARCH07 PASS as evidence that the ANIMO process scheduler is temporally source-equivalent.

The missing temporal layer is now made explicit by `TS01_SCHEDULER_SENTINELS.csv`.

## 2. Areas already represented in ARCH07

### Hydrology frame timing and generation identity

TS01-S20 maps strongly to:

- `H001` valid detailed frame;
- `H009` accepted-generation mismatch;
- `H011` configuration/binding mismatch;
- `T001` begin-trial identity binding.

ARCH07 already requires interval and accepted-generation identity before process execution. TS01 adds the legacy-specific reason this matters: revision 53 relies on sequential hydrology record consumption and does not itself prove explicit per-record time alignment.

### Crop uptake transfer linkage

TS01-S14 maps to `C005` and `C006`. ARCH07 requires realized N/P uptake to be linked to the matching typed transfer event and remain uncommitted before accept. TS01 adds the source ordering constraint that the soil sink occurs during transport and plant integration follows later. Both are needed to prevent double application.

### Rejected trial atomicity

TS01-S26 maps to `T002`, and its replay consequence maps to `T009`. This is future architecture behaviour, not a literal legacy retry mechanism.

### Checkpoint and split-run framework

TS01-S19 and S21-S25 map partly or strongly to `T006` and `T008`. ARCH07 already reserves owner-correct checkpoint and split-run experiments. TS01 adds the exact legacy event, crop/year, report-period and final-generation boundaries that those experiments must exercise.

## 3. Scheduler semantics intentionally outside ARCH07

The following TS01 requirements are not adapter-field conformance tests and should remain owned by a process-scheduler/TIME qualification layer:

- S01 clock-before-staging;
- S02 result-to-start staging;
- S08 potential-before-actual pass;
- S10 previous-step neighbour reads in `Resp_miner`;
- S11 `Sqnu` sequential same-step propagation;
- S12 actual NH4 before NO3 source/transport chain;
- S13 per-layer coupled P transport/sorption/precipitation;
- S15 balance observation after physical completion;
- S16 report reset is not a physical commit;
- S18 final serialization uses end/result generation.

ARCH07 should reference these sentinels when a concrete adapter is embedded in a runtime, but it should not duplicate them as adapter schema rules.

## 4. Event-adapter gap

TS01-S03 through S07 and S17 expose a separate gap between normalized configuration and runtime event scheduling:

- management uses `(t0,t1]`;
- annual harvest/root residue uses `[t0,t1)`;
- same-row addition precedes ploughing;
- same-step additions are visible before `UBoundconc` and later chemistry;
- crop identity can differ at the two interval endpoints;
- year closeout and next-year initialization live on opposite sides of the boundary.

ARCH07 contains crop residue/export bundle tests (`C008-C010`) but no test currently establishes these legacy event-time predicates or row-order semantics. That is not a defect in ARCH07's stated scope. It is a distinct scheduler/management-adapter qualification need.

A future management/event adapter specification should import S03-S07 and S17 rather than inventing a generic event interval convention.

## 5. Split-run refinement

ARCH07 `T008` currently specifies a generic accepted-boundary split-run comparison. TS01 decomposes this into at least four distinct behavioural families:

1. clean non-event split, S22;
2. event split before/after management, S21/S23;
3. crop/harvest/year boundary split, S24;
4. mid-report-period split with physical and diagnostic continuation separated, S25.

Passing only the clean case would not establish the others. In particular, management cursor state and report accumulators are continuation hazards not proven by physical state restoration alone.

## 6. Final serializer refinement

ARCH07 `T006` tests owner-correct checkpoint composition, but TS01-S18/S19 add two source-specific requirements:

- the last legacy interval has no following `Init`, so final state comes from the `Rs*` end/result generation;
- legacy `Output_Init` can mutate `Rsamplpo_act` by clamping it before write, so a modern serializer must either remain pure or represent such compatibility behavior explicitly.

This does not mean the modern checkpoint should reproduce the clamp. It means reproducing it cannot be hidden inside serialization.

## 7. Admission consequences

A future runtime should require separate evidence for:

- `ADAPTER_RUNTIME`: ARCH07 field/identity conformance;
- `TEMPORAL_SCHEDULER`: TS01 source-order and generation sentinels;
- `COUPLED_TRANSACTION`: ARCH07 transaction tests plus TS01 temporal bindings;
- `REFERENCE_BEHAVIOR`: split-run/order/event equivalence after PREP02R provides independent evidence;
- `SCIENTIFIC_ADMISSION`: any intentional change to source-observed order or event semantics.

No one layer substitutes for the others.

## 8. Qualification boundary

This crosswalk is documentation and traceability only. It changes no ARCH07 artifact, defines no production adapter, executes no coupled runtime, and does not alter the TS01 qualified closeout decision.
