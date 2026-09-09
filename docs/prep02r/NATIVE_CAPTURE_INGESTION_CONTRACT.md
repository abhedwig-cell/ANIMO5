# ANIMO-PREP02R — Native Capture Ingestion Contract

Status: `READY_FOR_GENUINE_WINDOWS_CAPTURE_AND_FAIL_CLOSED_INGESTION_NOT_YET_RUN`.

## Purpose

This contract closes the tooling gap between a genuine Windows execution of the received 2026 `animo41.exe` and later PREP02R evidence review.

The received executable remains:

`MODERN_NATIVE_REBUILD_NOT_HISTORICAL_REFERENCE`

Nothing in this capture or ingestion route may relabel it as historical B2 evidence.

## Raw harness contract

Windows capture tool:

`tools/prep02r_capture_ruurlo_native.ps1`

Raw harness schema:

`animo-prep02r-ruurlo-native-harness-capture-v1`

This schema is deliberately distinct from the more general:

`animo-prep02r-native-run-capture-v2`

in `PREP02R_NATIVE_RUN_MANIFEST_TEMPLATE.json`. The Windows harness output is a raw two-run transfer artifact. It must first be validated before any reviewed native-run record is constructed.

The harness pins:

- received executable SHA-256 `40e29853a0431cc7e2b787dfeb1870f44e1ff402b5aaebd6f56c8365fc5b178d`;
- frozen testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- frozen Ruurlo case content-set SHA-256 `0f12d19f74e6640b6d17f8f401ac9c294e35ae13064205ed4d1821d6a15c9ac9`;
- frozen `Input/SWATRE.UNF` SHA-256 `36d8dbeee7a46c769026c7441ea607160a715768571ba3e048b32ee2ace74d13`.

It uses a host-independent UTF-8 byte-order path sort for content-set hashing, so Windows culture or case ordering cannot silently alter the pinned case identity.

For each of two clean executions it records:

- pre-run file count and content-set identity;
- post-run file count and content-set identity;
- every changed or newly created file with size and SHA-256;
- every deleted pre-existing file with its original size and SHA-256;
- stdout and stderr size and SHA-256;
- exit status and timing metadata;
- explicit `input_content_transformed=false`.

`Start-Process` is used with direct stdout/stderr redirection rather than PowerShell pipeline redirection, avoiding PowerShell text re-encoding of the process streams.

The staged executable is removed before transfer packaging. The temporary full testbank extraction is also removed. The transfer ZIP therefore contains capture evidence, not redistributed executable bytes or an unnecessary full extracted testbank. A SHA-256 sidecar for the transfer ZIP is emitted after packaging.

## Ingestion validator

Validator:

`tools/prep02r_validate_native_capture.py`

The validator accepts either the transfer ZIP or an extracted capture directory. It fails closed on:

- wrong harness schema or evidence class;
- wrong executable, testbank, Ruurlo or hydrology identity;
- executable bytes present in the transfer bundle;
- temporary frozen-testbank extraction still present;
- missing run directories or process streams;
- mismatch between captured files and manifest hashes/sizes;
- unreported changed/new files;
- unreported deleted files;
- false raw-repeat declarations;
- any capture record that claims historical-reference, normal-B2 or production admission.

The validator recomputes the post-run delta against:

`integration/animo-prep/PREP02R_RUURLO_NATIVE_INPUT_PIN_20260909.json`

It then uses the existing fail-closed legacy output comparator to classify repeat execution as one of:

- `NATIVE_REPEAT_EXACT_RAW`;
- `NATIVE_REPEAT_DECLARED_VOLATILE_ONLY`;
- `NATIVE_REPEAT_DIFFERENT_FAIL_CLOSED`.

Only the already-declared volatile metadata rules may be normalized. No scientific numeric tolerance is applied.

## Validator test evidence

A six-test repository test suite is present at:

`tests/test_prep02r_validate_native_capture.py`

A local Linux mirror of the validator plus the existing comparator contract was executed after the final integrity hardening. Result:

`6 / 6 PASS`

Covered cases:

1. exact repeated capture;
2. declared volatile-only repeat difference;
3. unlisted changed output;
4. declared file deletion and recomputation;
5. executable bytes improperly included in transfer;
6. false `NATIVE_REPEAT_EXACT_RAW` manifest declaration.

The PowerShell harness itself has not been executed in this controlled environment because no genuine Windows/PowerShell runtime is available here. That remains an explicit execution boundary, not a hidden qualification claim.

## Post-capture workflow

After a genuine Windows capture is returned:

1. verify the transfer ZIP SHA-256 against its sidecar or independently recorded upload hash;
2. run `prep02r_validate_native_capture.py` and persist its JSON report;
3. require capture-integrity PASS;
4. require repeat classification to be exact or declared-volatile-only before using one run as a cross-runtime diagnostic candidate;
5. compare the validated ordinary native output surface against the deterministic GNU Ruurlo diagnostic surface;
6. classify every native-vs-GNU difference by output, variable, unit and likely compiler/runtime mechanism;
7. define no global tolerance;
8. retain the result as cross-runtime diagnostic evidence only.

Even perfect native/GNU agreement does not satisfy a `HISTORICAL_FIDELITY_CLAIM`, does not create normal B2, and does not close the independent historical acquisition gate.
