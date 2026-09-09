# ANIMO-PREP06 process conservation identities

Status: `SOURCE_BOUND_PREPARATORY_EVIDENCE`.

These identities state what must cancel for a selected control volume. They are not claims that every revision-53 branch already satisfies the identity. Where a known discrepancy violates or incompletely exposes an identity, that is stated explicitly.

## ID-WATER-PROFILE: detailed water profile

For a detailed profile over one timestep:

`external water in - external water out - Δ(matrix water + snow + ponding + interception) = 0`

Internal vertical layer fluxes cancel. If macropores are included in the same profile, macropore storage and direct drainage must also be included. Revision-53 detailed hydrology includes `Sict-Sic`; the public `Bawa` residual does not. This is TCD-018. Macropore extension of the public ledger is incomplete under TCD-025.

## ID-INTERNAL-INTERFACE-CANCEL: adjacent-layer transport

For any conserved species crossing an interface shared by two included layers:

`outflow(layer i) + inflow(layer i+1) = 0`

The sign differs by layer perspective, but the physical transfer is one event. A future ledger should therefore create one typed transfer edge and derive both layer views from it.

## ID-SOLUTE-LAYER: generic dissolved-solute layer

For labile DOM/DON/DOP, NH4 and NO3 in a layer:

`Δstorage = vertical in - vertical out + lateral in - lateral out + process production - process consumption - crop uptake`

where storage includes the source-defined aqueous and, when applicable, sorbed contribution. `TRANSPORT.FOR`/`Transsub.for` are the local solver seam. TCD-015 violates the NO3 identity in the negative-concentration reconstruction branch. TCD-016 exposes that the identity cannot be satisfied through surface dry-down without an explicit continuation state or explicit export.

## ID-SOLUTE-PROFILE: dissolved-solute profile

Summing ID-SOLUTE-LAYER over all included layers cancels internal vertical interfaces. Remaining terms are top/bottom boundary exchange, lateral drainage/infiltration, runoff/runon/irrigation, process conversion, uptake and total storage change.

## ID-MATERIAL-ADDITION: fertilizer/manure/deposition

For a management addition:

`material amount × species composition = retained state addition + explicitly external loss`

For NH4-containing material the explicit volatilized fraction belongs on the external-loss side. Organic solid, dissolved organic and mineral fractions must each map to their own species state. This identity is about composition bookkeeping, not about subsequent transformation.

## ID-CROP-N and ID-CROP-P: soil-to-plant uptake

For a whole soil+plant control volume:

`soil mineral nutrient loss = plant actual nutrient-state gain`

For the soil-only public balance the same transfer is an external crop-uptake sink. `Upintg_Plant`, `Upintg_Grass` and `Upintg_Extern` explicitly add realized uptake to `Rsamplni_act` and `Rsamplpo_act`, which supports treating crop N/P as physical state rather than reporting only.

## ID-CROP-RESIDUE, ID-CROP-HARVEST and ID-CROP-GRAZING

Root death and modeled crop-loss fractions are internal when both crop and soil are inside the control volume:

`crop state loss = soil residue gain + external removal`

For harvest, the modeled residue fraction `Osha` returns to soil material and the remainder of yield is external export. For grazing, `Osgr` is the modeled returned/lost fraction and the remaining consumed biomass is external unless another management return explicitly represents it. A future ledger should not infer these remainders from a soil-only balance.

## ID-REDISTRIBUTION: ploughing/mixing

For an encompassing profile:

`Σ source-store losses + Σ destination-store gains = 0`

No mass is created by redistribution. TCD-017 is a public organic-P ledger defect because `Addit` tracks both top-reservoir loss and soil gain, while `Bapo(Redi)` omits the top term. The physical state trajectory is not the defect.

## ID-ORG-TRANSFORM: organic-pool transformations

For each conserved quantity represented by a transformation branch:

`source organic-pool loss = gains to other organic pools + mineral release - mineral immobilization + external gaseous/mineral products as applicable`

The same event should have independent C/OM, N and P quantities derived from the appropriate species composition. Detailed transformation arrays are evidence/report views, not separate stores.

