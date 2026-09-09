# ANIMO5 branch authority model

Work unit: `ANIMO-RG02`

Status: `BLOCKED_UNRESOLVED_PARALLEL_LINEAGE_COLLISIONS`

This document governs repository integration only. It does not reinterpret scientific findings and does not admit corrected legacy behaviour, B3, B4 or production migration.

## 1. Authority rule

A branch name is not evidence of authority. RG02 assigns authority from persisted work-unit status, exact ancestry, later reconciliation, downstream consumption, PR context and CI evidence tied to a known head.

For every work-unit identifier, one branch may be the integration authority. Other branches are classified as one of:

- `SUPPLEMENTAL_EVIDENCE`: unique evidence may be retained, but the branch is not merged wholesale into the canonical line.
- `SUPERSEDED_DO_NOT_MERGE`: the branch is redundant, explicitly superseded, or an obsolete review/copy/shadow surface.
- `UNRESOLVED_REQUIRES_RECONCILIATION`: no safe integration decision can yet be made without an explicit consolidation step.

Authority is scoped. A branch can be authoritative for its own evidence or candidate design without being authoritative for B3, B4, production physics or numerical policy.

## 2. High-confidence authority decisions

| Work unit | Authoritative branch or anchor | Disposition | Basis |
| --- | --- | --- | --- |
| PREP01 to PREP05 baseline | `baseline/animo-prep01-05-evidence` @ `9df84bd0ab9bc4ef8e214f01da616aa257a24b13` | AUTHORITATIVE_BASELINE_ANCHOR | Frozen stabilized evidence snapshot; PR #1 is closed and superseded by RG01 |
| RG01 | `baseline/animo-rg01-preparatory-stabilized` and matching work head `662bca8aff40f4dca1f6ccdde6bef6274c6bede2` | AUTHORITATIVE_GOVERNANCE_BASE | Qualified RG01 closeout and active PR #3 |
| EB01 | `work/animo-eb01-evidence-baseline-model` @ `52411b9d2d6d80717914bc6642544290a54ded21` | AUTHORITATIVE | Canonical B0 to B4 model and PR #6; copy/pr/review refs are byte-identical aliases |
| EG01 | `work/animo-eg01-controlled-b0-retention` @ `a818b5a37b80ed92aded0b9c404990d356eb2300` | AUTHORITATIVE | Dedicated B0 retention work unit and PR #4 |
| PREP02R | `work/animo-prep02r-historical-reference-recovery` @ `e29aa75f782a17e1cca6b0c2791ba04077e8bde7` | AUTHORITATIVE_BLOCKED | Persisted status says historical reference artifact not yet obtained |
| PREP06 | `work/animo-prep06-conserved-state-ledger` @ `9b1f1ea51c24fb82823290193651830dc61ea3c8` | AUTHORITATIVE | Qualified conserved-state and transfer-ledger evidence; used by NQ, ARCH and later qualification lines |
| PREP07 | `work/animo-prep07-transfer-edge-audit` @ `c4fe28b7878f6e8155560754b87b7ae115dd6473` | AUTHORITATIVE_FOR_IDENTIFIER | Qualified status and downstream ancestry into PREP08 transfer probes, PREP09 element-transfer and the active PREP10 stable-DOM lineage |
| PREP08 | `work/animo-prep08-causal-management-probes` @ `933795e2e9bf72a78b5fcf5412510f057d0ab869` | AUTHORITATIVE_FOR_IDENTIFIER | Substantive qualified causal work; later PREP09 option audit explicitly records PREP08 as consumed by management causal probes |
| PREP09 | `work/animo-prep09-element-transfer-and-slow-sorption` @ `e3c3b0dfa8daabe345c51be8c4f29f2731d65c47` | AUTHORITATIVE_FOR_IDENTIFIER | Qualified evidence and explicit base of active PREP10 PR #9 and its downstream B3 intake |
| PREP10 | `work/animo-prep10-stable-dom-plough-accumulators` @ `65cd4a65a3ea27cd4ce004f505d5022fdb08b9ab` | AUTHORITATIVE_FOR_IDENTIFIER | PR #9 is the active review surface; later PREP10C and B3 intake explicitly use this lineage |
| PREP10C | `work/animo-prep10c-stable-dom-event-reset-authoritative` @ `549545921dc8175f01d86c283647acd470c14290` | AUTHORITATIVE_REVIEW_SURFACE | PR #14 explicitly re-anchors PREP10C on authoritative PREP10 and supersedes older PREP10C histories |
| NQ01 | `work/animo-nq01-numerical-qualification-architecture` @ `e558dff12b127e0662cad62beea7527b42ad89ac` | AUTHORITATIVE | Active branch is 33 commits ahead of stale alias head `438a883...` and carries the latest persisted NQ01 qualification architecture |
| TQ01 | `work/animo-tq01-testcase-qualification` @ `5c43ee16df37a0a1357614fdec527f25e5ca8c16` | AUTHORITATIVE | Primary branch and PR #15 are 10 commits strictly ahead of all shadow refs |
| TH01 | `work/animo-th01-rev53-theory-provenance` @ `a3360415364ef4a66a81d7b6715bcd400829df1b` | AUTHORITATIVE | Qualified theory/provenance review surface, PR #13 |
| TH02 | `work/animo-th02-rev41-lineage-recovery` @ `f7f3722b14f65340dc6d67a8f80d74f5d0ebb158` | AUTHORITATIVE | PR #16; eight commits ahead of the no-op TH02 release-lineage ref |
| B3Q01 | `work/animo-b3q01-scientific-admission-framework` @ `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54` | AUTHORITATIVE_FRAMEWORK | Qualified B3 governance, no corrected legacy admitted |
| B3A01 | `work/animo-b3a01-tcd027-class-a-readiness` @ `b2bac82512fef0fa232e759f0c68b472567c11d5` | AUTHORITATIVE_FOR_B3A01_ONLY | Seven commits cleanly ahead of B3Q01, readiness only |
| TCD028 B3 intake | `work/animo-b3-tcd028-stable-dom-intake` @ `7f38b79d88c05fd86c89fbdd7a5794b90ffba2bf` | AUTHORITATIVE_RESERVATION_FOR_TCD028 | PR #10 reserves canonical TCD-028 without admitting it or appending a corrected baseline |
| ARCH01 to ARCH07 | their named `work/animo-arch0x-*` branches | AUTHORITATIVE_CANDIDATE_DESIGN_PER_WORKUNIT | Sequential qualified candidate architecture; every status explicitly says canonical gates and production remain unadmitted |
| GHG01 | `work/animo-ghg01-ghg-qualification` @ `33b9941f7de80a67df08d8b6a75c2a12921019fe` | AUTHORITATIVE_IN_PROGRESS | Own persisted status; based on TH02 |
| SQ01 | `work/animo-sq01-tcd016-dry-solute-state` @ `3763abf7f9aba46e185d791c6617ef64301bb96d` | AUTHORITATIVE_IN_PROGRESS | Own persisted status; explicitly based on B3Q01 and treats parallel theory/prep branches as pinned evidence |
| TS01 | `work/animo-ts01-temporal-semantics` @ `9a85f84aaf422dd1a590c6f42a250be15a142984` | AUTHORITATIVE_IN_PROGRESS | Own persisted source-bound status; based on PREP06 |
| RG02 | `work/animo-rg02-branch-authority-integration` | AUTHORITATIVE_IN_PROGRESS | Dedicated branch created from exact RG01 closeout |

