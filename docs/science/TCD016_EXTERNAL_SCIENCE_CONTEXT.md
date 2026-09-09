# TCD-016 external scientific context for model-evolution review

Work unit: `ANIMO-SQ01`

Status: `SUPPLEMENTAL_GENERAL_SCIENCE_CONTEXT_NOT_ANIMO_AUTHORITY`

Production migration: `NOT_ADMITTED`

## 1. Purpose and evidence boundary

This note records general scientific context that is useful for reviewing the proposed TCD-016 continuation-state hypothesis.

It is intentionally separated from ANIMO-specific evidence.

The sources below may inform whether a conservative continuation state is a scientifically reasonable model-evolution abstraction. They do **not** establish intended ANIMO 3.x/4.x behaviour, do **not** qualify the legacy `0.1 mm` surface activation boundary as a physical phase threshold, and do **not** supply a missing ANIMO dry-to-wet law.

The controlling ANIMO-SQ01 conclusion therefore remains:

`BLOCKED_TCD016_INSUFFICIENT_THEORY_FOR_CORRECTED_LEGACY_ADMISSION`.

## 2. Evaporation can destroy the concentration coordinate without destroying solute mass

A broad porous-media literature shows that as water evaporates, dissolved salts can become strongly concentrated and can precipitate or crystallize when solubility limits are exceeded. The location and form of retained salt depend on pore geometry, capillarity, wettability and composition.

Examples include the review by Shokri et al. on multi-scale soil salinization and experimental/model studies of evaporation-driven salt precipitation in porous media.

This supports only a generic state-model point:

> when a liquid volume vanishes, a finite nonvolatile solute mass need not vanish with it.

It does **not** show that the residual TCD-016 NH4-N is specifically a crystalline salt, nor that the relevant surface control volume behaves like the saline porous-media systems in those studies.

Implication for Candidate A:

A mass coordinate independent of aqueous volume is scientifically plausible as a conservative representation shell, but its chemical phase identity remains open.

## 3. NH4 can interact strongly with soil solids

Experimental clay-mineral studies show that ammonium adsorption can occur through cation-exchange and related surface processes, and that adsorption varies substantially with mineralogy, pH and concentration.

Representative sources:

- Nommik & Vahtras (1982), *Retention and Fixation of Ammonium and Ammonia in Soils*, Agronomy Monograph 22, DOI `10.2134/agronmonogr22.c4`.
- Applied Clay Science (2018), *Adsorption of ammonium by different natural clay minerals: Characterization, kinetics and adsorption isotherms*, DOI `10.1016/j.clay.2017.11.007`.
- Applied Clay Science (2023), *Environmental effects on ammonium adsorption onto clay minerals: Experimental constraints and applications*, DOI `10.1016/j.clay.2023.107165`.

This general literature makes one SQ01 restriction more important, not less:

`surface aqueous NH4 -> soil sorbed NH4`

cannot be inserted merely as a conservation repair. Such a transfer requires physical contact with a soil-solid owner and an adsorption law whose parameters depend on soil properties.

Therefore the literature does not rehabilitate Candidate B as corrected legacy behaviour.

## 4. NH4-N is not guaranteed to remain chemically inert during a dry interval

Ammonium and ammonia form a coupled acid-base system. Agricultural literature shows that gaseous NH3 loss can depend strongly on pH, temperature, fertilizer form, soil properties, application conditions and water regime.

Representative evidence includes:

- Bouwman et al. (2002), *Estimation of global NH3 volatilization loss from synthetic fertilizers and animal manure applied to arable lands and grasslands*, Global Biogeochemical Cycles, DOI `10.1029/2000GB001389`.
- He et al. (1999), *Ammonia volatilization from different fertilizer sources and effects of temperature and soil pH*, Soil Science 164:750-758.
- Recent reviews of agricultural ammonia volatilization and mitigation likewise identify temperature, pH, moisture/water regime and soil properties as controlling factors.

Consequently, the SQ01 Candidate-A dry-hold rule:

`M_cont,end = M_cont,beg`

must remain interpreted as a **fail-closed model policy when no dry-phase process has been admitted**, not as a scientific claim that real surface NH4 is inert.

