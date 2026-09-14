# ANIMO-GHG10 — TCD-034 Frozen-Driver Dual-Selector Replay

## Scope

GHG10 consumes `ANIMO-GHG09@31c8ba9a53cb602c7a4a71f501384058ef7be7b2` and owns only the case-bound replay question: does the qualified GHG06A fixed-depth `T50` selector produce materially different plant-growth temperature forcing than the reconstructed revision-53 `Te(Nuroup+1)` selector on a real, frozen multi-year environmental driver trace?

This workunit is evidence-only. It does not modify production source, frozen B0, the canonical TCD register, the central B3 queue, aggregate/routing authority, the central testbank registry, calibration parameters or any testcase input.

## Pinned inputs

The supplied ANIMO testbank archive is pinned by SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

Within that archive, GHG10 uses only the frozen GHGMais driver inputs needed for selector replay:

- `ANIMO_testbank/GHGMais/Input/result.bun`, SHA-256 `cd4202745ee8a9ccd890e6aa6d3f551ff3bb80041efd178aedb3f5f4bbe002e2`;
- `ANIMO_testbank/GHGMais/Input/result_crop_ext.inp`, SHA-256 `075a3a612df2b8745d3eda65eac7c56d6c37eb2beea5b91e4cb6dc1edb526679`;
- `ANIMO_testbank/GHGMais/Input/soil.inp`, SHA-256 `6a07157f64c0913f977487c1719794c1126416646b0b329ce39940935601f760`.

The replay is source-informed by frozen revision-53 `Input_hydro.for`, `root_extern.for` and `ghg_ch4.for`. The relevant facts are: hydrological input provides layer-wise `Flev` and `Te`; external-root `Nuroup` is the deepest layer with `Flev>=1e-7`; the reconstructed current selector after the root loops is `Te(Nuroup+1)` for positive-root states; and the GHG06A model-evolution selector evaluates daily mean soil temperature at fixed depth 0.50 m by adjacent-centre interpolation when layer centres bracket the target.

## Provenance boundary

The GHGMais package is **not** promoted to a revision-53 B2 testcase. PREP01 already established a source/testcase contract lineage mismatch: the supplied textual GHG/organic-matter input grammar does not natively match the supplied revision-53 parser. GHG10 therefore uses `result.bun` and `result_crop_ext.inp` only as a frozen environmental-driver trace.

This is a counterfactual selector replay, not an ANIMO executable replay. It does not assert that either selector produced the supplied historical outputs.

The frozen GHGMais `soil.inp` also has `FvegCH4=0`. Consequently GHG10 does not infer methane flux changes. It quantifies only selector temperature and the directly implied source growth multiplier `fGrow`.

## Replay extraction

The frozen driver covers 3652 daily records from 2010-01-01 through 2019-12-31 with 32 soil compartments. The active-root subset contains 1604 daily records.

For each active-root day:

1. `Nuroup` is reconstructed as the deepest compartment with `Flev>=1e-7`;
2. the current/reconstructed selector is evaluated at `Te(Nuroup+1)`;
3. the corresponding layer-centre depth is recorded;
4. the GHG06A `T50` operator is evaluated at 0.50 m;
5. both temperatures are passed through the unchanged revision-53 growth response with `Tegr=7 degC` and `Temat=Tegr+10 degC`;
6. temperature difference, `fGrow` difference and growth-regime identity are recorded.

The full extracted replay CSV generated during this workunit has SHA-256 `970bdc7b8666ddc30df5427310799efab77239d6cd02d11d92d977a54b45783e`. The repository persists its exact provenance hash, annual aggregates, regime transition matrix and representative replay rows. The full CSV remains an external evidence attachment because the frozen binary testbank itself is not redistributed by this workunit.

## Results

Across the 1604 active-root days, the reconstructed current selector samples layer centres between 0.075 and 0.325 m, while GHG06A targets 0.50 m.

Temperature divergence is material in this driver trace:

- mean absolute difference: 1.158471164 degC;
- median absolute difference: 0.960713760 degC;
- maximum absolute difference: 5.384873259 degC;
- 1210 days have absolute difference >=0.5 degC;
- 767 days have absolute difference >=1 degC;
- 246 days have absolute difference >=2 degC;
- 76 days have absolute difference >=3 degC;
- 17 days have absolute difference >=4 degC;
- 5 days have absolute difference >=5 degC.

The selector difference propagates materially into the non-linear growth response:

- mean absolute `fGrow` difference: 0.278623662;
- maximum absolute `fGrow` difference: 2.487223461;
- 231 of 1604 active days, 14.401496%, change growth-regime classification;
- 196 days change from `MATURE` under the reconstructed current selector to `TRANSITION` under T50;
- 34 days change from `OFF` to `TRANSITION`;
- 1 day changes from `TRANSITION` to `OFF`.

The unweighted active-day sum of `fGrow` is 5315.363443385 for the reconstructed current selector and 5028.789447034 for T50, a difference of -5.391428%. This is **not** a methane-flux result. The sum is retained only as a compact sensitivity descriptor over this specific driver trace. Actual plant-mediated CH4 flux also depends on vegetation activation, roots, storage/phase factors and methane concentration, and `FvegCH4` is zero in the frozen case.

The effect is not confined to one year. Every year from 2010 through 2019 has non-zero selector divergence and growth-response differences. Annual regime-change fractions range from about 5.4% to 24.6% of active-root days.

## Scientific interpretation

GHG10 converts the GHG09 analytic sensitivity warning into direct case evidence. On this frozen ten-year driver trace, replacing `Te(Nuroup+1)` by fixed-depth T50 is not representation-only and not numerically negligible. It changes the forcing presented to the plant-growth response often enough and strongly enough that legacy parameter transfer cannot be presumed safe.

The evidence remains deliberately bounded. One environmental driver trace cannot establish the full intended application envelope, empirical validity or the correct parameterization of the evolved model. It also cannot resolve historical ANIMO selector intent.

## Disposition

The qualified case-bound disposition is:

`QUALIFIED_TCD034_FROZEN_GHGMAIS_DRIVER_DUAL_SELECTOR_REPLAY_CASE_EVIDENCE_V1`

This means:

- material selector divergence is demonstrated on one pinned ten-year driver trace;
- material `fGrow` regime changes are demonstrated;
- GHG09's parameter non-transferability warning is corroborated by case evidence;
- the evidence is not B2, not methane-flux validation, not empirical model validation and not Class-F admission.

## Remaining Class-F gates

After GHG10, `application_envelope_difference` is no longer wholly untested, but it is still not closed. A scientifically defensible Class-F admission still requires broader representative/application-envelope evidence, empirical or observational validation appropriate to plant-mediated CH4 behavior, explicit calibration/parameter consequences, and the required scientific review/admission step. Historical revision-53 selector intent remains unresolved and must stay attached as residual uncertainty.
