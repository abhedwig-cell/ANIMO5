# ANIMO 4.1.x release-lineage and extension-introduction reconciliation

Status: `PARTIAL_LINEAGE_RECOVERY_WITH_MATERIAL_CHRONOLOGY_CORRECTIONS`

Production migration: `NOT_ADMITTED`

## 1. Scope and evidence boundary

This TH02 document follows the qualified TH01 theory/provenance inventory and focuses on release chronology rather than process equations.

Frozen source:

`ANIMO_4.1.5.53(3).zip`

SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

The source archive is treated as B0 identity evidence. Source comments and SVN keyword expansions are provenance evidence, not authoritative theory and not automatically authoritative release history.

## 2. Archive-level 4.1.5 marker versus file-level SVN metadata

`Version.inc` identifies:

- tag path `animo4.1.5`;
- revision `53`;
- Intel Visual Fortran Composer XE 12.1.0.233 Intel 64.

The file-level metadata tell a different and more heterogeneous story.

A complete scan of the 65 source/archive members shows:

- 53 files with an expanded `$HeadURL` pointing to `tags/animo4.1.4`;
- 12 files without a parseable expanded `HeadURL` tag;
- no file-level expanded `HeadURL` observed that points to `tags/animo4.1.5`;
- parseable `$Id` revisions ranging through the historical range already observed by PREP01, with most expanded IDs dated in 2013, plus later changes such as `Animo.for` revision 41 dated 2016-08-26.

Therefore the correct provenance statement remains:

`ARCHIVE_IDENTIFIED_AS_4_1_5_REV53_FILE_LEVEL_LINEAGE_HETEROGENEOUS`

The exact bytes are fixed. A homogeneous SVN `animo4.1.5` tag checkout is not proven by the embedded keywords.

## 3. The ANIMO 4.1 release marker is real but is not a per-feature introduction marker

Forty-seven source members contain at least one history comment of the form:

`2011 Groenendijk, Renaud` / `Release of ANIMO4.1`

This is strong source-internal evidence that an ANIMO 4.1 release lineage existed and that a broad source refresh was associated with 2011.

However, the marker is repeated across many generic routines that clearly predate 4.1. It must therefore be interpreted as a release/maintenance stamp, not as evidence that every feature in those files was introduced in 2011.

One especially useful counterexample is `Function.for`: many unrelated utility functions repeat the same 2003 ANIMO4.0 and 2011 ANIMO4.1 release comments. That pattern demonstrates why the release marker cannot be used as a per-routine feature-introduction timestamp.

Classification:

`SOURCE_HISTORY_COMMENT_RELEASE_STAMP_NOT_FEATURE_INTRODUCTION_PROOF`

## 4. ANIMO 4.1 date ambiguity inside the frozen source

The dominant release stamp says 2011. But `ChoosePClass` in `Function.for` has a more specific history block:

- `2010 Renaud`;
- `Release of ANIMO4.1`.

The routine description says it chooses crop-uptake variables according to a P class for `EMW2012`.

This creates a narrow internal chronology ambiguity:

- broad source-history stamp: ANIMO4.1 in 2011;
- P-class routine-specific history: ANIMO4.1 in 2010.

This does not prove two releases. It may reflect development versus release timing, a copied history block, later comment editing, or an internal pre-release lineage.

TH02 therefore records:

`ANIMO41_RELEASE_YEAR = 2010_OR_2011_SOURCE_INTERNAL_UNRESOLVED`

until independent release documentation is recovered.

## 5. Greenhouse-gas chronology is earlier than ANIMO 4.1

The dedicated GHG source files contain specific history comments:

- `ghgasses.for`: `2007-08 Hendriks`;
- `ghg_ch4.for`: `2007 Hendriks`;
- `ghg_n2o.for`: `2008 Hendriks`;
- `ghgtransport.for`: `2007 Hendriks`;
- `ghgtranssub.for`: `2007 Hendriks`.

Several of these comments then say `Release of ANIMO4.0`.

That literal release label cannot be reconciled with the supplied official 2005 ANIMO 4.0 User's Guide as a complete version description, because the GHG implementation work is dated 2007-2008 and the supplied guide does not document this operational GHG contract.

