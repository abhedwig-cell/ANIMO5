# ANIMO-KT06 Independent Tier C Review Handoff

## Review target

Workunit:

`ANIMO-KT06 — Explicit Hydrology Runtime Interval Binding`

Candidate claim:

> Within the declared exact whole-day envelope, a complete explicit-state KT05
> hydrology packet can be bound to a KT02 requested interval without making
> producer time authoritative, without placing forcing in accepted continuation
> state and without bypassing KT02 atomic publication.

This is a runtime/coupling-semantics claim. It is not an ANIMO scientific
process or numerical-equivalence claim.

## Frozen review target

- branch:
  `work/animo-kt06-explicit-hydrology-runtime-binding`;
- exact implementation/remediation head:
  `fc818917a46408d55cd7f03e2fa8257534683907`;
- exact-head CI:
  `35286651951 -> SUCCESS`;
- KT02 authority:
  `ANIMO-KT02@1f88db4dc87fc4d93075884ac35a59711f0725bf`;
- KT02 frozen executable:
  `1909709e7a244b5d0ee53342a26bab74815c118c`;
- KT03 authority:
  `ANIMO-KT03@c5d4c14fbd4ce77ed5ef369bb8ecaee0709ea3b8`;
- canonical KT05 closeout:
  `3319e57adbf6036a86684f8e26d9559454c07b82`;
- KT05 frozen implementation:
  `69dd607ba1efa28de3f83cc963526021352b3311`.

KT03F01 is explicitly not a consumed qualified authority.

Suggested independent review branch:

`review/animo-kt06-explicit-hydrology-runtime-binding-independent`

The review must be performed from a genuinely separate review context. The
authoring context must not self-approve this Tier C gate.

## Primary review surfaces

1. `prototype/kt06/mod_animo_explicit_hydrology_runtime_binding.f90`
2. `tests/kt06/test_kt06_explicit_hydrology_runtime_binding.f90`
3. `tests/kt06/mod_kt06_lwkm_interval_fixture.f90`
4. `tests/kt06/test_kt06_fixture_contract.py`
5. `docs/kt06/WORK_UNIT_CONTRACT.md`
6. `docs/kt06/RECONCILIATION.md`
7. `docs/kt06/PRECLOSE_REVIEW_NOTES.md`
8. `docs/kt06/ADVERSARIAL_REVIEW.md`
9. `reference/kt06/LWKM_FIRST_INTERVAL_METADATA.json`
10. `integration/animo-kt06/ANIMO-KT06_CHECKPOINT.json`

Also inspect the consumed frozen KT02 and KT05 implementations where needed to
verify ownership claims rather than trusting KT06 documentation.

## Questions for the independent reviewer

1. Does KT02 remain the sole accepted-time and publication authority?
2. Can producer endpoint/duration metadata influence runtime time beyond
   fail-closed equality checks?
3. Is the calendar-id plus integer-offset relation sufficiently explicit and
   bounded for this candidate, without smuggling in a calendar conversion?
4. Does the complete KT05 packet get validated and projected before a runtime
   candidate can be returned?
5. Is hydrology forcing genuinely outside accepted continuation state?
6. Does the stale-forcing two-request test adequately prove nonpublication of a
   partial private interval?
7. Does the probe naming and documentation sufficiently prevent the no-op
   admissible candidate from being confused with real ANIMO scientific
   admissibility?
8. Is the B1 LWKM contact bounded correctly, given that most test packet fields
   are synthetic?
9. Are any Hlpimp=1 semantics, `Hydro_detailed` science, retry policy,
   timestep selection or production-coupling claims being imported implicitly?
10. Are there hidden overflow, calendar, lineage, retry or forcing-lifecycle
    cases that require remediation before even a nonproduction runtime-binding
    qualification?

## Required review result

Return one of:

- `PASS_CLAIM_UNCHANGED`;
- `PASS_WITH_NON_SEMANTIC_REMEDIATION`;
- `REOPEN_RUNTIME_SEMANTIC_CLAIM`;
- `NEGATIVE_DISPOSITION_REQUIRED`.

Any change to time ownership, forcing ownership, accepted-state semantics,
interval mapping or consumed scientific authority requires reopening
qualification rather than documentation-only closeout.
