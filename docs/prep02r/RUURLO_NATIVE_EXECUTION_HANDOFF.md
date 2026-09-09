# ANIMO-PREP02R — Ruurlo Native Execution Handoff

Status: `READY_FOR_GENUINE_WINDOWS_EXECUTION_NOT_YET_RUN`.

## Purpose

The received `animo41.exe` is useful as a modern native Intel-family cross-runtime diagnostic, but it is not a historical B2 reference. This handoff makes the next executable step reproducible and fail-closed without copying the executable into the repository or treating a successful run as historical admission.

## Pinned artifacts

Executable:

`animo41.exe`

SHA-256:

`40e29853a0431cc7e2b787dfeb1870f44e1ff402b5aaebd6f56c8365fc5b178d`

Frozen testbank:

`ANIMO_testbank.zip`

SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Frozen Ruurlo case content-set SHA-256:

`0f12d19f74e6640b6d17f8f401ac9c294e35ae13064205ed4d1821d6a15c9ac9`

Frozen hydrology file:

`Input/SWATRE.UNF`

SHA-256:

`36d8dbeee7a46c769026c7441ea607160a715768571ba3e048b32ee2ace74d13`

Historical runner semantics:

```text
..\animo41.exe Animo.ini
```

Machine-readable input pin:

`integration/animo-prep/PREP02R_RUURLO_NATIVE_INPUT_PIN_20260909.json`

## Runtime dependency result

Static inspection of the received PE executable found only `KERNEL32.dll` and `imagehlp.dll` in its import table. No external Intel Fortran runtime DLL is imported. Intel Fortran RTL strings are embedded in the executable.

This materially lowers the practical Windows launch dependency, but it does not prove historical identity. The executable remains classified as:

`MODERN_NATIVE_REBUILD_NOT_HISTORICAL_REFERENCE`

See:

`integration/animo-prep/PREP02R_EXECUTABLE_RUNTIME_DEPENDENCY_REVIEW_20260909.json`

## Capture harness

Use:

`tools/prep02r_capture_ruurlo_native.ps1`

The harness:

1. checks the exact executable and testbank SHA-256 values before execution;
2. extracts a clean frozen RuurloGrass copy;
3. independently rechecks the complete case content-set and SWATRE bytes;
4. stages the executable only in a temporary run parent directory;
5. invokes the historical command relation without changing input content;
6. performs two clean runs;
7. captures exit status, stdout, stderr, runtime environment and every changed/new case file under SHA-256;
8. records raw repeat determinism without introducing a numerical tolerance;
9. removes the executable from the transferable capture bundle before packaging it.

The harness intentionally does not classify a matching native run as historical truth.

## Example command on Windows

From a directory containing the received `animo41.exe`, the frozen `ANIMO_testbank.zip`, and a checkout of this branch:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\prep02r_capture_ruurlo_native.ps1 `
  -ExecutablePath .\animo41.exe `
  -TestbankZip .\ANIMO_testbank.zip `
  -CaptureRoot .\PREP02R_Ruurlo_native_20260909
```

Use a new `CaptureRoot` path for each attempt.

Expected result files include:

- `PREP02R_RUURLO_NATIVE_CAPTURE.json`;
- `run1` raw case/output capture;
- `run2` raw case/output capture;
- stdout/stderr hashes and files;
- a transfer ZIP named after the capture root.

The transfer ZIP deliberately does not contain `animo41.exe`.

## After capture

The next PREP02R step is:

1. ingest the capture ZIP under hash control;
2. verify both runs and classify native repeat determinism;
3. compare the ordinary native output surface with the deterministic GNU diagnostic route;
4. classify every native-vs-GNU difference by output, variable, unit and likely runtime mechanism;
5. do not introduce a global tolerance;
6. keep the result as cross-runtime diagnostic evidence unless independent historical provenance is separately obtained.

A successful modern native run can strengthen compiler/runtime reconstruction. It cannot satisfy a `HISTORICAL_FIDELITY_CLAIM` and cannot by itself make normal B2 available under GOV02.

## Remaining independent acquisition gate

For a no-B2 Class-A route, GOV02 still requires documented B2 acquisition closure. The updated request draft is:

`docs/prep02r/WUR_ARCHIVAL_REQUEST_DRAFT.md`

It has been narrowed after receipt of the project files and 2026 executable. Sending remains a human external action.
