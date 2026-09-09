# ANIMO5 Candidate Type Model

Work unit: `ANIMO-ARCHG01`

Status: `CANDIDATE_TYPE_MODEL_POST_TS01_REVALIDATED_NOT_PRODUCTION_API`

This type model reconciles ARCH01 through ARCH07 and incorporates qualified source-bound TS01 temporal constraints. Names are semantic contracts, not committed language-level structs, classes, Fortran derived types, ABI layouts, storage precision, or a canonical TIME controller.

## Common rules

- Every continuation-critical physical store has one runtime owner.
- Configuration is immutable for a bound trial.
- Physical units are explicit.
- Optional physical state exists only for an active and scientifically admitted feature.
- Diagnostics, derived views, journals and scratch are not physical state owners.
- Process reads must declare their state generation where temporal meaning matters.
- Source-observed event boundaries and order are preserved unless a later qualification admits a difference.
- ARCHG01 defines no numerical tolerance, precision or convergence policy.
- Serialization is schema- and identity-aware. No silent resize, zero fill, truncation, unit guessing or ownership conversion is allowed.

## `ModelConfiguration`

**Owner:** model instance / configuration builder.

**Mutability:** immutable after normalization and trial binding.

**Lifetime:** model-instance lifetime, with replacement only through an explicit accepted-boundary transition contract.

**Units:** configuration values and references carry explicit unit/schema semantics.

**Serialization:** canonical normalized manifest with deterministic fields and domain-separated identities.

**Validation:** reject unknown fields, hidden scientific defaults, impossible feature combinations, duplicate crop ownership, incompatible hydrology mode, missing feature admission identity, invalid P-site cardinality, unsupported dormant surface stable DOM, and incompatible schema or policy references.

**Legacy relationship:** target of `LegacyInputAdapter`; not equivalent to any one legacy input file or parser-global representation.

## `ModelState`

**Owner:** ANIMO model instance for ANIMO-owned physical components.

**Mutability:** no direct mutation through the aggregate root; physical mutation occurs through `TrialState`.

**Lifetime:** continuation state across accepted intervals.

**Units:** explicit per component/state family.

**Serialization:** only through `RestartSnapshot`, and only for ANIMO-owned continuation-critical components.

**Validation:** every PREP06 continuation-critical physical family maps to exactly one component owner or explicit external-owner coordinate. Derived, scratch, diagnostic and unsupported dormant families are excluded.

**Legacy relationship:** logical aggregate of physical owner components only. It is explicitly not a replacement mega-state for long legacy argument lists.

## `AcceptedState`

**Owner:** ANIMO transaction lifecycle.

**Mutability:** immutable.

**Lifetime:** one logical accepted generation until the next successful commit.

**Units:** identical to the contained `ModelState`.

**Serialization:** eligible for physical checkpoint at an accepted boundary.

**Validation:** bound to configuration identity, physical-layout identity, accepted generation, geometry, feature topology and state-schema versions.

**Legacy relationship:** modern abstraction of the authoritative beginning/end continuation generation. TS01 shows that legacy has meaningful current/start versus result/end generations, but no literal atomic end-step commit. Behavioural equivalence of the modern commit remains a TIME/reference qualification question.

## `TrialState`

**Owner:** one trial transaction.

**Mutability:** mutable within that trial only.

**Lifetime:** begin-trial to accept or reject.

**Units:** identical to corresponding `ModelState` fields.

**Serialization:** excluded from normal portable restart payload.

**Validation:** created from exactly one `AcceptedState` plus one immutable `StepContext`; cannot cross-bind to another trial identity.

**Legacy relationship:** represents current-interval working state and final candidate result without exposing legacy distributed partial commits as the modern contract. TS01 requires same-step management/residue mutation to become visible to downstream readers in the source-defined order.

## `StepContext`

**Owner:** transaction orchestrator.

**Mutability:** immutable after trial binding.

**Lifetime:** one proposed interval / trial.

**Units:** interval endpoints, forcing values and exchange fields carry explicit time and physical unit contracts.

**Serialization:** may be persisted in replay/qualification evidence, but is not physical state.

**Validation:** configuration identity, accepted generation, trial ID, interval identity, forcing bindings, external-frame identities and event/schedule bindings must agree.

**Temporal contract after TS01:**

- preserve event-class-specific endpoint semantics rather than one universal convention;
- preserve same-row ordering where source-observed;
- expose enough provenance for process seams to distinguish accepted, post-event trial, provisional, actual, previous-step-neighbour and same-step-upstream reads;
- bind but not invent a canonical retry/reject policy;
- do not authorize layer reordering or topology transition.

**Legacy relationship:** gathers interval, forcing, management and exchange context that legacy obtains through long argument lists, file cursors and globals. It does not itself implement the process scheduler.

## `TransferEvent`

**Owner:** trial transfer journal; produced by process/boundary logic and observed by ledgers.

**Mutability:** append-only after creation.

**Lifetime:** one trial; discarded physically on reject and retained as committed interval evidence on accept.

**Units:** amount has an explicit unit compatible with conserved quantity. Direction is encoded by source/sink endpoints and amount is non-negative.

