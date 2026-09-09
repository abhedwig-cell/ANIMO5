# ANIMO-STATEQ01 NH4 adsorbed-state checkpoint reconstruction qualification

Status: `PASS_FROZEN_SOURCE_COMPONENT_RECONSTRUCTION_CONTINUITY_FULL_MODEL_SPLIT_RUN_OPEN`

Canonical STATE admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## Question

STATEQ01 classifies adsorbed NH4 as real nitrogen storage but proposes not to serialize it as a second independent checkpoint owner if it is deterministically reconstructable from accepted aqueous NH4 and the exact soil/sorption coordinates.

The evidence now consists of a source audit plus two complementary component probes. The stronger probe executes original frozen `TRANSPORT.FOR` together with original `Transsub.for` under the PREP01 deterministic GNU diagnostic build contract. A second isolated seam probe remains useful for checking assignment and balance semantics independently. Neither is a full-model restart qualification.

## Source invariant

Revision 53 initializes soil-layer adsorbed NH4 in `Inicalc.for` as:

```text
Cxnh(Ln) = Rhbd(Ln) * Socfnh(Ln) * He(Ln) * Conh(Ln)
```

The generic transport routine computes the end-of-step adsorbed amount as:

```text
Rscx(Ln) = He(Ln) * Rhbd(Ln) * Socf(Ln) * Rsc
Rsco(Ln) = Rsc
```

For the AMMONIUM call, `Rscx` is `Rscxnh`, `Rsco` is `Rsconh`, and `Socf` is `Socfnh`. Therefore at the completed transport result boundary:

```text
Rscxnh(Ln) = He(Ln) * Rhbd(Ln) * Socfnh(Ln) * Rsconh(Ln)
```

The upper-boundary initialization path in `UBoundconc.for` and management redistribution paths in `Addit.for` restore the same equilibrium relation after they modify current NH4 state. `Init.for` then copies prior accepted `Rscxnh` to current `Cxnh` for ordinary continuation.

A source-wide assignment audit finds no separate process mutation of `Rscxnh` outside the generic transport result and initialization/reset lifecycle. Revision 53 therefore does not provide evidence for an independent accepted-boundary degree of freedom for equilibrium adsorbed NH4.

## Checkpoint consequence

Adsorbed NH4 remains real physical N storage and remains part of the control volume. It need not be a second independently mutable checkpoint owner if restore has the exact inputs needed to reconstruct it:

- accepted `Rsconh` / canonical aqueous NH4 concentration;
- layer thickness `He`;
- dry bulk density `Rhbd`;
- NH4 sorption coefficient `Socfnh`;
- exact layer/layout identity;
- the admitted arithmetic/precision policy.

The candidate reconstruction is:

```text
Cxnh_restored(Ln) = He(Ln) * Rhbd(Ln) * Socfnh(Ln) * Conh_restored(Ln)
```

Reconstruction must occur after exact accepted aqueous state and configuration/layout are bound and before continuation or diagnostics consume adsorbed storage.

## Primary frozen-source component probe

The B0 source archive is fixed at:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

The primary RC-R5 probe executes original frozen:

- `TRANSPORT.FOR` SHA-256 `3f597b896ab5514e0b836f5547b342e317b03c8e3e58e053e113bd1c17e2f998`;
- `Transsub.for` SHA-256 `c548e5d372ffbc7f4d4e4d8d86609cf1f34cf70ea513d345e3c7fada5cf6b552`;
- `Param.inc` SHA-256 `20d85ed8bca9e0060d3b51c2f800ff02fdf0bc3ebb8c834baf4afca870a33475`.

It uses the PREP01 deterministic GNU diagnostic semantics relevant to these units, including eight-byte default REAL/DOUBLE and static local storage. This is diagnostic source-component evidence, not historical Intel/B2 evidence.

The first transport step is nontrivial. Starting from aqueous NH4 `0.010`, the original routines produce:

