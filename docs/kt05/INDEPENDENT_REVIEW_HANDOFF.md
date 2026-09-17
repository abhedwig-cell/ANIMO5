# ANIMO-KT05 Independent Tier C Review Handoff

## Review target

Workunit:

`ANIMO-KT05 — Explicit-State Hydrology Runtime Interval Binding`

Candidate claim:

> Within a deliberately bounded whole-day envelope, an explicit-state
> KT03-derived hydrology interval binding can be validated against a KT02
> runtime interval without making producer floating time authoritative and
> without placing hydrology forcing into accepted continuation state.

This is an architecture/runtime-semantics claim, not an ANIMO scientific
process claim.

## Frozen review target

- branch: `work/animo-kt05-explicit-state-runtime-adapter`;
- exact implementation/remediation head:
  `c67c28f0475c42351c1a66f58d4d44ce8b584ee5`;
- exact-head CI:
  `35285939129 -> SUCCESS`;
- KT02 runtime authority:
  `ANIMO-KT02@1f88db4dc87fc4d93075884ac35a59711f0725bf`;
- KT02 frozen executable:
  `1909709e7a244b5d0ee53342a26bab74815c118c`;
- KT03 authority:
  `ANIMO-KT03@c5d4c14fbd4ce77ed5ef369bb8ecaee0709ea3b8`;
- KT03 frozen contract implementation:
  `e844c7658a95819fc0463c55737f9bd41b29a6da`.

KT03F01 is deliberately not a consumed qualified authority.

Suggested independent-review branch:

`review/animo-kt05-explicit-state-runtime-binding-independent`

The independent review must be performed from a genuinely separate review
context. The authoring context must not self-approve this Tier C gate.

## Primary review surfaces

1. `prototype/kt05/mod_animo_explicit_hydrology_runtime_adapter.f90`
2. `tests/kt05/test_kt05_explicit_runtime_adapter.f90`
3. `docs/kt05/WORK_UNIT_CONTRACT.md`
4. `docs/kt05/RECONCILIATION.md`
5. `docs/kt05/PRECLOSE_REVIEW_NOTES.md`
6. `docs/kt05/ADVERSARIAL_REVIEW.md`
7. `reference/kt05/LWKM_FIRST_EXPLICIT_INTERVAL.json`
8. `integration/animo-kt05/ANIMO-KT05_CHECKPOINT.json`

## Questions for the independent reviewer

1. Does the adapter preserve KT02 as the sole accepted-time and commit
   authority, or does any forcing field become a hidden time owner?
2. Is the distinct interval-binding identity sufficient to prevent the compact
   view from being confused with the full KT03 `HydrologyStep` schema?
3. Is pinning the runtime calendar contract plus exact integer day offset a
   defensible bounded mapping, with all unsupported fractional/subday cases
   genuinely fail-closed?
4. Does the producer endpoint/duration gate catch stale or mismatched forcing
   before it can publish accepted state?
5. Does the multi-request failure test adequately demonstrate that a valid
   first private commit cannot leak when later forcing identity fails?
6. Is forcing ownership correctly kept outside accepted continuation state?
7. Does the LWKM derived fixture support only the bounded real-producer contact
   claimed, without implying B2 or full hydrology equivalence?
8. Are any Hlpimp=1 semantics, ANIMO scientific admissibility, retry policy or
   production-coupling claims being imported implicitly?
9. Should the semantic source-authority pins or calendar/offset composition be
   strengthened before this candidate is admitted even as a nonproduction
   runtime-binding qualification?

## Required review outcome

Return one of:

- `PASS_CLAIM_UNCHANGED`;
- `PASS_WITH_NON_SEMANTIC_REMEDIATION`;
- `REOPEN_RUNTIME_SEMANTIC_CLAIM`;
- `NEGATIVE_DISPOSITION_REQUIRED`.

Any change to time ownership, forcing ownership, mapping semantics, accepted
state or consumed authority requires reopening qualification rather than a
documentation-only close.
