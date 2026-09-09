# ANIMO-ARCH04 feature-layout compatibility

Status: `CANDIDATE_ARCHITECTURE_DESIGN`.

ARCH04 defines a logical feature-layout manifest so checkpoint restore, coupled state exchange and batched execution can reject incompatible state topology before any state bytes are consumed.

## Two layout identities

The candidate separates:

- `physical_layout_id`: identity of physical/externally coordinated state topology, owner modes and state dimensions;
- `observer_layout_id`: identity of diagnostic observer allocation and continuation schema.

Changing diagnostics alone must not alter `physical_layout_id`.

This separation prevents output configuration from becoming a hidden part of physical model state.

## Physical compatibility fields

At minimum the physical identity is a deterministic function of:

- state schema identity;
- normalized feature set;
- hydrology mode and hydrology exchange schema;
- layer/domain geometry identity;
- surface-reservoir activation;
- stable-DOM activation;
- crop ownership mode and matching crop schema/exchange schema;
- GHG activation plus admission/schema identity when active;
- macropore activation plus admission/schema identity when active;
- fast and slow P site counts;
- organic-fraction count;
- precision-policy reference.

ARCH04 does not define the precision policy. It only requires the eventual selected policy to participate in compatibility when it changes representation or restart equivalence.

## Restore rule

A physical checkpoint may be restored only if its `physical_layout_id` exactly matches the target model configuration, unless a separately qualified state migration procedure exists.

No implicit resizing, truncation, zero-filling or site-count conversion is allowed.

Examples of fail-closed mismatches include:

- different layer geometry even when layer counts happen to match;
- different fast or slow P site counts;
- ANIMO-owned crop checkpoint restored into external-crop ownership mode;
- checkpoint with GHG state restored into a configuration where GHG is not admitted;
- macropore checkpoint restored into an aggregated hydrology configuration;
- different hydrology exchange units/field schema;
- different precision representation where no migration policy is qualified.

## Feature changes at accepted boundaries

ARCH04 does not generally permit dynamic feature topology mutation during a run. Turning a persistent-state feature on or off changes physical state topology and therefore requires either:

1. construction of a new model instance from an admitted initialization/migration transaction; or
2. a future specifically qualified topology-transition contract.

A plain timestep commit is not such a contract.

Diagnostic mode is different: observer allocation may change at an accepted boundary if diagnostic continuation semantics are respected and the physical layout is unchanged.

## Batch/execution implication

The same feature-layout identity can later be used to group logical columns into homogeneous execution classes. This is an implementation opportunity, not an ARCH04 production admission. Columns with different physical topology belong to different layout classes rather than silently allocating a superset and pretending the physics is identical.

## Relationship to ARCH02 and ARCH03

ARCH02 uses compatible owner/shape identity to define checkpoint sufficiency. ARCH04 makes those compatibility inputs explicit.

ARCH03 already includes `feature_layout_id` and `geometry_id` in the candidate MassLedger observer schema. ARCH04 provides the logical content behind that feature-layout identity. It does not yet make the MassLedger canonical.
