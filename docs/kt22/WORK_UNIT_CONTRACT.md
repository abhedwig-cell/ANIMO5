# ANIMO-KT22 Work Unit Contract

Workunit: `ANIMO-KT22 - Pinned LWKM TCD-042 Exclusion-Boundary Decomposition and Routing`.

Execution discipline: `RECONCILE -> DECOMPOSE -> CROSS-CHECK -> PERSIST -> QUALIFY -> REVIEW`.

## Purpose

KT21 established that only 50 of 1453 deterministic packets in the pinned LWKM sequence intersect the currently admitted TCD-042 B1/E1 hydrology-side envelope, while 1401 deterministic packets were labelled `TCD042_HYDROLOGY_OUTSIDE_ADMITTED_SCOPE` and two were ponding.

KT22 determines what that 1401-packet remainder actually is. It does not widen TCD-042 and does not add scientific process semantics.

The central question is whether the remainder exposes an unresolved numerical subthreshold TCD-042 gap, or whether it lies on a different legacy branch that is outside the atomized TCD-042 fallback by construction.

## Authorities

Current program rebaseline:

`ANIMO-RG09@b019ac4507648e57c196a8a62806d804f39014a2`

Predecessor characterization:

`ANIMO-KT21@e591344d9a2fd03b92fd56af1b9b555099edc340`

TCD-042 bounded parent authority:

`ANIMO-B3D35@9ca23f41dc3c28af686b1bc0bff8e7d66416d367`

Exact-zero scientific authority:

`ANIMO-UBQ01@6895b67799f26888025eced7188e7190b2a0d07d`

Bounded no-ponding hydrology execution candidate:

`ANIMO-HYDROEXEC01@182dac2fc34ca42ed798203e90efeca1221f21e8`

GOV04 authority:

`1bbe4c211197590f346803106e45dca5faae79fc`

## Frozen legacy discriminator

Revision-53 `UBoundconc` computes, in the no-ponding branch:

`Flux = Max(0.0, Flib(1) + Rurv)`

It then selects the ordinary finite-positive exponential branch when:

`Flux >= 1.0d-8`

and selects the fallback branch only when:

`Flux < 1.0d-8`.

The admitted bounded TCD-042 parent is exactly the positive-HETOP fallback scope:

`Flpn=0 AND Hetop>0 AND (Flux=0 OR (0<Flux<1.0d-8 AND 0<P<=3.8510200002999744e-7 AND binary64))`.

B3D35 explicitly lists `Flux>=1.0d-8` and `Flpn!=0` outside the atomized TCD-042 parent claim.

Therefore KT22 must not reinterpret those domains as missing TCD-042 semantics.

## Pinned source

Source container:

`ANIMO_testbank.zip`

SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Hydrology member:

`ANIMO_testbank/LWKM_gras_1040.2021.2045/input/SWATRE.UNF`

SHA-256:

`b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c`

Soil member:

`ANIMO_testbank/LWKM_gras_1040.2021.2045/input/SOIL.INP`

SHA-256:

`57f2173723172bb5f92621786f7a49b23b8f497ee3554f25a36ea19ae0968f3c`

The exact bounded geometry remains `Hetop=0.02 m`, `Lefrrv=0.2`, `Lefrso=0.25`.

## Decomposition result

The exact KT21 partition is preserved:

- 1800 packets total;
- 347 initial packets blocked by source-undefined first-call `Runinu`;
- 1453 packets deterministic after the first source assignment of `Runinu`;
- 36 exact-zero B1 packets;
- 14 finite-positive E1 packets;
- 1401 no-ponding packets outside the admitted TCD-042 parent;
- 2 ponding packets.

KT22 reclassifies only the already deterministic 1401-packet outside remainder.

All 1401 packets satisfy:

`Flpn=0 AND Flux>=1.0d-8`.

None satisfy:

`Flpn=0 AND 0<Flux<1.0d-8 AND P>Pmax`.

The minimum resolved flux in that remainder is `5.111600000000339e-7 m d-1`, more than 51 times the TCD-042 branch threshold. The maximum is `0.010496963211764706 m d-1`.

Thus the entire 1401-packet remainder belongs to the revision-53 ordinary positive-flow branch, not to an unqualified numerical sub-envelope of TCD-042.

The two ponding packets remain a separate `Flpn!=0` capability gap. The first 347 packets remain blocked by the independent first-call `Runinu` provenance problem.

## Routing consequence

KT21's 1401-packet label was a correct fail-closed application-envelope label, but it must not be read as evidence that TCD-042 itself needs a 1401-packet scope extension.

For sequential real-source application, the missing scientific/runtime surface is now decomposed into three independent fronts:

1. source-faithful first-call `Runinu` continuation/provenance for the initial 347 packets;
2. a typed scientific consumer/composition for the revision-53 no-ponding ordinary positive-flow `Flux>=1.0d-8` branch;
3. a separately qualified ponding `Flpn!=0` branch for the two observed packets.

This workunit authorizes none of those semantics. It only routes the evidence.

## Evidence class and review

Evidence class:

`B1_DIAGNOSTIC_ROUTING_DERIVED_FROM_PINNED_B0_NOT_B2`.

Conservative risk tier:

`GOV04 Tier C evidence/runtime characterization`.

Same-agent adversarial review may test the internal consistency of the routing claim, but cannot satisfy any genuinely independent review or admission gate.

## Hard boundaries

No TCD-042 widening.

No ordinary positive-flow scientific implementation.

No ponding implementation.

No invented first-call `Runinu`.

No B2 historical equivalence.

No B3 mutation or readmission.

No canonical state, forcing or checkpoint admission.

No TB7.

No B4.

No production.

No Status A or AA.
