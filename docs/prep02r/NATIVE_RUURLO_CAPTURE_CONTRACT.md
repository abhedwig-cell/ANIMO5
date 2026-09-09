# ANIMO-PREP02R — Native Ruurlo Reference Capture Contract

Status: `DIAGNOSTIC_NATIVE_C10_READY_IF_WINDOWS_RUNTIME_AVAILABLE_REFERENCE_NATIVE_STILL_PROVENANCE_BLOCKED`.

## Purpose

Define the exact evidence surface for native ANIMO execution. The preferred first case is `RuurloGrass`.

Two execution purposes are now distinguished:

1. `REFERENCE_NATIVE_ATTEMPT`: requires a provenance-qualified historical or explicitly governance-admitted equivalent reference artifact;
2. `CROSS_RUNTIME_DIAGNOSTIC_NATIVE`: may use a clearly classified nonhistorical native rebuild to learn about compiler/runtime behaviour, but can never be relabelled as historical B2 evidence.

The received `PREP02R-C10` executable is eligible only for the second purpose.

## Preconditions

Every native execution requires:

- executable receipt manifest and SHA-256 identity;
- explicit lineage classification;
- artifact bytes unchanged from receipt;
- frozen testcase bytes identified before execution;
- no corrected-legacy source or translated scientific testcase substituted;
- execution purpose declared before launch.

A `REFERENCE_NATIVE_ATTEMPT` additionally requires provenance strong enough for the claimed reference route.

A `CROSS_RUNTIME_DIAGNOSTIC_NATIVE` may proceed with a nonhistorical candidate only when its nonreference classification is recorded up front and all generated evidence remains labelled diagnostic.

## Received diagnostic candidate C10

The supplied native executable received on 2026-09-09 is:

`animo41.exe`

SHA-256:

`40e29853a0431cc7e2b787dfeb1870f44e1ff402b5aaebd6f56c8365fc5b178d`

Classification:

`MODERN_NATIVE_REBUILD_NOT_HISTORICAL_REFERENCE`

Static evidence identifies it as a 2026 x64 Debug rebuild. Its use is therefore limited to:

`CROSS_RUNTIME_DIAGNOSTIC_NATIVE`.

Before every launch the executable hash must be recomputed and must match exactly.

## Frozen first case

Primary case:

`RuurloGrass`

Frozen testbank archive SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

The supplied historical-style runner is:

```text
..\animo41.exe Animo.ini
copy *.bal Output\*.bal
copy *.out Output\*.out
del *.bal
del *.out
pause
```

For qualification capture, do **not** execute the post-processing runner as the first action. It copies and deletes generated root-level output and would destroy the raw pre-postprocessing tree.

The first controlled invocation should therefore run the executable directly from the untouched extracted `RuurloGrass` working directory with:

```text
<absolute-or-staged-path>\animo41.exe animo.ini
```

The raw generated tree must be captured before optionally reproducing the historical runner's copy/delete behaviour as a separate filesystem-semantics check.

The native run should use the original case bytes and original `SWATRE.UNF` bytes directly. Windows case-insensitive filename resolution and backslash paths are part of the native runtime contract, not testcase changes.

## Capture before execution

Record:

- declared purpose: `REFERENCE_NATIVE_ATTEMPT` or `CROSS_RUNTIME_DIAGNOSTIC_NATIVE`;
- executable filename and SHA-256;
- receipt-manifest identity;
- claimed version/revision and provenance source;
- lineage classification;
- operating-system version/build and architecture;
- native or VM environment identity;
- locale, code page and timezone when they may affect formatted output;
- required runtime libraries and hashes when available;
- command line and working-directory layout;
- complete input-file inventory and SHA-256 values;
- exact hydrology file identity;
- whether any filename/path compatibility staging was needed;
- explicit `input_content_transformed = false` for the preferred native path.

If the executable is reconstructed from source rather than supplied as a binary, additionally capture:

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
- stdout and stderr capture;
- all warnings and STOP messages;
- complete generated output tree before runner post-processing;
- byte size and SHA-256 for every generated output file;
- files created, missing or unexpectedly retained;
- output timestamps as metadata while keeping scientific bytes untouched;
- runtime duration as diagnostic information only;
- complete input-tree hashes again after execution to prove input nonmutation.

The raw output tree must be preserved before any normalization or comparison.

The ANIMO 4.0 user guide documents the normal successful-completion text as:

`Successful completion of simulation`

Presence of that text is a completion indicator, not by itself a scientific qualification result.

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

For `PREP02R-C10`, even exact native/GNU agreement would mean only:

`CROSS_RUNTIME_CORROBORATION_FOR_A_2026_NATIVE_REBUILD`.

It would not prove historical revision-53 execution.

## Observer boundary

Observer-only high-precision capture remains blocked until an ordinary native build/reference contract has first been established. The observer build must reproduce ordinary native legacy output before its additional unrounded quantities are trusted.

## Machine-readable record

Use:

`integration/animo-prep/PREP02R_NATIVE_RUN_MANIFEST_TEMPLATE.json`

The template deliberately defaults all admission fields to `false` and leaves evidence fields null until a real native run exists.
