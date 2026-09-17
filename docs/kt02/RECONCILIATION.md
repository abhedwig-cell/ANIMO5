# ANIMO-KT02 Reconciliation

Date: 2026-09-17

Phase: `RECONCILE`

## Existing-work check

No branch matching `kt02`, `transient` or an equivalent explicit cross-model runtime extraction workunit was found before branch creation. Existing runtime-related branches are model-specific ANIMO qualification workunits or the closed `ANIMO-KT01` reuse prototype.

KT02 therefore opens a new semantic decision surface rather than duplicating an existing workunit.

## ANIMO source state

KT02 starts from the closed KT01 branch head:

`ANIMO-KT01@df30e79a8785b4fd83746e80e7766935225e90d3`

KT01 froze its executable qualification target at:

`25819e08fa34676e8dddd0254c4539f6b4372b89`

with exact-head CI success and no ANIMO production `src/` diff from the governing authority. KT01 qualified only a nonproduction ANIMO-native runtime substrate prototype. It explicitly did not create a shared cross-model runtime library and did not admit B3, B4, production or canonical TIME.

The governing central ANIMO regie authority consumed by KT01 remains:

`ANIMO-GOV06@7a7d3a1f5a5c07bf36b7e6e2915338dabde20660`

## SWAP5 live delta

The SWAP5 canonical observed during KT02 reconciliation is:

`integration/f-ci-canonical@fc6c4e00d3b94f39dee5a30d68f4c6ef22385f9e`

The frozen Status-A scientific production source authority used by KT01 remains:

`50346642bd565f79134ea17d5462e544b354998c`

A live compare from that source authority to the current canonical shows the canonical is 357 commits ahead. The delta contains substantial documentation, application-host, solver-selection, adapter, publication and qualification additions.

Critically for KT02, none of the six SWAP5 source files pinned by KT01 as the runtime-reuse evidence set appear as modified in that compare:

- `src/transaction/mod_transaction_reference.f90`
- `src/kernel/mod_kernel_transactions.f90`
- `src/kernel/mod_kernel_committed_persistence.f90`
- `src/runtime/mod_canonical_contracts.f90`
- `src/runtime/mod_canonical_interval_runtime.f90`
- `src/runtime/mod_a23bu_worker_execution_context.f90`

Therefore the KT01 source-semantic pins for those files remain valid for the initial KT02 extraction analysis. The newer canonical must still be consulted for additional architecture evidence, but a wholesale requalification of the six frozen source files is not required at RECONCILE.

## New relevant SWAP5 evidence since KT01

The current canonical now contains a public architecture document `docs/numerics/transactional-time-stepping.md`. It states the same high-level transaction invariants relevant to KT02:

- committed state is accepted persistent authority;
- candidate state is tentative;
- scratch/workspace is disposable;
- rejected attempts must not leak into accepted state;
- retry begins from accepted authority;
- external publication follows accepted state;
- restart reconstructs committed state rather than arbitrary scratch;
- process/solver code must not silently become global execution policy.

This newer documentation is consistent with the frozen runtime mechanics consumed by KT01 and adds useful public architectural framing. It does not by itself authorize cross-model library extraction.

## KT01 extraction baseline

KT01 classified the examined SWAP5 runtime mechanics as:

- `DIRECT_PORT`: 0
- `PORT_WITH_ANIMO_ADAPTATION`: 3
- `DESIGN_ONLY`: 3
- `REJECT`: 6

That negative result is a design constraint for KT02. KT02 must not interpret cross-model reuse as literal source copying. The shared candidate must be a new neutral contract derived from common semantics, with model-specific assumptions left behind adapters.

## Reconciled decision

`PROCEED_TO_EXTRACT`

There is sufficient, non-conflicting evidence to begin a bounded cross-model extraction phase because:

1. KT01 independently demonstrated ANIMO-native transaction, interval, checkpoint and scratch-isolation mechanics without production mutation;
2. SWAP5 retains the corresponding frozen runtime mechanics and now documents the same transaction invariants publicly;
3. the relevant frozen SWAP5 core source files have not changed since the authority used by KT01;
4. no equivalent KT02 workunit was found;
5. the remaining scientific and numerical-policy differences are explicit and can be treated as adapter/policy exclusions rather than silently generalized.

## Next permitted action

Construct an explicit cross-model extraction matrix and candidate neutral contract. Do not yet modify ANIMO production source, SWAP5 source, B3/B4 state or create a separately versioned shared-runtime repository.