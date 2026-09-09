# ANIMO-ARCH01 typed transfer contract

Status: `CANDIDATE_ARCHITECTURE_DESIGN_NOT_RUNTIME_API`.

PREP06 showed that physical state, process transfers and reporting accumulators must be separated. This document defines the candidate semantic contract for doing that in ANIMO5. The corresponding transfer-type registry is `integration/animo-architecture/ARCH01_TRANSFER_TYPES.csv`.

## Event model

A physical transfer is represented once as a directed event from a source compartment to a sink compartment. The event amount is non-negative. Direction carries the sign semantics.

A future runtime event needs, at minimum:

- `event_id`: unique within a trial transaction;
- `process_id`: process or boundary route that produced the event;
- `conserved_quantity`: for example water, nitrogen, phosphorus, organic-matter mass, CH4-C or N2O-N;
- `source_compartment`;
- `sink_compartment`;
- `source_species`;
- `sink_species`;
- `amount` and unit;
- `t0`, `t1` or equivalent step interval;
- `control_volume_scope` or enough compartment identity to derive it;
- optional site/layer/domain coordinates;
- evidence/diagnostic tags where qualification requires them.

`EXT:*` compartment identifiers denote a boundary outside the chosen physical system. A management application is not itself a state; its retained material becomes one or more typed transfer legs into physical stores.

## Conserved quantity is not the same as species

This distinction is mandatory.

Nitrification can transform NH4-N into NO3-N and N2O-N while the conserved quantity remains nitrogen. Sorption can move phosphorus between aqueous and sorbed carriers. Organic transformations can move N or P between organic and mineral pools.

A single event may not silently move one conserved quantity into another merely because two legacy variables have similar names. Cross-quantity conversion requires an explicit conversion contract. This rule is the architecture response to the defect pattern demonstrated by TCD-023.

For carbon, ARCH01 intentionally distinguishes `organic_matter_mass` from elemental-C quantities. The revision-53 OM/GHG reconciliation is not sufficiently qualified to infer one global conversion automatically.

## Reaction bundles

A process with multiple products is represented as a bundle of typed legs linked by one reaction/process instance. For a conserved quantity `Q`:

`sum(source legs in Q) = sum(internal sink legs in Q) + sum(external sink legs in Q)`

subject only to an explicitly qualified residual policy.

Examples include nitrification, denitrification and organic-matter transformation. The bundle model avoids forcing a one-source/one-sink abstraction onto real partitioning while retaining exact conservation accounting.

## Control-volume views

Internal versus external classification is a view, not a property that must be hard-coded separately into every process.

Crop N uptake is:

- external to a soil-only control volume;
- internal to a combined soil+crop control volume.

Matrix-to-macropore exchange is internal to a combined matrix+macropore profile but crosses the boundary of either subdomain considered alone.

A canonical ledger should derive these views from the same event and compartment topology rather than ask process routines to write different balance arrays.

## Transfer classes

The machine registry defines twelve semantic classes:

- internal state transfer;
- external boundary input;
- external boundary output;
- management addition;
- management removal;
- phase transfer;
- reaction partition;
- soil/crop transfer;
- matrix/macropore transfer;
- initialization projection;
- numerical-constraint diagnostic event;
- reporting observation.

The last two require care. A numerical constraint is not automatically a physical flux, and an observation is never a physical transfer.

## Initialization

Initialization projection is a separate transaction before the first accepted runtime state. If a representation is projected among solution, sorbed or precipitated stores, the total conserved quantity must remain invariant unless an explicit external adjustment is part of the qualified initialization contract.

TCD-014 prevents treating the existing revision-53 P initialization policy as already admitted. ARCH01 only specifies the conservation requirement.

## Numerical constraints

Clipping or state-domain enforcement must not be disguised as a transfer event. If a constraint changes conserved mass, one of the following must be true before production admission:

1. the removed/added amount is represented by a physically justified source or sink state;
2. an external boundary flux is explicitly generated and scientifically qualified;
3. the state representation is extended so mass remains representable.

Otherwise the occurrence is diagnostic nonclosure. TCD-015 and TCD-016 motivate this separation.

## Reporting observers

Mass-balance and detailed-process reports consume state snapshots and the transfer journal. They do not own physical mass and do not write independent transfer totals that later feed physics.

Beginning and end storage are generated from the same state registry. Internal transfer totals are generated from the same event journal. This eliminates an entire class of bookkeeping asymmetries exemplified by TCD-017, TCD-018, TCD-026, TCD-027 and TCD-028.

## Trial semantics

All physical events belong to a trial transaction. On reject, the trial state and event journal are both discarded. On commit, both are atomically admitted. A report may observe either a trial or committed journal only under an explicit diagnostic policy; a report can never cause commit.

## Qualification boundary

This is a semantic design contract, not a runtime API or production data structure. Units, enumeration names, concrete layout, precision, reaction coefficients and tolerance policies remain subject to later admitted design and qualification. TCD-025, TCD-029, GHG theory gaps and PREP02 reference qualification remain blockers where applicable.
