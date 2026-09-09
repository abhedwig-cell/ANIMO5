# TCD-042 zero-throughflow atomization

Work unit: `ANIMO-UBQ01`

Target: `TCD-042`

Branch: `work/animo-ubq01-tcd042-upper-boundary-transaction`

Status: `SOURCE_THEORY_ATOMIZATION_PERSISTED_BEFORE_EXECUTABLE_VALIDATION`

## Scope

This note qualifies only the exact `Flux = 0` upper-boundary-reservoir branch. It does not select policy for the finite interval `0 < Flux < 1.0d-8`, does not change the threshold, and does not admit any correction.

Frozen identities:

- B0 source archive SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- B0 testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- ANIMO 4.0 user-guide/documentation SHA-256 `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`.

No production source is modified by UBQ01.

## Source owner and transaction

The exact revision-53 source already contains a persistent upper-boundary solute owner.

`Hetop` is the thickness of the virtual reservoir from which additions are leached. `Conhtop`, `Conitop`, `Codiormatop`, `Codiornitop`, `Copotop` and `Codiorpotop` are its accepted beginning concentrations. `Rs...top` are its accepted end concentrations.

The owner relation is source-bound by three independent surfaces:

1. `Outbal_Init.for:119-123` books beginning upper-reservoir N storage as `Conhtop*Hetop` and `Conitop*Hetop`.
2. `Outbal_calc.for:1173-1179` books end upper-reservoir N storage as `Rsconhtop*Hetop` and `Rsconitop*Hetop`.
3. `Init.for:324-336` promotes each `Rs...top` end state into the next interval's `...top` beginning state.

`Addit.for:360-370` also writes dissolved additions directly into this owner when there is no ponding, by dividing added mass by `Hetop`.

Therefore TCD-042 is not, for the exact-zero atom, a missing-owner or missing-state-representation problem. The state already exists and persists.

## Governing local reservoir equation recovered from the source algebra

For `Flpn = 0`, `UBoundconc.for:110-149` computes a residence-time reservoir response with

`P = St * Flux / Hetop`

and, for the ordinary positive-flow branch,

`A1 = exp(-P)`

`A2 = (1 - A1) / Flux`

`B1 = (1 - A1) / P`

`B2 = (1 - B1) / Flux`.

For any solute with beginning concentration `C0` and areic input rate `Load`, the source then evaluates

`C1 = C0*A1 + Load*A2`

and

`Cavg = C0*B1 + Load*B2`.

These coefficients are the exact solution and time-average of the local well-mixed reservoir balance

`Hetop * dC/dt = Load - Flux*C`.

Consequently the local conservation identity is

`Hetop*C1 = Hetop*C0 + St*Load - St*Flux*Cavg`.

No model extension is needed to obtain this identity. It is the identity represented by the existing positive-flow source algebra.

## Exact zero-throughflow limit

Taking the mathematical limit `Flux -> 0` while keeping `St`, `Hetop` and `Load` finite gives

`A1 -> 1`

`A2 -> St/Hetop`

`B1 -> 1`

`B2 -> St/(2*Hetop)`.

Thus at exact zero throughflow:

`C1 = C0 + Load*St/Hetop`

`Cavg = C0 + Load*St/(2*Hetop)`.

Because the advective output is exactly zero, conservation reduces to

`Hetop*C1 = Hetop*C0 + St*Load`.

The legacy fallback at `UBoundconc.for:119-123` instead sets

`A1=1, A2=0, B1=1, B2=0`.

It therefore produces `C1=C0` and discards `St*Load` from the represented end storage whenever `Load` is nonzero and `Flux=0`.

## Natural Ruurlo witness

MASSQ02 R016 provides a natural exact-zero witness at `TITO=1915`:

- `Iopthyvs = 0`;
- `Flib(1) = 0`;
- `Rurv = 0`;
- therefore `Flux = Max(0,Flib(1)+Rurv) = 0`;
- `Pr = 0.0002000407 m d-1`;
- `Coprnhyn = 0.002534 kg m-3`;
- `Coprniyn = 0.00084 kg m-3`;
- `St = 1 d`.

