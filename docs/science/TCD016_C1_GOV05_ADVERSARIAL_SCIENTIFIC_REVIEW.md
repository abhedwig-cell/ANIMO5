# ANIMO-SQ02 — TCD-016-C1 GOV05 adversarial scientific review

Work unit: `ANIMO-SQ02`

Target: `TCD-016-C1 surface NH4 continuation-state ownership`

Branch: `work/animo-sq02-tcd016-c1-continuation-state-scientific-review`

Base authority: `ANIMO-B3Q06@11e9bcdc6654e63f84875bf1f28dc54abe725700`

Upstream scientific packet: `ANIMO-SQ01@26d0c74aa440bd73c23709d313e24ea8af2a0bcd`

Review governance: `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`

This workunit does not patch production source, does not admit TCD-016 into B3, does not open B4, and does not change the canonical queue. Its purpose is narrower: decide whether the SQ01 noncommittal areic continuation-state concept is scientifically acceptable as a **model-evolution topology**, while separating that topology from any still-unqualified physical phase or process law.

## 1. Fixed evidence inherited from SQ01

SQ01 established and persisted the following source-bound facts:

- the frozen source archive is SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- the frozen testbank archive is SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- the natural layer-0 NH4 event at `TITO=1490` contains `1.3880242022597072e-5 kg N m-2` before the wet-to-low-storage transition;
- the observed `Transsub` branch returns zero remaining and average aqueous concentration while no declared outflow or alternate owner receives that mass;
- layer 0 is the ponding/surface aqueous compartment;
- the existing `Conhtop/Rsconhtop` state is a distinct additions reservoir with its own provenance and release law;
- no existing generic dry surface NH4 state was found;
- soil NH4 sorption belongs to soil-layer state, not the layer-0 ponding compartment;
- the parent `TCD-016` was atomized into C1 state ownership and E1 numerical transition policy, with E1 dependent on C1.

SQ02 does not reinterpret these as B2 evidence and does not increase their historical-evidence strength.

## 2. Supplemental ANIMO-specific theory recovery

During SQ02, the public WUR full-text record for the ANIMO 3.5 process report was rechecked:

`https://edepot.wur.nl/363774`

In section 2.1.3 that report describes an **imaginary storage reservoir at the soil surface** into which additions are dissolved and whose remaining material is retained by bookkeeping until rainfall releases it. This is consistent with SQ01's source reconstruction of `Conhtop/Rsconhtop` as an additions reservoir.

That evidence strengthens one negative conclusion: the existing top reservoir must not be silently repurposed as a generic destination for residual solute from a disappearing ponding compartment. Its documented role is management/addition storage.

The official WUR publication record for Alterra Report 983 remains identifiable as the ANIMO 4.0 process description, but SQ02 does not claim that all of its full text has been ingested into immutable repository evidence. Therefore no negative assertion is made about uninspected passages.

## 3. Scientific question reviewed

The review question is not:

> Which dry NH4 phase did historical ANIMO intend?

That remains unanswered.

The bounded question is:

> Is an areic, chemically noncommittal continuation mass a scientifically defensible **conservation shell for model evolution** when the current aqueous concentration coordinate loses the ability to represent finite mass?

Proposed topology coordinate:

`M_surface_NH4_non_aqueous_continuation [kg N m-2]`

This name deliberately avoids asserting crystallization, sorption, precipitation, residual liquid water, or any other specific phase.

## 4. Adversarial alternatives

### 4.1 Delete the residual mass when water disappears

Rejected. Disappearance of an aqueous coordinate is not a declared external nitrogen flux or transformation. It cannot, by itself, satisfy the mass-control-volume identity.

### 4.2 Force all residual mass through the tiny water outflow

Rejected. SQ01 showed that this closes the ledger only by generating a pathological concentration and still fails to define a persistent state if water reaches zero.

### 4.3 Reuse first-layer sorbed NH4

Rejected as an automatic repair. It invents a cross-compartment and cross-phase transfer that is not implied by the representation transition.

### 4.4 Reuse `Conhtop/Rsconhtop`