## ID-STABLE-DOM-P: stable-DOM phosphorus partition

Within the stable-DOM P branch:

`transformed P = P assimilated to humus + P released to mineral/other P sinks`

Every term on the right must be computed from a phosphorus transfer quantity. TCD-023 violates this species identity because two `Transfop` partition terms use `Transfon17` in Case(2).

## ID-N-MINERALIZATION and ID-P-MINERALIZATION

For positive net mineralization:

`organic nutrient loss = mineral nutrient gain`

For immobilization the direction reverses:

`mineral nutrient loss = organic nutrient gain`

`Tomnni` and `Tomnpo` are rate/step-transfer variables, not stores. Their sign selects the direction. TCD-023 can perturb the P side because it feeds the phosphorus transformation partition.

## ID-NITRIFICATION

Without an explicit gaseous partition:

`NH4-N loss = NO3-N gain`

With the GHG option active:

`NH4-N loss = NO3-N gain + N2O-N production`

The topology is source-supported. PREP06 does not independently qualify the exact revision-53 GHG coefficient/theory contract.

## ID-DENITRIFICATION

`NO3-N loss = N2-N export + N2O-N production/export/state change`

The split depends on the active denitrification/GHG formulation. This is an external loss from a soil-mineral-N control volume and a transfer into explicit gas state when N2O is retained before emission.

## ID-P-SORPTION: mineral-P phase system

For a layer, excluding external transport and biological source/sink terms:

`Δ(PO4 aqueous + fast sorbed + slow sorbed + precipitated P) = 0`

Sorption/desorption and precipitation/dissolution are internal phase transfers. TCD-019 shows that a local tangent substituted for an exact finite secant can bias this identity over many small steps. TCD-024 shows that slow-site kinetics can use the wrong parameter index. These are different defects and require different qualification.

## ID-P-INITIAL: initial P partition

A purely representational initialization/projection must satisfy:

`P total before projection = P total after projection`

TCD-014 shows that revision-53 per-layer acceptance thresholds can allow small inconsistencies that accumulate into a material profile-level first-step residual. PREP06 records the state/ledger seam without changing the frozen input or initialization policy.

## ID-DRYDOWN: vanishing liquid storage

When aqueous storage goes to zero:

`old dissolved mass = explicit outflow + alternate retained-state mass + transformed mass`

Setting concentration to zero is not itself a mass sink. TCD-016 demonstrates a reachable branch where remaining NH4 mass is zeroed while the tiny positive outflow is below the export threshold and no alternate dry-solute state exists.

## ID-MACROPORE-WATER

The specialized macropore water identity is source-explicit:

`macropore inflow + old storage = macropore outflow + new storage`

with matrix exchange internal to a combined matrix+macropore profile and direct drainage external. `MAPOHYDRO` evaluates this closure. TCD-025 concerns the main public ledger interface, not the existence of the specialized identity.

## ID-MACROPORE-SOLUTE

For each macropore dissolved species:

`solute inflow + SrWaMpOld × CoMp = solute outflow + SrWaMp × RsCoMp`

`MAPOTRANSPORT` evaluates this storage-aware balance. The main public balance route does not receive all required macropore storage state and does not integrate `Dra4` consistently across families, which is TCD-025.

## ID-REPORT-ACCUM: reporting-only accumulators

For a report accumulator:

`new accumulator(slot) = old accumulator(same slot) + current transfer contribution`

This is not a physical conservation equation, but it is a ledger-integrity identity. TCD-027 violates it for organic-P slot 24 by seeding from slot 25. Because the physical state and total balance do not change, this confirms the accumulator is reporting-only.

## Elemental-C limitation

No new claim is made that revision 53 has a single qualified elemental-carbon closure across OM, crop dry matter, CO2 and CH4. The source and ANIMO 4.0 documentation are sufficient to map the relevant stores and transfers, but not to equate all historical OM/dry-matter quantities with elemental C without an explicit conversion/theory contract. ANIMO5 should make that conversion contract explicit before a canonical C ledger is admitted.
