# ANIMO-STATEQ10 Work Unit Contract

Workunit: `ANIMO-STATEQ10 - First-Interval Detailed-Hydrology Origin Normalization Qualification`.

Execution discipline: `RECONCILE -> SOURCE MAP -> IMPLEMENT NORMALIZATION -> QUALIFY -> REVIEW -> HANDOFF`.

## Purpose

STATEQ10 qualifies only the source-defined conversion from already-read revision-53 REAL(4) initial hydrology coordinates into the first detailed-hydrology origin values needed by the current bounded route.

It does not parse the hydrology file and it does not choose missing initial values.

## Bounded source route

The qualified candidate is limited to:

`Hlpimp=11 AND Iopthyvs=1`

for these source coordinates:

- `SMofro(1:Nl) -> Mofro(1:Nl)`;
- `sSic -> Sic`;
- `SPn -> Pn`;
- `SSnla -> Snla`.

Frozen revision-53 `input1.for` reads those inputs as REAL(4) and converts every value through `Dble_trunc`.

## Frozen source identity

ANIMO 4.1.5 revision-53 archive:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Members:

- `input1.for`: `041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95`
- `Function.for`: `8d18e2558b43d38382033ed43a77bf00a71995804a20db0253f3a9795d748e59`

The mapped `input1.for` block is lines 2629 through 2648.

The mapped `Dble_trunc` implementation is `Function.for` lines 293 through 337.

## Dble_trunc

STATEQ10 preserves the source algorithm rather than relying on a generic REAL(4)-to-REAL(8) cast.

For already-read REAL(4) value `R4`, revision-53:

1. obtains the truncated integer part through `KINT`;
2. obtains `R=MOD(R4,1.0)`;
3. derives a decimal scaling exponent from `-LOG10(ABS(R))`;
4. evaluates the scaled fractional part in REAL(4);
5. rounds the promoted scaled value with `KIDNNT`;
6. constructs the REAL(8) result from that rounded decimal fraction plus the integer part.

STATEQ10 implements that source mapping explicitly in `normalize_rev53_real4`.

No generic cast is substituted.

## Typed candidate

The bounded first-origin type contains only:

- `Pn`;
- `Sic`;
- `Snla`;
- `Mofro(1:Nl)`.

It excludes `Runinu`.

STATEQ08 established that the first-call historical `Runinu` value is source-undefined and unqualified. STATEQ10 must not manufacture it.

## Relation to STATEQ09

STATEQ10 concerns only the first interval.

STATEQ09 concerns accepted endpoint to next-origin continuation after an interval has been accepted.

The two are complementary but distinct:

- first interval: STATEQ10 source-normalized initial values;
- later intervals: STATEQ09 exact accepted endpoint transfer;
- detailed-mode `Runinu`: STATEQ08 separate execution continuation.

## Exclusions

The same source area also reads `Wale`, `Late`, layer thickness `He` and other variables. They are outside this bounded first-origin contract because the currently targeted HYDROEXEC01 origin bundle does not require them as evolving origin coordinates.

Static geometry/configuration required by HYDROEXEC01 remains separately owned.

## Historical claim boundary

STATEQ10 qualifies source conversion semantics from explicit REAL(4) input values.

It does not establish that a particular historical testbank file contained a specific initial value unless separately evidenced.

It does not claim B2 historical runtime equivalence.

## Governance

This is input/state runtime semantics, conservatively classified as GOV04 Tier C.

Same-agent review may qualify the bounded candidate as `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Independent Tier C review remains required before canonical input/state admission.

## Hard boundaries

No file parser.
No first-call Runinu assumption.
No generic REAL(4)->REAL(8) replacement.
No canonical state registry mutation.
No checkpoint schema change.
No hydrology equations.
No B3 mutation.
No B4.
No production.
No Status A or AA.
