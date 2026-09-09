# ANIMO 4.1.5 revision 53 extension theory reconciliation

Status: `QUALIFIED_INVENTORY_WITH_EXPLICIT_UNRESOLVED_GAPS`

This document is a theory/provenance audit of the frozen ANIMO 4.1.5 revision-53 source. It is not a replacement theory manual and it does not promote source behaviour to intended science where independent documentation is absent.

## 1. Evidence boundary

Frozen source:

`ANIMO_4.1.5.53(3).zip`

SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Supplied principal documentation:

ANIMO 4.0 User's Guide, Alterra Report 224 (2005), SHA-256:

`ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`

The supplied guide is authoritative evidence for the documented 4.0 interface and inherited 4.0 concepts. It is not a version-specific authority for the complete revision-53 process set.

The official WUR record for Groenendijk, Renaud & Roelsma (2005), *Prediction of nitrogen and phosphorus leaching to groundwater and surface waters; process descriptions of the ANIMO 4.0 model*, Alterra Report 983, establishes that a dedicated 4.0 process description exists. Its role here is `AUTHORITATIVE_INHERITED_ANIMO40_THEORY`. TH01 has identified the public record and eDepot location, but has not made the external report bytes part of B0.

Source-internal SVN metadata is heterogeneous. `Version.inc` identifies `animo4.1.5`, revision `53`, while observed file-level `$HeadURL` values commonly point at `tags/animo4.1.4`. Therefore chronology inferred from source comments is provenance evidence, not proof of an exact homogeneous release lineage.

## 2. Reconciliation rule

Every process is classified separately. The following meanings are strict:

- `THEORY_CONFIRMED`: governing scientific concept is independently documented closely enough to judge the legacy formulation at the process level. This does not by itself qualify historical numerical behaviour.
- `THEORY_PARTIALLY_RECONSTRUCTED`: independent evidence supports the process and broad intent, but one or more revision-specific equations, parameters, activation semantics or couplings remain source-derived.
- `CODE_DEFINED_THEORY_UNCONFIRMED`: the source makes a coherent algorithm visible, but TH01 found no sufficiently independent scientific authority for that revision-specific feature.
- `THEORY_CODE_CONFLICT`: independent or inherited theory is sufficient to identify a source implementation inconsistency.
- `INSUFFICIENT_EVIDENCE`: not enough evidence exists to define intended science.

## 3. Inherited ANIMO 4.0 baseline

The 4.0 guide and Report-983 lineage establish the principal inherited model architecture:

- fresh organic matter, dissolved organic matter, root exudates and humus/biomass;
- mineralisation/immobilisation coupled across C, N and P;
- NH4 and NO3 processes including nitrification and denitrification;
- dissolved transport of organic matter/N/P, NH4, NO3 and PO4;
- phosphorus equilibrium sorption, non-equilibrium sorption and precipitation;
- crop nutrient uptake;
- environmental response functions for aeration/moisture, temperature and pH;
- water-driven compartment transport and explicit mass-balance reporting.

Revision-53 source retains these concepts. Qualification of later or differently labelled extension surfaces therefore starts from inheritance, not from an assumption that all revision-53 functionality is new.

## 4. Greenhouse gases

### Reconciliation state

`THEORY_PARTIALLY_RECONSTRUCTED`

### Independent evidence

Hendriks, Wollewinkel & van den Akker (2007/2008) publicly describe a process-based SWAP-ANIMO model for peat soils that simulates CO2, CH4 and N2O, subsidence and nutrient loading and was calibrated/validated against Dutch field experiments. This independently confirms the scientific existence and intended process-based nature of a SWAP-ANIMO GHG extension.

It does not establish the exact equations or input contract of the frozen revision-53 source.

### Revision-53 implementation-derived formulation

The frozen source contains explicit CH4 and N2O state, production, transport, transformation and emission routines.

For CH4, source inspection shows:

- methanogenesis is restricted to the anaerobic fraction represented by `1 - Rdfaox`;
- eligible substrate is assembled from dissolved organic matter, exudates, humus and selected fresh-organic-matter fractions;
- the source computes a temperature factor and a pH factor and multiplies these with `R0CH4pr` and eligible organic substrate;
- CH4 oxidation depends on CH4 and O2 availability, with temperature response and an oxygen competition constraint shared with organic-matter transformation/nitrification demand;
- CH4 exists in dissolved and gas-phase state connected through a Bunsen partition relation;
- transport/emission mechanisms include diffusion, gas/water advection, plant-mediated transport and ebullition.

