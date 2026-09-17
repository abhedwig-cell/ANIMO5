# ANIMO-KT02 Adversarial Review Remediation

Review mode remains `same-agent / not genuinely independent`.

Assurance label remains `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Original reviewed executable head: `5a6c990f04f44837812ee15e7827688ff495c7ac`.

Remediated frozen executable head: `1909709e7a244b5d0ee53342a26bab74815c118c`.

Exact-head GitHub Actions run for the remediated executable: `35278517691`, conclusion `SUCCESS`.

## Finding closure

### KT02-R1, accepted/trial authority externally mutable

Status: `RESOLVED_FOR_BOUNDED_PROTOTYPE`.

`accepted_store_t`, `trial_state_t` and `trial_result_t` now have private components in `mod_transient_transactions`. Clients no longer assign accepted time, generation, lineage or trial-origin provenance directly. The ordinary API is reduced to controlled initialization, accepted-state snapshots/accessors, `begin_trial`, trial payload snapshot, result construction and `commit_trial`/reject.

Persistence keeps one explicitly named `reconstruct_accepted_store_trusted` boundary. This is a deliberate privileged reconstruction seam, analogous to a trusted persistence adapter boundary, and is not ordinary transaction mutation authority. KT02 does not claim protection against deliberately malicious code executing inside the same Fortran process and calling a trusted API.

The structural test now checks that accepted, trial and result carriers have private components and that the trusted reconstruction boundary is explicit.

### KT02-R2, target-bound responsibility overstated

Status: `RESOLVED`.

The contract now distinguishes two responsibilities:

- `run_interval` owns the active requested target and rejects zero/backward progress and endpoints beyond that target before trial execution;
- standalone `commit_trial` owns exact accepted-origin validation, stale-origin rejection, complete admissibility and strictly forward endpoint progress.

This matches the implementation and avoids pretending that a context-free transaction primitive knows an interval target it was never given.

### KT02-R3, client object authority insufficiently constrained

Status: `RESOLVED_AS_EXPLICIT_CLIENT_CONTRACT`.

The candidate contract now states that `transient_client_t` is non-authoritative execution context. A client may retain diagnostics, caches, numerical workspace or policy counters, but physical continuation authority must reside only in the accepted payload. Retained warm-start information must be disposable or separately proven not to alter scientific identity across reject/retry.

This is a semantic contract rather than a language-enforced guarantee. A later production adapter must prove this property for its concrete model implementation.

### KT02-R4, unchecked `int64` total in ANIMO-like proof client

Status: `RESOLVED`.

The ANIMO-like client now checks target-store addition and total-storage addition for representability before computing the synthetic conservation comparison. This removes the avoidable proof-client overflow ambiguity.

### KT02-R5, exact time not SWAP5 production authority

Status: `ACCEPTED_EXPLICIT_BOUNDARY`.

No change. KT02 qualifies only the exact-time candidate inside the nonproduction shared prototype. It does not claim SWAP5 production migration.

### KT02-R6, generic atomic sidecar not proven

Status: `ACCEPTED_EXPLICIT_BOUNDARY`.

No change. The current shared core qualifies one accepted physical payload only. A generic atomic sidecar/event product remains a future extension decision and is not part of the KT02 positive claim.

## Post-remediation test evidence

The exact-head workflow compiles the neutral runtime and both proof clients with `gfortran -std=f2008 -Wall -Wextra -Werror`, executes the dual-client runtime tests, and executes the structural dependency/opacity checks. Run `35278517691` completed successfully on `1909709e7a244b5d0ee53342a26bab74815c118c`.

The test set demonstrates, within the bounded synthetic prototype:

- first-attempt rejection followed by retry from the same accepted origin;
- exact-target completion with publication only after full interval completion;
- incomplete interval failure without external publication of privately accepted intermediate progress;
- stale-generation commit rejection after another candidate has already committed;
- checkpoint/restore of accepted continuation state;
- worker scratch reset across attempts/models;
- one shared runtime serving both continuous solver-shaped and multi-store conservation-shaped clients;
- absence of SWAP/ANIMO scientific module imports and selected domain-specific science terms from the shared runtime core.

## Review disposition

`SELF_REVIEW_PASS_NONPRODUCTION_DUAL_CLIENT_PROTOTYPE_ONLY`.

Material open findings after remediation: none within KT02's stated nonproduction scope.

This result is not independent production-admission evidence and does not authorize production migration, a separately versioned shared library, B4 opening, canonical TIME admission or SWAP5-ANIMO production coupling.