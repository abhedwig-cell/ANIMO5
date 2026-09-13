# ANIMO-SQ03 — TCD-016-C1 dry-hold and rewetting process-envelope qualification

Work unit: `ANIMO-SQ03`

Target: `TCD-016-C1`

Parent: `TCD-016`

Branch: `work/animo-sq03-tcd016-c1-process-envelope`

Base: `ANIMO-SQ02@09ab76f0b44cb72956875fa379d68bbf97f1a0c7`

Current global B3 closure authority at authoring start: `ANIMO-B3Q06@11e9bcdc6654e63f84875bf1f28dc54abe725700`

Current aggregate authority at authoring start: `ANIMO-RG05O@bc9e6ed997a078336645210ebb4d99ae976893fe`

GOV05 authority: `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`

This workunit does not modify production source, frozen B0, the canonical TCD register, the central queue, B4, or any B3 admission.

## 1. Purpose

SQ02 qualified only the model-evolution state topology: a persistent, chemically noncommittal areic continuation owner can conserve layer-0 NH4 mass when aqueous surface storage ceases to be a usable coordinate. SQ02 deliberately did not qualify a dry-phase identity, a dry-period reaction law, a remobilization law, or the legacy numerical thresholds.

SQ03 asks the next narrower question:

> What process envelope can be scientifically and architecturally fixed before a particular dry-phase chemistry or rewetting kinetic law is known?

The answer is not a new kinetic model. It is a fail-closed interface contract that prevents unqualified physics from being smuggled into an implementation.

## 2. Pinned upstream evidence

The substantive evidence is inherited by exact SHA from SQ01 and SQ02.

SQ01 established:

- the natural NH4 mass-loss event at the surface wet-to-dry transition;
- absence of an existing generic dry surface NH4 owner;
- semantic separation of layer-0 aqueous NH4, soil-layer sorption, and `Conhtop/Rsconhtop`;
- the exact local conservation identity;
- the generic bounded rewetting form `0 <= T_dry_to_aq <= M_dry_before`;
- that instantaneous redissolution is diagnostic only, not qualified kinetics;
- that a dry-hold equality can be used only when no dry-phase process has been admitted.

SQ02 then qualified the continuation-state topology for model evolution while preserving all process-law uncertainty.

A live WUR publication-record recheck on 2026-09-13 again confirmed Alterra Report 983 and its eDepot target. The full text remained unavailable from the current work environment because the eDepot endpoint returned access denial. That acquisition attempt is not promoted into theory evidence and no negative claim about uninspected Report 983 text is made.

## 3. Qualified process-envelope semantics

### 3.1 Epistemic persistence rule

When the continuation owner exists and **no explicitly qualified transfer or transformation is active**, the required state update is:

`M_cont_after = M_cont_before`

This is qualified as an epistemic fail-closed persistence rule. It means the model may not delete, manufacture, reroute, volatilize, sorb, nitrify, precipitate, dissolve, or otherwise transform continuation mass merely because no process law has been specified.

It is **not** a scientific assertion that real surface NH4 is chemically inert during dry periods.

A production-quality physical model remains incomplete until the relevant dry-period processes are qualified for the intended application envelope.

### 3.2 Every nonzero change requires a typed transfer

Any change in continuation mass must be accounted for by one or more named transfers with:

- source owner;
- destination owner or declared external sink;
- element/species identity;
- unit `kg N m-2` at the state-transfer interface;
- activation condition;
- amount or rate law;
- ordering relative to other transfers;
- restart semantics if transfer can be partial or delayed.

The MassLedger may observe these transfers but may not infer or create them.

### 3.3 Rewetting remains an interface, not a law

For a future transfer from continuation state to aqueous surface NH4:

`T_rewet = F_rewet(M_cont_before, water_state, forcing, parameters, dt)`

with hard bounds:

`0 <= T_rewet <= M_cont_before`

and exact ownership updates:

`M_cont_after = M_cont_before - T_rewet`

`M_aq_gain = T_rewet`

before subsequent declared runoff, infiltration, adsorption, or reaction removes any part of the aqueous mass.

SQ03 qualifies these bounds and ownership identities only. It does not qualify the functional form of `F_rewet`, a transfer fraction, a timescale, a concentration law, or instantaneous dissolution.

### 3.4 Hydrological activation must not be invented from a solute threshold

A future rewetting law must be activated by an admitted receiving aqueous state. The legacy `0.1 mm` representation boundary and the `Fu` threshold are not promoted into physical phase theory by SQ03.

If a later process model chooses one of those values as a physical trigger, it must provide independent scientific qualification.

