# ANIMO-ARCH03 candidate MassLedger model

Status: `CANDIDATE_ARCHITECTURE_DESIGN_NOT_CANONICAL_MASS_GATE`.

ARCH03 turns PREP06 conservation identities into one observer model over ARCH01 typed transfer events and ARCH01/ARCH02 state ownership. It is deliberately observer-only: it does not own physical mass, mutate model state, choose a timestep, accept a trial, or define a numerical closure tolerance.

## 1. One ledger, many views

The runtime should not maintain a separate hand-written balance implementation for every report. A single event journal and state registry must support multiple control-volume views.

For one conserved quantity `Q` and one selected control volume:

`R_Q = S_end(Q) - S_begin(Q) - I_external(Q) + O_external(Q)`

where:

- `S_begin` is derived from the accepted beginning state;
- `S_end` is derived from the committed end state, or from an explicitly requested trial snapshot for diagnostics;
- `I_external` is the sum of typed events whose source is outside and sink is inside;
- `O_external` is the sum of typed events whose source is inside and sink is outside.

Events with both endpoints inside are internal and cancel from the profile-level residual. Events with both endpoints outside are irrelevant to that control volume.

The equation is semantic. ARCH03 does not define a floating-point tolerance or numerical pass/fail threshold.

## 2. Storage is generated from owner state

Beginning and end storage are generated from canonical owner fields, not copied from `Bawa`, `Bfom`, `Bano`, `Bapo` or other reporting accumulators.

This directly addresses the failure classes already established in PREP06:

- TCD-018: a real interception-water store is absent from the public water ledger;
- TCD-026: a real exudate OM store is omitted from beginning storage;
- TCD-017: physical P redistribution is conservative while a report omits one leg;
- TCD-027 and TCD-028: detailed reporting accumulators can be wrong or duplicated without changing physical state.

A storage observer therefore needs a state-to-quantity projection, not a legacy balance-array mapping.

## 3. Transfer events are consumed once

Each admitted physical transfer is emitted once by the process/transfer layer and consumed once by the ledger observer. The observer derives its role from endpoint membership.

This eliminates the need for process routines to independently maintain:

- source loss arrays;
- sink gain arrays;
- profile balance arrays;
- detailed process-report arrays;
- soil-only and soil+crop variants of the same physical event.

A reporting view may aggregate events by process, layer, species or boundary, but aggregation never creates a second physical event.

## 4. Conserved quantity and species remain separate

The ledger groups closure by `conserved_quantity`, not by variable-name similarity.

Examples:

- NH4-N to NO3-N is a nitrogen transfer;
- PO4-P aqueous to sorbed P is a phosphorus phase transfer;
- crop uptake can move N from soil mineral state into plant N state;
- stable-DOM P transformations remain phosphorus even if carrier/species changes.

TCD-023 shows why this separation is mandatory: a P reaction cannot silently consume an N transfer amount.

ARCH03 also preserves the existing qualification boundary between organic-matter mass and elemental carbon. `organic_matter_mass`, `crop_dry_matter`, and `carbon_as_CH4_C` are separate quantity contracts until an explicit and scientifically qualified conversion/reaction contract exists.

## 5. Reaction bundles

A reaction with multiple outputs is represented by a bundle of typed legs sharing one process instance and conserved quantity.

For one quantity `Q`:

`bundle_nonclosure = sum(source legs) - sum(internal sink legs) - sum(external sink legs)`

A bundle observer exposes this quantity separately from the interval-level residual.

This is useful for:

- nitrification;
- denitrification;
- organic-pool transformations;
- mineralization/immobilization;
- stable-DOM transformations;
- GHG-linked partitions when later qualified.

A nonzero reaction-bundle residual is not repaired by the observer. It is diagnostic evidence against the producer contract.

## 6. Numerical constraints are diagnostics, not physical fluxes

`TT-CONSTRAINT` events such as negative-concentration clipping or dry-down loss are kept outside normal physical transfer totals unless a later qualified design assigns the changed mass to a real alternate state or explicit boundary flux.

The ledger therefore exposes `constraint_nonclosure` alongside the physical closure residual.

This prevents numerical clipping from being made invisible by inventing a balancing flux after the fact. TCD-015 and TCD-016 are the relevant precedent.

## 7. Initialization is separate

Initialization projection is evaluated before the first accepted runtime state.

For purely representational partitioning:

`initialization_nonclosure = total_after - total_before`

and should be semantically zero.

TCD-014 shows that initial P partitioning requires its own qualification and must not be hidden inside the first runtime interval ledger.

## 8. Trial and commit semantics

The canonical operational ledger observes committed intervals only.

A diagnostic trial ledger may be generated from:

- accepted beginning state;
- trial result state;
- trial event journal.

When a trial is rejected, both trial state and its trial ledger are discarded. A diagnostic observer may retain explicitly labeled evidence outside the physical model state, but this cannot alter later committed closure.

ARCH03 does not define the generic acceptance policy itself. That belongs to the later TIME gate.

## 9. Diagnostic continuation

Physical MassLedger reconstruction for a committed interval requires owner snapshots plus the exact committed event journal. Long-period cumulative reports may additionally need diagnostic continuation state across checkpoints.

That continuation state belongs to diagnostics, not to the physical checkpoint. ARCH02 already separates these concerns.

## 10. Fail-closed compatibility

A ledger comparison or restart continuation must fail closed when any of the following differs without an explicit migration contract:

- ledger schema;
- conserved-quantity registry;
- state-owner schema;
- geometry/layer topology;
- P site counts;
- feature activation layout;
- crop ownership mode;
- macropore admission mode;
- GHG admission mode;
- unit contract;
- event-journal schema.

## 11. Qualification boundary

ARCH03 provides a candidate architecture only. It does not establish that revision 53 is behaviourally reference-qualified, does not repair any TCD, and does not admit the repository's canonical MASS gate.
