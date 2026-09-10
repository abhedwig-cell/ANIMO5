# ANIMO-B3B06R — Independent Second-Line Review Instructions for TCD-030

This branch is a review handoff only. The review must be performed in a genuinely separate ChatGPT context. Do not treat ANIMO-B3B06 conclusions as authoritative merely because they are present on this branch.

## Target

TCD-030: macropore initial NO3 validation wrong-species check.

## Review starting point

Readiness authority:

`ANIMO-B3B06@98235bad7d7fb25b5053e9101c52c0ee3226692a`

Readiness CI:

`34474895406` — expected conclusion `success`

Review handoff status was first persisted at:

`ANIMO-B3B06R@d3980653d8affac71d29ae20d4fe20b1509b0345`

Before writing a review result, recheck live that the readiness authority, review branch, governance pins, canonical routing and TCD-030 issue/evidence state have not been superseded.

## Authorities to verify independently

- aggregate central regie: `ANIMO-RG05E@eed822037ed8d906a2ab424220597cffac9cca73`;
- GOV04: `1bbe4c211197590f346803106e45dca5faae79fc`;
- GOV03: `cbd262bdabe92923113b7326f2f42822ce9a971c`;
- B3Q01: `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- MP01: `7b5979dd6301b9d55d23e8c22948a0dba24b229b`;
- later macropore evidence, including MP02 and any newer MP workunit found live;
- B3I01 and all later canonical routing/register authorities;
- frozen B0 retention authority and exact frozen source identity.

## Independence requirement

The reviewer must reconstruct the source seam and qualification logic from source and evidence rather than simply confirming the readiness report.

At minimum, independently establish:

1. routine and exact branch condition;
2. exact values read for macropore NH4 and NO3;
3. exact value arguments passed by the two NO3-labelled validation calls;
4. intended corrected species/value selectors;
5. exact lower/upper-bound semantics of the checker, including the meaning of `999.0`;
6. diagnostic and error-return path;
7. whether the seam affects validation only or also changes stored model state;
8. activation gate for macropore input processing;
9. whether TCD-025 ledger composition or TCD-031 restart/state composition is absent;
10. whether GOV04 Tier B remains justified or Tier C escalation is required.

## Branch-coverage review

Recheck the executable matrix rather than relying on its reported PASS. The review should require at least:

- active macropore, valid unequal NH4 and NO3 values;
- active macropore, first NO3 value negative while NH4 stays valid;
- active macropore, second NO3 value negative while NH4 stays valid;
- exact lower boundary `0.0`;
- a just-below-zero NO3 value;
- a value above `999.0` to verify whether `999.0` is a sentinel rather than an actual upper bound;
- negative NH4 with valid NO3 as an ownership/control case;
- inactive macropore configuration.

The unequal-species controls are mandatory. A test where NH4 and NO3 happen to be equal cannot prove a wrong-species selector defect.

## Expected-difference contract to challenge

The readiness workunit claims that the proposed atomic correction is limited to replacing the two wrong NO3 validation value selectors and that expected differences are restricted to input acceptance/rejection plus directly associated diagnostics.

The reviewer must independently decide whether that is correct.

Do not claim trajectory equivalence for cases where one implementation rejects before model execution and the other proceeds. On the common accepted-input domain, verify that no physical transport state, persistent state, restart semantics, solver behaviour or numerical policy changes are introduced by the proposed local correction.

## GOV04 decision

Default hypothesis presented by readiness: Tier B local species/input-validation algebra.

Escalate to Tier C and fail the Tier-B admission route if independent evidence shows that a valid correction requires any of:

- persistent macropore state semantics;
- restart semantics;
- initialization-state reconstruction;
- runtime architecture changes;
- numerical-policy or solver changes;
- unresolved state/source ownership with scientific consequences.

## Historical evidence

Historical behaviour remains `UNKNOWN` unless a qualified B2 source is actually found and proven applicable. Do not promote synthetic or source-only evidence to historical reference evidence.

## Allowed outcomes

The independent review should end in one explicit fail-closed result, for example:

- `PASS_INDEPENDENT_SECOND_LINE_REVIEW_TIER_B`;
- `FAIL_SCIENTIFIC_FALSIFICATION`;
- `FAIL_EVIDENCE_INSUFFICIENCY`;
- `FAIL_PROVENANCE_INSUFFICIENCY`;
- `FAIL_TOOLING_VALIDATOR_FAILURE`;
- `FAIL_SCOPE_AMBIGUITY`;
- `ESCALATE_TIER_C`.

Record the exact evidence and pins supporting the result.

## Prohibited actions in this review workunit

Do not:

- edit production source;
- edit the canonical TCD register;
- perform B4 work;
- start production migration;
- update central regie;
- combine this review with downstream disposition/admission;
- treat the authoring-context readiness conclusion as the independent decision.

If and only if the independent review passes with unchanged claim, route, pins and scope, the next downstream workunit may combine TCD-030 formal disposition and admission closeout under GOV04 Tier B.
