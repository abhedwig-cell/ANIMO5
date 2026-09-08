# Testcase inventory interpretation

The machine-readable table is `TESTCASE_INVENTORY.csv`; exact member-level identities are in `reference/testcases/testbank_manifest.csv`.

## Frozen cases

| Testcase | Period | Configuration evidence | Provenance classification | Executability |
| --- | --- | --- | --- | --- |
| CranGrass | 1992-01-01 to 1999-12-31 | P on, aeration 0, internal crop uptake | documented example from input header | blocked: executable absent |
| CranMais | 1974-01-01 to 1982-12-31 | P off, aeration 0, internal crop uptake | documented example from input header | blocked: executable absent |
| GHGMais | 2010-01-01 to 2019-12-31 | GHG on, external crop uptake | feature case, provenance unverified | blocked: executable absent |
| GrassPeat | 1986-01-01 to 2000-12-31 | P on, aeration 1, external crop uptake | feature case, provenance unverified | blocked: executable absent |
| LWKM_gras_1040.2021.2045 | 2021-01-01 to 2045-12-31 | P on, aeration 1, external crop uptake | production/reference-named case, unverified | blocked: executable absent |
| Puitmijn_Cranendonck_60 | 2002-01-01 to 2013-12-31 | P on, aeration 0, internal crop uptake | project case, provenance unverified | blocked: executable absent |
| RuurloGrass | 1980-01-01 to 1985-04-30 | P off, aeration 0, internal crop uptake | unknown provenance | blocked: executable absent |
| STONE_akk_0006.2001.2015 | 2001-01-01 to 2015-12-31 | P on, aeration 1, external crop uptake | historical/reference-named case, unverified | blocked: executable absent |
| Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA | 2015-01-01 to 2017-12-31 | P on, aeration 1, internal crop uptake | project case, provenance unverified | blocked: executable absent |

## Numerical oracle status

No case is admitted as RR or QG evidence. All frozen `Output/` directories are empty. No rounded report table is promoted to an oracle.

## Static packaging anomalies

Six cases have `animo.ini` entries that do not resolve to a file in the archive. This is an observed packaging fact, not yet a defect. The parser may treat some keys as optional depending on configuration. That question remains `NOT_ASSESSED`.
