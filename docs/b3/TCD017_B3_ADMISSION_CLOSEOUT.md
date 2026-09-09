# TCD-017 B3 admission closeout

Work unit: `ANIMO-B3D02`

Target: `TCD-017`

Class: `A_ACCOUNTING_REPORTING_ONLY`

Route: `INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY`

## Decision basis

ANIMO-B3D01 reconciled the GOV03 route and all Class-A readiness gates but remained fail-closed because independent second-line review was still pending.

ANIMO-B3A02R subsequently completed that review on the frozen review object `3ff8f4bda77c631b82110b83317c6a9b42b867ad` and persisted:

`PASS_TCD017_INDEPENDENT_SECOND_LINE_READINESS_REVIEW`

at review head:

`8b38b03ac489c349192ae9fa55a8fe51cea183cb`

with GitHub Actions run `34393646704` successful and issue #25 updated with the review result.

GOV03 remains authoritative for the route precondition:

- `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`;
- `G6U = ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS`.

## Atomic admission

The admitted scientific/accounting claim is only that the already-existing top-reservoir dissolved-organic-P ploughing loss:

`Addiorpotoppl(I)`

must contribute to the `Bapo(Redi,Ly)` redistribution ledger in the bounded reporting branch through:

```fortran
Bapo(Redi,Ly) = Bapo(Redi,Ly) + Addiorpotoppl(I)*Z
```

The corresponding layer redistribution is already represented through `Addiorpopl(I,Ln)`, and the encompassing top-plus-layer physical redistribution closes before any reporting correction.

## Final disposition

The correct B3 disposition under the GOV03 route is:

`HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY`

This is deliberately not `PRESERVE_HISTORICAL_BEHAVIOUR`, because no B2 historical behavioural reference exists, and it is not a historical-fidelity claim.

It admits the atomic Class-A scientific/accounting correction into the B3 scientific legacy baseline with inherited historical uncertainty.

## Gates

All mandatory gates are PASS:

- B0 identity;
- B1 causal evidence;
- GOV03 historical-uncertainty route;
- theory/accounting identity;
- causal source evidence;
- conservation;
- expected-difference contract;
- non-interference;
- path coverage;
- independent second-line review;
- residual uncertainty;
- Class-A-specific evidence;
- composition gate as not applicable.

## Explicit boundaries

This admission does not:

- establish revision-53 historical behaviour;
- create or recover B2;
- promote the modern rebuild or problematic executable to B2;
- authorize a production source patch;
- admit B4;
- admit production migration;
- qualify composition with TCD-027, TCD-028 or any other organic-P finding;
- change frozen B0 source, testcase or the canonical TCD register.

Historical revision-53 behaviour remains `UNKNOWN`.

The independent second-line review was performed in a separate ChatGPT context from the B3A02/B3D01 authoring context. No organizational or human independence beyond that is claimed.

## Result

Subject to successful B3D02 validator and scope guard, TCD-017 becomes the first atomic B3 scientific admission under the qualified historical-uncertainty route.
