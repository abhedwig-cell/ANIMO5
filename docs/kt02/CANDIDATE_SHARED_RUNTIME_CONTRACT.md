# ANIMO-KT02 Candidate Shared Transient Runtime Contract

Status: nonproduction candidate contract for KT02 dual-client qualification only.

## Architectural intent

The shared substrate coordinates transient execution but does not contain model science. It owns authority transitions. Clients own the physical meaning of state, forcing, process calculation and admissibility.

The core rule is:

`accepted authority -> private attempt -> client calculation -> client assessment -> atomic commit OR reject -> accepted authority`

No client calculation may directly mutate externally authoritative accepted state.

## Required abstract responsibilities

### TimeCoordinate

A time coordinate provides exact identity and total ordering only within one explicit calendar contract. The prototype implementation may use the already qualified bounded TIME02-style rational representation. Approximate floating-point equality is not part of the shared contract.

Required operations:

- validate;
- compare equality;
- order before/after;
- add an explicitly represented positive interval where representable;
- fail closed on incompatible calendar identity or arithmetic overflow.

The shared core does not define calendar conversion or a global timestep quantum.

### TimeInterval

A requested interval contains exact `t0` and `t1` with `t1 > t0`.

An interval execution may contain multiple internal accepted substeps, but external success is permitted only when the private working state reaches exactly `t1`.

### AcceptedStore

An accepted store contains:

- stable lineage/model-instance identity;
- monotonic revision/generation;
- exact accepted time;
- one opaque client physical-state payload;
- optional atomic sidecar publication state only through a neutral extension boundary.

The shared core must not inspect scientific fields of the payload.

### Checkpoint

A checkpoint is an immutable snapshot of accepted continuation authority plus compatibility identities required by the client adapter. It must not contain rejected candidate state, active trial journals, worker scratch or transient diagnostics.

The persistence kernel is serialization-neutral. File I/O and codec choice remain adapter responsibilities.

### TrialOrigin

A private attempt is bound to exactly one accepted origin:

- lineage;
- revision/generation;
- exact origin time.

The core rejects stale, foreign or mismatched origins before publication.

### ClientAttempt

A client attempt receives:

- an immutable/snapshotted accepted origin;
- a requested candidate endpoint;
- client-owned forcing/input;
- worker-local scratch/context.

It returns a candidate result with:

- opaque candidate physical payload;
- exact candidate endpoint;
- explicit origin provenance;
- client-supplied admissibility result;
- optional client-owned diagnostics;
- optional sidecar publication candidate.

The attempt function may calculate science but may not publish authoritative state.

### Admissibility

The runtime never invents or chooses scientific acceptance criteria. It consumes an explicit client-supplied result with at least:

- evidence complete: yes/no;
- admissible: yes/no;
- optional opaque typed assessments for diagnostics/audit.

Incomplete evidence cannot be treated as acceptance.

### Commit

Commit validates the entire candidate postimage before mutation. At minimum it checks:

- accepted store valid;
- trial provenance complete;
- lineage match;
- revision/generation match;
- exact origin-time match;
- forward candidate progress;
- endpoint not beyond the active requested target;
- explicit complete admissibility;
- client payload validity through a client validation hook;
- optional sidecar publication capacity/validity if used.

Only after all checks pass may accepted physical state, accepted time, revision/generation and any atomic sidecar publication be replaced. Any failure leaves all externally authoritative outputs unchanged.

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

## Proposed nonproduction module partition

The KT02 prototype should be organized so that model-neutral code can later be extracted without path or module-name dependence on ANIMO:

- `prototype/kt02/runtime/mod_transient_time.f90`
- `prototype/kt02/runtime/mod_transient_contracts.f90`
- `prototype/kt02/runtime/mod_transient_transactions.f90`
- `prototype/kt02/runtime/mod_transient_interval_runtime.f90`
- `prototype/kt02/runtime/mod_transient_persistence.f90`
- `prototype/kt02/runtime/mod_transient_worker_context.f90`

Synthetic clients should be separate:

- `prototype/kt02/clients/mod_swap_like_client.f90`
- `prototype/kt02/clients/mod_animo_like_client.f90`

No runtime module may `use` either client module or any production SWAP5/ANIMO scientific module.

## SWAP-like proof client

The SWAP-like client should model a compact continuous-state problem with solver-style diagnostics and a policy that may reject and retry an attempted endpoint. It is not a Richards solver and must not copy SWAP physical equations.

The purpose is to prove transaction, retry, scratch and interval mechanics in a solver-shaped client.

## ANIMO-like proof client

The ANIMO-like client should model multiple synthetic conserved stores and optional directed transfer events. It may expose several conservation assessments rather than one aggregate water balance. It must not copy ANIMO nutrient or organic-matter equations.

The purpose is to prove that the same transaction and interval core works for a materially different process/accounting shape.

## Future coupled participant seam

KT02 may define but not productionize a neutral participant lifecycle:

1. bind accepted origin for `[t0,t1]`;
2. prepare private attempt context;
3. calculate candidate;
4. return explicit admissibility and proposed endpoint;
5. commit or reject only under orchestrator control.

A later SWAP5-ANIMO coupling workunit must decide joint interval ownership, timestep negotiation and typed hydrology-transfer semantics. KT02 does not assume that either model is permanently the time master.

## Qualification boundary

KT02 passes only if one shared implementation serves both proof clients without model-specific forks in the core and without importing model-specific science or numerical policy.

If this cannot be demonstrated cleanly, the correct KT02 result is a narrower shared substrate or a negative extraction disposition.