`work/animo-archg01-candidate-architecture-consolidation` currently points exactly at the ARCH07 head and has no independent persisted ARCHG01 status at the observed snapshot. `work/animo-mp01-macropore-qualification` likewise points at the TH02 head. They are reservations, not authority established by name. They remain `UNRESOLVED_REQUIRES_RECONCILIATION` until they acquire an explicit contract/status or are deliberately retired.

## 3. Duplicate lineage dispositions

### PREP07

`work/animo-prep07-transfer-edge-audit` and `work/animo-prep07-transfer-species-identity` diverge. Both contain substantive persisted evidence. The transfer-edge line is authoritative for the PREP07 identifier because it is the qualified ancestor consumed by the downstream PREP08/PREP09/PREP10 chain. The species-identity line is `SUPPLEMENTAL_EVIDENCE`. It must be transplanted as a separately identified evidence packet before any canonical consolidation. It must not be merged wholesale into PREP07.

### PREP08

`work/animo-prep08-causal-management-probes` is authoritative for PREP08. `work/animo-prep08-transfer-probes` is `SUPPLEMENTAL_EVIDENCE` because it contains unique diagnostic work on the transfer-edge lineage. `work/animo-prep08-restart-state-continuity` is only a reservation and is `SUPERSEDED_DO_NOT_MERGE`; the later option-audit closeout explicitly says restart/state continuity must receive a new work-unit number.

### PREP09

The element-transfer/slow-sorption and option-contract branches diverge and both are qualified. The element-transfer branch is authoritative for PREP09 because the active PREP10 and B3 chain consumes it. The option-contract branch is `SUPPLEMENTAL_EVIDENCE_RENUMBER_REQUIRED`. Its parser-option audit is not discarded, but it may not overwrite the PREP09 status artifact or its local TCD numbering during consolidation.

### PREP10

The stable-DOM plough-accumulator branch is authoritative. The causal-activation branch is `SUPPLEMENTAL_EVIDENCE_ALREADY_RECONCILED`; PR #7 is closed and its evidence is explicitly pinned by the later PREP10 reconciliation artifact. The restart-state-continuity branch is `SUPPLEMENTAL_EVIDENCE_RENUMBER_AND_TCD_RECONCILE_REQUIRED`. It contains unique restart findings but reused PREP10 after the identifier had already acquired an authoritative stable-DOM lineage. It must not be merged as PREP10.

### PREP10C

The re-anchored event-reset branch is authoritative for PREP10C review. The old candidate branch is `SUPERSEDED_DO_NOT_MERGE` after PR #11 was closed and replaced by PR #14. The reset-readiness branch is also `SUPERSEDED_DO_NOT_MERGE` as PREP10C. Its provisional `TCD-032` is not a canonical TCD ID.

