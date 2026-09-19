# TRACE Exposure Batch 02

Date selected: 2026-09-19
Model: ANIMO
Selection ref: `138eb8848f5341c5a7bd1c1a153e2d36e3b9bd17`
Status: `SELECTED_BEFORE_DETAILED_INSPECTION`

## Purpose

Extend the prospective denominator after Batch 01 without selecting targets because of suspected discrepancies.

## Selection rule

Reuse the three Batch-01 strata and advance to different named scientific surfaces using directory/file names only.

1. **Process/transport relation:** in `docs/b3`, advance from the Batch-01 TCD015 subject to the next lexicographic top-level TCD subject, TCD017.
2. **Transfer/partition relation:** in `docs/ghg`, advance from TCD032 to the next lexicographic TCD subject, TCD033.
3. **Numerical-scientific convention:** in `docs/numerics`, use the remaining named TCD numerical policy after the already exposed precision baseline, TCD019.

No detailed content of these three selected documents was read to decide selection.

## Selected elements

| Element ID | Stratum | Surface used to identify element |
|---|---|---|
| TRACE-ELEM-ANIMO-B02-001 | process/transport relation | `docs/b3/TCD017_B3_ADMISSION_CLOSEOUT.md` |
| TRACE-ELEM-ANIMO-B02-002 | transfer/partition relation | `docs/ghg/TCD033_CH4_COMPONENT_PARTITION_QUALIFICATION.md` |
| TRACE-ELEM-ANIMO-B02-003 | numerical-scientific convention | `docs/numerics/TCD019_RESTRICTED_NO_FALLBACK_NUMERICAL_POLICY.md` |

## Handling

The v0.2 protocol and codebook remain unchanged.

For each element:

- reconstruct theory/documentation/implementation/evidence authority;
- stop and register a candidate at the first previously unknown substantive conflict;
- freeze pre-resolution evidence before adjudication;
- retain excluded candidates as observed candidate triggers;
- close null elements explicitly in the denominator.

Historical pre-freeze discrepancies encountered inside a selected subject remain historical and cannot be promoted into Batch-02 confirmatory results.
