# ANIMO-GHG01 — revision-53 GHG process reconstruction

Status: `QUALIFIED_PROCESS_RECONSTRUCTION_WITH_EXACT_EQUATION_AUTHORITY_GAPS`

Evidence target: ANIMO 4.1.5 revision 53 frozen source archive, SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`.

This document separates scientific process provenance from source reachability. Presence of an equation in revision 53 is never used by itself as scientific validation.

## 1. Release chronology and authority boundary

The official ANIMO 4.0 user guide is Renaud, Roelsma & Groenendijk (2005), Alterra Report 224. It documents carbon mineralisation, CO2 release, nitrification, denitrification, oxygen/aeration and WFPS response, but its `>simopt:` contract has no greenhouse-gas switch and its documented output selection has no dedicated CH4/N2O GHG suite. This is strong version-specific evidence that the later GHG input/output contract must not be projected backwards onto the documented 2005 ANIMO 4.0 release.

Public scientific evidence establishes a later SWAP-ANIMO GHG extension. Hendriks, Wollewinkel & van den Akker (2007), *Predicting soil subsidence and greenhouse gas emission in peat soils depending on water management with the SWAP-ANIMO model*, describes a process-based model for CO2, CH4 and N2O and reports calibration and validation against two Dutch peat fields. Stolk et al. (2009), *Simulation of nitrous oxide peak emissions from a Dutch peat soil with SWAP-ANIMO*, independently confirms an active SWAP-ANIMO N2O process chain coupled to hydrology, carbon and nitrogen cycling.

The authority chain is materially strengthened by two peer-reviewed 2011 publications. Stolk et al. (2011), *Simulation of Daily Nitrous Oxide Emissions from Managed Peat Soils*, Vadose Zone Journal 10(1), 156-168, DOI `10.2136/vzj2010.0029`, states that ANIMO was extended for N2O production, consumption and transport and gives the main equations in its appendix. Stolk, Hendriks, Jacobs, Moors & Kabat (2011), *Modelling the effect of aggregates on N2O emission from denitrification in an agricultural peat soil*, Biogeosciences 8, 2649-2663, DOI `10.5194/bg-8-2649-2011`, explicitly describes the `Original concept for N2O` and provides governing ANIMO equations for the N2O state relation, transport, nitrification, denitrification and aeration. Equation-level comparison with revision 53 is recorded in `GHG_THEORY_AUTHORITY_RECOVERY_2011.md`.

Both 2011 publications cite a more detailed Hendriks et al. work, *Modelling of greenhouse gas emissions with ANIMO 4.0*. A separate October 2011 Alterra report cites that work as `in voorbereiding` and associates it with Alterra report 2054. Report 2054 is therefore a high-value authority lead, not a recovered/frozen release specification.

Revision-53 GHG source files carry `tags/animo4.1.4` source metadata while their history comments identify Hendriks GHG work in 2007/2008 and sometimes call that work a release of `ANIMO4.0`. TH02 already classifies this as conflicting version labelling with strong pre-4.1 implementation provenance. The safe chronology is therefore:

1. official documented ANIMO 4.0 in 2005 does not expose the later GHG contract;
2. a SWAP-ANIMO GHG development line demonstrably exists by 2007 and N2O work by 2008/2009;
3. detailed peer-reviewed ANIMO-specific N2O equations are published in 2011 for the original equilibrium concept;
4. that GHG line is present in source tagged as ANIMO 4.1.4 and in frozen revision 53;
5. the exact first supported release and a complete release-specific revision-53 GHG specification remain unresolved.

Primary public sources used here:

- Renaud, L.V., Roelsma, J. & Groenendijk, P. (2005), Alterra Report 224, WUR eDepot 20340.
- Hendriks, R.F.A., Wollewinkel, R. & van den Akker, J.J.H. (2007), WUR eDepot 159749.
- Stolk, P.C., Hendriks, R.F.A., Jacobs, C.M.J. & Moors, E.J. (2009), WUR eDepot 168932.
- Stolk et al. (2011), Vadose Zone Journal 10(1), 156-168, DOI `10.2136/vzj2010.0029`.
- Stolk, Hendriks, Jacobs, Moors & Kabat (2011), Biogeosciences 8, 2649-2663, DOI `10.5194/bg-8-2649-2011`.
- Walter, B.P. & Heimann, M. (2000), *Global Biogeochemical Cycles* 14, 745-765, DOI `10.1029/1999GB001204`.

## 2. Revision-53 activation path

`input1.for` reads `GreenHouseGasOption` for `AnimoVersion=41` and validates `IoptGHG` in `[0,2]`. It also contains a later six-position compatibility read for `AnimoVersion=40`, but the 2005 version-specific 4.0 guide documents only five `>simopt:` switches. The source compatibility branch is therefore not evidence that the official 2005 release supported GHG.

The main program contains two active guarded calls:

- `Animo.for:705-722`: `If (IoptGHG.Ge.1) Call GHGasses(1,...)` after aeration and before final actual reaction rates and nitrate transport;
- `Animo.for:867-883`: `If (IoptGHG.Ge.1) Call GHGasses(2,...)` after definitive nitrate transport, explicitly labelled final N2O calculations.

`ghgasses.for` task 1 calculates air-flow coupling, calls `GHG_Methane` once and `GHG_NitrousOxide` once. Task 2 calls `GHG_NitrousOxide` again after definitive NO3 calculation. This makes CH4 and N2O source-reachable scientific branches, not dormant output code.

## 3. State and transport ownership

Initial GHG state is explicit in revision 53:

- `INITIAL.INP >methan:` supplies `CsCH4(0:NL)`, documented in source as total air+water CH4-C concentration per soil volume;
- `INITIAL.INP >nitoxi:` supplies `CsN2O(0:NL)`, total air+water N2O-N concentration per soil volume;
- `Inicalc.for` partitions system concentration into dissolved concentration using the reciprocal Bunsen solubility coefficient;
- GHG transport calculates end-of-step `RsCoCH4`, `RsCsCH4`, `RsCoN2O`, `RsCsN2O`;
- `Init.for` copies accepted dissolved gas result states into the next step's current dissolved states; system gas result states are separately persisted by output/restart handling.

`ghgtransport.for` and `ghgtranssub.for` solve coupled liquid/gas transport with Bunsen partitioning, molecular diffusion, water advection, air advection and source/sink terms. The total system result state is reconstructed from liquid concentration, gas concentration, water-filled pore volume and air-filled pore volume.

The 2011 Biogeosciences paper independently documents the same original N2O equilibrium concept: a total soil N2O state related to dissolved concentration through water content, air content and the reciprocal Bunsen coefficient, with simultaneous gas/water diffusion, air advection, water advection, drainage, production and reduction. This independently supports the N2O state/transport formulation class. It does not establish historical revision-53 execution.

## 4. Governing-relation provenance matrix

The provenance label applies to the stated relation, not to the whole subsystem. `INDEPENDENT_THEORY` may here include an independent peer-reviewed ANIMO-specific equation that matches revision-53 source, while the release-identity boundary remains explicit.

| Process / governing relation | Revision-53 implementation evidence | Provenance | Qualification boundary |
| --- | --- | --- | --- |
| CO2 from ordinary organic transformations | Base ANIMO organic transformation cycle, `Rates.for`, `resp_miner.for`, output/ledger logic | `VERSION_SPECIFIC_DOCUMENTATION` | 2005 ANIMO 4.0 documentation supports CO2 release from decomposition, but not the later selected-fraction GHG contract. |
| GHG selection of organic fractions for CO2/subsidence | `>outGHG:` fraction list, `FlCO2fr`, `Diorma_CO2`, `Frdo_CO2`, `Frhu_CO2` | `SOURCE_ONLY` | No revision-53 or 4.1.4 scientific specification found that independently fixes this exact selection algorithm. |
| CH4 anaerobic substrate production | `ghg_ch4.for::CH4produc`; substrate from DOM, exudates, humus and selected fresh OM; oxygen-status, temperature and pH factors | `INDEPENDENT_THEORY` for mechanism; `SOURCE_ONLY` for exact rev53 equation/constants | Hendriks et al. 2007 and Walter & Heimann 2000 support process-based methanogenesis; no independent authority found for the exact rev53 polynomial/Q10/source-pool formula. |
| CH4 temperature response | source `5**((T-Tref)/10)` above 0 C | `SOURCE_ONLY` | Exact Q10=5 relation not independently qualified. |
| CH4 pH response | source quadratic between pH 3.3 and 10 | `SOURCE_ONLY` | Exact coefficients not independently qualified. |
| CH4 oxidation | `ghg_ch4.for::CH4oxid`; CH4 and O2 limitation, temperature response, oxygen-demand coupling | `INDEPENDENT_THEORY` for mechanism; `SOURCE_ONLY` for exact rev53 kinetics | Oxidation is a standard process in the independent wetland CH4 model lineage, but exact rev53 rate law and constants remain source-bound. |
| CH4 diffusion | gas/liquid diffusion via `ghgtransport.for`; surface emission from concentration gradient | `INDEPENDENT_THEORY` | Walter & Heimann 2000 supports diffusion; the shared ANIMO gas/water diffusion form is independently documented for N2O in 2011. Exact CH4 coefficient functions remain source-specific. |
| CH4 water and air advection | `ghgtransport.for`, air flow constructed in `ghgasses.for` | `SOURCE_ONLY` for exact CH4 coupling | The shared GHG transport class is ANIMO-documented for N2O, but an exact independent CH4-specific equation authority was not recovered. |
| CH4 plant-mediated transport | root/growth-weighted transport with `FvegCH4`, plant oxidation fraction `PvCH4Ox` | `INDEPENDENT_THEORY` for mechanism; `SOURCE_ONLY` for exact rev53 relation | Walter & Heimann 2000 explicitly models plant-mediated transport. Exact ANIMO implementation remains source-bound. |
| CH4 ebullition | saturated/ponded excess over temperature-adjusted threshold is moved upward and may emit | `INDEPENDENT_THEORY` for mechanism; `SOURCE_ONLY` for exact threshold formula | Walter & Heimann 2000 explicitly models ebullition. Exact ANIMO threshold law remains unqualified. |
| N2O production during nitrification | `QPrN2Onit = -FrNitrN2O * Rekinh * Avconh * Mofr * He`; threshold/min/max/exponent WFPS fraction in `FracN2Onitr` | `INDEPENDENT_THEORY` for production and WFPS relation; temperature subrelation `UNRESOLVED` | 2011 ANIMO Appendix A15/A16/A18 matches the production and WFPS structure. Appendix A17 as printed conflicts in exponent sign with revision-53 `2**(-(T-Tref)/10)`. |
| N2O production by denitrification | competition for reducing capacity between NO3 and N2O, pH, temperature and aeration factors | `INDEPENDENT_THEORY` for core ANIMO relation | 2011 ANIMO Appendix A9/A10 strongly matches the source competition structure. pH, Q10=2.6 and aeration-response subrelations are exact/algebraic matches. Exact release identity and some stoichiometric mapping remain open. |
| N2O reduction to N2 | `QRdN2O`, first/zero-order handling in `ghg_n2o.for` | `INDEPENDENT_THEORY` for process and competition concept; exact aeration placement `UNRESOLVED` | 2011 Appendix A11 documents the reduction relation, but its printed numerator omits the aeration factor that revision 53 folds into `RatFacN2O`. Detailed authority/change history is required. |
| N2O diffusion and air/water advection | shared `GHGtransport` machinery; surface diffusion and air-flow emission terms | `INDEPENDENT_THEORY` | 2011 original-concept Eq. 1-3 and Appendix A19 independently document the same state, transport and effective-diffusion structure. Revision-53 caps and temperature-dependent free-diffusion functions remain source-specific. |
| Aeration/redox control | base aeration routines provide `Rdfaox`, `Rdfantfc`, oxygen demand/concentrations and WFPS/aeration states to GHG | `VERSION_SPECIFIC_DOCUMENTATION` for base ANIMO aeration; `INDEPENDENT_THEORY` for N2O-specific 2011 equation relation | 2005 guide documents base oxygen-diffusion and WFPS approaches; 2011 Appendix A independently gives governing ANIMO aeration relations used by the N2O formulation. |
| Bunsen air/water partitioning for N2O | `Inicalc.for`, `GHGtransport` | `INDEPENDENT_THEORY` | 2011 original-concept Eq. 2 explicitly defines total N2O state under reciprocal-Bunsen equilibrium and matches revision-53 state reconstruction. Exact source Bunsen coefficient function remains source-specific. |
| CO2-equivalent annual conversion | `CvCH4_CO2`, `CvN2O_CO2` from `>outGHG:` and annual GHG output | `UNRESOLVED` as historical scientific setting | GHGMais carries 25 and 298, but exact intended assessment convention and release provenance are not established by revision-53 documentation. |

## 4.1 Post-closeout 2011 equation-authority recovery

Detailed source-to-publication reconciliation is persisted in `docs/ghg/GHG_THEORY_AUTHORITY_RECOVERY_2011.md` and `integration/animo-ghg/GHG_THEORY_AUTHORITY_RECOVERY_2011.json`.

The strongest recovered exact or near-exact matches are:

- N2O equilibrium total-state relation;
- original N2O conservation-and-transport structure;
- effective simultaneous gas/water diffusion;
- nitrification production and WFPS dependence;
- denitrification pH response;
- relative N2O/NO3 denitrification temperature response with Q10=2.6;
- denitrification aeration-response relation;
- core denitrification production/reduction competition structure;
- diffusion and air-flow emission classes.

Two relation-level discrepancies remain explicitly unresolved:

- `GHG01-LCL-N2O-NITRIFICATION-TEMPERATURE-SIGN-DOC-SOURCE`;
- `GHG01-LCL-N2O-REDUCTION-AERATION-FACTOR-DOC-SOURCE`.

Neither is classified as a legacy code defect at this stage. Report 2054 or equivalent detailed authority plus source/change history is needed to distinguish source evolution from publication notation or implementation divergence.

## 5. Output observability

When `IoptGHG>=1`, revision 53 defines GHG output units 41-54 in `Outsel.for` including:

- `Carbondiox.out`;
- `CH4Emis.out`, CH4 system concentration, liquid concentration, production and oxidation;
- `N2OEmis.out`, N2O system concentration, liquid concentration, production by denitrification, production by nitrification and reduction;
- `AnnualGHG.csv`;
- subsidence output where the option permits it.

CH4 emission output separates diffusion, air-flow, ebullition and plant-mediated components. N2O emission separates diffusion and air-flow components.

These outputs prove observability in source. They do not prove historical behaviour without a compatible historical testcase and qualified runner.

## 6. Process readiness

| Process | B3 readiness evidence |
| --- | --- |
| Base CO2 mineralisation/aeration | `THEORY_READY`, `SOURCE_READY`, `REFERENCE_BLOCKED` for the GHG-specific extension |
| CH4 production | `THEORY_READY`, `SOURCE_READY`, `TESTCASE_LINEAGE_BLOCKED`, `REFERENCE_BLOCKED`, exact kinetics partly `SOURCE_ONLY` |
| CH4 oxidation | `THEORY_READY`, `SOURCE_READY`, `TESTCASE_LINEAGE_BLOCKED`, `REFERENCE_BLOCKED`, exact kinetics partly `SOURCE_ONLY` |
| CH4 transport/emission | `THEORY_READY`, `SOURCE_READY`, `TESTCASE_LINEAGE_BLOCKED`, `REFERENCE_BLOCKED`, exact CH4 coupling partly `SOURCE_ONLY` |
| N2O nitrification production | `THEORY_READY`, `SOURCE_READY`, `TESTCASE_LINEAGE_BLOCKED`, `REFERENCE_BLOCKED`, temperature-sign relation `UNRESOLVED` |
| N2O denitrification production/reduction | `THEORY_READY`, `SOURCE_READY`, `TESTCASE_LINEAGE_BLOCKED`, `REFERENCE_BLOCKED`, reduction aeration-factor placement `UNRESOLVED` |
| N2O transport/emission | `THEORY_READY`, `SOURCE_READY`, `TESTCASE_LINEAGE_BLOCKED`, `REFERENCE_BLOCKED` with strong 2011 ANIMO-specific equation authority |
| Exact revision-53 GHG coefficient set as a whole | `INSUFFICIENT_EVIDENCE`, but N2O equation authority is materially stronger than at initial closeout |

`THEORY_READY` here means the scientific process class is independently supported. For N2O several governing equations now also have independent ANIMO-specific peer-reviewed authority. It still does not mean every revision-53 coefficient, subrelation or release-specific algebraic detail has been independently fixed.

## 7. Scientific conclusion

Revision 53 contains a genuine, coupled and source-reachable GHG subsystem. Broad CH4 and N2O scientific intent is independently supported by contemporary SWAP-ANIMO publications and established wetland methane theory.

The 2011 authority recovery materially changes the strength of the N2O evidence: several governing N2O relations are no longer merely source-bound but can be reconciled directly with peer-reviewed ANIMO-specific equations for the original equilibrium concept. Two document-source conflicts remain unresolved, and the exact complete revision-53 coefficient/equation set is still not supported by a recovered release-specific specification. CH4 exact kinetics remain substantially more source-bound than the N2O formulation.

The correct qualification therefore remains process-level theory provenance plus exact source reconstruction, with equation-level authority recorded where demonstrated and historical-reference gaps retained explicitly. The overall ANIMO-GHG01 closeout remains `QUALIFIED_GHG_THEORY_SOURCE_AND_INPUT_LINEAGE_EVIDENCE_WITH_HISTORICAL_REFERENCE_GAPS`; B3 and production migration remain not admitted.
