# First process and dataflow inventory

Evidence level: `SOURCE_PLUS_ANIMO4_DOCUMENTATION_BASELINE`.

The 4.0 guide provides process concepts and a technical main-program description. The supplied 4.1.5 revision-53 source provides the actual call structure to be audited. This document does not claim that 4.0 documentation and 4.1.5 implementation are identical.

## Main-program ordering observed in supplied 4.1.5 source

At a high level the main program calls:

1. `Input1`
2. `Inicalc`
3. `Input_Echo`
4. `Outbal_write`
5. yearly/time-step initialization via `Init` and optional class/crop initialization
6. `Input_hydro`
7. crop/root route: `Root_plant`, `Grassprd` + `Root_grass`, or `Root_extern`
8. `Input_addit` and `Addit`
9. `Uboundconc`
10. crop-uptake parameter route: `Uptpar_Plant`, `Uptpar_Grass`, or `Uptpar_extern`
11. optional `Input_SoilTemper`, then `Temper`
12. organic-fraction/rate preparation via `Fracpoint` and `Rates1`
13. transport/mineral-response sequence including `Transca`, `Resp_miner`, `Transport`
14. aeration route: `Aeration_original` or `Aeration_sonicg`
15. optional greenhouse-gas route
16. `Rates2`, further transformation/transport, denitrification and corrections
17. `Transgen`
18. uptake integration: `Upintg_Plant`, `Upintg_Grass`, or `Upintg_Extern`
19. crop/output reporting
20. `Outbal_calc`, `Outbal_write`, `Outsel`
21. final `Output_Init`

This is an observed orchestration sequence, not yet a complete dependency graph between every internal variable.

## Process-family inventory

| Process family | Documentation evidence | Source evidence | Reads/writes/state status | PREP01 status |
| --- | --- | --- | --- | --- |
| Carbon / organic matter | fresh OM, dissolved OM, exudates, humus/biomass and transformations | `Rates*`, `Resp_miner`, `Transca`, transformation/output code | detailed state ownership NOT_YET_MAPPED | INVENTORIED |
| Nitrogen | NH4, NO3, organic N, nitrification, denitrification, uptake, gaseous losses | `Denitr`, `Resp_miner`, transport, uptake, GHG routines | detailed state ownership NOT_YET_MAPPED | INVENTORIED |
| Phosphorus | dissolved, sorbed equilibrium/non-equilibrium, precipitated and organic P | P-class, transport/sorption and balance code | detailed state ownership NOT_YET_MAPPED | INVENTORIED |
| Aeration / oxygen | original oxygen-diffusion and SONICG/WFPS routes documented | `Aeration_original`, `Aeration_sonicg`, `OXYDEM` | depends on hydrology and transformation demand | INVENTORIED |
| Greenhouse gases | not covered as a primary 4.0 guide process | `GHGasses`, CH4/N2O and GHG transport routines present in 4.1.5 | 4.1.5-specific theory provenance incomplete | DOCUMENTATION_GAP |
| Solute transport | guide documents advective transport, dispersion representation and sinks/sources | `Transport`, `Transgen`, `Transca`, `Transorp`, `Transsub`, MAPO transport | flow-direction/order sensitive | INVENTORIED |
| Crop interaction | annual crops, grassland and external crop route documented | plant/grass/external root, uptake-parameter and integration routines | external forcing plus internal crop state, exact ownership pending | INVENTORIED |
| Hydrology | SWAP/WATBAL precomputed hydrology documented | `Input_hydro`, `Hydro_detailed`, `Hydro_Aggregated`, MAPO hydrology | exchange contract currently file/runtime coupled | INVENTORIED |
| Management/fertilization | additions, fertilization and tillage documented | `Input_addit`, `Addit` | management schedule plus state mutation | INVENTORIED |
| Boundary conditions | top/lateral/bottom chemistry documented | parser plus upper-boundary concentration routines | forcing/boundary data, exact ownership pending | INVENTORIED |
| Macropore | guide says 4.0 route was not fully operational | MAPO source units exist in 4.1.5 | testbank has no active macropore case | COVERAGE_AND_DOCUMENTATION_GAP |
| Sulphate | not established by supplied 4.0 guide | option appears in testcase configuration; source-level scientific route not yet reconciled | NOT_ASSESSED | DOCUMENTATION_GAP |

## Mass flow and state audit boundary

The 4.0 guide explicitly documents separate mass balances for water, organic matter, ammonium, nitrate, organic nitrogen, phosphate and organic phosphorus. The 4.1.5 source contains `Outbal_Init`, `Outbal_calc` and `Outbal_write` with much larger interfaces.

PREP01 does not yet classify individual variables as canonical persistent state, scratch, forcing or diagnostics. That classification requires a read/write/continuation audit, especially across `Init`, `Inicalc`, transformation, transport and balance routines.

## Migration implication

Process extraction must follow the observed shared ordering and mass-accounting dependencies. Independent documentation and interface audits can run in parallel, but canonical state, time-step semantics, mass accounting and shared exchange contracts remain serial foundation gates.
