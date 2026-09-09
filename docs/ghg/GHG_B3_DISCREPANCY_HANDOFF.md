# ANIMO-GHG01 — B3 discrepancy and governance handoff

Status: `POST_CLOSEOUT_HANDOFF_PERSISTED_NO_CANONICAL_TCD_ALLOCATION`

This handoff packages the source-confirmed findings from ANIMO-GHG01 for later B3 and RG02 reconciliation. It does not reopen the GHG01 qualification, allocate canonical TCD numbers, repair revision-53 source, or admit production migration.

## Governance boundary

Live RG02 evidence at handoff time identifies `work/animo-rg02-branch-authority-integration@27231ac9e52380c4ec10c9cf8e1cff5b72711e96` as the active branch-authority integration line. Its local-TCD reconciliation states that the qualified B3Q01 canonical register ends at `TCD-027`, with only a separate `TCD-028` reservation observed. Post-027 identifiers created on evidence branches are not canonical unless allocated through the B3 governance line.

Therefore this document uses GHG01-local finding keys only.

Existing canonical GHG discrepancies remain distinct:

- `TCD-008`: GHG theory/version documentation gap;
- `TCD-013`: GHGMais versus revision-53 input-contract lineage mismatch.

Neither identifier is broadened here to absorb newly found conservation or observer defects.

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

GHG01 closes theory/source/input-lineage qualification only to the declared level. GHG B3 admission remains blocked by four independent evidence classes:

- exact revision-53 equation and parameter authority, linked to existing `TCD-008`;
- matching historical testcase/input lineage, linked to existing `TCD-013`;
- source-confirmed conservation-path and balance-observer findings documented above;
- absence of a qualified historical reference runner/output oracle.

No finding in this handoff is a production patch specification. No canonical TCD number is allocated here.
