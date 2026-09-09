# TCD-042 zero-throughflow atomization

Work unit: `ANIMO-UBQ01`

Target: `TCD-042`

Branch: `work/animo-ubq01-tcd042-upper-boundary-transaction`

Status: `QUALIFIED_EXACT_ZERO_CLASS_B_ATOM_PARENT_NUMERICAL_SUBTHRESHOLD_ATOM_PENDING`

## Scope

This note qualifies only the exact `Flux = 0` upper-boundary-reservoir atom. It does not select policy for the finite interval `0 < Flux < 1.0d-8`, does not change the threshold, and does not admit any correction.

Frozen identities:

- B0 source archive SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- B0 testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- ANIMO 4.0 user-guide/documentation SHA-256 `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`.

No production source is modified by UBQ01.

## Existing owner

Revision 53 already contains a persistent upper-boundary solute owner. `Hetop` is the virtual-reservoir thickness. `Conhtop`, `Conitop`, `Codiormatop`, `Codiornitop`, `Copotop` and `Codiorpotop` are accepted beginning concentrations; the corresponding `Rs...top` coordinates are accepted end concentrations.

The owner relation is source-bound by independent surfaces:

1. `Outbal_Init.for:119-123` books beginning upper-reservoir N storage as `Conhtop*Hetop` and `Conitop*Hetop`;
2. `Outbal_calc.for:1173-1179` books end storage as `Rsconhtop*Hetop` and `Rsconitop*Hetop`;
3. `Init.for:324-336` promotes each accepted `Rs...top` end state into the next interval's beginning state;
4. `Addit.for:360-370` writes dissolved additions into the same owner when there is no ponding.

Therefore the exact-zero atom is not a missing-owner or missing-state problem.

## Local equation and exact zero limit

For `Flpn = 0`, `UBoundconc.for:110-149` uses

`P = St*Flux/Hetop`

and, on the ordinary positive-flow branch,

`A1 = exp(-P)`

`A2 = (1-A1)/Flux`

`B1 = (1-A1)/P`

`B2 = (1-B1)/Flux`.

For beginning concentration `C0` and areic input rate `Load`:

`C1 = C0*A1 + Load*A2`

`Cavg = C0*B1 + Load*B2`.

This is the exact solution and time average of

`Hetop*dC/dt = Load - Flux*C`,

with conservation identity

`Hetop*C1 = Hetop*C0 + St*Load - St*Flux*Cavg`.

The unique mathematical limit for exact `Flux = 0` is

`A1 = 1`, `A2 = St/Hetop`, `B1 = 1`, `B2 = St/(2*Hetop)`,

so

`C1 = C0 + Load*St/Hetop`

and

`Cavg = C0 + Load*St/(2*Hetop)`.

The exact-zero conservation identity becomes

`Hetop*C1 = Hetop*C0 + St*Load`.

The legacy fallback for `Flux < 1.0d-8` instead sets `A1=1, A2=0, B1=1, B2=0`. At exact zero this leaves `St*Load` outside represented end storage whenever `Load != 0`.

## Natural Ruurlo witness

MASSQ02 R016 supplies a natural exact-zero witness at `TITO=1915` in `RuurloGrass`:

- `Flux = 0` from `Flib(1)=0` and `Rurv=0`;
- `Pr = 0.0002000407 m d-1`;
- `Coprnhyn = 0.002534 kg m-3`;
- `Coprniyn = 0.00084 kg m-3`;
- `St = 1 d`;
- `Hetop = 0.02 m`.

The booked mineral-N load is `0.006749373218 kg ha-1 d-1`. MASSQ02 observed `0.0067493732130969875 kg ha-1 N` nonclosure at this transaction. UBQ01 does not use the decimal difference as a tolerance or as the basis of the correction.

## Executable exact-zero evidence

The synthetic exact-zero oracle is green at GitHub Actions run `34362690102`, head `656bc7fe073a6e7636e73f88940e98bf023db9b7`. It proves the recovered zero-flow storage identity for NH4 and NO3 without tolerance and includes an exact zero-load negative control.

A separate B0-hash-pinned natural diagnostic probe then isolated the candidate exact-zero coefficients to `TITO=1915` only. This avoids letting earlier corrected events contaminate the causal comparison.

For `RuurloGrass`:

- 1,914 preceding accepted trace records are bitwise identical;
- the first difference is exactly `TITO=1915`;
- forcing, hydrology coordinates, beginning upper-reservoir state and immediate layer-1 state remain equal;
- the only immediate differences are the four predeclared direct mineral-N reservoir coordinates `Rsconhtop`, `Rsconitop`, `Avconhtop`, `Avconitop`;
- all four corrected binary64 values equal the recovered exact-zero formula predictions bitwise;
- the exact-zero zero-load control is bitwise unchanged;
- an ordinary positive-flow control is bitwise unchanged;
- later layer-1 chemistry differences appear only after the changed top-reservoir state has propagated forward.

The machine-readable record is `integration/animo-science/TCD042_NATURAL_EXACT_ZERO_PROBE.json`. Comparison policy is `EXACT_BITWISE_NO_TOLERANCE`.

The integrated validator covering source/theory identity, the synthetic exact-zero oracle contract, the isolated natural first difference, both non-interference controls and finite-positive reachability passed on GitHub Actions run `34365508588` at head `87171f13e2492e8f467bc456c2a90564b54ffe5c`.

This evidence supports a local causal first difference rather than an accounting-only repair or new-state interpretation.

## Atomization decision for exact zero

### Class A accounting-only

Rejected for exact zero. Delaying or removing the booked precipitation input would preserve the physical loss and break continuity with the existing positive-flow reservoir equation.

### Class C missing state

Rejected for exact zero. The persistent upper-reservoir owner already exists and is represented in beginning/end storage and continuation.

### Class B local algebra

Qualified as the candidate atom classification:

`B_LOCAL_ALGEBRA_ZERO_FLOW_LIMIT`

The correction candidate is the unique exact-zero limit of the already represented reservoir equation. It changes the existing reservoir state and causal descendants but does not add a state owner or redefine the process.

This is qualification/readiness evidence only. It is not B3 admission.

## Finite positive sub-threshold seam is reachable

The legacy fallback also applies to `0 < Flux < 1.0d-8`. UBQ01 has now scanned the frozen testbank with the baseline diagnostic trace.

Eight cases were executable for this scan; `GHGMais` was fail-closed before trace production by its separate GHG input/output contract, so no absence claim is made for that case. Across the eight executed cases:

- 15,043 no-ponding records were scanned;
- 5,370 had exact `Flux=0`;
- 1,238 had finite positive `0<Flux<1.0d-8`;
- six of the eight executed cases reached that finite-positive sub-threshold interval.

Thus the finite-positive seam is naturally reachable. It cannot be silently absorbed into the exact-zero Class-B atom. Its provisional route is numerical-policy work:

`E_NUMERICAL_POLICY`

Materiality, a cancellation-safe evaluation and any threshold/numerical policy remain unresolved. No tolerance, threshold change, new TCD reservation or canonical child is created by this reachability result. The machine record is `integration/animo-science/TCD042_SUBTHRESHOLD_REACHABILITY.json`.

## Current boundary

The exact-zero atom is qualified as Class-B readiness evidence from source, theory, synthetic oracle and isolated natural executable evidence. The parent TCD-042 is not fully closed because the finite-positive sub-threshold atom remains open and because GOV02/B3Q01 route and independent admission review are separate gates.

UBQ01 authorizes no production source change, no corrected-legacy admission, no B3 baseline and no production migration.
