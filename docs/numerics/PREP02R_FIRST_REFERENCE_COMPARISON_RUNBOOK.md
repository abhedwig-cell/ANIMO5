# ANIMO-NQ01 / PREP02R First Reference Comparison Runbook

Status: `READY_AWAITING_PROVENANCE_QUALIFIED_B2_ARTIFACT`.

## Purpose

This runbook turns the NQ01 comparison architecture into an executable sequence for the first independent historical comparison.

It does not establish B2, define a tolerance, qualify numerical equivalence, admit a numerical correction or authorize production migration.

The preferred first case remains `RuurloGrass` unless PREP02R changes that decision with stronger live evidence.

## Frozen identities

Use the exact frozen evidence identities already established by ANIMO5 governance:

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank archive SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- B1 GNU diagnostic executable SHA-256: `0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`.

Recheck these against the live PREP02R and governance records before a real comparison. This runbook must not override a later provenance correction.

## Gate 0: B2 receipt and lineage

Do not execute the native artifact until PREP02R has recorded:

- artifact filename and SHA-256;
- receipt manifest;
- acquisition source;
- claimed version and revision;
- exact, nearby or distinct-lineage classification;
- retained original bytes;
- controlled storage location outside any public redistribution path where required;
- explicit decision that a native qualification attempt is permitted.

A downloaded or received executable is not B2 merely because it runs.

## Gate 1: frozen testcase staging

Prepare a clean `RuurloGrass` working tree from the frozen testbank bytes.

Record separately:

- input-tree manifest;
- hydrology-file identity;
- command line;
- working-directory structure;
- filesystem or drive mapping;
- locale, code page and timezone if relevant;
- runtime libraries and environment identity.

Path-only compatibility staging is allowed when it leaves input content unchanged. Record `input_content_transformed = false`.

Any input-content edit creates a distinct derived artifact and blocks the preferred frozen comparison path until explicitly qualified.

## Gate 2: ordinary native run

Run the uninstrumented native artifact first.

Preserve before normalization:

- stdout bytes and SHA-256;
- stderr bytes and SHA-256;
- process exit status;
- complete output tree;
- byte size and SHA-256 of each file;
- created, missing and unexpectedly retained files;
- warnings and STOP messages;
- runtime duration as non-scientific diagnostic metadata.

Do not parse and discard the raw outputs. Derived comparison files are secondary evidence.

## Gate 3: repeat determinism

When practical, repeat the same ordinary native run from a fresh frozen input tree.

Classify only as:

- `NATIVE_REPEAT_EXACT`;
- `NATIVE_REPEAT_DECLARED_VOLATILE_ONLY`;
- `NATIVE_REPEAT_DIFFERENT_FAIL_CLOSED`.

Do not invent a tolerance for native repeat differences.

## Gate 4: corresponding B1 run

Run the pinned B1 GNU diagnostic route on the same frozen testcase identity.

Record:

- executable SHA-256;
- compiler/runtime contract;
- compatibility transformations;
- command line and environment;
- input-tree manifest;
- raw output-tree manifest.

B1 remains `DIAGNOSTIC_NOT_REFERENCE` even if every compared value agrees with B2.

## Gate 5: raw and formatted-tree comparison

Before any structured unrounded comparison:

1. compare file sets and path semantics;
2. compare raw hashes where exact identity is meaningful;
3. run `tools/compare_legacy_output_trees.py`;
4. retain both raw and declared-volatile-normalized results;
5. classify every remaining difference as file/path, formatting, binary-record, precision or potentially scientific.

A report-level match does not prove unrounded scientific equivalence.

A report-level mismatch is not automatically harmless formatting. Numeric report differences remain fail-closed until classified.

## Gate 6: observer eligibility

Observer instrumentation is permitted only after an ordinary provenance-qualified native contract exists.

For an observer build:

- derive it from the same qualified native source/build lineage where possible;
- record observer patch identity;
- write observer values to a separate evidence stream;
- do not feed observer values back into the scientific calculation;
- do not change evaluation order, solver logic, precision policy, convergence, clipping or inputs;
- compare all ordinary outputs against the uninstrumented native run.

Observer output is trusted only when ordinary output remains exact or differs solely in explicitly declared volatile metadata.

Otherwise classify the instrumentation as perturbing behaviour and stop.

## Gate 7: structured capture

Use:

`integration/animo-numerics/REFERENCE_CAPTURE_SCHEMA.json`

Required schema version:

`1.1.0`

