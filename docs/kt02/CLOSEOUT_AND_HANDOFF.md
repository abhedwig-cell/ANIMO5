# ANIMO-KT02 Closeout and Handoff

## Final disposition

ANIMO-KT02 is closed as a qualified nonproduction model-neutral transient-runtime dual-client prototype.

Exact verdict:

`QUALIFIED_NONPRODUCTION_MODEL_NEUTRAL_TRANSIENT_RUNTIME_DUAL_CLIENT_PROTOTYPE_NO_PRODUCTION_LIBRARY_OR_MODEL_ADMISSION`

This closes the bounded architecture/reuse workunit. It does not admit the prototype into ANIMO5 or SWAP5 production and does not create a production shared library.

## Frozen executable qualification target

- branch: `work/animo-kt02-cross-model-transient-runtime`
- frozen executable head: `1909709e7a244b5d0ee53342a26bab74815c118c`
- exact-head GitHub Actions run: `35278517691`
- result: `SUCCESS`
- base: closed `ANIMO-KT01@df30e79a8785b4fd83746e80e7766935225e90d3`
- ANIMO production `src/` modification in KT02: none

Later KT02 commits after the frozen executable head contain only contract/review/qualification/closeout metadata unless explicitly stated otherwise.

## What changed conceptually

KT01 showed that selected SWAP5 transaction/runtime ideas could be reproduced in an ANIMO-native prototype, but also showed that direct source reuse was generally the wrong abstraction. KT02 takes the next step: the shared mechanics are no longer named or structured as ANIMO-specific runtime code.

The prototype now has model-neutral runtime modules and two separate clients. A SWAP-like continuous-state client and an ANIMO-like multi-store conservation client both use the same transaction, time, interval, persistence and scratch-isolation implementation.

The executable proof therefore supports a real architectural distinction:

- the shared substrate owns authority transitions and interval mechanics;
- model adapters own physical state meaning, process calculation and admissibility;
- scientific and numerical policy remains outside the substrate.

## Review result

The first executable version was not accepted immediately. Same-agent adversarial review identified a material authority defect: accepted/trial carriers were publicly mutable and provenance could be forged by cooperative client code.

The prototype was hardened so that accepted state, trial origin and result provenance are opaque. Contract mismatches around target ownership and client-object authority were also reconciled, and the ANIMO-like synthetic conservation arithmetic was guarded against overflow. The remediated executable was then recompiled and retested successfully.

Review assurance remains:

`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`

Post-remediation review disposition:

`SELF_REVIEW_PASS_NONPRODUCTION_DUAL_CLIENT_PROTOTYPE_ONLY`

That is sufficient for this research prototype only, not for production admission.

## Qualified shared-core surface

KT02 qualifies, within the frozen prototype envelope:

- accepted/candidate authority separation;
- lineage, generation and exact origin identity;
- private trial execution;
- stale-origin rejection;
- atomic accepted-payload publication or no publication;
- bounded retry from accepted authority;
- private interval progress and exact-target publication;
- bounded exact time identity/order mechanics;
- accepted-only serialization-neutral checkpoint/restore;
- worker-local scratch isolation;
- externally supplied complete/admissible decision;
- one abstract physical-payload/client seam used by two materially different proof clients.

## Deliberately not generalized

The following remain outside the shared core because generalizing them now would either import model-specific science or claim evidence that does not yet exist:

- conserved-quantity registries and tolerances;
- ANIMO transfer/event-ledger semantics;
- SWAP water-balance fields;
- solver convergence and diagnostics;
- retry scale, step doubling and timestep selection;
- forcing payload structure;
- calendar conversion;
- model file grammars and production restart codecs;
- hydrology-to-ANIMO data semantics;
- network or service transport.

The exact time implementation is qualified only as a shared nonproduction candidate. Current SWAP5 production has not thereby migrated away from its admitted production time representation.

## Why no separate shared-library repository yet

KT02 proves that a neutral implementation can serve two synthetic model shapes. It does not yet prove that the abstraction remains clean when attached to real ANIMO production-era state and legacy input semantics.

Creating a separately versioned runtime package now would therefore freeze an abstraction one step too early. The stronger next test is a real-model adapter.

## Next workunit

The next permitted work should be a separate real-ANIMO adapter workunit. Its purpose is to connect one bounded, real ANIMO timestep/hydrology boundary to the qualified KT02 runtime without changing ANIMO scientific equations.

That workunit should, at minimum:

1. identify one exact legacy timestep input boundary, preferably the hydrology information historically consumed from SWAP/SWATRE data;
2. define a typed ANIMO adapter representation for that boundary without redesigning the science;
3. keep legacy file reading behind an adapter so the same scientific kernel can be driven by file-backed or in-memory typed input;
4. represent real ANIMO accepted continuation state through an explicit adapter rather than copying the KT02 synthetic payload;
5. run a bounded legacy case through the adapter and compare it with the existing reference/testbank evidence;
6. prove that reject/retry or interval orchestration does not leak hidden ANIMO state outside the accepted payload;
7. keep SWAP5 production coupling out of scope until this standalone ANIMO adapter proof succeeds.

Only after that real ANIMO proof should we decide whether to extract the neutral runtime into its own package/repository and whether to open a separate SWAP5-ANIMO joint interval-orchestrator workunit.

## Authoritative KT02 evidence set

- `docs/kt02/WORK_UNIT_CONTRACT.md`
- `docs/kt02/RECONCILIATION.md`
- `docs/kt02/SHARED_RUNTIME_EXTRACTION_MATRIX.csv`
- `docs/kt02/CANDIDATE_SHARED_RUNTIME_CONTRACT.md`
- `docs/kt02/ADVERSARIAL_REVIEW.md`
- `docs/kt02/ADVERSARIAL_REVIEW_REMEDIATION.md`
- `docs/kt02/QUALIFICATION_REPORT.md`
- `docs/kt02/CLOSEOUT_AND_HANDOFF.md`
- `integration/animo-kt02/ANIMO-KT02_STATUS.json`
- `integration/animo-kt02/ANIMO-KT02_CHECKPOINT.json`
- `prototype/kt02/runtime/`
- `prototype/kt02/clients/`
- `tests/kt02/`
- `.github/workflows/animo-kt02-cross-model-runtime.yml`
