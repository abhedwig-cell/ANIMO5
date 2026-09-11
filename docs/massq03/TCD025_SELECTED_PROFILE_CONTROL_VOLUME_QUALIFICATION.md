# ANIMO-MASSQ03 — TCD-025 selected-profile macropore control-volume qualification

Base authority: `ANIMO-RG05J@624bbad35add93de29ac89649155d9fa086a73af`

Consumed readiness authority: `ANIMO-B3A08@7a7309e913e8216a20ac134539470e3e5eb4302f`

## Question

TCD-025 concerns missing macropore terms in the public/main water and C/N/P balance observers. B3A08 established that a whole-profile macropore correction direction is structurally determinate, but that public balances can use arbitrary `BALNMI..BALNMA` layer intervals. The remaining Tier-C question is whether an interval that intersects active macropores has an independently source-owned control-volume boundary representation.

This work unit qualifies only that control-volume question. It does not implement a correction and does not perform B3 admission.

## Revision-53 source reconstruction

`Outbal_calc.for:229-230` assigns each public balance its own `Ln1 = Balnmi(Ly)` and `Ln2 = Balnma(Ly)`. The public balance surface is therefore not inherently whole-profile.

For each active macropore domain `D`, `MAPOHYDRO.FOR:71-116` determines the active bottom `LnBoMp(D)` and the top of stored macropore water `LnTpMpSr(D)`. The interval

`S_D = [LnTpMpSr(D), LnBoMp(D)]`

is the stored/saturated part used by the macropore transport routine.

In the unsaturated part, `MAPOTRANSPORT.FOR:470-490` propagates transported species mass layer by layer. The crossing amount is explicitly source-owned as

`TpAm(D) = AvCoML(D,Ln) * FlMpVt(D,Ln+1) * St`.

A boundary within that unsaturated chain therefore has a source-defined transported-mass term.

The saturated part is different. `MAPOTRANSPORT.FOR:494-533` aggregates all inflow and outflow over `S_D` and solves one domain-level mixed reservoir using `SrWaMp(D)`, `SrWaMpOld(D)`, `CoMp(D)`, `AvCoMp(D)` and `RsCoMp(D)`. Lines 540-542 assign the same domain-average `AvCoMp(D)` to every layer in `S_D`; they do not create an internal layer-to-layer species transfer. The source-level mass check at lines 637-659 also closes only the domain-total stored mass `SrWaMp*RsCoMp` against domain-total inputs and outputs.

`Init.for:505-529` reinforces that ownership: beginning/end solute concentration state is stored per macropore domain, whereas the retained layer-resolved old water storage is only a combined water geometry quantity. It is not a layer-resolved persistent species-mass state.

## Qualified boundary-admissibility predicate

Let the soil-layer part of a public balance interval be

`I = [max(1, BALNMI), BALNMA]`.

For each active macropore domain `D`, the selected interval satisfies the saturated-reservoir boundary admissibility condition only when

`I ∩ S_D = ∅`  **or**  `S_D ⊆ I`.

Equivalently: a public balance may fully exclude or fully enclose each active saturated macropore reservoir. It may not cut through only part of `S_D` if the observer claims exact source-owned species conservation.

This predicate is a necessary control-volume condition, not a sufficient proof that every other public-balance term is already complete. In particular, MASSQ03 does not promote a candidate observer correction to B3 readiness.

## Why a partial saturated-reservoir cut fails closed

If `I` contains only part of `S_D`, revision-53 owns one mixed concentration and one total stored species mass for the whole reservoir. It does not own a species transfer across the artificial internal layer boundary introduced by the reporting interval. Multiplying the mixed concentration by selected layer water storage can allocate mass geometrically, but it still does not independently determine the transported species amount across that artificial boundary with a source-owned timing and sign contract.

Defining the missing crossing term as the value needed to close the selected residual is forbidden. That would make the observer the source of its own conservation proof.

The result is therefore scientific non-closure of that selected reporting control volume, not merely missing output plumbing.

## Water versus species scope

The decisive negative result is established for the dissolved-species ledgers. That alone is sufficient to reject a universal exact TCD-025 claim over arbitrary public balance intervals. MASSQ03 intentionally does not claim that every water-only partial-reservoir interval is impossible to reconstruct, because revision-53 also carries layer-resolved macropore water geometry. Any broader water theorem would require its own independently owned internal saturated-flow contract.

## Consequence for TCD-025

The general TCD-025 public-balance surface cannot be certified as an exact accounting-only observer over arbitrary `BALNMI..BALNMA` intervals. A later correction/readiness work unit has two scientifically legitimate choices:

1. restrict its exact claim to intervals satisfying the qualified boundary-admissibility predicate and then prove the remaining observer terms; or
2. introduce and separately qualify a new state/observer contract that defines partial saturated-reservoir control volumes without using the residual as its own oracle.

MASSQ03 chooses neither production policy. It only qualifies the boundary semantics.

Historical active-case magnitude remains unknown without B2 evidence. No production source, canonical TCD register, B3 admission, B4 surface, numerical tolerance, solver policy or persistent-state design is changed here.
