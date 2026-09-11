# ANIMO-B3D22 — TCD-031 Tier-C Formal Disposition

## Scope

This workunit records the formal scientific disposition for TCD-031 after the completed targeted Tier-C rereview. It does not perform B3 admission, modify production source, change the frozen B0, update the canonical TCD register, compose TCD-025, or authorize B4 or migration.

The exact authoring base is `ANIMO-B3B10R2@7648e7b2813f3abc5904e4c34e36072d81d9844f`. The current aggregate at opening is `ANIMO-RG05H@3e4247928bb43f30def951fa8804560636affbef`.

A live governance recheck found an important transition that the first B3D22 checkpoint had missed: `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904` had already qualified with exact-head CI run `34546470484` before B3D22 authoring. B3D22 therefore uses GOV05 as current review governance. The stale initial observation is corrected explicitly rather than hidden.

This does not invalidate or relabel B3B10R2. GOV05 is prospective and explicitly preserves completed GOV04 reviews. B3B10R2 completed before GOV05 qualification and keeps its original genuinely independent GOV04 process status. It is not converted into a same-agent review and no new review is required merely because the governance model changed afterward.

## Scientific finding

The scientific object that a later admission workunit may accept is one atomic restart-state correction:

`COMPLETE_ACCEPTED_MACROPORE_SOLUTE_STATE_TRANSFER_ACROSS_RESTART_BOUNDARY`

The accepted persistent ANIMO solute owner is the `CoMp*` family for both macropore domains. Without phosphorus this is eight persistent scalars. With phosphorus active under `IPO.EQ.1`, `CoMpDiorPo(1:2)` and `CoMpPo(1:2)` add four scalars, giving twelve.

The frozen revision-53 evidence establishes the defect mechanism at claim scope. The active `Output_Init` path does not serialize the macropore solute continuation state. The active `Animo` call surface likewise omits the macropore arguments. `Init` then promotes `RsCoMp*` into `CoMp*`. No native valid restart load or initialization of the six `RsCoMp*` result families exists before the relevant promotion. A restart can therefore omit accepted state and can overwrite restored `CoMp*` unless the result alias is made consistent with the restored accepted state.

The correction must contain both sides of the boundary. Every enabled accepted `CoMp*` coordinate must be serialized and restored exactly, and the non-independent `RsCoMp*` result alias must be initialized from restored `CoMp*` before any legacy result-to-start promotion can execute. `AvCoMp*`, `AvCoML*` and `MpReKo*` remain current-interval workspace and are reconstructed, not checkpointed. Compatible external hydrology state remains a prerequisite for restore and resume.

A serializer-only change is not sufficient. A restore-direction-only change is also not sufficient. Splitting these into separate scientific corrections would break the reviewed atomic identity.

## Evidence boundary

ANIMO-STATEQ04 qualified the candidate accepted-boundary restore transaction with all six species families, both macropore domains, native-bad and domain-drop causal controls, a fresh Stage-B process and exact bytewise comparison without numerical tolerance. ANIMO-B3B10R2 independently closed the source/provenance gates that had caused the first B3B10R review to fail closed.

This is enough for a claim-scoped formal B3 disposition. It is not evidence of whole-model active production split equivalence. Whole-model production restart equivalence, migration readiness and whole-model checkpoint validation remain not proven. Those claims require later production-bound evidence and cannot be inferred from this disposition.

## Historical uncertainty

No qualified historical B2 reference is available. Under GOV03, historical revision-53 active macropore restart behaviour remains `UNKNOWN_WITHOUT_B2`. Source reconstruction establishes what the frozen source does structurally; it does not reconstruct historical user intent or native historical manifestation.

The formal disposition is:

`HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY`

The eligible route for a later atomic admission is:

`INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY`

The route name comes from the unchanged B3Q01 schema. Under GOV05 that legacy field name does not imply that future same-agent reviews are independent. In this particular lineage, however, the pinned B3B10R2 review really was completed under the older GOV04 process and retains that historical assurance.

## Tier C and admission separation

TCD-031 remains Tier C because the claim directly concerns persistent state ownership, restart/cold-start discrimination, initialization semantics and checkpoint lifecycle. GOV05 preserves the GOV04 scientific gates and strictest-trigger logic while changing only the review-process assurance model. No Tier-D composition or production-bound trigger is introduced here. There is no solver, tolerance or numerical-policy change.

B3D22 remains disposition-only. This is conservative and consistent with the pre-existing Tier-C state/restart pattern. GOV05 does not require collapsing disposition and admission into one workunit, and its user-zero-intervention workflow allows a disposition or admission only when the preceding scientific gates are satisfied. A separate B3D23 admission therefore remains the clean next decision surface.

No production patch follows automatically from scientific admission.

## Expected difference surface

A future implementation of the admitted correction may change resumed active-macropore solute concentrations and their causally downstream transport, exchange, state, fluxes, balances and outputs where the native restart path omitted or overwrote accepted state. It must not change continuous unsplit semantics away from checkpoint/restore paths, cold-start `INITIAL.INP` mapping, the two-domain physical meaning, the `IPO.EQ.1` phosphorus guard, external hydrology ownership, current-interval workspace ownership, numerical precision policy, solver/tolerance policy or frozen B0 identities.

## TCD-025 boundary

TCD-025 is not executed or composed here. The passed TCD-031 review may be consumed as a certified dependency by a separate Class-A ledger-readiness workunit, but that downstream readiness remains its own scoped workunit.

## Decision

`QUALIFIED_TIER_C_FORMAL_DISPOSITION_READY_FOR_SEPARATE_B3_ADMISSION_DECISION`

This decision becomes current B3D22 authority only after the remediated governance-aware package passes exact-head CI.