**Minimum semantics:** event ID, process ID, conserved quantity, source/sink compartment, source/sink species/carrier, amount, unit ID, interval/trial identity, optional coordinates, optional reaction-bundle ID and evidence tags.

**Validation:** no negative amount, compatible quantity/unit, required endpoints, no cross-quantity conversion without explicit conversion contract, and no reporting observation or numerical constraint masquerading as physical transfer.

**TS01 refinement:** potential-pass values do not become committed physical events merely because legacy provisional routines write result-shaped arrays. Crop uptake is one physical soil-to-crop transfer, with soil loss and crop gain as two state effects of that same transfer.

## `ExternalExchange`

**Owner:** external producer plus coupling orchestrator for frame identity; ANIMO owns only an immutable consumer view.

**Mutability:** immutable under one frame identity.

**Lifetime:** one accepted generation and bound interval/trial, unless a static contract is explicitly separated.

**Units:** every exchange field has explicit unit and shape metadata. Producer-specific signs are normalized at the adapter boundary.

**Serialization:** optional exchange evidence with producer, schema, generation, interval, geometry, feature-layout and precision-policy identity.

**Validation:** reject stale generation, wrong interval, schema/unit/geometry/layout mismatch, unsupported feature, silent defaulting or frame mutation under an existing identity.

**Relation to `TransferEvent`:** not the same type. State coordinates remain observations. Validated interval-integrated physical transfers normalize exactly once into `TransferEvent` records.

**TS01 refinement:** hydrology-time alignment must become explicit adapter validation rather than an implicit sequential-file assumption.

## `MassLedger`

**Owner:** diagnostic observer layer.

**Mutability:** immutable result for one quantity/control-volume view after construction.

**Lifetime:** interval result or accumulated diagnostic report.

**Units:** storage and transfer terms use explicit conserved-quantity ledger units.

**Serialization:** optional diagnostic evidence; never physical checkpoint state.

**Validation:** beginning/end storage from one projection registry; external classification from endpoint membership; internal events cancel for enclosing volumes; observations/constraint diagnostics/provisional passes are excluded from physical totals.

**Legacy relationship:** replaces distributed physical balance booking as modern accounting authority while retaining legacy reports as comparison/diagnostic evidence only.

**State source rule:** wider control volumes use an ownership-aware `CanonicalStateView` with immutable external-owner observations rather than copying foreign state into `ModelState`.

## `RestartSnapshot`

**Owner:** checkpoint subsystem.

**Mutability:** immutable once created and read-only with respect to accepted physical state.

**Lifetime:** persisted accepted-boundary continuation artifact.

**Units:** payload preserves state-field units and explicit time/generation identity.

**Serialization:** contains checkpoint schema/version, accepted ANIMO-owned state, configuration and layout identities, accepted time/generation, geometry, component schema versions, external-owner synchronization references, integrity hash and explicit diagnostic-continuation policy.

**Validation:** exact compatibility required for direct restore. Foreign hydrology/crop state is not embedded as ANIMO-owned payload.

**Legacy relationship after TS01:** `INITIAL.OUT` is historical restart-style evidence, not the canonical checkpoint contract. It omits continuation context and `Output_Init` contains a phosphorus clamp side effect. Any legacy restart compatibility transformation must therefore be explicit and separately qualified.

## `DiagnosticsView`

**Owner:** observer/diagnostic subsystem.

**Mutability:** generated read-only view, except isolated diagnostic continuation counters.

**Lifetime:** snapshot, interval, report period or explicitly configured diagnostic continuation period.

**Serialization:** optional. Report-equivalent continuation may require separate observer continuation state.

**Validation:** cannot mutate physical state, create physical transfers, decide trial acceptance or change physical layout.

**TS01 refinement:** report accumulation/reset occurs after physical interval calculation and is not a physical commit.

## `LegacyInputAdapter`

**Owner:** ingestion/integration layer outside the scientific process kernel.

**Mutability:** stateless where practical; parse context is short-lived and not physical state.

**Lifetime:** input ingestion and normalization.

**Units:** converts only through explicit qualified mappings; ambiguous units fail closed.

**Serialization:** emits normalized configuration plus provenance including B0 member/hash, adapter version, transformations, warnings/errors, unsupported dispositions and resulting configuration identity.

**Validation:** no hidden defaults after normalization, unsupported option activation, parser-visible non-operational feature promotion, scientific admission by parser logic, or silent correction of testcase/source bytes.

**TS01 refinement:** legacy scheduling/event fields may be normalized only while retaining their qualified endpoint and ordering semantics.

## Deliberate non-type: `CanonicalStateView`

`CanonicalStateView` is a read-only composition of authoritative state from multiple owners for ledgers and diagnostics. It is not a physical owner and is not serialized as a mega-state.

Examples include ANIMO soil-only state, ANIMO soil plus ANIMO-owned crop, or ANIMO state plus immutable accepted external-crop observations.

## Production boundary

These semantic types may guide future implementation interfaces and tests. Concrete language types, memory layout, precision, process scheduler, canonical TIME representation, retry/reject controller, binary checkpoint format, unit-conversion implementation and production adapters remain unadmitted.
