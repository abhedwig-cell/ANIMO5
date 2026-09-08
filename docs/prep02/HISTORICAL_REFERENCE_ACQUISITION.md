# ANIMO-PREP02 historical reference acquisition packet

Status: `ACTIONABLE_EXTERNAL_REFERENCE_ROUTE_IDENTIFIED_ARTIFACT_NOT_YET_OBTAINED`.

## Why this packet exists

PREP02 cannot promote the reproducible GNU diagnostic build to behavioural reference status without an independent historical anchor.

Inspection of the supplied frozen archives found:

- no Visual Studio/Intel Fortran project or solution file;
- no build log containing the original release flags;
- no native ANIMO executable;
- testcase runner scripts that refer to `animo41.exe`, but that executable is absent.

The source itself identifies:

`Intel Visual Fortran Composer XE 12.1.0.233 [Intel(R) 64]`

The GNU runtime-contract probe also shows that default REAL kind, DOUBLE PRECISION kind and local-storage duration are behaviourally material. Reconstructing an arbitrary Intel build is therefore not enough.

## Public WUR acquisition lead

The current public WUR ANIMO product page was checked on 2026-09-08:

`https://www.wur.nl/en/research/products-services/animo`

The page states that an executable is available upon request, describes ANIMO as normally distributed as an executable release, and says that information about programme code or model availability is obtainable via Leo Renaud.

The same page contains clearly historical platform wording, including references to MS-DOS and older platforms. Therefore it is an acquisition lead, not proof that revision 4.1.5 revision 53 is currently downloadable or still retained.

## Preferred artifacts, in order

### A. Exact historical release executable

Highest-value artifact:

```text
ANIMO 4.1.5 revision 53 executable
historical runner name: animo41.exe
```

Required provenance where available:

- release/version identifier;
- creation or release date;
- original filename;
- originating archive, share, release directory or maintainer record;
- whether it was the executable used with the supplied testcase family;
- platform/architecture;
- SHA-256 calculated immediately after receipt.

The executable must be retained in a controlled evidence location. Public GitHub need contain only hashes and provenance unless redistribution is explicitly permitted.

### B. Original Intel project/build metadata

Request any available:

- `.sln`;
- `.vfproj` or related Intel Fortran project file;
- release configuration export;
- build log;
- compiler command line;
- linker command line;
- compiler property screenshots or archived notes.

The following settings are particularly important because PREP01/PREP02 show behavioural sensitivity:

- default REAL size;
- DOUBLE PRECISION size/semantics;
- local variable storage duration, including `/Qsave` or equivalent project behaviour;
- PowerStation-compatible unformatted I/O settings, including `/fpscomp:ioformat` or equivalent;
- optimisation and floating-point model;
- source-unit selection, especially `input1.for` versus `input1_1.for` and `Outsel.for` versus `Outselorg.for`;
- preprocessing, alignment and calling-convention settings.

### C. Historical Ruurlo output bundle

If a trusted executable cannot initially be supplied, an archived output tree produced by that executable for the supplied `RuurloGrass` case is still useful.

Prefer:

- complete generated file set;
- `message.out`;
- balance files;
- concentration/state output;
- run date and executable identity;
- input bundle identity;
- any batch file or run log tying the output to the executable.

This is weaker than possessing the executable, but it can provide an independent comparison surface.

### D. Nearest retained ANIMO release

If exact revision 53 is unavailable, request the nearest retained 4.1.x executable plus exact version/revision provenance.

Such an executable must not be silently treated as revision-53 truth. It can only support a version-delta qualification chain after source/input differences are identified.

## Minimum first qualification once an executable is obtained

Use `RuurloGrass` first.

Required controls:

1. preserve the received executable bytes and calculate SHA-256;
2. run on a compatible Windows/runtime environment;
3. use the frozen testcase files without GNU text/path translation;
4. identify the exact hydrology bytes used;
5. record exit/STOP behaviour and the complete message stream;
6. hash the complete generated output file set;
7. compare the native output with the GNU diagnostic build at compatibility and numerical levels;
8. do not define a global tolerance from observed differences;
9. classify each difference by variable, unit, formatting precision and compiler/runtime semantics.

Passing this first case may support:

`QUALIFIED_MINIMAL_NATIVE_REFERENCE_BUILD_CONTRACT`

It does not yet qualify all ANIMO processes.

## If build metadata is also obtained

A same-compiler observer-only build becomes possible after the ordinary historical build has been reproduced.

That observer build should add high-precision evidence streams without altering ordinary output or process state, as defined in `REFERENCE_QUALIFICATION_PLAN.md`.

## Suggested request wording

The technical request should ask specifically for historical qualification material, not simply "the newest ANIMO".

Requested minimum:

```text
ANIMO 4.1.5 revision 53, preferably the historical animo41.exe used with the
4.1-era testcase set, plus any retained Intel Visual Fortran project/build file
or release build log. We only need it for controlled behavioural qualification
of a modernization effort and can retain the binary in a controlled location.
```

If revision 53 is unavailable, ask which 4.1.x release is retained and whether the revision/build provenance is known.

## Current gate

An actionable acquisition route is now identified, but no independent native artifact has yet been obtained.

PREP02 remains:

`BLOCKED_HISTORICAL_REFERENCE_ENVIRONMENT_REQUIRED`.

Production migration remains `NOT_ADMITTED`.
