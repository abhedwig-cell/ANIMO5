# ANIMO-GOV06 Unified Program Regie

Authority type: governance only. This policy does not alter scientific source, B0, B3 admission, aggregate admission, B4, production migration, Status A or Status AA.

## Governing ANIMO authorities pinned at authoring

- current aggregate: `ANIMO-RG05O@bc9e6ed997a078336645210ebb4d99ae976893fe`
- current global B3 closure gate: `ANIMO-B3Q06@11e9bcdc6654e63f84875bf1f28dc54abe725700`, qualified negative: three top-level TCDs remain unadmitted, TCD-016, TCD-034 and TCD-040
- current routing authority carried by RG05O: `ANIMO-B3I10@942f26fe32eaf91679e59a1968ae173a3703e22d`
- `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`
- `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`
- `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`
- observed current qualification-family heads: `SQ08@f89ec3b0bfd053c2c903cbbcf2243bb4ab4a5741`, `NQ05@62080a8e731681407e2e7e759decc49c1a47fa7b`, `MASSQ04@3e0f8254d9cd7966a4491b3068d0239b8ccda5f9`, `STATEQ07@26f6e61da328a5578b9c4b332de04eb99a3ac04f`, `RUNTIMEQ03@a3e822f8e97fe1312a7dfa73601a49ae7375163e`, `SYNQ05@ca3b6fba99ddc70e1f063ac98088f8825f467c1a`, `TB07A@6d77e92f5beb2a30deb7411d93890aa7a5559685`, `ARCHG02@db8183802631902f41aa5bec518a3c2e63e03ab7`.

A branch head is evidence that an authority exists, not by itself evidence that a stream is currently active. Moving authorities must be rechecked before execution or composition.

## SWAP5 lessons inspected and translated

The live inspected SWAP5 governance authorities remained `F-RG01A@4553204468695553cf69a48d1c97598c471156d6`, `F-RG01B@5e2561d9051fba81769565291b1bf3089c7ddcd9`, `F-RG01C@56b86e29e0960e396059caf47c193440d571b709`, `F-RG01D@0877971d1117cb0067aa363d0868d682f62a6844`, and rebaseline `F-RG03@aac2644149dda47282a25a39892c6dc808323dd0`.

ANIMO5 adopts the useful abstract lessons: semantic contract ownership rather than file ownership, explicit parallelism classes, research maturity labels, runtime-independent workunits with durable resumption records, a capability-map-first approach to completion, responsibility-based module contracts, and periodic regie rebaselining.

ANIMO5 rejects direct transfer of SWAP5 weights, denominators, module topology, solver-specific contracts, v1 completion percentages, or SWAP-specific canonical naming. ANIMO5 has its own B0-B4 lifecycle, TCD/B3 admission semantics, C/N/P conservation obligations and Status A/AA path.

## Semantic contract ownership

Every workunit SHALL declare consumed semantic contracts, owned or modified semantic contracts, each contract's `FROZEN` or `MOVING` status, owner, allowed files or semantic scope, forbidden overlap, dependencies and exit gate. Branch separation and disjoint filenames are insufficient for `SAFE_PARALLEL`.

Parallelism classes are:

- `SAFE_PARALLEL`: no shared moving semantic contract and no shared authority mutation.
- `PARALLEL_AFTER_PINNING`: work consumes shared semantics only after exact immutable authority pins and does not co-own them.
- `SERIAL_REQUIRED`: work changes a shared moving semantic contract, shared composition authority, routing authority, aggregate authority, production gate, or another single-writer surface.

Paused work retains semantic ownership until explicit release, supersession, or closeout. Conflicting ownership fails closed and triggers immediate regie rebaseline.

## Research maturity

Where research maturity is relevant, use exactly `RESEARCH_ISOLATED`, `CONTRACT_COMPATIBLE`, `INTEGRATION_CANDIDATE`, `PRODUCTION_ADMITTED`. No transition is implicit. Research authority cannot silently become production authority. Optional research is excluded from production-completion scope unless a later versioned scope authority explicitly includes it.

## Runtime-independent execution and resumption

A workunit is defined by scientific or architectural cohesion, not by one ChatGPT runtime. A paused or interrupted runtime does not invalidate scientific work and does not release ownership automatically.

