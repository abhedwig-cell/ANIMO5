# ANIMO5 development governance

Canonical evidence and baseline terminology is defined in:

`docs/governance/ANIMO5_EVIDENCE_BASELINE_MODEL.md`

Controlled B0 retention and run-lineage requirements are defined in:

`docs/eg01/B0_RETENTION_AND_LINEAGE_POLICY.md`

Branch authority and integration ownership are defined in:

`docs/governance/ANIMO_BRANCH_AUTHORITY_MODEL.md`

## Evidence-first progression

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
- tested does not imply qualified;
- a branch name does not imply authority;
- a local discrepancy number does not imply canonical allocation.

Every behavioural work unit must state which baseline level it uses and which conclusion that level permits.

## Evidence classes and retention

B0 is immutable historical evidence identity. B1 is diagnostic observation. B2 is independent historical behaviour. B3 is explicitly reconciled scientific legacy behaviour. B4 is the admitted modern canonical implementation.

EG01 additionally distinguishes retained and derived evidence classes:

`B0_RAW_IMMUTABLE`, `B0_MANIFEST`, `WORKING_COPY`, `COMPATIBILITY_TRANSFORM`, `DIAGNOSTIC_OUTPUT`, `REFERENCE_OUTPUT`, `CORRECTED_LEGACY`, `MIGRATED_ANIMO5`.

These classes refine provenance and storage handling. They do not replace the B0 to B4 baseline hierarchy.

Public Git may retain provenance metadata and hashes, but Git history or Git object hashes are not the sole preservation mechanism for B0. Raw B0 bytes whose redistribution basis is absent, restricted or uncertain remain outside public Git in controlled storage.

Controlled immutable B0 retention is an explicit gate. A B0 blocker may not be lifted merely because an artifact hash or manifest exists in Git. The exact raw bytes must be retained under an authorized storage authority with write protection, access control, independently recoverable backup, post-ingest checksum verification and a demonstrated restore/revalidation path.

Compatibility transforms receive their own identity and digest, record their parent B0 identity and transformation recipe or tool, and never replace or inherit the raw B0 identity.

Every persisted diagnostic, reference, corrected-legacy or migrated run that can influence scientific qualification must record machine-readable input lineage. `REFERENCE_OUTPUT` requires a dedicated admission gate; diagnostic output is not promoted by naming convention or test success alone.

Actual controlled immutable storage is not proven merely because the EG01 contract and proof gate are present in the repository.

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
- baseline level used for evidence and comparison;
- work-unit identifier and authoritative branch ownership.

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

Parallel work may target documentation analysis, test tooling, interface audit, testcase qualification, process inventory, historical reference recovery, conserved-state/transfer-ledger audits, or Status A/AA gap analysis when files and semantic ownership do not overlap.

Shared semantic foundations such as canonical state architecture, time contract, transaction semantics, mass accounting, exchange interfaces, numerical policy, precision policy, common process ordering, cross-stream governance files and B3 admission require serial ownership and explicit gates.

## Branch and canonical-artifact ownership

From RG02 onward:

1. one work-unit identifier has one authoritative branch;
2. parallel experiments use an explicit supplemental/candidate identity or a new work-unit identifier;
3. branch suffixes such as `final`, `review`, `copy`, `shadow`, `temp`, `candidate` or `authoritative` do not establish authority;
4. superseded branches are retained as evidence but are not integration surfaces;
5. cross-stream canonical files have one designated owner;
6. canonical TCD allocation is owned by B3 governance from the qualified B3Q01 tail onward;
7. preparatory branches may retain historical local identifiers as provenance, but may not allocate project-canonical IDs;
8. direct branch merges are prohibited when both branches mutate a same-path canonical register or a same-workunit status artifact;
9. supplemental evidence is transplanted path-by-path with source branch, head and blob provenance;
10. silent last-writer-wins integration is prohibited.

The machine-readable authority and local-ID reconciliation records are under `integration/animo-reg/`.

## Frozen legacy rule

Frozen source, documentation and testcase artifacts are immutable B0 evidence. Corrections are separate descendants with explicit rationale and tests.

Compatibility transforms, diagnostic builds, generated output and corrected source never replace B0.

## Scientific change rule

No discrepancy is silently fixed. Every theory/documentation/code difference is registered and classified before adoption.

For a closed physical conservation identity, historical numerical agreement is not by itself sufficient justification to preserve a causally demonstrated mass creation, destruction, duplication, cross-species transfer or omitted storage term. Such corrections still require explicit B3 admission.

Changes to nonlinear solvers, tolerances, linearisations, convergence criteria or precision policy require separate numerical qualification and are not reduced to bookkeeping fixes solely because a residual improves.

Physics changes require explicit scientific admission and are not silently folded into corrected legacy.

## Historical-reference fallback

Failure to recover an exact historical executable must be recorded, but it does not make scientific qualification permanently impossible.

After a documented reasonable acquisition effort, a process-scoped B3 item may use the `INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY` route defined by the canonical evidence model. This requires stronger source, theory or conservation, test, expected-difference, non-interference and review evidence. It cannot waive uncertainty for poorly documented physics or broad numerical-policy changes.

## Production boundary

Repository convergence, governance consolidation, successful CI, candidate architecture completeness or B1 causal evidence do not by themselves admit B3, B4 or production migration.

`scientific_baseline_changed=false` for governance-only convergence.

`corrected_legacy_admitted=false` unless a separate B3 admission explicitly says otherwise.

`production_migration_admitted=false` until the applicable B3, architecture and B4 gates are explicitly satisfied.
