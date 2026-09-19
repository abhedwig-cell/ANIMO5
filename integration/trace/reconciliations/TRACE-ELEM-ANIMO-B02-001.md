# TRACE-ELEM-ANIMO-B02-001 reconciliation

Date closed: 2026-09-19
Prospective result: `CONFIRMED_AND_REPAIRED`
Confirmed case: `TRACE-ANIMO-0003`

## Element

TCD-017 organic-P ploughing redistribution reporting-ledger scientific admission, selected before detailed inspection as the Batch-02 process relation.

## Scientific identity

The admitted Class-A correction remains:

`Bapo(Redi,Ly) = Bapo(Redi,Ly) + Addiorpotoppl(I)*Z`

for the bounded reporting branch.

The corresponding physical top-reservoir and layer redistribution already closes before this reporting correction. The admitted change affects the reporting ledger, not physical state or process-flux trajectories.

Historical revision-53 behaviour remains `UNKNOWN` because no qualified B2 behavioural reference exists.

## Prospective discrepancy

The reviewer closeout was written while B3D02 validation was still pending and retained that conditional Result sentence after validation passed and the workunit was closed as qualified.

The machine status and admission record published the final admission correctly. The reviewer-facing closeout did not.

Commit chronology and validator reconstruction confirmed that this was not a deliberately frozen pre-validation evidence object.

## Existing-regression outcome

`REGRESSION_MISSED`.

The B3D02 validator read the affected reviewer document on the qualified tested head but checked only historical-uncertainty and boundary wording. It did not assert agreement between the Result section and the qualified machine status.

## Resolution

The reviewer closeout now states the successful validation and final qualified B3 scientific admission, while retaining the historical-uncertainty and no-production-migration boundaries.

The B3D02 validator now rejects stale conditional Result wording once the machine state is qualified. The current TRACE workflow invokes that validator for changes on this authority surface.

No scientific equation or production source changed.

Repair postimage `c6efa57032727ed15102561e8eeacc311c8bfff1` passed TRACE research integrity run `35429927284`.

This element remains in the denominator as a confirmed prospective discrepancy, not as a null observation.