### NQ01

The active numerical-qualification-architecture branch is authoritative. `final`, `ignore`, `copy`, `packet-temp` and `stop` all point at the same older head `438a8838731208d19f8fe158254054b9ac2f5b33`, which is an ancestor of the active line. They are `SUPERSEDED_DO_NOT_MERGE` aliases. Their content is already contained in the authoritative NQ01 ancestry.

### TQ01

The primary branch is strictly ahead of the common shadow head. All three shadow refs are `SUPERSEDED_DO_NOT_MERGE` aliases.

### EB01

Primary, copy, PR and review refs point to the same commit. The primary branch is authoritative because it owns the canonical document and PR #6. The other three refs are `SUPERSEDED_DO_NOT_MERGE` aliases, not separate evidence streams.

### TH02

`work/animo-th02-release-lineage-recovery` is still at the TH01 head and has no TH02 work. `work/animo-th02-rev41-lineage-recovery` is eight commits ahead and is PR #16. The latter is authoritative. The former is `SUPERSEDED_DO_NOT_MERGE`.

## 4. Canonical register ownership

### Theory/code discrepancy IDs

The last cross-stream canonical discrepancy register accepted by the B3 governance line is the B3Q01 snapshot through `TCD-027`. B3Q01 records the canonical register blob as `224acc350fde69d3c4aebed8628c0f945e0b3367` and the tail as `TCD-027`.

Later PREP branches independently wrote local `TCD-028`, `TCD-029`, `TCD-030`, `TCD-031`, `TCD-032`, `TCD-033` and `TCD-034` labels. These labels collide across divergent branches and are not canonical merely because they are present in a CSV. PR #10 separately reserves canonical `TCD-028` for the stable-DOM B3 intake. Therefore:

- B3 governance owns canonical TCD allocation from `TCD-028` onward.
- preparatory branches may retain their historical local labels as provenance only;
- no post-027 preparatory label may be copied into the canonical register unchanged unless the B3 owner explicitly maps it;
- a reconciliation record must preserve `source_branch`, `local_id`, `canonical_id_or_unassigned`, `finding_identity_hash_or_locator` and disposition;
- silent CSV union is forbidden.

### B3 classification and disposition registers

B3Q01 owns the classification schema and the existing-TCD classification snapshot. B3A01 and individual B3 intake branches may add work-unit-local readiness/disposition artifacts, but must not silently rewrite the B3Q01 classification register. Promotion requires an explicit B3 governance update.

### Evidence baseline governance

EB01 owns the B0 to B4 semantics. RG01/RG02 own repository and integration governance. EG01 owns controlled B0 retention policy. These roles are complementary and must be integrated by explicit artifact transplant or a governance consolidation commit, not by choosing one branch as a replacement for the others.

### Migration DAG and Status A/AA registers

`docs/governance/MIGRATION_DAG.md` and `docs/quality/STATUS_A_AA_GAP_REGISTER.csv` predate several later branches. They are cross-cutting governance artifacts. From RG02 onward they must have one designated governance owner, proposed as the RG series, and changes from evidence, theory, numerical or architecture branches must arrive as reviewed proposals rather than direct parallel rewrites.

### Architecture contracts

ARCH01 through ARCH07 are authoritative candidate-design artifacts for their own work units. They are not canonical STATE, TIME, MASS or EX admission. Candidate architecture may be consolidated separately, but B3/B4 authority cannot be inferred from architectural completeness or CI success.

## 5. Branch creation policy from RG02 onward

1. One work-unit identifier has one authoritative branch.
2. A parallel experiment uses a new identifier or an explicit suffix with `candidate` or `supplemental` status recorded in a machine-readable status artifact before substantive work.
3. Reusing an existing work-unit number for a different subject is forbidden after the first authoritative work-unit closeout.
4. A status artifact must identify `branch`, `base_commit`, `decision`, `persisted`, `tested`, `qualified`, `blocked` and the non-admission flags relevant to the work unit.
5. `final`, `review`, `copy`, `shadow`, `temp`, `candidate`, `authoritative` and similar names do not confer authority.
6. Superseded branches remain immutable evidence unless deliberately deleted later. They are marked `SUPERSEDED_DO_NOT_MERGE` in the authority register.
7. Canonical register owners allocate IDs. A work unit that does not own a register may reserve a local key only, never a canonical TCD number.
8. Cross-stream canonical files use a single-owner proposal model. Parallel branches may carry proposed patches, but the owner branch performs the canonical mutation after reconciliation.
9. Direct branch merges are prohibited when both sides mutate a canonical register or a same-path status artifact for the same work-unit identifier.
10. Cherry-picks are allowed only when the selected commit has disjoint semantic ownership and does not import stale canonical-register state.

## 6. Current gate

RG02 resolves repository authority well enough to prevent accidental last-writer-wins integration, but it does not resolve the content identity of every local post-027 TCD or every duplicate PREP07 to PREP10 evidence packet. Canonical convergence is therefore blocked pending explicit consolidation.

`scientific_baseline_changed=false`

`corrected_legacy_admitted=false`

`production_migration_admitted=false`
