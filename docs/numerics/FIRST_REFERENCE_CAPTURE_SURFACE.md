# ANIMO-NQ01 First Independent Reference Capture Surface

Status: `SOURCE_BOUND_CAPTURE_SURFACE_PREDEFINED_AWAITING_B2`.

## Purpose

NQ01 must decide before the first B2 run which scientific quantities are worth comparing. Waiting until a native executable exists would invite ad hoc variable selection after seeing the answer.

The machine-readable selection is:

`integration/animo-numerics/FIRST_REFERENCE_CAPTURE_SURFACE.json`

It is derived from the qualified PREP06 conserved-state and transfer-ledger registers observed on:

`work/animo-prep06-conserved-state-ledger`

at head:

`9b1f1ea51c24fb82823290193651830dc61ea3c8`.

PREP06 reports 53 state rows and 124 transfer rows and classifies that preparatory evidence as:

`QUALIFIED_CONSERVED_STATE_AND_TRANSFER_LEDGER_PREPARATORY_EVIDENCE`.

This NQ01 surface is therefore source-bound to named state and transfer identities rather than invented from report columns after B2 arrives.

## Important boundary

The registry is not a claim that every listed process is active in `RuurloGrass`.

For each surface the first native exercise must establish activation separately. A listed surface may be omitted only when inactivity is recorded from input options, source-bound branch evidence, unambiguous ordinary output, or an observer branch/call-context after observer non-interference has passed.

This avoids two opposite errors:

- forcing capture of processes that are absent from the case;
- silently dropping a process because it is difficult to observe.

## Core state trajectories

The first-reference surface includes, when active and observer-capable:

- matrix water state as hydrologic context;
- top NH4, NO3 and PO4 boundary reservoirs;
- aqueous and adsorbed NH4;
- aqueous NO3;
- aqueous, fast-sorbed, slow-sorbed and precipitated P;
- labile dissolved organic matter, N and P;
- stable dissolved organic matter, N and P;
- fresh organic matter, humus, exudate-derived humus and exudate storage;
- active crop N and P stores.

These are classified as `PHYSICAL_STORAGE_STATE` in NQ01 even when the legacy representation is concentration-based. The actual storage interpretation, units and spatial owner must follow PREP06, not the raw Fortran symbol alone.

The standard state checkpoints are:

- `INITIAL_STATE`;
- `PRE_PROCESS_STATE`;
- `POST_PROCESS_STATE`;
- `ACCEPTED_END_OF_STEP_STATE`;
- `FINAL_STATE`.

Not every routine needs every checkpoint. The point is that the selected trajectory cannot be reduced to one final value when process history matters.

## Core transfer trajectories

The registry preselects important internal and boundary transfers for N and P, including:

- vertical NH4, NO3 and PO4 transport;
- drainage and bottom exchange;
- crop N and P uptake;
- N and P mineralization and immobilization;
- nitrification and denitrification;
- fast and slow P sorption;
- P precipitation;
- initial P partition projection;
- event-conditional DOM and PO4 plough redistribution.

The transfer IDs are taken directly from the PREP06 transfer register. They must not be replaced by similarly named report terms without an explicit semantic mapping.

## Cumulative ledgers

NQ01 defines semantic ledger IDs for the main profile accounting surfaces:

- `PROFILE-NH4` mapped to legacy `Banh`;
- `PROFILE-NO3` mapped to legacy `Bani`;
- `PROFILE-INORGANIC-P` mapped to legacy `Bapp`;
- `PROFILE-ORGANIC-N` mapped to legacy `Bano`;
- `PROFILE-ORGANIC-P` mapped to legacy `Bapo`;
- `PROFILE-DOM-C` mapped to legacy `Bdom`.

These NQ01 ledger IDs are semantic comparison identifiers. They are not a claim that the legacy balance arrays themselves are canonical physical state. PREP06 explicitly warns against that interpretation.

Ledger comparison should retain:

- initial storage contribution;
- period accumulation;
- reset semantics;
- final cumulative balance;
- member identity, sign and index mapping where individual terms are compared.

A final residual alone is insufficient.

## Defect-sensitive numerical capture

Three known numerical or state-transition seams receive explicit diagnostic surfaces when activated.

### Nonlinear P sorption

Related findings:

- `TCD-014` initialization consistency;
- `TCD-019` nonlinear conservation policy;
- `TCD-024` slow-sorption site/index seam.

Capture should include, as applicable:

- nonlinear iteration index;
- constitutive branch;
- fallback path;
- nonlinear residual;
- accepted aqueous PO4;
- fast sorbed P;
- slow sorbed P;
- precipitated P.

Trial iterates are additional evidence only when needed to characterize solver path. They remain `TRIAL_STATE`, not accepted physical state.

### NO3 nonnegative constraint path

For `TCD-015`, capture branch activation, pre-constraint NO3, accepted NO3 and transport residual when the branch is exercised.

### NH4 surface dry-down path

For `TCD-016`, capture branch activation, surface water state, NH4 mass before and after the transition, and the transport residual when the path is exercised.

## Precision and oracle requirements

Every floating scientific surface requires the unrounded capture contract:

`docs/numerics/UNROUNDED_REFERENCE_CAPTURE_CONTRACT.md`.

A rounded legacy report may confirm event timing or coarse behaviour, but it cannot substitute for an unrounded oracle where scientific comparison depends on smaller differences.

No numerical tolerance is defined by this registry.

## Relationship to PREP02R

The first native case remains `RuurloGrass` only because that is still the live PREP02R preference. If PREP02R changes the preferred first case, the capture surface should be re-evaluated for activation coverage before execution. The source-bound semantic register remains reusable.

The first B2 exercise should therefore proceed in this order:

1. qualify B2 provenance sufficiently for execution;
2. characterize which registered processes are active in the frozen case;
3. preserve ordinary native output;
4. establish observer non-interference if unrounded capture is possible;
5. instantiate only the active, semantically justified records from the capture-surface registry;
6. run the structured comparator without tolerance;
7. disposition every non-exact scientific difference separately.

## Current boundary

This registry predefines comparison scope. It does not establish numerical equivalence.

Current NQ01 status remains:

`QUALIFIED_NUMERICAL_QUALIFICATION_ARCHITECTURE_AWAITING_INDEPENDENT_REFERENCE_DATA`.

Production migration remains:

`NOT_ADMITTED`.
