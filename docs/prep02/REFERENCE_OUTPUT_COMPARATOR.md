# PREP02 fail-closed legacy output comparator

Status: `IMPLEMENTED_TESTED_QUALIFICATION_TOOLING_NOT_REFERENCE_ADMISSION`.

## Purpose

PREP02 needs a comparison layer that can accept trusted native legacy output later without quietly turning formatting noise or numerical differences into a global tolerance.

`tools/compare_legacy_output_trees.py` provides that layer.

The tool does not decide whether an executable is a scientific reference. It only compares two output trees and emits machine-readable evidence.

## Comparison policy

The comparator is fail-closed.

It distinguishes:

- `EQUAL_RAW`;
- `EQUAL_DECLARED_VOLATILE_NORMALIZATION_ONLY`;
- `DIFFERENT`.

A tree comparison returns `DIFFERENT_FAIL_CLOSED` when:

- a reference file is missing;
- a candidate file is missing;
- an unexpected candidate file is present when comparing whole trees;
- any common file differs after the declared volatile normalization.

No numerical tolerance is used to convert a scientific difference into a pass.

For differing text files the tool may report numerical token counts and maximum absolute or relative difference as diagnostics. Those values are explicitly non-admission evidence.

## Declared volatile normalization

Normalization is restricted to exact legacy metadata-line shapes already identified during PREP01 reproducibility work:

- file creation timestamp;
- `ANIMO40-run started on` timestamp;
- message run-start timestamp;
- message run-end timestamp;
- elapsed CPU seconds.

The regular expressions are anchored to complete metadata lines. Dates and numbers elsewhere in scientific output are not normalized.

`--raw-only` disables even this metadata normalization.

## File-scope control

By default the tool compares complete directory trees.

For historical-reference qualification a caller may instead provide an explicit `--file-list`. That permits the run harness to compare exactly the generated output contract without accidentally treating copied inputs or execution-environment helper files as scientific output.

`--exclude` is available for explicit path-pattern exclusions. Exclusion choices must be persisted by the calling qualification workunit. They are not hidden inside this tool.

## Validation

Unit coverage is persisted in `tests/test_compare_legacy_output_trees.py` for:

1. declared timestamp-only difference passes only after declared normalization;
2. a scientific numerical change from `1.25` to `1.26` fails closed and is reported numerically;
3. an unexpected candidate file fails closed;
4. raw-only mode does not normalize a run timestamp.

The comparator core was also exercised against existing PREP02 diagnostic LWKM outputs for the top-term and stable-ledger variants. These natural-case runs differ only in volatile metadata because the stable-DOP ledger term is dormant in the supplied testcase. The observed comparison was:

- common files: 69;
- raw equal: 61;
- equal after declared volatile normalization: 8;
- different after normalization: 0;
- decision: `MATCH_AFTER_DECLARED_VOLATILE_NORMALIZATION`.

That real-case check is a tooling validation only. Neither side is promoted to a historical reference.

## Intended PREP02 use

When a trusted historical Intel/native run becomes available, the qualification harness should persist:

- exact executable identity and toolchain provenance;
- exact testcase input identity;
- explicit generated-output file list;
- raw output hashes;
- comparator report;
- any separate numerical-parity analysis required beyond formatted output.

A formatted-output match is necessary evidence for supported surfaces, not sufficient evidence for scientific reference qualification by itself.

## Gate

`REFERENCE_OUTPUT_COMPARATOR_READY_NATIVE_REFERENCE_STILL_REQUIRED`