Independent public evidence strongly supports the dated scientific implementation chronology. Hendriks, Wollewinkel and van den Akker published a process-based SWAP-ANIMO GHG model in 2007 that simulates CO2, CH4 and N2O and was calibrated/validated against two peat experimental fields.

Public source:

`https://research.wur.nl/en/publications/predicting-soil-subsidence-and-greenhouse-gas-emission-in-peat-so/`

The current WUR ANIMO product page also lists greenhouse-gas emission as a newer model capability:

`https://www.wur.nl/en/research/products-services/animo`

The defensible chronology is therefore:

- GHG scientific/model development existed by 2007;
- N2O-specific source work is explicitly dated 2008;
- the GHG route was later present in the 4.1.4-tagged source lineage and the supplied 4.1.5/rev53 archive;
- the source phrase `Release of ANIMO4.0` cannot be equated without qualification to the official 2005 ANIMO 4.0 release documented by the supplied guide.

Classification:

`CONFLICTING_VERSION_LABEL_WITH_STRONG_PRE_41_IMPLEMENTATION_PROVENANCE`

This strengthens TH01's broad GHG provenance but does not solve exact revision-53 theory or parser lineage.

## 6. Macropore chronology materially predates ANIMO 4.0 and 4.1

The most important chronology correction concerns macropores.

`MAPOTRANSPORT.FOR` explicitly says it is part of:

`ANIMO 3.7.5, version that includes macropores`

and records:

`9-9-1999 R.F.A. Hendriks creation`.

This is source-internal provenance, but it is independently corroborated by the peer-reviewed 1999 Journal of Hydrology paper by Hendriks, Oostindie and Hamminga. That paper describes a modified FLOCR/ANIMO combination with permanent macropores and internal catchment domains and reports preferential solute transport through cracked/macroporous clay.

WUR publication record:

`https://research.wur.nl/en/publications/simulation-of-bromide-tracer-and-nitrogen-transport-in-a-cracked-/`

A later Alterra report also states that ANIMO was adapted with preferential transport and rapid drainage through macropores based on the Hendriks 1993 / Hendriks et al. 1999 lineage.

This means the following distinction is necessary:

- `FIRST_KNOWN_IMPLEMENTATION_LINEAGE`: pre-4.0, at least ANIMO 3.7.5 / 1999 for macropore solute transport;
- `OFFICIAL_ANIMO40_OPERATIONAL_STATUS`: the supplied 4.0 guide says the macropore option is not fully operational;
- `REV53_SOURCE_STATUS`: active macropore water and solute routines are present.

Source presence before 4.0 and non-operational status in the official 4.0 guide are not contradictory. They refer to different questions: experimental/branch implementation versus supported release functionality.

This requires refinement of any TH01 wording that implied the macropore process itself was first introduced after ANIMO 4.0.

Corrected chronology classification:

`PRE40_IMPLEMENTATION_LINEAGE_WITH_ANIMO40_NONOPERATIONAL_RELEASE_STATUS_AND_LATER_REV53_ACTIVE_SOURCE`

## 7. Macropore hydrology source itself shows multiple chronology layers

The current revision-53 archive contains at least three distinct macropore chronology signals:

1. `MAPOTRANSPORT.FOR`: ANIMO 3.7.5 and creation in 1999;
2. `mapoinput.for`: history entries in 2007 and 2008, both labelled as ANIMO4.0 release activity, including `Release of ANIMO4.0 (32)`;
3. `MAPOHYDRO.FOR`: an `October 2008` marker.

These are consistent with long-running development and later integration/rework, not with a single clean feature introduction in one release.

The scientific hydrological lineage is further consistent with later SWAP macropore theory, but TH02 does not use later SWAP documentation to assign an ANIMO release number.

## 8. Stable DOM has strong formulation provenance but conflicting release nomenclature

TH01 already identified a public BMBF/UFZ project report containing a stable dissolved organic matter extension with parameter names that closely overlap the frozen source.

TH02 confirms that this public report describes:

