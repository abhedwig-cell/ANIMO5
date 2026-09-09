# ANIMO-TH02 — ANIMO 4.1.x Release-Lineage, Extension Introduction & Provenance Recovery

Status: `IN_PROGRESS_RELEASE_LINEAGE_RECOVERY`

## Purpose

Resolve the main version-lineage gaps left explicitly open by ANIMO-TH01. TH02 does not attempt to rewrite the revision-53 theory manual. It reconstructs when and through which historical ANIMO lineage the relevant extensions entered, using source metadata, source history comments, public WUR/Alterra material and any defensible release/change documentation that can be recovered.

TH02 starts from the qualified TH01 closeout head:

`a3360415364ef4a66a81d7b6715bcd400829df1b`

TH01 decision:

`QUALIFIED_REV53_THEORY_PROVENANCE_INVENTORY_WITH_EXPLICIT_UNRESOLVED_GAPS`

## Frozen evidence

Frozen source:

- artifact: `ANIMO_4.1.5.53(3).zip`
- SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- archive-level version marker: `animo4.1.5`
- archive-level revision marker: `53`

Supplied principal documentation:

- ANIMO 4.0 User's Guide
- SHA-256: `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`

## Primary questions

TH02 must answer, where evidence permits:

1. Which revision-53 files explicitly claim an ANIMO 4.1 release lineage?
2. Which process families have source history predating ANIMO 4.0 despite being non-operational or incompletely documented in the supplied 4.0 guide?
3. Which source files still carry `tags/animo4.1.4` metadata inside the supplied 4.1.5 archive?
4. Which extensions can be tied to dated implementation events or earlier ANIMO versions without treating comments as authoritative theory?
5. Which TH01 statements need refinement because release chronology and operational availability are not the same thing?
6. Can public reports, manuals or project documents independently corroborate the source-internal chronology?

## Priority scope

At minimum:

- ANIMO 4.1 release marker and 2011 source-history comments;
- stable DOM introduction and later C/N/P expansion;
- greenhouse-gas introduction chronology;
- macropore chronology, including the apparent ANIMO 3.7.5 / 1999 source lineage versus ANIMO 4.0 non-operational documentation;
- P-class / EMW2012 chronology;
- soil-temperature input routing;
- source-file SVN `Id` / `HeadURL` / revision metadata relevant to 4.1.4 versus 4.1.5 provenance.

## Evidence classes

TH02 distinguishes:

- `ARCHIVE_LEVEL_VERSION_MARKER`
- `SOURCE_FILE_SVN_METADATA`
- `SOURCE_HISTORY_COMMENT`
- `PUBLIC_RELEASE_OR_CHANGE_DOCUMENTATION`
- `PUBLIC_PROJECT_PROVENANCE`
- `PUBLIC_SECONDARY_MODEL_DESCRIPTION`
- `CONFLICTING_VERSION_LINEAGE_EVIDENCE`
- `UNRESOLVED`

A source history comment is provenance evidence only. It is not automatically theory authority or proof that a capability was operational in the named release.

## Hard rules

- no frozen source modification;
- no testcase modification;
- no corrected-legacy patch;
- no production code implementation;
- no physics change;
- no numerical-policy change;
- no silent promotion of source comments to authoritative release history;
- no assumption that implementation date equals release date;
- no assumption that source presence equals operationally supported functionality;
- no B3 or B4 admission solely from provenance recovery.

## Expected outputs

- `docs/theory/REV41_RELEASE_LINEAGE_RECONCILIATION.md`
- `docs/theory/REV41_SOURCE_HISTORY_REGISTER.csv`
- `docs/theory/MACROPORE_RELEASE_LINEAGE_RECONCILIATION.md`
- `integration/animo-theory/ANIMO-TH02_STATUS.json`

TH02 may propose precise corrections to TH01 provenance wording when evidence requires it, but must preserve TH01's evidence-class boundaries.

Production migration remains `NOT_ADMITTED`.
