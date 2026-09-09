# ANIMO-ARCH04 — Feature Activation & State Allocation Architecture

Status: `CANDIDATE_ARCHITECTURE_WORK_UNIT`.

## Purpose

Define a fail-closed candidate architecture for feature activation, state allocation and layout identity using the qualified preparatory and candidate-design evidence from PREP06 and ARCH01–ARCH03.

ARCH04 answers a narrow question: given one model configuration, which state owners, derived views, scratch spaces and diagnostic observers are present, who owns them, and which dimensions determine their layout?

It does not implement production state, activate blocked legacy features, or admit the canonical STATE/TIME/MASS gates.

## Starting point

Exact parent candidate-design closeout:

`bc27bd7cf0c8148b38768315d2fa54014f5a6cf9`

from `work/animo-arch03-mass-ledger-observer`.

Frozen evidence identities remain unchanged:

- source ZIP SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- ANIMO 4.0 User Guide SHA-256 `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`.

## Inputs

ARCH04 consumes, but does not supersede:

- PREP06 conserved-state and transfer-ledger evidence;
- ARCH01 state ownership and typed transfer design;
- ARCH02 restart/checkpoint candidate design;
- ARCH03 MassLedger observer candidate design;
- open TCD evidence that constrains feature admission.

## Required outputs

1. feature registry with activation/admission semantics;
2. exact 53-family allocation projection from ARCH01;
3. feature interaction/dependency matrix;
4. feature-layout identity and compatibility contract;
5. fail-closed structural audit and machine-readable status.

## Architecture rules

1. Inactive optional functionality must not silently retain physical state ownership.
2. Derived views are recomputed or allocated ephemerally and are not continuation state.
3. Step-local scratch is allocated only for an active process path and is never checkpoint state.
4. Diagnostic observers are allocated independently from physical state.
5. Externally owned hydrology or crop state is not duplicated as hidden persistent ANIMO state.
6. Site-resolved state dimensions are explicit layout dimensions, not inferred from derived totals.
7. A parser-visible feature is not automatically a supported runtime feature.
8. Feature combinations that violate an ownership, geometry, qualification or state-layout contract fail closed.
9. A layout identity must be sufficient to reject incompatible checkpoint restore or state exchange.
10. Feature activation may change allocation and event topology, but may not silently change scientific equations or numerical policy.

## Hard boundaries

ARCH04 does not:

- change the frozen legacy source;
- change supplied testcases;
- define production memory layout or language-specific structs;
- define precision or numerical tolerances;
- qualify GHG theory-to-ledger closure;
- activate macropores without an admitted active case;
- promote dormant stable surface DOM/DON/DOP into supported state;
- repair multi-site phosphorus behaviour;
- admit corrected legacy behaviour;
- admit canonical STATE, TIME or MASS;
- implement production migration.

## Qualification class

Maximum decision for this workunit:

`QUALIFIED_CANDIDATE_FEATURE_ACTIVATION_AND_STATE_ALLOCATION_ARCHITECTURE`

with `reference_qualified=false` and `production_migration_admitted=false`.
