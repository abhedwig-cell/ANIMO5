# ANIMO-GHG01 — B3 discrepancy and governance handoff

Status: `POST_CLOSEOUT_HANDOFF_PERSISTED_NO_CANONICAL_TCD_ALLOCATION`

This handoff packages the source-confirmed and theory-source reconciliation findings from ANIMO-GHG01 for later B3 and RG02 reconciliation. It does not reopen the GHG01 qualification, allocate canonical TCD numbers, repair revision-53 source, or admit production migration.

## Governance boundary

Live RG02 evidence at initial handoff time identified `work/animo-rg02-branch-authority-integration@27231ac9e52380c4ec10c9cf8e1cff5b72711e96` as the active branch-authority integration line. Its local-TCD reconciliation states that the qualified B3Q01 canonical register ends at `TCD-027`, with only a separate `TCD-028` reservation observed. Post-027 identifiers created on evidence branches are not canonical unless allocated through the B3 governance line.

Therefore this document uses GHG01-local finding keys only.

Existing canonical GHG discrepancies remain distinct:

- `TCD-008`: GHG theory/version documentation gap;
- `TCD-013`: GHGMais versus revision-53 input-contract lineage mismatch.

Neither identifier is broadened here to absorb newly found conservation, observer or equation-reconciliation findings.

## GHG01 local candidate findings

### `GHG01-LCL-METHANOGENESIS-SOURCE-POOL-TRANSFER`

Classification: `SOURCE_CONFIRMED_INCOMPLETE_PHYSICAL_TRANSFER_PATH`

Revision-53 CH4 production can draw carbon from DOM, exudates, humus and fresh organic-matter fractions. A separate active DOM depletion path exists in `Rates2`, but the intended comprehensive `GHG_Miner` calls in `resp_miner.for` are commented out. No equivalent active source-pool depletion path was found for the exudate, humus and fresh-organic-matter CH4 contributions.

The same inactive `GHG_Miner` route contains the intended coupling of methanogenesis and CH4 oxidation to GHG CO2/subsidence accounting. The CO2/subsidence producer-path observation is therefore retained as a dependent subfinding of this root transfer-path issue rather than allocated a separate local candidate.

Impact boundary: source structure permits an incomplete C-transfer chain if the GHG branch is activated. Numerical magnitude and historical executable behaviour remain unqualified because no revision-53-compatible historical GHG case and no qualified historical reference executable are available.

Recommended B3 treatment: separate from TCD-008 and TCD-013; candidate for canonical discrepancy allocation after independent source review and activated-case reproduction.

### `GHG01-LCL-GHG-OUTBAL-WORKING-ARRAYS`

Classification: `SOURCE_CONFIRMED_BALANCE_OBSERVER_INTERFACE_DEFECT`

`Outbal_calc.for` declares and consumes `AmCH4` and `AmN2Odeni`, but these arrays are not arguments of `Outbal_calc` and no active assignment under those symbols was found. The physical GHG process variables available elsewhere are different arrays, including `QPrCH4`, `QPrN2Oden`, gas states and emission fluxes.

`AmN2Onitr` is different: it is calculated locally in `Outbal_calc`. This asymmetry makes the CH4 and denitrification-N2O observer terms specifically suspect rather than the complete GHG output family generically unimplemented.

Impact boundary: source-confirmed observer/interface defect. Historical printed values and numerical magnitude are `REFERENCE_BLOCKED` and must not be inferred from unqualified compiler-local-storage behaviour.

Recommended B3 treatment: candidate for a distinct canonical discrepancy because this is a balance-observer defect, not a theory-lineage or parser-lineage issue.

### `GHG01-LCL-GAS-STORE-CN-CONTROL-VOLUME`

Classification: `MODEL_WIDE_CONSERVATION_CONTROL_VOLUME_GAP`

Revision 53 has dynamic physical gas stores for CH4-C and N2O-N. The standard organic-C and mineral-N balance residuals do not include these gas stores as canonical start/end state. The nutrient ledgers can therefore be internally meaningful only as smaller control volumes that treat conversion to gas as leaving those particular ledgers. They are not sufficient as a model-wide C/N conservation proof once GHG state is active.

This finding must not automatically be classified as a legacy physics defect. The unresolved question is whether the historical public balances intentionally used smaller control volumes. For ANIMO5, however, a model-wide MassLedger must include CH4-C and N2O-N storage and explicit atmosphere-boundary transfers.

Recommended B3/architecture treatment: retain as a control-volume and state-ownership qualification requirement. Allocate a canonical TCD only if B3 governance decides that revision-53 claimed a model-wide balance that is contradicted by this scope.

