# ANIMO-PREP08 — Restart & State Continuity Audit

Status: `WORK_UNIT_RESERVED_SOURCE_BOUND_AUDIT_ONLY`.

## Purpose

Establish the revision-53 restart and state-continuity contract before ANIMO5 state ownership or transactional stepping is designed.

The audit asks which dynamic quantities are:

- read from legacy initial/restart input;
- copied from accepted state to next-step working state;
- written back to restart output;
- reconstructed rather than persisted;
- omitted or asymmetrically represented across those boundaries.

## Starting point

Exact parent PREP07 closeout:

`aefdbbcbd7aaac121831cf2dd522a152260594d0`

Frozen evidence identities remain unchanged.

## Scope

Allowed:

- source-bound parsing of initialization, state-copy and restart-output paths;
- machine-readable state continuity inventory;
- symmetry tests across read/copy/write boundaries;
- controlled diagnostic restart probes using temporary execution copies if needed;
- architecture requirements for accepted/trial/restart state ownership.

Not allowed:

- modifying frozen legacy source or supplied testcase artifacts;
- redefining scientific initialization policy;
- introducing new time integration;
- production process migration;
- treating deterministic GNU execution as historical reference truth.

## Primary source surfaces

Initial targets include:

- `input1.for` / initial-condition parsing;
- `Inicalc.for`;
- `Init.for`;
- `Output_Init.for`;
- state/result pairs such as `Co/Rsco`, `Ex/Rsex`, `Huex/Rshuex`, `Huos/Rshuos`, sorption stores, stable dissolved-organic states and mineral solutes.

## Confirmation discipline

A source asymmetry is not automatically a defect. Some values are intentionally derived from authoritative state or parameters. Every candidate must be classified as one of:

- persisted dynamic state;
- derived state;
- diagnostic/output-only state;
- parser compatibility field;
- unresolved ownership ambiguity;
- causally confirmed restart/state-continuity defect.

## Architectural objective

ANIMO5 must eventually have an explicit distinction between:

- immutable configuration;
- committed dynamic state;
- trial/working state;
- derived/cache state;
- restart serialization;
- diagnostics.

PREP08 provides evidence for that design but does not implement it.

Production migration remains `NOT_ADMITTED`.
