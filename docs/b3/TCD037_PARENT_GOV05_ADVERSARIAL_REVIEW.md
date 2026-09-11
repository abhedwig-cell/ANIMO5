# ANIMO-B3D27 — GOV05 adversarial review of TCD-037 parent composition

Reviewed immutable authoring head: `17387b7282a6f5b40fec290bd4c28cc6cef8f767`.

Assurance mode: `SINGLE_AGENT_ADVERSARIAL_REVIEW`.

Assurance strength: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

This review is deliberately not described as genuinely independent. It is a second-pass adversarial reconstruction under GOV05. The earlier authoring head `74711b4ce5ada0e8748014dff0f7c131bdde96ad` was not reviewed to disposition: a pre-review challenge found that the new composition claim lacked its own executable bounded oracle. The authoring surface was therefore remediated and refrozen at the exact head above before this review began.

## Adversarial reconstruction

The strongest incorrect alternative is to restore one profile array per gas and infer index 0 from the layer values. That fails for both gases. CH4 layer formation and top-boundary exchange are different quantities, while the legacy index-0 surface is overloaded between `CH4e` atmosphere exchange and the formation-side `CO2e` complement. N2O has an even clearer collision: profile production cannot own a field labeled total atmosphere emission because the model contains dynamic gas state and an explicit reduction sink.

A second tempting alternative is to interpret all fields carrying an `e` suffix as nonnegative emission. The frozen GHG source contradicts that interpretation. Both CH4 and N2O atmosphere rates are signed, with negative values explicitly defined as uptake by the soil. The parent package preserves that sign and the exact-rational oracle changes only the atmosphere field when the atmosphere tuple is sign-flipped.

A third alternative is to close a same-timestep gas balance by forcing formation to equal atmosphere exchange. That is rejected. CH4 can be stored or oxidized before atmosphere transfer. N2O can be stored or reduced to N2. The parent package correctly refuses any formation-equals-emission theorem and makes no complete GHG carbon or N2O ledger claim.

## Claim-by-claim attack

### Child completeness

A1 covers CH4 layer formation. A2 covers the CH4 profile semantic split. A3 covers layer denitrification N2O formation. A4 covers total atmosphere N2O exchange. The apparently missing N2O nitrification surface is not missing: its local scratch producer is built before use and its existing reporting threshold was explicitly excluded from TCD-037. `QRdN2O` is a separate reduction sink, not a fifth observer producer. No fifth child is justified.

### Cross-child overlap and double counting

A1 and A2 intentionally share the CH4 formation quantity only through the layer-to-profile sum used for the formation-side dissimilation complement. The atmosphere `CH4e` term has an independent boundary owner. A3 and A4 concern the same species but different process locations. No destination field receives two competing owners. The parent package does not define a cross-element GHG total, so CH4 organic-matter-basis terms cannot be accidentally added to N2O nitrogen-basis terms.

### Units and names

The most misleading name is `CO2e`. In this balance context it is not a climate CO2-equivalent metric. The CH4 amount is converted from `kg C m-2` to the organic-matter balance basis through `Cfracom` and the hectare factor. N2O remains on an N mass basis. The package states this explicitly and therefore does not promote a unit/name ambiguity into a scientific claim.

### Lifetime, state and restart

The corrected observer inputs are timestep rates converted to timestep amounts. They are not new persistent state. The invalid legacy locals do not gain an invented lifetime. No physical state or process flux is changed. A parent-level restart theorem would require separate evidence about reporting-accumulator serialization; the package does not make that claim. This is a bounded nonclaim, not a hidden pass-by-assumption.

### Conservation and accounting

The parent correction improves ownership of observer increments only. It does not claim whole-model conservation, complete gas closure or a whole-model golden baseline. This boundary is scientifically necessary because formation, oxidation/reduction, storage and atmosphere transfer are separate terms.

### Adjacent discrepancies

No term required for the parent mapping is owned by TCD-032 through TCD-036. The four child admissions already exclude those domains, and the parent package keeps them as noninterference exclusions. No contradictory evidence was found that would require reopening any child admission.

### Historical strength

The parent exact-rational oracle is a composition proof only. It is not a historical runtime reference, not natural active-GHG evidence and not B2. Child historical uncertainty is therefore preserved rather than silently upgraded.

## Parent-level oracle challenge

The bounded oracle deliberately makes formation and atmosphere exchange unequal, flips atmosphere signs independently, changes formation independently, changes N2O denitrification independently, preserves nitrification/reduction sentinels, and verifies rate-time amount equivalence. It also defines no `ghg_total` or climate `CO2e` output. These are exactly the failure modes a bad parent composition would collapse.

The oracle is not sufficient by itself to prove source semantics. That source semantics is reused from the exact-pinned RUNTIMEQ03 and child admissions under `VERIFY_AND_REUSE`. Its role is narrower: to prove that the new parent conjunction is internally coherent and interaction-safe.

## Risk review

The strictest applicable trigger is composition. Tier A is unavailable because the decision is no longer atomic. The parent combines four admitted atoms and shared layer/profile/boundary accounting semantics. GOV04 Tier D therefore applies. No production or B4 trigger is present, so the remaining Tier-D stages stay separate and unperformed.

## Review disposition

All challenged predicates remain supported after the second pass. No substantive correction to the refrozen authoring surface is required.

Disposition:

`PASS_GOV05_SINGLE_AGENT_ADVERSARIAL_PARENT_COMPOSITION_REVIEW_NOT_INDEPENDENT`

The exact reviewed authoring head is ready for a separate persisted parent-integration/admission closeout surface. This review does not itself admit TCD-037, update RG05I, authorize B4 or authorize production migration.
