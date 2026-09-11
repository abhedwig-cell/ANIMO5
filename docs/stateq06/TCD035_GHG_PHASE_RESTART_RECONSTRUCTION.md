# ANIMO-STATEQ06 — TCD-035 GHG restart phase reconstruction qualification

## Question

Can the revision-53 GHG restart phase discontinuity be resolved without adding a new physical gas state?

## Frozen-source semantics

Revision 53 serializes the accepted total gas-water system concentrations `RsCsCH4(0:Nl)` and `RsCsN2O(0:Nl)` to `INITIAL.OUT`. The active dissolved concentrations `CoCH4` and `CoN2O` are phase views derived from total system concentration, water-filled porosity, saturated porosity and the reciprocal Bunsen coefficient.

For a soil layer the source relation is:

`Co = Cs / (theta + r(T) * (theta_sat - theta))`

where `r(T) = 1 / AlfaBunsen(gas,T)`.

`AlfaBunsen` is source-defined from Sander-style Henry-law parameters. Revision 53 uses `KH_O=0.00134, ESdvR=1750` for CH4 and `KH_O=0.0245, ESdvR=2600` for N2O, with thermodynamic temperature clamped at 273.15 K.

The restart initialization in `Inicalc.for` reconstructs the soil-layer phase view using `Terf`, not the accepted checkpoint temperature coordinate. GHG01 therefore established a source-confirmed restart phase reconstruction discontinuity whenever the accepted checkpoint phase ratio differs from the reference-temperature ratio.

## Qualified ownership rule

For TCD-035 soil layers `1..Nl`:

- `Cs` is the accepted checkpoint GHG owner coordinate;
- `Co` is a derived aqueous phase view and is not a second independent checkpoint owner;
- exact restart reconstruction requires the accepted checkpoint hydrology coordinate (`theta`, `theta_sat`) and accepted checkpoint temperature `T_checkpoint`;
- the source Bunsen relation is then used with `T_checkpoint`;
- use of `Terf` is not an equivalent reconstruction except under the source-derived exact continuity conditions.

The exact equality conditions are:

1. `r(T_checkpoint) == r(Terf)`;
2. `theta_sat - theta == 0` (no gas-filled pore volume);
3. `Cs == 0`.

This workunit does not qualify a generic temperature model. It consumes the existing checkpoint-sufficiency rule that future-influencing thermodynamic state must be rebound/restored exactly.

## Executable oracle

The STATEQ06 oracle spans both gases, multiple nonzero total concentrations, unsaturated/saturated water states, checkpoint temperatures and reference temperatures. It verifies:

- exact reconstruction from accepted checkpoint coordinates reproduces the continuous phase view;
- the revision-53 `Terf` reconstruction is detectably different in unsaturated nonzero-gas cases when the Bunsen ratio differs;
- saturated, zero-gas and equal-ratio controls collapse to the exact equality conditions;
- CH4 and N2O use their own source coefficients and are never interchanged.

The oracle is source-derived B1 evidence, not B2 and not a whole-model split-run baseline.

## Classification consequence

The prior queue label for TCD-035 was `C provisional` while checkpoint phase ownership/reconstruction was unresolved. STATEQ06 resolves the bounded soil-layer owner model without adding, splitting or redefining a physical storage. The owner is already the serialized total-system `Cs`; `Co` is deterministically derived from accepted checkpoint coordinates.

A later readiness workunit may therefore assess a bounded local restart-reconstruction correction under Class B, while retaining Tier-C review risk because restart semantics alter future trajectories. STATEQ06 itself performs no B3 admission.

## Excluded scope

- layer0/ponding GHG restart continuity, which remains TCD-036;
- GHG hidden within-timestep solver/context state from BUILDQ03;
- TCD-032, TCD-033 or TCD-034;
- continuous-run Bunsen update policy beyond the restart boundary;
- canonical STATE admission;
- checkpoint serialization format migration;
- whole-model GHG split-run equivalence;
- historical revision-53 magnitude;
- production source changes, B4 or production migration.

Historical behavior remains `UNKNOWN_WITHOUT_B2`.
