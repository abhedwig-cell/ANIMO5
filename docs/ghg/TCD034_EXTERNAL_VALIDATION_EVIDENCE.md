# ANIMO-GHG11 — TCD-034 External Validation Evidence & Class-F Readiness Acquisition

## Scope

GHG11 consumes the exact green GHG10 authority `ANIMO-GHG10@ad24f3a6dcf2b0a7f4dc1cc9b49e6422f8d36159` and owns only the external scientific-evidence question for the TCD-034 model-evolution pathway.

This workunit does not reinterpret external literature as historical ANIMO evidence. Every external publication is classified as `NEW_MODEL_EVOLUTION_SCIENTIFIC_EVIDENCE_NOT_HISTORICAL_ANIMO_AUTHORITY`.

No production source, frozen B0, canonical TCD register, B3 queue, aggregate/routing authority or central testbank registry is modified. No Class-F, B3 or production admission is performed.

## Evidence question

After GHG06A–GHG10, the remaining problem is no longer whether the fixed-depth selector is mathematically defined or whether changing the selector can matter. Those questions are already bounded. The remaining scientific question is whether available observational and published evidence is sufficient to validate the evolved plant-mediated methane process, including its selector, parameterization and intended application envelope.

## Evidence recovered

### Walter & Heimann process model

Walter and Heimann (2000), DOI `10.1029/1999GB001204`, is the strongest external scientific ancestor identified for the CH4 plant-transport structure. The peer-reviewed model explicitly includes diffusion, plant-mediated transport and ebullition and was tested against observational data at five wetland sites across North America, Europe and Central America. The full text states that the wider evidence base comprised 15 microsites within six wetlands.

For plant-mediated transport the paper uses a rate constant `kp = 0.01 h-1`, equivalent to `0.24 d-1`, a site vegetation factor `Tveg`, a root-distribution factor, a plant-growth factor and methane concentration. A rhizospheric oxidation fraction is applied before atmospheric plant emission. These structural fingerprints strongly match the ANIMO revision-53 plant pathway already reconstructed in GHG05–GHG07.

Appendix B defines the vegetation-growth response from daily mean soil temperature at 50 cm below ground, with minimum and maximum growth-state values 0 and 4, a growth-start temperature of 2 degC in cold regions or 7 degC elsewhere, and maturity at the growth-start temperature plus 10 degC. This is scientific support for the GHG06 conceptual T50 identity, but it does not prove the historical ANIMO discretization rule and does not validate GHG06A's particular layer-centre interpolation operator.

The same paper is also explicit about residual validation needs. It states that more thorough testing would benefit from datasets containing model-internal quantities such as methane production rate, methane oxidation rate and the fraction of methane transported by plants. That is directly relevant to TCD-034: whole-flux agreement alone is not enough to isolate or validate the plant-transport selector.

Sources:

- Walter, B.P. & Heimann, M. (2000), Global Biogeochemical Cycles 14(3), 745–765, DOI `10.1029/1999GB001204`.
- NASA GISS/NTRS metadata and the publisher/Max Planck full text were used to cross-check the bibliographic and process claims.

### SWAP-ANIMO evidence at Zegveld

Hendriks, Wolleswinkel and van den Akker (2007) describe a process-oriented SWAP-ANIMO model for CO2, CH4 and N2O, subsidence and nutrient loading. The WUR record states that the model was calibrated and validated using two experimental peat fields in the Netherlands. The accessible full-text material identifies both fields at the Zegveld experimental farm, with ditchwater levels about 55 and 15 cm below the soil surface and measurements over 2003–2005.

The methods text documents substantial hydrological, temperature and C/N/P observations. It describes SWAP calibration against groundwater, pressure head, water content and soil temperature, followed by ANIMO calibration against C/N/P concentrations. This is meaningful system-level evidence, but the accessible evidence does not isolate the TCD-034 plant-mediated CH4 selector or show a positive selector-specific validation experiment.

