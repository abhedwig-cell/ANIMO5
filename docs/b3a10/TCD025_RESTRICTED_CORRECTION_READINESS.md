# TCD-025 restricted correction readiness

## Qualified upstream constraint

MASSQ03 defines the public interval as `I=[max(1,BALNMI),BALNMA]` and each active saturated macropore mixed reservoir as `S_D=[LnTpMpSr(D),LnBoMp(D)]`.

For dissolved-species accounting, a necessary boundary gate is:

`for every active D: (I intersection S_D is empty) OR (S_D subset_of I)`.

A partial cut through `S_D` is not source-closed and is outside this correction candidate.

## Observer ownership

For water, revision 53 owns accepted combined layer storage `SrWaMpCpOld(Ln)` and current domain/layer storage `SrWaMpCp(D,Ln)`. For a selected interval, the source-owned water-storage terms are therefore exactly the old selected sum over `SrWaMpCpOld` and the new selected sum over both domains of `SrWaMpCp`. Source-owned `FlMpVt` crossing the selected upper/lower boundaries supplies the macropore vertical boundary transfer. Its source sign is preserved; no absolute-value or residual reconstruction is allowed.

For dissolved species, the unsaturated transfer chain owns layerwise `TpAm`, while saturated storage is owned as one mixed reservoir per domain. If the public interval encloses the complete saturated reservoir, its old/new species storage can be included as the whole-domain source-owned mass. If the interval excludes the reservoir, no fraction of that mixed reservoir is allocated into the interval. The source-owned signed `TpAm=AvCoML*FlMpVt(next)*St` transfer is used where an admissible interval boundary crosses the unsaturated chain.

Main-Bypass direct drainage `FlMpOuDrMp` is an external loss. For species X the source-owned amount is the selected layer sum of `FlMpOuDrMp(Ln)*AvCoMpX(1)*St`. `FlMpOuDrSo` is routed through soil and is not added as a second external macropore loss. Matrix/macropore exchange is internal once both physical compartments are represented and must cancel rather than be re-added as an external term.

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

Macropore water terms retain the revision-53 areic water basis (`m3 m-2`, dimensionally m). Dissolved-species storage and transfer are concentration multiplied by areic water storage or transfer and therefore are areic mass. B3A10 introduces no atomic-weight conversion and no numerical tolerance.

## Exact synthetic oracle

The persisted oracle cases use integer/rational values so equality is exact. They test whole-reservoir storage plus direct-drain closure, source-owned unsaturated boundary transfer, DON/NH4/NO3 separation and N-family aggregation, DOP/PO4 separation and P-family aggregation, matrix/macropore exchange cancellation, the prohibition on counting `FlMpOuDrSo` as an external loss, and fail-closed rejection of partial saturated-reservoir cuts.

These are synthetic B1-style algebraic oracles only. They are not B2 historical evidence.

## Adversarial precheck and remediation

The first frozen authoring head passed its own CI but the GOV05 adversarial precheck found two weaknesses: the validator proved only that the pinned upstream commits existed rather than mechanically checking the exact B3A08/MASSQ03 decisions it depended on, and the selected-profile water-storage contract was underspecified. The authoring surface was therefore reopened, the upstream semantic checks and exact selected-water ownership were added, and review must restart from the new immutable head. No PASS is inherited from the superseded freeze.

## Readiness consequence

The restricted correction surface can be scientifically specified for intervals satisfying the MASSQ03 boundary predicate. It cannot be promoted directly to an admission of the unrestricted canonical TCD-025 claim, because partial saturated-reservoir cuts remain unsupported. A later routing/scoping work unit must either partition the canonical claim or establish an additional independently owned partial-reservoir observer/state contract before a parent admission can be considered.
