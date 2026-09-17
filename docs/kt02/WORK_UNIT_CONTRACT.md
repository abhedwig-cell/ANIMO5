# ANIMO-KT02 Work Unit Contract

Workunit: `ANIMO-KT02 — Cross-Model Transient Runtime Contract Extraction & Dual-Client Proof`

Execution discipline: `RECONCILE -> EXTRACT -> PROTOTYPE -> QUALIFY -> CLOSE`.

This is a bounded architecture/runtime-reuse workunit. It has no B3, B4 or production ADMIT phase.

## Purpose

KT02 tests whether runtime mechanics now independently evidenced in SWAP5 and ANIMO-KT01 can be represented once as a scientifically neutral transient-model substrate, without making either model the owner of that substrate and without importing model-specific physics or numerical policy.

A positive KT02 result may qualify only a nonproduction cross-model contract and executable dual-client proof. It does not create a production shared library and it does not migrate SWAP5 or ANIMO5 production code.

## Consumed authorities

- ANIMO central regie authority: `ANIMO-GOV06@7a7d3a1f5a5c07bf36b7e6e2915338dabde20660`
- qualified ANIMO reuse prototype close head: `ANIMO-KT01@df30e79a8785b4fd83746e80e7766935225e90d3`
- KT01 frozen executable qualification target: `25819e08fa34676e8dddd0254c4539f6b4372b89`
- ANIMO candidate exact-time authority consumed by KT01: `ANIMO-TIME02@b4d78cf32cb149cf50aa2b0a0fbefee571eee6b8`, with canonical time admission still false
- SWAP5 current canonical observed at KT02 reconcile: `integration/f-ci-canonical@fc6c4e00d3b94f39dee5a30d68f4c6ef22385f9e`
- SWAP5 frozen Status-A scientific production source authority used by KT01: `50346642bd565f79134ea17d5462e544b354998c`

The current SWAP5 canonical is newer than the scientific production source authority. KT02 must distinguish documentation/application/runtime additions from changes to the previously pinned reusable kernel/runtime source. Reuse evidence is refreshed only where relevant source semantics changed.

## Owned semantic surface

KT02 may own only a nonproduction, model-neutral contract and proof implementation for:

- exact interval identity and ordering;
- accepted, trial/candidate and checkpoint authority separation;
- atomic publication and rejection/rollback mechanics;
- provenance, lineage and stale-origin protection;
- committed-only persistence envelopes without storage I/O;
- private interval execution with publication only after complete requested interval;
- worker-local scratch isolation;
- externally supplied acceptance/admissibility decisions;
- model-neutral execution outcomes and bounded failure states.

KT02 may use two synthetic adapters/clients, one SWAP-like and one ANIMO-like, solely to prove that the same substrate can serve materially different transient model shapes without embedding either model's science.

## Must not own

KT02 must not own or choose:

- scientific process equations or process ordering;
- Richards/HeadCalc, nutrient, carbon, phosphorus, nitrogen, crop, snow, groundwater or surface-water physics;
- solver choice, nonlinear convergence rules, temporal error estimator, step-doubling, retry scaling or timestep policy;
- model-specific conservation quantities, tolerances or balancing corrections;
- SWAP or ANIMO file grammars and legacy persistence formats;
- hydrology-to-ANIMO coupling payload content beyond a future typed-interface placeholder;
- calendar conversion policy not already justified by the time contract;
- distributed transport, REST, sockets, cloud execution or service deployment;
- production restart schema;
- production dependencies of SWAP5 or ANIMO5;
- Status A or Status AA claims.

## Extraction rule

A mechanic is eligible for the shared substrate only if all of the following hold:

1. it is evidenced independently by at least two model contexts or by one model plus a scientifically neutral qualification prototype;
2. its contract can be stated without SWAP-specific or ANIMO-specific scientific fields;
3. it does not choose scientific or numerical acceptance policy;
4. it can fail closed when required information is absent;
5. both synthetic clients can use the exact same implementation rather than forked copies.

If a candidate mechanic requires model-specific assumptions, KT02 must classify it as `ADAPTER_OWNED`, `DESIGN_ONLY` or `REJECT`, not force it into the shared core.

## Dual-client proof requirement

A positive KT02 qualification requires one executable substrate implementation and two materially different clients:

- a SWAP-like client with continuous physical state, solver-style diagnostics and retry-capable interval execution;
- an ANIMO-like client with multiple conserved stores and transfer/event style accounting.

The clients may define their own state payloads and admissibility inputs. They may not duplicate or modify the transaction, time, commit/rollback or interval-execution core.

The proof must include at least:

- commit succeeds once from the exact accepted origin;
- stale lineage/revision/origin-time commit rejects;
- rejected trial leaves accepted state unchanged;
- retry starts from the same accepted origin;
- incomplete interval execution publishes nothing externally;
- exact target completion publishes once;
- checkpoint contains accepted continuation state only;
- worker scratch never enters checkpoint or accepted state;
- both clients pass the same substrate-level conformance suite;
- static checks demonstrate absence of SWAP5 and ANIMO scientific module dependencies in the substrate core.

## Coupling preparation boundary

KT02 may define the minimal future shape of a coupled interval participant contract, for example `prepare/attempt -> assess -> commit or reject`, but may not implement a SWAP5-ANIMO production coupling. A later workunit must qualify coupled ownership of time, joint acceptance and typed hydrology transfer semantics.

## Shared-library boundary

KT02 must not create a separately versioned production library or repository. The first goal is to prove a stable shared contract inside an isolated prototype. Repository/package extraction is a later decision after the dual-client proof shows that no model-specific leakage is required.

## Fail-closed rule

Any abstraction that weakens either model's state authority, imports hidden scientific policy, invents ANIMO science, changes SWAP5 production semantics, or requires duplicate model-specific forks of the supposed shared core is a failed extraction candidate.