# ANIMO-GHG01 — GHG input-lineage reconciliation

Status: `GHGMAIS_NOT_REV53_INPUT_CONTRACT_COMPATIBLE_EXACT_CONSUMING_LINEAGE_UNRESOLVED`

No input in the frozen testbank is repaired or silently translated by this assessment.

## 1. Frozen evidence

- revision-53 source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- supplied testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- frozen GHGMais `animo.ini`: `1259cb35b191a40da55d234264a456653d82c85fc918754c88b859b973eb6024`
- frozen GHGMais `runanimo.bat`: `f751bc72630302fd24637923ae7e6e1c119ce68f4f5e1424ccd0434dd081d8b5`
- frozen GHGMais `Input/general.inp`: `0210c9529ae90178412154aa40cf74b44872129a646ad933857650448220224f`
- frozen GHGMais `Input/material.inp`: `65bd1870d42b33008b45edd1d928a6f42d9b10bd9a01acca535f0af891745804`
- frozen GHGMais `Input/soil.inp`: `6a07157f64c0913f977487c1719794c1126416646b0b329ce39940935601f760`
- frozen GHGMais `Input/initial.inp`: `93d2ac920f614b2a92f5b85f83cc1c6678403baaa6afdfdba54f8a5ddca851a8`
- frozen GHGMais `Input/result.bun`: `cd4202745ee8a9ccd890e6aa6d3f551ff3bb80041efd178aedb3f5f4bbe002e2`

These hashes identify the artifact. They do not establish its original date, exact ANIMO executable, or native producing release.

## 2. Runner identity

The supplied direct file starts with `Animo41`. `runanimo.bat` invokes only:

```text
ANIMO animo.ini
```

There is no executable in the supplied GHGMais package whose binary identity can be tied to revision 53. `Animo41` establishes a steering/input-family identity, not an exact revision.

The supplied hydrology binary contains embedded provenance text:

```text
Project: SOMERS
Model version: Swap 4.2.277
Generated at: 2026-07-28 11:16:14
```

This matters for lineage interpretation. The frozen GHGMais testbank member is a composite/reworked supplied artifact, not evidence of an untouched 2007/2008 execution package. It remains legitimate B0 historical input evidence as supplied, but its internal timestamps and modern SWAP hydrology must not be used to infer an old ANIMO runner.

## 3. Revision-53 GENERAL contract

For `AnimoVersion=41`, `input1.for` reads named `>simopt:` options including:

- `HydrologicInput`;
- `PhosphorusCycle`;
- `SulphateSimulation`;
- `AerationModel`;
- `CropUptakeModel`;
- `MacroPoreOption`;
- `GreenHouseGasOption`;
- `SoilTempFile`.

When `IoptGHG>=1`, revision 53 additionally requires a distinct `>outGHG:` label in `GENERAL.INP` containing, in order:

1. `NuCO2fr`;
2. the `CO2fr(1:NuCO2fr)` fraction-number list;
3. `CvCH4_CO2` and `CvN2O_CO2`.

The parser fails closed if that label is absent.

## 4. GHGMais GENERAL contract

GHGMais uses the named ANIMO 4.1-style simulation options and sets:

```text
GreenHouseGasOption=1
```

It contains a named `[GreenHouseGasses]` output-selection block with:

- CO2 output selections enabled;
- CH4 emission, concentration, production and oxidation outputs disabled;
- N2O emission, system concentration, liquid concentration, denitrification production, nitrification production and reduction enabled;
- annual GHG enabled;
- subsidence disabled.

However, the frozen file contains no `>outGHG:` label. Therefore it cannot natively satisfy the revision-53 parser even though it clearly represents a GHG-active ANIMO 4.1-style input family.

## 5. `>defGHG:` versus revision-53 `>outGHG:`

GHGMais places this GHG metadata in `MATERIAL.INP`:

```text
>defGHG:
25. 298. 6 11 12 13 14 15 16
```

The comments identify the fields as CH4 CO2-equivalent factor, N2O CO2-equivalent factor, number of selected CO2 fractions and the selected fraction numbers.

Revision 53 expects equivalent-looking semantic categories under `GENERAL.INP >outGHG:`, but in a different record order: fraction count and fraction list first, then the two conversion factors. Similar-looking values are evidence of lineage relation, not permission to call the schemas equivalent.

The observed divergence is therefore both location and record-layout divergence.

## 6. `>orgcom:` and `>deffra:` divergence

Revision 53 requires `MATERIAL.INP >orgcom:` and reads a single global `Cfracom`, validated in `[0.1,1.0]`.

GHGMais has no `>orgcom:` block. Instead each `>deffra:` row contains additional positional columns identified in its own header as `RQ(fn)` and `cbfr(fn)` before `nifr(fn)`.

Revision 53 reads each `>deffra:` row as:

```text
Frno, Recfav, Hufros, Ratio_rd_st, Asfa, Nifr, [Pofr]
```

It does not read the GHGMais `RQ` and `cbfr` columns there. Consequently, passing the GHGMais row directly to revision 53 shifts positional assignment. A per-fraction `cbfr` also cannot be silently collapsed into the single revision-53 `Cfracom` without introducing an interpretation not encoded by the revision-53 schema.

This is the decisive evidence that GHGMais is not merely missing one label.

## 7. Soil and initial GHG contract overlap

Unlike the material schema, important later GHG blocks do align structurally with revision-53 expectations:

GHGMais `SOIL.INP` contains:

- `>Ghgdif:`;
- `>GhgCH4:` with production, oxidation, atmospheric concentration, ebullition and vegetation-related parameters;
- `>GhgN2O:` with denitrification competition, nitrification fraction response and atmospheric concentration parameters.

GHGMais `INITIAL.INP` contains:

- `>methan:` system CH4-C state;
- `>nitoxi:` system N2O-N state.

Those overlaps strengthen the conclusion that the case belongs to a closely related later GHG lineage. They do not remove the earlier parser incompatibilities.

## 8. Official 2005 ANIMO 4.0 comparison

The official 2005 ANIMO 4.0 user guide documents a five-field `>simopt:` record and no dedicated GHG input blocks such as `>outGHG:`, `>defGHG:`, `>Ghgdif:`, `>GhgCH4:`, `>GhgN2O:`, `>methan:` or `>nitoxi:`. It does document CO2 production, N2O as part of the N cycle, denitrification and aeration.

This establishes a useful negative lineage boundary: neither the GHGMais contract nor the revision-53 GHG contract should be called the documented 2005 ANIMO 4.0 input contract.

## 9. Lineage conclusion

The strongest defensible statement is:

`GHGMais` represents a GHG-active ANIMO 4.1-era or closely related development/input family that shares substantial GHG state and parameter vocabulary with revision 53 but differs structurally in GHG metadata placement and organic-fraction schema. The exact source or executable that natively consumes the supplied schema has not been identified.

Do not infer an exact revision from the `Animo41` direct-file token, comments dated 2010, file timestamps, or the current 2026 SWAP hydrology payload.

Closure requires either:

1. provenance-qualified source/executable code that natively consumes `>defGHG:` plus the GHGMais `>deffra:` layout; or
2. an independently provenance-qualified GHG testcase known to be native to revision 53.

Until then: `TESTCASE_LINEAGE_BLOCKED` and `REFERENCE_BLOCKED`.