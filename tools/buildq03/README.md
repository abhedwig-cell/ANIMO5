# BUILDQ03 diagnostic reproduction assets

These files support B1 runtime-semantic qualification only. They are not production patches and do not alter the frozen revision-53 source or testbank.

## Frozen evidence

- source ZIP SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank ZIP SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- compiler used: GNU Fortran 14.2.0
- diagnostic numerical kind contract: eight-byte default REAL, matching the PREP01 GNU compatibility contract

## Persisted diffs

- `GHGPONDING_EXPLICIT_CONTEXT.patch`
- `GHGTRANSSUB_EXPLICIT_CONTEXT.patch`
- `GHGTRANSPORT_EXPLICIT_CONTEXT.patch`

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

## Admission boundary

The diffs show one possible explicit-context representation used to test equivalence. They do not define the production API and do not authorize source correction, corrected-legacy admission, persistent ModelState allocation, or historical Intel equivalence.
