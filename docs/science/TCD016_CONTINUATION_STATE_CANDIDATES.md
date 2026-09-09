# TCD-016 continuation-state candidates

Work unit: `ANIMO-SQ01`

Status: `CANDIDATES_QUALIFIED_FOR_DISPOSITION_NOT_FOR_B3_ADMISSION`

Production migration: `NOT_ADMITTED`

## Decision rule

A candidate is acceptable for further scientific admission only if it can represent mass through wet -> dry -> wet transitions without deletion, duplication or a concentration singularity, and if its phase ownership, units, restart state and remobilization semantics can be stated explicitly.

Conservation by itself is necessary but not sufficient. In particular, forcing the residual mass through an arbitrarily small water flux is rejected because it replaces a missing state with a pathological concentration.

## Candidate A: explicit dry or immobile surface-solute store

### Proposed state

Introduce a surface phase state such as:

`M_dry_NH4_surface [kg N m-2]`

owned by the surface chemistry or ponding control volume, separate from:

- aqueous layer-0 NH4 concentration
- soil-layer adsorbed NH4
- the fertilizer additions reservoir.

The state should be an areic mass, not a concentration. That avoids requiring water volume while the phase is dry.

### Wet-to-dry transfer

When the aqueous surface phase disappears, any mass not accounted for by declared external outflow or reaction remains inside the control volume and is transferred internally from aqueous layer-0 storage to the dry store.

The transfer is not an external flux and must not appear as leaching or runoff.

### Dry hold

During a fully dry interval the store remains unchanged unless a separately qualified dry-phase process acts on it. SQ01 does not infer dry volatilization, sorption or reaction kinetics from general chemistry.

### Rewetting

At rewetting, some or all dry-store mass must transfer back into an aqueous or other explicitly defined phase. A simple diagnostic assumption of instantaneous dissolution closes conservation, but SQ01 does not qualify that kinetic rule as ANIMO theory.

If a future theory source establishes finite dissolution, volatilization, crystallization or surface-soil exchange, those must be represented as explicit transfers rather than hidden concentration adjustments.

### Interaction with adsorption

The current source has NH4 sorption state for soil layers, not for the ponding layer. Therefore the dry store must not automatically become `Cxnh(1)` or another soil sorption store. Once remobilized NH4 actually enters layer 1 through a water or process transfer, the existing soil sorption theory can act there normally.

### Interaction with transport

The dry store is immobile with respect to water transport while no aqueous phase exists. Mobile transport begins only after transfer to an aqueous state. This avoids interpreting zero-water storage as a highly concentrated mobile solution.

### Restart

The dry store must be part of canonical restart/checkpoint state. A restart that persists only `Rsconh(0)` is insufficient once dry storage exists.

### Architecture

This candidate fits the PREP06 ownership rule well:

- one explicit physical owner
- unit `kg N m-2`
- accepted and result state
- typed internal transfers `surface_aqueous -> surface_dry` and `surface_dry -> surface_aqueous_or_other_phase`
- ledger observes the transfer rather than becoming the owner.

### Numerical conditioning

Good. Mass remains finite while water volume tends to zero. Concentration is computed only when an aqueous phase is representable.

### Scientific status

`PREFERRED_PROPOSED_MODEL_EXTENSION`

The state is scientifically coherent as a conservative abstraction, but the available ANIMO-specific theory does not define this dry phase or its rewetting kinetics. Under the SQ01 hard rule it cannot be labelled corrected legacy behaviour yet.

## Candidate B: absorb continuation mass into existing sorbed or solid phase

### Possible interpretation

Move residual layer-0 NH4 into the existing adsorbed NH4 state, for example in the first soil layer.

### Conservation

Algebraically possible if the exact same mass is removed from aqueous layer 0 and added to a declared sorbed store.

### Scientific problem

The legacy phase ownership does not support this transfer:

- `Socfnh` and `Rhbd` are mapped to soil layers `1..Nl`
- the ponding layer has no corresponding solid matrix owner
- the diagnostic event has zero layer-0 sorption contribution
- moving mass into layer 1 requires an interface transfer and adsorption process that is not represented by the drying event itself.

ANIMO 4.0 documents NH4 sorption to soil, but that does not imply that disappearance of ponded water instantaneously deposits all residual ammonium into the first soil-layer sorption pool.

### Rewetting

If moved to soil sorption, later release would follow soil desorption/partition semantics rather than surface-residue dissolution. That materially changes future state and flux trajectories.

### Restart

Existing soil sorbed state is restartable, so storage mechanics are available. This does not solve the scientific ownership problem.

### Numerical conditioning

Good if the transfer were physically justified.

### Scientific status

`REJECTED_AS_CORRECTED_LEGACY_CANDIDATE`

Reason: it introduces an unsupported cross-phase and cross-compartment transfer. It may be a possible future physical model only if independent theory specifies such deposition/sorption behaviour.

