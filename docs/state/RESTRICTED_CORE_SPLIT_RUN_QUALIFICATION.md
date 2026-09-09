# ANIMO-STATEQ02 restricted-core executable split-run qualification

Status: `IN_PROGRESS_PERSISTED_BEFORE_LONG_EXECUTION`

Branch: `work/animo-stateq02-restricted-core-executable-split-run`

Base: `ANIMO-STATEQ01@4adae99576eb56978da71f7c8a250e4445fd3bc4`

External canonical-intake authority checked: `work/animo-b3i01-canonical-register-append@383c7a83e84a578969f92113280dc715b7bdddb4`.

Frozen B0 identities required for every executable probe:

- source archive SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank archive SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

## Purpose

Qualify behavioural restart semantics for an explicitly restricted C/N/P core envelope by comparing uninterrupted execution with:

`run -> accepted boundary -> checkpoint -> restore -> continue`.

This workunit is qualification-only. It does not implement production checkpoint code and does not make a whole-model STATE claim.

## Fail-closed scope

Included when the executable fixture can preserve all contracts:

- C/N/P physical state;
- explicit P site-resolved state;
- management continuation;
- upper-boundary addition reservoirs;
- exact external hydrology-frame identity;
- accepted-state boundary identity;
- continuation-critical cumulative physical state.

Excluded unless independently complete:

- GHG, including canonical `TCD-041` lower-air-boundary initialization omission;
- macropores;
- `TCD-016-C1` dry-solute continuation transition;
- surface-layer restart paths affected by canonical `TCD-040` layer-0 aqueous restart initialization zeroing;
- internal-crop restart state while PREP12 crop continuation findings remain unresolved;
- report accumulators as physical owners.

The restricted surface guard therefore requires exact zero surface storage and exact zero layer-0 dissolved restart state. Nonzero cases are rejection sentinels, never normalized inputs.

## Hard rules

- no restart-output editing to force equality;
- no omitted-state zero fill;
- no hidden tolerance;
- no report accumulator promoted to physical state;
- no canonical STATE admission from parser/serializer roundtrip alone;
- no production implementation;
- exact equality wherever representation permits;
- floating trajectory comparison only under a previously qualified numerical policy. STATEQ02 invents no tolerance.

## Required boundary matrix

The campaign will attempt at least:

1. ordinary interior accepted boundary;
2. management-adjacent accepted boundary;
3. year boundary;
4. P-active explicit-site state;
5. nonzero upper-boundary reservoir state with no surface ponding;
6. zero-surface-storage negative-control acceptance plus deliberate positive-surface rejection sentinel.

Additional sentinels cover incompatible external-frame identity and nonzero layer-0 restart state.

## Evidence discipline

The first persisted checkpoint precedes long compilation/execution. Final claims will distinguish:

- B0 hash-pinned executable evidence;
- synthetic B0-derived fixture evidence, explicitly not B2;
- source/synthetic contracts inherited from STATEQ01;
- unresolved discrepancies.

No result is claimed until recorded in the companion matrix and diff artifacts.
