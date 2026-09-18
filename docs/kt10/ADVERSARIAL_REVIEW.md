# ANIMO-KT10 Same-Agent Adversarial Review

Review mode: `same-agent / not genuinely independent`.

Assurance label: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Frozen KT10 harness head reviewed:

`0c29b1ff14c0e6fca3cf13fe7c8662825ac86da3`

Exact-head GitHub Actions run:

`35294371116 -> SUCCESS`

Subject under test:

- frozen KT06 implementation head: `fc818917a46408d55cd7f03e2fa8257534683907`;
- frozen KT06 implementation blob:
  `prototype/kt06/mod_animo_explicit_hydrology_runtime_binding.f90`
  = `9a24ea833291f761d2fa76ca4cc9fee28436c614`;
- KT02 runtime modules on the KT10 branch are blob-identical to the frozen KT02
  authority;
- the KT05 adapter on the KT10 branch is blob-identical to the frozen KT05
  implementation.

This review is limited to the KT10 test/evidence claim. It does not review or
qualify KT06 itself.

## Review questions

### 1. Does KT10 test difficult producer-time representation boundaries?

**PASS.**

The harness exercises missing forcing, missing calendar binding, negative
producer offset, negative runtime origin, offset overflow, fractional endpoint,
negative endpoint, negative zero, NaN endpoint, infinite step, calendar
mismatch and subday runtime mapping.

The deliberate REAL64 integer envelope is tested on both sides:
`2^53 - 1` succeeds and `2^53` is rejected by the declared bounded mapping.

### 2. Does KT10 exercise atomic publication failure rather than only direct client validation?

**PASS.**

The generation-overflow case reconstructs an otherwise valid accepted store at
maximum generation, executes through the shared KT02 runtime and verifies that a
failed commit leaves the externally accepted generation, time and payload
unchanged.

This directly probes the publication boundary rather than only the KT06 client.

### 3. Can the retry flag convert a KT06 hard client failure into a retry or acceptance?

**PASS.**

The harness supplies a producer-step mismatch while
`retry_permitted_after_reject=.true.`. The shared runtime returns
`CLIENT_ATTEMPT_FAILED`, performs one attempt, performs no commit and leaves the
external accepted store unchanged.

This is consistent with the KT02 contract: retry permission applies only after a
constructed trial result reaches `commit_trial` and is rejected specifically as
`ACCEPTANCE_REJECTED_OR_INCOMPLETE`. It does not mask a client execution
failure.

### 4. Are lineage and transaction ownership still protected?

**PASS within the declared KT10 surface.**

KT06 never receives or constructs lineage metadata. The shared KT02 runtime
creates the trial from the working accepted store, while `commit_trial` checks
lineage id, origin generation and origin time before publication. Therefore a
KT06 forcing packet cannot directly forge a different lineage through the
frozen interface.

KT10 does not add a synthetic lineage-corruption hook because doing so would
require changing the shared transaction interface rather than testing the frozen
KT06 boundary. The generation-overflow case nevertheless exercises a real
transactional nonpublication failure.

### 5. Does KT10 silently broaden the KT06 candidate claim?

**PASS.**

No KT02 runtime module, KT05 adapter or KT06 implementation file is changed by
KT10. The new workunit adds only tests, documentation, a workflow and its own
checkpoint.

KT10 does not add subday support, calendar conversion, multi-packet forcing,
retry policy, scientific admissibility, Hlpimp semantics or production
coupling.

## Exact-head execution evidence

GitHub Actions run `35294371116` completed successfully.

Successful steps include:

1. frozen KT02 qualification tests;
2. frozen KT05 compiled adapter tests;
3. KT06 baseline binding tests;
4. KT10 adversarial boundary harness;
5. KT10 checkpoint JSON validation.

No failing test was suppressed or reclassified.

## Findings

No material finding was identified against the bounded KT10 claim.

Two boundary observations remain important but are not KT10 defects:

- the KT06 calendar relation is deliberately an exact calendar-id plus
  nonnegative integer-day-offset relation, not a general calendar conversion;
- KT06 remains a probe/runtime-binding candidate and does not establish real
  ANIMO scientific admissibility merely because a packet validates and projects.

Both boundaries were already explicit before KT10 and are preserved.

## Review verdict

`SELF_REVIEW_PASS_SUPPLEMENTAL_ADVERSARIAL_KT06_BOUNDARY_EVIDENCE_ONLY`

KT10 is suitable to close as supplemental nonproduction test evidence for the
genuinely independent KT06 GOV04 Tier C review.

This verdict has **no KT06 qualification or admission effect**.

The next semantic gate remains the genuinely independent KT06 Tier C review.
