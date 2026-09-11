# TCD-025-A1 restricted water-ledger admission candidate

## Atomic object

`TCD-025-A1` is the water-only public/main macropore ledger correction for selected balance intervals admitted by the B3A10/B3I08 bounded scope.

The inherited interval predicate is deliberately retained unchanged:

`for every active D: (I intersection S_D is empty) OR (S_D subset_of I)`.

For A1 this is a conservative scope boundary inherited from the common parent partition. B3D28 does not infer or admit a wider water-only interval surface.

## Source-owned correction identity

For selected interval `I`, the correction observes only existing revision-53 owners:

- beginning macropore water storage: `sum(Ln in I) SrWaMpCpOld(Ln)`;
- ending macropore water storage: `sum(Ln in I) sum(active D) SrWaMpCp(D,Ln)`;
- signed vertical macropore water transfer crossing the selected interval boundary: source-owned `FlMpVt` with native orientation preserved;
- Main-Bypass direct external drainage over the selected interval: selected-layer sum of `FlMpOuDrMp`;
- `FlMpOuDrSo` is routed through the soil path and is not counted as a second external macropore loss;
- matrix/macropore exchange is internal to the combined public control volume and is not reclassified as an external flux.

The admitted object is the accounting identity that these source-owned terms must be represented in the public water observer for the bounded selected interval. It is not a production implementation or a new hydrological model.

## Expected difference

Only the public/main water ledger/report is expected to change when a later production implementation realizes this admitted identity. Existing water state, macropore transfer fluxes, matrix state, process flux trajectories, timestep acceptance, restart state and numerical policy are unchanged by the scientific admission itself.

No residual-derived flux is admitted. No absolute-value transformation may erase source sign. No second count of `FlMpOuDrSo` is admitted.

## Evidence strength

MP01 directly exercised the frozen specialized water kernel and demonstrated local water conservation for storage, matrix exchange, direct drainage and precipitation/storage probes. B3A10 adds exact-rational observer-level ownership and negative-control oracles. MASSQ03 and B3I08 bound the selected-profile surface. None of this is a historical B2 reference.

Historical revision-53 active-macropore public-ledger behaviour therefore remains unknown. The admissible scientific conclusion is a corrected accounting identity with historical uncertainty, not a claim that revision 53 historically produced this corrected observer result.

## Parent and sibling boundary

Admission of A1 does not admit DOM, N or P siblings and cannot compose the parent. A5 remains an unresolved blocker for the broad selected-profile parent claim. Parent composition requires a later explicit decision.
