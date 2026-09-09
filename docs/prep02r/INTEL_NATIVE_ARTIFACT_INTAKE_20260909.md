# ANIMO-PREP02R — Intel-native executable and Visual Fortran build-file intake, 2026-09-09

Status: `RECEIVED_CURRENT_INTEL_NATIVE_EXECUTABLE_AND_BUILD_METADATA_HISTORICAL_REFERENCE_NOT_YET_QUALIFIED`

## Purpose

Record and classify the newly supplied `animo41.exe`, `animo41.sln` and `animo41.vfproj` before native execution. Raw binary/build artifacts remain outside the public repository; only hashes and provenance observations are persisted.

This supplement changes PREP02R materially: the expected `animo41.exe` bytes and Visual Fortran project metadata are now available for controlled native case execution. It does **not** by itself establish a historical B2 reference.

## Receipt identities

- `animo41.exe`
  - SHA-256: `40e29853a0431cc7e2b787dfeb1870f44e1ff402b5aaebd6f56c8365fc5b178d`
  - size: `6,778,368` bytes
- `animo41.sln`
  - SHA-256: `206dd6cc23b7d53c117131e16f15a22c4c97afc1c81febb3c73d789cdb9551f2`
  - size: `1,233` bytes
- `animo41.vfproj`
  - SHA-256: `f8ac40ea91df926a035396b0afe8584ea0d9c19711535a12b4f12634ce688b2a`
  - size: `9,829` bytes

All were hashed before execution. Receipt manifests are under `integration/animo-prep/receipts/` and retain `reference_admitted=false` and `native_execution_admitted=false` until lineage review.

## Executable static identity

The executable is a `PE32+` x86-64 Windows console program. Static PE metadata reports:

- PE timestamp: `2026-05-27T13:41:28Z`;
- linker version: `14.35`;
- image version: `4.0`;
- subsystem version: `6.0`.

Embedded strings include:

- `ANIMO: 4.1`;
- `file:///V:/svn_Animo/tags/animo4.1.5`;
- `Version.inc`;
- `Intel Fortran RTL Message Catalog V20.0-001 Jan 10 2019`.

The binary also contains the PDB path:

`D:\USR\5200048928_SWAP_ANIMO\ANIMO\x64\Debug\animo41.pdb`

and source paths rooted at:

`D:\USR\5200048928_SWAP_ANIMO\ANIMO\src_develop_for_20260519`

This is important. The binary is plainly a recent/current build, not an untouched 2010/2011-era executable. Therefore receipt of the executable closes the earlier `bytes_available=false` condition, but not the historical-provenance condition required for ordinary B2 admission.

## Visual Fortran project evidence

`animo41.sln` is a Visual Studio 2010 format solution containing an Intel Fortran project for Win32 and x64, Debug and Release.

`animo41.vfproj` declares:

- `ProjectCreator="Intel Fortran"`;
- `Keyword="Console Application - Converted from CVF"`;
- project version `11.0`.

For `Debug|x64`, the project records especially relevant runtime-semantics choices:

- free source form;
- default REAL promoted through `RealKIND=realKIND8`;
- `LocalVariableStorage=localStorageSave`;
- `LocalSavedScalarsZero=true`;
- `FloatingPointExceptionHandling=fpe0`;
- `FloatingPointModel=source`;
- CVF calling convention;
- bounds checking enabled;
- multithreaded debug runtime.

These settings are directly relevant to the BUILDQ hidden-state/storage-duration work because the project explicitly requests saved local storage and, in this debug x64 configuration, zero initialization of saved scalars.

The project references 63 source/include members. Every one of those 63 names exists in the frozen revision-53 source archive. The frozen archive has two additional members not referenced by this project: `input1_1.for` and `outselorg.for`.

This establishes strong build-surface consistency, but not exact proof that the supplied executable was compiled from the exact frozen source bytes. The PE/PDB metadata does not contain an independently verifiable source checksum set.

## Testbank execution binding

The frozen testbank already contains historical launchers using exactly:

`..\animo41.exe Animo.ini`

for at least:

- `CranGrass`;
- `CranMais`;
- `GrassPeat`;
- `RuurloGrass`.

This makes the received executable operationally suitable for the existing native capture contract without testcase content translation. The first controlled native case remains `RuurloGrass`.

The ANIMO 4.0 user guide independently documents the same command-line execution pattern: executable plus an `Animo.ini` direct file. It also states that `INITIAL.out` can be used to initialize another run and that `MESSAGE.out` captures warning/error messages, both relevant to native output capture. The guide is inherited 4.0 documentation, not proof of revision-53 binary identity.

## Scientific evidence interpretation

The received materials support three different statements that must remain separate:

1. **Native execution is now operationally possible.** The testbank launchers and project format are consistent with the supplied executable.
2. **A current Intel-native cross-compiler comparison is now possible.** This is high-value evidence for compiler/runtime semantics and can expose differences hidden by the GNU diagnostic build.
3. **Historical B2 is not yet established.** The executable timestamp and build path identify a 2026 build. Without stronger provenance tying its executable bytes to the intended historical reference environment, it must not be promoted to historical behaviour truth.

A successful native run therefore first produces `CURRENT_INTEL_NATIVE_BEHAVIOURAL_EVIDENCE`, not automatically `QUALIFIED_HISTORICAL_REFERENCE_ENVIRONMENT`.

## Required first execution

Use the exact frozen `RuurloGrass` case under the PREP02R native capture contract:

- preserve the received executable hash;
- use original frozen case bytes;
- execute `..\animo41.exe Animo.ini` from the case working directory layout;
- record Windows version/build, architecture, locale, timezone and working directory;
- capture stdout/stderr, exit status and complete raw generated output tree;
- preserve every generated file before normalization;
- repeat from a clean case tree when practical;
- compare the raw/native result to the deterministic GNU B1 output without a global numerical tolerance.

After Ruurlo succeeds, expand to the eight revision-53-compatible frozen cases. `GHGMais` remains separately lineage-qualified because the supplied testcase contract is already known to mismatch revision 53.

## Effect on TCD-015 / B3B01

For TCD-015 this unlocks the missing **native Intel execution axis**. If the affected LWKM nitrate branch is subsequently captured under this executable, B3B01 can compare the exact historical-style Intel runtime response against GNU B1 and the proposed `Hv1-Hv` correction.

However, the current B3B01 admission gate must remain fail-closed until PREP02R determines whether this artifact is strong enough for a qualified B2 route, or whether separate historical provenance is still required. Independent second-line review remains independently required.

## Current decision

`RECEIVED_CURRENT_INTEL_NATIVE_EXECUTABLE_AND_BUILD_METADATA_HISTORICAL_REFERENCE_NOT_YET_QUALIFIED`

Native execution is the next evidence-producing action. No reference, corrected legacy, B3 or production migration is admitted by this intake.
