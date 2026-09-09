# ANIMO-ARCH03 — Candidate MassLedger Observer Architecture

Status: `CANDIDATE_ARCHITECTURE_DESIGN_NOT_CANONICAL_MASS_GATE`.

## Purpose

Translate the source-bound conservation identities from PREP06 and the typed transfer/state ownership contracts from ARCH01/ARCH02 into one candidate MassLedger observer model for ANIMO5.

ARCH03 defines how storage, boundary transfers, internal transfers, reaction bundles and diagnostic nonclosure are observed. It does not implement production physics, change numerical policy, repair legacy defects, or admit the canonical MASS gate.

## Starting point

Parent architecture head:

`a079d93c965f6073586c55ee4b3544dd8873b723`

from `work/animo-arch02-restart-checkpoint-sufficiency`.

Evidence identities remain:

- source ZIP SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- ANIMO 4.0 documentation SHA-256 `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`.

## Inputs

Normative candidate-design inputs for this workunit are:

- `docs/prep06/PROCESS_CONSERVATION_IDENTITIES.md`;
- `integration/animo-prep/PREP06_CONSERVED_STATE_INVENTORY.csv`;
- `integration/animo-prep/PREP06_TRANSFER_LEDGER.csv`;
- `docs/arch01/STATE_OWNERSHIP_MODEL.md`;
- `docs/arch01/TYPED_TRANSFER_CONTRACT.md`;
- `integration/animo-architecture/ARCH01_STATE_OWNERSHIP.csv`;
- `integration/animo-architecture/ARCH01_TRANSFER_TYPES.csv`;
- `docs/arch02/RESTART_CHECKPOINT_MODEL.md`.

## Required design properties

The candidate MassLedger shall:

1. derive beginning and end storage from canonical owner state, never from reporting accumulators;
2. consume each admitted physical transfer event once from the typed transfer journal;
3. derive internal versus external classification from control-volume membership of event endpoints;
4. preserve conserved quantity separately from species/carrier identity;
5. represent multi-leg reactions as linked bundles with one conservation identity;
6. exclude reporting observations and unqualified numerical constraints from physical flux totals;
7. expose raw closure residuals without inventing a numerical tolerance policy;
8. distinguish physical closure from diagnostic/report-continuation state;
9. support soil-only, soil+crop and matrix+macropore control-volume views without duplicating events;
10. fail closed when state, feature, geometry, quantity, unit, journal schema or ownership identity is incompatible.

## Canonical residual convention

For conserved quantity `Q` over an observation interval and selected control volume:

`R_Q = S_end(Q) - S_begin(Q) - I_external(Q) + O_external(Q)`

A semantically closed interval has `R_Q = 0` before any later numerical tolerance policy is applied.

Internal transfers cancel by construction and therefore do not enter the profile-level residual. They may still be exposed in detailed process views.

## Hard boundaries

ARCH03 does not:

- admit ARCH01 as canonical STATE;
- define or admit generic TIME acceptance/retry semantics;
- define a numerical residual tolerance;
- claim a global elemental-carbon ledger across organic matter, crop dry matter, CO2 and CH4;
- admit GHG or macropore production behaviour;
- qualify corrected legacy behaviour;
- modify frozen legacy source or supplied testcases;
- admit production migration.

The repository migration DAG still requires qualified migration baseline `QM`, then canonical `STATE`, then `TIME`, then `MASS`.

## Qualification ceiling

The strongest allowed result is:

`QUALIFIED_CANDIDATE_MASS_LEDGER_OBSERVER_ARCHITECTURE_DESIGN`

with at least:

- `canonical_mass_gate_admitted=false`;
- `reference_qualified=false`;
- `production_implemented=false`;
- `legacy_source_modified=false`;
- `testcase_modified=false`;
- `production_migration_admitted=false`.

`persist early, test second` applies.
