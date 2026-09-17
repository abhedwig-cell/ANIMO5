# ANIMO-KT07 Qualification Report

## Disposition

KT07 qualifies a bounded B1 derived evidence fixture for the complete first
explicit-state LWKM Hlpimp=11 hydrology packet and its lossless consumption by
the frozen KT05 compiled hydrology call-boundary adapter.

Exact verdict:

`QUALIFIED_B1_DERIVED_FULL_LWKM_EXPLICIT_HYDROLOGY_PACKET_FIXTURE_AND_COMPILED_KT05_PROJECTION_NO_B2_OR_RUNTIME_OR_SCIENTIFIC_EQUIVALENCE`

Frozen qualified evidence/tooling head:

`2d469e0a00071b73207112222199eef82c96a961`

Exact-head GitHub Actions run:

`35288769233 -> SUCCESS`

## Qualified evidence identities

- supplied LWKM `SWATRE.UNF` SHA-256:
  `b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c`;
- first dynamic logical-record group SHA-256:
  `2e5e8ff7c088ddd94f91aeb663ea10abdecfda0ac4cd418a8bf90be955389ec7`;
- normalized typed-step SHA-256:
  `eeeb862839cce8111535fae86220d8574240804b9f6f029f7ec8e07ceb65da1c`.

The committed fixture is
`reference/kt07/LWKM_FIRST_EXPLICIT_HYDROLOGY_STEP.json`.

## Qualified capabilities

The frozen KT07 head establishes:

1. a complete persisted first LWKM Hlpimp=11 normalized `HydrologyStep`
   derived from the pinned producer bytes;
2. independent fail-closed pins for raw file, dynamic logical-record group and
   normalized typed-step identity;
3. machine validation of schema, dimensions, explicit interception state,
   temperature availability and complete array shapes;
4. a fail-closed materializer for regenerating the fixture when the pinned raw
   B0 file is available;
5. deterministic JSON-to-Fortran fixture generation for compiled adapter tests;
6. successful frozen KT05 validation of the complete derived packet;
7. successful frozen KT05 projection of the producer-derived
   `Hydro_detailed` external subset;
8. exact preservation of all projected values represented by the persisted
   B1 fixture;
9. successful legacy-slice mapping while preserving ANIMO-owned index-zero
   slices.

## Evidence strength

The qualified evidence class remains:

`B1_DERIVED_FROM_PINNED_B0_PRODUCER_NOT_B2`

KT07 does not upgrade the KT03 diagnostic normalization to B2. The raw B0 file
remains external to the repository and CI does not independently execute the
historical Intel/PowerStation model environment.

The first failed CI run was a test-expression/tooling failure and did not alter
this evidence classification.

## Relationship to KT06

KT07 does not consume KT06 as qualified authority and does not alter the open
KT06 Tier C gate.

KT07 may be reused later as stronger B1 producer-contact evidence for work that
consumes the KT03/KT05 hydrology contract, provided its exact identities and
scope remain unchanged.

It cannot substitute for the genuinely independent Tier C review required to
qualify KT06 runtime interval semantics.

## Review evidence

Same-agent review assurance:

`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`

Final same-agent result:

`SELF_REVIEW_PASS_B1_EVIDENCE_TOOLING_ONLY`

The only substantive evidence-integrity finding, KT07-R1, was remediated before
the frozen qualified head and exact-head CI.

## Explicit nonclaims

KT07 does not qualify:

- B2 historical compiler or executable equivalence;
- Hlpimp=1 or Hlpimp=2 semantics;
- revision-53 `Hydro_detailed` execution or numerical equivalence;
- ANIMO scientific admissibility or conservation;
- KT02 or KT06 runtime integration;
- SWAP5 in-memory production;
- retry or timestep-selection policy;
- production source migration;
- B3/B4 admission;
- Status A or Status AA.

## Handoff

The runtime/coupling lane remains at the KT06 independent Tier C review
boundary. KT07 is closed and can be cited as bounded B1 packet evidence after
its frozen head is verified.
