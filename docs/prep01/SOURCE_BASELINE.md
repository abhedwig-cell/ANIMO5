# ANIMO legacy source baseline candidate

Status: `AVAILABLE_HASH_FROZEN_PENDING_CONTROLLED_RETENTION_AND_BUILD_QUALIFICATION`.

## Supplied artifact

- project artifact: `ANIMO_4.1.5.53(3).zip`
- size: 350,696 bytes
- SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- file payload: 65 files under `ANIMO_4.1.5.53/`
- extracted payload size: 1,778,068 bytes
- exact per-member hashes: `reference/source/source_manifest.csv`

The archive was inspected without rewriting, repacking, line-ending normalization or source edits.

## Version evidence

`Version.inc` self-identifies:

- tag path: `animo4.1.5`
- revision: `53`
- model: ANIMO, Agricultural Nutrient Model
- build toolchain: `Intel Visual Fortran Composer XE 12.1.0.233 [Intel(R) 64]`

`Animo.for` describes version 4.1 and historical development through 2011. Several file-local RCS comments still mention older tag paths such as `animo4.1.4`; those comments are retained as provenance evidence and are not silently reconciled.

## Source composition

Observed source includes a main program, subroutines/functions and include files. Extensions are predominantly `.for`/`.FOR`, with two `.f90` files and include files including `Animo.inc`, `Param.inc`, `Version.inc`, `outbal1.inc` and `outbal2.inc`.

Potential alternate/duplicate source units are present, notably `input1.for` versus `input1_1.for`, and `Outsel.for` versus `Outselorg.for`. The main-program call signatures are consistent with the newer `input1.for` and `Outsel.for` variants, but build selection remains an explicit build-evidence item rather than being inferred from ZIP timestamps alone.

## Retention boundary

The GitHub repository is public. No redistribution licence or other legal basis for publishing the supplied source archive was established in PREP01. Therefore the raw source archive is not republished to this public repository. Its exact archive identity and all member hashes are persisted. A controlled immutable B0 byte snapshot still requires a storage location with an established legal basis.

No source content has been copied into `src/`; ANIMO5 production migration remains not admitted.
