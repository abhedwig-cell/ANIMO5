# ANIMO-PREP02R — GNU Ruurlo File-Level Comparison Surface

Status: `QUALIFIED_FOR_CROSS_RUNTIME_DIAGNOSTIC_USE_ONLY`.

## Purpose

PREP01 recorded a deterministic GNU Ruurlo result, including an aggregate normalized output-bundle hash and an output-file count. That evidence is useful, but it did not persist the exact file list plus aggregation algorithm needed to use the old aggregate hash as a transparent future cross-runtime comparison contract.

This record therefore defines a new, explicit file-level GNU diagnostic surface for `RuurloGrass`. It does not reinterpret the older PREP01 aggregate hash and it does not create historical B2 evidence.

Machine-readable authority:

`integration/animo-prep/PREP02R_GNU_RUURLO_FILE_SURFACE_20260909.json`

## Pinned identities

Frozen source ZIP SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Frozen testbank ZIP SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Deterministic GNU diagnostic executable SHA-256:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

Compiler used for the recheck:

`GNU Fortran 14.2.0`

The executable hash reproduced exactly from the frozen source under the existing PREP01 GNU diagnostic build contract before the surface was captured.

## Case preparation

The execution copy follows the already qualified PREP01/PREP02 diagnostic adapter semantics:

- Windows separators in the direct file are materialized for the Linux execution copy;
- case-insensitive input-path resolution is materialized without changing scientific values;
- the quoted `PrintBalLabel` spelling is adapted while preserving its character payload;
- PowerStation sequential-unformatted framing is converted to GNU record framing while preserving logical hydrology payload bytes.

These are diagnostic execution adaptations. They are not a native or historical representation claim.

## Execution result

Two clean prepared `RuurloGrass` runs were executed independently.

Both runs reached:

`Successful completion of simulation`

The GNU process exits through legacy `STOP 100`, so the observed process status was `100` with `STOP 100` on stderr. In this source contract that is the successful legacy completion path, not a newly inferred failure.

Each clean prepared case contained 20 files before execution and 92 files after execution. The model changed or created exactly 72 files in each run and deleted none.

## File-level repeat result

For every one of the 72 changed/new files the surface records:

- relative path;
- normalized byte size;
- normalized SHA-256.

Raw bytes differed between the two runs in 35 files. Every one of those raw differences disappeared under the already declared volatile-metadata rules in `tools/compare_legacy_output_trees.py`.

After that declared normalization:

- file set: identical;
- normalized file sizes: identical;
- normalized file hashes: identical for all 72 files;
- normalized differing files: `0`;
- scientific numerical tolerance applied: `false`.

The resulting explicitly defined normalized content-set SHA-256 is:

`6230855d66fab5ca278d7aa6ca1f712ff7a8e58bfd6c7508c05ae3d10ebe01f5`

The content-set algorithm is recorded in the JSON itself and is based on path, normalized size and normalized file hash for every file sorted by UTF-8 path bytes.

## Relation to the earlier PREP01 aggregate

PREP01 recorded for Ruurlo:

- `generated_output_file_count = 73`;
- `normalized_output_bundle_sha256 = df0ec1c5995272e8f663762e4432c2ccf13480f03527cde956f506363d2eefd8`.

The new surface contains 72 changed/new files inside the prepared case tree and uses a newly explicit aggregation algorithm. The earlier repository evidence does not preserve enough information to prove that PREP01's count and aggregate hash used the same capture boundary or aggregation rule.

Therefore PREP02R deliberately does **not**:

- force the new file count to 73;
- try candidate aggregation formulas until the old hash is reproduced;
- infer a scientific difference from the count difference;
- relabel the old aggregate hash as a file-level oracle.

The old PREP01 record remains valid for what it actually proves: deterministic diagnostic execution under its recorded capture convention. The new v1 surface is the transparent contract for the future native-versus-GNU cross-runtime comparison.

## Allowed use

This surface may be used to ask whether the received 2026 Intel-family native executable produces the same ordinary Ruurlo output bytes, after the same declared volatile normalization, on the corresponding output paths.

A complete match would strengthen cross-runtime reconstruction evidence. A mismatch must be classified by path and content and may not be hidden with a global numerical tolerance.

Neither outcome by itself establishes historical ANIMO 4.1.x behaviour.

## Gate effect

`normal_B2_reference_available = false`

`historical_reference_admitted = false`

`production_migration_admitted = false`

The historical acquisition and provenance gate remains separate.
