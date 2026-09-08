# Compiler and legacy Fortran interface audit baseline

Status: `NOT_ASSESSED_SOURCE_UNAVAILABLE`.

The requested interface audit is defined here as an explicit work area, but no code-level result is claimed without source.

| Audit item | PREP01 status | Classification |
| --- | --- | --- |
| implicit interfaces | NOT_ASSESSED | NOT_ASSESSED |
| type mismatches | NOT_ASSESSED | NOT_ASSESSED |
| kind mismatches | NOT_ASSESSED | NOT_ASSESSED |
| scalar/array mismatches | NOT_ASSESSED | NOT_ASSESSED |
| shape inconsistencies | NOT_ASSESSED | NOT_ASSESSED |
| missing/incorrect intents | NOT_ASSESSED | NOT_ASSESSED |
| unused arguments | NOT_ASSESSED | NOT_ASSESSED |
| propagation-only arguments | NOT_ASSESSED | NOT_ASSESSED |
| inconsistent call sites | NOT_ASSESSED | NOT_ASSESSED |
| aliasing | NOT_ASSESSED | NOT_ASSESSED |
| missing initialization | NOT_ASSESSED | NOT_ASSESSED |
| unclear argument semantics | NOT_ASSESSED | DOCUMENTATION_GAP |
| unclear argument units | NOT_ASSESSED | DOCUMENTATION_GAP |
| hidden side effects | NOT_ASSESSED | NOT_ASSESSED |
| global/common/module mutable state | NOT_ASSESSED | NOT_ASSESSED |
| STOP/WRITE/READ/OPEN/CLOSE in compute logic | NOT_ASSESSED | NOT_ASSESSED |

Permitted classifications for later source audit:

`CONFIRMED_DEFECT`, `SUSPICIOUS_LEGACY_CONSTRUCT`, `REDUNDANT_INTERFACE`, `DOCUMENTATION_GAP`, `NOT_ASSESSED`.

A modern compiler may be used as a diagnostic instrument after source ingest. Compiler warnings alone will not be treated as proof of scientific defects.
