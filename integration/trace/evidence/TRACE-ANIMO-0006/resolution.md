# TRACE-ANIMO-0006 resolution

Date: 2026-09-19
Outcome: `CONFIRMED_AND_CLOSED`
Disposition: `DOCUMENTATION_CORRECTED`
Regression counterfactual: `REGRESSION_MISSED`

## Confirmed discrepancy

The reviewer-facing TCD-026 admission closeout still said:

- admission was “subject to this workunit's fail-closed validation”;
- “if validation is green” TCD-026 would become admitted.

At the same current authority state, B3D08 machine status recorded:

- `tested=true`;
- `qualified=true`;
- `work_unit_complete=true`;
- `scientific_b3_admission_qualified=true`.

The machine closeout already recorded the bounded scientific B3 admission as true.

## Post-freeze chronology

The prospective candidate was frozen before reading the B3D08 validator or branch chronology.

After freeze, reconstruction showed:

- tested B3D08 head `37cad3a863eadff7d6e8c1905fb87aebb5784f7d` passed run `34447821815`;
- final B3D08 head `cc280b630d6dc0d6bc1b8b0783ccfa4f91e15624` changed only the status closeout;
- the final head passed the same workflow in run `34447874356`;
- the reviewer document remained byte-identical at the final head;
- no immutable authoring-freeze contract assigned the conditional prose a permanent provenance role.

## Why the pre-existing regression missed it

The B3D08 validator correctly checked:

- TCD identity and class;
- route and review authority;
- historical uncertainty;
- bounded admission decision;
- hard nonclaims;
- machine qualified/tested state;
- required reviewer tokens.

But it did not reject conditional reviewer phrases after the machine state became qualified.

Therefore the exact final B3D08 workflow was green while the reviewer closeout still communicated a pending admission state.

The regression counterfactual is `REGRESSION_MISSED`.

## Scientific consequence

The demonstrated consequence is interpretative.

The TCD-026 scientific identity itself was consistent:

`Bfom(Inip_x,Ly) = Bfom(Inip_x,Ly) + Ex(Ln) * P`

as an `A_ACCOUNTING_REPORTING_ONLY` correction, with historical behaviour `UNKNOWN`, no whole-model formatted-restart identity claim and no production authorization.

No physical state, process flux, initialization physics, restart state, forcing or numerical policy discrepancy was demonstrated.

## Repair

A clean owner-line repair changed only:

- `docs/b3/TCD026_B3_ADMISSION_CLOSEOUT.md`;
- `tools/validate_b3d08_tcd026_admission.py`.

The reviewer closeout now states that fail-closed validation succeeded and the bounded scientific admission is complete.

The validator now fails if a qualified B3D08 status coexists with either stale conditional phrase.

Owner-line repair head:

`a27e13e6edadb35e11478e5ca914d8421dd181f7`

The original `ANIMO-B3D08 TCD026 admission closeout` workflow and scope guard passed on that exact head in run `35439411812`.

## TRACE significance

ANIMO-0006 independently reproduces the mechanism first seen in ANIMO-0003: reviewer-facing admission prose can remain conditional after machine qualification unless the validator checks cross-representation status consistency.

That repeated mechanism is evidence for a recurring governance failure mode within the observed sample, not a repository-wide prevalence estimate.
