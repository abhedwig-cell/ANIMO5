# ANIMO-KT06 Independent Tier C Review Entry Prompt

Use this text to start the review in a genuinely separate ChatGPT conversation.

---

Ga verder met repository:

`abhedwig-cell/ANIMO5`

Werk rechtstreeks met de GitHub-connector.

Dit is een **genuinely independent GOV04 Tier C second-line review** van:

`ANIMO-KT06 — Explicit Hydrology Runtime Interval Binding`

Werk read-only ten opzichte van de frozen KT06 implementation totdat het
reviewverdict vaststaat. Vertrouw eerdere authoring-context conclusies niet als
bewijs. Reconstructeer de relevante claim zelfstandig uit code, tests,
contracts en pinned evidence.

Review branch:

`review/animo-kt06-explicit-hydrology-runtime-binding-independent`

Frozen KT06 implementation target:

`fc818917a46408d55cd7f03e2fa8257534683907`

Frozen KT06 implementation blob:

`prototype/kt06/mod_animo_explicit_hydrology_runtime_binding.f90`

`9a24ea833291f761d2fa76ca4cc9fee28436c614`

Candidate claim:

> Within the declared exact whole-day envelope, a complete explicit-state KT05
> hydrology packet can be bound to a KT02 requested interval without making
> producer time authoritative, without placing forcing in accepted continuation
> state and without bypassing KT02 atomic publication.

Risk tier:

`GOV04_TIER_C_RUNTIME_SEMANTICS`

Read first:

1. `docs/kt06/INDEPENDENT_REVIEW_HANDOFF.md`
2. `integration/animo-kt06/ANIMO-KT06_REVIEW_PACKET.json`
3. `docs/kt06/WORK_UNIT_CONTRACT.md`
4. `docs/kt06/RECONCILIATION.md`
5. `docs/kt06/ADVERSARIAL_REVIEW.md`
6. `prototype/kt06/mod_animo_explicit_hydrology_runtime_binding.f90`
7. `tests/kt06/test_kt06_explicit_hydrology_runtime_binding.f90`
8. frozen KT02 runtime implementation and transaction code
9. frozen KT05 adapter implementation
10. `docs/kt06/INDEPENDENT_REVIEW_SUPPLEMENT_KT07_KT09.md`
11. `docs/kt06/INDEPENDENT_REVIEW_SUPPLEMENT_KT10.md`

Treat KT07-KT10 strictly as supplemental evidence, not as changes to the frozen
KT06 target and not as qualified runtime authority.

Review independently at least:

- accepted-time ownership;
- external-publication ownership;
- producer endpoint/duration influence on runtime time;
- calendar-id and integer-offset semantics;
- forcing ownership and continuation-state exclusion;
- KT05 validation/projection ordering;
- stale-forcing and partial private interval behavior;
- transaction atomicity;
- lineage and generation protection;
- retry semantics;
- integer/REAL64 conversion limits and overflow;
- untested forcing-lifecycle or packet-selection assumptions;
- risk that the probe admissibility candidate is mistaken for real ANIMO
  scientific admissibility;
- accidental import of Hlpimp semantics, Hydro_detailed science, timestep
  selection, production coupling or B3/B4 claims.

Do not broaden the review into unrelated ANIMO science.

The review must return exactly one principal verdict:

- `PASS_CLAIM_UNCHANGED`
- `PASS_WITH_NON_SEMANTIC_REMEDIATION`
- `REOPEN_RUNTIME_SEMANTIC_CLAIM`
- `NEGATIVE_DISPOSITION_REQUIRED`

For every material finding, give the exact file/surface and explain whether it
changes time ownership, forcing ownership, accepted-state semantics, interval
mapping or consumed scientific authority.

If the verdict is PASS, persist an independent review report and review
checkpoint on the review branch, clearly labelled as independent second-line
review evidence. Do not mutate the frozen KT06 implementation.

If the verdict requires semantic reopening, do not patch KT06 silently. Persist
the review finding and hand back to a separate remediation workunit.

No Status A, B3, B4 or production claim follows automatically from a PASS.
