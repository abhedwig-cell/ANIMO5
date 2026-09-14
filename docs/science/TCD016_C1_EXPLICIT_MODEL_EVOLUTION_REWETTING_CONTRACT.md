# TCD-016-C1 explicit model-evolution rewetting assessment

Work unit: `ANIMO-SQ09`

Branch: `work/animo-sq09-tcd016-c1-explicit-model-evolution`

Base: `ANIMO-B3B14@1f13c7cab30772f4aa8d5071b19d13761c2b5f16`

## Purpose

B3B14 established that TCD-016 cannot become ready for a separate B3 admission while the continuation state has no scientifically bounded continuation-to-receiver lifecycle. SQ09 is the separately authorized model-evolution decision workunit for that blocker.

Authorization to evaluate a new model assumption is not scientific evidence for that assumption. SQ09 therefore separates three questions:

1. Can one minimal rewetting candidate be specified without hidden state, arbitrary thresholds or unconstrained parameters?
2. Does the candidate satisfy the already qualified state, transfer, mass, restart and failure envelopes?
3. Is the candidate scientifically qualified under the B3Q01 Class F requirements?

The answers are yes, yes at contract level, and no with the present evidence.

## Frozen inputs

SQ09 consumes but does not rewrite the qualified TCD-016 lineage. SQ02 provides the finite continuation owner `M_surface_NH4_non_aqueous_continuation`, unit `kg N m-2`, within the surface chemistry ponding control volume. SQ03 requires every nonzero change to be a typed transfer and permits exact no-process persistence only as fail-closed safety semantics. SQ06 found no concrete dry-hold physical law. SQ07 found no scientifically qualified rewetting receiver, activation or kinetics. SQ08 qualified only a chemically noncommittal NH4-N provenance envelope, not a physical phase or molecular species. MASSQ04 fixes the storage identity `S_NH4=S_aq+S_complex+S_cont` and forbids balance accounting from inventing physics.

B3B14 then concluded that a state representation plus mass conservation is not sufficient to close the parent. The remaining admission-blocking scientific surface is the rewetting lifecycle, with TCD-016-E1 still dependent on C1.

## Candidate space

SQ09 considered five useful alternatives and one fail-closed control.

`M0` keeps the continuation mass indefinitely whenever no separately qualified process exists. This is a valid safety state but not a parent scientific lifecycle. Promoting it to permanent physical inertness would silently change the meaning of the upstream negative qualifications.

`M1` defines a new functional model abstraction, `REWETTABLE_SURFACE_NH4_N_RESIDUE_EQUIVALENT`. It does not claim a salt, solid phase, sorbed state, counter-ion, hydration state or molecular species. It says only that, within this proposed model evolution, the continuation owner is treated as a rewettable NH4-N equivalent when explicit surface aqueous storage reappears.

`M2` uses partial or finite-rate remobilization. It requires a fraction, rate, equilibrium parameter or similar quantity that presently has no provenance or validation basis.

`M3` sends the continuation mass directly to the first soil layer. That adds infiltration-coupled receiver physics which SQ07 did not qualify.

`M4` chooses a specific solid, salt or molecular identity. SQ08 explicitly found that evidence insufficient.

`M5` splits the mass among multiple receivers. No current evidence defines the fractions, kinetics or competing destinations.

M1 is therefore the least parameterized candidate that can be made fully operational for testing. Selection means selection for Class F assessment, not scientific admission.

## Selected candidate M1

The candidate uses the existing continuation state as source and the logical surface aqueous NH4 storage, `S_aq`, as receiver.

Activation occurs only when explicit positive surface aqueous storage exists in the same control volume. This is a state-topology condition, not a new numerical threshold. SQ09 does not use the legacy 0.1 mm boundary, the legacy `Fu` guard, a concentration floor or any invented epsilon.

At activation the candidate applies one atomic internal transfer:

`T_rewet = M_cont_before`

`M_cont_after = 0`

`S_aq_after = S_aq_before + T_rewet`

Therefore:

`M_cont_before + S_aq_before = M_cont_after + S_aq_after`

exactly, before any later process changes the control volume.

The ordering contract is:

1. establish the explicit surface aqueous storage;
2. apply the continuation-to-surface-aqueous transfer;
3. only then allow any process that exports or transforms surface aqueous NH4, including runoff, infiltration, sorption after arrival, biochemical transformation or atmospheric loss.