These exact equations are `IMPLEMENTATION_DERIVED_NOT_INDEPENDENT_THEORY` until a matching formulation document is found. Source comments cite Walter & Heimann (2000) for the methanogenesis relation and Hendriks-related work for later GHG formulations, but a comment-level citation is not sufficient to promote the equation to revision-53 authoritative theory.

For N2O, source inspection shows:

- production from nitrification is represented as a fraction of nitrification;
- denitrification partitions reduction through NO3 to N2O and N2O to N2;
- relative N2O/NO3 reduction depends on pH, temperature, aeration and a relative electron-acceptor-strength parameter;
- N2O is transported as a dissolved/gas species through the generic GHG transport machinery;
- emission includes diffusive and advective exchange with the atmosphere.

Again, these exact relations remain implementation-derived pending independent equation-level confirmation.

### Conservation and temporal assumptions

PREP06 confirms GHG state ownership is separate from public C/N/P balance arrays. CH4 carbon and N2O nitrogen therefore require explicit element-level reconciliation before a future canonical ledger can claim full GHG conservation. Revision-53 GHG routines iterate process coefficients within a model timestep rather than acting as simple post-processing emissions.

### Known discrepancies

The supplied `GHGMais` testcase does not match the revision-53 GHG parser contract. Revision 53 requires `>outGHG:` fields, while the supplied case uses a different named-section schema and an expanded organic-fraction contract. This is a provenance blocker, not a reason to translate the testcase.

### B3 relevance

Historical behaviour preservation cannot yet be judged for the GHG extension. A source-specific theory/change document and a native source/testcase pairing are still required. B2 remains highly desirable. Production admission is blocked.

## 5. Macropore transport and storage

### Reconciliation state

`THEORY_PARTIALLY_RECONSTRUCTED`

### Inherited and public theory

ANIMO 4.0 already exposes the intended macropore interface, including two domains named Main Bypass Flow and Internal Catchment, macropore water storage, matrix exchange, wall contact and rapid drainage variables. The same guide repeatedly marks the route as not operational in ANIMO 4.0.

The SWAP 3.2 theory lineage independently documents the same two hydrological domains. Main Bypass represents continuous/interconnected pores that carry water rapidly and can discharge to drains. Internal Catchment represents discontinuous pores that terminate at depth and force infiltration into the matrix. This strongly supports the hydrological provenance of the revision-53 macropore interface.

It does not independently define ANIMO's revision-53 nutrient-transfer equations.

### Revision-53 implementation-derived formulation

The frozen source contains active `MAPOHYDRO` and `MAPOTRANSPORT` routines. Source-bound states and fluxes include:

- water storage `SrWaMp` for two domains;
- matrix/macropore exchange by layer;
- surface inflow from precipitation and routed runoff;
- vertical macropore transport;
- direct rapid drainage from the Main Bypass domain;
- macropore concentrations and result concentrations for NH4, NO3, dissolved organic matter/N/P and PO4;
- transfer from macropores into matrix as source terms for ordinary matrix transport.

The specialized solute balance uses old and new macropore storage explicitly. These are physical stores, not reporting-only quantities.

### Known discrepancy

PREP06 TCD-025 establishes that the specialized macropore balance control volume is larger than the main public balance interface. The main ledger does not receive all macropore storage/result states, and `Dra4` integration is incomplete/inconsistent across species. The supplied testbank activates `MacroPoreOption=0` everywhere, so no behavioural magnitude is established.

### B3 relevance

Hydrological domain intent is reasonably supported. ANIMO-specific solute process theory and behavioural evidence are not. A dedicated active macropore qualification case and independent theory are required before B3 or corrected-ledger admission.

## 6. Stable dissolved organic matter

### Reconciliation state

`THEORY_PARTIALLY_RECONSTRUCTED_WITH_VERSION_LABEL_CONFLICT`

### Provenance

The supplied canonical 2005 ANIMO 4.0 User's Guide has one dissolved-organic-matter pool, not a stable/labile split.

