# TTUTIL pilot selection

## Result

No runtime TTUTIL adapter is qualified in IO01 at this point. The audit selects bounded pilots but deliberately does not vendor or introduce an unpinned TTUTIL dependency into ANIMO5.

### Pilot A: direct-file routing contract

Selection: `ANIMO.INI / direct file`.

Why first:

- natural B0 coverage is broad: every supplied testcase has an `animo.ini` routing file;
- it contains no physical parameter units and no scientific calculations;
- the normalized target is narrow, `LegacyInputBinding`;
- it is a good place to prove the required distinction between exact legacy quirks and a cleaner native schema.

Qualification requirements include valid path mapping, version header, quoted-name handling, duplicate-selector behaviour, unknown-selector behaviour, missing required bindings and conditional CHE/CRU/STE bindings.

A native TTUTIL-format steering file may be piloted as a *second versioned representation*, but the old direct file must remain accepted by `LegacyRevision53TextAdapter` for a representation-only claim.

### Pilot B candidate: non-GHG static MATERIAL core

Selection status: `SELECTED_AFTER_PILOT_A_ONLY`.

Use a natural non-GHG case such as RuurloGrass. Restrict the first pilot to the material schema actually active in that case and dump every normalized field, array dimension, unit and default flag. Do not include GHGMais or infer cross-lineage GHG fields.

MATERIAL is preferable to a first SOIL or PLANT pilot because it is static and has no dynamic runtime stream, but it is still not low risk. Stable-DOM and later GHG extensions mean the adapter must be explicitly schema-versioned.

## Why SOIL and PLANT are not first

SOIL controls geometry, feature-dependent arrays and source-only compatibility defaults. PLANT contains crop-type-dependent records, optional harvesting/meteo sections and source-side scientific compatibility defaults. Both are suitable later, after the normalization/default machinery has been proven on a narrower surface.

## Implementation blocker

`TTUTIL_DEPENDENCY_AND_LEGACY_STRICTNESS_CONTRACT_NOT_PINNED`.

The public TTUTIL syntax is order-independent and name-based, while revision-53 ANIMO41 named GENERAL input is sequential. Before any TTUTIL code enters this repository, the work must pin the TTUTIL source/version/license provenance and decide whether TTUTIL is only a lexical utility behind a strict legacy adapter or a separate native-schema adapter. Implementing first and deciding this later would make parser behaviour accidental.

No pilot is classified `QUALIFIED_REPRESENTATION_ONLY_TTUTIL_ADAPTER_CANDIDATE` yet.
