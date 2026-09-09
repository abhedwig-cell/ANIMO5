# ANIMO-UBQ03 - HETOP zero-thickness upper-reservoir domain characterization

Status: `QUALIFIED_CHARACTERIZATION_HETOP_ZERO_PARSER_ADMISSIBLE_CONDITIONALLY_UNDEFINED_NO_GLOBAL_ZERO_THICKNESS_POLICY`

This work unit characterizes the exact-zero `HETOP` domain exposed by B3B02 and B3E01. It does not change input validation, production source, TCD routing or scientific admission.

## Input and documentation contract

The frozen revision-53 parser reads `Hetop` in `input1.for:1826-1829` and validates it on `[0.0, 0.2]`. `Checkrea` rejects only values strictly below or above the bounds, so `Hetop=0` is accepted.

The ANIMO 4.0 user's guide gives the same range `[0.0 ... 0.2] m` and describes `HETOP` as the thickness of the virtual reservoir from which fertilizer additions leach proportional to cumulative precipitation. No special computational semantics for exactly zero thickness were identified in the reviewed HETOP definition and reservoir description.

The existing frozen testbank does not exercise that lower endpoint. Nine SOIL.INP files were checked and all use `Hetop=0.02 m`.

## Frozen-source division inventory

The hash-pinned revision-53 source contains nine direct divisions by `hetop` in four process files:

- `Addit.for:361,363,365,367`, when material is assigned to the top addition reservoir;
- `UBoundconc.for:114`, for no-ponding flow with `Flux >= 1.0d-8`;
- `Uptpar_Grass.for:92,194`, in uptake coupling with reservoir inflow;
- `Uptpar_Plant.for:110,283`, in analogous plant-uptake calculations.

No zero-thickness guard was found around these division contracts. The main call order is `Addit -> UBoundconc -> uptake parameters`, so a zero-thickness configuration may encounter the singular representation at several distinct points depending on management and crop options.

This does not prove that every possible `Hetop=0` execution fails. Several paths are conditional. It does prove that zero is admitted by the input contract while no general zero-capacity reservoir semantics are implemented across the production paths that own `HETOP`.

## Important distinction inside UBoundconc

The `TCD-042` subthreshold fallback itself is not the source of a division at every zero-thickness event.

For `Flpn=0`:

- `Flux >= 1.0d-8` executes `P=St*Flux/Hetop` and is singular at `Hetop=0`;
- `0 < Flux < 1.0d-8` uses the legacy fallback `A1=1, A2=0, B1=1, B2=0`, so this particular code path avoids division;
- `Flux=0` uses that same fallback and also avoids division in `UBoundconc` itself.

The finite-positive E1 problem therefore must not be described as an existing revision-53 divide-by-zero defect inside its legacy fallback. The issue is different: the NQ03 corrected E1 representation uses `P=St*Flux/Hetop`, while the raw canonical E1 trigger inherited from B3I05 does not exclude the parser-admissible zero-thickness domain. Other runtime paths can also divide by `Hetop` independently.

Likewise, the B1 positive-`Hetop` exact-zero limit remains mathematically valid for `Hetop>0`, but it has no finite continuation to a loaded reservoir of exactly zero capacity.

## Consequence for B1 and E1

UBQ03 does not invalidate either previously qualified positive-thickness result:

- TCD-042-B1 remains a qualified exact-zero correction hypothesis on `Hetop>0`;
- TCD-042-E1 retains the independently reviewed NQ03 numerical policy on its declared positive-`Hetop` natural envelope.

It does block silent widening of either policy to the complete parser-level domain. Neither adding `Hetop>0` as a production guard nor changing the SOIL.INP lower bound is authorized here. Either action would define new input/runtime behavior and needs an explicit qualification route.

## Runtime evidence boundary

A historical B2 execution at `Hetop=0` is not available. The recovered Intel project contract makes floating-point exception handling relevant, but the exact historical executable/runtime is not qualified. UBQ03 therefore does not claim a specific historical outcome such as crash, infinity or NaN.

The source-level conclusion is narrower and stronger: revision-53 admits `Hetop=0`, multiple reachable scientific paths divide by `Hetop`, and no source-wide zero-thickness policy or guard is defined.

## Decision

`QUALIFIED_CHARACTERIZATION_HETOP_ZERO_PARSER_ADMISSIBLE_CONDITIONALLY_UNDEFINED_NO_GLOBAL_ZERO_THICKNESS_POLICY`

This is a characterization, not a correction admission. No new top-level TCD is reserved. The result should feed a later input-domain/runtime-contract intake if the program wants to decide whether zero must be rejected, given separate semantics, or represented by another reservoir formulation.