A 2008 WUR SWAP-ANIMO peat study explicitly recommended adding a second dissolved organic matter pool to distinguish labile/fresh and more stable peat-derived organic matter. A 2011 BMBF/UFZ report then describes model development starting from ANIMO 3.8, records active participation by Alterra ANIMO developers, and shows a carbon-cycle extension with stable dissolved organic matter and sorbed stable DOM. Its process diagram contains parameter names that strongly overlap revision 53, including `Ratio_rd_st`, `sdofr`, `recfSDO`, `recfHSDO` and `asfaSDO`. The report also states that the modified branch was used by the original ANIMO developers at Alterra/Wageningen.

This is substantially stronger provenance than a later application description. It independently supports the broad carbon-side stable-DOM state and transformation topology.

However, the 2011 report labels its improved branch `ANIMO Version 4.0`. That conflicts with the supplied 2005 ANIMO 4.0 guide, which predates the 2007-2010 development project and contains no second DOM pool. TH01 therefore classifies the exact release-number relation as `CONFLICTING_EVIDENCE`. The external label is not silently mapped onto the frozen revision-53 lineage.

Later WUR ANIMO application material independently confirms that stable and labile DOM pools became part of ANIMO use, but likewise does not resolve the exact introducing revision.

### Revision-53 implementation-derived formulation

The source contains stable DOM carbon, nitrogen and phosphorus concentrations, restart states and average/result states. `Resp_miner` makes the stable pool part of the transformation system rather than a passive tracer.

Observed pathways include:

- production of stable DOM from fresh organic matter;
- partitioning of decomposed labile DOM between stable and non-stable routes through `SDOfr`;
- stable-DOM decay controlled by `recfSDO`;
- partition of stable-DOM decay between dissimilation and humus formation through `asfaSDO`;
- transfer between humus and stable DOM through `recfHUSDO`;
- separate stable-DOM sorption through `SocfSDO`;
- C/N/P co-transport and storage.

The independent 2011 diagram makes the broad carbon topology and several parameter roles reasonably defensible. It does not independently establish the revision-53 N/P generalization, exact rate algebra, temporal integration or parameter calibration. Those parts remain `IMPLEMENTATION_DERIVED_NOT_INDEPENDENT_THEORY`.

### Theory/code conflict

PREP04 TCD-023 is a direct C/N/P symmetry violation in the stable-DOM decay accounting path. The P outputs `Transfop(19)` and `Transfop(20)` are formed from `Transfon(17)` in one source branch instead of the corresponding P term. The intended elemental partition identity is clear from the parallel C/N branches and from other branches in the same routine. This is therefore a genuine theory/code conflict, not merely undocumented behaviour.

### B3 relevance

The broad carbon-side stable-DOM concept can be scientifically reviewed with medium-high confidence. Exact release numbering and the N/P extension remain unresolved, and TCD-023 remains a corrected-legacy qualification item. B2 remains necessary or must be replaced by the stronger independent-scientific-admission fallback defined by EB01.

## 7. Phosphorus sorption and precipitation

### 7.1 Fast equilibrium sorption

Reconciliation: `THEORY_CONFIRMED` for the inherited ANIMO 4.0 Langmuir core.

The 4.0 guide explicitly defines equilibrium sorption options and states that ANIMO 4.0 operationally uses one Langmuir equilibrium site. Public WUR descriptions continue to characterize ANIMO's fast reaction as reversible Langmuir adsorption.

Revision 53 generalizes source branches to linear, Langmuir and Freundlich choices and multiple sites. Those additional supported code paths require version-specific interface/provenance evidence before being called inherited 4.0 production semantics.

TCD-019 is not a dispute about Langmuir theory. It is a numerical finite-change/convergence-policy issue in the nonlinear solver and must remain a separate numerical qualification.

### 7.2 Slow non-equilibrium sorption

The 4.0 guide explicitly lists:

- `OPTCXSL=1`: linear;
- `OPTCXSL=2`: Langmuir;
- `OPTCXSL=3`: Freundlich;
- one to three slow sites;
- separate first-order adsorption and desorption rate constants.

Therefore slow Langmuir is not a revision-53 invention. It is an inherited documented constitutive option, even though later standard ANIMO descriptions predominantly describe the calibrated slow fixation process as a three-component Freundlich rate equation.

That distinction matters. Later Freundlich-focused documentation must not be misread as proof that the slow-Langmuir branch is unintended.

For `OPTCXSL=3`, the conceptual model is strongly supported: slow diffusion/fixation is time dependent, slower and less reversible than the fast sorption pool. Supplied P cases exercise this route.

