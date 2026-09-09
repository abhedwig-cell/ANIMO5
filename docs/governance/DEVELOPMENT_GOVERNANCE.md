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

ANIMO-EG01 defines the controlled-retention classes used across the programme:

`B0_RAW_IMMUTABLE`, `B0_MANIFEST`, `WORKING_COPY`, `COMPATIBILITY_TRANSFORM`, `DIAGNOSTIC_OUTPUT`, `REFERENCE_OUTPUT`, `CORRECTED_LEGACY`, `MIGRATED_ANIMO5`.

The public repository may retain provenance metadata and hashes, but Git history or Git object hashes are not the sole preservation mechanism for B0. Raw B0 bytes whose redistribution basis is absent, restricted or uncertain remain outside public Git in controlled storage.

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

Controlled immutable B0 retention is an explicit gate. A B0 blocker may not be lifted merely because an artifact hash or manifest exists in Git. The exact raw bytes must be retained under an authorized storage authority with write protection, access control, independently recoverable backup, post-ingest checksum verification and a demonstrated restore/revalidation path.

Compatibility transforms must receive their own identity and digest, record their parent B0 identity and transformation recipe/tool, and must never replace or inherit the raw B0 identity.

Every persisted diagnostic, reference, corrected-legacy or migrated run that can influence scientific qualification must record machine-readable input lineage. `REFERENCE_OUTPUT` requires a dedicated admission gate; diagnostic output is not promoted by naming convention or test success alone.

## Scientific change rule

No discrepancy is silently fixed. Every theory/documentation/code difference is registered and classified before adoption.