- starting from ANIMO 3.8;
- model development to a version labelled `ANIMO Version 4.0`;
- a new stable dissolved organic matter pool;
- `Ratio_rd_st`, `sdofr`, `recfSDO`, `asfaSDO` and a humus-to-SDO exchange term;
- new parameters and changed input files;
- active collaboration with the original ANIMO developers at Alterra;
- use of the modified version by Alterra.

Public report:

`https://edocs.tib.eu/files/e01fb12/72746826X.pdf`

This is unusually strong formulation and developer-provenance evidence. But the version label conflicts with the supplied official 2005 ANIMO 4.0 guide, which does not expose a separate stable-DOM state family.

The safest interpretation is not that either source is false. Instead, `ANIMO Version 4.0` was not a globally unique release identifier across all development/project lineages.

TH02 therefore strengthens the classification to:

`CONFLICTING_VERSION_NOMENCLATURE_PARALLEL_OR_PROJECT_LINEAGE_PLAUSIBLE`

The exact merge point into the official 4.1.x line remains unresolved.

## 9. P-class / EMW2012 chronology

`ChoosePClass` is the strongest source-internal introduction marker found for the P-class route:

- routine purpose explicitly references `EMW2012`;
- history says `2010 Renaud` and `Release of ANIMO4.1`;
- the routine copies class-indexed N/P uptake and crop-loss arrays into active arrays.

Other revision-53 source surfaces expose `PClassOption`, `PClassYearSwitch`, class tables and P-status calculations based on `PAL` or `PW`.

This is sufficient to refine TH01's lineage statement from merely `ANIMO 4.1-era` to:

`SOURCE_HISTORY_TIES_PCLASS_SELECTION_TO_2010_ANIMO41_DEVELOPMENT_AND_EMW2012_CONTEXT`

It is still not independent scientific theory for the class thresholds, switching policy or parameter values. Those remain blocked for B3.

## 10. Soil-temperature file routing

`Input_SoilTemp.for` is a separate source member with a 2000 history signal, while the generic 4.1 parser exposes `SoilTempFile` and the 4.0 theory already contains temperature-dependent process functions and hydrology-supplied/internal temperature routes.

TH02 therefore finds no basis for calling soil-temperature dependence itself a 4.1 physics extension. The later surface is best interpreted as input-routing/interface evolution unless contrary evidence is recovered.

## 11. Consequences for TH01 interpretation

TH02 does not invalidate the TH01 qualification decision. It does refine chronology in three important ways.

### Macropores

Do not describe the macropore process family as simply a post-4.0 invention. Its experimental/source lineage reaches at least ANIMO 3.7.5 / 1999. The supplied official 4.0 guide's non-operational status remains valid for that release surface.

### GHG

Do not tie first implementation to ANIMO 4.1. GHG development is independently visible by 2007 and source comments date CH4/N2O work to 2007-2008. The exact official release in which it became supported remains unresolved.

### Stable DOM

Do not state a simple official `post-4.0` introduction chronology. A project lineage labelled ANIMO 4.0 already contains the stable-DOM formulation, but that label conflicts with the official supplied 4.0 guide. Exact official merge/release provenance remains unresolved.

## 12. What remains unresolved

TH02 has not located a public authoritative ANIMO 4.1 or 4.1.x release note/change log that maps features to release numbers.

Still open:

- exact official release date of ANIMO 4.1, because frozen-source comments point to both 2010 and 2011;
- exact merge/release point of stable DOM into the official Wageningen ANIMO line;
- exact supported-release introduction of GHG;
- exact supported-release reactivation/completion of macropore functionality after the 4.0 non-operational state;
- relationship between `tags/animo4.1.4` file keywords and the archive-level 4.1.5 revision-53 marker;
- exact release provenance for P-class thresholds and EMW2012 parameter datasets.

## 13. Interim qualification

TH02 can already defend:

`QUALIFIED_PARTIAL_41X_RELEASE_LINEAGE_WITH_PRE40_MACROPORE_AND_PRE41_GHG_PROVENANCE_AND_EXPLICIT_VERSION_CONFLICTS`

This is a provenance qualification only.

It is not:

`QUALIFIED_COMPLETE_ANIMO41_CHANGELOG`

and it does not alter B3 or B4 admission.
