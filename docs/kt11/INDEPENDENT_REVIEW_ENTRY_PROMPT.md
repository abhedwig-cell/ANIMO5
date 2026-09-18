# ANIMO-KT11 Independent Tier C Review Entry Prompt

Use this text in a genuinely separate ChatGPT conversation.

---

Ga verder met repository:

`abhedwig-cell/ANIMO5`

Werk rechtstreeks met de GitHub-connector.

Voer een **genuinely independent GOV04 Tier C second-line review** uit van:

`ANIMO-KT11 - Typed Multi-Packet Hydrology Provider and Forcing Lifecycle`

Review branch:

`review/animo-kt11-multi-packet-hydrology-provider-independent`

Frozen KT11 candidate head:

`843ac357f8b86f84131ddc08bf2097bb5af4e080`

Frozen implementation blob:

`prototype/kt11/mod_animo_multi_packet_hydrology_provider.f90`
= `a41d0f61da6dd30a18dbfadbe4b29b00259fa41e`

Lees eerst:

- `docs/kt11/INDEPENDENT_REVIEW_HANDOFF.md`;
- `integration/animo-kt11/ANIMO-KT11_REVIEW_PACKET.json`;
- `docs/kt11/WORK_UNIT_CONTRACT.md`;
- `docs/kt11/RECONCILIATION.md`;
- provider source and tests;
- frozen KT06, KT05 and KT02 surfaces waar nodig.

Behandel eerdere same-agent conclusies uitsluitend als reviewondersteuning, niet
als bewijs. Reconstructeer de claim zelfstandig.

Controleer met name packet identity, duplicate semantics, equal-endpoint
different-duration semantics, deep-copy ownership, stateless repeated lookup,
sparse provider behaviour, missing-packet atomicity, forcing ownership, KT06
delegation, time/calendar ownership, overflow, retry exclusions en de precieze
evidence strength van KT08/KT09.

Geef exact een van:

- `PASS_CLAIM_UNCHANGED`
- `PASS_WITH_NON_SEMANTIC_REMEDIATION`
- `REOPEN_RUNTIME_SEMANTIC_CLAIM`
- `NEGATIVE_DISPOSITION_REQUIRED`

Persist bij PASS een independent review report en checkpoint op de reviewbranch.
Wijzig de frozen KT11 implementation niet tijdens review. Als een semantische
wijziging nodig is, persist de finding en reopen in een aparte remediation
workunit.
