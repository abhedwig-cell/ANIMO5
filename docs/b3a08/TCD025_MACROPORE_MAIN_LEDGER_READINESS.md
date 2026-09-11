# TCD-025 macropore main-ledger readiness

Work unit: `ANIMO-B3A08`

Base: `ANIMO-RG05I@94afe7d649a8c60758a41996f0059de0acddd2fc`

## Result before adversarial review

The earlier `WAITING_ON_STATE` reason is partly obsolete. `ANIMO-B3D23@6c9ab83952b53566b878b533c08e3cb10074f399` admits the atomic TCD-031 macropore restart-state correction with historical uncertainty. TCD-025 therefore no longer has to wait on an unspecified macropore solute restart owner.

The remaining ledger problem is real. MP01 source/kernel evidence and MP02 complete-case B1 activation show that macropore storage and Main-Bypass direct drainage are reachable physical state/flux while the public water, DOM, N and P residuals do not consistently contain those terms. No historical active B2 reference exists, so historical magnitude remains unknown.

## Whole-profile identity

For the whole model profile, the correction direction is structurally determinate from existing owners. The macropore subsystem already supplies domain-total beginning/end water storage, accepted/result concentrations for the six dissolved species, and the direct external Main-Bypass drainage. `FlMpOuDrSo` is routed through the soil and must not be counted again as an external macropore loss. The combined matrix plus macropore identity can therefore cancel matrix/macropore exchange internally and add only genuine external macropore transfers.

That is not yet enough to grant a Tier-A waiver.

## Selected-profile control-volume seam

`Outbal_calc.for` does not calculate only one whole-profile balance. Every configured balance uses `Balnmi(Ly)` and `Balnma(Ly)` as an arbitrary layer interval.

The frozen macropore source has a different topology in its saturated part. `MAPOTRANSPORT.FOR` treats the saturated portion of each macropore domain as a domain-level mixed reservoir with one accepted/result concentration. `MAPOHYDRO.FOR` and the hydrology interface do expose layer-resolved macropore water storage, but the transport kernel does not expose a source-owned saturated-domain vertical solute transfer across every possible interior layer boundary.

Therefore a balance interval that cuts through the saturated macropore reservoir does not yet have a source-defined independent solute control-volume boundary flux. Constructing that missing flux as whatever value makes the residual zero would be scientifically invalid because it would turn the observer into its own closure proof.

This is the decisive B3A08 finding. The whole-profile observer correction may remain accounting-only, but the general TCD-025 public-balance claim covers a broader selected-profile surface whose exact state/control-volume semantics have not been qualified.

## GOV04/GOV05 consequence

The B3 queue classification remains `A_ACCOUNTING_REPORTING_ONLY`; B3 class and review risk are separate. Under the strictest-risk rule, unresolved state/control-volume ownership with scientific consequences defeats the Tier-A waiver. The candidate review risk is therefore Tier C.

This does not lower a scientific gate and does not constitute a TCD-025 admission. Under GOV05, a later substantive Tier-C qualification or admission uses mandatory same-agent adversarial review and must never be described as genuinely independent.

## Next work

Open a dedicated TCD-025 selected-profile state/control-volume qualification. It must decide, from source-bound evidence, whether active-macropore public balances are valid only for whole-profile control volumes, whether a source-owned exact selected-profile boundary representation can be reconstructed, or whether an additional observer/state contract is scientifically required.

Only after that question is closed should a TCD-025 B3 admission candidate be frozen.
