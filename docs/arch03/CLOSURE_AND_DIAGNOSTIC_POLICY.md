# ANIMO-ARCH03 closure and diagnostic policy

Status: `CANDIDATE_ARCHITECTURE_DESIGN_NO_NUMERICAL_TOLERANCE`.

## Semantic closure

ARCH03 defines the algebraic conservation residual only:

`R = S_end - S_begin - I_external + O_external`

The target identity is `R = 0`.

ARCH03 deliberately does not define `abs(R) <= tolerance`. A tolerance is numerical policy and must be qualified separately after canonical state and time semantics are admitted.

## Why this separation matters

Several legacy findings show different causes of nonclosure:

- TCD-014: initialization partition consistency;
- TCD-015: local transport reconstruction;
- TCD-016: vanishing-water state representability;
- TCD-018: omitted physical water storage in the public ledger;
- TCD-019: finite-change constitutive numerical nonclosure;
- TCD-023: cross-species reaction binding;
- TCD-025: incomplete macropore control-volume exposure;
- TCD-029: multi-site management state/constitutive mismatch.

A single tolerance cannot turn these into the same problem. ARCH03 therefore reports raw residual and diagnostic cause channels separately.

## Diagnostic channels

The candidate observer exposes at least:

- `closure_residual`: profile/control-volume conservation residual;
- `reaction_bundle_nonclosure`: source/sink mismatch inside one typed reaction bundle;
- `initialization_nonclosure`: representational projection mismatch before first accepted state;
- `constraint_nonclosure`: state-domain clipping or similar numerical constraint mass change not assigned to a qualified physical route;
- `observer_integrity_status`: duplicate/missing event consumption, incompatible owner mapping or report mutation.

These channels are evidence. They do not repair model state.

## Reporting integrity versus physical closure

A reporting defect can coexist with a physically closed trajectory. TCD-017, TCD-027 and TCD-028 demonstrate that distinction.

Conversely, a physical defect can be hidden by a compensating reporting convention. Therefore:

1. physical closure is derived from owner state and typed events;
2. detailed reports are projections of those same sources;
3. report-specific accumulator identities are tested separately;
4. no report accumulator participates in physical closure.

## Trial diagnostics

A trial ledger may be evaluated before commit to support solver diagnostics. It must be labeled trial evidence and may not mutate accepted state or cumulative committed reporting.

On reject, trial state and trial event journal are discarded together. Any retained diagnostic record is nonphysical evidence only.

## Future numerical qualification

A later numerical-policy workunit may define:

- absolute or relative closure thresholds;
- scaling by storage or flux magnitude;
- precision-dependent criteria;
- reaction-bundle versus profile thresholds;
- accumulation rules over long runs.

ARCH03 does not pre-empt those choices.
