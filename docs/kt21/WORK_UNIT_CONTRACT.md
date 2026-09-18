# ANIMO-KT21 Work Unit Contract

Workunit: `ANIMO-KT21 - Pinned LWKM Bounded TCD-042 Hydrology-Envelope Characterization`.

Execution discipline: `RECONCILE -> CHARACTERIZE -> CROSS-CHECK -> PERSIST -> QUALIFY -> REVIEW`.

## Purpose

KT21 characterizes, without changing science, how the exact pinned LWKM hydrology sequence intersects the currently admitted TCD-042 hydrology-side envelope.

This workunit exists because KT20 proved a materially real packet can reach the application boundary, but the first packet cannot be treated as a historical accepted application merely by choosing a convenient `Runinu` value.

KT21 makes that limitation quantitative.

## Authorities

Current program rebaseline:

`ANIMO-RG09@b019ac4507648e57c196a8a62806d804f39014a2`

Pinned real-file provider:

`ANIMO-KT19@6245aad4aca962cb2a63d0394bb7f2baa686457d`

Cross-language bridge:

`ANIMO-KT20@c41a28580421bf4dce770e438535ba92a57567cd`

Runinu source classification:

`ANIMO-STATEQ08@e9ee7fc9e69a62c58b6eacd6379220cc51c1bf07`

Accepted endpoint-to-origin transfer:

`ANIMO-STATEQ09@f6e91fc1cb664d67caccc02e6ab21525a768d006`

Bounded hydrology equations:

`ANIMO-HYDROEXEC01@182dac2fc34ca42ed798203e90efeca1221f21e8`

TCD-042 parent:

`ANIMO-B3D35@9ca23f41dc3c28af686b1bc0bff8e7d66416d367`.

## Pinned source

Hydrology source:

`ANIMO_testbank/LWKM_gras_1040.2021.2045/input/SWATRE.UNF`

SHA-256:

`b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c`

Soil configuration source:

`ANIMO_testbank/LWKM_gras_1040.2021.2045/input/SOIL.INP`

SHA-256:

`57f2173723172bb5f92621786f7a49b23b8f497ee3554f25a36ea19ae0968f3c`

Bounded `>profil:` values consumed by the characterization:

- `Hetop=0.02 m`;
- `Lefrrv=0.2`;
- `Lefrso=0.25`;
- layer count 30.

No B0 raw file is committed by KT21.

## Runinu rule

STATEQ08 established a real source ambiguity:

- detailed `Hydro_detailed` assigns `Runinu=-Ru` for negative runoff;
- assigns `Runinu=0` on the positive/non-near-zero runoff branch;
- does not assign `Runinu` in the near-zero runoff branch.

Therefore the first call has an unknown `Runinu` whenever the source enters the near-zero branch.

KT21 starts `Runinu` as explicitly unknown. It does not assume zero.

A packet remains blocked by that unknown continuation until a later source branch assigns `Runinu`.

## Characterization method

For each KT19-normalized packet:

1. preserve the source-defined endpoint-to-next-origin coordinates;
2. apply the bounded HYDROEXEC01 runoff partition and top-layer hydrology equations;
3. keep the first-call `Runinu` symbolic/unknown until a source branch assigns it;
4. classify ponding separately;
5. for deterministic no-ponding packets calculate `Flux` and `P=St*Flux/Hetop`;
6. compare only against the existing B3D35 hydrology-side envelope.

Classes are:

- `BLOCKED_FIRST_CALL_RUNINU`;
- `PONDING_OUTSIDE_TCD042`;
- `TCD042_B1_EXACT_ZERO_HYDROLOGY`;
- `TCD042_E1_HYDROLOGY_ENVELOPE`;
- `TCD042_HYDROLOGY_OUTSIDE_ADMITTED_SCOPE`;
- `REV53_RUNOFF_PARTITION_SINGULARITY`.

## External pinned-source result

For the exact 1800-packet LWKM sequence:

- 347 initial packets are blocked by the source-undefined first-call `Runinu`;
- packet index 347 is the first non-near-zero runoff event and assigns `Runinu=0`;
- 1453 packets from that point are deterministic with respect to the initial `Runinu`;
- 2 deterministic packets are ponding;
- 36 fall on the exact-zero B1 hydrology branch;
- 14 fall inside the finite-positive E1 hydrology envelope;
- 1401 deterministic packets remain outside the currently admitted TCD-042 hydrology scope;
- no bounded runoff-partition singularity occurs.

Thus only 50 of the deterministic packets intersect the current TCD-042 hydrology-side B1/E1 envelope.

## Critical interpretation

The 50-packet intersection is NOT a sequential accepted-application result.

The current bounded application cannot simply advance through the real source to those anchors because most intervening deterministic packets are outside the admitted TCD-042 scope, and the first 347 packets carry an unresolved historical `Runinu` dependency.

KT21 is therefore characterization evidence, not an application admission.

## Evidence class

The persisted full-source result is:

`B1_DIAGNOSTIC_CHARACTERIZATION_DERIVED_FROM_PINNED_B0_NOT_B2`.

Packet normalization follows the KT03 diagnostic `Dble_trunc` lineage and therefore does not establish independent historical compiler equivalence.

## Governance

KT21 changes no model equations and admits nothing.

Conservative review tier: GOV04 Tier C evidence/runtime characterization.

Same-agent review is only:

`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

## Hard boundaries

No first-call Runinu value invented.
No TCD-042 scope widening.
No sequential real-source application claim.
No B2.
No B3 mutation.
No central KT11 admission.
No canonical forcing/state/checkpoint admission.
No TB7.
No B4.
No production.
No Status A or AA.
