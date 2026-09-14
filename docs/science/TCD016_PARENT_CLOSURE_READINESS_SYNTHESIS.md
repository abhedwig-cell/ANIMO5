# ANIMO-B3B14 TCD-016 Parent Scientific Closure and Readiness Synthesis

Work unit: `ANIMO-B3B14`

Scope: closure/readiness synthesis only. This work unit performs no B3 admission, no model evolution, no production change, no TCD/register/queue/aggregate/routing mutation, no B4 action and no TB7 opening.

## GOV06 execution contract

Owned semantic contract: `TCD016_PARENT_READINESS_SYNTHESIS`.

Consumed frozen contracts are pinned to `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`, `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`, `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`, `ANIMO-GOV06@7a7d3a1f5a5c07bf36b7e6e2915338dabde20660`, `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`, `ANIMO-B3Q06@11e9bcdc6654e63f84875bf1f28dc54abe725700`, `ANIMO-RG05O@bc9e6ed997a078336645210ebb4d99ae976893fe`, `ANIMO-B3I10@942f26fe32eaf91679e59a1968ae173a3703e22d`, `ANIMO-SQ01@26d0c74aa440bd73c23709d313e24ea8af2a0bcd`, `ANIMO-SQ02@09ab76f0b44cb72956875fa379d68bbf97f1a0c7`, `ANIMO-SQ03@58dc3c5c108ee97fd6bea107b7a9e686596617b1`, `ANIMO-SQ04@063627cddd478904c437c9c47f02513ef0d9326b`, `ANIMO-SQ05@897ba742630f06381a2b89290db80d5f405ab51d`, `ANIMO-SQ06@2dbabfd5f57120c583645415e87f7eb792a8c0d7`, `ANIMO-SQ07@2076c0def17c504a3ba29db02d964d4a6238d2cf`, `ANIMO-SQ08@f89ec3b0bfd053c2c903cbbcf2243bb4ab4a5741`, and `ANIMO-MASSQ04@3e0f8254d9cd7966a4491b3068d0239b8ccda5f9`.

All consumed scientific semantics are `FROZEN` for this work unit. Aggregate, queue, routing, testbank composition, B4 and production authorities are not owned. Parallelism class is `PARALLEL_AFTER_PINNING`: this work unit composes immutable evidence and does not co-own shared moving authorities.

## Reconstructed parent definition

The canonical TCD register defines TCD-016 as `NH4 surface-layer dry-down mass conservation`. The scientific requirement is that dissolved ammonium cannot leave with evaporation and that conserved N mass must survive a wet-to-dry surface transition. The revision-53 failure occurs when layer 0 dries: `Transsub` sets `Rsc=0` and exports remaining solute only when `Fu>1e-6`; at the canonical Puitmijn event the remaining NH4-N is therefore removed from represented state, producing about `0.13880242022597 kg N ha-1` mass loss. The counterfactual tiny-outflow closure is scientifically unusable because it creates an extreme concentration. The register classifies this as `CONFIRMED_LEGACY_CODE_DEFECT_AND_STATE_MODEL_GAP` and requires an explicit conservative dry-down state to be defined and qualified.

SQ01 atomized the scientific problem into TCD-016-C1, the missing physical continuation-state/lifecycle problem, and TCD-016-E1, the numerical policy around the low-storage/export seam. E1 remains dependent on C1. No evidence after SQ08 creates another TCD-016 child. For parent readiness, C1 cannot be narrowed to storage bookkeeping alone because SQ01 and SQ02 explicitly include phase ownership, dry-hold semantics and remobilization/rewetting in the class-C scientific closure surface. E1 does not become independently ready while C1 lacks executable scientific lifecycle semantics.

## What is positively qualified

The original state-existence defect is real and causally localized. A finite areic continuation owner, `M_surface_NH4_non_aqueous_continuation` in `kg N m-2`, is scientifically acceptable as a chemically noncommittal conservation-state topology. It is independent of aqueous volume, is owned by the surface chemistry/ponding control volume, must be persistent and restartable if implemented, and may not be reconstructed from a balance residual. The mass ontology is explicit: `S_NH4 = S_aq + S_complex + S_cont`. All nonzero owner changes require typed transfers with a declared source, receiver or external sink, identity, activation, amount/rate, ordering and restart semantics.

SQ03 also qualifies a fail-closed no-process update, `M_cont_after=M_cont_before`, but only as epistemic state-persistence semantics. It is not a physical inertness law. SQ08 qualifies only an identity envelope: NH4-N provenance, areic mass coordinate, finite representation at zero water, and persistent physical-state ownership. It does not qualify a solid, adsorbed, aqueous-film, gas or fixed multiphase identity.

