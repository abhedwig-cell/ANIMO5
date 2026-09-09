# BUILDQ03 diagnostic reproduction assets

These files support B1 runtime-semantic qualification only. They are not production patches and do not alter the frozen revision-53 source or testbank.

## Frozen evidence

- source ZIP SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank ZIP SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- compiler used: GNU Fortran 14.2.0
- diagnostic numerical kind contract: eight-byte default REAL, matching the PREP01 GNU compatibility contract

## Persisted diffs and probes

- `GHGPONDING_EXPLICIT_CONTEXT.patch`
- `GHGTRANSSUB_EXPLICIT_CONTEXT.patch`
- `GHGTRANSPORT_EXPLICIT_CONTEXT.patch`
- `GHGASSES_PHASE_PROJECTION_PROBE.f90`
- `ghgasses_phase_original.f90`
- `ghgasses_phase_explicit.f90`
- `ghgasses_phase_original_boundary_control.f90`
- `ghgasses_phase_explicit_boundary_control.f90`
- `ghgasses_phase_driver_original.f90`
- `ghgasses_phase_driver_explicit.f90`

The CH4 and N2O explicit-context probes are recorded by source/output hashes in `docs/build/GHG_EXPLICIT_CONTEXT_QUALIFICATION.md` and `integration/animo-build/BUILDQ03_GHG_CONTEXT_MATRIX.json`. Their larger diagnostic diffs remain B1 evidence and are not production patches.

## Source-format normalization used only for combined transport diagnostics

Revision-53 fixed-form sources contain a mixed continuation convention: column-6 continuation plus redundant trailing ampersands, and some source lines extend beyond column 72. For the isolated `GHGtransport`/`GHGtranssub` GNU harness, a syntax-preserving diagnostic copy was made by:

1. retaining the column-6 continuation markers;
2. removing only redundant trailing ampersands, also when immediately followed by an inline `!` comment;
3. compiling the normalized fixed-form copy with line length 132;
4. supplying the same revision-53 dimension parameter values needed by the isolated routines.

No executable equation, branch condition, coefficient expression or task ordering was changed in the retained/static reference variant.

This normalization means the combined transport reference is source-equivalent diagnostic evidence, not a byte-exact copy of the frozen source file. The qualification documents preserve that distinction.

## Key diagnostic hashes

### GHGponding

- exact isolated source: `5de27ef4688f4a4d21a534c931d2d437aafbcba3df22f9e2114f7902e4c979ca`
- explicit snapshot source: `9f733396dd96e17e1bb7caa748d65012af8a0abd1b34525b3a354f4dbb9c28bd`
- retained/static and explicit-context output: `b7284678e9658b48ac6f77d8aeb71639350c4c43db810741525acd94baa1afef`

### CH4oxid

- exact diagnostic unit: `43a77989e7d0e8bf3e1fa8370a009bb2334252c2965746ad4b7c6225e8889362`
- explicit-context unit: `f1def7438038d332876abdbab889db05e0e1114114d4a52942e51e9b727fee73`
- retained/static and explicit-context output: `c01bba7b40652cbd38e1c3199a0e244db0f70cce6f08a0771c8741a18974e54c`

### N2Oproreduc / NO3N2OReduc

- exact diagnostic unit: `aa2b1b3ef84f78c0275310aaf76fbb1292f789c925a8f3c5fe6c8eb5c85d28aa`
- explicit-context unit: `ea1aafa987487f6a5aef323459ec5e864d6325f17bfb9a5ed5dc71e2783b7cab`
- retained/static and explicit-context output: `ffb0c1fb1f7471ac9d50d214717ce1bcc520fdf2fbb5e91e223d3a5ec52f88b4`

### GHGtranssub

- normalized reference unit: `42eb241ee570e83eb4e55151b107a4c97b8730db81c613ae28218d89430f3420`
- explicit-context unit: `6adb9df1eee8729a476b18b620074d40aea44648bb404a8d1109411daeb92ae8`
- retained/static and explicit-context output: `54bb8578d13d1f65ee156c2bb6aa7ec105656d8528178f38a867849d2dbb3e8b`
- original automatic-storage output: `f7ee8df3bfe131e05b8119e519c65f5c221f58b018b500ed40196baade9ceca4`

