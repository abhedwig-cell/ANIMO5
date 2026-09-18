# ANIMO-HYDROEXEC01 Work Unit Contract

Workunit: `ANIMO-HYDROEXEC01 - Bounded Revision-53 No-Ponding Upper Hydrology Execution Qualification`.

Execution discipline: `RECONCILE -> SOURCE MAP -> IMPLEMENT -> QUALIFY -> REVIEW -> CLOSE/HANDOFF`.

## Purpose

HYDROEXEC01 is the first executable realization of the exact revision-53 upper-boundary hydrology algebra needed to produce the already qualified HYDROQ01 and HYDROQ02 carriers.

It is deliberately not a full migration of `Hydro_detailed`.

The implementation covers only the bounded source path required for no-ponding TCD-042 composition and keeps every omitted responsibility explicit.

## Authorities

Program authority:

`ANIMO-RG06@8efdd151d89e1cff131d4b21e2acf559ca1828d6`

Hydrology input boundary:

`ANIMO-KT05` as consumed through the admitted runtime lane.

Resolved hydrology carrier:

`ANIMO-HYDROQ01@5301d90024c64057f2cb88fda1dbaa93aabfca47`

Resolved runoff/load context:

`ANIMO-HYDROQ02@08d5b8301c217cf9d33d2bf248be133f2b5243fc`

Scientific consumer scope:

`ANIMO-B3D35@9ca23f41dc3c28af686b1bc0bff8e7d66416d367`

## Frozen source identity

ANIMO 4.1.5 revision-53 archive:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Exact source members:

- `Hydro_detailed.for`: `f3b8adc7ae56fc6f7002ce667c15288511984423e66ca619ccb4e90622bfbf5d`
- `MODFLUX.FOR`: `0c0909922e88ee59233cabc307fb18243ea86023b4722879f6301259780de93d`

Historical Visual Fortran project file used as precision evidence:

`animo41.vfproj` SHA-256 `f8ac40ea91df926a035396b0afe8584ea0d9c19711535a12b4f12634ce688b2a`

The project specifies `RealKIND="realKIND8"`, so the bounded executable realization uses binary64.

## Exact bounded source path

HYDROEXEC01 implements only the following source responsibilities:

1. no-ponding classification from beginning/end ponding plus snow storage;
2. revision-53 runoff partition for `Ru`, `Runinu`, `Rupr`, `Rurv`, `Ruso`;
3. first top-layer `Flab(1)` reconstruction;
4. detailed-hydrology `Dif` calculation for `Iopthyvs=1`;
5. `Evso = Max(0, Evso-Dif)`;
6. final top-layer `Flab(1)` reconstruction;
7. the `Modflux` identity `Flib(1)=Max(0,Flab(1))`;
8. emission of HYDROQ01 and HYDROQ02 typed values with one shared execution identity.

## Scope

The bounded execution envelope is:

- `Iwa=2`;
- `Iopthyvs=1`;
- `Ioptmp=0`;
- `Flpn=0`;
- at least one soil layer;
- exact forward whole-day KT02 interval;
- KT05 producer step exactly equal in binary64 to that KT02 interval;
- source inputs finite;
- positive top-layer thickness;
- no singular positive-runoff partition denominator.

Ponding and macropores are rejected.

## Start context and hidden continuation

KT05 supplies the proposed end-side external hydrology values but does not own all beginning-state values used by revision-53 `Hydro_detailed`.

HYDROEXEC01 therefore requires explicit start/configuration coordinates:

- `Pn`;
- `Sic`;
- `Snla`;
- `Mofro(1)`;
- `He(1)`;
- `Lefrrv`;
- `Lefrso`;
- call-entry `Runinu`.

The call-entry `Runinu` requirement is source-derived, not invented. In the revision-53 near-zero runoff branch, `Runinu` is not assigned. Because it is an in/out argument, the branch preserves the caller-provided value.

HYDROEXEC01 makes that hidden continuation explicit and does not replace it with zero.

This is not yet a claim that `Runinu` belongs in canonical ANIMO5 physical state. State ownership/admission remains a separate decision.

## Numerical policy

The source expression order is retained for the bounded equations.

The CI build uses binary64 and disables floating-point contraction/fast-math behavior for this prototype.

No epsilon or balancing correction is introduced.

A source singularity in the positive-runoff partition is rejected fail-closed rather than silently repaired.

## Outputs

HYDROEXEC01 emits:

- `resolved_upper_hydrology_t` for HYDROQ01;
- `tcd042_runoff_load_context_t` for HYDROQ02;
- diagnostics containing the source-resolved runoff split, `Dif`, corrected `Evso`, `Flab(1)` and `Flib(1)`.

Diagnostics are not accepted physical state.

## Not implemented

HYDROEXEC01 does not implement:

- full-profile water-balance qualification;
- lower-layer `Modflux` execution;
- calculation sequence `Sqnu`;
- macropore `Mapohydro`;
- ponding science;
- aggregated hydrology;
- every `Hydro_detailed` output;
- a canonical owner for call-entry `Runinu`;
- production source.

## Governance

This is a bounded cross-module scientific execution candidate and is conservatively Tier D under GOV04.

Same-agent review can qualify the candidate package only as `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Independent Tier D review remains required before admission/composition use.

## Hard boundaries

No B3 mutation.
No TCD re-admission.
No TB7.
No B4.
No production.
No Status A.
No Status AA.
No silent near-zero `Runinu=0` repair.
No full `Hydro_detailed` claim.
