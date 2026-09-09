# ANIMO-NQ01 Representation Comparison Policy

Status: `FAIL_CLOSED_REPRESENTATION_COMPARISON_DEFINED_AWAITING_B2`.

## Purpose

B1-versus-B2 differences must be separated into representation differences and scientific trajectory differences. Treating every byte mismatch as physics is too strict, but treating every formatting or compiler difference as harmless is equally unsafe.

This policy covers four representation domains:

- `file_path_compatibility`;
- `formatting`;
- `binary_record_representation`;
- `precision_representation`.

The machine comparator is:

`tools/compare_b1_b2_representation.py`.

The predefined first-reference subject registry is:

`integration/animo-numerics/FIRST_REFERENCE_REPRESENTATION_SURFACE.json`.

It consumes `representation_observations` from the same structured B1 and B2 capture files used by the scientific comparator.

## Core rule

Representation differences are classified separately, but they are not automatically accepted.

The comparator performs no normalization. For each observation it aligns B2 and B1 by:

- representation domain;
- subject.

It then compares the declared classification and recorded representation text exactly.

A mismatch is reported as one of:

- `FILE_PATH_COMPATIBILITY_DIFFERENCE`;
- `FORMATTING_DIFFERENCE`;
- `BINARY_RECORD_REPRESENTATION_DIFFERENCE`;
- `PRECISION_REPRESENTATION_DIFFERENCE`.

Every such mismatch fails closed until a separate disposition establishes that it is representation-only and scientifically irrelevant.

An empty observation set is not an exact match. The comparator rejects empty B1 or B2 representation evidence as `SCHEMA_OR_PROVENANCE_FAILURE`. This prevents a vacuous match from entering the first-reference packet.

## Predefined subject selection

Representation subjects must not be selected after inspecting B2 differences.

The first-reference registry predefines subjects such as:

- working-directory and relative input-tree layout;
- path staging or drive mapping;
- filesystem case semantics;
- text encoding and line endings;
- floating exponent representation;
- declared volatile metadata surface;
- hydrology record-marker convention, byte order and payload real kind;
- internal default-real kind;
- explicit `REAL(4)` exchange boundary;
- floating-point compiler model;
- structured-capture serialization.

Not every subject is necessarily observable from a historical binary. A predefined subject may be omitted only when it is not jointly observable or not applicable, and that omission needs a recorded rationale. Omission is an evidence gap, not evidence of equivalence.

## Why normalization is not built into this comparator

Some normalization is already legitimate at the raw legacy-output-tree layer, for example declared volatile timestamps or CPU duration. That logic belongs in an explicit normalization contract such as the existing formatted-tree comparator.

The structured representation comparator deliberately does not inherit or guess those rules. Otherwise a new difference could become non-failing merely because it occurs in a familiar-looking metadata field.

A future normalization rule must therefore be:

1. explicitly named;
2. scoped to a specific representation subject;
3. shown not to alter scientific values, event timing or control flow;
4. recorded in the comparison packet.

## File and path compatibility

Examples include:

- historical relative path expectations;
- drive mappings;
- case sensitivity;
- legacy directory layouts.

Path differences may ultimately be representation-only when the exact frozen input bytes are unchanged. They are not automatically harmless because a path change can also change which file is opened.

The first-reference packet therefore still requires:

`input_content_transformed = false`.

## Formatting

Examples include:

- line endings;
- whitespace;
- exponent letter formatting;
- column width;
- explicitly volatile run metadata.

A formatting mismatch in a scientific number is not representation-only merely because the file is formatted text. Rounded decimal output can hide or create apparent equality. The unrounded scientific comparator remains authoritative for scientific values when observer capture exists.

## Binary-record representation

Examples include:

- record-marker width;
- byte order;
- unformatted sequential record conventions;
- scalar kind size;
- raw binary payload layout.

A binary representation difference may be a compatibility issue rather than a model difference, but any conversion must be explicit. Converted bytes are derived artifacts and are not B0.

## Precision representation

Examples include:

- `REAL(4)` exchange payload versus `REAL(8)` internal state;
- different compiler default-real policies;
- different round-trip serialization methods;
- known low-level floating representation differences.

A precision representation difference is not itself proof of a scientific trajectory difference. It is also not permission to introduce a tolerance. The scientific comparator must still compare unrounded state, transfer and ledger values under a qualified precision contract.

## Comparator decisions

Possible top-level decisions are:

- `MATCH_EXACT_REPRESENTATION_OBSERVATIONS`;
- `DIFFERENT_REPRESENTATION_FAIL_CLOSED`;
- `SCHEMA_OR_PROVENANCE_FAILURE`.

A successful representation comparison does not establish numerical equivalence. It only shows that the non-empty recorded representation observations match exactly.

## Relationship to the other NQ01 tools

The first B2 exercise uses three evidence layers:

1. `tools/compare_legacy_output_trees.py` for raw file-set, bytes and declared volatile normalization;
2. `tools/compare_b1_b2_representation.py` for structured representation-domain separation;
3. `tools/compare_b1_b2_reference.py` for scientific state, transfer, ledger and control-flow comparison.

The first-reference packet validator checks that the evidence chain is complete without converting any comparator result into automatic admission. When observer structured captures exist, the packet requires the representation layer to be run.

## Current boundary

No representation difference is currently pre-approved as a scientific numerical tolerance.

No solver or precision policy is changed by this work.

NQ01 remains:

`QUALIFIED_NUMERICAL_QUALIFICATION_ARCHITECTURE_AWAITING_INDEPENDENT_REFERENCE_DATA`.

Production migration remains:

`NOT_ADMITTED`.