No direct transfer to layer 1 or `Conhtop` reinterpretation is introduced.

The event is parameter-free and atomic. Before activation, restart restores exact `M_cont`. A checkpoint may not expose a half-applied rewetting event. After the event the source pool is zero, so repeated evaluation cannot transfer the same mass twice and no hidden process-memory variable is required.

If no surface water exists, the candidate emits no transfer and the already qualified fail-closed state persistence remains in force. If the source mass is zero, activation is a no-op. If a later dry-down creates new continuation mass, that new mass is eligible at the next activation.

## Important low-storage consequence

A full transfer into any positive surface water volume can create a very large aqueous concentration when the volume is very small. SQ09 does not hide or numerically regularize this consequence. It introduces no clipping, concentration ceiling, minimum water volume, export threshold or tolerance.

That surface belongs to the already atomized Class E child TCD-016-E1. Because the M1 physical contract is not scientifically qualified in SQ09, E1 remains blocked. Even after a future scientific admission of a rewetting contract, E1 would still require its own numerical-policy qualification.

## Why M1 is not scientifically qualified here

B3Q01 classifies a change in constitutive process behavior as Class F model evolution unless authoritative intended theory proves that it is actually a corrected legacy formulation. Class F requires, among other things, authoritative theory and validation evidence appropriate to the process. It cannot be admitted as a B3 legacy correction merely because it conserves mass or is operationally convenient.

M1 has a bounded scientific rationale: it is conservative, parameter-free, restart-explicit, falsifiable and does not require a hidden dry-state concentration. Its relationship to the legacy baseline is also explicit: it is new model evolution, not a claim about revision-53 behavior. Calibration implications are nil and the conservation identity is exact.

Two gates nevertheless fail.

First, there is no pinned authoritative ANIMO theory or qualified material-identity evidence showing that the entire continuation mass is physically a completely and instantaneously rewettable NH4 equivalent. Naming a new functional state does not make its constitutive behavior true.

Second, the current evidence contains no qualified observation or experiment that distinguishes complete instantaneous remobilization from partial remobilization, finite-rate release, direct soil transfer or transformation. Synthetic tests can validate the algebra and state machine, but they cannot validate physical behavior.

Generic external ammonium chemistry is not used to bridge this gap. SQ08 leaves the continuation material physically unidentified, so generic solubility or fertilizer literature cannot establish that this particular modeled state follows M1 without a qualified material mapping or a discriminating experiment.

The Class F result is therefore fail-closed:

`QUALIFIED_NEGATIVE_CLASS_F_CANDIDATE_NOT_SCIENTIFICALLY_ADMISSIBLE_WITH_CURRENT_EVIDENCE`

The canonical B3 routing remains:

`PHYSICS_CHANGE_REQUIRES_SEPARATE_SCIENTIFIC_ADMISSION`

This is a routing/disposition statement, not an admission.

## Evidence strength and maturity

M1 is retained as a bounded `RESEARCH_ISOLATED` candidate. The contract-level oracle may prove:

- no transfer while dry;
- exact complete source-to-receiver transfer when activated;
- exact same-control-volume mass conservation;
- no double transfer after the source pool reaches zero;
- repeatability over separate dry/wet cycles.

Those checks are model-evolution evidence for algebra, lifecycle and implementation boundaries only. They are not B2 historical evidence and are not physical process validation.

Historical revision-53 behavior remains `UNKNOWN_WITHOUT_B2`.

## Consequence for TCD-016

SQ09 does not close C1 scientifically and does not make the parent ready for B3 admission. C1 remains `UNRESOLVED_NOT_ADMITTED`; the parent remains `UNRESOLVED_NOT_ADMITTED`; E1 remains blocked; no queue, TCD register, aggregate, routing, central testbank, B4 or production authority is changed.

The next scientifically useful work is not to invent a rate constant or relax the evidence gate. It is to acquire evidence capable of testing M1: a traceable material-to-process basis and/or a dry-down/rewetting experiment or observational dataset that measures retained NH4-N, receiver behavior and release time course well enough to discriminate complete instantaneous remobilization from the live alternatives.

Only after that evidence is qualified should a separate Class F scientific-admission workunit be considered. Only after an appropriate rewetting contract is scientifically qualified or separately admitted should TCD-016-E1 numerical-policy qualification proceed.
