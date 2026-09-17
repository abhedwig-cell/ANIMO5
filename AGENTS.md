# ANIMO5 agent guide

This file is a repository entry point for coding and research agents. It is navigational. It does not replace scientific authorities, governance decisions, qualified evidence, work-unit status records, integration records, or production-admission contracts.

## Source of truth

Use repository state as authority. Chat history, local scratch notes, generated summaries, and remembered branch state are working context only.

When starting material work:

1. Read the exact target branch and HEAD commit and pin that ref for the current phase.
2. When resuming an existing work unit, read its versioned status, checkpoint, closeout, or recovery record first if the path is known. Use it as navigation to the recovery point, relevant paths and dependency surface; it is not a substitute for the owning authority.
3. Reconcile only the relevant live delta since the recorded checkpoint or reconciliation state. For current ANIMO5 scope questions, read the current regie, branch-authority, integration-DAG and evidence-model authorities before relying on older preparatory or migration material.
4. Read the relevant accepted scientific, architectural, evidence and governance capability documentation.
5. Identify the owning workstream, semantic contracts and interfaces touched.
6. State which architecture invariants, evidence classes, TCD/B3 surfaces, runtime contracts or production gates are affected.
7. Distinguish implemented, persisted, tested, reviewed, qualified, admitted, preserved and production-authoritative state.

If repository state and chat context disagree, repository state wins.

## Read first

For most work, start here:

- `docs/governance/ANIMO_GOV06_UNIFIED_PROGRAM_REGIE.md` - current unified programme-regie rules, semantic ownership, research maturity, resumption and admission separation.
- `docs/governance/ANIMO_BRANCH_AUTHORITY_MODEL.md` - branch authority and what branch state can and cannot establish.
- `docs/governance/ANIMO_CANONICAL_INTEGRATION_DAG.md` - integration ordering, authority boundaries and non-automatic merge/admission relations.
- `docs/governance/ANIMO5_EVIDENCE_BASELINE_MODEL.md` - B0-B4 evidence and production-authority semantics.
- `docs/architecture/ANIMO5_ARCHITECTURE_INVARIANTS.md` - normative ANIMO5 architecture invariants.
- `docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv` - central theory/code discrepancy evidence surface where applicable.
- `docs/quality/STATUS_A_AA_GAP_REGISTER.csv` - current Status-A/AA gap evidence; absence from a denominator is not automatically a defect.
- `docs/testing/TEST_ARCHITECTURE.md` - test architecture and evidence roles.
- `PROVENANCE.md` - repository and supplied-evidence provenance boundary.

Then read the work-unit-specific contract, status, checkpoint, reconciliation, review, qualification and closeout files for the change being made.

Older preparatory, local-TCD, target-architecture, migration and branch-local status artifacts remain valid only for their recorded scope. They must not override later qualified governance, aggregate, B3, integration or production authorities for present-state claims.

## Hard rules

- Do not invent current state from filenames, chat summaries, branch names, open PR titles or remembered SHAs. Re-read the repository.
- Do not treat target architecture, a branch head, a successful diagnostic run or a local status file as proof of canonical admission or production authority.
- Do not silently change a shared semantic contract. Record ownership, authority and the design or scientific decision first when required.
- Preserve the separation between B0 historical artifact identity, B1 diagnostic/corrected-reference evidence, B2 independently recovered historical behaviour, B3 scientific qualification/admission and B4/production authority.
- Historical uncertainty must remain explicit. Evidence never promotes itself into historical truth or production authority.
- Mass conservation is a hard invariant. Do not invent balancing mass, fluxes or hidden state to make a test pass.
- Rejected trials must not modify committed physical state or leak authoritative continuation state through scratch, caches, diagnostics or adapter-local mutation.
- Keep physical/scientific configuration separate from numerical execution policy.
- Keep file I/O, external exchange, scientific state, scratch, diagnostics and results separated according to the accepted architecture contracts.
- Preserve one ANIMO computational kernel for standalone and coupled execution. Coupling must use explicit exchange contracts; ANIMO must not depend on internal SWAP state and SWAP must not depend on internal ANIMO state.
- Do not import SWAP5-specific physics, solver policy, calendars, tolerances, completion denominators or canonical naming into ANIMO5 merely because a runtime mechanic was useful there. Reuse only the bounded neutral contract actually qualified for ANIMO5 or cross-model use.
- Verification evidence qualifies only the exact scope tested. Synthetic or reconstructed evidence remains in its explicit evidence class and is not B2 historical truth.
- Immutable evidence is inherited only while its relevant dependency surface remains unchanged. Requalify affected capabilities, not unrelated ones.
- Confirmed legacy defects must not be silently preserved as scientific truth or silently corrected. Route them through the applicable TCD, scientific qualification, reference and admission process.
- A negative scientific qualification is a valid closed result. Do not weaken a gate to force a positive result.
- Production migration, B4 opening, Status A and Status AA require their explicit authorities. No research prototype, candidate architecture or local qualification promotes itself automatically.

