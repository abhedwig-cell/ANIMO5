# ANIMO-KT13 Work Unit Contract

Workunit: `ANIMO-KT13 - Bounded Selected-Packet TCD-042 End-to-End Nonproduction Composition Qualification`.

Execution discipline: `RECONCILE -> COMPOSE -> QUALIFY -> REVIEW -> HANDOFF`.

## Purpose

KT13 composes the already-qualified bounded pieces into one real nonproduction interval execution:

`selected hydrology packet -> KT06 binding -> KT05 projection -> HYDROEXEC01 -> HYDROQ01/HYDROQ02 -> UBFORCE02 -> UBFORCE01 load channel -> KT12 TCD-042 -> KT02 atomic commit`.

This is the first workunit that proves the bounded revision-53 upper-boundary hydrology, chemistry-bearing load resolver and admitted TCD-042 algebra can execute as one transaction.

## Exact authorities consumed

Program:

`ANIMO-RG06@8efdd151d89e1cff131d4b21e2acf559ca1828d6`

Runtime binding:

`ANIMO-KT06-A1@56384db4107aed484218363e26dbb7be7f51e8de`

TCD-042 parent science:

`ANIMO-B3D35@9ca23f41dc3c28af686b1bc0bff8e7d66416d367`

TCD-042 transaction client:

`ANIMO-KT12@8f0e8e4bfd0b391b781f7c69b7d2063d5cf8705e`

Resolved upper hydrology carrier:

`ANIMO-HYDROQ01@5301d90024c64057f2cb88fda1dbaa93aabfca47`

Resolved runoff/load context:

`ANIMO-HYDROQ02@08d5b8301c217cf9d33d2bf248be133f2b5243fc`

Bounded hydrology execution:

`ANIMO-HYDROEXEC01@182dac2fc34ca42ed798203e90efeca1221f21e8`

Upper solute-load carrier:

`ANIMO-UBFORCE01@9f9204ba53169285ac84272704de14836962ef41`

Upper solute-load resolver:

`ANIMO-UBFORCE02@931e32cec69dc78a03015f01190cff97bf1fe1b4`

Runinu continuation classification:

`ANIMO-STATEQ08@e9ee7fc9e69a62c58b6eacd6379220cc51c1bf07`

## Frozen implementation identities

KT13 composes exact frozen implementation blobs:

- KT06 binding: `9a24ea833291f761d2fa76ca4cc9fee28436c614`
- KT12 TCD-042 client: `e9ef255f9905e5b4fe3d8761f2ecd7105a6451ad`
- HYDROQ01: `081e6b45e777ebccb852b3d1adde05ed6baaeb6a`
- HYDROQ02: `786dce177c50c91149dad33289306f935b61b354`
- HYDROEXEC01: `b4b621d1957291b7cf26931fe065d2cbcb89e71c`
- UBFORCE01: `fbe12e01df715ed7c95c59f5dd6b1ee73604034f`
- UBFORCE02: `a82bd7ef40ce18ddb00e45933290d1999de05884`

KT13 does not alter those modules.

## Selected-packet boundary

KT13 accepts one hydrology packet that has been selected by the surrounding application/provider layer.

KT13 does not reimplement KT11 multi-packet selection.

Before any scientific calculation, the selected packet is passed through the admitted KT06 binding client. KT06 therefore remains the authority for:

- producer/runtime whole-day mapping;
- producer-day offset;
- schema/unit validation;
- exact producer step and endpoint relation;
- KT05 projection eligibility.

Only if that binding passes does KT13 continue.

## Scientific composition path

After KT06 validation:

1. KT05 projects the selected packet to the explicit `Hydro_detailed` boundary.
2. HYDROEXEC01 executes the bounded revision-53 no-ponding upper hydrology equations.
3. HYDROQ01 carries resolved `Flpn`, post-`Modflux` `Flib(1)` and `Rurv`.
4. HYDROQ02 carries resolved `Rupr` and `Runinu`.
5. UBFORCE02 evaluates the pinned wet/advective load equations from resolved hydrology plus explicit chemistry.
6. UBFORCE01 selects one legacy load channel.
7. KT12 executes only the already-admitted TCD-042 B1/E1 algebra.
8. KT02 owns trial construction and the only accepted-state commit.

## Runinu continuation boundary

STATEQ08 qualifies `Runinu` as detailed-mode execution continuation state but does not admit it to the canonical state registry or checkpoint schema.

KT13 therefore requires it explicitly inside the HYDROEXEC01 start context.

This permits a bounded one-interval scientific composition test without pretending that multi-interval restart/state ownership is solved.

KT13 does not choose a first-call historical `Runinu` value and does not zero the near-zero branch.

## Chemistry boundary

KT13 consumes explicit typed chemistry forcing.

It does not parse `BOUNDARY.INP`.

Dry deposition remains separate and is not included in the load resolver.

## Atomicity

All hydrology binding, hydrology resolution and load resolution happen before KT02 publication.

A failure before the KT02 commit leaves the external accepted TCD-042 store unchanged.

An out-of-admitted-scope TCD-042 flux similarly fails before external publication.

## Supported envelope

The composed candidate remains bounded to the intersection of all consumed authorities:

- exact whole-day KT02 interval;
- selected KT05 explicit hydrology packet valid under KT06;
- detailed route `Iwa=2`, `Iopthyvs=1`, `Ioptmp=0`;
- no ponding;
- explicit call-entry `Runinu`;
- explicit required beginning hydrology context;
- explicit chemistry forcing;
- TCD-042 parent admission:
  `Flpn=0 AND Hetop>0 AND (Flux=0 OR (0<Flux<1.0d-8 AND 0<P<=3.8510200002999744e-7 AND binary64))`.

## Governance

KT13 is a cross-module scientific composition candidate and is Tier D.

It may be same-agent qualified as a nonproduction composition candidate.

It cannot be admitted without genuine independent Tier D review of the composition boundary and its prerequisite candidate authorities.

## Hard boundaries

No KT11 provider implementation change.
No BOUNDARY parser.
No dry deposition.
No full Hydro_detailed.
No ponding.
No macropores.
No canonical Runinu state admission.
No first-call Runinu assumption.
No retry/timestep policy.
No TCD-042 scope widening.
No B3 mutation.
No TB7.
No B4.
No production.
No Status A or AA.
