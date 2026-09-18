# ANIMO-HYDROQ02 Work Unit Contract

Workunit: `ANIMO-HYDROQ02 - TCD-042 Resolved Rupr/Runinu Load-Context Qualification`.

Execution discipline: `RECONCILE -> SOURCE MAP -> IMPLEMENT CONTRACT -> QUALIFY -> REVIEW -> HANDOFF`.

## Purpose

HYDROQ02 extends the resolved hydrology boundary only with the two runoff-partition outputs required by the source-authorized UBFORCE02 load equations:

- `Rupr`;
- `Runinu`.

It does not reconstruct those values from raw `Ru`.

## Authorities

Current program:

`ANIMO-RG06@8efdd151d89e1cff131d4b21e2acf559ca1828d6`

Resolved upper hydrology carrier:

`ANIMO-HYDROQ01@5301d90024c64057f2cb88fda1dbaa93aabfca47`

Load resolver candidate:

`ANIMO-UBFORCE02@931e32cec69dc78a03015f01190cff97bf1fe1b4`

Frozen source:

`Hydro_detailed.for@f3b8adc7ae56fc6f7002ce667c15288511984423e66ca619ccb4e90622bfbf5d`

## Source mapping

Revision-53 runoff partition logic contains three relevant routes.

For `Ru<0`:

`Runinu=-Ru`
`Rupr=0`
`Rurv=0`
`Ruso=0`

For the near-zero branch:

`-1e-8 < Ru < 1e-8`

the routine assigns:

`Rupr=0`
`Rurv=0`
`Ruso=0`

but does not locally assign `Runinu`.

For the remaining positive runoff route, `Runinu=0` is assigned before runoff partitioning and `Rupr` is then resolved from `Ru`, `Lefrrv`, `Lefrso` and precipitation constraints.

This matters. A new resolver must not silently assume that `Runinu=max(0,-Ru)` reproduces all revision-53 runtime behavior, because the near-zero branch does not establish that rule locally.

HYDROQ02 therefore qualifies only a captured resolved-value contract. It does not repair or reinterpret the historical near-zero branch.

## Contract

`tcd042_runoff_load_context_t` contains:

- schema id;
- resolution-stage id;
- hydrology execution id;
- exact origin time;
- exact endpoint time;
- resolved `Rupr`;
- resolved `Runinu`.

The execution identity must match the hydrology execution producing any companion HYDROQ01 resolved values.

Both values are preserved exactly.

No sign rule is added in this workunit.

## Scope

Whole-day exact KT02-compatible interval identity only.

No subday mapping.

No raw runoff reconstruction.

No runoff-partition algorithm migration.

## Governance

This is a hydrology/science composition interface candidate and is conservatively GOV04 Tier D.

Same-agent review may qualify the contract candidate. Independent Tier D review remains required before a composition admission can rely on it.

## Hard boundaries

No Hydro_detailed implementation.
No Rupr algorithm migration.
No Runinu repair.
No tolerance.
No B3 mutation.
No TB7.
No B4.
No production.
No Status A or AA.
