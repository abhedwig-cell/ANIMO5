# ANIMO-KT01 Qualification Report

## Qualification target

Frozen executable authoring head: `25819e08fa34676e8dddd0254c4539f6b4372b89`

Exact-head CI: GitHub Actions run `35043168090`, job `104627245057`, result `SUCCESS`.

Review: Review 2 in `docs/kt01/REVIEW.md` and `integration/animo-kt01/ANIMO_KT01_ADVERSARIAL_REVIEW.json`.

Review mode: `same-agent / not genuinely independent`.

GOV05 assurance: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

## Verdict

`QUALIFIED_NONPRODUCTION_ANIMO_NATIVE_TRANSACTION_AND_INTERVAL_RUNTIME_SUBSTRATE_REUSE_PROTOTYPE_NO_B3_B4_OR_PRODUCTION_ADMISSION`

This qualification is intentionally narrow. It qualifies the isolated executable mechanics under `prototype/kt01/` against the frozen ANIMO authorities and exact SWAP5 source provenance recorded by KT01. It does not admit any scientific process or production implementation.

## Reuse classes materialized

### PORT_WITH_ANIMO_ADAPTATION

Three classified source responsibilities were materialized as ANIMO-native control structure:

1. Transaction publication mechanics from SWAP5 `src/kernel/mod_kernel_transactions.f90`, adapted to ANIMO lineage/generation, exact TIME02 candidate coordinates, explicit trial provenance, supplied generic conservation acceptance and a separately owned committed event ledger.
2. Committed-only persistence mechanics from SWAP5 `src/kernel/mod_kernel_committed_persistence.f90`, adapted to ANIMO checkpoint-schema, state-layout, configuration and feature-layout identities plus exact time, while excluding event history and all trial/scratch state from physical continuation.
3. Private interval-working-state/final-publication mechanics from SWAP5 `src/runtime/mod_canonical_interval_runtime.f90`, adapted to exact time, private physical and event-ledger progress, test-only retry permission and exact requested-target completion.

### DESIGN_ONLY

The neutral runtime-contract separation, transaction clone/retry isolation pattern and worker-owned scratch/reset lifecycle were used as architecture evidence and implemented as newly written ANIMO-native structures. They are not literal source ports.

### DIRECT_PORT

None. No inspected SWAP5 executable element met the strict no-semantic-adaptation definition.

### REJECT retained

The prototype does not import SWAP floating-time identity/progress, retry scaling, step-doubling, solver fallback policy, water-specific balance acceptance, HeadCalc/Richards payload, hydraulic or groundwater sensitivity, SWAP calendar assumptions, SWAP file formats, SWAP execution classes or SWAP persistent physical-state layout.

## Qualified mechanics

Within the bounded prototype envelope, qualification covers:

- accepted physical origin isolated from private trials;
- retry from the same authoritative accepted origin after an admissibility rejection;
- atomic commit of physical postimage and a separately owned event-ledger postimage;
- exactly one generation advance per successful commit;
- fail-closed lineage, stale-generation and exact-origin-time checks;
- rejected-event isolation;
- worker/job-local scratch reset and model-to-model isolation;
- generic multi-quantity, control-volume-labelled acceptance input without runtime-selected scientific tolerances;
- exact normalized rational candidate-time identity, ordering and bounded arithmetic without REAL equality, epsilon, ULP or unchecked cross multiplication;
- accepted-only physical checkpoint/restore mechanics with explicit compatibility identities;
- exact split-run/restart continuation mechanics in synthetic evidence;
- private accepted internal interval progress with no external publication before exact requested-target completion;
- fail-closed invalid progress, failed retry permission, exhaustion, capacity and nonrepresentability paths;
- no file I/O or hidden mutable SAVE state in the prototype kernel path;
- no runtime dependency on SWAP5 modules;
- no modification under ANIMO `src/` relative to the frozen GOV06 base.

## Evidence boundary

The executable tests cover the requested properties plus additional negative controls. The final test matrix is `docs/kt01/PROTOTYPE_TEST_MATRIX.md`. Structural checks pin all six exact SWAP5 blobs and enforce production-tree and dependency boundaries.

The restart test is synthetic transaction-runtime evidence. It is not evidence of historical revision-53 restart behavior and does not create B2 authority.

The time backend uses bounded signed `int64` arithmetic. TIME02 mathematical-integer semantics have not been reduced: values or operations outside the executable representation envelope fail closed. The prototype pipe serialization is an exact executable round-trip harness only and is not claimed as TIME02 canonical JSON.

## Governance state after qualification

- `canonical_time_admission = false`
- `B3_admission_changed = false`
- `B4_opened = false`
- `production_opened = false`
- `ANIMO_Status_A_claimed = false`
- `ANIMO_Status_AA_claimed = false`
- `B2_historical_reference_created = false`
- `SWAP5_dependency_at_runtime = false`
- `shared_cross_model_library_created = false`

SWAP5 Status-A remains source provenance and design evidence only. No SWAP5 scientific or release authority transfers to ANIMO5.

## Residual boundaries

KT01 does not qualify arbitrary-precision production time storage, canonical TIME serialization, a final ANIMO conserved-quantity registry, scientific tolerances, process equations, process ordering, real forcing adapters, coupled-owner transaction protocol, production restart format or production encapsulation choices.

The review is same-agent and therefore carries lower independence assurance than a genuinely independent review. The qualification claim is not widened to compensate for that limitation.
