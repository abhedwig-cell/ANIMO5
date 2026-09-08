# First process and dataflow inventory

Evidence level: `TESTCASE_CONFIGURATION_ONLY`.

Without production source or theory documentation, PREP01 does not claim detailed process equations, ordering, state variables, or mass flows. The register below identifies process families that are directly visible in testcase configuration names/comments and marks deeper fields as not assessed.

| Process family | Evidence observed | Reads/writes/state | Dependencies | PREP01 status |
| --- | --- | --- | --- | --- |
| Carbon / organic matter | organic material/fraction definitions and organic-matter balance output options appear in inputs | NOT_ASSESSED | soil, management likely, exact contract NOT_ASSESSED | INVENTORIED |
| Nitrogen | N material fractions, NH4/NO3 boundary concentrations and N balance options are present | NOT_ASSESSED | hydrology/crop/management likely, exact contract NOT_ASSESSED | INVENTORIED |
| Phosphorus | `PhosphorusCycle` option is present and active in 6 of 9 cases | NOT_ASSESSED | chemistry/hydrology, exact contract NOT_ASSESSED | INVENTORIED |
| Sulphate | `SulphateSimulation` option is present and inactive in all 9 cases | NOT_ASSESSED | NOT_ASSESSED | COVERAGE_GAP |
| Aeration / redox related | `AerationModel` values 0 and 1 occur | NOT_ASSESSED | hydrology/soil, exact contract NOT_ASSESSED | INVENTORIED |
| Greenhouse-gas option | active only in `GHGMais` | NOT_ASSESSED | NOT_ASSESSED | FEATURE_CASE_PRESENT |
| Solute/nutrient transport | detailed hydrologic input is selected in all cases and boundary concentrations are supplied | NOT_ASSESSED | hydrology | INVENTORIED |
| Crop interaction | `CropUptakeModel` values 0 and 1 occur; `PLANT.INP` and optional crop external input exist | NOT_ASSESSED | crop data / external crop route | INVENTORIED |
| Hydrology | all cases select `HydrologicInput=2`; binary hydrology inputs are present | NOT_ASSESSED | SWAP/SWATRE-derived input likely from filenames only | INVENTORIED |
| Management/fertilization | `MANAGEMENT.INP` appears in all cases; some files contain crop and material additions | NOT_ASSESSED | time/crop/material | INVENTORIED |
| Boundary conditions | `BOUNDARY.INP` appears in all cases | NOT_ASSESSED | precipitation/runon/irrigation chemistry visible in comments | INVENTORIED |
| Macropore | `MacroPoreOption=0` in all 9 cases | NOT_ASSESSED | NOT_ASSESSED | NO_ACTIVE_TEST_COVERAGE |

## Ordering dependencies

`NOT_ASSESSED` until source and/or theory documentation are frozen.

## Persistent state, temporary work and mass flows

`NOT_ASSESSED` until source ingest. PREP01 intentionally does not infer persistent state from file names alone.
