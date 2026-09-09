# TTUTIL 4.27 source provenance checkpoint

## Purpose

This note records the source-provenance state for the TTUTIL dependency considered by ANIMO-IO01. It does **not** admit a TTUTIL-backed ANIMO production adapter and it does not alter any frozen ANIMO B0 material.

## Materialized SWAP/WUR distribution

The user-supplied `SWAP_4.3.1.zip` is now available in the qualification runtime and its SHA-256 is:

`2b48353db6cdf00246a1e5c0dcaafc2c61858729fad18446a1dc66359ec2a360`

This exactly matches the SWAP 4.3.1 package identity already pinned by prior project evidence.

The embedded TTUTIL archive is:

`SWAP_4.3.1/tools/SWAP/source/TTUTIL.ZIP`

Its exact SHA-256 is:

`ee40b4bc20b158163318a4a77a1294e0d9430f5cb73641fcf4a2f3c773d01193`

The independently materialized `/mnt/data/ttutil_official/TTUTIL.ZIP` has the same SHA-256, so it is byte-identical to the embedded archive.

The embedded source expands to 168 files:

- 135 `.for` files;
- 18 `.f90` files;
- 11 `.inc` files;
- 4 `.gin` files.

The 153 Fortran compilation units therefore match the previously expected TTUTIL source extent. `ttuver.for` declares `CUR_V=4.27`, so the embedded source baseline is TTUTIL 4.27.

A per-file SHA-256 manifest is recorded in `integration/animo-io/TTUTIL-4.27-SHA256SUMS.txt`.

## Distribution license evidence

The supplied SWAP 4.3.1 distribution contains `license/License.txt`. It states that SWAP version 4 is distributed under LGPL version 3 and that `TTUTIL427.LIB` is distributed under LGPL version 2.1. The present work records that distribution statement as provenance evidence; it does not silently substitute the different historical wording carried by third-party or mirror repositories.

The current WUR download remains behind the WUR registration and license-acceptance form, so this workunit did not fabricate registration information or perform a fresh download on the user's behalf.

## Public `SWAP-model/ttutil` comparison

A public repository exists at:

- repository: `SWAP-model/ttutil`;
- inspected commit: `bd8601dca3cfb449a79accddd39a566811f1a75e`;
- source version declared by its `ttuver.for`: 4.27;
- build metadata version: 4.2.7.

Its README explicitly calls the repository **unofficial**, and byte comparison now proves that it is not an exact substitute for the SWAP 4.3.1 embedded source.

Known byte-level differences include:

- official `rddata.for` Git-blob SHA-1 `5637572c55bc6a1f009cc594f4b6091112670bf5`, mirror `a297cf4f3d48cbc2bf68a71fae19e88da7c4741b`;
- official `ver4_27.for` Git-blob SHA-1 `9859787315ec9d4a6a03afb261f7e9a982b1d991`, mirror `ada71a792bbde74c8ac1baf2c1f3285f1bcd0a2`;
- the official `ver4_27.for` declares `SUBROUTINE VER4_27`, while the inspected mirror file declares `SUBROUTINE VER4_25`.

Therefore the mirror remains useful as public context and build-system reference only. It is **not** the authoritative source used for ANIMO qualification.

## Build and smoke qualification

The exact extracted official source was compiled locally with GNU Fortran 14.2.0 using legacy-compatible flags. All 153 Fortran compilation units compiled and were archived into a static library.

Local build result:

- objects: 153;
- library: `libttutil427_gfortran.a`;
- local library SHA-256: `3b623a668582776bf6b2d4930fe3199c9b59b9b6e7299f6896793a003ca031e6`.

A parser smoke program then executed `RDINIT` plus `RDSINT` on a native TTUTIL file containing `X = 42` and returned `TTUTIL_SMOKE_X=42`.

The static-library hash is evidence for this local compiler/build invocation only; it is not a cross-platform canonical artifact identity.

## Qualification consequence

The former IO01 dependency-provenance blocker is now resolved at source level:

1. the exact SWAP 4.3.1 package bytes are present and match the previously pinned package SHA-256;
2. the exact embedded TTUTIL archive is independently pinned;
3. TTUTIL version 4.27 is source-confirmed;
4. all 168 embedded files are individually hash-manifested;
5. the official source compiles with GNU Fortran 14.2.0 and passes a native parser smoke test;
6. the public mirror has been proven non-identical and is not used as authoritative source.

This does **not** by itself qualify an ANIMO representation-only adapter. The remaining admission condition is behavioural: the strict revision-53 legacy grammar and its historical accept/reject/default semantics must remain explicit, while any native TTUTIL representation must be separately versioned.

No binary hydrology input is converted to TTUTIL. No GHG lineage is normalized. No production migration or B4 admission follows from this source qualification alone.
