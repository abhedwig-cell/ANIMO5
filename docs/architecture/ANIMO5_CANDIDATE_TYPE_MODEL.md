# ANIMO5 Candidate Type Model

Work unit: `ANIMO-ARCHG01`

Status: `CANDIDATE_TYPE_MODEL_NOT_PRODUCTION_API`

This type model reconciles ARCH01-ARCH07. Names are semantic contracts, not committed language-level structs, classes, Fortran derived types, ABI layouts, or storage precision.

## Common rules

- Every physical store has one runtime owner.
- Configuration is immutable for a bound trial.
- Physical units are explicit. No field is interpreted from name or position alone.
- Candidate state fields inherit quantity and unit semantics from PREP06 and later admitted process contracts.
- ARCHG01 does not choose canonical floating precision or numeric tolerance.
- Serialization is schema- and identity-aware. No silent resize, zero fill, truncation, unit guessing, or ownership conversion.
- Optional physical state exists only for an active and scientifically admitted feature.
- Diagnostics, derived views, journals, and scratch are not physical state owners.

## `ModelConfiguration`

**Owner:** model instance / configuration builder.

**Mutability:** immutable after normalization and trial binding. A new configuration produces a new identity.

**Lifetime:** model-instance lifetime, with explicit replacement only at an accepted boundary under a future qualified transition contract.

**Units:** configuration fields are typed metadata. Geometry and parameter references carry their own unit/schema contracts. No scientific value receives an implicit unit.

**Serialization:** canonical normalized manifest with deterministic field ordering and domain-separated identities. Required fields are explicit; inactive conditional fields are explicit `null`.

**Validation:** reject unknown fields, hidden scientific defaults, impossible feature combinations, duplicate crop ownership, incompatible hydrology mode, missing feature admission identity, invalid P-site cardinality, unsupported dormant surface stable DOM, and incompatible schema/policy references.

**Legacy relationship:** target of `LegacyInputAdapter`. It is not equivalent to GENERAL.INP, SOIL.INP, CHEMPAR.INP, PLANT.INP, BOUNDARY.INP, MANAGEMENT.INP, SWATRE/WATBAL inputs, or parser globals.

## `ModelState`

**Owner:** ANIMO model instance for ANIMO-owned physical components.

**Mutability:** no direct mutation through the root object. Mutation occurs only through `TrialState`.

**Lifetime:** continuation state across accepted timesteps.

**Units:** component fields use explicit physical unit IDs. Typical source concepts include areic mass, concentration, water coordinate and site-resolved store quantities, but ARCHG01 does not freeze one numeric representation.

**Serialization:** only through `RestartSnapshot`, and only for ANIMO-owned continuation-critical components.

**Validation:** every PREP06 continuation-critical physical family maps to exactly one component owner or an explicit external-owner coordinate. Derived, scratch, diagnostic and unsupported dormant families are excluded.

**Legacy relationship:** logical aggregate of `SurfaceReservoirState`, `OrganicMatterState`, `DissolvedOrganicState`, `MineralNitrogenState`, `MineralPhosphorusState`, optional ANIMO-owned `CropState`, and later-admitted optional state groups. It is explicitly not a replacement mega-argument object.

## `AcceptedState`

**Owner:** ANIMO transaction lifecycle.

**Mutability:** immutable.

**Lifetime:** from one successful commit until the next successful commit.

**Units:** identical to the contained `ModelState`.

**Serialization:** eligible for physical checkpoint at an accepted boundary.

**Validation:** bound to exact configuration identity, physical-layout identity, accepted generation, geometry, feature topology and state-schema versions.

**Legacy relationship:** replaces implicit "start/old" global-array semantics with an explicit accepted snapshot.

## `TrialState`

**Owner:** one trial transaction.

**Mutability:** mutable within the trial only.

**Lifetime:** begin-trial to accept or reject.

**Units:** identical to the corresponding `ModelState` fields.

**Serialization:** not part of a normal portable restart payload.

**Validation:** created from exactly one `AcceptedState` plus an immutable `StepContext`; cannot outlive or cross-bind to another trial identity.

**Legacy relationship:** replaces implicit "result/new" arrays and partial process mutation. A process cannot commit its own partial state.

## `StepContext`

**Owner:** transaction orchestrator.

**Mutability:** immutable after trial binding.

**Lifetime:** one proposed interval / trial.

**Units:** interval endpoints and forcing values carry explicit time and physical unit contracts. Exact calendar/time semantics remain TS01-open.

**Serialization:** may be persisted in diagnostic or replay evidence, but is not physical state.

**Validation:** exact configuration identity, accepted generation, trial ID, interval identity, forcing bindings and external-frame identities must agree.

**Legacy relationship:** gathers timestep, forcing, management and exchange context that legacy routines obtain through long argument lists, files, and global arrays. It does not define process order.

## `TransferEvent`

**Owner:** trial transfer journal; produced by process/boundary logic and observed by ledgers.

**Mutability:** append-only record after creation.

**Lifetime:** one trial. On accept it becomes part of the committed interval journal; on reject it is discarded physically.

**Units:** `amount` has an explicit unit compatible with `conserved_quantity`. Direction is encoded by source/sink endpoints, so amount is non-negative.

**Minimum semantic fields:** event ID, process ID, conserved quantity, source compartment, sink compartment, source species/carrier, sink species/carrier, amount, unit ID, interval/trial identity, optional layer/site/domain coordinates, optional reaction-bundle ID, and evidence tags.

**Serialization:** committed journals may be persisted for replay/qualification/diagnostics. Serialization must preserve quantity, unit, endpoint and indexing identity.