Independent observational work at drained Zegveld pasture is especially important for interpreting that limitation. The integrated N2O/CH4 grassland project reports that drained agricultural peat at Zegveld had virtually zero CH4 emission and attributes this partly to the absence of aerenchymatous wetland-plant roots that would connect deeper anaerobic layers to the atmosphere. A 1997 field study similarly reports annual CH4 fluxes near zero for drained Zegveld pasture.

Therefore Zegveld is valuable for hydrology, temperature, carbon/nitrogen and low-CH4 constraints, but it is not by itself a strong positive validation case for the plant-mediated methane pathway targeted by TCD-034.

Sources:

- Hendriks, R.F.A., Wolleswinkel, R. & van den Akker, J.J.H. (2007), *Predicting soil subsidence and greenhouse gas emission in peat soils depending on water management with the SWAP-ANIMO model*, WUR/Carbon in Peatlands proceedings.
- RIVM (2000), *The integrated nitrous oxide and methane grassland project*.
- Langeveld et al. (1997), *Emissions of CO2, CH4 and N2O from pasture on drained peat soils in the Netherlands*.

### Wider model-validation context

The 2012 Dutch integrated GHG synthesis reports that SWAP-ANIMO was applied primarily to plot-scale N2O analyses at managed grassland sites. For CH4 it stresses that detailed water-table and vegetation information is crucial and that CH4 observations contain exchange behavior that remains difficult to capture. This reinforces rather than removes the need for process-specific CH4 validation.

Later methane-model work reusing the Walter-Heimann plant pathway continues to treat the vegetation transport factor as empirical or data-constrained. This supports the GHG09 conclusion that selector evolution cannot be assumed parameter-neutral.

These sources are useful model-evolution evidence. They do not become historical ANIMO authority.

## Readiness assessment

The external literature now supports four positive propositions:

1. fixed-depth soil temperature around 50 cm is an explicit scientific quantity in the Walter-Heimann growth formulation;
2. plant-mediated transport, root distribution, vegetation transport capability and rhizospheric oxidation are empirically motivated process components;
3. the broader process family has been tested across multiple wetland environments;
4. SWAP-ANIMO GHG work has been calibrated/validated in Dutch peat settings at system level.

Those propositions are not sufficient for TCD-034 Class-F admission. The remaining evidence gap is specific: there is no recovered dataset/package that simultaneously identifies the evolved selector input, positive plant-mediated CH4 activation, the relevant plant/root state, observed CH4 flux and enough process-partition information to distinguish the selector from compensating parameter changes.

In particular, the evidence acquired here does not justify carrying `Kpl`, `FvegCH4`, `Tegr` or `PvCH4Ox` unchanged into the evolved selector. It also does not validate GHG06A interpolation as empirically superior to other fixed-depth reconstruction operators.

## Minimum empirical package needed next

A defensible positive validation package should, for at least one plant-mediated-CH4-active site and preferably multiple contrasting sites, include:

- observed or reconstructable daily soil temperature profiles that include/bracket 0.50 m and also permit reconstruction of the legacy root-index selector;
- water table and hydrological state;
- vegetation identity/density, rooting depth or root distribution and phenological state;
- positive methane concentrations and surface CH4 flux time series;
- evidence that plant-mediated transport is materially active, ideally measured or independently constrained pathway fractions and rhizospheric oxidation;
- enough time variation that legacy and T50 selectors become observationally distinguishable rather than nearly collinear;
- calibration/validation separation or other protection against parameter compensation;
- multi-site or otherwise justified envelope coverage if the admission scope is broader than one site.

## Disposition

GHG11 qualifies the evidence inventory as:

`QUALIFIED_TCD034_EXTERNAL_MODEL_EVOLUTION_EVIDENCE_PARTIAL_EMPIRICAL_SUPPORT_CLASS_F_VALIDATION_GAP_REMAINS_V1`

This is a positive qualification of the evidence inventory and a negative admission-readiness conclusion. The evidence materially strengthens the scientific lineage and validation design, but TCD-034 remains `NOT_READY_FOR_CLASS_F_SCIENTIFIC_ADMISSION`.

Historical revision-53 selector intent remains unresolved. No B3 admission and no production migration are authorized.
