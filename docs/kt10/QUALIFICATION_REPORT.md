# ANIMO-KT10 Qualification and Closeout Report

## Decision

KT10 is closed as supplemental adversarial test evidence around the frozen KT06
runtime-binding candidate.

Exact verdict:

`QUALIFIED_SUPPLEMENTAL_ADVERSARIAL_TEST_EVIDENCE_FOR_FROZEN_KT06_NO_KT06_QUALIFICATION_EFFECT`

This is a test/evidence qualification only.

## Frozen evidence target

- branch: `work/animo-kt10-kt06-adversarial-boundary-harness`;
- tested harness head: `0c29b1ff14c0e6fca3cf13fe7c8662825ac86da3`;
- exact-head CI run: `35294371116`;
- CI conclusion: `SUCCESS`;
- reviewed KT06 implementation head:
  `fc818917a46408d55cd7f03e2fa8257534683907`;
- reviewed KT06 implementation blob:
  `9a24ea833291f761d2fa76ca4cc9fee28436c614`;
- review assurance: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

## Qualified supplemental evidence

KT10 adds executable evidence that the frozen KT06 boundary fails closed for:

- missing forcing and missing calendar binding;
- negative runtime or producer-coordinate cases;
- producer-time mapping overflow;
- fractional, negative, negative-zero and nonfinite producer metadata;
- calendar mismatch and subday mapping;
- REAL64 integer representation immediately at and above the declared
  `2^53 - 1` exact-integer envelope;
- accepted-store generation overflow without external publication;
- a retry-permitted flag presented alongside a KT06 hard client failure.

The exact-head workflow also reruns frozen KT02, KT05 and KT06 tests.

## Review result

Same-agent adversarial review verdict:

`SELF_REVIEW_PASS_SUPPLEMENTAL_ADVERSARIAL_KT06_BOUNDARY_EVIDENCE_ONLY`

No material defect was found in the bounded KT10 evidence claim.

## Dependency integrity

The KT02 runtime modules used by KT10 are blob-identical to the frozen KT02
authority. The KT05 adapter is blob-identical to the frozen KT05 implementation.
The KT10 runner pins the KT06 implementation blob and fails before compilation
if that file changes.

KT10 therefore strengthens evidence around the frozen candidate without
silently changing the subject under test.

## Nonclaims

KT10 does not qualify or admit:

- KT06 under GOV04 Tier C;
- ANIMO scientific admissibility;
- Hlpimp=1 or Hlpimp=2 semantics;
- `Hydro_detailed` scientific execution;
- subday or fractional time mapping;
- multi-packet forcing;
- retry or timestep-selection policy;
- production migration;
- B3 or B4;
- Status A or Status AA.

## Next permitted action

Provide KT10 as supplemental evidence to the genuinely independent KT06 Tier C
reviewer.

The independent reviewer must still return one of the allowed KT06 review
results against the frozen KT06 target. KT10 must not be used as a substitute
for that review.