### GHGtransport plus GHGtranssub

- normalized retained/static reference unit: `c6146280c53b6c08890e5ecc5ce22a8374f9350908e674f4e040d72482dfbff0`
- explicit combined context unit: `63575307aa170187b68b3e20d116c535b02a5d4984c2f88195ad531a5e078f12`
- retained/static and explicit-context output: `5ead8015d31cfe0ae58a8a9d3fecb49f5059c31c674c9af2824c0d131f709afc`
- original automatic-storage output: `b3f0b2a71608e132a1fe5ac67f1fd42b2f308cef06ca0c0b77bfe3f3678f7d1b`

### GHGasses retained versus explicit phase context

The 16-case cross-call matrix is described in `docs/build/GHGASSES_PHASE_CONTEXT_AND_BOTTOM_BOUNDARY_PROBE.md`.

- hidden-local projection kernel: `f6161e49bbfa62d7a0d2368cd49d43cde1291aa1c22580aff71cdf9b4e3e65ab`
- explicit-context kernel: `dcf1c2923c5e49218cf69350b903fc10476e1bad383d879e87d84ee48f47e482`
- retained kernel with diagnostic `Flair(Nl+1)=0.0` control: `bf5d3a368d3ee2f9e36d651e207814a25a31510f8b8bcf4df92228ce4f94f6d3`
- explicit kernel with the same diagnostic control: `2439d63bfe2dc9753dff7d302f7434117265609512ffc4832c59e08646eab9b2`
- retained driver: `107196e03c3fd1c06b667ea1ac1782e54fde5f2c7c6c908c54f3d6cdbfc242f3`
- explicit driver: `900e2e477e69c416b544655b1669a9ae2009802ba1833f02d0456aae3d9212a6`
- retained/static and boundary-controlled explicit-context output: `c4f47a3e09b6087a37d7351dcea62aa103a4e2421e1a018693eba8d9edbfcc55`
- automatic hidden-context output: `411f2ee264dbdb4c3f5bd80eed58e17f131f610512bb57d7545113335febdc46`

Example reproduction of the isolated storage-duration comparison:

```text
gfortran -O0 -fno-automatic -fdefault-real-8 -fdefault-double-8 \
  tools/buildq03/ghgasses_phase_original_boundary_control.f90 \
  tools/buildq03/ghgasses_phase_driver_original.f90 -o ghgasses_static.exe
./ghgasses_static.exe > static.out

gfortran -O0 -fautomatic -finit-real=snan -fdefault-real-8 -fdefault-double-8 \
  tools/buildq03/ghgasses_phase_explicit_boundary_control.f90 \
  tools/buildq03/ghgasses_phase_driver_explicit.f90 -o ghgasses_explicit.exe
./ghgasses_explicit.exe > explicit.out
sha256sum static.out explicit.out
```

The two files should both hash to `c4f47a3e09b6087a37d7351dcea62aa103a4e2421e1a018693eba8d9edbfcc55` for the qualified controlled matrix.

The versions without the boundary control preserve the separate `Flair(Nl+1)` first-use hazard. The boundary-controlled versions isolate the cross-call storage-duration question. `Flair(Nl+1)=0.0` is a diagnostic control, not an admitted source correction.

### Independent GHGasses deterministic reprojection matrix

`GHGASSES_PHASE_PROJECTION_PROBE.f90` independently reconstructs the phase projection twice from the same explicit inputs after stack clobbering. Its source SHA-256 is:

`5d002a3bc969f36bf3e6fa0a48c66cb6e88f3f00fa9bf3c4c64ae9c72ed44bef`

GNU O0 and O2 each produce 64 byte-identical output lines with SHA-256:

`5a532e79df994fb29019d74ad7e5cbdf7dc1a73ea6e7c5743c0b810a591cfbe3`

This is supplementary evidence that the projection is deterministic under invariant explicit inputs. It does not replace the qualified explicit phase-context representation and does not prove full legacy call-graph input invariance.

## Admission boundary

The diffs and probe kernels show diagnostic explicit-context representations used to test equivalence. They do not define the production API and do not authorize source correction, corrected-legacy admission, persistent ModelState allocation, historical Intel equivalence, or the `Flair(Nl+1)` boundary initializer as intended science.
