# ANIMO-PREP07 — Cross-Species Transfer & Ledger Identity Audit

Status: `WORK_UNIT_RESERVED_SOURCE_BOUND_AUDIT_ONLY`.

## Purpose

Systematically audit the frozen ANIMO 4.1.5 revision-53 source for cross-species, cross-pool and wrong-ledger bindings in C/N/P process and transfer calculations.

PREP07 generalizes the defect pattern already demonstrated by TCD-023. It does not assume every mixed C/N/P expression is wrong. A candidate is promoted only when source semantics, units, symmetry or a causal execution probe demonstrate that the binding is inconsistent.

## Starting point

Exact parent closeout:

`fe832c15692768b94869235e4ea53065682189b9`

from `work/animo-prep06-conserved-state-ledger`.

Frozen evidence identities remain unchanged:

- source ZIP SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

## Scope

Allowed:

- static source analysis;
- machine-readable symbol/species inventory;
- unit and species-identity checks;
- comparison of C/N/P analogue formulas;
- controlled synthetic or natural-case diagnostic probes in temporary copies;
- documentation and qualification tooling.

Not allowed:

- changing frozen reference source or supplied testcase artifacts;
- broad physics cleanup;
- admitting corrected-legacy behaviour without historical reference qualification;
- production migration.

## Candidate classes

Audit candidates include:

1. N-derived variables used in P equations or vice versa without an explicit stoichiometric conversion;
2. C/N/P analogue arrays indexed into the wrong species family;
3. process-output or balance slots populated from a different species or pool;
4. transformed mass fractions whose dimensions or stoichiometry do not match the target ledger;
5. parameter arrays bound to the wrong conserved constituent.

Intentional stoichiometric coupling is not a discrepancy. The audit must distinguish explicit conversion from accidental cross-species reuse.

## Confirmation threshold

A finding may be classified as confirmed only with at least one of:

- exact algebraic contradiction with the source's own C/N/P analogue formulas;
- dimensional/species inconsistency with no explicit conversion factor;
- causal diagnostic probe changing only the suspected binding and demonstrating the predicted local ledger or trajectory effect;
- independently documented theory showing the binding is wrong.

## Governance

`persist early, test second` applies.

Keep separate:

- source suspicion;
- causally confirmed legacy defect;
- corrected-legacy candidate;
- reference-qualified correction.

PREP07 is source-bound qualification work only.

Production migration remains `NOT_ADMITTED`.