**Validation:** no negative amount; quantity/unit must match registry; source/sink required; cross-quantity conversion forbidden without explicit conversion contract; reporting observations and numerical constraint diagnostics cannot masquerade as physical events.

**Legacy relationship:** replaces parallel balance-array and detailed-accumulator booking as the physical transfer truth.

## `ExternalExchange`

**Owner:** external producer plus coupling orchestrator for frame identity; ANIMO owns only its immutable consumer view.

**Mutability:** immutable under one frame identity.

**Lifetime:** one accepted generation and one bound interval/trial, unless a static contract object is explicitly separated.

**Units:** every exchange field has explicit unit and shape metadata. Producer-specific signs are normalized at the adapter boundary.

**Serialization:** frame evidence may be persisted with producer, schema, generation, interval, geometry, feature-layout and precision-policy identity.

**Validation:** reject stale generation, wrong interval, schema mismatch, unit mismatch, geometry mismatch, layout mismatch, unsupported feature, silent field defaulting, or frame mutation under an existing identity.

**Legacy relationship:** replaces direct reading of SWAP/WATBAL/crop internals as mutable state. Legacy names are evidence for required information, not future API names.

**Relation to `TransferEvent`:** not the same type. External state coordinates remain observations. Validated interval-integrated physical transfers are normalized exactly once into `TransferEvent` records.

## `MassLedger`

**Owner:** diagnostic observer layer.

**Mutability:** immutable result for one chosen quantity/control-volume view after construction.

**Lifetime:** interval result or accumulated diagnostic report.

**Units:** storage and transfer terms use the conserved quantity's explicit ledger unit. No implicit unit conversion.

**Serialization:** optional diagnostic evidence. Not physical checkpoint state.

**Validation:** beginning and end storage come from the same state-projection registry; external transfer classification is derived from endpoint membership; internal events cancel in whole-control-volume residual; observations/constraint diagnostics are excluded from physical event totals.

**Legacy relationship:** replaces BAWA/BAN/BAP/BAOM and detailed hand-maintained ledgers as physical accounting authority. Legacy reports remain comparison/diagnostic outputs, not owners.

**State source rule:** ANIMO-only ledgers use ANIMO canonical owner state. Wider ledgers use an ownership-aware canonical state view with immutable external-owner observations, without copying ownership into `ModelState`.

## `RestartSnapshot`

**Owner:** checkpoint subsystem.

**Mutability:** immutable once created.

**Lifetime:** persisted accepted-boundary continuation artifact.

**Units:** payload preserves state-field unit identities; time identity is explicit but final time/calendar contract remains TS01-open.

**Serialization:** contains checkpoint schema/version, accepted ANIMO-owned state, configuration and physical-layout identities, accepted time/generation identity, geometry, component schema versions, external-owner synchronization references, integrity hash, and an explicit diagnostic-continuation policy.

**Validation:** exact compatibility required for direct restore. Foreign hydrology/crop state is not embedded as ANIMO-owned payload.

**Legacy relationship:** not defined by INITIAL.OUT alone. Legacy restart files are evidence for continuation fields, not the modern checkpoint contract.

## `DiagnosticsView`

**Owner:** observer/diagnostic subsystem.

**Mutability:** generated read-only view, except diagnostic continuation counters that are isolated from physical state.

**Lifetime:** snapshot, interval, report period, or explicitly configured diagnostic continuation period.

**Units:** explicit per observed field.

**Serialization:** optional. If report-equivalent continuation across a mid-report-period restart is promised, required observer continuation state is serialized separately from physical state.

**Validation:** cannot mutate physical state, create physical transfers, decide trial acceptance, or change `physical_layout_id`.

**Legacy relationship:** absorbs state outputs, detailed transformation reports, balance outputs, branch/fallback traces, and qualification capture without making those outputs state owners.

## `LegacyInputAdapter`

**Owner:** ingestion/integration layer, outside the scientific process kernel.

**Mutability:** stateless where practical. Any parse context is short-lived and must not become model physical state.

**Lifetime:** input ingestion / normalization.

**Units:** converts only through explicit qualified mappings. Unknown or ambiguous units fail closed.

**Serialization:** emits normalized configuration plus provenance record: B0 member/hash, parser/adapter version, compatibility transformations, warnings/errors, unsupported-option dispositions, and resulting configuration identity.

**Validation:** no hidden defaults after normalization; no unsupported option activation; no parser-visible non-operational feature promotion; no scientific admission by parser logic; no silent correction of testcase or source bytes.

**Legacy relationship:** interprets legacy ANIMO steering/input files and produces the modern normalized static contract. PREP03 governs version/parser mismatches. ARCH06 governs normalized identity. ARCH07 provides the model for future adapter qualification evidence.

## Deliberate non-type: `CanonicalStateView`

For ledger and diagnostic construction ARCHG01 uses the term `CanonicalStateView` as a read-only composition of authoritative state from multiple owners. It is not a new physical owner and is not required to be serialized as one object.

Examples:

- soil-only ledger: ANIMO `AcceptedState`;
- soil-plus-ANIMO-crop ledger: ANIMO `AcceptedState` including ANIMO-owned `CropState`;
- soil-plus-external-crop ledger: ANIMO `AcceptedState` plus immutable accepted external crop observations;
- matrix-plus-macropore ledger: one admitted ANIMO state containing both matrix and macropore stores.

This avoids duplicating foreign state merely to make ledger code convenient.

## Production boundary

These semantic types may be used to design implementation interfaces and tests. Concrete language types, memory layout, precision, process schedule, timestep controller, binary checkpoint format, unit-conversion implementation, and production adapters remain unadmitted.
