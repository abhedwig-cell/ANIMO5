# ANIMO-KT01 Adversarial Review

## Review 1

Review target: `fc4df11c467bcd26951a3e7b168e5bf9c676b94b`

Review mode: `same-agent / not genuinely independent`

GOV05 process label: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`

Risk posture: strict review. KT01 touches transaction boundaries, restart representation, exact-time realization and interval publication mechanics. A green build is therefore necessary but not sufficient.

Exact-head evidence: GitHub Actions run `35042404231`, job `exact-head-qualification`, completed successfully against exactly the review target. The executable suite and structural guards passed.

### Ownership reconstruction

The reviewed design separates accepted state, trial state, worker scratch and diagnostics, uses exact TIME02 candidate coordinates, keeps interval progress private until exact target completion, and does not depend on SWAP5 modules at runtime. The prototype is isolated below `prototype/kt01/` and the GOV06-to-authoring-head diff contains no `src/` production change.

### Adversarial counter-hypotheses

1. A rejected trial or failed interval could leak candidate physical state. Existing tests reject this hypothesis.
2. Retry could start from a mutated rejected origin. Existing runtime trace tests reject this hypothesis.
3. TIME02 could have been weakened by floating equality, epsilon, ULP logic or unchecked rational cross multiplication. Source and structural checks reject this hypothesis.
4. SWAP scientific policy could have leaked through retry, water-balance, solver, calendar or hydraulic payloads. Source review and structural checks reject this hypothesis for the inspected prototype.
5. A checkpoint could contain worker scratch, diagnostics or rejected trial state. Source review rejects those specific paths.
6. Committed transfer/event history could have been conflated with accepted physical continuation state and restart state. This hypothesis is confirmed.

### Material finding KT01-R1-F01

Severity: material architecture/ownership defect.

The reviewed head places `TransferJournal` as `AcceptedState%committed_journal`, copies accepted trial events into that field during commit, and persists that journal inside `AcceptedCheckpoint`.

That is too broad for KT01. The governing/reconciled contract treats the transfer/event journal as trial-local typed events and distinguishes physical continuation state from observer/ledger state. A committed event ledger can be a legitimate output of atomic publication, but making the ledger part of physical `AcceptedState` and restart continuation silently changes ownership and persistence semantics. KT01 has no authority to make that scientific/restart choice.

This is not repaired by the passing tests. The tests only prove that rejected events are not copied into the current carrier. They do not justify making accepted event history part of physical continuation state.

### Required bounded remediation

- remove committed event history from `AcceptedState`;
- remove event history from `AcceptedCheckpoint`;
- keep `TrialState%trial_journal` private to the attempt;
- publish accepted trial events to an explicit committed event ledger that remains separate from physical accepted state;
- make interval execution keep both private physical progress and private accepted-event progress until exact interval completion, then publish both together;
- add verification that checkpoint state excludes the event ledger and that failed/incomplete intervals publish neither physical state nor accepted events.

No TIME, scientific-process, mass-tolerance, B3, B4 or production policy change is permitted by this remediation.

### Review 1 verdict

`REMEDIATION_REQUIRED_AUTHORING_HEAD_NOT_QUALIFIED`

The reviewed head `fc4df11c467bcd26951a3e7b168e5bf9c676b94b` remains unqualified despite successful exact-head CI. After material remediation a new immutable authoring head must be frozen, exact-head CI rerun, and the adversarial review restarted against that new head.

## Review 2, restarted after remediation

Review target: `25819e08fa34676e8dddd0254c4539f6b4372b89`

Review mode: `same-agent / not genuinely independent`

GOV05 process label: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`

Applicable posture: Tier-C-style enhanced review because KT01 exercises state ownership, exact numerical identity and restart/checkpoint behavior. This is a review discipline only. It does not assign B3/B4 maturity to the prototype.

Exact-head evidence: GitHub Actions run `35043168090`, job `104627245057` / `exact-head-qualification`, completed `SUCCESS` against exactly `25819e08fa34676e8dddd0254c4539f6b4372b89`. The GOV06-to-authoring-head compare is 38 commits ahead, zero behind, with no file under `src/` changed.

### Reconstructed claims and counter-hypothesis

The strongest alternative considered is that SWAP5 reuse has imported hidden SWAP scientific policy, or that the remediated transaction design still conflates physical continuation, event history, retry policy or canonical time admission. That alternative was tested against the exact source, executable tests, structural guards, the reuse matrix and the frozen authority map rather than against the authoring narrative alone.

