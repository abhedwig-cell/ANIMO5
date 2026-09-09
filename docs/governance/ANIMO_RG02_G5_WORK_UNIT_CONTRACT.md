# ANIMO-RG02 G5 work unit contract

Status: `RESERVED_AND_STARTED`.

## Work unit

`ANIMO-RG02-G5 — Independent Theory, Testing, Numerical, Temporal & Scientific Stream Attachment`

Repository: `abhedwig-cell/ANIMO5`

Branch: `work/animo-rg02-g5-independent-stream-attachment`

Parent RG02 authority head at start: `ec8709cd6a37c985ab7452bc0f2e6e64a430db6a`.

## Purpose

Attach independently qualified ANIMO5 evidence streams to the RG02 integration DAG by explicit branch/head/status references while preserving their evidence strength, authority boundaries, unresolved blockers and non-admission status.

This gate must not collapse theory, testcase, numerical, temporal, architecture or scientific work into one truth source. It records how they coexist and which later gates consume them.

## Required live refresh

Before qualification, refresh at least:

- theory/provenance streams (`TH01`, authoritative `TH02`);
- testcase qualification (`TQ01`);
- numerical qualification (`NQ01`, applicable `NQ02` work);
- temporal qualification (`TS01`, `TIME01` candidate contract);
- architecture governance (`ARCHG01`, relevant candidate architecture heads);
- discrepancy/scientific qualification streams where persisted (`SQ01`, `MP01`, `GHG01`);
- B3 governance/admission authority (`B3Q01`).

Authority must be established from live branch/head/status evidence, not branch-name inference. Parallel aliases, shadow/copy/final/ignore/stop branches must not be promoted automatically.

## Evidence-preservation rules

1. G5 attaches references, it does not silently merge branch contents.
2. Source-bound evidence remains source-bound.
3. Synthetic or structural qualification remains non-B2.
4. Candidate architecture remains candidate architecture.
5. Numerical policy qualification is not scientific admission unless the owning workunit says so.
6. B3Q01 remains owner of canonical discrepancy/admission classification.
7. B2 reference absence remains visible wherever relevant.
8. `TIME01` may remove an unspecified architecture seam but does not itself admit canonical TIME.
9. GHG/macropore gaps remain explicit if their own workunits are incomplete or blocked.
10. No B4 or production migration admission may be inferred from successful G5 attachment.

## Deliverables

- `docs/governance/ANIMO_RG02_G5_STREAM_ATTACHMENT.md`
- `integration/animo-reg/g5/ANIMO_RG02_G5_STREAM_REGISTER.csv`
- `integration/animo-reg/g5/ANIMO_RG02_G5_GATE_MATRIX.csv`
- `integration/animo-reg/g5/ANIMO_RG02_G5_STATUS.json`

A fail-closed structural checker may be added if useful. It may validate attachment integrity only and must not claim runtime, scientific or historical behavioural qualification.

## Qualification target

`QUALIFIED_INDEPENDENT_STREAM_ATTACHMENT_NO_SCIENTIFIC_COLLAPSE`

with at minimum:

- `b2_reference_qualified = false` unless independently trustworthy B2 has actually become available;
- `b3_scientific_admission = false` for G5 itself;
- `canonical_time_admitted = false` unless separately admitted by its owning gate;
- `b4_baseline_admitted = false`;
- `production_migration_admitted = false`.

## Change boundary

No legacy source modification. No historical testcase modification. No production implementation. No correction admission. No scientific reclassification owned by another workunit.
