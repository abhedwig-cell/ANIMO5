# Testcase inventory interpretation

The machine-readable table is `TESTCASE_INVENTORY.csv`; exact member-level identities are in `reference/testcases/testbank_manifest.csv`. Diagnostic execution hashes are also persisted in `integration/animo-prep/PREP01_DIAGNOSTIC_EXECUTION.json`.

## Frozen cases and current execution evidence

| Testcase | Period | Configuration evidence | Provenance classification | Current execution status |
| --- | --- | --- | --- | --- |
| CranGrass | 1992-01-01 to 1999-12-31 | P on, aeration 0, internal crop uptake | documented example from input header | diagnostic success, deterministic, reference not qualified |
| CranMais | 1974-01-01 to 1982-12-31 | P off, aeration 0, internal crop uptake | documented example from input header | diagnostic success, deterministic, reference not qualified |
| GHGMais | 2010-01-01 to 2019-12-31 | GHG on, external crop uptake | feature case, provenance unverified | blocked: supplied input contract does not match revision-53 source |
| GrassPeat | 1986-01-01 to 2000-12-31 | P on, aeration 1, external crop uptake | feature case, provenance unverified | diagnostic success, deterministic, reference not qualified |
| LWKM_gras_1040.2021.2045 | 2021-01-01 to 2045-12-31 | P on, aeration 1, external crop uptake | production/reference-named case, unverified | diagnostic success, deterministic, reference not qualified |
| Puitmijn_Cranendonck_60 | 2002-01-01 to 2013-12-31 | P on, aeration 0, internal crop uptake | project case, provenance unverified | diagnostic success, deterministic, reference not qualified |
| RuurloGrass | 1980-01-01 to 1985-04-30 | P off, aeration 0, internal crop uptake | unknown provenance | diagnostic success, deterministic, reference not qualified |
| STONE_akk_0006.2001.2015 | 2001-01-01 to 2015-12-31 | P on, aeration 1, external crop uptake | historical/reference-named case, unverified | diagnostic success, deterministic, reference not qualified |
| Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA | 2015-01-01 to 2017-12-31 | P on, aeration 1, internal crop uptake | project case, provenance unverified | diagnostic success, deterministic, reference not qualified |

## Diagnostic versus reference executability

Eight cases now complete under the reproducible GNU diagnostic build. Repeated runs and an independently rebuilt diagnostic executable produce the same generated output after normalizing only volatile run timestamp and elapsed CPU seconds.

This changes the previous executability assessment, but not the qualification status. The GNU build uses inferred legacy compiler semantics, including eight-byte default `REAL` and static local storage, plus explicit execution-only compatibility adapters. Historical Intel equivalence is not yet demonstrated.

Therefore:

- diagnostic successful cases: `8/9`;
- deterministic diagnostic cases: `8/9`;
- qualified RR cases: `0/9`;
- qualified QG cases: `0/9`;
- trusted numerical oracle cases: `0/9`.

## GHGMais blocker

`GHGMais` is no longer blocked by binary hydrology. Its multiblock PowerStation record framing is parsed successfully.

The case stops in revision-53 `input1.for` because `IoptGHG >= 1` requires a `>outGHG:` section, while the supplied `GHGMais/Input/general.inp` has no such section and uses a different set of GHG output keys. The testcase is therefore not silently translated. Its matching ANIMO source/version provenance must be found before GHG qualification.

## Numerical oracle status

The original frozen `Output/` directories remain empty. Diagnostic outputs generated during PREP01 are retained as reproducibility evidence only and are **not** promoted to `FROZEN_LEGACY`, `CORRECTED_LEGACY_REFERENCE`, RR or QG values.

## Static packaging observations

Six cases contain `animo.ini` references that do not resolve to files in the archive. Successful diagnostic execution shows that several of those unresolved paths are not mandatory for the active configuration. The exact conditional parser contract is now source-auditable and should be captured during the detailed I/O contract work rather than repaired at packaging level.
