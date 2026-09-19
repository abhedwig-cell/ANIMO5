# TRACE Exposure Batch 03

Date selected: 2026-09-19
Model: ANIMO
Selection ref: `d4eed5257379de6d5fa4767aeda3868ee765ef18`
Status: `SELECTED_BEFORE_DETAILED_INSPECTION`

## Purpose

Batch 03 expands the prospective ANIMO denominator after the first two mixed-stratum batches.

## Selection rule

The dedicated `docs/numerics` and `docs/ghg` reviewer surfaces used in the first two batches contain no third unexposed peer file under the same simple progression rule. Batch 03 therefore uses a deterministic B3 admission-surface expansion rather than selecting a new subject because it appears suspicious.

Selection used file names and prior exposure membership only:

1. consider `docs/b3/*_B3_ADMISSION_CLOSEOUT.md`;
2. exclude TCD-015 and TCD-017 because they were exposed in Batches 01 and 02;
3. ignore the companion `*_GOV03_FORMAL_DISPOSITION.md` files for selection because they belong to the same TCD authority chain;
4. sort the remaining admission-closeout names lexicographically;
5. select the first three.

This yields:

1. TCD-018;
2. TCD-024;
3. TCD-026.

No selected closeout was read before this selection was persisted.

## Selected elements

| Element ID | Representation stratum | Identification surface |
|---|---|---|
| TRACE-ELEM-ANIMO-B03-001 | scientific relation / admission chain | `docs/b3/TCD018_B3_ADMISSION_CLOSEOUT.md` |
| TRACE-ELEM-ANIMO-B03-002 | scientific relation / admission chain | `docs/b3/TCD024_B3_ADMISSION_CLOSEOUT.md` |
| TRACE-ELEM-ANIMO-B03-003 | scientific relation / admission chain | `docs/b3/TCD026_B3_ADMISSION_CLOSEOUT.md` |

## Handling

TRACE protocol/codebook v0.2 remains frozen.

For each element:

- reconstruct scientific meaning and the documentation/code/evidence/admission chain;
- stop at the first previously unknown substantive conflict and freeze it before resolution;
- distinguish immutable historical/pre-review provenance from current competing authority;
- preserve exclusions and null observations in the denominator;
- do not count pre-freeze known TCD history as a new prospective discrepancy.

Batch 03 is a planned coverage-expansion batch, not a random prevalence sample.
