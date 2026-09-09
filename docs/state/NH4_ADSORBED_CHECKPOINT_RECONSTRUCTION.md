# ANIMO-STATEQ01 NH4 adsorbed-state checkpoint reconstruction qualification

Status: `SOURCE_RECONSTRUCTION_CONTRACT_QUALIFIED_SPLIT_RUN_STILL_OPEN`

Canonical STATE admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## Question

STATEQ01 classifies adsorbed NH4 as real nitrogen storage but proposes not to serialize it as a second independent checkpoint owner if it is deterministically reconstructable from accepted aqueous NH4 and the exact soil/sorption coordinates.

This note qualifies that source-level reconstruction contract. It does not claim portable restart equivalence.

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

## What is not admitted

This source invariant does not by itself prove that a complete uninterrupted trajectory and a split trajectory are equivalent. RC-R5 therefore remains open behaviorally until a split-run or equivalent accepted-boundary replay test demonstrates that reconstruction under the admitted numerical policy reproduces the promised continuation.

Failure of that future test would require reconsidering the checkpoint representation or arithmetic policy. It would not justify silently serializing two independently mutable NH4 owners.

## Reproducible audit

`tools/stateq01/audit_nh4_adsorbed_reconstruction.py` verifies the exact frozen source identity, the required source assignments, and the absence of unexpected direct `Rscxnh` process assignments.

Final classification:

`NH4_ADSORBED_PHYSICAL_STORAGE_DERIVED_RECOMPUTABLE_AT_ACCEPTED_BOUNDARY_SOURCE_CONTRACT_QUALIFIED`

`RC-R5 = PARTIAL_SOURCE_QUALIFICATION_ONLY`
