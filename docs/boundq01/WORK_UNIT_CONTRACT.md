# ANIMO-BOUNDQ01 Static BOUNDARY Chemistry Adapter Qualification

## Purpose

BOUNDQ01 qualifies a bounded nonproduction revision-53 BOUNDARY.INP adapter for the chemistry coordinates needed by the TCD-042 upper-boundary forcing lane.

It does not migrate the complete BOUNDARY family.

## Authorities

Program:
`ANIMO-RG06@8efdd151d89e1cff131d4b21e2acf559ca1828d6`

Input audit:
`ANIMO-IO01@2bcf65360b08d278f28f1cc61ac96714db4793a3`

General grammar work remains separately represented by IO02 and is not widened here.

Chemistry forcing contract and resolver:

- `ANIMO-UBFORCE01@9f9204ba53169285ac84272704de14836962ef41`
- `ANIMO-UBFORCE02@931e32cec69dc78a03015f01190cff97bf1fe1b4`

Architecture:
`ANIMO-ARCH05@99b6098a19db405ce34928af89bb78b856dce7cd`

## Frozen source grammar

Revision-53 `input1.for` SHA-256:

`041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95`

The bounded adapter preserves the relevant legacy mechanics:

- labels are resolved by exact first-eight-character match;
- the first matching label wins;
- list-directed record conversion is performed by Fortran itself;
- `Ioptidti` and `Ioptirti` are read from `>optibc:`;
- only `Ioptidti=0 AND Ioptirti=0` is accepted;
- yearly precipitation concentrations and dry N deposition are read from `>topbou:`;
- static runon and irrigation chemistry are read from their sequential positions in `>topbou:`;
- lateral/run-in chemistry is read from `>latbou:`;
- P fields are present only when external configuration says `Ipo=1`.

## Source range contracts

The adapter preserves revision-53 Checkrea ranges for this bounded route.

Precipitation chemistry:
- NH4-like and NO3-like channels: 0..1
- PO4-like channel when active: 0..1

Dry deposition:
- N channels: 0..100

Static runon:
- mineral N and P concentrations: 0..999
- DOM/DON/DOP concentration channels: 0..10

Static irrigation:
- mineral N and P concentrations: 0..999
- DOM/DON/DOP concentration channels: 0..10

Lateral/run-in:
- mineral N and P concentrations: 0..1
- DOM: 0..10
- DON: 0..1
- DOP: 0..0.1

No range is relaxed to accommodate tests.

## Normalized representation

The adapter exposes:

- yearly precipitation NH/NI and optional P chemistry;
- yearly dry-deposition NH/NI values;
- static runon chemistry;
- static irrigation chemistry;
- static lateral/run-in chemistry.

Dry deposition is retained as a separate normalized family and is not passed implicitly into UBFORCE01/02.

The adapter does not select the active yearly precipitation slot. Calendar/year selection remains a separate TIME/configuration responsibility.

## Natural testbank evidence

The user-supplied frozen testbank SHA-256 is:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Nine BOUNDARY.INP cases were scanned. All nine use:

`Ioptidti=0 AND Ioptirti=0`.

Both `Ipo=0` and `Ipo=1` cases are present.

This is natural grammar/option evidence only, not historical B2 behavior.

## Exclusions

No `>runoti:` parser.
No `>irriti:` parser.
No bottom-boundary chemistry.
No dry-deposition process execution.
No active-year selection.
No GENERAL parser.
No hydrology calculation.
No TCD-042 re-admission.
No production migration.

## Risk

The work is representation and forcing-interface code, but it feeds scientific execution. Conservative candidate risk is GOV04 Tier C because parser/order/runtime representation mistakes could change model behavior. Any later composition with TCD-042 remains Tier D.
