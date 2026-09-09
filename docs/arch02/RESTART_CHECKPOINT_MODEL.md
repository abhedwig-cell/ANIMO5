# ANIMO-ARCH02 restart and checkpoint model

Status: `CANDIDATE_ARCHITECTURE_DESIGN_ONLY`.

ARCH02 derives restart semantics from ARCH01 ownership, not from legacy file formats. It therefore distinguishes ownership, continuation sufficiency and reporting continuity explicitly.

## Core rule: checkpoint only accepted state

A portable ANIMO5 checkpoint is created only at an accepted transaction boundary. The checkpoint contains the last committed model state, the exact model/configuration identity needed to interpret that state, and the continuation metadata required to construct the next trial.

The following are explicitly excluded from a physical checkpoint:

- trial/result state that has not been committed;
- uncommitted transfer-journal events;
- step-local rates and scratch;
- derived averages and aggregate views;
- balance/report observers as physical state.

This preserves the ARCH01 invariant that rejected trials cannot mutate committed state. It also avoids defining partial-trial serialization semantics before the TIME gate exists.

## Three restart ownership classes

### 1. ANIMO-owned physical continuation state

Physical ANIMO stores are serialized in their canonical owner representation. This includes the surface/addition reservoir, organic matter, dissolved organic matter, mineral N and mineral P. Site-resolved P state is stored site-resolved, not only through derived totals.

Conditional ANIMO state is included only when the corresponding feature is admitted and active. This applies to GHG and macropore state. The checkpoint manifest must record feature activation so inactive layouts are not silently interpreted as active ones.

### 2. Externally owned coordinated state

Hydrological storage coordinates required by nutrient transport are explicit in ARCH01 but are not duplicated as ANIMO-owned checkpoint fields. A coupled restart must restore them from the hydrology owner and prove that the external state refers to the same accepted model time and spatial discretization.

This is stricter than simply omitting water from ANIMO. ANIMO declares the dependency, expected identity and synchronization point, while ownership remains external.

Crop state is ownership-mode dependent. Where ANIMO owns the crop compartment it belongs in the ANIMO checkpoint. Where WOFOST or another crop owner is authoritative, the coupled checkpoint must restore crop state from that owner and bind it to the same accepted time. The mode must be explicit in the checkpoint manifest.

### 3. Recomputed state

Derived state is reconstructed after restore from canonical owners. This includes:

- aggregate surface-water views;
- potential crop demand/reference state when it is derivable from restored owner state and forcing/configuration;
- GHG aqueous phase views derived from system state;
- fast/slow P site totals;
- average concentrations;
- process rates and scratch.

Recomputed fields must not be serialized merely because the legacy source persisted similarly named arrays. Persisting both owner and derived copies would create a restart consistency problem.

## Diagnostic continuation is separate

Mass-balance and detailed process accumulators are not physical state, but they can still be continuation-critical for output equivalence when a restart occurs inside a reporting period. ARCH02 therefore defines a second payload class: `DiagnosticContinuationState`.

A minimal physical checkpoint can omit it. A restart promising identical cumulative reports across a mid-period boundary must either serialize the diagnostic accumulators or constrain checkpoints to reporting-period boundaries where those accumulators are reset. See `DIAGNOSTIC_CONTINUATION_MODEL.md`.

## Required checkpoint manifest

A candidate checkpoint manifest contains at least:

- checkpoint schema version;
- exact model build/evidence identity;
- accepted model time and time-unit/calendar contract once TIME is qualified;
- spatial discretization identity;
- active feature set;
- crop ownership mode;
- external hydrology owner identity and synchronization token when coupled;
- serialized ANIMO state component versions;
- diagnostic continuation policy;
- integrity hash for payload and manifest.

The exact binary format is deliberately not selected here.

## Restore protocol

Candidate restore order:

1. validate checkpoint and configuration identity;
2. restore ANIMO-owned accepted state;
3. bind externally owned hydrology/crop state for the exact same accepted time where applicable;
4. restore diagnostic continuation state when required;
5. reconstruct all derived views;
6. initialize fresh trial scratch and an empty trial transfer journal;
7. run structural and conservation sanity checks before allowing the next trial.

A restore must fail closed if external owner time, layer geometry, site counts, active-feature layout or quantity dimensions do not match.

## Known evidence constraints

TCD-026 reinforces that physical state membership cannot be inferred from legacy beginning-balance coverage. TCD-025 means macropore state cannot be admitted only because restartable arrays exist. TCD-029 means site-resolved fast-P state and constitutive configuration must remain aligned. TCD-008 leaves the GHG state-to-ledger contract open.

## Qualification boundary

This is a candidate continuation architecture. It has not demonstrated behavioural restart equivalence of revision 53 and does not satisfy the migration DAG's canonical STATE or TIME gates.