For every floating scientific record:

- record storage kind and bit width where known;
- serialize exact IEEE bits or a proven round-trip decimal representation;
- set `capture_is_round_trip = true` only when this has actually been established;
- retain the raw observer stream and its SHA-256.

A capture with `rounded_report_only = true` may contain report evidence but cannot serve as an unrounded floating scientific oracle.

Minimum comparison checkpoints, where relevant to the quantity, are:

- `INITIAL_STATE`;
- `PRE_PROCESS_STATE`;
- `POST_PROCESS_STATE`;
- `ACCEPTED_END_OF_STEP_STATE`;
- `CUMULATIVE_PERIOD_BALANCE`;
- `FINAL_STATE`.

`TRIAL_STATE` is additional diagnostic evidence and must never be confused with accepted physical state.

## Gate 8: comparison-surface selection

Do not invent source variable names simply to populate the schema.

Select comparison records only when their scientific meaning is established from source-bound inventories, PREP06 state/transfer-ledger work, process ownership evidence, documentation or explicit observer mapping.

For each selected quantity declare:

- comparison variable class;
- semantic state, transfer or ledger identity;
- units;
- layer, compartment, species and site/fraction applicability;
- source routine and call context;
- temporal checkpoints;
- whether branch and fallback path are relevant;
- whether cumulative/reset semantics apply.

For `EXACT_ACCOUNTING_IDENTITY`, additionally declare:

- `ledger_member_id`;
- `ledger_sign`;
- `index_mapping_id` when applicable.

A matching numeric value does not excuse a different ledger member, sign or index mapping.

## Gate 9: structured B2 versus B1 comparison

Run:

`tools/compare_b1_b2_reference.py <b2-capture.json> <b1-capture.json> --json <comparison.json>`

The comparator is fail-closed and contains no numerical tolerance.

Expected categories include:

- exact match;
- declared non-scientific representation-only difference;
- formatted-report difference requiring classification;
- unqualified numerical difference;
- control-flow difference;
- accounting-identity difference;
- precision-representation difference;
- unit mismatch;
- missing or unexpected record;
- schema or provenance failure.

A difference in captured `branch_id` or `fallback_id` fails even when the resulting value matches.

## Gate 10: first-comparison disposition

Retain the comparison as evidence. Do not convert it directly into an admission decision.

Possible immediate outcomes are:

- exact or representation-only comparison evidence with a qualified B2 reference;
- exact match to a B2 candidate whose provenance still remains unqualified;
- one or more unqualified numerical differences requiring cause analysis;
- control-flow divergence requiring historical and numerical interpretation;
- insufficient unrounded capture;
- failed observer non-interference;
- provenance or testcase mismatch.

No outcome from the comparator alone establishes B3.

## Numerical-difference rule

For every non-exact floating scientific difference record:

- exact B2 value;
- exact B1 value;
- units;
- absolute difference;
- relative difference as diagnostic magnitude only;
- affected state/flux/ledger trajectory;
- first temporal divergence where observable;
- associated branch/fallback differences;
- precision representation;
- whether the difference is present in ordinary formatted output;
- whether further observer capture is needed.

Do not accept or reject it by magnitude alone.

## Tolerance rule

There is no NQ01 numerical tolerance.

Do not:

- use the maximum B1 to B2 mismatch;
- use the maximum historical balance residual;
- use report print precision;
- use an arbitrary relative percentage;
- tune a threshold until the comparison passes.

Any future tolerance must come from a separate process-specific numerical qualification with an explicit evidence basis.

## Completion record for the first exercise

The first comparison packet should contain at minimum:

- PREP02R B2 receipt/provenance manifest;
- frozen testcase/input manifest;
- native ordinary run manifest;
- native repeat result if performed;
- B1 run manifest;
- both raw output-tree manifests;
- formatted-tree comparator result;
- observer non-interference evidence if observer capture is used;
- B2 structured capture;
- B1 structured capture;
- structured comparison result;
- difference classification record;
- explicit statement of whether B2 itself is candidate or qualified;
- explicit statement that numerical equivalence remains unqualified unless separately admitted.

## Current exit state

Until PREP02R obtains independent reference data:

`QUALIFIED_NUMERICAL_QUALIFICATION_ARCHITECTURE_AWAITING_INDEPENDENT_REFERENCE_DATA`

Numerical equivalence:

`NOT_QUALIFIED_NO_INDEPENDENT_B2_DATA`

Production migration:

`NOT_ADMITTED`