Any substantial incomplete workunit SHALL persist a resumption record containing: identity and scope; current phase; exact governing authorities; current aggregate or canonical authority; consumed and owned contracts; frozen or moving classification; scientific and design decisions; commits and changed files; completed tests and results; review status; blockers; next safe action; and moving authorities requiring live recheck. The machine-readable schema in GOV06 is normative for new records.

## Evidence and assurance

ANIMO5 preserves distinct evidence and authority layers:

- B0: immutable historical artifact identity and provenance. It is not correctness.
- B1: corrected or reproducible diagnostic/reference evidence as governed by its qualified authority. It is not automatically historical truth.
- B2: independently recovered historical behavioural reference where actually qualified.
- B3: scientific qualification and explicit admission by bounded process scope.
- synthetic or reconstructed evidence: useful only under its explicit evidence class and never promoted to B2.
- model-evolution evidence: evidence for a proposed new bounded scientific contract, not historical fidelity and not production authority.
- production authority: only through the explicit B4 and production decision surfaces.

Historical uncertainty must remain explicit. Evidence does not promote itself into authority.

## Scientific review

GOV05 remains controlling where applicable: `MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW`. Same-agent review SHALL be labeled `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT` and never called independent. Genuinely independent review remains required wherever a governing authority separately requires it.

The default review sequence is: authoring complete, immutable authoring head, exact-head CI, adversarial review, remediation if required, new immutable head after substantive remediation, final exact-head CI. A negative scientific qualification is a valid closed result.

## Admission and composition separation

The following are never equivalent: qualification and admission; child admission and parent admission; local admission and aggregate authority; aggregate authority and queue or composition completeness; composition completeness and production admission. No authority promotion is automatic. Shared aggregate, canonical, routing, queue or composition mutations are `SERIAL_REQUIRED`.

## Module Contract Standard

An ANIMO5 module is an architectural or scientific responsibility, not one Fortran source file. The GOV06 module schema covers identity and authority; owns, must-not-own and non-goals; parameters; persistent dynamic state; derived state; requests and forcing; numerical configuration; results and diagnostics; scratch or workspace; provided and consumed semantic contracts; transaction semantics; C/N/P conservation obligations; time semantics; restart and persistence; optionality and scaling; fail-closed behavior; replaceability boundary; evidence and open gaps.

The module registry is an index and governance overlay, not a second source of scientific truth. It MUST point to governing scientific and architectural authorities rather than restating equations or inventing semantics. Existing qualified B3 science is not invalidated retroactively. Schema-conforming manifests are required prospectively before B4 production admission for new or materially changed modules.

## Scope and denominator

The current ANIMO5 whole-program denominator is `DENOMINATOR_NOT_YET_QUALIFIED`. TCD admission count is not whole-program completion. GOV06 persists a capability map across scientific B3 closure, architecture readiness, production migration/B4, testbank and release qualification, documentation and scientific traceability, Status A readiness, Status AA readiness, and optional research.

No numerical percentage or weight is authorized because the present repository does not yet contain a defensible frozen, non-arbitrary whole-program scope with qualified weights. A later denominator or weight model requires a new versioned governance authority and cannot rewrite historical progress retroactively.

## Regie cycle and rebaseline triggers

The program cycle is `rebaseline -> classify dependencies and ownership -> parallel execute where safe -> qualify/admit -> preserve evidence -> rebaseline`.

Return to regie after a bounded set of substantive closeouts, after a major aggregate or canonical architecture change, immediately on contract-ownership conflict, immediately on scope or denominator conflict, and before major B3-completeness, B4, Status A or release decisions.

## Current rebaseline result

RG05O is the current aggregate authority inspected here, while B3Q06 is the later global closure gate and remains negative. Therefore B3 composition is incomplete and B4 remains closed. TB07A is a fail-closed testbank prerequisite authority, not permission to establish a composed release baseline. Status A and Status AA gap evidence remains open. GOV06 changes none of those states.

The initial execution-wave map is deliberately conservative. TCD-016, TCD-034 and TCD-040 scientific closure work may proceed only under their own authorities and contract ownership. Any B3 parent admission, queue recompute, aggregate composition, B4 decision or production migration remains serialized and outside GOV06.
