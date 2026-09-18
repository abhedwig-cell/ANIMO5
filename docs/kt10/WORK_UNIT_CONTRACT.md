# ANIMO-KT10 Work Unit Contract

Workunit: `ANIMO-KT10 — KT06 Adversarial Runtime-Boundary Harness`.

Execution discipline: `RECONCILE -> QUALIFY TEST HARNESS -> REVIEW -> CLOSE`.

## Purpose

KT10 is a test/evidence workunit around the frozen KT06 Tier C candidate.

It does **not** qualify KT06 and it does not change KT06 implementation
semantics.

The bounded question is:

> Does the frozen KT06 implementation fail closed at difficult time,
> integer-representation, overflow, calendar and transaction boundaries that are
> directly relevant to the independent-review handoff?

## Subject under test

Frozen KT06 implementation head:

`fc818917a46408d55cd7f03e2fa8257534683907`

Frozen implementation Git blob:

`prototype/kt06/mod_animo_explicit_hydrology_runtime_binding.f90`
=
`9a24ea833291f761d2fa76ca4cc9fee28436c614`.

KT10 consumes this only as a **subject under test**, never as qualified
authority. The test runner fails before compilation if this blob changes.

## Adversarial boundary set

The harness probes:

- missing forcing;
- missing calendar binding;
- negative producer offset;
- negative runtime origin;
- producer endpoint mapping overflow;
- fractional producer endpoint;
- negative producer endpoint;
- negative-zero producer endpoint;
- NaN endpoint;
- infinite producer step;
- calendar mismatch;
- subday endpoint;
- exact success at the deliberate REAL64 integer envelope `2^53 - 1`;
- fail-closed rejection immediately above that envelope;
- accepted-store generation overflow with no external publication;
- retry-permitted flag applied to a KT06 client hard failure, proving it does
  not silently become an acceptance retry.

The existing KT06 stale-forcing private-commit/nonpublication test is rerun
unchanged as baseline evidence.

## Governance

This workunit adds tests only. It changes no production source, KT02 runtime,
KT05 adapter, KT06 implementation, time ownership, forcing ownership, retry
policy, accepted-state semantics, scientific state or process semantics.

Same-agent review must remain labelled
`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

A green KT10 result is supplemental evidence for the genuinely independent
KT06 Tier C reviewer. It is not an independent review outcome.

## Exclusions

No KT06 qualification/admission, no new runtime semantics, no multi-packet
provider, no Hlpimp=1 semantics, no `Hydro_detailed` science, no production
migration, no B3/B4 and no Status A/AA.
