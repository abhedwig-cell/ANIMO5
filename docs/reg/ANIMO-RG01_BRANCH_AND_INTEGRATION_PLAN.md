# ANIMO-RG01 branch and integration plan

Status: `PERSISTED_BRANCH_DECISION_PRODUCTION_MIGRATION_NOT_ADMITTED`.

Baseline evidence head: `9df84bd0ab9bc4ef8e214f01da616aa257a24b13`.

Baseline anchor branch: `baseline/animo-prep01-05-evidence`.

RG01 branch: `work/animo-rg01-baseline-stabilization`.

## Baseline boundary

The exact PREP01-PREP05 evidence baseline is commit `9df84bd0ab9bc4ef8e214f01da616aa257a24b13`. It contains the final observed PREP05 cross-species symmetry evidence. PREP06 reservation/checkpoint files are also present because the reservation was interleaved on the shared bootstrap lineage before the last PREP05 audit commits. PREP06 execution is not part of the PREP01-PREP05 baseline qualification scope.

The baseline anchor is a historical pointer, not proof of controlled immutable B0 retention. GitHub branch protection is not currently enabled, so process discipline must not be described as technical immutability.

## Forward branch policy

`work/animo-prep01-bootstrap` is no longer the default parent for new work.

New work units must branch from an explicit admitted or preparatory anchor and declare that parent SHA in their work-unit contract. Until a later integration baseline is admitted, source-bound preparatory work may use the final ANIMO-RG01 stabilization head as its parent. No work unit may infer production admission from ancestry alone.

Recommended branch families:

- `baseline/*`: pinned evidence or admitted integration anchors; no feature development;
- `work/animo-prep*`: one preparatory audit or reference-qualification work unit per branch;
- `work/animo-cl*`: corrected-legacy qualification work, only after its source/reference gate permits it;
- `work/animo-pm*`: production migration, prohibited until corrected-legacy and migration-baseline admission;
- `work/animo-rg*`: governance, integration and baseline control.

Parallel branches must have disjoint semantic ownership. Shared state architecture, time/transaction semantics, mass-accounting contracts, exchange contracts and numerical policy remain serial-owner surfaces.

## PR #1 decision

PR #1 is mechanically mergeable, but it is not governance-ready for merge as currently described. Its title is PREP01-specific while its live head contains PREP01 through PREP05 evidence plus a PREP06 reservation. It has 161 commits and 116 changed files. The current main branch and bootstrap branch are both unprotected and have no required status checks. The Status A/AA gap register also contains stale PREP01-era evidence descriptions.

Do not merge PR #1 as-is. Do not retrospectively split or rewrite its 161-commit evidence history merely to obtain smaller PRs. That would add provenance risk without changing the scientific qualification boundary.

After RG01 metadata reconciliation is persisted, close PR #1 unmerged as superseded and use an accurately scoped RG01 preparatory-baseline PR for any later integration into `main`. Such an integration PR remains preparatory evidence only. It must not claim reference admission, corrected-legacy admission or production-migration admission.

## Integration policy

Merging preparatory metadata into `main` is a repository-governance action, not a scientific qualification event. A future merge is allowed only when the PR scope, evidence identities, open blockers and non-admission statements are internally consistent and the intended merge policy is explicit. RG01 itself performs no production migration and no corrected-legacy source admission.