```text
accepted Rsco = 0.010307667655236559
accepted Rscx = 0.002679993590361505
```

Reconstruction from accepted `Rsco`, `He`, `Rhbd` and `Socfnh` gives exactly the same value within that build:

```text
reconstructed Cx = 0.002679993590361505
```

A second original `TRANSPORT + Transsub` call then gives exact uninterrupted-versus-reconstructed equality within the diagnostic build for:

- end aqueous concentration;
- end adsorbed amount;
- interval-average concentration;
- incoming amount;
- outgoing amount.

The exact final vector for both paths is:

```text
Rsco = 0.010452035544246962
Rscx = 0.00271752924150421
Avco = 0.010380227551667098
Toin = 0.00015
Toou = 0.00010380227551667098
```

The negative sentinel deliberately sets restored `Cx` to zero while leaving accepted aqueous NH4 unchanged. The component's concentration outputs remain the same, but original `TRANSPORT.FOR` reports a mass-balance deviation with `BATR = 0.002680`. This is an important boundary on the interpretation: `Cx/Rscx` is not supported as an independent physical degree of freedom, but its physical adsorbed mass cannot simply disappear from storage accounting.

Primary record:

`integration/animo-state/NH4_ADSORBED_SOURCE_PROBE.json`

Runner and fixture:

- `tools/stateq01/run_rc5_nh4_adsorption_source_probe.py`;
- `tests/stateq01/fixtures/stateq01_rc5_nh4_adsorption_probe.f90`.

## Supplemental isolated seam probe

A separate probe isolates the `Rscx` result/balance seam in original `TRANSPORT.FOR` while replacing `Transsub` by a neutral pass-through and disabling the unreachable macropore call. It confirms exact reconstruction and balance-ledger dependence in both a default-REAL seam build and a REAL8/DOUBLE8 seam build.

This supplemental default-REAL seam result must not be misread as qualification of the complete model under default REAL. PREP01 found the full revision-53 GNU four-byte-default-REAL build unstable because of broader interface/build semantics. The seam probe only establishes local expression and ledger behaviour.

Supplemental record:

`integration/animo-state/NH4_ADSORBED_RECONSTRUCTION_SOURCE_PROBE.json`

Runner and fixture:

- `tools/stateq01/run_rc5_nh4_adsorbed_reconstruction_probe.py`;
- `tests/stateq01/fixtures/stateq01_rc5_nh4_adsorbed_reconstruction_probe.f90`.

## Interpretation boundary

The combined evidence supports the candidate ownership statement more strongly than source inspection alone:

1. accepted `Rscxnh` is deterministically tied to accepted aqueous NH4 and immutable sorption/layout inputs at the exercised boundary;
2. reconstructing it with the same arithmetic semantics reproduces the next original transport component exactly in the PREP01 diagnostic build;
3. omitting the reconstructed adsorbed storage corrupts the original transport storage ledger even though it does not change the exercised aqueous trajectory;
4. therefore `Rscxnh` remains `DERIVED_RECOMPUTABLE_PHYSICAL_STORAGE_VIEW`, not a second independently mutable checkpoint owner and not disposable diagnostic state.

Still open:

- full ANIMO uninterrupted-versus-split continuation on a profile-clean executable route;
- interaction with management and other process ordering at the split;
- canonical serializer precision policy;
- admitted numerical comparison policy for broader trajectories;
- B2 historical-reference qualification;
- canonical STATE admission.

Final classification:

`NH4_ADSORBED_PHYSICAL_STORAGE_DERIVED_RECOMPUTABLE_AT_ACCEPTED_BOUNDARY_SOURCE_AND_COMPONENT_CONTRACT_QUALIFIED`

`RC-R5 = PASS_FROZEN_SOURCE_COMPONENT_RECONSTRUCTION_CONTINUITY_FULL_MODEL_SPLIT_RUN_OPEN`