The review finds that the prototype is narrower than SWAP5 in the required places. It reuses control structure only. Floating-time identity, SWAP tolerance and step-doubling policy, single-water acceptance, hydraulic scratch, groundwater sensitivity, calendar assumptions, file formats and SWAP physical layouts remain rejected. There is no SWAP module dependency at runtime.

### Review-1 finding closure

`KT01-R1-F01` is closed. `AcceptedState` no longer owns committed event history. `AcceptedCheckpoint` has private components and contains no transfer journal or event ledger. `TrialState%trial_journal` remains attempt-local. A separate `CommittedEventLedger` receives accepted events only through a validated postimage. Interval execution clones both physical accepted state and the separate ledger privately and publishes both only after exact requested-target completion. Tests 08, 18, 27, 36 and 37 plus structural guards S08-S10 exercise these boundaries.

`KT01-R1-F02` is closed. Directed transfer identity is `source_id -> sink_id`; negative amounts are rejected before journal mutation. Test 35 is the explicit negative control.

`KT01-R1-F03` is closed. Test 38 compares uninterrupted continuation with an accepted-checkpoint split and restore. Exact final physical time, lineage/generation, synthetic physical storage and the separately retained event history agree without an invented tolerance. This is synthetic restart-mechanics evidence only, not historical ANIMO restart evidence.

### Exact-time review

TIME02 is not weakened. The time path contains no REAL declaration or conversion, no epsilon/ULP equality and no unchecked denominator cross multiplication. Exact rational comparison uses a continued-fraction/Euclidean method. Arithmetic detects fixed-width overflow and fails closed.

The executable backend now states an explicit bounded `int64` representation envelope. Overlength or delimiter-ambiguous calendar identifiers fail closed. The pipe-delimited serializer is explicitly described as a prototype round-trip harness, not the TIME02 canonical JSON interchange form. No fixed global timestep quantum is introduced and `canonical_time_admission=false` remains unchanged.

### State, persistence and ownership review

Physical accepted state, trial state, trial event journal, committed event ledger, worker scratch and diagnostics have distinct ownership. Trial provenance is required before commit. Lineage, generation and exact origin time are validated. Generation advances exactly once after successful commit. A checkpoint is constructible through the persistence boundary only from accepted physical continuation and excludes event history, rejected state, worker scratch and diagnostics.

The fixed capacities and fixed-width identifiers are prototype representation limits, not scientific registry or tolerance decisions. Overflow/capacity failure is fail-closed. They therefore bound the executable prototype without claiming future production layouts.

### Conservation and numerical-policy review

The runtime receives typed quantity/control-volume assessments and requires supplied completeness and admissibility. It does not select a tolerance, calculate a balancing term or hard-code water semantics. Tests cover multiple quantities, incomplete evidence rejection and absence of a balancing event. Retry permission is synthetic test-plan input. No physical timestep, subdivision, step-doubling or solver fallback policy is admitted.

### Governance and provenance review

The exact six SWAP5 source blobs remain pinned to `50346642bd565f79134ea17d5462e544b354998c` and were already verified identical at current SWAP5 canonical `992a5c657bfe10a10100f92e0cb77c4825ae65b6`. The matrix distinguishes `PORT_WITH_ANIMO_ADAPTATION`, `DESIGN_ONLY` and `REJECT`; no element is claimed as `DIRECT_PORT`. Source headers and provenance documentation bind each materialized module to its exact source or ANIMO authority.

The prototype remains under `prototype/kt01/`. There is no modification of ANIMO scientific production source, no B3 queue/admission mutation, no B4 opening, no production opening, no shared cross-model library, no B2 historical-reference creation and no Status A/AA claim.

### Residual uncertainty and non-authority

This is a same-agent process and therefore retains correlated-reasoning and confirmation-bias risk. It is not human, organizational or genuinely independent review.

The bounded `int64` time backend is not arbitrary-precision TIME02 production realization. The prototype serializer is not canonical TIME02 JSON. The fixed event-ledger capacity and fixed identifier widths are prototype implementation envelopes. A later production implementation must separately qualify its representation, serialization, encapsulation and real process adapters under the authority then in force.

No real ANIMO process, real forcing frame, final conserved-quantity registry, scientific tolerance or final production restart format has been qualified here.

### Review 2 verdict

`SELF_REVIEW_PASS_NONPRODUCTION_PROTOTYPE_ONLY`

No material blocker remains within KT01 scope at the reviewed authoring head. This result is `same-agent / not genuinely independent` and supports only qualification of the isolated nonproduction prototype. It does not admit canonical TIME, B3, B4, production, historical equivalence, Status A or Status AA.
