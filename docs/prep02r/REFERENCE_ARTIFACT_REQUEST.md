# ANIMO-PREP02R — Reference Artifact Request Packet

Purpose: obtain historical qualification evidence for ANIMO 4.1.5 revision 53 without asking the recipient to validate ANIMO5 or to endorse reconstructed GNU behaviour.

## Why this must be an archival request

The current WUR ANIMO product page states that an executable is available upon request. However, the current ANIMO agreement linked from that page explicitly identifies the distributed program as:

```text
ANIMO
Version 4.0
Authors P. Groenendijk, L.V. Renaud
```

Therefore a normal current ANIMO request must not be assumed to yield ANIMO 4.1.x or revision 53. PREP02R must ask specifically for retained historical 4.1.x release/build material.

Please do not substitute the current/default Version 4.0 distribution for the historical request unless it is supplied and labelled separately as a distinct lineage.

## Requested artifact order

### 1. Exact historical executable

Preferred artifact:

```text
ANIMO 4.1.5
revision 53
historical runner name likely: animo41.exe
```

Please retain/provide with as much of the following provenance as available:

- original filename;
- exact version and revision;
- release/build date;
- originating release directory, archive, share, repository tag or archived machine;
- whether it was used with the historical 4.1-era testcase set;
- platform and architecture;
- any release note or manifest that accompanied it;
- source checkout, SVN tag/revision or source archive identity used for the build, if known.

PREP02R will calculate SHA-256 immediately after receipt. Binary redistribution is not required. Controlled access is sufficient.

### 2. Original build/project metadata

Any retained item is useful:

- `.sln`;
- `.vfproj` or related Intel Fortran project file;
- project property export/screenshots;
- build log;
- compiler command line;
- linker command line;
- `.bat`, `.cmd`, `.props` or environment setup used for release builds;
- archived build VM/workstation image or software inventory;
- release manifest or source checkout record tying the project to the executable.

The frozen source identifies:

```text
Intel Visual Fortran Composer XE 12.1.0.233 [Intel(R) 64]
```

Settings of particular qualification interest are default REAL size, DOUBLE PRECISION semantics, local storage duration, PowerStation-compatible unformatted record conventions, optimization, floating-point model, preprocessing, source-unit selection, linker/runtime-library assumptions and any compatibility options.

### 3. Executable-linked historical testcase output

If the executable itself is unavailable, a complete archived run remains useful when its provenance identifies the executable.

Preferred case:

`RuurloGrass`

Prefer:

- complete input tree;
- complete output tree;
- stdout/stderr or console log if retained;
- `MESSAGE.out`;
- balance files;
- state/concentration output;
- run date;
- executable filename/version/hash if known;
- batch/cmd runner or release manifest tying run and executable together.

A rounded figure/table copied from a report is not sufficient as the sole numerical oracle.

### 4. Nearest retained 4.1.x release

If revision 53 is not retained, please identify the nearest available ANIMO 4.1.x executable and its exact version/revision provenance.

PREP02R will treat it as a distinct lineage. It will not be silently relabelled as revision-53 truth.

## Source-lineage detail that may help archive searching

The supplied frozen source archive is byte-pinned as:

`ANIMO_4.1.5.53(3).zip`

SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Its `Version.inc` states:

```text
file:///V:/svn_Animo/tags/animo4.1.5
revision 53
Intel Visual Fortran Composer XE 12.1.0.233 [Intel(R) 64]
```

There is an unresolved provenance detail: the PREP01 file-level SVN keyword audit found that all 53 observed `$HeadURL` values point to `file:///V:/svn_Animo/tags/animo4.1.4/...`, while the archive-level `Version.inc` identifies `animo4.1.5` revision 53. This may be stale keyword expansion or another release procedure, but the supplied evidence does not decide which.

For that reason, any archived release manifest, source checkout record, SVN export path, build directory or known source archive tied to the executable would be especially valuable.

## Suggested request text

> We are reconstructing the historical behavioural reference for a controlled modernization of ANIMO. Our frozen source self-identifies ANIMO 4.1.5 revision 53 and Intel Visual Fortran Composer XE 12.1.0.233 Intel64. The supplied historical testcase runners refer to `animo41.exe`, but that executable and its Intel project metadata are absent. The current WUR ANIMO agreement is for Version 4.0, so this is specifically an archival request rather than a request for the current/default distribution. Do you still have the historical ANIMO 4.1.5 revision-53 executable, preferably the `animo41.exe` used with the 4.1-era testcase set, or any retained `.vfproj`/`.sln`, build log, release directory, source-checkout record, archived VM or Ruurlo output tied to a known executable? We only need the material for controlled scientific qualification and can keep binary artifacts outside public GitHub. If revision 53 is unavailable, the nearest provenance-qualified 4.1.x release would also be valuable, provided its exact version/revision is known.

## Publicly documented contact route

The historical ANIMO 4.0 User's Guide identifies L.V. Renaud and H.P. Oosterom for program-code/model-availability questions and P. Groenendijk for model formulations.

The current WUR ANIMO product page identifies Leo Renaud and Piet Groenendijk as ANIMO experts and states that an executable is available upon request.

Current product page:

`https://www.wur.nl/en/research/products-services/animo`

Current ANIMO agreement:

`https://backend.wur.nl/sites/default/files/2026-01/Agreement%20Animo%202026.pdf`

Current WUR general software terms:

`https://backend.wur.nl/sites/default/files/2025-10/GENERAL-TERMS-CONDITIONS-ENG.pdf`

The general terms restrict third-party redistribution without prior written WENR permission. PREP02R therefore assumes controlled retention of any received executable and public persistence only of hashes/provenance unless redistribution permission is explicit.

This contact route is an acquisition lead only. It does not establish that revision 53 is currently retained.

## Admission after receipt

Receipt alone does not qualify an artifact. PREP02R will first preserve bytes and provenance, hash them, classify lineage, and only then decide whether a native `RuurloGrass` qualification run is admissible.
