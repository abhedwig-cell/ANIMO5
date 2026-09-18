# ANIMO-KT06 Independent Review Supplement — KT10 Adversarial Runtime-Boundary Evidence

This supplement is review support only. It does **not** change the frozen KT06
implementation/remediation target:

`fc818917a46408d55cd7f03e2fa8257534683907`

It does not change the KT06 candidate claim, risk tier, qualification state or
required independent-review outcome.

## KT10 evidence

Workunit:

`ANIMO-KT10 — KT06 Adversarial Runtime-Boundary Harness`

Closeout head:

`e4f7f4576cbe5b4d8f2b57b16ea98041fcc06428`

Exact-head CI:

`35294863617 -> SUCCESS`

KT10 verdict:

`QUALIFIED_SUPPLEMENTAL_ADVERSARIAL_TEST_EVIDENCE_FOR_FROZEN_KT06_NO_KT06_QUALIFICATION_EFFECT`

Same-agent review assurance:

`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`

The harness pins the frozen KT06 implementation blob and reruns frozen KT02,
KT05 and KT06 tests before its own adversarial tests.

The additional executable boundary set covers:

- missing forcing;
- missing runtime calendar binding;
- negative producer offset;
- negative runtime origin;
- producer-time mapping overflow;
- fractional, negative and negative-zero producer endpoints;
- NaN endpoint and infinite producer step;
- calendar mismatch;
- subday endpoint rejection;
- exact acceptance at the declared REAL64 integer envelope `2^53 - 1`;
- rejection immediately above that envelope;
- accepted-store generation overflow with no external publication;
- a retry-permitted flag presented alongside a KT06 hard client failure.

KT10 also checked that the KT02 runtime modules used by the harness are
blob-identical to the frozen KT02 authority and that the KT05 adapter is
blob-identical to the frozen KT05 implementation.

## How the independent reviewer should use KT10

KT10 narrows one review question: several previously hypothetical overflow,
calendar and retry/failure-lifecycle cases now have executable fail-closed
evidence.

It does **not** answer the Tier C review on behalf of the reviewer.

The reviewer should independently determine:

1. whether the tested boundary set is sufficient for the stated KT06 claim;
2. whether KT02 remains the sole accepted-time and external-publication authority;
3. whether the calendar-id plus integer offset is a bounded relation rather than
   an implicit calendar conversion;
4. whether forcing remains outside accepted continuation state;
5. whether any untested lineage, retry, stale-forcing or packet-lifecycle path
   can alter the semantic conclusion;
6. whether the probe candidate can still be mistaken for real ANIMO scientific
   admissibility.

## Explicit non-effects

KT10 does not:

- change the frozen KT06 implementation;
- qualify KT06 under GOV04 Tier C;
- supply an independent review result;
- qualify multi-packet forcing;
- qualify retry or timestep-selection policy;
- qualify subday or fractional time mapping;
- qualify Hlpimp semantics;
- execute or qualify `Hydro_detailed` science;
- establish ANIMO scientific admissibility;
- establish B3, B4, Status A or Status AA.

The required independent result remains one of:

- `PASS_CLAIM_UNCHANGED`;
- `PASS_WITH_NON_SEMANTIC_REMEDIATION`;
- `REOPEN_RUNTIME_SEMANTIC_CLAIM`;
- `NEGATIVE_DISPOSITION_REQUIRED`.
