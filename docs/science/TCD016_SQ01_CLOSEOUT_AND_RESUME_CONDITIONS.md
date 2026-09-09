# ANIMO-SQ01 closeout and resume conditions for TCD-016

Work unit: `ANIMO-SQ01`

Target: `TCD-016`

Status: `EVIDENCE_COMPLETE_FOR_SQ01_SCOPE_BLOCKED_ON_EXTERNAL_SCIENTIFIC_DEPENDENCIES`

Production migration: `NOT_ADMITTED`

## 1. Why SQ01 should stop here

SQ01 has reached the point where further source scanning is unlikely to resolve the controlling scientific uncertainty.

The work unit has already established, source-bound and diagnostic-bound:

- the natural NH4 mass-loss event;
- the exact `Transsub` deletion path;
- the shared `0.1 mm` surface-state activation seam in hydrology and layer-0 transport;
- the two-step deactivation lifecycle;
- the absence of an existing persistent surface NH4 owner across deactivation;
- the distinction from soil NH4 sorption and the additions reservoir;
- the pathological nature of forcing the missing mass through a tiny water flux;
- the need to atomize the problem into physical-state ownership (`TCD-016-C1`) and numerical transition policy (`TCD-016-E1`);
- the shared surface-representation hazard for other solutes without widening the historical discrepancy beyond evidence;
- a review-ready conservative continuation-state hypothesis;
- a prepared independent scientific review packet.

Additional general soil-chemistry and porous-media literature has now been separated into `TCD016_EXTERNAL_SCIENCE_CONTEXT.md`. That evidence supports the plausibility of a conservation shell for model evolution, while also showing why specific adsorption, volatilization, precipitation and remobilization laws cannot be silently inferred.

The remaining blocker is therefore not a missing code location.

It is a scientific model-definition decision.

## 2. Current authoritative SQ01 conclusions

Parent TCD:

`TCD-016 = UNRESOLVED_NOT_ADMITTED`

Primary class:

`C_MISSING_PHYSICAL_STATE_OR_INCOMPLETE_STATE_MODEL`

Secondary class:

`E_NUMERICAL_POLICY_CHANGE`

Preferred model-evolution hypothesis:

`M_surface_NH4_non_aqueous_continuation [kg N m-2]`

Scientific status:

`PREFERRED_PROPOSED_MODEL_EXTENSION_REVIEW_READY_NOT_ADMITTED`

Overall route:

`PHYSICS_MODEL_EXTENSION_REQUIRED`

unless authoritative historical ANIMO theory is recovered that defines the intended continuation phase and transitions.

## 3. What would justify resuming SQ01

SQ01 should be reopened only when at least one of the following evidence changes occurs.

### Resume trigger A: authoritative ANIMO theory recovered

Examples:

- full-text Alterra Report 983;
- another authoritative ANIMO 3.x/4.x process/design document;
- source-history documentation that explicitly explains the physical meaning of the surface deactivation and remobilization behaviour.

Required effect:

The evidence must address phase identity, dry-hold semantics or remobilization, not merely repeat general conservation or ponding descriptions.

### Resume trigger B: independent scientific review completed

Use:

`docs/science/TCD016_C1_INDEPENDENT_REVIEW_PACKET.md`

The review must separate:

- conservation-state acceptability;
- required physical phase specificity;
- dry-hold processes;
- rewetting/remobilization law;
- status of the legacy `0.1 mm` boundary;
- species-general topology versus species-specific chemistry.

A scientific review does not itself create B3 admission.

### Resume trigger C: explicit governance decision for model evolution

If the project explicitly decides that Candidate A is to be evaluated as new ANIMO5 physics rather than corrected legacy behaviour, the next work should be a separate scientific model-evolution qualification.

That route must not be represented as closure of historical TCD-016 by a local bug fix.

### Resume trigger D: new historical runtime evidence materially changes scope

Examples:

- a newly recovered authoritative executable/toolchain establishes relevant layer-0 runtime state;
- a natural historical case demonstrates the same surface-state failure for another species;
- a historical case disproves an SQ01 source interpretation.