For `OPTCXSL=2`, the constitutive target is documented, but the revision-53 integration contains TCD-024. `Conc_unl` nests a sorption-site loop `J` inside an unrelated trial loop `I` and uses `Parcxsl(3,I)` in one Langmuir exponent instead of the site-specific `Parcxsl(3,J)`. PREP05 synthetic evidence shows the single index correction removes more than 99.5% of the induced P nonclosure in the qualification probe and is inert on the supplied Freundlich route.

Reconciliation for slow Langmuir is therefore `THEORY_CODE_CONFLICT`.

### 7.3 Precipitation/dissolution

The inherited 4.0 concept is threshold-controlled precipitation/dissolution of mineral P, with instantaneous precipitation as the documented operational 4.0 route. Revision 53 retains an additional first-order kinetic option. That kinetic option is `CODE_DEFINED_THEORY_UNCONFIRMED` until version-specific authority is found.

### B3 relevance

The P theory is considerably stronger than for GHG/macropores because the core is independently documented. B3 still requires behavioural qualification, and TCD-019/TCD-024 must not be combined into one correction because they affect different scientific/numerical seams.

## 8. P-class-dependent crop forcing

### Reconciliation state

`CODE_DEFINED_THEORY_UNCONFIRMED`

`input1.for` exposes `PClassOption`, `PClassYearSwitch` and `PClass`. `ChoosePClass` selects class-indexed crop N/P uptake and crop-loss forcing arrays. The source comment identifies the context as `EMW2012` and labels the routine as ANIMO 4.1-era.

TH01 found no independent document in the current evidence set defining the class thresholds, scientific meaning, switching rule or provenance of the class-indexed forcing data. The code is clear about selection mechanics but not enough to define scientific intent.

This process is therefore not B3-ready.

## 9. Parser-visible non-theory surfaces

### Sulphate

`SulphateSimulation` and `PrintBalSulphate` are parser-visible in the ANIMO 4.1 input route, but PREP03 found no corresponding implemented sulphate process system in the frozen source.

Classification:

`INSUFFICIENT_EVIDENCE`

This must not be treated as latent production physics merely because the parser accepts a switch.

### Soil temperature file

`SoilTempFile` is a later parser/input-routing surface. The underlying temperature response of organic transformations and nitrification is inherited from ANIMO 4.0. The parser addition is not evidence of changed physics by itself.

Classification:

`THEORY_PARTIALLY_RECONSTRUCTED`

## 10. Process-level B3 assessment

| process | evidence strength | B3 judgement |
| --- | --- | --- |
| Core C/N/P transformations | high inherited 4.0 theory | scientific theory basis usable, historical behaviour still needs B2/B3 reconciliation |
| Fast P Langmuir | high | theory-ready for inherited core; TCD-019 remains numerical qualification |
| Slow P Freundlich | high | theory-ready; historical behaviour/tolerances still require B2 |
| Slow P Langmuir | medium-high | blocked by TCD-024 plus missing independent algorithm-level reference |
| Instantaneous P precipitation | high inherited core | theory-ready for inherited route |
| Stable DOM | medium-high carbon topology, medium-low to medium exact N/P equations | partial only; version-label conflict, TCD-023 and N/P provenance block admission |
| GHG CH4/N2O | medium broad intent, low-to-medium exact revision equations | partial only; matching theory and testcase lineage required |
| Macropore nutrient transport | medium hydrological provenance, low-to-medium ANIMO solute theory | partial only; no active testbank evidence |
| P-class crop forcing | low-to-medium | source-defined only, not B3-ready |
| Sulphate parser option | insufficient | not a qualified process |

## 11. Qualification decision

TH01 does not support `QUALIFIED_REV53_THEORY`.

It does support:

`QUALIFIED_REV53_THEORY_PROVENANCE_INVENTORY_WITH_EXPLICIT_UNRESOLVED_GAPS`

because:

1. the inherited 2005 ANIMO 4.0 theory boundary is identifiable;
2. the major revision-53 extension surfaces are separated from that inherited boundary without forcing ambiguous external version labels into the release lineage;
3. public provenance exists for GHG, stable DOM intent and macropore hydrological architecture;
4. source-only equations are explicitly labelled non-independent;
5. known theory/code conflicts are separated from missing-theory gaps;
6. each process now has an explicit B3 readiness judgement.

Production migration remains:

`NOT_ADMITTED`

No frozen source, testcase, physics or numerical policy was changed by TH01.
