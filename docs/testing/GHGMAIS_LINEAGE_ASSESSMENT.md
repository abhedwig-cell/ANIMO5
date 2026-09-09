# GHGMais lineage assessment

Status: `NATURAL_CASE_LINEAGE_UNCERTAIN_SOURCE_TESTCASE_CONTRACT_MISMATCH`

`GHGMais` is retained unchanged as B0 historical input evidence. It is not admitted as a revision-53 behavioural case.

## Observed contract differences

The supplied `general.inp` sets `GreenHouseGasOption=1` and contains a named `[GreenHouseGasses]` output block, including `CO2emission_Comp`, `CO2emission_Slct`, `CO2emission_OMpc`, `CH4emission`, `N2Oemission` and `AnnualGHG`. It does not contain the `>outGHG:` section required by supplied revision-53 `input1.for` when `IoptGHG>=1`. Revision 53 expects `NuCO2fr`, a CO2 fraction list, and CH4/N2O CO2-equivalent conversion factors there. The unmodified B1 run stops at this first mismatch with `STOP 1995`.

The case instead places GHG-related values in `material.inp` under `>defGHG:` (`CH4_CO2e=25`, `N2O_CO2e=298`, `NuCO2fr=6`, fraction numbers 11..16). A controlled input-only diagnostic copy of those already-present values into a temporary `>outGHG:` block advanced only to a second independent mismatch. Revision 53 then requires `>orgcom:` with `Cfracom`, which the case lacks. Its `>deffra:` layout also contains extra positional `RQ` and `cbfr` fields compared with the revision-53 schema.

This is therefore a structural schema divergence, not one missing label. Positional translation would change field assignment and cannot be treated as a provenance-preserving repair.

## What can be retained as historical evidence

Reliable B0 facts include the exact supplied bytes and hashes, `Animo41` steering identity, GHG option selection, simulation dates, crop/hydrology member identities, the observed GHG/material schema, and the fact that this package was supplied inside the frozen testbank. These facts describe the artifact.

The following must **not** be attributed to revision 53: successful execution, GHG trajectories, the intended placement/meaning of `RQ`/`cbfr`, the source revision that consumes `>defGHG:`, or numerical equivalence with revision-53 GHG code.

## Possible lineage

The evidence is consistent with a later or divergent ANIMO 4.1-era input-contract lineage in which GHG and organic-matter fields were reorganized. The exact consuming source revision has not been established. No exact revision number is inferred.

## Required closure

Close the lineage gap only by obtaining either a source/executable that natively consumes the supplied GHGMais schema with provenance, or an independently provenance-qualified GHGMais package known to match revision 53. A compatibility transform may be useful diagnostically, but it remains a derived artifact and cannot convert this B0 case into a revision-53 historical reference.
