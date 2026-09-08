# GHGMais source/testcase provenance evidence

Status: `BLOCKED_SOURCE_TESTCASE_CONTRACT_LINEAGE_MISMATCH`.

This note records a source-bound comparison between the supplied `GHGMais` testcase and the supplied ANIMO 4.1.5 revision-53 source. It is not a proposal to translate or repair the testcase.

## 1. First parser mismatch

The supplied `GHGMais/Input/general.inp` enables greenhouse gases:

`GreenHouseGasOption=1`

and contains a `[GreenHouseGasses]` output-selection block with named keys including:

- `CO2emission_Comp`;
- `CO2emission_Slct`;
- `CO2emission_OMpc`;
- `CH4emission`;
- `N2Oemission`;
- `AnnualGHG`.

It does not contain a `>outGHG:` section.

The supplied revision-53 `input1.for` takes a different route. When `IoptGHG >= 1`, it unconditionally searches `GENERAL.INP` for `>outGHG:` and then reads:

1. `NuCO2fr`;
2. `CO2fr(1:NuCO2fr)`;
3. `CvCH4_CO2` and `CvN2O_CO2`.

The unmodified diagnostic execution therefore stops with `STOP 1995`, reporting that `>outGHG:` is absent.

## 2. Equivalent-looking data are located elsewhere in the testcase

`GHGMais/Input/material.inp` contains a different section:

`>defGHG:`

with the values:

- `CH4_CO2e = 25`;
- `N2O_CO2e = 298`;
- `NuCO2fr = 6`;
- `CO2frno = 11 12 13 14 15 16`.

This strongly suggests that the testcase belongs to an input-contract revision in which at least part of the GHG configuration moved or was redesigned. It does not prove which ANIMO source revision generated or consumed that contract.

## 3. The mismatch is broader than one missing label

A controlled diagnostic input-only probe copied the already-present `>defGHG:` values into a temporary `>outGHG:` section, solely to determine whether the mismatch ended there. That probe is not a candidate reference testcase and its modified inputs are not admitted.

The parser then advanced to a second independent mismatch in `MATERIAL.INP`:

- revision-53 `input1.for` unconditionally requests `>orgcom:` and reads `Cfracom`;
- supplied `GHGMais/Input/material.inp` has no `>orgcom:` section;
- revision-53 `>deffra:` expects fields `frno recfav hufros Ratio_rd_st asfa nifr [pofr]`;
- supplied GHGMais `>deffra:` contains the expanded fields `frno recfav hufros Ratio_rd_st asfa RQ cbfr nifr pofr`.

The additional `RQ` and `cbfr` fields are material because positional list-directed parsing would assign different values to the revision-53 variables even if the missing labels were inserted.

Therefore the case is not safely recoverable by adding one omitted section. It exposes a structurally different GHG/organic-matter input schema.

## 4. Qualification consequence

PREP01 must not:

- invent a `>outGHG:` block;
- drop or reorder `RQ`/`cbfr` columns;
- infer `Cfracom`;
- translate the testcase into the revision-53 schema;
- claim GHGMais as a revision-53 regression or qualification case.

Any such step would manufacture a new testcase and destroy provenance.

The correct owner action is to locate either:

1. the ANIMO source revision that natively accepts the supplied GHGMais contract; or
2. a GHGMais testcase package known to match ANIMO 4.1.5 revision 53.

Only after that lineage is established may GHG scientific qualification begin.

## 5. Current classification

`SOURCE_TESTCASE_PROVENANCE_MISMATCH`

Binary hydrology is not the blocker. The blocker is the textual source/testcase contract lineage.