### 3.5 Process ordering is scientific state semantics

A concrete future process law must declare ordering relative to at least:

- re-creation of surface aqueous storage;
- upper-boundary additions mixing;
- same-step runoff;
- same-step infiltration to layer 1;
- NH4 soil adsorption after mass reaches soil water;
- NH4 transformation and atmospheric loss processes.

Different orderings can change trajectories while conserving total mass. Therefore ordering cannot be left as an implementation accident.

## 4. Candidate process families and current disposition

The following process families are physically plausible in general science but remain unqualified for the continuation state in ANIMO5:

| process family | current disposition | reason |
| --- | --- | --- |
| NH3 volatilization | `UNQUALIFIED` | requires phase identity plus pH, temperature, water/chemical state and a qualified flux law |
| nitrification or other biochemical conversion | `UNQUALIFIED` | requires a defined active phase and environmental controls |
| transfer to soil water | `UNQUALIFIED` | requires a physical interface-transfer law and ordering with infiltration |
| transfer to soil sorption | `UNQUALIFIED` | cannot bypass aqueous/soil ownership without a qualified cross-phase transfer |
| precipitation/fixation/crystallization | `UNQUALIFIED` | no ANIMO-specific continuation-phase theory recovered |
| rewetting dissolution/remobilization | `UNQUALIFIED_FUNCTION`, bounded interface only | destination/bounds are known, kinetics are not |

General scientific context can justify keeping these possibilities open. It does not select one.

## 5. Why the dry-hold rule is not hidden inertness

A strong counter-hypothesis is that keeping `M_cont` unchanged when no process is admitted is itself an unqualified physical law.

That would be true if SQ03 claimed physical completeness or production adequacy. It does not.

The qualified statement is narrower: **an unspecified process has zero authority to mutate conserved state**. Persistence is therefore the neutral state-update rule of the conservation shell while process physics remains unresolved. The residual uncertainty explicitly records that real NH4 may transform during that interval.

This distinction matters because the opposite policy, silently applying a guessed sink or destination, would irreversibly encode unqualified physics and could no longer be separated from conservation repair.

## 6. Exact oracle contract

`tools/sq03/tcd016_c1_process_envelope_oracle.py` exercises only algebraic envelope properties using `Decimal` arithmetic and no tolerance:

- exact dry-hold persistence for the canonical SQ01 residual mass;
- exact bounded rewetting partitions for zero, partial, and complete transfer fractions;
- sequential partial transfers without loss or duplication;
- rejection of fractions below zero or above one;
- rejection of an implicit untyped sink.

This oracle is synthetic architecture evidence. It is not B2, not a process calibration, and not a historical trajectory baseline.

## 7. Adversarial boundaries

SQ03 must fail closed against all of the following overclaims:

- persistence proves chemical inertness;
- a generic bounded `F_rewet` qualifies a kinetic law;
- conservation alone identifies the receiving phase;
- instantaneous dissolution is the default;
- soil sorption can receive continuation mass directly;
- a concentration cap or water floor can replace the continuation owner;
- the legacy `0.1 mm` or `Fu` threshold is automatically physical;
- current synthetic evidence substitutes for historical B2;
- this workunit opens E1 numerical qualification;
- this workunit admits TCD-016-C1 or the parent TCD-016.

## 8. Qualification decision

The bounded SQ03 decision is:

`QUALIFY_TCD016_C1_FAIL_CLOSED_PROCESS_ENVELOPE_FOR_MODEL_EVOLUTION; QUALIFY_STATE_PERSISTENCE_WHEN_NO_PROCESS_IS_ADMITTED_AND_EXACT_BOUNDED_TYPED_TRANSFER_INTERFACE; KEEP_ALL_SPECIFIC_DRY_AND_REWETTING_PROCESS_LAWS_UNQUALIFIED`

Consequences:

- C1 remains `UNRESOLVED_NOT_ADMITTED` for B3;
- the parent TCD-016 remains `UNRESOLVED_NOT_ADMITTED`;
- E1 remains blocked because numerical transition policy must not be qualified before the physical activation/process contract is specified;
- production migration remains unauthorized;
- historical behavior remains `UNKNOWN_WITHOUT_B2`.

## 9. Next scientifically meaningful work

A later workunit may choose one process family only when it has an explicit scientific basis. The highest-value next evidence remains authoritative ANIMO-specific dry-surface/re-wetting theory or a deliberately new ANIMO5 process formulation with an application envelope, calibration/parameter basis, observables, and falsification criteria.

Until such evidence exists, SQ03 should be treated as the interface contract around unresolved physics, not as the physics itself.
