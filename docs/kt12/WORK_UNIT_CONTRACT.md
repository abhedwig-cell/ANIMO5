# ANIMO-KT12 Work Unit Contract

Workunit: `ANIMO-KT12 - TCD-042 Scientific Consumer on the Transaction Runtime and Resolved-Hydrology Seam Qualification`.

Execution discipline: `RECONCILE -> IMPLEMENT -> QUALIFY -> REVIEW/HANDOFF -> CLOSE`.

## Purpose

KT12 is the first bounded workunit that places already admitted ANIMO scientific algebra inside the KT02 transaction runtime.

It consumes the bounded TCD-042 parent admission without widening it. The scientific scope remains exactly:

`Flpn=0 AND Hetop>0 AND (Flux=0 OR (0<Flux<1.0d-8 AND 0<P<=3.8510200002999744e-7 AND binary64))`

with TCD-042-B1 and TCD-042-E1 as admitted by their existing B3 authorities.

KT12 also tests whether the current KT11 -> KT06 -> KT05 hydrology lane can already supply the exact scientific forcing required by TCD-042.

## Authorities

Program rebaseline:

`ANIMO-RG06@8efdd151d89e1cff131d4b21e2acf559ca1828d6`

Exact-final workflow:

`35359364830 -> SUCCESS`

Runtime:

- `ANIMO-KT11-A1@50731bf118deb8ef1029f220a40b39a99240e480`
- `ANIMO-KT06-A1@56384db4107aed484218363e26dbb7be7f51e8de`
- KT02 frozen runtime inherited through KT11.

Science:

- `ANIMO-B3D35@9ca23f41dc3c28af686b1bc0bff8e7d66416d367`, parent admission;
- `ANIMO-B3D33@8b2a4071d623bc2e3003dca8977e032d5c0d8c3c`, exact-zero B1 admission;
- `ANIMO-B3D34@22e4ec3bb88e2e13905ccbbb2f380a9bf235db55`, finite-positive E1 admission;
- `ANIMO-UBQ01@6895b67799f26888025eced7188e7190b2a0d07d`;
- NQ03 selected binary64 natural-envelope policy as consumed by the admitted E1 authority.

## Frozen source mapping

The following revision-53 source files are used only to establish the exact seam between external hydrology input and TCD-042. Their byte identities are pinned:

- `Hydro_detailed.for`: SHA-256 `f3b8adc7ae56fc6f7002ce667c15288511984423e66ca619ccb4e90622bfbf5d`;
- `MODFLUX.FOR`: SHA-256 `0c0909922e88ee59233cabc307fb18243ea86023b4722879f6301259780de93d`;
- `UBoundconc.for`: SHA-256 `b9a7ec980d40c0f76279077852190788e36cd976d185b12683a38da0c7dfecf7`.

These files are members of the frozen B0 source package. KT12 does not modify or redistribute them.

## Owned surface

KT12 owns only:

1. a nonproduction TCD-042 transaction-runtime scientific client;
2. a candidate typed carrier for the already-resolved post-`Hydro_detailed` upper-boundary hydrology quantities consumed by TCD-042;
3. transaction tests proving accept/reject atomicity around the admitted TCD-042 algebra;
4. a composition-readiness decision for connecting that client to the current KT11/KT06 lane.

The candidate resolved-hydrology carrier is NOT a qualified Hydro_detailed output authority and is NOT a replacement for Hydro_detailed.

## Scientific implementation

For exact `Flux=0`, KT12 implements only the admitted B1 limit:

`C1 = C0 + Load*St/Hetop`

`Cavg = C0 + Load*St/(2*Hetop)`

For admitted finite-positive E1, KT12 implements only the admitted NQ03 policy:

`P = St*Flux/Hetop`

`A1 = exp(-P)`

`f = 1-P/2+P^2/6`

`g = 1/2-P/6+P^2/24`

`A2 = (St/Hetop)*f`

`B1 = f`

`B2 = (St/Hetop)*g`

`C1 = C0*A1 + Load*A2`

`Cavg = C0*B1 + Load*B2`

No tolerance, fallback, extrapolation or alternative threshold is added.

KT02 exact accepted time is the sole source of `St`. Producer time remains non-authoritative.

## Critical composition boundary

KT05 projects producer-derived values TO the `Hydro_detailed` call surface. It expressly does not own or execute:

- `Flpn`;
- runoff partitioning;
- `Rurv`;
- `Modflux`;
- accepted hydrology state.

Frozen revision-53 science derives the TCD-042 throughflow only after those operations:

`Flux = Max(0, Flib(1) + Rurv)`.

`Flib(1)` is a `Modflux` output from post-`Hydro_detailed` `Flab`, not merely the producer `Flab(1)` carried by KT05.

Therefore KT12 MUST NOT connect raw KT11/KT05 `flab(1)` directly to TCD-042.

A direct `KT11 -> KT06 -> TCD042` science composition is positive only if an independently qualified post-`Hydro_detailed` resolved-hydrology authority exists. None is admitted at KT12 authoring.

## Governance

This work crosses the runtime/science module boundary and is therefore treated conservatively as a GOV04 Tier D composition candidate.

Same-agent adversarial review may qualify the authoring package as a bounded candidate. It cannot satisfy the required independent composition review or admit the composition.

## Hard boundaries

No production source.
No B4.
No TCD re-admission.
No TCD-042 scope widening.
No Hetop=0.
No Flux >= 1e-8.
No P beyond NQ03.
No generic calendar conversion.
No subday policy.
No direct raw KT05 Flab-to-TCD042 shortcut.
No Hydro_detailed emulation.
No Modflux emulation.
No balancing mass or numerical tolerance.
No TCD-016, TCD-034 or TCD-040 change.
No Status A or AA.
