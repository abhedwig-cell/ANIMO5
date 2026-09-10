# ANIMO-B3B06R - TCD-030 Independent Second-Line Review Handoff

This branch is a handoff only. No independent review has been performed or approved in the ANIMO-B3B06 authoring context.

## Exact review candidate

Review target: `TCD-030`

Readiness authority: `ANIMO-B3B06@98235bad7d7fb25b5053e9101c52c0ee3226692a`

Readiness CI: GitHub Actions run `34474895406`, conclusion `success`.

Readiness decision presented for independent verification:

`PASS_ATOMIC_TIER_B_READINESS_REQUIRES_ONE_INDEPENDENT_SECOND_LINE_REVIEW`

The reviewer must not inherit that decision as a premise.

## Authority pins

- aggregate regie: `ANIMO-RG05E@eed822037ed8d906a2ab424220597cffac9cca73`;
- post-aggregate TCD-027 admission, external authority only: `ANIMO-B3D13@b20841eb71c338cad21abd8164fa025d8efc75c4`;
- GOV04: `1bbe4c211197590f346803106e45dca5faae79fc`;
- GOV03: `cbd262bdabe92923113b7326f2f42822ce9a971c`;
- B3Q01: `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- MP01: `7b5979dd6301b9d55d23e8c22948a0dba24b229b`;
- MP02: `6b0f2e7470f13baeb6612b0bddb662a497dea528`;
- B3I01 routing: `7b2be9d9742aaad78128c0531591d8e38d7e8450`;
- later B3I03 routing observation: `6a015587807130b4ce12c9f1518c1ddac4e5d624`;
- B3I03 canonical register append: `814ea660d367494432beb63ea78298d1f6cd73d7`;
- frozen B0 retention: `ANIMO-EG01@a818b5a37b80ed92aded0b9c404990d356eb2300`.

Historical behaviour must remain `UNKNOWN` unless the reviewer finds a separately qualified B2 authority.

## Required independent checks

The reviewer must independently establish or fail closed on all of the following:

1. Recheck that no later TCD-030 workunit, issue, evidence, governance authority, or superseding routing has appeared.
2. Verify the frozen B0 archive and exact `mapoinput.for` and `input1.for` identities against controlled provenance. Do not rely only on the readiness prose.
3. Inspect `MaPoInput` directly and verify the `Nupa.EQ.4` path, `>MPnitr:` read order, the two NO3-labelled Checkrea calls, their actual value arguments, and the `Ioptmp.Eq.1` caller gate.
4. Inspect `Checkrea` directly and verify the lower-bound error path and the 999 no-limit sentinel. Do not silently substitute the ANIMO 4.0 documentation range for revision-53 source semantics.
5. Verify that NH4 and NO3 are distinct owners and that the proposed correction is exactly two value-selector substitutions, not an initialization or state reconstruction change.
6. Reproduce the positive, negative, unequal-species, lower-bound, just-below-bound, high-sentinel, NH4-control, and inactive-macropore cases, or provide stronger equivalent coverage.
7. Verify the comparison-domain statement. Physical trajectory equivalence is permitted only where both forms accept the same input. No trajectory-equivalence claim is allowed where corrected validation stops and legacy continues.
8. Verify source-local non-interference for already-valid input: no physical transport algebra, persistent state, restart, numerical policy, solver, tolerance, TCD-025 ledger, or TCD-031 persistent-state change.
9. Reclassify the GOV04 tier from evidence. If persistent-state semantics, restart semantics, initialization-state reconstruction, runtime architecture, or numerical policy is required, return a Tier-C escalation instead of Tier-B PASS.
10. Verify the readiness branch scope and green CI independently. CI is evidence that the encoded contract is self-consistent, not proof of the scientific claim by itself.

## Review disposition

A Tier-B PASS must be genuinely independent and explicit. If the review fails or is incomplete, classify the cause under GOV04 as applicable: `SCIENTIFIC_FALSIFICATION`, `EVIDENCE_INSUFFICIENCY`, `PROVENANCE_INSUFFICIENCY`, `TOOLING_VALIDATOR_FAILURE`, or `SCOPE_AMBIGUITY`.

Do not edit production source, the canonical TCD register, B4 status, production migration status, or central regie in this review workunit.

After an independent PASS with unchanged claim, route, pins, and scope, one downstream workunit may combine TCD-030 formal disposition and admission closeout under GOV04. This handoff does not perform that downstream decision.