The frozen Ruurlo `SOIL.INP` gives `Hetop = 0.02 m`.

The precipitation loads are therefore exactly, from the recorded decimal witness values:

- NH4-N: `Pr*Coprnhyn = 5.069031338e-7 kg m-2 d-1`, equal to `0.005069031338 kg ha-1 d-1`;
- NO3-N: `Pr*Coprniyn = 1.68034188e-7 kg m-2 d-1`, equal to `0.00168034188 kg ha-1 d-1`;
- total mineral N: `0.006749373218 kg ha-1 d-1`.

MASSQ02 observed `0.0067493732130969875 kg ha-1 N` nonclosure, which localizes to the same transaction subject to diagnostic floating evaluation. UBQ01 does not use that small decimal difference as a tolerance or as the basis of the correction.

For the exact-zero limit, the implied end-concentration increments are:

- NH4-N: `2.534515669e-5 kg m-3`;
- NO3-N: `8.4017094e-6 kg m-3`.

The corresponding time-average increments are one half of those values.

## Theory reconciliation

The ANIMO 4.0 user guide independently states that:

- precipitation concentrations are explicit top-boundary inputs;
- the first compartment's incoming downward boundary uses precipitation with user-defined concentration;
- `Hetop` is the thickness of the virtual reservoir used for additions;
- `UBoundconc` calculates the upper-boundary concentration and the top layer used for additions;
- mass-balance output includes beginning and end storage plus boundary inputs.

This does not by itself specify the exact zero-flow discretization. The decisive zero-flow rule comes from the exact limiting form of the revision-53 positive-flow reservoir equation, combined with the already represented persistent owner and conservation identity.

## Atomization decision

For exact `Flux = 0`, the evidence rejects the three provisional interpretations as follows.

### Class A accounting-only

Rejected for the exact-zero atom.

Removing or delaying the booked precipitation input would make the ledger close only by preserving the legacy loss of a load that the source has already defined as an input to the upper-reservoir equation. It would also be discontinuous with the positive-flow reservoir equation as `Flux -> 0`.

### Class C missing state

Rejected for the exact-zero atom.

The required upper-reservoir state owner already exists, is included in beginning/end storage, receives additions, and is promoted across timesteps. No new physical store is required.

### Class B local algebra

Selected as the candidate classification for the exact-zero atom.

The defect is the local fallback coefficients used to avoid division by zero. The mathematically continuous zero-flow coefficients are uniquely determined by the existing positive-flow algebra. Applying those coefficients changes the existing reservoir state and later trajectories, but does not add or redefine state and does not require a new governing process.

Candidate class:

`B_LOCAL_ALGEBRA_ZERO_FLOW_LIMIT`

This is classification and qualification evidence only, not B3 admission.

## Deliberate nonclaim: positive sub-threshold flow

The source applies the same fallback for every `Flux < 1.0d-8`, not only `Flux = 0`.

UBQ01 does not silently generalize the exact-zero result to that finite interval. For `0 < Flux < 1.0d-8`, replacing the exact positive-flow solution by its strict zero-flow limit is a numerical approximation and can become a Class E numerical-policy question.

The exact-zero atom can therefore proceed independently while the finite positive sub-threshold seam remains fail-closed and separately classified if it is shown to be reachable and material.

## Required executable follow-up

Before UBQ01 can close as qualified Class-B readiness input, execute at least:

1. a synthetic exact-zero oracle proving the storage identity for NH4 and NO3 with no tolerance;
2. a natural Ruurlo exact-zero correction probe showing that only the declared upper-boundary reservoir transaction and causal descendants differ;
3. an exact non-interference control with `Load=0, Flux=0`;
4. a positive-flow control demonstrating that the ordinary branch is unchanged;
5. a reachability scan for `0 < Flux < 1.0d-8` so that the numerical seam is not silently absorbed into TCD-042.

No source correction, B3 admission or production migration is authorized by this note.
