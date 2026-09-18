# ANIMO-HYDROQ01 Work Unit Contract

Workunit: `ANIMO-HYDROQ01 - TCD-042 Post-Hydro_detailed Resolved Upper-Boundary Hydrology Contract & Source Mapping`.

Execution discipline: `RECONCILE -> SOURCE MAP -> IMPLEMENT CONTRACT -> QUALIFY -> REVIEW -> HANDOFF`.

## Purpose

HYDROQ01 qualifies only the typed resolved-hydrology seam required between the existing ANIMO hydrology responsibility and downstream TCD-042 science.

It does not implement `Hydro_detailed` or `Modflux`. It defines and tests the smallest explicit carrier that can represent the already-resolved revision-53 no-ponding hydrology values consumed by TCD-042 after those routines have run.

## Frozen authorities

Program authority:

`ANIMO-RG06@8efdd151d89e1cff131d4b21e2acf559ca1828d6`

Runtime authorities:

- `ANIMO-KT11-A1@50731bf118deb8ef1029f220a40b39a99240e480`
- `ANIMO-KT06-A1@56384db4107aed484218363e26dbb7be7f51e8de`

Scientific consumer candidate:

`ANIMO-KT12@8f0e8e4bfd0b391b781f7c69b7d2063d5cf8705e`

TCD-042 parent science:

`ANIMO-B3D35@9ca23f41dc3c28af686b1bc0bff8e7d66416d367`

## Frozen revision-53 source identity

Source archive:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Exact source members:

- `Hydro_detailed.for`: `f3b8adc7ae56fc6f7002ce667c15288511984423e66ca619ccb4e90622bfbf5d`
- `MODFLUX.FOR`: `0c0909922e88ee59233cabc307fb18243ea86023b4722879f6301259780de93d`
- `UBoundconc.for`: `b9a7ec980d40c0f76279077852190788e36cd976d185b12683a38da0c7dfecf7`

These identities are evidence pins only. HYDROQ01 does not modify or republish frozen B0 source.

## Exact source mapping

For revision-53 no-ponding execution:

1. `Hydro_detailed` sets `Flpn=0` when both beginning and end surface ponding+snow storage are below its threshold.
2. Within every `Flpn=0` runoff path, resolved `Rurv` is exact zero before return from the runoff partitioning block.
3. `Hydro_detailed` recalculates `Flab(1)` from internal ANIMO water-balance terms.
4. `Hydro_detailed` calls `Modflux`.
5. `Modflux` sets `Flib(Ln)=Max(0,Flab(Ln))`, therefore `Flib(1)` is a post-`Hydro_detailed`, post-`Modflux` resolved quantity.
6. `UBoundconc` subsequently computes no-ponding top-reservoir throughflow as `Flux=Max(0,Flib(1)+Rurv)`.

Because `Rurv=0` on this resolved no-ponding branch and `Flib(1)>=0`, the TCD-042 hydrology input is equivalent there to the resolved `Flib(1)`, but the carrier retains `Rurv` explicitly so that the source invariant is machine-verifiable rather than silently assumed.

## Qualified carrier candidate

`resolved_upper_hydrology_t` owns only:

- schema identity;
- unit-contract identity;
- resolution-stage identity;
- hydrology execution provenance identifier;
- exact KT02-compatible origin time;
- exact KT02-compatible endpoint time;
- resolved `Flpn`;
- post-`Modflux` `Flib(1)`;
- resolved `Rurv`.

Current bounded unit semantics:

- `Flib(1)`: m d-1;
- `Rurv`: m d-1;
- time coordinate: KT02 exact day coordinate in the currently admitted whole-day envelope.

## Bounded scope

HYDROQ01 qualifies only the TCD-042 no-ponding resolved carrier:

`Flpn=0 AND Flib_top>=0 AND Rurv=exact binary64 zero`

with an exact forward whole-day interval and non-empty execution identity.

HYDROQ01 does not qualify ponding, subday mapping, generic calendars, other downstream flux families or complete `Hydro_detailed` output.

## Critical ownership rule

KT05 `flab(1)` is producer-side input to `Hydro_detailed`.

HYDROQ01 `flib_top` is post-`Hydro_detailed`, post-`Modflux` resolved output.

They are not interchangeable.

## Governance

This seam spans two scientific modules and is intended for later composition with KT12. It is conservatively classified as a GOV04 Tier D composition-interface candidate.

Same-agent adversarial review may qualify the bounded contract package as a candidate, but cannot satisfy any independent Tier D admission gate.

## Hard boundaries

No production source change.
No Hydro_detailed implementation.
No Modflux implementation.
No KT05 Flab promotion.
No TCD-042 re-admission.
No B3 mutation.
No TB7.
No B4.
No production.
No Status A or AA.
