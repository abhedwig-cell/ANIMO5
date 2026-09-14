# ANIMO5 capability-flow delivery policy

Status: `ACTIVE_PROSPECTIVE_DELIVERY_OVERLAY`

Effective for new work started after 2026-09-14.

Base governance pin: `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`.

This policy changes delivery granularity and coordination. It does not change ANIMO science, weaken GOV05 scientific gates, rewrite historical workunits, admit any TCD, open B4, or authorize production.

## 1. Default planning unit is a capability

The default unit of planning is a capability, not an individual observation, test, document, correction, or admission sub-step.

A capability may contain multiple atomic commits and scientific decisions. Atomicity remains mandatory at commit and decision level, but a separate workunit, branch, qualification cycle, or review cycle is not required for every atomic commit.

Normal flow:

`CAPABILITY -> pin authority/contracts once -> atomic commits -> integrated falsification -> qualification/review at the capability boundary -> canonical disposition`

A new workunit or branch is exceptional rather than automatic.

## 2. Branch creation gate

Create a new authoritative workunit/branch only when at least one of these conditions holds:

1. a scientific, numerical, persistent-state, restart, API, or canonical governance contract changes;
2. semantic ownership would otherwise collide with another active capability;
3. evidence must remain independently pin-able because failure or reversal must not contaminate the active capability line;
4. the applicable GOV05/B3 governance route explicitly requires a separate decision surface;
5. an experiment is deliberately isolated and is recorded as non-authoritative research or supplemental evidence.

If none applies, keep the work as tasks or atomic commits inside the existing capability branch.

A discovered uncertainty does not by itself justify a new workunit.

## 3. No process-branch proliferation

For one capability or admission route, do not create branches whose only purpose is a process phase or checkpoint, including names such as:

`final`, `review`, `copy`, `shadow`, `temp`, `staging`, `freeze`, `package`, `ci`, `artifacts`, `checkpoint`, or equivalent.

Use immutable Git commits on the authoritative branch as authoring/review/checkpoint pins. GOV05 already requires immutable checkpoints; those checkpoints are commits, not extra branches.

A second branch is allowed only when the branch-creation gate in section 2 is satisfied.

Historical branches are not deleted or rewritten solely to conform to this rule.

## 4. Evidence inheritance by default

Persisted immutable evidence is inherited until invalidated. Do not rerun or recreate evidence merely to reproduce ceremony.

Reuse is valid only when all of the following remain true:

- the exact evidence pin is recorded;
- the current claim is within the original evidence scope;
- none of the evidence dependencies changed;
- no contradictory or superseding evidence exists;
- the evidence is not promoted to a stronger class than originally qualified.

An evidence dependency is invalidated when the relevant source, contract, state definition, numerical policy, fixture, oracle, expected-difference contract, or interpretation boundary changes.

When invalidated, rerun only the affected evidence slice. Unaffected evidence remains inherited.

This operationalizes GOV05 `VERIFY_AND_REUSE`; it does not weaken it.

## 5. Delivery risk routing

The following delivery classes determine process weight. They are routing classes, not replacements for GOV05 scientific tiers. The strictest applicable GOV05/B3 trigger still wins.

| Delivery class | Typical change | Default route |
| --- | --- | --- |
| R0 | documentation, metadata, diagnostics with no semantic effect | test/check + commit; no standalone qualification |
| R1 | semantics-preserving refactor, harness, tooling, mechanical cleanup | targeted tests + lightweight review inside capability |
| R2 | state, IO, API, restart, lifecycle, adapter, integration contract | targeted qualification at capability boundary |
| R3 | physics, conservation, numerical semantics, scientific state, production-authorizing composition | full applicable scientific qualification and GOV05 adversarial review |

R0/R1 work must escalate if evidence shows a semantic effect. A label never overrides observed risk.

## 6. Work-in-progress limit

At most three production-relevant capability streams may be active at the same time.

`ACTIVE` means substantive authoring, qualification, or integration work is currently being performed, not merely that an old branch exists.

Independent research, preservation, verification, or measurement work may run outside this limit only when:

- it does not mutate shared semantic ownership;
- it does not require a moving production interface;
- it is explicitly marked `RESEARCH_ISOLATED`, `PRESERVATION`, `VERIFICATION_ONLY`, or `MEASUREMENT_ONLY`;
- it cannot silently become a production dependency.

When the limit is reached, finish, pause, or integrate an active capability before activating another production-relevant stream.

## 7. Capability-level qualification

Do not perform a full governance and qualification cycle for every internal atomic step of one capability.

Within a capability:

- keep commits small and revertible;
- persist important scientific decisions when they occur;
- run cheap local tests continuously;
- accumulate the evidence package;
- perform integrated falsification and the applicable scientific review at the capability boundary.

Split the capability only if a new contract boundary, ownership collision, materially different risk class, or independent scientific decision surface appears.

## 8. Governance stop rule

Do not create a new governance artifact merely because a new uncertainty was discovered.

A new governance artifact is justified only when it does at least one of the following:

- removes a concrete authority or ownership ambiguity;
- defines a reusable contract required by multiple later tasks;
- resolves a real collision that blocks technical or scientific work;
- creates an auditable decision surface required by an existing qualification route;
- measurably reduces future repeated work.

If it only restates an existing rule or adds another layer needed to interpret earlier governance, do not create it. Amend or reference the existing authority instead.

## 9. Progress accounting

Project progress is reported by capability completion, not number of branches or workunits.

Track four completion dimensions:

1. capability implementation;
2. scientific/technical qualification;
3. canonical integration;
4. preservation and traceability.

A completed governance document, branch, review packet, or admission sub-step is not counted as an independent unit of product progress unless it closes one of those dimensions.

## 10. Minimal process telemetry

For each completed capability, record only these overhead indicators:

- number of substantive implementation/science commits;
- number of governance/evidence-only commits;
- number of evidence reruns caused by actual invalidation;
- number of reopened decisions;
- number of other active branches that had to be reconciled before completion.

Use these metrics to detect process cost. Do not create a separate telemetry workunit for each capability.

## 11. Existing GOV05 decision surfaces remain

This policy does not collapse decision surfaces that GOV05 deliberately keeps separate, including composition qualification, integration qualification, B4 decision, and production authorization.

It changes how work is grouped before those boundaries. One capability can carry multiple atomic steps to the next legitimate decision surface; it cannot skip that surface.

## 12. Transitional rule

Existing qualified, failed, blocked, or historical work remains unchanged. Existing branches remain evidence and are not cleaned up merely for policy conformity.

From the effective date forward:

- prefer continuation inside an active capability over opening a new workunit;
- prefer immutable commit checkpoints over process branches;
- inherit valid evidence until a dependency invalidates it;
- enforce the three-stream production WIP limit;
- bundle qualification at capability boundaries;
- stop creating governance whose only effect is more governance.

If this delivery overlay conflicts with a scientific, historical-evidence, B3, GOV05, B4, or production safety gate, the stricter scientific/safety gate controls.
