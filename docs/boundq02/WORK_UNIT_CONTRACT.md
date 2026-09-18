# ANIMO-BOUNDQ02 Static Boundary Year Cursor & Interval Binding Qualification

## Purpose

BOUNDQ02 qualifies the source-faithful year-selection semantics that bind the already-qualified BOUNDQ01 static BOUNDARY chemistry representation to an exact runtime interval and to the UBFORCE02 chemistry forcing type.

It does not parse BOUNDARY.INP and does not alter any chemistry values.

## Authorities

Program:
`ANIMO-RG06@8efdd151d89e1cff131d4b21e2acf559ca1828d6`

Static boundary chemistry adapter:
`ANIMO-BOUNDQ01@62b4fc36f2a47b67c08eedb095c60a5c059b77d8`

Upper-load chemistry resolver:
`ANIMO-UBFORCE02@931e32cec69dc78a03015f01190cff97bf1fe1b4`

Candidate exact calendar semantics:
`ANIMO-TIME02@b4d78cf32cb149cf50aa2b0a0fbefee571eee6b8`

The TIME02 calendar identity used here is:

`ANIMO_PG_86400_NOLEAPSECONDS_V1`

with `0001-01-01T00:00:00 -> day_index=0`.

## Frozen source identity

ANIMO 4.1.5 revision-53 archive:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Relevant source members:

- `Animo.for`: `352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7`
- `Init.for`: `287db00773ea21a155383b01a3ea35426c216117085822069e7bd844f71e0058`

## Exact revision-53 selection semantics

Revision-53 computes the year index in `Init` from the interval-origin expression:

`GDATE(Juda-St, Yr, ...)`

`Yn = Yr - Yrmi + 1`

The yearly precipitation chemistry and dry-deposition scalars are refreshed only when:

`Juda-St <= Judami OR (Month==1 AND Day==1)`

The source then assigns:

`Coprnhyn = Coprnh(Yn)`

`Coprniyn = Coprni(Yn)`

`Coprpoyn = Coprpo(Yn)`

`Drdepnhyn = Drdepnh(Yn)`

`Drdepniyn = Drdepni(Yn)`

BOUNDQ02 preserves this lifecycle rather than simplifying it to "select by civil year on every interval".

## Cursor contract

The candidate `boundary_year_cursor_t` stores only forcing-selection continuation:

- initialized/not initialized;
- active source year;
- active 1-based BOUNDARY year slot.

For the first interval, the slot is selected from the exact interval-origin civil year.

For later intervals, the slot changes only when the exact interval origin is 1 January. Otherwise the previous slot is retained.

This means that if a caller presents a later-year interval whose origin is not exactly 1 January while the accepted cursor still points to the previous year, BOUNDQ02 preserves the previous slot. This is deliberate source fidelity, not a correction.

The cursor is returned as a candidate `next_cursor`; the accepted cursor input is not mutated. A transaction layer can therefore publish it only together with an accepted interval.

## Exact calendar binding

BOUNDQ02 converts the TIME02 exact whole-day coordinate to a proleptic-Gregorian civil date under the pinned calendar contract.

The legacy compatibility envelope is years 1 through 3000.

Subday year selection is not qualified in this workunit.

## Interval frame

The `static_boundary_interval_frame_t` binds:

- exact origin time;
- exact endpoint time;
- boundary source identity;
- selected source year;
- selected slot;
- UBFORCE02 chemistry forcing;
- dry NH and NI deposition values as a separate family.

Dry deposition is never folded into the UBFORCE02 wet/advective chemistry forcing.

## Chemistry mapping

For the selected slot:

- yearly precipitation NH and NI are mapped to precipitation chemistry;
- yearly precipitation P is mapped only when phosphorus is enabled;
- static runon chemistry is copied exactly;
- static irrigation chemistry is copied exactly;
- static lateral/run-in chemistry is copied exactly.

No concentration transformation, interpolation or tolerance is introduced.

## Important year-boundary consequence

The source refresh condition is exact 1 January at the interval origin.

Therefore a timestep that skips across 1 January without a subsequent interval beginning exactly on 1 January would retain the previous chemistry cursor in revision-53.

BOUNDQ02 preserves that behavior explicitly.

Any future decision to instead select by civil year continuously is a model/runtime semantic change and requires separate disposition.

## Governance

BOUNDQ02 is runtime forcing-selection semantics feeding scientific composition. Conservative candidate risk is GOV04 Tier C.

Same-agent review is limited to `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Independent Tier C review remains required before canonical forcing-cursor admission.

## Hard boundaries

No BOUNDARY parser change.
No chemistry value correction.
No dynamic runon or irrigation.
No dry-deposition process execution.
No continuous "current civil year" replacement of the source cursor.
No canonical forcing-cursor state admission.
No checkpoint schema change.
No B3 mutation.
No TB7.
No B4.
No production.
