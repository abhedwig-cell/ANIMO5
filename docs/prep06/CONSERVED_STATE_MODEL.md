# ANIMO-PREP06 conserved-state model

Status: `SOURCE_BOUND_PREPARATORY_EVIDENCE`.

This document separates physical storage, derived state, rate variables and reporting accumulators in the frozen ANIMO 4.1.5 revision-53 source. The detailed machine-readable register is `integration/animo-prep/PREP06_CONSERVED_STATE_INVENTORY.csv`.

Frozen source SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`.

## Classification rule

A variable is classified as physical storage only when the source gives it timestep persistence or restart semantics and a process or balance uses it as mass/water held in a control volume. A concentration can therefore be a physical-state coordinate even when storage is calculated from concentration times water volume, sorption capacity or layer thickness. Variables that merely sum sites, average concentrations, express rates or accumulate output are not promoted to physical storage.

The source already contains an accepted/start versus result/end transaction seam. `Init.for` promotes result variables such as `Mofrt`, `Rsconh`, `Rsconi`, `Rsos`, `Rscopo`, `Rsamcxfa` and `SrWaMp` to the corresponding next-step start state. ANIMO5 should preserve that distinction rather than flattening it during migration.

## Conserved domains

The register contains 53 state or non-state families. The main physical domains are:

- water: canopy interception, snow, ponding/surface representation, matrix water and macropore water;
- organic matter: fresh organic fractions, original humus, exudate-derived humus and exudate material;
- dissolved organic matter: separate labile and stable C/OM, N and P concentration families, with storage including the source-defined instantaneous sorption contribution;
- mineral N: aqueous NH4, separately adsorbed NH4 and aqueous NO3;
- mineral P: aqueous PO4, fast sorption sites, slow sorption sites and precipitated P;
- surface/addition reservoir: top-reservoir NH4, NO3, labile DOM/DON/DOP and PO4, with storage proportional to `Hetop`; stable surface DOM is parser-representable but revision-53 forces it to zero and is therefore retained as dormant rather than active state;
- crop: shoot/root dry matter plus actual plant N and P are persistent plant-compartment states. Potential N/P states are demand/reference state and are not conserved storage;
- GHG: `CsCH4` and `CsN2O` are restartable total soil-system gas concentrations in air plus water. Their `Co*` water concentrations are phase representations derived through the Bunsen partition. The exact revision-53 theory-to-public-ledger reconciliation remains open;
- macropores: water and six dissolved solute families have explicit storage in the specialized macropore solvers, but the main public ledger does not expose the same complete control volume.

## Carbon qualification boundary

The ANIMO 4.0 documentation describes a carbon cycle, but the historical public mass-balance family is principally an organic-matter balance rather than a standalone elemental-carbon ledger. Revision 53 additionally contains explicit CH4-C and CO2-related GHG pathways. PREP06 therefore does not claim that one global elemental-C identity has been qualified. It records the actual OM and GHG state ownership so a later ANIMO5 carbon ledger can be defined without silently equating dry matter, organic matter and elemental C.

## Crop ownership boundary

The soil balances treat nutrient uptake as an outward flux from the soil control volume, while `Upintg_*` increments `Rsamplni_act` and `Rsamplpo_act`. Conversely, crop/root loss routines reduce crop state and feed residues into soil organic material. A future whole-system ledger should therefore contain a plant compartment explicitly. Treating crop uptake only as an external sink would lose a real internal transfer when the control volume includes vegetation.

## Physical state versus ledger observers

`Bawa`, `Bfom`, `Bahu`, `Bdom`, `Banh`, `Bani`, `Bano`, `Bapp` and `Bapo` are reporting/accounting accumulators. `Bafom`, `Bafon` and `Bafop` are detailed process-report accumulators. Neither family is authoritative physical state. This distinction is directly supported by the source: `Outbal_Init` reconstructs beginning storage from the physical variables, while `Outbal_calc` accumulates flux and end-storage terms.

## Known discrepancy mapping

- TCD-014: initial PO4 solution/sorption state can be individually accepted while leaving a profile-level first-step mass-ledger seam. This is an initialization/partition consistency issue, not evidence that any one P state is nonphysical.
- TCD-015: the NO3 negative-concentration branch violates local transport closure through a double-counted moisture-storage derivative.
- TCD-016: surface NH4 dry-down exposes a missing continuation state when water storage vanishes and remaining solute is neither retained nor explicitly exported.
- TCD-017: physical organic-P redistribution is conservative, but the public organic-P ledger omits the top-reservoir side of the transfer.
- TCD-018: interception water is a real state because detailed hydrology includes `Sict-Sic`; the public water ledger interface omits this storage change.
- TCD-019: PO4 sorption stores are physical, while the small-delta constitutive/numerical policy can introduce biased nonclosure.
- TCD-023: stable-DOM P is a separate P state family; its Case(2) partition incorrectly uses an N transfer quantity in two P terms.
- TCD-024: slow-sorption sites are distinct physical P stores and must use site-specific parameters; revision 53 indexes one affinity parameter by nonlinear trial counter rather than site.
- TCD-025: macropore storage belongs in the canonical state model if macropores remain supported.
- TCD-026: initial exudate OM is a real restartable store even though the fresh-OM beginning ledger omits it.
- TCD-027: detailed transfer accumulators are reporting only; the defect changes reporting without changing physical state.

## ANIMO5 ownership constraints

Every conserved store should have one owner, one unit contract and explicit accepted/result state. Internal transfers should carry source and sink state IDs rather than be reconstructed independently in several reporting arrays. Beginning and end storage must be generated from the same state registry. Derived averages, site totals and balance accumulators should remain views. Parser-visible state must not be exposed as supported state unless its timestep evolution is defined and tested.
