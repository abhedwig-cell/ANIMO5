# TCD-016 conservation and rewetting contract

Work unit: `ANIMO-SQ01`

Status: `QUALIFICATION_CONTRACT_DEFINED_CANDIDATE_NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## 1. Control volume

The local control volume is the ANIMO surface compartment associated with layer 0, plus any explicitly admitted continuation phase owned by that same surface subsystem.

For NH4-N, define at a transition boundary:

- `M_aq`: aqueous NH4-N mass in layer 0, kg N m-2
- `M_dry`: explicit dry or immobile surface NH4-N mass, kg N m-2, only if such a state is admitted
- `M_other`: any other explicitly declared internal phase in the same control volume, kg N m-2
- `I_ext`: external NH4-N input during the step, kg N m-2
- `O_ext`: external NH4-N output during the step, kg N m-2
- `R`: net reaction loss from NH4-N to another named species or external gas during the step, kg N m-2. A reaction must have an explicit destination or species transfer.

The required local identity is:

`M_before + I_ext - O_ext - R = M_after`

with:

`M_before = M_aq_before + M_dry_before + M_other_before`

and:

`M_after = M_aq_after + M_dry_after + M_other_after`.

No numerical threshold may make a term disappear from this identity.

## 2. Aqueous storage definition

For layer 0 in the current source:

`M_aq = Mofr(0) * He(0) * C_NH4`.

Because `Mofr(0) * He(0)` is derived from ponding plus snow water storage, `M_aq` becomes unable to represent finite mass when that water storage becomes zero.

A concentration is therefore not a sufficient state coordinate through complete phase disappearance.

## 3. Phase-transfer rule for any acceptable continuation model

If a future candidate introduces a dry surface store, the wet-to-dry transfer must be formulated as an internal transfer after all independently defined boundary fluxes and reactions for the transition have been accounted for:

`T_aq_to_dry = max(0, M_aq_remaining_when_aqueous_phase_disappears)`

and then:

`M_aq_after = 0`

`M_dry_after = M_dry_before + T_aq_to_dry`.

This equation defines a conservation requirement, not a kinetic theory. The condition that triggers the physical disappearance of the aqueous phase must come from the admitted hydrological/state model, not from an arbitrary solute-concentration cap.

## 4. Dry-hold rule

For a dry interval with no admitted dry-phase process:

`M_dry_after = M_dry_before`

and:

`M_aq = 0`.

If future theory introduces volatilization, surface-soil transfer, crystallization, dissolution into microscopic water films or another dry-phase process, each must appear as a named transfer with source, destination, unit and rate law.

## 5. Rewetting rule

Rewetting is not qualified merely by making concentration finite.

An acceptable rewetting contract must specify:

1. activation condition for the receiving aqueous phase
2. amount transferred from dry to wet state during the timestep
3. whether transfer is instantaneous or kinetic
4. any fraction remaining dry after the step
5. interaction with runoff and infiltration during the same step
6. ordering relative to layer-1 NH4 adsorption and other reactions
7. restart state if rewetting is only partial.

A generic formulation is:

`T_dry_to_aq = F_rewet(M_dry_before, water_state, forcing, parameters, dt)`

with the hard bounds:

`0 <= T_dry_to_aq <= M_dry_before`

`M_dry_after = M_dry_before - T_dry_to_aq`

and:

`M_aq_after` includes exactly `+T_dry_to_aq` before any subsequent external transport or reaction removes it.

SQ01 does not qualify a particular `F_rewet` from the available ANIMO theory.

## 6. Synthetic conservation experiment

The experiment uses the source-bound TCD-016 event as its initial wet-to-dry state and then extends it with controlled dry-hold and rewet steps. It is diagnostic only. It is not a modified historical testcase.

### 6.1 Step S1: wet -> dry

Initial state from the captured event:

`M_before = 1.3880242022597072e-5 kg N m-2`.

For the isolated test:

- external solute input = 0
- declared NH4 reaction = 0
- physically represented solute outflow = 0 at the precision relevant to the legacy branch because `Avc=0`
- no initial dry store.

Legacy result:

| store/term | mass kg N m-2 |
| --- | ---: |
| aqueous before | 1.3880242022597072e-5 |
| dry before | 0 |
| external input | 0 |
| external output | 0 |
| reactions | 0 |
| aqueous after | 0 |
| dry after | 0 |
| closure residual | 1.3880242022597072e-5 |

This fails conservation.

Candidate A diagnostic result:

| store/term | mass kg N m-2 |
| --- | ---: |
| aqueous before | 1.3880242022597072e-5 |
| dry before | 0 |
| aqueous after | 0 |
| dry after | 1.3880242022597072e-5 |
| closure residual | 0 |

This proves that an explicit dry store can close the state transition. It does not prove that the store or transfer law is ANIMO's intended science.

### 6.2 Step S2: dry hold

Controlled forcing:

- zero ponding water
- zero NH4 input
- zero NH4 output
- zero admitted dry-phase reactions.

Candidate A diagnostic result:

`M_dry_before = M_dry_after = 1.3880242022597072e-5 kg N m-2`

closure residual = 0.

The legacy model cannot perform this experiment with retained mass because it has no state coordinate for the dry mass.

### 6.3 Step S3: dry -> wet

For a purely diagnostic remobilization test, introduce exactly `1.0e-3 m` of water storage and temporarily assume complete instantaneous dissolution of the dry store.

Then:

`M_aq_after = 1.3880242022597072e-5 kg N m-2`

`M_dry_after = 0`

and the resulting concentration is:

`C = M / V = 0.013880242022597071 kg N m-3`.

Closure residual = 0.

This concentration is finite because a finite water volume exists. The experiment demonstrates a conservative state path only. It must not be interpreted as qualification of instantaneous dissolution kinetics.

## 7. Residual-water conditioning experiment

At the captured wet-to-dry event the actual final water storage is:

`Mt * Ld = 3.256434e-6 m`.

If the complete remaining mass were held in that water, concentration would be approximately:

`4.2624 kg N m-3`.

When the hydrological ponding state subsequently reaches exactly zero, conservation by concentration alone requires division by zero. Introducing an arbitrary positive floor merely moves the singularity into a policy choice and creates water that is not owned by the hydrological state.

Candidate C therefore fails the conditioning and ownership contract under current ANIMO hydrology.

## 8. Restart contract

Any admitted continuation state must satisfy checkpoint equivalence:

`run(A -> checkpoint -> restart -> B) == run(A -> B)`

for the complete physical state, within the separately qualified numerical precision policy.

For Candidate A this requires the checkpoint to preserve at minimum:

- dry surface NH4 mass
- phase-active flag only if not derivable from water state
- any kinetic rewetting state if future theory introduces one.

The existing `Rsconh(0)` restart coordinate is insufficient because concentration at zero water volume cannot encode dry mass.

## 9. Interaction with soil adsorption

Surface dry mass and soil-layer sorption must remain separate owners.

A transfer from the surface subsystem to soil layer 1 must be attached to a physical transport or process event. Once NH4 mass arrives in the first soil layer, existing ANIMO soil adsorption can partition it according to the admitted soil theory.

No admissible implementation may directly change `Cxnh(1)` merely because layer-0 water disappears.

## 10. Interaction with transport ordering

A future implementation must declare whether rewetting transfer is applied:

- before same-step runoff
- before same-step infiltration into layer 1
- before or after upper-boundary additions are mixed
- before or after NH4 reactions.

Different orderings can change trajectories even when total mass closes. Therefore process ordering is part of the scientific contract, not an implementation detail.

## 11. Reject conditions

A continuation candidate is rejected if any of the following is true:

- mass disappears at wet-to-dry transition
- the same mass exists in more than one store after a transfer
- finite mass is represented only by unbounded concentration as water tends to zero
- dry-to-wet remobilization has no defined destination
- restart omits a state required to reproduce future behaviour
- units mix concentration, areic mass and solid-phase content without explicit conversion
- a numerical threshold is treated as physical phase theory without evidence
- an existing reservoir or sorbed state is reused despite incompatible ownership semantics
- an external outflow is invented solely to close the ledger.

## 12. Qualification gates still open

The following Class C gates remain open after SQ01:

- authoritative ANIMO-specific theory for the missing continuation phase
- authoritative rewetting/remobilization law
- independent scientific review of that phase model
- expected trajectory differences over a physical application envelope
- non-interference tests after a scientifically specified candidate exists.

The conservation, units, ownership and restart requirements are now explicit, but the missing scientific theory prevents corrected-legacy admission.
