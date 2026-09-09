# BUILDQ02 diagnostic probes

These files reproduce the controlled GNU evidence used by ANIMO-BUILDQ02. They are diagnostic qualification material only. They are not production ANIMO source.

Required frozen source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Compiler used for recorded evidence:

`GNU Fortran 14.2.0`

The revision-53 source expects case-insensitive include lookup. On a case-sensitive diagnostic extraction, create a temporary alias `param.inc` to the frozen `Param.inc`. This is the already qualified PREP01 platform adaptation and must not modify the archived bytes.

Common flags:

```text
-I<revision53-source-directory>
-ffree-form
-ffree-line-length-none
-std=legacy
-fdefault-real-8
-fdefault-double-8
```

`MAPOHYDRO_SAFE_DIAGNOSTIC.patch` is intentionally stored under `tools/buildq02`. Apply it only to a temporary copy of frozen `MAPOHYDRO.FOR` after verifying the source archive hash. It contains two separate diagnostic hypotheses:

1. reconstruct `LnBoMpMx` from explicit `LnBoMp(1:2)` at Task 4;
2. structurally sequence already-present bounds and layer-zero distinctions so invalid array coordinates are not evaluated speculatively.

Neither hypothesis is an admitted source correction.

## Storage probe

Compile `mapohydro_storage_driver.f90` against unchanged `MAPOHYDRO.FOR` with both static and automatic storage, then against the patched temporary copy.

The recorded BUILDQ02 evidence uses O0 and O2. Automatic unchanged source must not be treated as an oracle because its result depends on retained local contents.

## 64-case matrix

Compile `mapohydro_matrix_driver.f90` against:

- unchanged source with `-fno-automatic` at O0 and O2;
- patched temporary source with `-fautomatic` at O0 and O2;
- both applicable bounds-checking variants;
- patched source with `-finit-real=snan` plus bounds checking.

The recorded complete stdout SHA-256 for every listed variant is:

`16dc28adce374a956e77dc17420d814b64bf112ae3ff5524afe2422cb29433e3`

No output normalization is applied.

## Modflux-coupled Task-2 probe

Compile both unchanged `MAPOHYDRO.FOR` and unchanged `MODFLUX.FOR` with `mapohydro_modflux_coupled_driver.f90` and `-fcheck=bounds`.

Mode `1` generates `Sqnu=[1,0,2]` through `Modflux` and exposes the Task-2 backward-scan `FlMpInEf(...,0)` read in unchanged MAPOHYDRO.

Mode `2` also generates `Sqnu=[1,0,2]`, but with an outgoing-flux range spanning layer zero, exposing the later `CoStat` branch `FlMpInEf(...,0)` read.

The patched temporary MAPOHYDRO completes both modes under bounds checking. This demonstrates runtime-domain sequencing, not historical Intel behaviour.

Machine-readable recorded results are in:

`integration/animo-build/BUILDQ02_MAPOHYDRO_RUNTIME_MATRIX.json`
