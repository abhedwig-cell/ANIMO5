# ANIMO-PREP02R — Reference Artifact Request Packet

Purpose: obtain historical qualification evidence for ANIMO 4.1.5 revision 53 without asking the recipient to validate ANIMO5 or to endorse reconstructed GNU behaviour.

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
- any release note or manifest that accompanied it.

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
- archived build VM/workstation image or software inventory.

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

## Suggested request text

> We are reconstructing the historical behavioural reference for a controlled modernization of ANIMO. Our frozen source identifies ANIMO 4.1.5 revision 53 and Intel Visual Fortran Composer XE 12.1.0.233 Intel64. The supplied historical testcase runners refer to `animo41.exe`, but that executable and its Intel project metadata are absent. Do you still have the historical ANIMO 4.1.5 revision-53 executable, preferably the `animo41.exe` used with the 4.1-era testcase set, or any retained `.vfproj`/`.sln`, build log, release directory, archived VM or Ruurlo output tied to a known executable? We only need the material for controlled scientific qualification and can keep binary artifacts outside public GitHub. If revision 53 is unavailable, the nearest provenance-qualified 4.1.x release would also be valuable, provided its exact version/revision is known.

## Publicly documented contact route

The historical ANIMO 4.0 User's Guide identifies L.V. Renaud and H.P. Oosterom for program-code/model-availability questions and P. Groenendijk for model formulations.

The current WUR ANIMO product page continues to direct program-code/model-availability inquiries to Leo Renaud and states that an executable is available upon request.

Current product page:

`https://www.wur.nl/en/research/products-services/animo`

This contact route is an acquisition lead only. It does not establish that revision 53 is currently retained.

## Admission after receipt

Receipt alone does not qualify an artifact. PREP02R will first preserve bytes and provenance, hash them, classify lineage, and only then decide whether a native `RuurloGrass` qualification run is admissible.
