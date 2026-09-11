# TCD-025 restricted correction readiness

## Qualified upstream constraint

MASSQ03 defines the public interval as `I=[max(1,BALNMI),BALNMA]` and each active saturated macropore mixed reservoir as `S_D=[LnTpMpSr(D),LnBoMp(D)]`.

For dissolved-species accounting, a necessary boundary gate is:

`for every active D: (I intersection S_D is empty) OR (S_D subset_of I)`.

A partial cut through `S_D` is not source-closed and is outside this correction candidate.

## Observer ownership

For water, revision 53 owns accepted/current macropore water storage and layer-resolved vertical macropore water transfer. The restricted observer can therefore use source-owned water storage and boundary transfer without inventing a hydrological residual term.

For dissolved species, the unsaturated transfer chain owns layerwise `TpAm`, while saturated storage is owned as one mixed reservoir per domain. If the public interval encloses the complete saturated reservoir, its old/new species storage can be included as the whole-domain source-owned mass. If the interval excludes the reservoir, no fraction of that reservoir is allocated into the interval. The source-owned unsaturated boundary transfer is used where the interval boundary crosses the unsaturated chain.

Main-Bypass direct drainage `FlMpOuDrMp` is an external loss. `FlMpOuDrSo` is routed through soil and is not added as a second external macropore loss. Matrix/macropore exchange is internal once both physical compartments are represented and must cancel rather than be re-added as an external term.

## Species and public-family mapping

The candidate preserves six source species before aggregation:

- DOM: `DiorMa`;
- DON: `DiorNi`;
- NH4-N: `Nh`;
- NO3-N: `Ni`;
- DOP: `DiorPo`;
- PO4-P: `Po`.

The N public family is the sum of DON, NH4-N and NO3-N after their separate storage and transfer identities are evaluated. The P public family is the sum of DOP and PO4-P after separate evaluation. DOM remains the existing DOM family. No climate-carbon, total-organic-carbon or stoichiometric conversion claim is introduced.

## Units

Macropore water terms are areic water storage/transfer. Dissolved-species storage and transfer are concentration multiplied by areic water storage or water transfer and therefore are areic mass. B3A10 introduces no atomic-weight conversion and no tolerance.

## Exact synthetic oracle

The persisted oracle cases use integer/rational values so equality is exact. They test:

- whole-reservoir storage plus direct-drain closure;
- source-owned unsaturated boundary transfer;
- DON/NH4/NO3 separation and N-family aggregation;
- DOP/PO4 separation and P-family aggregation;
- matrix/macropore exchange cancellation;
- the prohibition on counting `FlMpOuDrSo` as an external loss;
- fail-closed rejection of partial saturated-reservoir cuts.

These are synthetic B1-style algebraic oracles only. They are not B2 historical evidence.

## Readiness consequence

The restricted correction surface can be scientifically specified for intervals satisfying the MASSQ03 boundary predicate. It cannot be promoted directly to an admission of the unrestricted canonical TCD-025 claim, because partial saturated-reservoir cuts remain unsupported. A later routing/scoping work unit must either partition the canonical claim or establish an additional independently owned partial-reservoir observer/state contract before a parent admission can be considered.
