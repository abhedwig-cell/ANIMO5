# GNU Fortran compatibility probe

Evidence class: diagnostic experiment only. This is not the frozen legacy source and not a qualified reference build.

## Environment

- GNU Fortran 14.2.0
- source candidate: supplied `ANIMO_4.1.5.53(3).zip`, SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- historical toolchain declared by `Version.inc`: Intel Visual Fortran Composer XE 12.1.0.233, Intel 64

## Source-form finding

The `.for` suffix must not be interpreted as proof of fixed-form source. The source uses free-form continuation and modern declarations. A GNU probe using fixed form produces extensive syntax failures. A probe using `-ffree-form -ffree-line-length-none` is consistent with the observed source syntax.

## Platform/toolchain dependencies found

1. Include-name case assumes a case-insensitive filesystem, for example source files named `Param.inc` / `Animo.inc` while include statements also use lower/mixed-case spellings.
2. `Animo.for` uses Intel `dfport`/`secnds` timing functionality.
3. `Function.for` relies on `KINT` and `KIDNNT`, not provided by GNU Fortran as used in this probe.
4. `Outsel.for` contains a nested implied-do WRITE-list form rejected by GNU Fortran 14.2.

These are compatibility findings. They are not by themselves scientific defects.

## Probe build result

For investigation only, the following changes were made in a separate temporary copy, never in the frozen archive:

- case aliases for include names;
- a minimal compatibility shim for `dfport/secnds`;
- a minimal compatibility shim for `KINT`/`KIDNNT`;
- a targeted GNU-only rewrite of the rejected `Outsel.for` implied-do output-list syntax;
- selection of `input1.for` instead of `input1_1.for`, and `Outsel.for` instead of `Outselorg.for`, based on compatibility with the main-program signatures.

With those probe-only adaptations, the selected 58 Fortran compilation units compile and link under GNU Fortran 14.2. The resulting executable is a portability experiment, not a behavioural reference.

Strict compilation emits a large diagnostic set, especially around implicit interfaces and legacy calling conventions. Individual diagnostics must be triaged source-bound before any is classified as a defect.

## Runtime probe

A testbank run can pass initial text-input parsing only after probe-only Windows-path/case normalization and one parser compatibility adaptation. It subsequently fails while reading the binary hydrology input (`SWATRE.UNF`) under GNU sequential-unformatted I/O.

Therefore:

- native historical build reproduction: `NOT_REPRODUCED`;
- GNU portability feasibility: `PARTIALLY_DEMONSTRATED_WITH_NONREFERENCE_SHIMS`;
- testcase behavioural reference: `NOT_ESTABLISHED`;
- binary hydrology format/runtime compatibility: `BLOCKER`.
