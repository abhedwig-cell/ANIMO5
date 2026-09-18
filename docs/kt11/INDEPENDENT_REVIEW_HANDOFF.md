# ANIMO-KT11 Independent GOV04 Tier C Review Handoff

## Review target

Workunit:

`ANIMO-KT11 - Typed Multi-Packet Hydrology Provider and Forcing Lifecycle`

Frozen candidate head:

`843ac357f8b86f84131ddc08bf2097bb5af4e080`

Frozen provider implementation:

`prototype/kt11/mod_animo_multi_packet_hydrology_provider.f90`

Blob:

`a41d0f61da6dd30a18dbfadbe4b29b00259fa41e`

Exact-head CI:

`35351056242 -> SUCCESS`

Risk tier:

`GOV04_TIER_C_RUNTIME_SEMANTICS`

## Candidate claim

> An immutable collection of complete KT05 explicit hydrology packets can
> deterministically select exactly one packet from a bounded whole-day KT02
> requested interval, remain stateless across repeated requests, fail closed on
> missing or duplicate interval keys, and delegate the selected packet through
> admitted KT06 without changing KT02 time, accepted-state or publication
> ownership.

## Authorities to verify rather than merely trust

- KT06 admission:
  `ANIMO-KT06-A1@56384db4107aed484218363e26dbb7be7f51e8de`;
- frozen KT06 implementation head:
  `fc818917a46408d55cd7f03e2fa8257534683907`;
- frozen KT06 implementation blob:
  `9a24ea833291f761d2fa76ca4cc9fee28436c614`;
- central-regie attachment:
  `ANIMO-RG05P@9a8d0d886f745be91153f47437cb0de2b3076ab2`;
- frozen KT05 adapter blob:
  `9ed1d6d3e91d9f5522f8c2a49a5e19eed1d82a9a`;
- frozen KT02 interval runtime blob:
  `ac8eed3b7385daad3cb7c926bd7dab9d99e0a888`;
- frozen KT02 transaction blob:
  `182164ca4bf4a890d98f9c89366764e5d818b10c`.

Supplemental producer evidence only:

- KT08 closeout:
  `281dc65cbaceaa61d31f9cb731b3c5a733ca5d57`;
- KT09 closeout:
  `249066b7c07d505ba9a72a5aa199401a4349b0da`.

## Primary review surfaces

1. `prototype/kt11/mod_animo_multi_packet_hydrology_provider.f90`
2. `tests/kt11/test_kt11_multi_packet_hydrology_provider.f90`
3. `tests/kt11/run_kt11_tests.sh`
4. `docs/kt11/WORK_UNIT_CONTRACT.md`
5. `docs/kt11/RECONCILIATION.md`
6. `docs/kt11/ADVERSARIAL_REVIEW.md`
7. `docs/kt11/QUALIFICATION_REPORT.md`
8. `integration/animo-kt11/ANIMO-KT11_CHECKPOINT.json`
9. `integration/animo-kt11/ANIMO-KT11_REVIEW_PACKET.json`
10. frozen KT06, KT05 and KT02 implementation surfaces as needed.

## Independent questions

The reviewer should independently determine whether:

1. the exact `(endpoint, duration)` key is sufficient and unambiguous for the
   bounded claim;
2. permitting equal endpoints with different durations is correct because KT02
   origin plus endpoint identifies the interval;
3. intrinsic derived-type assignment genuinely isolates the private packet
   collection from later caller mutation;
4. no hidden mutable cursor, consumption state or request-order dependency
   exists;
5. sparse/unordered provider semantics are adequately bounded and missing
   coverage fails closed;
6. a missing later packet cannot partially publish a KT02 private interval;
7. the delegate path preserves KT06 as the binding owner rather than silently
   reimplementing or bypassing it;
8. forcing remains outside accepted continuation state;
9. calendar and producer-offset semantics remain exactly those admitted by KT06;
10. no retry, timestep-selection, scientific-admissibility or production claim
    is imported;
11. KT08/KT09 evidence is used only at its actual B1 producer/contact strength;
12. any overflow, duplicate-key, lifecycle or aliasing case remains untested and
    materially threatens the claim.

"Lifecycle" in this workunit means immutable provider availability and repeatable
selection. It does not mean streaming, dynamic reload, cache eviction or
external producer orchestration.

## Required principal result

Return exactly one of:

- `PASS_CLAIM_UNCHANGED`;
- `PASS_WITH_NON_SEMANTIC_REMEDIATION`;
- `REOPEN_RUNTIME_SEMANTIC_CLAIM`;
- `NEGATIVE_DISPOSITION_REQUIRED`.

Any semantic change to packet identity, lookup ownership, forcing ownership,
time ownership, accepted-state semantics, interval mapping or consumed
scientific authority requires reopening rather than documentation-only closeout.

The independent review must be performed from a genuinely separate review
context. Creation of a review branch is not itself review evidence.