## Negative scientific knowledge

SQ04 establishes that revision-53 management volatilization, soil nitrification, soil NH4 sorption, `Conhtop`, and aqueous transport are not reusable unchanged as the continuation process or owner. SQ05 finds no explicit ANIMO 4.0 user-guide contract for a dry continuation phase or rewetting law. SQ06 closes the dry-hold search negatively: no concrete dry-hold physical process law is currently defensible, and conservative persistence may not be promoted to physical inertness. SQ07 closes the rewetting search negatively: no receiver, activation criterion or kinetics can be selected without adding unsupported phase, receiver, solubility, ordering or parameter semantics. SQ08 closes the identity search at a bounded noncommittal envelope and explicitly leaves phase/speciation unresolved.

These are closed scientific results, not unfinished searches. Repeating the same search without new material evidence or an explicitly authorized model-evolution assumption would be circular.

## Readiness hypotheses

`H1` fails. State ownership and mass closure are necessary but do not by themselves define a scientifically executable lifecycle. Treating fail-closed persistence as the B3 dry-process law would silently convert safety semantics into an inertness claim.

`H2` is supported, specifically for the continuation-to-rewetting lifecycle. A concrete dry transformation need not be invented merely to preserve state safely, but the parent correction cannot define post-rewet scientific behaviour while every receiver/activation/kinetics candidate remains unqualified. Indefinite retention is not a qualified physical alternative.

`H3` is only partly supported. Specific phase/speciation is not required to represent, conserve or restart the bounded continuation state, so its absence is not independently an admission blocker for those claims. It is, however, upstream of the missing rewetting/process contract because current evidence cannot map a physical transfer law without additional identity semantics.

`H4` is not a valid B3-readiness escape hatch. A narrower claim that only an explicit conserved continuation store exists is already a valid model-evolution topology qualification, but promoting that topology to the parent B3 scientific correction would silently narrow TCD-016-C1 relative to SQ01/SQ02 and would turn a fail-closed no-process guard into model behaviour. B3Q01 prohibits using conservation closure alone to waive poorly documented physics.

`H5` does not independently block closure: the known child set is compositionally reconstructed. The failure is scientific lifecycle completeness, not missing bookkeeping of an unknown child.

## Admission blocker test

State ownership, storage representation, elemental/species bookkeeping and restart coordinate are sufficient for capture, persist and restore. They are not sufficient for `continue` across rewetting because no scientific transfer from continuation storage to any receiving physical owner is qualified. That transfer is necessary for an executable corrected lifecycle, not merely a later enhancement. Therefore the residual uncertainty is admission-blocking.

Historical revision-53 behaviour remains `UNKNOWN_WITHOUT_B2`. Under GOV03/B3Q01, historical uncertainty can in principle be carried as residual uncertainty when the scientific behaviour is independently qualified. Here it is not the decisive blocker: the current scientific rewetting behaviour itself is unqualified. Historical uncertainty therefore remains explicit but is not promoted into either a fidelity claim or the primary blocker.

## Mass, state and restart synthesis

Capture is bounded by the wet-to-continuation conservation transfer. Persistence is explicit physical state, not an observer residual. Restore requires exact restoration of `M_surface_NH4_non_aqueous_continuation`; no hidden phase memory is qualified. The no-process guard is split-run deterministic because it is exact state persistence only. This is enough for a bounded state/restart contract, but not for a complete executable parent science contract because `continue` after rewetting has no qualified receiver or transfer law.

## Testbank synthesis

The SQ06 dry-hold negative fragment, SQ07 rewetting negative fragment and SQ08 identity fragment are reusable preservation evidence for the corresponding negative/identity claims. They do not compose into a positive executable parent oracle. The B3B14 fragment records only this readiness decision and may not be treated as a whole-model golden baseline or as TB7 composition authority.

## Decision

Primary disposition:

`QUALIFIED_TCD016_PARENT_NOT_READY_EXPLICIT_MODEL_EVOLUTION_DECISION_REQUIRED`

The minimal blocker is not another search over the same ANIMO evidence. To proceed without new material identity evidence, a separate explicitly authorized model-evolution work unit must choose and scientifically qualify a bounded continuation-material/rewetting assumption, including receiver, activation, transfer law or kinetics, ordering and falsification/parameter provenance as applicable. Alternatively, genuinely new material identity evidence may reopen the existing SQ08 unlock route. B3B14 itself authorizes neither path.

No B3 admission is performed here. The exact next handoff is a separate, explicitly authorized TCD-016 model-evolution decision/qualification work unit, unless new material identity evidence is supplied first.