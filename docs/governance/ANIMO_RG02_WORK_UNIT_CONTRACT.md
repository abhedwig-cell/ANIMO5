# ANIMO-RG02 — Evidence Branch Convergence, Authority Resolution & Canonical Integration Planning

Status: `IN_PROGRESS_INVENTORY_PERSISTED_NO_INTEGRATION_ACTIONS`.

## Purpose

Resolve repository-level branch authority and integration ordering for the existing ANIMO5 evidence, theory, qualification, B3 and architecture branches without reinterpreting scientific findings.

## Starting point

Repository: `abhedwig-cell/ANIMO5`

RG02 branch: `work/animo-rg02-branch-authority-integration`

Exact governance parent: ANIMO-RG01 closeout `662bca8aff40f4dca1f6ccdde6bef6274c6bede2`.

Canonical evidence semantics are inherited from ANIMO-EB01: B0 immutable historical artifact evidence, B1 reproducible diagnostic legacy observation, B2 independent historical behavioural reference, B3 qualified scientific legacy baseline, B4 admitted canonical ANIMO5 baseline.

## Scope

RG02 may:

- inventory live `work/animo-*` and `baseline/*` refs;
- inspect ancestry, qualification/status artifacts, CI, PR and issue context;
- classify each branch as authoritative, supplemental evidence, superseded/do-not-merge, or unresolved/reconciliation-required;
- identify canonical-artifact collisions and forbid silent last-writer-wins integration;
- define one authoritative branch per workunit identifier;
- define ownership for canonical discrepancy, B3, governance and architecture registers;
- define an explicit integration DAG and consolidation prerequisites.

RG02 must not:

- modify frozen legacy source or supplied testcases;
- reinterpret, correct or replace scientific findings;
- change physics or numerical policy;
- admit corrected legacy;
- admit B3 or B4 behaviour;
- perform production migration;
- infer authority from branch naming alone.

## Authority evidence order

Branch authority is determined from the strongest available combination of:

1. explicit later reconciliation or supersession records;
2. qualification/status artifacts and persisted closeout identity;
3. exact ancestry and downstream consumption;
4. active PR/issue role and review surface;
5. CI/check evidence tied to the candidate head;
6. artifact collision analysis.

Names such as `final`, `copy`, `review`, `shadow`, `temp`, `candidate` and `authoritative` are only labels until corroborated by the evidence above.

## Fail-closed integration rule

Any branch that contains a unique scientific/evidence artifact but collides with an authoritative workunit identifier or canonical register is not silently discarded and is not directly merged. Its unique evidence must first be transplanted or reconciled through an explicitly numbered consolidation workunit.

## Non-admissions

`scientific_baseline_changed=false`

`corrected_legacy_admitted=false`

`production_migration_admitted=false`
