# ANIMO-STATEQ01 NH4 adsorbed-state checkpoint reconstruction qualification

Status: `PASS_FROZEN_SOURCE_COMPONENT_RECONSTRUCTION_DIAGNOSTIC_CONTINUITY_FULL_MODEL_SPLIT_RUN_OPEN`

Canonical STATE admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## Question

STATEQ01 classifies adsorbed NH4 as real nitrogen storage but proposes not to serialize it as a second independent checkpoint owner if it is deterministically reconstructable from accepted aqueous NH4 and the exact soil/sorption coordinates.

This note qualifies the source-level reconstruction contract and adds a hash-pinned execution of the relevant frozen `TRANSPORT.FOR` state/balance seam. It still does not claim portable full-model restart equivalence.

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

The upper-boundary initialization path in `UBoundconc.for` and the management redistribution paths in `Addit.for` restore the same equilibrium relation after they modify current NH4 state. `Init.for` then copies the prior accepted `Rscxnh` to current `Cxnh` for ordinary continuation.

A source-wide assignment audit finds no separate process mutation of `Rscxnh` outside the generic transport result and initialization/reset lifecycle. Thus revision 53 does not provide an independent accepted-boundary degree of freedom for equilibrium adsorbed NH4.

## Checkpoint consequence

For the candidate canonical state, the physical storage contribution remains part of the N control volume, but the checkpoint payload need not carry a second independently mutable NH4 adsorption coordinate if restore has all exact inputs:

- accepted `Rsconh` / canonical aqueous NH4 concentration;
- layer thickness `He`;
- dry bulk density `Rhbd`;
- NH4 sorption coefficient `Socfnh`;
- exact layer/layout identity;
- numerical/precision policy needed to reproduce the multiplication semantics.

The reconstruction rule is:

```text
Cxnh_restored(Ln) = He(Ln) * Rhbd(Ln) * Socfnh(Ln) * Conh_restored(Ln)
```

This must occur after the exact accepted aqueous state and configuration/layout are bound and before any process mutation.

## Frozen-source component execution

The B0 source archive was rechecked at:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

The source probe compiles the original revision-53 `TRANSPORT.FOR` and isolates its adsorbed-state/result and balance-diagnostic seam. `Transsub` is replaced by a neutral pass-through that leaves the aqueous concentration unchanged; `MapoTransport` is an unreachable link stub because macropores are disabled. This is deliberate. The test is about the `Rscx` ownership/reconstruction seam, not about numerical transport-solver qualification.

Two GNU Fortran 14.2.0 builds were executed locally against the hash-pinned archive:

- default REAL with `-O0`;
- default REAL 8 / DOUBLE 8 compatibility with `-O0 -fdefault-real-8 -fdefault-double-8`.

Within each build:

1. original `TRANSPORT.FOR` produced `Rsco` and `Rscx`;
2. uninterrupted continuation used the legacy-equivalent `Cx <- Rscx` handoff;
3. split continuation omitted `Rscx` from the checkpoint and reconstructed `Cx` from `Rsco`, `He`, `Rhbd` and `Socf` using the same source expression;
4. the reconstructed value was exactly equal to the prior `Rscx` within that build;
5. the uninterrupted and reconstructed paths both left the Transport balance diagnostic empty;
6. deliberately replacing the restored `Cx` by zero produced the expected balance-deviation diagnostic.

The execution record is:

`integration/animo-state/NH4_ADSORBED_RECONSTRUCTION_SOURCE_PROBE.json`

Reusable driver:

`tests/stateq01/fixtures/stateq01_rc5_nh4_adsorbed_reconstruction_probe.f90`

Reproduction runner:

`tools/stateq01/run_rc5_nh4_adsorbed_reconstruction_probe.py`

## Interpretation boundary

This adds stronger evidence than the earlier source audit, but the claim must stay narrow.

The probe demonstrates that `Rscxnh` can be omitted as a duplicate checkpoint owner and exactly reconstructed for the exercised source component when the accepted aqueous state and immutable sorption/layout inputs are restored at the same arithmetic policy. It also demonstrates that reconstruction matters for legacy Transport balance diagnostics.

It does **not** show that beginning adsorbed NH4 changes the next aqueous physical trajectory in this routine. In revision-53 `TRANSPORT.FOR`, `Cx` enters the balance check but is not passed into `Transsub`. It therefore would be incorrect to present this probe as full physical trajectory split-run evidence.

Still open:

- full ANIMO uninterrupted-versus-split continuation;
- interaction with management and other process ordering at the split;
- canonical serializer precision policy;
- B2 historical-reference qualification;
- canonical STATE admission.

Final classification:

`NH4_ADSORBED_PHYSICAL_STORAGE_DERIVED_RECOMPUTABLE_AT_ACCEPTED_BOUNDARY_SOURCE_COMPONENT_QUALIFIED`

`RC-R5 = PASS_FROZEN_SOURCE_COMPONENT_RECONSTRUCTION_DIAGNOSTIC_CONTINUITY_FULL_MODEL_SPLIT_RUN_OPEN`
