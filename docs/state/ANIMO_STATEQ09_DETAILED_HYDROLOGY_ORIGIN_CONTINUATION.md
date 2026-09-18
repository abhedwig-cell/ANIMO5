# ANIMO-STATEQ09 Work Unit Contract

Workunit: `ANIMO-STATEQ09 - Detailed-Hydrology Accepted Endpoint to Next-Origin Continuation Qualification`.

Execution discipline: `RECONCILE -> SOURCE MAP -> IMPLEMENT CONTRACT -> QUALIFY -> REVIEW -> HANDOFF`.

## Purpose

STATEQ09 qualifies the revision-53 state-transfer semantics that turn accepted end-of-step detailed-hydrology values into the beginning-of-step values used by the next interval.

The bounded route is the current SWAP detailed input path:

`Iwa=2 AND Iopthyvs=1 AND Hlpimp=11`.

## Frozen source identity

ANIMO 4.1.5 revision-53 archive:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Relevant members:

- `Animo.for`: `352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7`
- `Init.for`: `287db00773ea21a155383b01a3ea35426c216117085822069e7bd844f71e0058`

## Source ordering

Revision-53 `Animo.for` calls `Init` at the start of each timestep before `Input_hydro` and before `Hydro_detailed`.

The source comment explicitly describes the operation as:

`UPDATE STATE VARIABLES (RESULT FROM PREVIOUS STEP)`.

For the bounded route, `Init.for` performs:

- `Mofro(Ln)=Mofrt(Ln)`, for `Ln=1..Nl`;
- `Snla=Snt` when `Iopthyvs=1`;
- `Sic=Sict` when `Iopthyvs=1 AND Hlpimp=11`;
- `Pn=Pnt`.

These assignments are source-defined inter-step continuation semantics.

## Qualified candidate state

STATEQ09 defines a typed detailed-hydrology origin bundle containing:

- `Pn`;
- `Sic`;
- `Snla`;
- `Mofro(1:Nl)`.

For the bounded route, advancing one accepted endpoint into the next origin is an exact copy:

`Pn <- Pnt`

`Sic <- Sict`

`Snla <- Snt`

`Mofro(1:Nl) <- Mofrt(1:Nl)`.

No interpolation, averaging, clipping or tolerance is introduced.

## Relation to STATEQ08

`Runinu` is deliberately NOT part of the STATEQ09 bundle.

Revision-53 `Init` does not assign `Runinu`. STATEQ08 separately qualifies it as detailed-mode execution continuation state because the near-zero runoff branch can preserve its call-entry value.

The future multi-interval runtime therefore needs both:

1. STATEQ09 accepted endpoint-to-origin hydrology continuation;
2. STATEQ08 explicit `Runinu` execution continuation.

Do not merge those authorities silently.

## Static configuration exclusions

HYDROEXEC01 also consumes `He(1)`, `Lefrrv` and `Lefrso`.

Those are configuration/geometry inputs, not endpoint-to-origin state transferred by `Init`, and are outside STATEQ09.

## First interval

STATEQ09 qualifies transfer after an accepted endpoint exists.

It does not establish the initial simulation values of `Pn`, `Sic`, `Snla` or `Mofro`.

Initial-condition authority remains separate.

## Restart implication

If a restart boundary occurs after an accepted interval and the next detailed hydrology calculation requires these origin values, source-faithful continuation requires their values to be reconstructable.

STATEQ09 may qualify that dependency as a restart requirement candidate. It does not modify or admit the canonical checkpoint schema.

## Governance

The work changes no science. It qualifies state/restart runtime semantics and is conservatively treated as GOV04 Tier C.

Same-agent review is `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Independent Tier C review remains required before any new canonical state/checkpoint admission.

## Hard boundaries

No production source change.
No canonical state registry modification.
No checkpoint schema modification.
No initial-condition invention.
No Runinu ownership merge.
No hydrology equations.
No B3 mutation.
No B4.
No production.
No Status A or AA.
