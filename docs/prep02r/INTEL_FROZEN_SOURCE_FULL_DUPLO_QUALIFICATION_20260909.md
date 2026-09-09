# ANIMO-PREP02R — Frozen-source Intel full compatible-suite duplo qualification, 2026-09-09

Status: `QUALIFIED_CURRENT_FROZEN_SOURCE_INTEL_EXECUTABLE_BASELINE_REPEAT_DETERMINISTIC_8_CASES`

## Scope

This record qualifies repeatability of the project-selected current Intel executable baseline built directly from the frozen ANIMO 4.1.5 revision-53 source tree. It does not create or claim historical B2.

Leading executable for this qualification:

- SHA-256: `da51093a9da7bd99caee9898c713ab78eda972e3ce6e4bf5b2b2cb66bdab9e0e`
- build route: supplied Intel Visual Fortran project, `Debug|x64`, frozen revision-53 source tree
- executable path at execution time: `R:\AbV\intel_base\ANIMO_4.1.5.53\x64\Debug\animo41.exe`

Frozen testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

`GHGMais` was deliberately excluded because its frozen testcase has the already-known revision-53 input-contract mismatch. Its unexecuted source/input directory remains present in the extracted trees and is not counted as a qualified case.

## Received evidence packages

Two independent complete run trees were created from two fresh extractions of the frozen testbank and uploaded after execution.

- `intel_r53_run1.zip` SHA-256: `116e5d41c18281618a4c8684eb32b9f844c48c7b7e64f4a5824d1eff9ec70d06`
- `intel_r53_run2.zip` SHA-256: `40acbff9d192353cd33077929ea8c1494ead3789643fc6ade763f84f1a324903`

Each archive contains 524 files under its run root.

## Execution result

All 16 requested executions reached the legacy successful termination `STOP 100` / exit code `100` and printed `Successful completion of simulation`:

| Case | Run 1 | Run 2 |
|---|---:|---:|
| CranGrass | 100 | 100 |
| CranMais | 100 | 100 |
| GrassPeat | 100 | 100 |
| LWKM_gras_1040.2021.2045 | 100 | 100 |
| Puitmijn_Cranendonck_60 | 100 | 100 |
| RuurloGrass | 100 | 100 |
| STONE_akk_0006.2001.2015 | 100 | 100 |
| Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA | 100 | 100 |

All sixteen captured `STDERR.txt` files are empty. The sixteen paired stdout/stderr capture files are raw byte-identical between run 1 and run 2. `GrassPeat` retains its pre-existing stdout messages labelled `Error` about requested output-file specifications but nevertheless reaches the normal successful completion; this qualification does not reinterpret or suppress those messages.

## Full-tree repeat comparison

After stripping only the different top-level run-directory name, the two archives contain the same 524 relative file paths.

Within `ANIMO_testbank/` there are 499 files in each tree:

- 399 are raw byte-identical;
- 100 differ because they contain runtime metadata;
- all 499 become identical after normalizing only five explicit runtime metadata line families;
- no scientific values are normalized;
- no numerical tolerance is used.

The five normalized metadata families are:

1. `* ANIMO40-run started on:`
2. `File created on ...`
3. `ANIMO run start:`
4. `ANIMO run End:`
5. `Elapsed:`

The resulting normalized `ANIMO_testbank/` tree SHA-256 projection is identical in both runs:

`ee179425c21ced7a7773174b6f793a1e5adf464a8519dc889bad50926840c5cc`

Per-directory file counts and raw metadata-only differences are:

| Directory | Files | Raw equal | Metadata-only different | Equal after normalization |
|---|---:|---:|---:|---:|
| CranGrass | 45 | 38 | 7 | 45 |
| CranMais | 35 | 30 | 5 | 35 |
| GHGMais, unexecuted | 11 | 11 | 0 | 11 |
| GrassPeat | 73 | 59 | 14 | 73 |
| LWKM_gras_1040.2021.2045 | 67 | 59 | 8 | 67 |
| Puitmijn_Cranendonck_60 | 95 | 75 | 20 | 95 |
| RuurloGrass | 84 | 49 | 35 | 84 |
| STONE_akk_0006.2001.2015 | 59 | 51 | 8 | 59 |
| Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA | 29 | 26 | 3 | 29 |

The run-summary and `RUN_INFO.txt` capture records naturally differ in run number and clock timestamps and are not scientific model outputs.

## Baseline interpretation

This closes the repeat-determinism qualification for the current frozen-source Intel executable across the complete revision-53-compatible natural suite.

The project decision is therefore to use this executable as the **leading current executable qualification baseline** for revision-53 B1/native work. The separately received executable with SHA-256 `40e29853...` remains retained as a provenance-conflicting non-authoritative artifact because it was not built from the frozen source tree and differs materially on RuurloGrass.

This distinction is deliberate:

- `current_frozen_source_intel_baseline = qualified`
- `historical_B2_reference = not qualified`
- `historical_Intel_runtime_fidelity = not claimed`

## Consequences for TCD-015

The qualified frozen-source Intel baseline is now a defensible parent for an observer-only derivative build on the natural LWKM path. An observer derivative must first demonstrate ordinary-output non-interference against this exact uninstrumented baseline and may then expose the unrounded internal `Transsub` quantities needed for the scoped TCD-015 causal comparison.

No TCD-015 correction, clipping redesign, tolerance change, transport-physics change or historical admission is made by this qualification.