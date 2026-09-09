# ANIMO5 development governance

## Evidence-first progression

The canonical evidence and baseline terminology is defined in:

`docs/governance/ANIMO5_EVIDENCE_BASELINE_MODEL.md`

The project progression is:

```text
B0 historical artifact baseline
        -> B1 reproducible diagnostic legacy observation
        -> B2 independent historical behavioural reference where obtainable
        -> reconciliation and explicit discrepancy disposition
        -> B3 qualified scientific legacy baseline
        -> ANIMO5 architecture and process migration
        -> B4 ANIMO5 canonical admission baseline
        -> Status A
        -> continued scientific maturation
        -> Status AA
```

B1 and preparation of B3 evidence may proceed while B2 acquisition remains open. Production migration may not treat unresolved B1 observations as B2 or B3 evidence.

A corrected legacy reference is behavioural evidence. It is not automatically proof of agreement with model theory.

## Baseline semantics

The following implications are prohibited:

- reproducible does not imply reference;
- reference does not imply scientifically correct;
- diagnostic defect causality does not imply corrected-legacy admission;
- corrected-legacy admission does not imply ANIMO5 migration;
- tested does not imply qualified.

Every behavioural work unit must state which baseline level it uses and which conclusion that level permits.

## Evidence classes

Keep source, documentation/theory, testcase behaviour and independent historical behaviour separate until reconciliation evidence justifies a stronger claim.

B0 is immutable evidence identity. B1 is diagnostic observation. B2 is independent historical behaviour. B3 is explicitly reconciled scientific legacy behaviour. B4 is the admitted modern canonical implementation.

## Work-unit contract

Every medium work unit must declare before modification:

- intended change;
- affected components;
- physics change yes/no;
- numerical-policy change yes/no;
- expected differences;
- verification contract;
- checkpoint boundary;
- qualification requirement;
- baseline level used for evidence and comparison.

## Persistence rule

Use:

```text
useful work -> cheap checks -> persist to Git -> expensive operation
```

Every work unit reports separately:

`IMPLEMENTED`, `PERSISTED`, `TESTED`, `QUALIFIED`, `BLOCKED`.

A test pass does not silently imply qualification.

## Parallelism rule

`parallel where ownership is disjoint, serial where semantics are shared`.

Parallel work may target documentation analysis, test tooling, interface audit, testcase qualification, process inventory, historical reference recovery, conserved-state/transfer-ledger audits, or Status A/AA gap analysis when files/ownership do not overlap.

Shared semantic foundations such as canonical state architecture, time contract, transaction semantics, mass accounting, exchange interfaces, numerical policy, precision policy, common process ordering and B3 admission require serial ownership/gates.

## Frozen legacy rule

Frozen source, documentation, and testcase artifacts are immutable B0 evidence. Corrections are separate descendants with explicit rationale and tests.

Compatibility transforms, diagnostic builds, generated output and corrected source never replace B0.

## Scientific change rule

No discrepancy is silently fixed. Every theory/documentation/code difference is registered and classified before adoption.

For a closed physical conservation identity, historical numerical agreement is not by itself sufficient justification to preserve a causally demonstrated mass creation, destruction, duplication, cross-species transfer or omitted storage term. Such corrections still require explicit B3 admission.

Changes to nonlinear solvers, tolerances, linearisations, convergence criteria or precision policy require separate numerical qualification and are not reduced to bookkeeping fixes solely because a residual improves.

Physics changes require explicit scientific admission and are not silently folded into corrected legacy.

## Historical-reference fallback

Failure to recover an exact historical executable must be recorded, but it does not make scientific qualification permanently impossible.

After a documented reasonable acquisition effort, a process-scoped B3 item may use the `INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY` route defined by the canonical evidence model. This requires stronger source, theory/conservation, test, expected-difference, non-interference and review evidence. It cannot waive uncertainty for poorly documented physics or broad numerical-policy changes.
