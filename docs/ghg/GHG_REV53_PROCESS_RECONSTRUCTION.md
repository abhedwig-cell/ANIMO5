# ANIMO-GHG01 — revision-53 GHG process reconstruction

Status: `QUALIFIED_PROCESS_RECONSTRUCTION_WITH_EXACT_EQUATION_AUTHORITY_GAPS`

Evidence target: ANIMO 4.1.5 revision 53 frozen source archive, SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`.

This document separates scientific process provenance from source reachability. Presence of an equation in revision 53 is never used by itself as scientific validation.

## 1. Release chronology and authority boundary

The official ANIMO 4.0 user guide is Renaud, Roelsma & Groenendijk (2005), Alterra Report 224. It documents carbon mineralisation, CO2 release, nitrification, denitrification, oxygen/aeration and WFPS response, but its `>simopt:` contract has no greenhouse-gas switch and its documented output selection has no dedicated CH4/N2O GHG suite. This is strong version-specific evidence that the later GHG input/output contract must not be projected backwards onto the documented 2005 ANIMO 4.0 release.

Public scientific evidence establishes a later SWAP-ANIMO GHG extension. Hendriks, Wollewinkel & van den Akker (2007), *Predicting soil subsidence and greenhouse gas emission in peat soils depending on water management with the SWAP-ANIMO model*, describes a process-based model for CO2, CH4 and N2O and reports calibration and validation against two Dutch peat fields. Stolk et al. (2009), *Simulation of nitrous oxide peak emissions from a Dutch peat soil with SWAP-ANIMO*, independently confirms an active SWAP-ANIMO N2O process chain coupled to hydrology, carbon and nitrogen cycling.

Revision-53 GHG source files carry `tags/animo4.1.4` source metadata while their history comments identify Hendriks GHG work in 2007/2008 and sometimes call that work a release of `ANIMO4.0`. TH02 already classifies this as conflicting version labelling with strong pre-4.1 implementation provenance. The safe chronology is therefore:

1. official documented ANIMO 4.0 in 2005 does not expose the later GHG contract;
2. a SWAP-ANIMO GHG development line demonstrably exists by 2007 and N2O work by 2008/2009;
3. that line is present in source tagged as ANIMO 4.1.4 and in frozen revision 53;
4. the exact first supported release and exact release-specific scientific specification remain unresolved.

Primary public sources used here:

- Renaud, L.V., Roelsma, J. & Groenendijk, P. (2005), Alterra Report 224, WUR eDepot 20340.
- Hendriks, R.F.A., Wollewinkel, R. & van den Akker, J.J.H. (2007), WUR eDepot 159749.
- Stolk, P.C., Hendriks, R.F.A., Jacobs, C.M.J. & Moors, E.J. (2009), WUR eDepot 168932.
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

## 4. Governing-relation provenance matrix

The provenance label applies to the stated relation, not to the whole subsystem.

| Process / governing relation | Revision-53 implementation evidence | Provenance | Qualification boundary |
| --- | --- | --- | --- |
| CO2 from ordinary organic transformations | Base ANIMO organic transformation cycle, `Rates.for`, `resp_miner.for`, output/ledger logic | `VERSION_SPECIFIC_DOCUMENTATION` | 2005 ANIMO 4.0 documentation supports CO2 release from decomposition, but not the later selected-fraction GHG contract. |
| GHG selection of organic fractions for CO2/subsidence | `>outGHG:` fraction list, `FlCO2fr`, `Diorma_CO2`, `Frdo_CO2`, `Frhu_CO2` | `SOURCE_ONLY` | No revision-53 or 4.1.4 scientific specification found that independently fixes this exact selection algorithm. |
| CH4 anaerobic substrate production | `ghg_ch4.for::CH4produc`; substrate from DOM, exudates, humus and selected fresh OM; oxygen-status, temperature and pH factors | `INDEPENDENT_THEORY` for mechanism; `SOURCE_ONLY` for exact rev53 equation/constants | Hendriks et al. 2007 and Walter & Heimann 2000 support process-based methanogenesis; no independent authority found for the exact rev53 polynomial/Q10/source-pool formula. |
| CH4 temperature response | source `5**((T-Tref)/10)` above 0 C | `SOURCE_ONLY` | Exact Q10=5 relation not independently qualified. |
| CH4 pH response | source quadratic between pH 3.3 and 10 | `SOURCE_ONLY` | Exact coefficients not independently qualified. |
| CH4 oxidation | `ghg_ch4.for::CH4oxid`; CH4 and O2 limitation, temperature response, oxygen-demand coupling | `INDEPENDENT_THEORY` for mechanism; `SOURCE_ONLY` for exact rev53 kinetics | Oxidation is a standard process in the independent wetland CH4 model lineage, but exact rev53 rate law and constants remain source-bound. |
| CH4 diffusion | gas/liquid diffusion via `ghgtransport.for`; surface emission from concentration gradient | `INDEPENDENT_THEORY` | Walter & Heimann 2000 explicitly models diffusion. Exact ANIMO coefficient calculation remains source-specific. |
| CH4 water and air advection | `ghgtransport.for`, air flow constructed in `ghgasses.for` | `SOURCE_ONLY` | Physically standard transport, but no independent ANIMO-specific equation authority found. |
| CH4 plant-mediated transport | root/growth-weighted transport with `FvegCH4`, plant oxidation fraction `PvCH4Ox` | `INDEPENDENT_THEORY` for mechanism; `SOURCE_ONLY` for exact rev53 relation | Walter & Heimann 2000 explicitly models plant-mediated transport. Exact ANIMO implementation remains source-bound. |
| CH4 ebullition | saturated/ponded excess over temperature-adjusted threshold is moved upward and may emit | `INDEPENDENT_THEORY` for mechanism; `SOURCE_ONLY` for exact threshold formula | Walter & Heimann 2000 explicitly models ebullition. Exact ANIMO threshold law remains unqualified. |
| N2O production during nitrification | `QPrN2Onit = -FrNitrN2O * Rekinh * Avconh * Mofr * He`; moisture-dependent fraction calculated in N2O code | `INDEPENDENT_THEORY` for process; `SOURCE_ONLY` for exact rev53 fraction law | Stolk et al. 2009 supports direct nitrification N2O production, especially after NH4 fertilisation. Exact formula is not independently fixed. |
| N2O production by denitrification | competition for reducing capacity between NO3 and N2O, pH, temperature and aeration factors | `INDEPENDENT_THEORY` for process; `SOURCE_ONLY` for exact rev53 competition law | Stolk et al. 2009 supports denitrification as major peak source. Exact source equations/stoichiometric competition remain unqualified. |
| N2O reduction to N2 | `QRdN2O`, first/zero-order handling in `ghg_n2o.for` | `INDEPENDENT_THEORY` for process; `SOURCE_ONLY` for exact rev53 relation | N2O reduction is part of denitrification theory; exact rev53 kinetics lack release-specific authority. |
| N2O diffusion and air/water advection | shared `GHGtransport` machinery; surface diffusion and air-flow emission terms | `INDEPENDENT_THEORY` for gas transport class; `SOURCE_ONLY` for exact ANIMO coupling | No release-specific independent numerical specification found. |
| Aeration/redox control | base aeration routines provide `Rdfaox`, `Rdfantfc`, oxygen demand/concentrations and WFPS/aeration states to GHG | `VERSION_SPECIFIC_DOCUMENTATION` for base ANIMO aeration; `SOURCE_ONLY` for exact GHG coupling | 2005 guide documents oxygen-diffusion and WFPS approaches and nitrate use under anaerobiosis. Later GHG coupling is not in that release guide. |
| Bunsen air/water partitioning | `Inicalc.for`, `GHGtransport` | `SOURCE_ONLY` | Physical principle is established, but exact ANIMO function/parameterisation has no independently pinned rev53 authority in this work unit. |
| CO2-equivalent annual conversion | `CvCH4_CO2`, `CvN2O_CO2` from `>outGHG:` and annual GHG output | `UNRESOLVED` as historical scientific setting | GHGMais carries 25 and 298, but exact intended assessment convention and release provenance are not established by revision-53 documentation. |

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
| CH4 production | `THEORY_READY`, `SOURCE_READY`, `TESTCASE_LINEAGE_BLOCKED`, `REFERENCE_BLOCKED` |
| CH4 oxidation | `THEORY_READY`, `SOURCE_READY`, `TESTCASE_LINEAGE_BLOCKED`, `REFERENCE_BLOCKED` |
| CH4 transport/emission | `THEORY_READY`, `SOURCE_READY`, `TESTCASE_LINEAGE_BLOCKED`, `REFERENCE_BLOCKED` |
| N2O nitrification production | `THEORY_READY`, `SOURCE_READY`, `TESTCASE_LINEAGE_BLOCKED`, `REFERENCE_BLOCKED` |
| N2O denitrification production/reduction | `THEORY_READY`, `SOURCE_READY`, `TESTCASE_LINEAGE_BLOCKED`, `REFERENCE_BLOCKED` |
| N2O transport/emission | `THEORY_READY`, `SOURCE_READY`, `TESTCASE_LINEAGE_BLOCKED`, `REFERENCE_BLOCKED` |
| Exact revision-53 GHG coefficient set as a whole | `INSUFFICIENT_EVIDENCE` |

`THEORY_READY` here means the scientific process class is independently supported. It does not mean every revision-53 coefficient or algebraic detail has an independent source.

## 7. Scientific conclusion

Revision 53 contains a genuine, coupled and source-reachable GHG subsystem. Broad CH4 and N2O scientific intent is independently supported by contemporary SWAP-ANIMO publications and established wetland methane theory. The exact revision-53 equation set is not independently or release-specifically documented strongly enough to be treated as fully qualified scientific authority.

The correct qualification is therefore process-level theory provenance plus exact source reconstruction, with exact-equation and historical-reference gaps retained explicitly.