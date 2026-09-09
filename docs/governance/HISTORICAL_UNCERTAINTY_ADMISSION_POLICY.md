# Historical-uncertainty scientific-admission policy

Work unit: `ANIMO-GOV02`

## Purpose

This policy defines the only route by which a process-level scientific B3 disposition may eventually be considered when an independently trusted B2 historical reference is genuinely unavailable. The route does not create B2, does not prove historical fidelity and does not lower the scientific evidence burden.

Route identifier:

`INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY`

## Entry gate

The route is closed unless the relevant PREP02R scope has reached:

`B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`

No other PREP02R closure state is eligible. In particular, `B2_ACQUISITION_STILL_ACTIVE` and `B2_ACQUISITION_INSUFFICIENTLY_ATTEMPTED` are hard blocks.

## Mandatory acquisition evidence

Entry requires all of the following to be persisted and independently reviewable:

1. the prepared targeted WUR archival request was actually sent through a verified institutional route;
2. a response was received, or the lack of a recoverable artifact was otherwise documented without inventing a response;
3. at least one additional plausible archive/contact route was attempted where meaningful, or a concrete reason is recorded why no such route exists;
4. the public-search history is recorded;
5. an independent reviewer approved the stopping rationale;
6. there is no known concrete high-probability route that was consciously skipped.

A prepared but unsent request is not acquisition effort completion.

## Scientific evidence gate

For the scoped claim, all of the following are mandatory:

- explicit atomic B3 class and claim type;
- B0 identity/provenance for the source and testcase artifacts used;
- B1 causal evidence on the actual targeted path;
- a primary scientific authority strong enough for the class, such as authoritative theory, a closed conservation identity, an analytical oracle or an independently implemented numerical reference;
- at least one independent cross-check that does not rely on the same assumption, derivation or implementation as the primary oracle;
- expected corrected difference declared before acceptance evaluation;
- non-interference observations on all unaffected state/flux/process surfaces material to the claim;
- path coverage and edge conditions appropriate to the class;
- independent second-line review of the disposition and its evidence independence;
- class-specific requirements from `B2_REQUIREMENT_SCOPE.md`.

Synthetic evidence may contribute to causality, path coverage or an independently derived scientific oracle. It is never promoted to B2.

## Class hard blocks

- Class A cannot pass without a closed identity and physical state/flux non-interference.
- Class B cannot pass on one implementation-derived synthetic example.
- Class C cannot pass from conservation closure alone; explicit independent state-model authority is required.
- Class D historical representation equivalence cannot use this route. Only B3-to-B4 representation equivalence can proceed while inheriting historical uncertainty.
- Class E cannot pass because a residual became smaller. Separate numerical qualification and independent numerical review are mandatory.
- Class F cannot use this route as a legacy-correction admission shortcut. New physics requires separate model-evolution governance.

## Required disposition fields

A future B3 record using this route must persist at least:

```text
admission_route = INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY
historical_behaviour_status = UNKNOWN
historical_reference_status = UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT
historical_fidelity_claim_admitted = false
acquisition_record = <pinned PREP02R closure artifact>
primary_scientific_oracle = <pinned evidence>
independent_cross_check = <pinned evidence>
second_line_review = <pinned review>
```

The marker is not a warning that can be omitted later. It is part of provenance.

## Composition and B4 propagation

Any composition consuming such a B3 item must preserve the marker. A B4 migration record may claim representation equivalence only against the admitted B3 contract for the scoped process. It must not claim historical equivalence unless a later B2 comparison independently establishes that claim.

Release notes and regression documentation must distinguish:

- scientifically admitted process behaviour;
- historically qualified behaviour;
- historically unknown behaviour.

## Later recovery of B2

If B2 becomes available after a historical-uncertainty scientific disposition:

1. do not retroactively rewrite the original admission record;
2. open a new historical comparison against the recovered B2 artifact;
3. record agreement, bounded difference or discrepancy explicitly;
4. update downstream historical-fidelity claims only through a new reviewed governance action.

Scientific correctness and historical fidelity remain separate claim axes even after the comparison.

## Current activation state

At the GOV02 authority snapshot PREP02R records that the prepared external request has not yet been sent. Therefore:

`historical_uncertainty_route_active = false`

`current_PREP02R_policy_state = B2_ACQUISITION_STILL_ACTIVE`

No current TCD becomes eligible or admitted by publication of this policy.
