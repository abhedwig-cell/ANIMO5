# ANIMO-GHG01 — CH4 production, substrate partition and initialization reconciliation

Status: `CH4_TOTAL_PRODUCTION_FORMULATION_SUPPORTED_PARTITION_NONCLOSURE_CONFIRMED_SOURCE_INDEX_CANDIDATE_IDENTIFIED`

This post-closeout note deepens the revision-53 methane audit without creating a production correction, translating GHGMais, or claiming historical executable behaviour.

Frozen source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Rechecked source-file SHA-256 identities:

- `ghg_ch4.for`: `00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98`;
- `Inicalc.for`: `306dd3be262a9eaa293520c754190931bc54e76e7d84b3145efe5663a3e523e1`;
- `Rates.for`: `7a1a8aee4715d85b9b7e9e172f83756e4aee8b8278386c804210ef77dc2a857a`;
- `ghgasses.for`: `4bf5906f571a586d4312d8e7b0d57f6df3b4b6c2073410335616f3d3c042da93`.

## 1. Independent and version-near evidence boundary

Walter & Heimann (2000) independently supports the broad wetland-methane process classes used by ANIMO: substrate-dependent methanogenesis, oxidation, diffusion, plant transport and ebullition.

A 2012 Wageningen MSc thesis by Victoria Naipal, *Analysis of lake methane emissions using Open Path Wavelength Modulation Spectroscopy (WMS) and eddy covariance observations*, provides version-near secondary documentation of the SWAP-ANIMO methane production relation. It explicitly states that ANIMO uses the Walter & Heimann production form, linearly related to substrate availability, and reproduces the temperature and pH response relations. It also describes the methanogenic organic-matter pool construction as based on DOM plus other pools weighted by their respective decomposition rates, with a labile/resistant transition at `0.82e-3 d-1`.

This MSc thesis is useful corroborating documentation but is not treated as a revision-53 release specification or as equivalent to peer-reviewed primary model documentation. Exact revision-53 CH4 kinetics therefore remain only partly independently qualified.

## 2. Revision-53 total CH4 production relation

`ghg_ch4.for::CH4produc` states that methanogenesis follows Walter & Heimann (2000), depending on organic-matter quality, temperature and pH.

For a layer define:

- `A = 1 - Rdfaox`, the anaerobic fraction used by the routine;
- `S_i`, the pre-aeration methanogenic substrate contribution from each DOM/exudate/humus/fresh-OM source family;
- `S = sum(S_i)`;
- `E = RdfapH * CrfaTe * R0CH4pr`.

The routine first constructs `S`, then applies:

`OmSubCH4 = A * S`

and calculates:

`QPrCH4 = E * OmSubCH4 = E * A * S`.

Source response functions are:

- temperature, for `Te > 0`: `CrfaTe = 5**((Te-Terf)/10)`;
- temperature, for `Te <= 0`: zero production factor;
- pH for `3.3 <= pH < 10`: `RdfapH = -0.09*pH^2 + 1.195*pH - 2.965`;
- pH outside that interval: zero production factor.

The Naipal 2012 SWAP-ANIMO description independently reproduces the same production-factor form and the same pH polynomial. It presents the temperature relation in generic Q10 form, so the exact hard-coded revision-53 value `Q10=5` is not promoted here beyond source-specific authority unless a stronger parameter source is recovered.

Qualification:

- substrate-linear methane production class: `INDEPENDENT_THEORY`;
- ANIMO pH response polynomial: `VERSION_NEAR_SECONDARY_DOCUMENTATION_SUPPORTED_SOURCE_RELATION`;
- exact revision-53 hard-coded Q10 value 5: `SOURCE_ONLY` in this work unit.

## 3. Source-confirmed CH4 production-component nonclosure

After calculating total `QPrCH4`, revision 53 allocates production back to source pools as:

`QPrCH4_i = QPrCH4 * S_i / OmSubCH4`.

But `OmSubCH4` has already been multiplied by `A`, while each numerator `S_i` has not.

Substitution gives:

`QPrCH4_i = (E*A*S) * S_i/(A*S) = E*S_i`.

Therefore:

`sum_i(QPrCH4_i) = E*S = QPrCH4/A`.

Consequences:

