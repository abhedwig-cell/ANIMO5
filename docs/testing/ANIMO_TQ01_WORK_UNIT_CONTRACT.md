# ANIMO-TQ01 — Historical Testcase Lineage, Process Coverage & Evidence Strength Matrix

Branch: `work/animo-tq01-testcase-qualification`

Source head: `52411b9d2d6d80717914bc6642544290a54ded21`

Repository: `abhedwig-cell/ANIMO5`

## Purpose

Build a source-bound, evidence-level-aware qualification inventory for the nine supplied historical testcase directories in `ANIMO_testbank.zip`.

This work unit follows the canonical ANIMO5 B0-B4 evidence model. In particular:

- B0 testcase bytes are provenance/input evidence only;
- B1 successful GNU diagnostic execution is observation, not historical reference;
- synthetic probes may establish reachability, causality, conservation, non-interference or bounds behaviour, but are not B2 historical reference;
- test success does not itself establish qualification.

## Frozen identities

- source: `ANIMO_4.1.5.53(3).zip`
  - SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank: `ANIMO_testbank.zip`
  - SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- ANIMO 4.0 user's guide:
  - SHA-256 `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`

## Hard boundaries

This work unit SHALL NOT:

- modify frozen testcase bytes;
- silently repair a historical testcase;
- classify a compatibility transform as B0;
- classify a synthetic case as historical B2 reference;
- infer branch execution from successful process termination alone;
- establish numerical tolerances;
- admit production migration;
- promote B1 diagnostic output to B2.

## Required outputs

- `docs/testing/ANIMO_TESTCASE_LINEAGE.md`
- `docs/testing/PROCESS_COVERAGE_MATRIX.csv`
- `docs/testing/OPTION_COVERAGE_MATRIX.csv`
- `docs/testing/SYNTHETIC_CASE_EVIDENCE_POLICY.md`
- `docs/testing/GHGMAIS_LINEAGE_ASSESSMENT.md`
- `integration/animo-testing/ANIMO-TQ01_STATUS.json`

## Qualification target

The maximum preparatory decision for this work unit is:

`QUALIFIED_TESTCASE_LINEAGE_AND_PROCESS_COVERAGE_PREPARATORY_EVIDENCE`

with `historical_reference_qualified=false` unless an independent B2 reference has actually been admitted by PREP02R or another explicitly governed work unit.

Production migration remains `NOT_ADMITTED`.
