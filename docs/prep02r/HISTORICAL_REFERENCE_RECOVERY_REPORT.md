# ANIMO-PREP02R — Historical Reference Recovery Report

Status: `BLOCKED_HISTORICAL_REFERENCE_ARTIFACT_NOT_YET_OBTAINED`.

## 1. Live starting state

PREP02 was re-read from the source-bound preparatory evidence baseline before this continuation workunit was started.

Baseline branch:

`baseline/animo-prep01-05-evidence`

Baseline head at reservation:

`9df84bd0ab9bc4ef8e214f01da616aa257a24b13`

PREP02 decision remains:

`BLOCKED_HISTORICAL_REFERENCE_ENVIRONMENT_REQUIRED`

The current GNU executable remains explicitly:

`DIAGNOSTIC_NOT_REFERENCE`

No corrected-legacy or production-migration work is admitted by PREP02R.

## 2. Frozen artifact verification

The supplied local bytes were re-hashed on 2026-09-09.

| Artifact | SHA-256 | Result |
|---|---|---|
| `ANIMO_4.1.5.53(3).zip` | `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566` | exact match |
| `ANIMO_testbank.zip` | `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84` | exact match |
| ANIMO 4.0 User's Guide PDF | `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301` | exact match |

The source archive contains no `.exe`, `.dll`, `.sln`, `.vfproj`, `.vcxproj`, makefile or historical build log.

## 3. Exact source-bound release clues

`Version.inc` in the frozen source states:

```text
Rcstemp='file:///V:/svn_Animo/tags/animo4.1.5'
Rcsrev='53'
Built='Intel Visual Fortran Composer XE 12.1.0.233 [Intel(R) 64]'
```

The source therefore gives an exact tag/revision identity and compiler lineage string, but not the project settings or executable bytes required for independent behavioural admission.

The current build-contract reconstruction remains a hypothesis, not historical proof. In particular:

- eight-byte default REAL behaviour is materially required by the source/runtime evidence, but `/4R8` versus an equivalent Intel project setting is not historically proven;
- PowerStation-compatible sequential-unformatted I/O strongly points to Intel `/fpscomp:ioformat` semantics, but the exact historical project setting is absent;
- GNU `-fno-automatic` does not prove historical Intel `/Qsave` usage;
- optimization, floating-point model, alignment, preprocessing, linker settings and runtime-library assumptions remain unknown.

## 4. Supplied testbank search

Four frozen testcase launchers explicitly call:

```text
..\animo41.exe Animo.ini
```

These are `CranGrass`, `CranMais`, `GrassPeat` and `RuurloGrass`.

The executable itself is not present in the supplied testbank. Runner naming is therefore useful provenance evidence for the expected historical release family, but it is not enough to identify the exact executable revision.

Two `initial.out` files are present as historical-looking restart/state artifacts:

- `Puitmijn_Cranendonck_60/input/initial.out`, SHA-256 `1dba5ba4b644dc8aecb34fed22995d6c550c0ea994cbb1af85866d26ae35e209`;
- `Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA/Input/initial.out`, SHA-256 `f2983dd7648f98081ba66a88b5426808e387521e07e237e27c9fa408481807ed`.

No retained executable identity, run log or complete output tree ties either file to revision 53. They are therefore classified `UNATTRIBUTED_OUTPUT_NOT_REFERENCE`.

`GHGMais` remains excluded from first reference admission because the supplied input contract demonstrably belongs to a different or incomplete source lineage relative to revision 53.

## 5. Public historical search

A new targeted public search was performed for exact `animo41.exe`, ANIMO 4.1.5/revision-53 artifacts, project metadata and ANIMO4.1 documentation.

No trustworthy public copy of the exact revision-53 executable, an Intel Visual Fortran project/build file, or an executable-linked Ruurlo output bundle was found.

This negative result is only a search observation. It is not evidence that institutional or private historical archives do not contain the artifacts.

### Official WUR acquisition route

The current WUR ANIMO product page states that an executable is available upon request and that information on program code or model availability is obtainable via Leo Renaud. The page also presents Piet Groenendijk and Leo Renaud as current ANIMO experts.

This is the strongest public acquisition route found. It is not itself proof that revision 4.1.5 revision 53 is retained.

The page contains historical platform wording that does not line up cleanly with the frozen revision-53 Intel64 build string. For PREP02R it is therefore treated as an institutional contact/acquisition route, not as authoritative revision-53 platform metadata.

### Older native binary lineage evidence

Alterra report 1262, *Inbouw ANIMO in MEBOT*, documents a packaged runtime containing `ANIMO_Shell.dll`, `ANIMO_4_0_20.dll`, `DFORRTD.DLL` and `MSVCRTD.DLL`.

This proves that historical native ANIMO binary artifacts were distributed in at least one older integration context. It is a distinct ANIMO 4.0.20 lineage and cannot qualify revision 53 or satisfy the requested nearest-4.1.x fallback rule.

### ANIMO 4.1 documentation lead

A 2013 Alterra/STOWA report cites:

`Groenendijk, P., R.F.A. Hendriks and L.V. Renaud, 2013. Prediction of nutrient leaching to groundwater and surface waters and greenhouse gas emissions from soil. Process descriptions of the ANIMO4.1 model. Wageningen, Alterra, Report in prep.`

This is useful evidence that an explicit ANIMO4.1 documentation lineage existed by 2013. The cited report itself was not recovered in the targeted public search, and it contains no executable provenance in the citation alone.

## 6. Historical documentation contact route

The supplied ANIMO 4.0 User's Guide names:

- P. Groenendijk for model formulations;
- L.V. Renaud for program code or model availability;
- H.P. Oosterom for program code or model availability.

The current WUR product page still points program-code/model-availability inquiries to Leo Renaud. This continuity makes WUR/WENR the preferred first acquisition route before attempting unsupported compiler reconstruction from third-party material.

## 7. First native qualification remains blocked

`RuurloGrass` remains the preferred first native case because it is a supplied frozen legacy-style testcase, is documented in the ANIMO 4.0 guide, avoids the known GHGMais lineage mismatch, and already has a deterministic GNU diagnostic comparand.

Native execution has **not** been attempted because no provenance-qualified historical executable or verified historical Intel build environment has been obtained.

Therefore PREP02R has not performed:

- executable preservation/hash capture;
- native stdout/stderr capture;
- native output-tree capture;
- native-versus-GNU numerical comparison;
- variable-class-specific tolerance derivation;
- observer-only unrounded native capture.

Doing any of those with an untrusted or reconstructed executable and then calling it historical truth would violate the reference-admission contract.

## 8. Acquisition target now narrowed

Request in this order:

1. exact ANIMO 4.1.5 revision-53 executable, likely historical runner name `animo41.exe`, with release/archive provenance;
2. any retained `.sln`, `.vfproj`, project properties, build log, compiler/link command or archived VM/build machine from that release;
3. complete `RuurloGrass` output tree plus run log or other evidence tying it to a known executable;
4. if exact revision 53 is unavailable, nearest retained provenance-qualified 4.1.x executable with exact version/revision identification.

A nearby 4.1.x executable remains a separate lineage until a version-delta qualification chain establishes what it can and cannot anchor.

## 9. Current decision

No independent reference artifact satisfying PREP02R admission criteria has yet been obtained.

Decision:

`BLOCKED_HISTORICAL_REFERENCE_ARTIFACT_NOT_YET_OBTAINED`

The GNU diagnostic executable remains `DIAGNOSTIC_NOT_REFERENCE`.

Corrected legacy remains `NOT_ADMITTED`.

Production migration remains `NOT_ADMITTED`.