Such evidence should first be evaluated for whether it changes TCD-016 or requires a separate discrepancy.

## 4. What does not justify resuming SQ01

Do not reopen this work unit merely to:

- search the same frozen source again for the same branch;
- tune `1e-6`, `Factor=100` or the `Fu` threshold without C1 semantics;
- add a concentration cap;
- route missing mass through an artificial outflow;
- reuse `Conhtop` because it already persists;
- force mass into first-layer sorption because that state exists;
- assume instantaneous redissolution from the diagnostic closure experiment;
- widen TCD-016 to all solutes solely from shared code reachability;
- convert the adjacent `Transca` index-0 initialization finding into a TCD without runtime/consequence evidence.

## 5. Handoff if model evolution is authorized

A future model-evolution qualification should start from the following minimum contract rather than from legacy `Transsub` branch edits.

### State topology

One persistent continuation mass owner in areic units, independent of aqueous volume.

### Internal transfers

Explicit typed transfers from surface aqueous state into continuation state and from continuation state into each scientifically justified receiving state.

### Process separation

Potential dissolution, soil exchange, adsorption, volatilization, biochemical reaction or precipitation must be separate process contracts rather than hidden consequences of a representation switch.

### Numerical separation

Only after physical semantics are fixed may `TCD-016-E1` qualify transition thresholds, conditioning, precision sensitivity and timestep behaviour.

### Restart

Continuation mass must be canonical restart/checkpoint state and must satisfy restart equivalence across wet, crossing and dry intervals.

### Conservation

Every transition must satisfy a closed control-volume identity with no mass creation, deletion or invented external export.

## 6. Minimum future qualification sequence

If model evolution is authorized, the recommended dependency order is:

1. independent scientific disposition of C1;
2. explicit continuation-state phase/process contract;
3. cold initialization and restart semantics;
4. wet-to-continuation transition qualification;
5. dry-hold process qualification;
6. continuation-to-wet/other-phase remobilization qualification;
7. E1 numerical transition-envelope qualification;
8. natural NH4 regression and application-envelope non-interference;
9. separately scoped cross-species topology review;
10. B3 or successor governance decision appropriate to model evolution.

## 7. Persisted evidence set

Core reconstruction and qualification:

- `TCD016_DRY_SOLUTE_STATE_RECONSTRUCTION.md`
- `TCD016_CONTINUATION_STATE_CANDIDATES.md`
- `TCD016_CONSERVATION_AND_REWETTING_CONTRACT.md`
- `TCD016_C1_PROPOSED_NONAQUEOUS_STATE_CONTRACT.md`
- `TCD016_E1_LOW_STORAGE_THRESHOLD_RECONNAISSANCE.md`
- `TCD016_ATOMIZATION_AND_GATE_PLAN.md`

Theory and review:

- `TCD016_THEORY_EVIDENCE_SWEEP.md`
- `TCD016_HISTORICAL_THEORY_RECOVERY.md`
- `TCD016_EXTERNAL_SCIENCE_CONTEXT.md`
- `TCD016_C1_INDEPENDENT_REVIEW_PACKET.md`

Surface/scope evidence:

- `TCD016_SURFACE_STATE_ACTIVATION_SEAM.md`
- `TCD016_SHARED_SOLUTE_REACHABILITY.md`
- `TCD016_TRANSCA_LAYER0_PARAMETER_AUDIT.md`

Machine-readable records remain under:

`integration/animo-science/`.

## 8. Closeout decision

`SQ01_INTERNAL_EVIDENCE_WORK = COMPLETE_FOR_CURRENT_SCOPE`

`SQ01_REOPEN = ONLY_ON_NEW_SCIENTIFIC_OR_HISTORICAL_EVIDENCE_OR_EXPLICIT_MODEL_EVOLUTION_AUTHORITY`

`TCD-016-C1 = BLOCKED_PENDING_SCIENCE`

`TCD-016-E1 = BLOCKED_DEPENDS_ON_C1`

`PRODUCTION_MIGRATION = NOT_ADMITTED`
