# ANIMO-PREP02R — Historical Reference Environment Recovery & Reference Admission

Status: `WORK_UNIT_RESERVED_REFERENCE_RECOVERY_ONLY`.

## Purpose

Recover or obtain an independently trustworthy historical reference environment for the frozen ANIMO 4.1.5 revision-53 lineage, then admit reference behaviour only if provenance and native execution evidence support it.

Frozen source identity:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Frozen testbank identity:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Documentation identity:

`ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`

Current GNU diagnostic executable identity:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

The GNU executable remains `DIAGNOSTIC_NOT_REFERENCE`.

## Intended work

- verify PREP02 status and acquisition records against the live source-bound baseline;
- search repository evidence, supplied source/testbank metadata, WUR/Alterra public material and explicit historical contact routes for native executables, build metadata or executable-linked output;
- register every candidate with version/revision, date, toolchain, hash when bytes are available, provenance strength, relation to revision 53 and trust class;
- if a qualified executable is obtained, run a compatible frozen testcase natively, preferably `RuurloGrass`, without silent compatibility translation;
- capture full inputs, runtime environment, output tree, warnings, exit status and hashes;
- compare native reference behaviour with the GNU diagnostic route by difference class, without inventing a global numerical tolerance;
- reconstruct native build semantics only from evidence;
- design observer-only unrounded capture only after a native build/reference contract exists.

## Hard exclusions

Physics change: no.

Numerical-policy change: no.

Corrected-legacy fixes: not admitted.

Frozen source/testcase modification: not admitted.

Production migration: not admitted.

Rounded report output alone is not a numerical oracle.

A reproducible GNU run is not independent historical truth.

## Verification contract

Reference admission requires independence plus provenance. A historical executable with weak or unknown lineage can be retained as diagnostic evidence but cannot silently become revision-53 truth. A nearby 4.1.x release must be treated as a distinct lineage until version-delta evidence closes the gap.

## Checkpoint boundary

This reservation is persisted before external acquisition/research and before any native execution attempt. PREP02 remains blocked until independent historical evidence is actually obtained and qualified.
