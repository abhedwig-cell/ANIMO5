# TTUTIL pilot selection and qualification

## Result

Pilot A is now classified:

`QUALIFIED_REPRESENTATION_ONLY_TTUTIL_ADAPTER_CANDIDATE`

This classification is deliberately narrow. It applies only to the `DIRECT/animo.ini` routing contract normalized as `LegacyInputBinding/v1`. It does not admit a production input migration, a general TTUTIL replacement for revision-53 input, binary hydrology conversion, restart/config conflation, or GHG schema normalization.

## Pilot A: DIRECT/animo.ini routing contract

Two separate representation contracts are preserved:

- `LegacyRevision53TextAdapter` for the historical A4/A80 DIRECT grammar;
- `TTUTILNativeTextAdapter/v1` for a new versioned, name-based TTUTIL representation.

The native representation is not a drop-in parser for legacy files. It is a second representation that must normalize to the same narrow object.

### Runtime qualification

The reproducible qualification harness is:

- `tools/io01_direct_pilot.py`;
- `tools/materialize_ttutil427.py`;
- `tools/ttutil_direct_probe.f90`;
- `tools/qualify_io01_direct_pilot.py`;
- `tests/io/test_io01_direct_pilot.py`.

The committed evidence is `integration/animo-io/DIRECT-PILOT-QUALIFICATION.json`.

Against the frozen ANIMO testbank:

- natural `animo.ini` cases: 10;
- field-exact semantic equivalence passes: 10/10;
- normalized object: `LegacyInputBinding/v1`;
- TTUTIL version: 4.27;
- exact SWAP 4.3.1 package SHA-256: `2b48353db6cdf00246a1e5c0dcaafc2c61858729fad18446a1dc66359ec2a360`;
- embedded TTUTIL archive SHA-256: `ee40b4bc20b158163318a4a77a1294e0d9430f5cb73641fcf4a2f3c773d01193`;
- TTUTIL files verified: 168;
- Fortran compilation units built: 153;
- qualification compiler: GNU Fortran 14.2.0.

The native files are intentionally emitted in a different variable order from the legacy routing records. Exact normalized equality therefore demonstrates the intended representation boundary rather than accidental preservation of legacy record order.

GHGMais is included only at the routing-object level. This does not qualify the incompatible GHG input schema or erase its lineage issue.

## Legacy behaviour retained or made explicit

The compatibility normalizer preserves the defined revision-53 DIRECT behaviour needed by Pilot A, including:

- exact `Animo40` / `Animo41` first-seven-character header recognition;
- A4 selector and A80 payload truncation/padding semantics;
- quoted-name `Strip` behaviour where defined;
- duplicate known selectors use last assignment;
- unknown selectors are ignored in legacy mode but recorded diagnostically;
- absent `MES` defaults to `message.Out`;
- absent `GEN` is rejected before downstream physics;
- EOF without an explicit `END` is accepted at the DIRECT-read stage;
- CHE and STE selector presence is preserved explicitly.

The native TTUTIL schema intentionally fails closed on duplicate keys, unknown keys and missing mandatory `SchemaVersion`, `AnimoVersion` or `GEN`.

## Explicit undefined-behaviour exclusion

One revision-53 `Strip` edge is not normalized into a fake deterministic legacy contract.

For an empty or whitespace-only quoted payload such as `MES=""`, `Istart` can remain zero while `Ilast` becomes positive. The source then evaluates `Fname(0:Ilast)` although `Fname` is declared `CHARACTER(80)` with Fortran indices starting at 1. A bounds-checked build stops; an unchecked build may be runtime-dependent.

Pilot A therefore classifies this edge as:

`FAIL_CLOSED_NOT_NORMALIZED`

A blank unquoted payload, which leaves `Ilast=0`, remains a defined path and reaches the historical blank-value validation such as error 1016 for `MES=`.

## Pilot B candidate: non-GHG static MATERIAL core

Pilot B is now eligible to start as a separate bounded follow-on, but is not yet qualified.

Selection remains:

`MAT non-GHG static core`, using a natural non-GHG case such as RuurloGrass.

The first MATERIAL pilot must remain restricted to the schema actually active in that case and compare every normalized field, array cardinality, unit and default/presence flag before any model-output regression. GHGMais must not be used to infer or normalize cross-lineage GHG fields.

MATERIAL is preferred over SOIL or PLANT for the next pilot because it is static and has no dynamic runtime stream, while still exercising typed arrays and schema-version ownership.

## Non-admissions

Pilot A changes no scientific equations or state ownership. It does not vendor the WUR distribution automatically, does not alter frozen B0 source/testcases, does not convert binary hydrology, does not normalize GHG lineage, and does not admit production migration or B4.
