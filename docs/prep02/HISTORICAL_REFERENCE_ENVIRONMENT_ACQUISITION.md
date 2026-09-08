# Historical Intel reference-environment acquisition

Status: `ACTIONABLE_ACQUISITION_ROUTE_IDENTIFIED_ENVIRONMENT_NOT_ACQUIRED`.

## Purpose

PREP02 requires an independently trustworthy historical native execution before the deterministic GNU route can be admitted as a behavioural reference. This note turns the generic historical-environment blocker into a concrete acquisition target and records what has and has not been found.

No compiler binary, license file or ANIMO executable is stored in this public repository.

## Exact target identity

The supplied revision-53 `Version.inc` identifies:

`Intel Visual Fortran Composer XE 12.1.0.233 [Intel(R) 64]`.

Independent Intel Community material from the same period confirms the Intel64 compiler string:

`Intel Visual Fortran Intel 64 Compiler XE for applications running on Intel 64, Version 12.1.0.233 Build 20110811`.

Intel Community installation records identify the matching Fortran package as:

`w_fcompxe_2011.6.233`

and a 2011 Intel Community installation report explicitly names the Windows installer:

`w_fcompxe_2011.6.233.exe`

This is Intel Visual Fortran Composer XE 2011 Update 6 / compiler 12.1.0.233 generation. The exact historical ANIMO project settings remain separately unresolved.

## Vendor access reality in 2026

Current Intel guidance says legacy Parallel Studio XE / older developer-tool versions are unsupported and are not generally available as public downloads. Intel directs customers with appropriate active Priority Support entitlement to the Intel Registration Center and, for versions older than those directly listed, to the Online Service Center. Intel also notes that some old licensed installers require a legacy `.lic` file / alternate activation route.

Therefore PREP02 must not obtain this compiler from an unverified third-party mirror merely to make the blocker disappear.

## Preferred acquisition order

1. **Institutional WUR/Alterra archive**
   - locate an archived ANIMO development VM, workstation image, software archive, installer cache, license archive or build log from the 2011-2016 development period;
   - search specifically for `w_fcompxe_2011.6.233.exe`, Intel Composer XE 2011 Update 6, `ifort.exe`, `.vfproj`, `.sln`, `.props`, `.bat`, `.cmd`, build logs and `animo41.exe`;
   - preserve exact hashes and provenance before execution.

2. **Historical ANIMO release/build artifacts**
   - locate a trusted `animo41.exe` or neighbouring 4.1.x executable together with provenance sufficient to identify source/release lineage;
   - a binary without provenance is useful diagnostic evidence but is not automatically a reference.

3. **Intel entitlement route**
   - if WUR has a historical Intel software entitlement with active Priority Support, request the exact Composer XE 2011 Update 6 package through Intel's supported channels;
   - record installer hash, entitlement provenance and license/activation method in controlled evidence storage, not in public GitHub.

4. **Reconstructed clean VM**
   - construct a disposable Windows VM compatible with the compiler generation;
   - install the verified Intel package and required Microsoft linker/SDK environment;
   - keep the VM isolated from production networks because the toolchain is obsolete and unsupported;
   - freeze VM configuration, tool hashes and environment variables used for qualification.

## Native qualification matrix once acquired

Run in this order:

- I12-A: compiler defaults, only options strictly needed to compile;
- I12-B: I12-A plus eight-byte default REAL, candidate `/4R8` or equivalent;
- I12-C: I12-B plus PowerStation I/O compatibility, candidate `/fpscomp:ioformat`;
- I12-D: storage sensitivity only if required, comparing Intel default storage with `/Qsave` rather than assuming `/Qsave`.

Primary first testcase remains `RuurloGrass`.

A build that completes is not sufficient. Capture complete compiler/link command lines, environment, exact input/hydrology hashes, output inventory, warnings, STOP behaviour and repeated-run determinism.

## Public-search result

A targeted public-web search on 2026-09-08 located Intel evidence for the exact compiler/package generation and Intel's supported legacy-access route. It did **not** locate a trustworthy public ANIMO 4.1.5 executable, ANIMO project file or official ANIMO 4.1.5 binary release package.

This is a search observation only. It does not prove that such artifacts do not exist in WUR archives, private project storage, former developer systems or other controlled repositories.

## Sources used for acquisition planning

- Intel Community, examples showing compiler `12.1.0.233 Build 20110811` for Intel64 and IA-32.
- Intel Community, package ID `w_fcompxe_2011.6.233`, Composer XE 2011 Update 6.
- Intel Community, 2011 installation report naming `w_fcompxe_2011.6.233.exe`.
- Intel, "How do I get an older version of an Intel Software Development Product?", updated 2025-05-02.
- Intel, Software Download FAQ and Priority Support FAQ, current access policy for unsupported legacy products.

## Gate

`BLOCKED_HISTORICAL_REFERENCE_ENVIRONMENT_REQUIRED`

The blocker is now operationally specific, but it is not resolved until a trusted native executable or usable verified historical compiler environment is actually acquired.