## Work-unit discipline

For a material work unit, maintain a recoverable Git state before expensive or timeout-sensitive work. Follow the governing work-unit contract and GOV06 resumption requirements.

A checkpoint is a recovery boundary, not a default stopping point. After persisting a meaningful checkpoint, continue automatically with the next safe and authorized phase unless a real blocker, explicit review boundary, tool failure, ownership conflict or runtime risk requires stopping.

For connector-mediated repository work, use the retrieval order `status/checkpoint first -> exact ref -> relevant delta -> bounded files -> search only if needed`. Treat a search result as a locator rather than branch authority unless the search is explicitly scoped to the pinned target ref; re-read located paths at the exact target SHA before relying on them. Do not perform broad repository recovery when a valid status record and unchanged dependency surface make it unnecessary.

Every substantial work unit should make semantic ownership explicit. Classify shared contracts and authorities as frozen or moving and use the GOV06 parallelism classes `SAFE_PARALLEL`, `PARALLEL_AFTER_PINNING` and `SERIAL_REQUIRED`. Paused work retains ownership until explicit release, supersession or closeout.

Where research maturity applies, use exactly:

- `RESEARCH_ISOLATED`
- `CONTRACT_COMPATIBLE`
- `INTEGRATION_CANDIDATE`
- `PRODUCTION_ADMITTED`

No transition is implicit.

A useful handoff identifies at least:

```text
WORKSTREAM
WORK UNIT
BASELINE
STATUS / CHECKPOINT / RECOVERY RECORD
SCOPE
CONSUMED CONTRACTS / AUTHORITIES
OWNED OR MODIFIED CONTRACTS
FROZEN / MOVING CLASSIFICATION
FILES / COMPONENTS TOUCHED
RELEVANT PATHS / DEPENDENCY SURFACE
INTERFACES CHANGED
INVARIANTS AFFECTED
EVIDENCE CLASS / TCD / B3 SURFACE AFFECTED
IMPLEMENTATION STATUS
TEST STATUS
REVIEW STATUS
QUALIFICATION STATUS
ADMISSION / PRODUCTION STATUS
DEPENDENCIES / BLOCKERS
NEXT SAFE STEP
RECOVERY POINT
```

Do not report `tested`, `reviewed`, `qualified`, `admitted` or `production-authoritative` unless the named gate actually completed against the persisted postimage or exact frozen head required by the governing contract.

Same-agent adversarial review must be labeled `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`. Do not call it independent review.

## Change strategy

Prefer the smallest change that satisfies the accepted scientific, evidence, architecture and governance contracts.

Before editing code or contracts:

1. Locate the owning authority and current aggregate/regie context.
2. Read the work-unit status/checkpoint/recovery record when one exists.
3. Reconcile only the relevant live delta at the exact target ref.
4. Identify consumed and modified semantic contracts and whether their ownership is frozen or moving.
5. Decide whether the change is scientific, implementation, adapter/I-O, documentation, verification, governance or a production-admission decision.
6. Preserve existing qualified behaviour and evidence boundaries unless the work unit explicitly changes them.
7. Reopen a previously admitted or qualified capability only when dependency evidence or an explicit acceptance requirement justifies it.
8. Record adjacent findings without silently expanding scope.

When several authorities appear relevant, use the branch-authority model, integration DAG and current regie authority to determine what each document can and cannot establish.

## Validation

Run the narrowest relevant checks first, then the declared broader qualification or integration gates.

Use the work-unit-specific validators, test scripts, exact-head CI and reference/evidence checks named by the owning contract. Do not substitute an unrelated green CI result for the required evidence. Do not assume SWAP5 build, documentation or test commands apply to ANIMO5 unless ANIMO5 explicitly adopts them.

For historical/reference work, preserve supplied bytes and provenance. Compatibility adapters, diagnostic builds and reconstructed execution environments must remain explicitly classified and may not be reported as historical-reference truth unless the applicable B2 authority qualifies them.

## Documentation language

Use status language that makes authority, evidence class and time explicit. Useful labels include:

- **B0 historical artifact identity** - immutable identity/provenance evidence, not correctness.
- **B1 diagnostic/corrected-reference evidence** - qualified only for its stated diagnostic/reference scope.
- **B2 historical behavioural reference** - independently recovered historical behaviour only where explicitly qualified.
- **B3 scientific qualification/admission** - bounded scientific process authority, not production migration.
- **B4 / production authority** - explicit production migration/admission surface.
- **Current / canonically admitted** - part of the named current accepted boundary.
- **Candidate / target architecture** - design authority or candidate structure, not necessarily implemented or admitted.
- **Historical snapshot** - valid evidence for its recorded state, not present-state authority.
- **Proposed** - not yet accepted.
- **Qualified** - supported by named verification/review evidence for the stated scope.

Keep claims narrow enough that a future agent can trace each one to code, a scientific contract, a governance authority, a TCD/B3 disposition, a test, a review record or immutable evidence.