### `GHG01-LCL-N2O-NITRIFICATION-TEMPERATURE-SIGN-DOC-SOURCE`

Classification: `DOCUMENT_SOURCE_SIGN_CONFLICT_UNRESOLVED`

Peer-reviewed ANIMO-specific 2011 Appendix A17 represents the nitrification N2O-fraction temperature response with a Q10-ratio factor raised to `(T-Tref)/10`, while frozen revision 53 uses `2**(-(Te-Terf)/10)` in `FracN2Onitr`.

This is a direct document-source difference but is not yet a qualified code defect. Revision-53 source explicitly cites Maag & Vinther (1996), and the experimental literature is consistent with a decreasing N2O fraction from nitrification as temperature rises. A publication notation issue, source evolution, or different definition of the response factor therefore remains plausible.

Required B3 treatment: retain separately from generic TCD-008 and require the detailed Hendriks ANIMO GHG derivation, authoritative Report 2054 bytes or equivalent change history before scientific disposition.

### `GHG01-LCL-N2O-REDUCTION-AERATION-FACTOR-DOC-SOURCE`

Classification: `DOCUMENT_SOURCE_AERATION_FACTOR_PLACEMENT_CONFLICT_REQUIRES_DETAILED_AUTHORITY`

Peer-reviewed ANIMO-specific 2011 Appendix A11, as printed, does not include the denitrification aeration response factor in the numerator of the N2O reduction term, while its denominator does contain the factor. Frozen revision 53 constructs `RatFacN2O` from pH, temperature, aeration and electron affinity and uses the combined factor in its reduction partition.

The discrepancy is potentially material because aeration changes competition between N2O production and reduction. It is nevertheless not safe to choose one formulation as authoritative without the detailed derivation or version/change history.

Required B3 treatment: independent algebra/unit review plus detailed-authority recovery before any corrected-legacy decision.

## 2011 theory-authority consequence

Post-closeout web research recovered strong peer-reviewed ANIMO-specific N2O equation authority in Stolk et al. (2011), Vadose Zone Journal, DOI `10.2136/vzj2010.0029`, and Stolk et al. (2011), Biogeosciences, DOI `10.5194/bg-8-2649-2011`.

The Biogeosciences paper explicitly distinguishes the original equilibrium ANIMO N2O concept from a later mobile-immobile aggregate extension. The original concept matches revision-53 state and transport structure closely. Exact/algebraic source matches were found for the N2O Bunsen-equilibrium state relation, combined gas/water diffusion, nitrification production and WFPS response, denitrification pH response, the Q10=2.6 relative temperature response and the aeration-response relation. See `GHG_THEORY_AUTHORITY_RECOVERY_2011.md`.

This narrows TCD-008 materially for N2O, but does not close the release-specific documentation gap. It also exposes the two relation-level conflicts above, which must not be hidden inside a generic `SOURCE_ONLY` label.

## Required activated-case evidence

Before either source defect is admitted to corrected-legacy or production work, obtain a revision-53-compatible GHG case without silently translating GHGMais and record at minimum:

1. branch reachability for both `GHGasses(1)` and `GHGasses(2)`;
2. start/end `CsCH4/RsCsCH4` and `CsN2O/RsCsN2O` storage;
3. `QPrCH4Do`, `QPrCH4Ex`, `QPrCH4Hu`, `QPrCH4Os` and corresponding source-pool changes;
4. CH4 oxidation and the diffusion, air-flow, ebullition and plant-mediated emission components;
5. N2O nitrification production, denitrification production, N2O reduction and emission components;
6. ordinary C/N balance terms plus GHG-specific observer terms;
7. unrounded model-wide C and N residuals reconstructed from explicit state and transfers.

A synthetic or compatibility-derived case may establish causal reachability but cannot become B0 or B2 historical evidence. Historical behaviour remains reference-blocked until a qualified historical runner or equivalent admitted oracle exists.

## B3 admission consequence

GHG01 closes theory/source/input-lineage qualification only to the declared level. GHG B3 admission remains blocked by independent evidence classes:

- the remaining release-specific equation and parameter authority gap under `TCD-008`, now narrowed substantially for N2O but still open for CH4 and unresolved N2O subrelations;
- matching historical testcase/input lineage under `TCD-013`;
- source-confirmed conservation-path and balance-observer findings documented above;
- two N2O document-source equation conflicts requiring scientific disposition;
- absence of a qualified historical reference runner/output oracle.

No finding in this handoff is a production patch specification. No canonical TCD number is allocated here.