Rejected as semantic aliasing. Source reconstruction and ANIMO 3.5 process documentation both identify that state as the fertilizer/additions reservoir, not a generic residual-ponding state.

### 4.5 Maintain a positive ghost-water floor

Rejected with current hydrology. It invents water storage and makes concentration depend on an arbitrary physical/numerical floor.

### 4.6 Require a fully specified molecular phase before any continuation owner may exist

This is the strongest remaining counter-hypothesis. SQ02 does **not** reject the need for specific phase/process theory before production physics is admitted. It rejects only the stronger claim that no conservation-shell state may exist in a model-evolution architecture until every dry-phase process is known.

A model can carry conserved mass in a semantically explicit unresolved continuation owner while refusing to apply unqualified chemistry to it. That is a state-topology decision, not a claim that real NH4 is chemically inert.

## 5. Review disposition

SQ02 qualifies the following disposition:

`ACCEPT_NONCOMMITTAL_CONSERVATION_STATE_FOR_MODEL_EVOLUTION_WITH_ADDITIONAL_PROCESS_QUALIFICATION`

The qualification is intentionally narrow.

Qualified now:

1. a finite conserved surface-NH4 mass requires an owner independent of aqueous volume if it remains in the modeled control volume after the aqueous representation disappears;
2. an areic mass coordinate is suitable for that conservation-shell role because it remains finite at zero aqueous storage;
3. the owner must be persistent state and restart/checkpoint state if implemented;
4. transfers into and out of the shell must be explicit typed internal transfers, not hidden ledger corrections;
5. the MassLedger may observe but must not own or reconstruct this state;
6. the shell must not inherit fertilizer-reservoir, soil-sorption, volatilization, dissolution, or precipitation semantics without separate scientific qualification.

Not qualified now:

- a specific dry physical phase;
- dry-period chemical inertness;
- volatilization, sorption, precipitation, nitrification, or other dry-phase rates;
- instantaneous or finite-rate redissolution;
- transfer to layer 1;
- use of `0.1 mm` as a physical phase threshold;
- use of `Fu > 1e-6 m d-1` as a physical criterion;
- corrected historical ANIMO behavior;
- B3 admission;
- any production implementation.

## 6. Consequence for TCD-016-C1 and E1

TCD-016-C1 is **not admitted** by this workunit. Its scientific blocker is narrowed from “is a continuation owner concept acceptable at all?” to “which physical phase/process laws and transition semantics are scientifically admissible?”

TCD-016-E1 remains blocked behind C1. Numerical threshold qualification must not choose a transition threshold before the physical/process transition contract exists.

The parent `TCD-016` therefore remains:

`UNRESOLVED_NOT_ADMITTED`

and remains a blocker to positive whole-B3 composition.

## 7. Next scientifically meaningful work

The next work should not be another source scan of the same `Transsub` branch. It should be one of:

1. recover authoritative ANIMO-specific dry-surface NH4 phase/remobilization theory;
2. define and qualify a **new ANIMO5 model-evolution process contract** around the already accepted conservation shell, explicitly acknowledging that it is new physics rather than corrected historical behavior;
3. acquire new historical runtime/design evidence that changes the phase or transition interpretation.

Any future model-evolution process contract must separately qualify dry hold, atmosphere exchange, soil exchange, rewetting/remobilization, restart equivalence, and a physical application envelope.

## 8. Governance conclusion

This is a GOV05 same-agent adversarial scientific review. It is not genuinely independent and does not claim the higher assurance of the earlier GOV04 separate-context model.

`TCD-016-C1_TOPOLOGY = MODEL_EVOLUTION_ACCEPTED_WITH_PROCESS_LAWS_UNQUALIFIED`

`TCD-016-C1_B3 = UNRESOLVED_NOT_ADMITTED`

`TCD-016-E1 = BLOCKED_DEPENDS_ON_C1_PROCESS_CONTRACT`

`TCD-016_PARENT = UNRESOLVED_NOT_ADMITTED`

`PRODUCTION = NOT_AUTHORIZED`
