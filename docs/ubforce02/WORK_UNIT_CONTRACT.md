# ANIMO-UBFORCE02 Work Unit Contract

Workunit: `ANIMO-UBFORCE02 - TCD-042 Upper-Boundary Solute Load Resolver Qualification`.

Execution discipline: `RECONCILE -> SOURCE MAP -> IMPLEMENT -> QUALIFY -> REVIEW -> HANDOFF`.

## Purpose

UBFORCE02 implements only the already source-authorized revision-53 formulas that resolve the TCD-042 wet/advective top-load channels from:

- bounded hydrology context required by those formulas;
- explicit chemistry forcing;
- exact interval/provenance identity supplied to UBFORCE01.

It consumes the qualified UBFORCE01 typed carrier and does not widen its contract.

## Authorities

Program:

`ANIMO-RG06@8efdd151d89e1cff131d4b21e2acf559ca1828d6`

Carrier:

`ANIMO-UBFORCE01@9f9204ba53169285ac84272704de14836962ef41`

Architecture:

`ANIMO-ARCH05@99b6098a19db405ce34928af89bb78b856dce7cd`

Input audit:

`ANIMO-IO01@2bcf65360b08d278f28f1cc61ac96714db4793a3`

Frozen source archive:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Pinned source member:

`UBoundconc.for@b9a7ec980d40c0f76279077852190788e36cd976d185b12683a38da0c7dfecf7`

## Exact bounded source route

Only the source branch:

`Iwa=2 AND Iopthyvs=1`

is implemented.

Let:

`Wpr = Prr - Rupr + Prsn`.

Then revision-53 defines:

`Load1 = Wpr*Coprnhyn + Prirr*Coirrnh + Runon*Corunonnh + Runinu*Coidnh`

`Load2 = Wpr*Coprniyn + Prirr*Coirrni + Runon*Corunonni + Runinu*Coidni`

`Load3 = Prirr*Codiormairr + Runon*Codiormarunon + Runinu*Codiormaid`

`Load4 = Prirr*Codiorniirr + Runon*Codiornirunon + Runinu*Codiorniid`

when `Ipo=1`:

`Load5 = Wpr*Coprpoyn + Prirr*Coirrpo + Runon*Corunonpo + Runinu*Coidpo`

`Load6 = Prirr*Codiorpoirr + Runon*Codiorporunon + Runinu*Codiorpoid`

No alternative formulas are introduced.

## Hydrology context

The resolver consumes exactly:

- `Prr`;
- `Prsn`;
- `Prirr`;
- `Runon`;
- resolved `Rupr`;
- resolved `Runinu`.

UBFORCE02 does not derive `Rupr` or `Runinu` from raw runoff.

This is deliberate. In revision-53 `Hydro_detailed`, `Rupr` and `Runinu` are hydrology-resolution outputs. In particular, the near-zero runoff branch does not locally assign `Runinu`; UBFORCE02 therefore must not invent a deterministic replacement for that historical execution detail.

A later hydrology composition authority must explicitly supply the resolved values.

## Chemistry forcing

Chemistry is separate from hydrology per ARCH05.

The resolver carries explicit precipitation, irrigation, runon and run-in chemistry.

No parser is implemented here.

No BOUNDARY.INP grammar is migrated here.

When phosphorus is disabled, every phosphorus chemistry coordinate must be exact binary64 zero. This represents semantic absence rather than an inactive hidden value.

## Dry deposition

Dry N deposition is not part of this resolver.

Revision-53 applies it as a separate state pulse before the load formulas. Folding it into Load1 or Load2 would double-count and is prohibited.

## Numerical policy

The source formulas are evaluated in binary64 in explicit source order.

No epsilon, tolerance, clipping, sign correction or balancing term is introduced.

Equation tests use exact binary64 bit-pattern oracles.

## Governance

This is a science/forcing implementation seam. Conservative classification:

`GOV04 Tier D`.

Same-agent adversarial review may qualify the bounded implementation candidate but does not satisfy the independent Tier D admission gate.

## Hard boundaries

No BOUNDARY parser.
No hydrology resolver.
No Rupr/Runinu inference.
No dry deposition.
No ponding science.
No alternate Iwa/Iopthyvs branch.
No TCD re-admission.
No B3 mutation.
No TB7.
No B4.
No production.
No Status A or AA.
