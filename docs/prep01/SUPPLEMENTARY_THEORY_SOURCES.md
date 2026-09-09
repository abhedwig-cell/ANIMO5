# Supplementary theory and formulation sources

Status: `OFFICIAL_EXTERNAL_SOURCES_IDENTIFIED_NOT_FROZEN_AS_VERSION_4_1_5_SPECIFICATION`.

PREP01 keeps supplied/frozen documentation separate from external research used to locate missing theory. The sources below are official Wageningen University & Research records discovered after the initial documentation ingest. They are not silently promoted to the authoritative ANIMO 4.1.5 revision-53 specification.

## 1. ANIMO 4.0 process descriptions, Alterra Report 983

Official WUR record:

**Groenendijk, P., Renaud, L.V. & Roelsma, J. (2005). _Prediction of nitrogen and phosphorus leaching to groundwater and surface waters; process descriptions of the ANIMO 4.0 model_. Alterra-report 983.**

Canonical WUR document location reported by the Research Portal:

`https://edepot.wur.nl/35121`

The WUR record describes this as a 114-page academic report containing process descriptions implemented in ANIMO 4.0. It explicitly mentions model-formulation changes since ANIMO 3.5, including soil-moisture effects on mineralization and denitrification and support for externally supplied daily crop nutrient uptake.

The supplied ANIMO 4.0 User's Guide itself cites this report as the more extensive theoretical description.

### PREP01 use

Classification:

`OFFICIAL_4_0_THEORY_SOURCE_IDENTIFIED`

This report should become the primary C/N/P theory baseline for reconciliation once its exact document bytes are obtained through a controlled source and frozen by hash.

It still does **not** document later 4.1.x additions such as the supplied GHG implementation, later macropore code or every revision-53 parser/output change.

## 2. Early SWAP-ANIMO greenhouse-gas formulation evidence

Official WUR Research Portal record:

**Hendriks, R.F.A., Wollewinkel, R. & van den Akker, J.J.H. (2007). _Predicting soil subsidence and greenhouse gas emission in peat soils depending on water management with the SWAP-ANIMO model_. Proceedings of the First International Symposium on Carbon in Peatlands, pp. 583-586.**

Canonical WUR document location reported by the Research Portal:

`https://edepot.wur.nl/159749`

The official abstract states that a process-based model was developed to simulate peatland emissions of CO2, CH4 and N2O together with soil subsidence and nutrient loading, and that it was calibrated and validated against two Dutch experimental fields.

### Relation to supplied source

The supplied source contains:

- `ghgasses.for` with implementation-history comment `2007-08 Hendriks`;
- `ghg_ch4.for` with `2007 Hendriks`;
- `ghg_n2o.for` with `2008 Hendriks`;
- GHG transport routines and revision metadata from later maintenance snapshots.

The publication date and source comments therefore provide a plausible historical link between the published SWAP-ANIMO GHG work and the later source modules.

### PREP01 limitation

Classification:

`GHG_FORMULATION_PROVENANCE_LEAD_NOT_VERSION_SPECIFICATION`

The four-page conference contribution is not assumed to contain the complete equations, parameters or exact text-input contract of the supplied revision-53 source. A source-specific GHG formulation document is still required for scientific qualification.

## 3. Later independent confirmation that ANIMO had a newer GHG module

A 2022 Wageningen report chapter describing an ANIMO application states that its simulation used an adaptation to ANIMO 4.0 and explicitly says it **did not use the new greenhouse gas module**, described as direct simulation of CO2, CH4 and N2O.

This is useful lineage context because it independently confirms that a later GHG module existed, but it does not identify the exact revision, parser schema or equations corresponding to the supplied source/testcase.

Classification:

`LATER_CONTEXT_ONLY`

## 4. Evidence hierarchy

For ANIMO5 theory/code reconciliation, use the following priority:

1. exact version-specific theory/change document tied to the frozen source revision;
2. official process report for the closest documented model version;
3. supplied User's Guide and technical program description;
4. peer-reviewed or official process publications tied to named ANIMO modules;
5. later application reports as contextual evidence only;
6. code inference where documentation is absent, explicitly marked as inference.

No source below level 1 may erase a source/document discrepancy merely because its scientific description appears plausible.

## 5. Current documentation consequence

The previous statement that only summarized 4.0 theory was identifiable is now too narrow. PREP01 has located the official comprehensive ANIMO 4.0 process report and an early official GHG publication.

The remaining theory blocker is therefore more specific:

`4_0_CORE_THEORY_IDENTIFIED_4_1_X_CHANGE_AND_GHG_VERSION_SPECIFICATION_STILL_REQUIRED`

The raw external documents are not republished to this public repository. Their controlled byte freeze, where legally permitted, is a later evidence-ingest action.