- if `A = 1`, component production closes to total production;
- if `0 < A < 1`, the component sum exceeds total CH4 production by the exact factor `1/A`;
- the absolute component-total discrepancy is `E*S*(1-A)`;
- if `S = 0` while the routine passes the anaerobic-fraction early return, the component expressions contain a zero denominator and a `0/0` numerical-domain risk.

This is an internal source algebra result. It does not depend on historical output or on interpreting a documentation equation.

Classification:

`SOURCE_CONFIRMED_CH4_PRODUCTION_COMPONENT_PARTITION_NONCLOSURE`

Local reconciliation key:

`GHG01-LCL-CH4-PRODUCTION-COMPONENT-PARTITION`

## 4. Why the partition nonclosure matters to the C ledger

The component arrays are not diagnostic-only quantities.

`Rates.for::Rates2` actively uses `QPrCH4Do(Ln)` to construct a zero-order dissolved-organic-matter sink when `IoptGHG>=1`. Thus the DOM source-pool depletion path is driven by a component rate that, for partial anaerobiosis, is not the corresponding fraction of the total CH4 production after anaerobic scaling.

The inactive `GHG_Miner` routine likewise converts `QPrCH4Do`, `QPrCH4Ex`, `QPrCH4Hu` and `QPrCH4Os` into methanogenesis source-pool mineralisation terms. If that intended routine were activated unchanged, the same partition nonclosure would propagate into all source-family depletion terms.

This sharpens the earlier GHG ledger finding. The legacy source has two distinct problems:

1. the comprehensive source-pool transfer path is inactive for exudate, humus and fresh organic matter;
2. the production-component rates supplied to source-pool accounting do not sum to the gas-production rate whenever the anaerobic fraction is strictly between zero and one.

These findings must not be merged conceptually. Reactivating `GHG_Miner` alone would not establish conservation.

## 5. Fresh-organic-matter methanogenic weighting index candidate

`Inicalc.for` constructs `FOmCH4Os(Fn)` for each fresh-organic-matter fraction. The loop is:

```text
Do Fn = 1, Nf
   If (Recfav(Nf).Gt.0.00082) then
      FOmCH4Os(Fn) = (1-Asfa(Fn))*Recfav(Fn)/KrefDom
   Else
      FOmCH4Os(Fn) = ((1-Asfa(Fn))*Recfav(Fn)/KrefDom)**Rp
   Endif
Enddo
```

The branch selector uses `Recfav(Nf)`, the final defined fraction, while the calculated weight uses `Recfav(Fn)`, the current fraction.

This means one fraction's decomposition rate selects the linear-versus-power weighting rule for every fraction. The code is in bounds and therefore need not fail visibly.

The Naipal 2012 description states that labile and resistant organic-matter pools are distinguished using the decomposition-rate threshold and that the different pools are expressed relative to DOM using their respective decomposition rates. That description is more consistent with a per-fraction selector than with a global selector based on the last fraction, but it is secondary documentation and does not by itself prove a revision-53 typo.

Classification:

`SOURCE_CONFIRMED_CROSS_FRACTION_INDEX_DEPENDENCE_WRONG_INDEX_CANDIDATE_REFERENCE_UNEXERCISED`

Local reconciliation key:

`GHG01-LCL-CH4-FRESH-OM-WEIGHTING-INDEX`

Required closure before any correction:

- recover the detailed Hendriks ANIMO GHG derivation or source history;
- compare with an earlier/later source revision if provenance can be established;
- use a revision-53-compatible activated GHG case containing fresh-OM fractions on both sides of the `0.00082 d-1` threshold;
- separately test the current `Recfav(Nf)` selector and a diagnostic `Recfav(Fn)` counterfactual without promoting the latter to historical evidence.

## 6. Qualification consequence

The methane qualification is now more specific than the previous broad `SOURCE_ONLY` label for exact kinetics.

The total CH4 production structure and pH response have version-near documentary support, but the frozen source contains a source-internal component-partition nonclosure that directly reaches active DOM depletion. A separate initialization indexing construct can make all fresh-OM methanogenic weights depend on the last fraction's decomposition-rate class.

These are not historical behaviour claims because the supplied GHGMais case still does not reach the revision-53 GHG process branch and no qualified historical runner is available.

No production migration or B3 admission is permitted from this note.
