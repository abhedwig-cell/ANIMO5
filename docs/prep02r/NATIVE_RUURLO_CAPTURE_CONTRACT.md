# ANIMO-PREP02R — Native Ruurlo Reference Capture Contract

Status: `READY_IF_PROVENANCE_QUALIFIED_NATIVE_ARTIFACT_IS_OBTAINED`.

## Purpose

Define the exact evidence surface for the first native ANIMO reference attempt. The preferred first case is `RuurloGrass`. This contract is preparation only. It does not admit execution of an untrusted artifact and does not qualify a reference by itself.

## Preconditions

Native execution is permitted only after all of the following are explicitly reviewed:

- received executable or build artifact has a receipt manifest and SHA-256 identity;
- lineage is classified as exact revision-53 candidate, provenance-qualified nearby 4.1.x candidate, or another explicitly named lineage;
- provenance is strong enough to justify a controlled qualification attempt;
- the artifact remains unmodified from receipt;
- the frozen testcase bytes to be used are identified before execution;
- no corrected-legacy source or translated testcase is substituted.

## Frozen first case

Primary case:

`RuurloGrass`

Frozen testbank archive SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Known historical runner form:

```text
..\animo41.exe Animo.ini
```

The native run should use the original case bytes and historical hydrology bytes directly whenever the native runtime supports them. Any filesystem-only staging, drive mapping or compatibility environment must be recorded. Input-content transformation is not allowed silently.

## Capture before execution

Record:

- executable filename and SHA-256;
- receipt-manifest identity;
- claimed version/revision and provenance source;
- lineage classification and admission rationale for attempting the run;
- operating-system version/build and architecture;
- native or VM environment identity;
- locale, code page and timezone when they may affect formatted output;
- required runtime libraries and hashes when available;
- command line and working-directory layout;
- complete input-file inventory and SHA-256 values;
- exact hydrology file identity;
- whether any filename/path compatibility staging was needed;
- explicit `input_content_transformed = false` for the preferred native path.

If the executable is reconstructed from historical source rather than supplied as a binary, additionally capture:

- exact source archive or checkout identity;
- compiler identity and complete compiler command line;
- project files and hashes;
- linker command line;
- optimization and floating-point settings;
- default REAL and DOUBLE PRECISION semantics;
- local-storage policy;
- unformatted record convention;
- runtime-library assumptions.

## Capture during and after execution

Capture without filtering:

- invocation start and end timestamps;
- process exit status;
- stdout and stderr bytes and SHA-256;
- all warnings and STOP messages;
- complete generated output tree;
- byte size and SHA-256 for every output file;
- files created, missing or unexpectedly retained;
- output timestamps as metadata, while keeping scientific bytes untouched;
- runtime duration as diagnostic information only.

The raw output tree must be preserved before any normalization or comparison.

## Repeat determinism

Before comparing against GNU, repeat the same native execution from a clean copy of the same frozen input tree when practical.

Classify repeat behaviour as:

- `NATIVE_REPEAT_EXACT` when complete output trees are byte-identical;
- `NATIVE_REPEAT_DECLARED_VOLATILE_ONLY` only when differences are confined to explicitly inventoried volatile metadata;
- `NATIVE_REPEAT_DIFFERENT_FAIL_CLOSED` for any other difference.

Do not invent a tolerance to force repeat agreement.

## Native versus GNU comparison

After native capture, compare against the existing deterministic GNU diagnostic route in layers:

1. file-set and path semantics;
2. lexical formatting and record layout;
3. warnings and runtime-message classes;
4. numerically parsed ordinary output values;
5. state quantities where exposed;
6. flux quantities where exposed;
7. mass-balance terms and residuals;
8. process trajectory and event timing.

Use `tools/compare_legacy_output_trees.py` for fail-closed formatted-tree comparison, but treat its output only as comparison evidence. A comparator match does not itself admit either build as reference.

No global numerical tolerance is defined. Any non-exact numerical difference must first be classified by variable, unit, output precision, scale and likely compiler/runtime mechanism.

## Observer boundary

Observer-only high-precision capture remains blocked until an ordinary native build/reference contract has first been established. The observer build must reproduce ordinary native legacy output before its additional unrounded quantities are trusted.

## Machine-readable record

Use:

`integration/animo-prep/PREP02R_NATIVE_RUN_MANIFEST_TEMPLATE.json`

The template deliberately defaults all admission fields to `false` and leaves evidence fields null until a real native artifact exists.