## Candidate C: residual-water representation

### Possible interpretation

Never permit chemically active aqueous storage to reach zero. Maintain a minimum residual water volume and keep all remaining mass dissolved in it.

### Conservation

At any positive residual water volume, aqueous mass can be conserved as:

`M_aq = V_residual * C`.

For the observed event the actual final water areal storage is:

`Mt * Ld = 3.256434e-6 m`.

Holding the full residual NH4 mass in that volume would require about:

`4.2624 kg N m-3`.

That is finite for this particular step, but when hydrology subsequently supplies exactly zero ponding water the required concentration becomes undefined unless an artificial positive water floor is introduced.

### Scientific problem

The hydrological owner says ponding water can disappear. A chemically active residual water floor would therefore create water state that is not part of the supplied hydrological balance unless the hydrological model itself defines such a phase.

The required floor is also a numerical/state policy. Its size changes concentration and potentially reactions or transport. Selecting it from the existing `Transsub` threshold would confuse a numerical threshold with a physical water content.

### Rewetting

Mathematically easy because the residual solution is already present. Physically it assumes the solute stayed in a mobile or chemically equivalent aqueous phase throughout the dry interval.

### Restart

Restart would have to preserve the residual water state as well as concentration. Persisting concentration alone is not enough if the hydrological state is zero.

### Numerical conditioning

Poor near the imposed floor. Concentrations scale as `1/V_residual` and become highly sensitive to the arbitrary residual volume.

### Scientific status

`REJECTED_WITH_CURRENT_ANIMO_HYDROLOGY`

This candidate could only be reconsidered if authoritative ANIMO/SWAP coupling theory defines a nonzero chemically active residual surface-water film independently of the numerical transport threshold.

## Candidate D: reuse the existing artificial additions reservoir

### Possible interpretation

On disappearance of layer-0 ponding water, transfer residual dissolved mass into the existing top-reservoir state `Conhtop * Hetop`, then let `UBoundconc` remobilize it later.

### Conservation

Algebraically possible because the top reservoir is already a persistent mass-bearing state.

### Scientific problem

ANIMO theory and source semantics give this reservoir a specific purpose: delayed release of fertilizer/addition material, with residence time governed by water flux through `Hetop`. It is not a generic dry-residue phase for solute previously present in ponding water.

Using it for TCD-016 would silently change:

- state provenance
- release kinetics
- routing during later ponding
- interpretation of management additions
- restart meaning of `Conhtop`.

### Interaction with adsorption and transport

Remobilization would follow the artificial reservoir's flux law, not a source-supported dry-residue law. This can delay or reroute mass independently of the actual surface chemistry.

### Restart

Mechanically available, scientifically mislabelled.

### Numerical conditioning

Good, because mass is stored over finite `Hetop`, but good conditioning does not validate phase semantics.

### Scientific status

`REJECTED_SEMANTIC_ALIASING`

A pre-existing variable is not automatically an admissible physical owner for a new mass phase.

## Candidate comparison

| criterion | A explicit dry store | B soil sorption | C residual water | D additions reservoir |
| --- | --- | --- | --- | --- |
| mass conservation possible | yes | yes | yes if water floor > 0 | yes |
| no concentration singularity | yes | yes | no | yes |
| existing ANIMO state owner | no | yes, but wrong compartment/phase | no physical owner for extra water | yes, but wrong purpose |
| wet -> dry semantics explicit | yes, proposed | unsupported | artificial water floor | semantically aliased |
| dry hold defined | yes, proposed | yes under soil sorption | only with ghost water | yes under reservoir law |
| dry -> wet defined by ANIMO theory | no | not for this transfer | implicitly yes but unsupported | reservoir release exists but wrong semantics |
| restart can be made complete | yes, new state required | mechanically yes | requires water-state extension | mechanically yes |
| conditioning | good | good | poor near floor | good |
| corrected legacy claim defensible now | no | no | no | no |
| disposition | preferred extension | reject | reject | reject |

## Rejected counterfactual: force all mass through tiny outflow

The earlier diagnostic counterfactual that moves the entire remaining mass through the observed tiny `Fu` closes the ledger, but requires an average concentration of order `3.37e4 kg N m-3` for the captured event. This is not a physical continuation state. It is explicitly excluded from the candidate set.

## Candidate conclusion

Candidate A is the only candidate evaluated here that simultaneously provides:

- an explicit mass destination
- finite state at zero water storage
- unambiguous conservation bookkeeping
- clean restart semantics
- separation from soil sorption and fertilizer-reservoir ownership
- stable numerical conditioning.

That makes A the preferred design hypothesis, not an admitted correction. No available ANIMO-specific theory source in the SQ01 evidence set defines the dry surface phase or its rewetting kinetics. Therefore Candidate A must remain a proposed model extension until stronger theory and independent scientific review are obtained.
