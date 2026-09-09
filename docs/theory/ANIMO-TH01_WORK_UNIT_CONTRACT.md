# ANIMO-TH01 — Revision-53 Theory, Extension Provenance & Scientific Intent Qualification

Status: `IN_PROGRESS_SOURCE_BOUND_THEORY_PROVENANCE_AUDIT`

## Purpose

Build an explicit theory and provenance inventory for ANIMO 4.1.5 revision 53, with special attention to functionality not fully covered by the supplied ANIMO 4.0 User's Guide.

This work unit reconstructs evidence and scientific intent. It does not invent missing theory, modify the frozen source, patch legacy defects, change numerical policy, or admit ANIMO5 production migration.

## Source-bound identities

Frozen source archive:

- artifact: `ANIMO_4.1.5.53(3).zip`
- SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- embedded version: `animo4.1.5`
- embedded revision: `53`

Supplied principal documentation:

- artifact: ANIMO 4.0 User's Guide, Alterra Report 224 (2005)
- SHA-256: `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`

Evidence-governance base:

- branch: `work/animo-eb01-evidence-baseline-model`
- starting head: `52411b9d2d6d80717914bc6642544290a54ded21`
- canonical document: `docs/governance/ANIMO5_EVIDENCE_BASELINE_MODEL.md`

Additional source-bound preparatory evidence is read from its owning branches without composing production code. In particular PREP06 is pinned to:

- branch: `work/animo-prep06-conserved-state-ledger`
- observed head at TH01 start: `9b1f1ea51c24fb82823290193651830dc61ea3c8`

## Evidence classes

TH01 uses these evidence classes:

- `AUTHORITATIVE_VERSION_SPECIFIC_THEORY`
- `AUTHORITATIVE_INHERITED_ANIMO40_THEORY`
- `PUBLIC_SECONDARY_MODEL_DESCRIPTION`
- `IMPLEMENTATION_DERIVED_NOT_INDEPENDENT_THEORY`
- `PROVENANCE_ONLY`
- `CONFLICTING_EVIDENCE`
- `UNRESOLVED`

Code-derived formulations remain explicitly non-independent until supported by suitable theory evidence.

## Reconciliation states

Per process or extension, TH01 will assign one of:

- `THEORY_CONFIRMED`
- `THEORY_PARTIALLY_RECONSTRUCTED`
- `CODE_DEFINED_THEORY_UNCONFIRMED`
- `THEORY_CODE_CONFLICT`
- `INSUFFICIENT_EVIDENCE`

## Minimum scope

The audit covers at least:

- greenhouse-gas functionality, including methane and nitrous oxide;
- macropore transport and storage;
- stable dissolved organic matter;
- phosphorus sorption options;
- slow Langmuir/non-equilibrium sorption;
- phosphorus transformation extensions and P-class-related policy where scientifically relevant;
- parser-visible options absent from the ANIMO 4.0 documentation.

For each relevant process the audit records governing states, fluxes, parameters, equations or transformation relations where evidence allows, conservation constraints, activation/options, temporal assumptions, units, discrepancies and B3 relevance.

## Hard rules

- no frozen source modification;
- no testcase modification;
- no corrected-legacy patch;
- no production implementation;
- no numerical-policy change;
- no physics change;
- no undocumented code behaviour promoted to intended theory;
- no public or historical source coupled to revision 53 without a defensible version or content relationship.

## B3 rule

TH01 may qualify an evidence inventory with unresolved gaps. It must not declare `QUALIFIED_REV53_THEORY` unless evidence is actually sufficient across the relevant process groups.

Production migration remains `NOT_ADMITTED`.