If ANIMO5 model evolution later admits volatilization from the continuation state, it must be a separate typed external transfer with an explicit theory basis and parameter domain.

## 5. Drying and rewetting can alter nutrient transformations and fluxes

A meta-analysis of drying-rewetting studies found significant changes in soil N and P pools and process rates, including NH4, nitrification, mineralization, leaching and N2O responses. Effects depend on drying intensity, soil type, ecosystem and experimental setting.

Representative source:

- *Responses of soil nitrogen and phosphorus cycling to drying and rewetting cycles: A meta-analysis*, Soil Biology & Biochemistry 148 (2020) 107896, DOI `10.1016/j.soilbio.2020.107896`.

This argues against treating a universal instantaneous rewetting rule as scientifically self-evident.

The diagnostic SQ01 experiment that instantaneously redissolved all continuation mass was valid only as a mass-conservation/topology demonstration. It is not a qualified kinetic model.

## 6. Consequence for a model-evolution architecture

The external science supports a useful separation of concerns.

### 6.1 Conservation shell

A persistent areic state such as:

`M_surface_NH4_non_aqueous_continuation [kg N m-2]`

can serve as a conservative state owner when the aqueous concentration coordinate ceases to be representable.

Its minimum invariant is mass continuity, not a claim about a specific molecular form.

### 6.2 Process laws around the shell

Physical interpretation should be supplied only through separately qualified transfers, for example:

- continuation -> surface aqueous by dissolution/remobilization;
- continuation -> soil aqueous or soil solid after a justified interface transfer;
- continuation -> atmosphere as NH3 if volatilization theory is admitted;
- continuation -> another chemically identified state if precipitation/fixation theory requires it.

Each transfer needs its own activation variables, units, conservation identity, parameters, observations and restart semantics.

### 6.3 Species-general topology, species-specific chemistry

Because revision-53 surface transport has a shared representation seam across multiple solutes, a generic continuation-state **topology** may be architecturally cleaner than an NH4-only container.

General science does not support giving all species the same phase identity or remobilization kinetics. Species-specific scientific contracts remain necessary.

## 7. What this evidence does not resolve

This external context does not resolve the Class-C gates that remain blocked:

1. intended ANIMO phase identity;
2. intended ANIMO dry-hold chemistry;
3. intended ANIMO rewetting law;
4. physical derivation of the legacy `0.1 mm` activation boundary;
5. physical derivation of `Fu > 1e-6 m d-1`;
6. independent scientific review of the ANIMO5 model-evolution proposal.

Alterra Report 983 remains the highest-value unresolved ANIMO-specific document. Its official WUR record confirms the report and an eDepot target, but the full text could not be retrieved through the available public web path in SQ01. No negative claim is made about uninspected report text.

## 8. Review guidance

The external literature makes the following reviewer disposition scientifically plausible but does not decide it:

`ACCEPT_NONCOMMITTAL_CONSERVATION_STATE_FOR_MODEL_EVOLUTION_WITH_ADDITIONAL_PROCESS_QUALIFICATION`.

The reviewer should reject any inference that the state itself proves crystallization, adsorption, residual-film storage or chemical inertness.

A scientifically disciplined evolution path would therefore be:

`conserved continuation owner first`

followed by:

`separately qualified species-specific phase/process transfers`.

## 9. Final SQ01 significance

General science strengthens the argument that disappearing water is not a valid reason to delete solute mass and that multiple physical fates are possible.

Precisely because multiple fates are possible, it **does not** justify choosing one silently.

Therefore Candidate A is strengthened as a conservative model-evolution abstraction while the corrected-legacy admission remains blocked.

`MODEL_EVOLUTION_HYPOTHESIS = SCIENTIFICALLY_PLAUSIBLE_AS_CONSERVATION_SHELL`

`SPECIFIC_PHASE_AND_PROCESS_LAWS = NOT_QUALIFIED`

`CORRECTED_LEGACY_CANDIDATE = NOT_ESTABLISHED`

`PRODUCTION_MIGRATION = NOT_ADMITTED`
