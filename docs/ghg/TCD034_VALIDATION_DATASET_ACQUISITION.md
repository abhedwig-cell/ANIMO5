# ANIMO-GHG12 — TCD-034 Validation Dataset Acquisition & Joinability Readiness

## Scope

GHG12 starts from the exact green GHG11 authority `ANIMO-GHG11@98782bfa332aae0073d0686ad0261571a991a057` and owns only the validation-dataset acquisition/readiness question for the TCD-034 model-evolution path.

It does not perform model calibration, Class-F admission, B3 admission or production migration. It does not modify production source, frozen B0, the canonical register, the central queue, aggregate/routing authority or the central testbank registry.

All external datasets remain `NEW_MODEL_EVOLUTION_SCIENTIFIC_EVIDENCE_NOT_HISTORICAL_ANIMO_AUTHORITY`.

## Why a separate acquisition workunit is needed

GHG11 established that the literature supports the scientific lineage but does not yet provide a process-resolved validation package that identifies the evolved T50 selector independently of compensating plant-transport parameters. GHG12 therefore asks a narrower question: are public datasets now available that could support such a validation, and what remains before they can be used as admissible evidence?

## Strongest candidate: SPRUCE S1 Bog

The strongest public candidate stack is the SPRUCE S1 Bog archive in northern Minnesota.

### Direct plant-pathway measurements

`SPRUCE Methane Transport in Plants at S1 Bog, Marcell Experimental Forest, Minnesota, 2017-2019`, SPRUCE ID `spruce.200`, DOI `10.15485/3000566`, contains direct measurements of methane transport by ground-layer plants and trees, diffusion and whole-plot emissions from September 2018 and June 2019. It also contains porewater and atmospheric CH4/CO2 stable-isotope data from July 2017 to explore the relative magnitude of methane oxidation, plus episodic ebullition information. This is materially stronger for TCD-034 than system-level CH4 flux alone because the plant-mediated pathway is observed separately.

### Environmental forcing

SPRUCE ID `spruce.032`, DOI `10.3334/CDIAC/spruce.032`, provides half-hourly environmental records for the experimental plots over the period that covers 2017-2019, including soil temperature. The archive is explicitly intended to be paired with other SPRUCE data for model analysis. GHG12 does not yet claim that its released data dictionary contains the exact depth/time/location combination required to reconstruct both the 0.50 m T50 operator and the revision-53 root-index selector for each spruce.200 observation. That must be checked from the actual downloadable files.

SPRUCE ID `spruce.079`, DOI `10.25581/spruce.079/1608615`, provides half-hourly plot-level water-table depth beginning in 2015, including 2017-2019.

### Whole-ecosystem methane flux

SPRUCE ID `spruce.034`, DOI `10.3334/CDIAC/spruce.034`, provides large-collar community CO2 and CH4 flux measurements from 2011 through 2021 and therefore overlaps the spruce.200 period. This can provide an independent whole-ecosystem flux context, subject to matching plots, dates and microtopography.

### Root and vegetation information

SPRUCE ID `spruce.127` provides root production measurements resolved to plant functional type over 2015-2021, and other public SPRUCE vegetation datasets document species/community composition. These data improve the plausibility of reconstructing root/vegetation state, but GHG12 does not claim exact observation-level alignment with spruce.200.

## Joinability audit against the GHG11 minimum package

The public SPRUCE stack substantially improves the evidence situation:

- positive CH4 flux is available;
- plant-mediated transport is measured directly;
- diffusion and whole-plot emissions are measured;
- oxidation information is partly constrained by stable isotopes;
- water-table records overlap;
- soil-temperature records overlap;
- root and vegetation datasets exist.

However, validation readiness is not yet demonstrated. Four joinability questions remain material.

First, spruce.200 separates measurements made outside experimental enclosures in September 2018 and June 2019 from isotope measurements made inside enclosures in July 2017. The exact spatial keys linking each plant-transport observation to soil temperature, water table, roots, vegetation and whole-plot flux must be established from the data files and dictionaries.

Second, the exact soil-temperature depths needed for T50 reconstruction and legacy-selector reconstruction must be verified from spruce.032 or another overlapping SPRUCE forcing dataset. Dataset-level descriptions alone are not sufficient.

Third, the plant-transport measurements are episodic rather than a continuous multi-season time series. It is therefore not yet shown that the observations span enough temperature/phenology variation to distinguish the legacy root-index selector from the fixed 0.50 m selector without parameter compensation.

Fourth, SPRUCE is one peatland system. Even a successful S1 Bog validation would define a bounded site/application envelope, not a general ANIMO Class-F envelope.

## Secondary historical-model-data candidate

The Michigan peatland data used by Shannon and White and later Walter-Heimann include multi-year CH4 emissions, water-table depth, peat temperatures at multiple depths and CH4 concentration profiles. Modern literature confirms the existence and scientific use of these variables. GHG12 did not recover a public, machine-readable, provenance-complete package containing all original observations and location/measurement metadata. It is therefore classified as a high-value acquisition lead, not an admissible dataset.

## Readiness result

GHG12 qualifies the current acquisition state as:

`QUALIFIED_TCD034_PUBLIC_VALIDATION_DATASET_CANDIDATE_STACK_IDENTIFIED_DETAILED_JOINABILITY_EXTRACTION_REQUIRED_V1`

This is not empirical validation. It establishes that a materially stronger process-resolved candidate now exists publicly and is worth a dedicated extraction/join workunit.

The immediate next task is to download the authoritative spruce.200 package and the overlapping environmental/water-table/root/flux packages, pin their checksums and schemas, establish exact keys and dates, and determine whether both selector inputs can be reconstructed for the same plant-transport observations.

Until that succeeds, TCD-034 remains `NOT_READY_FOR_CLASS_F_SCIENTIFIC_ADMISSION`. Historical revision-53 selector intent remains unresolved.
