# ANIMO-KT02 Candidate Shared Transient Runtime Contract

Status: nonproduction candidate contract for KT02 dual-client qualification only.

## Architectural intent

The shared substrate coordinates transient execution but does not contain model science. It owns authority transitions. Clients own the physical meaning of state, forcing, process calculation and admissibility.

The core rule is:

`accepted authority -> private attempt -> client calculation -> client assessment -> atomic commit OR reject -> accepted authority`

No client calculation may directly mutate externally authoritative accepted state.

The accepted store, trial origin and trial result provenance are opaque in the hardened prototype. Ordinary clients can initialize new accepted authority, request a private trial, snapshot payloads and submit a candidate result, but cannot directly set accepted time/generation or forge trial provenance fields. Persistence has one explicitly named trusted reconstruction boundary for rebuilding accepted state from a validated checkpoint.

## Required abstract responsibilities

### TimeCoordinate

A time coordinate provides exact identity and total ordering only within one explicit calendar contract. The prototype implementation uses the already qualified bounded TIME02-style rational representation. Approximate floating-point equality is not part of the shared contract.

Required operations:

- validate;
- compare equality;
- order before/after;
- add an explicitly represented positive interval where representable;
- fail closed on incompatible calendar identity or arithmetic overflow.

The shared core does not define calendar conversion or a global timestep quantum.

This remains a prototype-level shared-time candidate. It does not imply that the current SWAP5 production runtime has migrated from its REAL-valued time representation.

### TimeInterval

A requested interval contains exact `t0` and `t1` with `t1 > t0`.

An interval execution may contain multiple internal accepted substeps, but external success is permitted only when the private working state reaches exactly `t1`.

The interval runtime, not the standalone transaction primitive, owns the active requested target. It therefore rejects zero/backward progress and candidate endpoints beyond the requested target before trial execution. Standalone transaction commit owns exact accepted-origin validation and strictly forward endpoint progress, but has no implicit interval target of its own.

### AcceptedStore

An accepted store contains:

- stable lineage/model-instance identity;
- monotonic revision/generation;
- exact accepted time;
- one opaque client physical-state payload.

The shared core does not inspect scientific fields of the payload. The hardened prototype keeps accepted components private and exposes only controlled initialization, snapshots and read-only identity/time accessors.

KT02 does not qualify a generic second atomic publication product such as an ANIMO transfer-event ledger. If such a sidecar is needed later, it requires a neutral extension contract and separate proof that atomic publication remains model independent.

### Checkpoint

A checkpoint is an immutable snapshot of accepted continuation authority plus compatibility identities required by the client adapter. It must not contain rejected candidate state, active trial journals, worker scratch or transient diagnostics.

The persistence kernel is serialization-neutral. File I/O and codec choice remain adapter responsibilities.

Restore uses an explicitly named trusted reconstruction boundary. That boundary exists to reconstruct accepted authority from already validated persistence evidence and is not an ordinary state-mutation API.

### TrialOrigin

A private attempt is bound to exactly one accepted origin:

- lineage;
- revision/generation;
- exact origin time.

The core rejects stale, foreign or mismatched origins before publication. Trial provenance fields are private in the hardened prototype; a caller cannot rewrite them after `begin_trial`.

### ClientAttempt

A client attempt receives:

- an immutable/snapshotted accepted-origin payload;
- the exact accepted origin time;
- a requested candidate endpoint;
- client-owned forcing/input or execution parameters through its adapter context.

It returns a candidate payload plus explicit admissibility. The attempt function may calculate science but may not publish authoritative state.

The client object itself is non-authoritative execution context. It may retain diagnostics, cache data, numerical workspace or test-policy counters, but it must not retain physical continuation state that survives independently of `AcceptedStore`. Any retained warm-start information must be disposable or separately proven not to alter scientific identity across reject/retry.

### Admissibility

The runtime never invents or chooses scientific acceptance criteria. It consumes an explicit client-supplied result with at least:

- evidence complete: yes/no;
- admissible: yes/no.

A later adapter may attach model-specific typed assessments for diagnostics or audit, but those quantities and tolerances remain outside the shared core. Incomplete evidence cannot be treated as acceptance.

### Commit

Transaction commit validates the complete candidate postimage before accepted-authority mutation. At minimum it checks:

- accepted store valid;
- trial provenance complete;
- lineage match;
- revision/generation match;
- exact origin-time match;
- strictly forward candidate progress;
- explicit complete admissibility;
- client payload validity.

Only after all transaction checks pass may accepted physical payload, accepted time and revision/generation be replaced. Any failure leaves accepted authority unchanged.

When commit runs inside an interval, the interval runtime has already additionally checked that the candidate endpoint does not exceed the requested target.

### RetryPolicy boundary

The core may execute a bounded attempt loop, but the client/application policy owns:

- whether retry is permitted;
- next candidate endpoint;
- subdivision factor;
- solver fallback choice;
- scientific/numerical tolerances;
- attempt budget configuration.

The core owns only enforcement of the supplied budget and the rule that each retry originates from accepted authority, not from a rejected candidate.

### WorkerContext

Worker context is explicitly non-authoritative scratch. It may contain client-specific numerical workspace and attempt diagnostics. It must be reset/rebound according to the client lifecycle and must never be serialized into accepted checkpoints by the shared core.

## Nonproduction module partition

The KT02 prototype is organized so that model-neutral code can later be extracted without path or module-name dependence on ANIMO:

- `prototype/kt02/runtime/mod_transient_time.f90`
- `prototype/kt02/runtime/mod_transient_contracts.f90`
- `prototype/kt02/runtime/mod_transient_transactions.f90`
- `prototype/kt02/runtime/mod_transient_interval_runtime.f90`
- `prototype/kt02/runtime/mod_transient_persistence.f90`
- `prototype/kt02/runtime/mod_transient_worker_context.f90`

Synthetic clients are separate:

- `prototype/kt02/clients/mod_swap_like_client.f90`
- `prototype/kt02/clients/mod_animo_like_client.f90`

No runtime module may `use` either client module or any production SWAP5/ANIMO scientific module.

## SWAP-like proof client

The SWAP-like client models a compact continuous-state problem with solver-shaped execution and a policy that can reject a first attempt and retry from the same accepted origin. It is not a Richards solver and copies no SWAP physical equations.

The purpose is to prove transaction, retry, scratch and interval mechanics in a solver-shaped client.

## ANIMO-like proof client

The ANIMO-like client models two synthetic nonnegative conserved stores with an internal directed transfer. Its conservation check is client-owned and uses guarded `int64` arithmetic. It does not copy ANIMO nutrient or organic-matter equations.

The purpose is to prove that the same transaction and interval core works for a materially different process/accounting shape.

KT02 does not yet expose the synthetic transfer as a separately committed event ledger. That remains outside this qualification.

## Future coupled participant seam

KT02 may define but not productionize a neutral participant lifecycle:

1. bind accepted origin for `[t0,t1]`;
2. prepare private attempt context;
3. calculate candidate;
4. return explicit admissibility and proposed endpoint;
5. commit or reject only under orchestrator control.

A later SWAP5-ANIMO coupling workunit must decide joint interval ownership, timestep negotiation and typed hydrology-transfer semantics. KT02 does not assume that either model is permanently the time master.

## Qualification boundary

KT02 can pass only if one shared implementation serves both proof clients without model-specific forks in the core, without direct mutation/forging of accepted or trial provenance, and without importing model-specific science or numerical policy.

A positive result qualifies only the bounded nonproduction dual-client prototype. It does not create a production shared library, migrate SWAP5 or ANIMO5 production code, admit canonical TIME, open B4, or qualify production coupling.