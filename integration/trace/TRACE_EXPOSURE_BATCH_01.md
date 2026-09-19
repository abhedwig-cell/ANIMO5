# TRACE Exposure Batch 01

Date selected: 2026-09-19
Model: ANIMO
Selection ref: `f9a933cec8feee223e78e006f8305767d244452c`
Status: `SELECTED_BEFORE_DETAILED_INSPECTION`

## Purpose

Create the first prospective denominator exposure without selecting components because they are suspected to contain discrepancies.

## Selection rule

Batch 01 uses three scientific-representation strata:

1. process/transport relation;
2. process transfer/ownership relation;
3. numerical-scientific convention.

Within the current documented surfaces, the first subject identifier or baseline surface in the relevant stratum was selected from directory/file names before detailed reading: TCD015 in B3, TCD032 in GHG, and the precision-policy baseline in numerics.

Known TRACE historical-pilot discrepancies are not eligible for confirmatory counting even if they overlap a selected subsystem.

## Selected elements

| Element ID | Stratum | Surface used to identify element |
|---|---|---|
| TRACE-ELEM-ANIMO-B01-001 | process/transport relation | `docs/b3/TCD015_B3_ADMISSION_CLOSEOUT.md` |
| TRACE-ELEM-ANIMO-B01-002 | transfer/ownership relation | `docs/ghg/TCD032_METHANOGENESIS_C_TRANSFER_OWNERSHIP_QUALIFICATION.md` |
| TRACE-ELEM-ANIMO-B01-003 | numerical-scientific convention | `docs/numerics/PRECISION_POLICY_BASELINE.md` |

## Prospective handling

For each element, reconciliation follows theory/documentation -> implementation trace -> pre-existing executable/regression evidence. If a previously unknown possible discrepancy is encountered, inspection stops at the point needed to state the conflict, a TRACE candidate is registered and pre-resolution evidence is frozen before resolution work continues.

An element with no confirmed discrepancy remains part of the denominator and is closed with `no_discrepancy_observed=true`.

This batch is not a random sample of ANIMO science. It is a planned, stratified exposure batch intended to make the inspection process observable and prevent result-driven component selection.
