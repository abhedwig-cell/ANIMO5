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
