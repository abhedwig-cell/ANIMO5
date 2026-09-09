# ANIMO5 development governance

## Evidence-first progression

```text
frozen legacy source and documentation
        -> reproducible legacy baseline
        -> audited/corrected legacy reference
        -> qualified migration baseline
        -> ANIMO5 architecture and process migration
        -> integrated qualification
        -> Status A
        -> continued scientific maturation
        -> Status AA
```

A corrected legacy reference is behavioural evidence. It is not automatically proof of agreement with model theory.

## Evidence classes

Keep source, documentation/theory, and testcase behaviour independent until reconciliation evidence justifies a stronger claim.

## Work-unit contract

Every medium work unit must declare before modification:

- intended change;
- affected components;
- physics change yes/no;
- numerical-policy change yes/no;
- expected differences;
- verification contract;
- checkpoint boundary;
- qualification requirement.

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

Parallel work may target documentation analysis, test tooling, interface audit, testcase qualification, process inventory, or Status A/AA gap analysis when files/ownership do not overlap.

Shared semantic foundations such as canonical state architecture, time contract, transaction semantics, mass accounting, exchange interfaces, numerical policy, precision policy, and common process ordering require serial ownership/gates.

## Frozen legacy rule

Frozen source, documentation, and testcase artifacts are immutable evidence. Corrections are separate descendants with explicit rationale and tests.

## Scientific change rule

No discrepancy is silently fixed. Every theory/documentation/code difference is registered and classified before adoption.
