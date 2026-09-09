# TTUTIL 4.27 source provenance checkpoint

## Purpose

This note records the source-provenance state for the TTUTIL dependency considered by ANIMO-IO01. It does **not** admit a TTUTIL-backed ANIMO production adapter and it does not alter any frozen ANIMO B0 material.

## Materialized SWAP/WUR distribution

The user-supplied `SWAP_4.3.1.zip` is available in the qualification runtime and its SHA-256 is:

`2b48353db6cdf00246a1e5c0dcaafc2c61858729fad18446a1dc66359ec2a360`

This exactly matches the SWAP 4.3.1 package identity already pinned by prior project evidence.

The embedded TTUTIL archive is:

`SWAP_4.3.1/tools/SWAP/source/TTUTIL.ZIP`

Its exact SHA-256 is:

`ee40b4bc20b158163318a4a77a1294e0d9430f5cb73641fcf4a2f3c773d01193`

The independently materialized TTUTIL archive has the same SHA-256, so it is byte-identical to the embedded archive.

The embedded source expands to 168 files:

- 135 `.for` files;
- 18 `.f90` files;
- 11 `.inc` files;
- 4 `.gin` files.

The 153 Fortran compilation units therefore match the previously expected TTUTIL source extent. `ttuver.for` declares `CUR_V=4.27`, so the embedded source baseline is TTUTIL 4.27.

A per-file SHA-256 manifest is recorded in `integration/animo-io/TTUTIL-4.27-SHA256SUMS.txt`.

The exact source can be materialized only from a user-supplied package that matches both the outer package hash and embedded TTUTIL archive hash using `tools/materialize_ttutil427.py`. The tool performs no network download, registration or license acceptance.

## Distribution license evidence

The supplied SWAP 4.3.1 distribution contains `license/License.txt`. It states that SWAP version 4 is distributed under LGPL version 3 and that `TTUTIL427.LIB` is distributed under LGPL version 2.1. The present work records that distribution statement as provenance evidence; it does not silently substitute the different historical wording carried by third-party or mirror repositories.

The current WUR download remains behind the WUR registration and license-acceptance form, so this workunit did not fabricate registration information or perform a fresh download on the user's behalf.

## Public `SWAP-model/ttutil` comparison

A public repository exists at:

- repository: `SWAP-model/ttutil`;
- inspected commit: `bd8601dca3cfb449a79accddd39a566811f1a75e`;
- source version declared by its `ttuver.for`: 4.27;
- build metadata version: 4.2.7.

Its README explicitly calls the repository **unofficial**, and byte comparison proves that it is not an exact substitute for the SWAP 4.3.1 embedded source.

Known byte-level differences include:

- official `rddata.for` Git-blob SHA-1 `5637572c55bc6a1f009cc594f4b6091112670bf5`, mirror `a297cf4f3d48cbc2bf68a71fae19e88da7c4741b`;
- official `ver4_27.for` Git-blob SHA-1 `9859787315ec9d4a6a03afb261f7e9a982b1d991`, mirror `ada71a792bbde74c8ac1baf2c1f3285f1bcd0a2`;
- the official `ver4_27.for` declares `SUBROUTINE VER4_27`, while the inspected mirror file declares `SUBROUTINE VER4_25`.

Therefore the mirror remains useful as public context and build-system reference only. It is **not** the authoritative source used for ANIMO qualification.

## Build and smoke qualification

The exact extracted official source was compiled locally with GNU Fortran 14.2.0 using legacy-compatible flags. All 153 Fortran compilation units compiled and were archived into a static library.

An initial smoke program executed `RDINIT` plus `RDSINT` on a native TTUTIL file containing `X = 42` and returned `TTUTIL_SMOKE_X=42`.

A later clean Pilot-A rebuild again compiled all 153 official TTUTIL units and linked `tools/ttutil_direct_probe.f90` successfully. Static-library byte hashes are intentionally not used as canonical dependency identities because they can vary with build path, object metadata and archive construction even when the exact source and compiler are unchanged. The source-package and per-file source hashes are the canonical provenance anchors.

## DIRECT Pilot A runtime qualification

`tools/qualify_io01_direct_pilot.py` reproduces the bounded runtime qualification from the two user-supplied frozen archives. It:

1. verifies the SWAP 4.3.1 package hash;
2. materializes and verifies all 168 TTUTIL 4.27 files;
3. compiles all 153 Fortran units;
4. links the native DIRECT probe;
5. verifies the frozen ANIMO testbank hash;
6. reads all 10 natural `animo.ini` routing files with the revision-53 compatibility normalizer;
7. emits a separate, deliberately reordered `TTUTILNativeTextAdapter/v1` representation;
8. executes the actual TTUTIL 4.27 reader;
9. compares `LegacyInputBinding/v1` semantic projections field-exactly.

Result: 10/10 natural routing cases are field-exact equivalent. The committed machine-readable evidence is `integration/animo-io/DIRECT-PILOT-QUALIFICATION.json`.

This qualification also records one explicit revision-53 runtime-undefined `Strip` edge. Empty or whitespace-only quoted payloads can make the source form `Fname(0:Ilast)`. That case is `FAIL_CLOSED_NOT_NORMALIZED`, not silently converted into a deterministic compatibility rule.

## Qualification consequence

The former IO01 dependency-provenance blocker is resolved at source level, and Pilot A now has bounded runtime equivalence evidence for the DIRECT routing object:

1. the exact SWAP 4.3.1 package bytes match the pinned package SHA-256;
2. the exact embedded TTUTIL archive is independently pinned;
3. TTUTIL version 4.27 is source-confirmed;
4. all 168 embedded files are individually hash-manifested;
5. the official source compiles with GNU Fortran 14.2.0 and passes runtime reads;
6. the public mirror is proven non-identical and is not used as authoritative source;
7. `LegacyRevision53TextAdapter` and `TTUTILNativeTextAdapter/v1` produce 10/10 field-exact equivalent `LegacyInputBinding/v1` routing objects on the natural testbank.

This supports `QUALIFIED_REPRESENTATION_ONLY_TTUTIL_ADAPTER_CANDIDATE` for Pilot A only. It does not qualify TTUTIL as a general replacement parser for other input families.

No binary hydrology input is converted to TTUTIL. No GHG lineage is normalized. No production migration or B4 admission follows from this source and Pilot-A qualification.
