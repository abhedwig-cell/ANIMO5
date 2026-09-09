# ANIMO-BUILDQ03 — GHGtransport and GHGtranssub explicit-context probe

Status: `QUALIFIED_CONTROLLED_EXPLICIT_CONTEXT_EQUIVALENCE_GHGASSES_PHASE_CONTEXT_REMAINS_OPEN`

## Scope

This probe closes the runtime-equivalence question for the hidden cross-call context inside `GHGtransport` and `GHGtranssub`. It remains B1 diagnostic evidence under canonical `TCD-011` and does not qualify historical Intel behaviour.

Frozen source identity remains:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Compiler:

`GNU Fortran 14.2.0`

## Diagnostic source-format boundary

Unlike the earlier isolated `GHGponding`, CH4 and N2O probes, this combined transport probe needed a syntax-preserving GNU fixed-form normalization because revision-53 source contains redundant end-of-line ampersands together with column-6 fixed-form continuation, plus source lines longer than 72 columns.

The diagnostic copy therefore:

- removes only redundant trailing continuation ampersands, including ampersands before inline comments;
- keeps column-6 continuation and all executable tokens unchanged;
- uses a minimal `param.inc` carrying the same revision-53 dimension parameter values required by the isolated routines;
- does not change the GHG equations or branch conditions in the legacy-reference variant.

The normalized legacy-reference copy SHA-256 is:

`c6146280c53b6c08890e5ecc5ce22a8374f9350908e674f4e040d72482dfbff0`

This is therefore a controlled source-equivalent diagnostic copy, not byte-exact frozen source.

## 1. GHGtranssub fixed Task-1 coefficient context

The source computes these quantities during Task 1 and reuses them after procedure return during Task 2 while `Reki` and `Reko` are allowed to change:

- `P1`;
- `P2`;
- `Y1`;
- `Y2`;
- `Y3`;
- `Hv`;
- `Hv2`;
- `Hvnil`;
- `AlfBuAv1` for the unsaturated-top branch.

The source comments themselves distinguish this fixed part from the Task-2 part that is dynamic because of `Reki` and `Reko`.

A two-layer controlled case ran Task 1, clobbered automatic local storage, changed `Reki` and `Reko`, and ran Task 2.

Original retained/static-local O0 and O2 execution were identical. Their output SHA-256 was:

`54bb8578d13d1f65ee156c2bb6aa7ec105656d8528178f38a867849d2dbb3e8b`

Original automatic O0 and O2 execution with signalling-NaN local initialization returned NaN for all captured Task-2 average and end concentrations. Their output SHA-256 was:

`f7ee8df3bfe131e05b8119e519c65f5c221f58b018b500ed40196baade9ceca4`

A diagnostic variant threaded the fixed Task-1 context explicitly through the caller. Under automatic O0 and O2 its complete Task-1 and Task-2 output was byte-identical to the retained/static reference, with the same SHA-256 `54bb8578...` above.

Diagnostic explicit-context source SHA-256:

`6adb9df1eee8729a476b18b620074d40aea44648bb404a8d1109411daeb92ae8`

Representative controlled values after the changed Task-2 rates:

- `AvC(1)=2.3228464248963156e-3`;
- `AvC(2)=2.7399690385126168e-3`;
- `RsC(1)=2.2534205328900983e-3`;
- `RsC(2)=2.6836402963722216e-3`.

### Semantic decision

The audited family is fixed within-timestep transport coefficient context, not persistent accepted-boundary physical state.

Qualified owner:

`FIXED_TIMESTEP_TRANSPORT_COEFFICIENT_CONTEXT`

Persistent `ModelState` candidate:

`false`

BUILDQ03 does not claim each member can be independently removed or recomputed. The qualified surface is the explicit context as a group.

## 2. GHGtransport branch and representation-snapshot context

`GHGtransport` itself retains these locals between Task 1 and Task 2:

- `Ln1`;
- `FlTopUns`;
- `Co1Old`.

`Ln1` is exactly derivable as `1-Flpn`. `FlTopUns` is a Task-1 branch classification. `Co1Old` is the pre-iteration top-layer concentration retained because the routine temporarily switches the unsaturated top compartment to an air-based concentration representation and later restores the original water-based representation.

The controlled test deliberately activated the unsaturated-top branch so that the `Co1Old` restoration seam was exercised. The combined source also included the hidden `GHGtranssub` Task-1 coefficient family above.

Original static-local O0 and O2 runs were byte-identical, including warning text and captured state, with SHA-256:

`5ead8015d31cfe0ae58a8a9d3fecb49f5059c31c674c9af2824c0d131f709afc`

Original automatic-local O0 and O2 runs completed but produced NaN throughout the captured Task-2 average/end gas state. Their output SHA-256 was:

`b3f0b2a71608e132a1fe5ac67f1fd42b2f308cef06ca0c0b77bfe3f3678f7d1b`

A diagnostic explicit-context variant threaded through:

- `Ln1`, `FlTopUns`, `Co1Old`;
- the complete qualified `GHGtranssub` fixed Task-1 context.

Under automatic O0 and O2, the explicit-context variant was byte-identical to original static-local O0 and O2 execution. All four reference/candidate outputs have SHA-256:

`5ead8015d31cfe0ae58a8a9d3fecb49f5059c31c674c9af2824c0d131f709afc`

Diagnostic explicit combined source SHA-256:

`63575307aa170187b68b3e20d116c535b02a5d4984c2f88195ad531a5e078f12`

Representative Task-2 captured values:

- restored `Co(1)=1.7000000000000001e-3`;
- `AvCo(1)=8.4815204769146592e-4`;
- `AvCo(2)=1.0368369096376289e-3`;
- `RsCo(1)=8.1509529423486851e-4`;
- `RsCo(2)=1.3505570766009080e-3`.

### Semantic decision

The appropriate owner is explicit gas-transport transaction/solver context. In particular, `Co1Old` is a pre-mutation representation snapshot and must not be inferred from the already-mutated top-layer concentration during Task 2.

Qualified owner:

`GAS_TRANSPORT_BRANCH_AND_REPRESENTATION_SNAPSHOT_CONTEXT`

Persistent `ModelState` candidate:

`false`

## 3. Consequence for TCD-011

This result removes the shared gas-transport family from BUILDQ03's runtime-equivalence open list. Together with the earlier BUILDQ03 probes, controlled explicit-context equivalence is now established for:

- `GHGponding` restore snapshot;
- CH4 oxidation solver context;
- N2O production/reduction and nested correction context;
- `GHGtransport` branch/representation snapshot;
- `GHGtranssub` fixed transport coefficients.

The remaining active GHG hidden-state family not yet runtime-qualified is the top-level `GHGasses` Task-1 to Task-2 hydrology/air-flow projection.

TCD-011 remains open because:

- `GHGasses` phase-context semantics are not yet closed;
- other non-GHG TCD-011 families exist;
- historical Intel project storage semantics remain unknown.

## Gate

`QUALIFIED_CONTROLLED_EXPLICIT_CONTEXT_EQUIVALENCE_FOR_GHG_TRANSPORT_STACK_GHGASSES_PHASE_CONTEXT_OPEN_HISTORICAL_INTEL_OPEN`

`new_canonical_tcd_requested=false`

`corrected_legacy_admitted=false`

`production_migration_admitted=false`
