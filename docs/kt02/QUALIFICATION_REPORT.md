# ANIMO-KT02 Qualification Report

## Qualification target

Workunit: `ANIMO-KT02 — Cross-Model Transient Runtime Contract Extraction & Dual-Client Proof`.

Frozen executable qualification head:

`1909709e7a244b5d0ee53342a26bab74815c118c`

Exact-head GitHub Actions run:

`35278517691` -> `SUCCESS`.

Subsequent commits containing contract reconciliation, review-remediation documentation, qualification metadata or closeout metadata do not constitute a new executable qualification target unless runtime/client/test code changes again.

## Verdict

`QUALIFIED_NONPRODUCTION_MODEL_NEUTRAL_TRANSIENT_RUNTIME_DUAL_CLIENT_PROTOTYPE_NO_PRODUCTION_LIBRARY_OR_MODEL_ADMISSION`

The verdict is intentionally narrow. It qualifies one isolated shared-runtime prototype and its dual-client proof. It does not qualify production use in SWAP5 or ANIMO5.

## Evidence consumed

KT02 consumes the closed KT01 reuse prototype and its frozen executable evidence, including its negative reuse classifications. KT01 established that literal SWAP5 source reuse was generally inappropriate: zero candidates were classified `DIRECT_PORT`; reusable mechanics required ANIMO adaptation or design-level derivation.

KT02 also reconciled the current SWAP5 canonical against the frozen Status-A scientific production source authority used by KT01. Although the current SWAP5 canonical had advanced substantially, none of the six SWAP5 runtime/kernel files pinned by KT01 as reuse evidence had changed. Newer SWAP5 transactional-time-stepping documentation remains consistent with the same committed/candidate/scratch authority pattern.

## What the executable prototype proves

The frozen prototype provides one implementation of model-neutral mechanics for:

- exact bounded time-coordinate identity and ordering using the TIME02-style rational representation already exercised in KT01;
- opaque accepted-state authority with lineage, generation and exact accepted time;
- opaque trial-origin provenance bound to one accepted origin;
- private candidate calculation and explicit client-supplied admissibility;
- stale-lineage/generation/origin-time rejection before publication;
- atomic accepted-payload publication after successful transaction validation;
- rejection without accepted-state mutation;
- bounded retry in which each retry starts from accepted authority rather than rejected candidate state;
- private multi-substep interval progress with external publication only after exact requested-target completion;
- serialization-neutral accepted-only checkpoint/restore mechanics;
- worker-local scratch reset/isolation;
- a common abstract payload/client boundary that does not require the core to know model-specific physical fields.

## Dual-client evidence

The same runtime modules are compiled once and used by two materially different synthetic clients.

The SWAP-like client has a continuous real-valued physical payload and solver-shaped reject/retry behaviour. Its first attempt can be rejected and retried from the same accepted origin. The proof then advances through accepted substeps to the exact requested target and verifies checkpoint/restore continuation state.

The ANIMO-like client has two nonnegative integer stores and a client-owned conservative transfer between them. It uses guarded arithmetic and its own conservation admissibility decision. The shared runtime does not know the quantity meaning or conservation equation.

This supports the architectural claim that the transaction/interval machinery is not inherently a SWAP water-runtime mechanism or an ANIMO nutrient-runtime mechanism.

## Fail-closed and authority evidence

The tests cover at least the following negative paths:

- rejected first attempt with permitted retry;
- retry from the same accepted generation/time;
- stale candidate rejected after a different candidate has committed;
- incomplete interval after private internal progress leaves the external accepted store unchanged;
- invalid progress/target checks in interval orchestration;
- opaque accepted/trial/result components verified structurally;
- runtime core checked for absence of direct SWAP/ANIMO scientific module dependencies and selected leaked domain terms.

The accepted, trial and result carriers were hardened after adversarial review. That remediation was recompiled and retested on the frozen executable head.

## Review assurance

Review mode: `same-agent / not genuinely independent`.

Assurance label: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Initial review verdict was `NOT_YET_QUALIFIABLE` because accepted/trial authority was publicly mutable and other contract boundaries were insufficiently explicit. The material authority finding and the bounded contract findings were remediated. The post-remediation disposition is:

`SELF_REVIEW_PASS_NONPRODUCTION_DUAL_CLIENT_PROTOTYPE_ONLY`.

This assurance level is sufficient only for the isolated research prototype claimed here. A production shared runtime or model integration requires separate review and admission evidence.

## Explicitly not qualified

KT02 does not qualify or authorize:

- a separately versioned shared runtime package or repository;
- any dependency change in SWAP5 production;
- any dependency change in ANIMO5 production;
- migration of current SWAP5 REAL-valued production time to the exact prototype time representation;
- canonical ANIMO TIME admission;
- scientific process equations or process ordering;
- solver selection, convergence policy, temporal error estimation, step doubling, retry scale or timestep selection;
- model-specific conserved-quantity registries or tolerances;
- a generic atomic event/transfer sidecar publication contract;
- SWAP5-ANIMO typed hydrology transfer semantics;
- joint coupled timestep ownership or negotiation;
- file grammars, legacy restart formats or production serialization;
- distributed/service transport;
- B3 mutation, B4 opening, Status A or Status AA claims.

## Production-tree noninterference

KT02 is isolated under `prototype/kt02/`, `tests/kt02/`, `docs/kt02/`, `integration/animo-kt02/` and its dedicated workflow. Comparison against the closed KT01 branch base shows no ANIMO production `src/` file modification.

## Handoff

The qualified KT02 asset can now be consumed by central coordination as a nonproduction architecture/runtime proof.

The next scientifically useful step is not to create a generic package immediately. It is to test the contract against a real ANIMO boundary while preserving legacy ANIMO science. A subsequent workunit should therefore construct a real ANIMO adapter around one bounded legacy timestep/hydrology input path and verify that the model can be driven through the shared runtime without changing process equations or reference behaviour.

Only after that real-model adapter proof should repository/package extraction and SWAP5-ANIMO joint interval orchestration be reconsidered.