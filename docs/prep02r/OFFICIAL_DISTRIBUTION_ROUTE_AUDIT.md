# ANIMO-PREP02R — Official Distribution Route Audit

Status: `OFFICIAL_ROUTE_CONFIRMED_HISTORICAL_4_1_X_RETENTION_UNPROVEN`.

Checked: 2026-09-09.

## Purpose

Determine what the current official WUR/Wageningen Environmental Research distribution route actually establishes about historical ANIMO 4.1.x availability, and what it does not establish.

This is acquisition evidence only. It does not qualify any executable or build as reference behaviour.

## Current official ANIMO product page

Official page:

`https://www.wur.nl/en/research/products-services/animo`

Observed on 2026-09-09:

- source code is stated to be unavailable in principle, with possible exceptions for joint/PhD research;
- an executable is stated to be available upon request;
- releases are stated to be available for internal and external use;
- the model is described as normally supplied as an executable release;
- obtaining the model is tied to WUR general terms and an ANIMO agreement;
- Piet Groenendijk and Leo Renaud are shown as ANIMO experts.

The page also contains clearly historical platform wording, including MS-DOS, SUN/UNIX and VAX/VMS and the statement that there is no Windows version. That wording conflicts with the supplied revision-53 source self-identification as an Intel 64 Visual Fortran build. It must therefore not be used as revision-53 platform provenance.

Classification:

`OFFICIAL_ACQUISITION_ROUTE_NOT_VERSION_PROVENANCE`

## Current official ANIMO agreement

Official agreement linked from the product page:

`https://backend.wur.nl/sites/default/files/2026-01/Agreement%20Animo%202026.pdf`

The current 2026 form explicitly identifies:

```text
ANIMO
Version 4.0
Authors P. Groenendijk, L.V. Renaud
```

This is materially important for PREP02R. The current public request route does **not** establish that ANIMO 4.1.x, ANIMO 4.1.5 or revision 53 is the release that would be supplied in response to a normal current ANIMO request.

Therefore a PREP02R request must be framed as an archival historical-reference request for the 4.1.x lineage, not as a generic request for the current ANIMO executable.

Classification:

`OFFICIAL_CURRENT_DISTRIBUTION_SCOPE_EVIDENCE_VERSION_4_0_NOT_R53_REFERENCE`

## Current official distribution conditions

Official general terms linked from the product page:

`https://backend.wur.nl/sites/default/files/2025-10/GENERAL-TERMS-CONDITIONS-ENG.pdf`

The terms are revised November 2017. They state that WENR software remains WENR property and that the user may not make the software available to a third party without prior written WENR permission.

PREP02R consequence:

- a historical executable obtained through WENR should be retained in controlled evidence storage;
- public GitHub should contain hashes, provenance and qualification records unless WENR explicitly permits redistribution;
- reference qualification does not require public redistribution of the executable bytes.

This aligns with the existing PREP02R controlled-retention rule.

## Historical contact continuity

The supplied ANIMO 4.0 User's Guide identifies:

- P. Groenendijk for model formulations;
- L.V. Renaud for program code or model availability;
- H.P. Oosterom for program code or model availability.

The current WUR product page still identifies Leo Renaud and Piet Groenendijk as ANIMO experts. This gives a strong institutional contact route, but not historical binary provenance by itself.

Preferred first contact target remains Leo Renaud for program/release availability. Piet Groenendijk is a useful second route for model/release-history context. H.P. Oosterom remains a historically documented route unless a current institutional contact path is independently established.

## Source-lineage caveat that must accompany the request

The frozen archive is byte-pinned as:

`ANIMO_4.1.5.53(3).zip`

SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

`Version.inc` self-identifies tag `animo4.1.5`, revision `53`, and Intel Visual Fortran Composer XE `12.1.0.233` Intel64.

However the PREP01 source-provenance audit found that all 53 observed file-level `$HeadURL` values point to `tags/animo4.1.4`, while file-level revisions range from 7 to 53. Exact homogeneous canonical SVN-tag provenance is therefore unresolved.

An archival request should consequently ask not only for `animo41.exe`, but also for any manifest, release directory, source checkout identity or build record that can establish which source tree was actually used for the historical executable.

## Acquisition implication

The current official route is stronger than an arbitrary web lead but weaker than an artifact:

1. WUR publicly confirms an executable-request route.
2. The current agreement explicitly names Version 4.0.
3. No public evidence yet establishes that 4.1.x or revision 53 remains in the normal distribution channel.
4. PREP02R must request historical archive material specifically.
5. Any received artifact remains unqualified until lineage and provenance are evaluated.

Current decision remains:

`BLOCKED_HISTORICAL_REFERENCE_ARTIFACT_NOT_YET_OBTAINED`.
