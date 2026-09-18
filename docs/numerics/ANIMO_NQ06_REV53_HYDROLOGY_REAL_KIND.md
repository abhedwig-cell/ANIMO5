# ANIMO-NQ06 Revision-53 Hydrology REAL-Kind Qualification

## Question

Before implementing a bounded modern `Hydro_detailed` execution seam, ANIMO5 must know whether the revision-53 source algebra was intended to run as default single precision or default double precision.

NQ01 requires a separate qualification whenever precision kind changes. Guessing from the bare `REAL` declarations is therefore not acceptable.

## Evidence

The user-supplied Visual Fortran project file has SHA-256:

`f8ac40ea91df926a035396b0afe8584ea0d9c19711535a12b4f12634ce688b2a`.

All four configurations in that file specify:

`RealKIND="realKIND8"`

and:

`FloatingPointModel="source"`.

The configurations are:

- Debug Win32;
- Release Win32;
- Debug x64;
- Release x64.

The supplied executable has SHA-256:

`40e29853a0431cc7e2b787dfeb1870f44e1ff402b5aaebd6f56c8365fc5b178d`

and contains Intel Fortran runtime identification consistent with the supplied Visual Fortran lineage. The executable evidence is supporting only. It does not independently prove every project option used to build that exact binary.

The frozen revision-53 routines relevant to the current TCD-042 lane all declare their floating variables as default `REAL`, not with an explicit kind:

- `Hydro_detailed.for`;
- `MODFLUX.FOR`;
- `UBoundconc.for`.

Their exact source hashes are already present in the frozen source manifest.

## Qualification

Within the bounded current lane, `real64` is the justified source-build-configuration-matched candidate precision for new nonproduction implementations of these default-REAL equations.

This is stronger than an arbitrary modernization choice. The supplied build project explicitly promoted default REAL to kind 8.

It is still not B2 historical behaviour. In particular NQ06 does not prove:

- exact executable provenance from the supplied vfproj to the supplied exe;
- exact Intel instruction selection or reassociation;
- exact historical trajectory equivalence;
- cross-compiler bitwise identity.

Those remain separate evidence questions.

## Consequence

A future bounded HYDROEXEC workunit does not need to introduce a new binary32 versus binary64 policy choice. It may use `real64` as the qualified candidate representation, provided it preserves source evaluation order where that order is part of the claim and does not turn this build-metadata qualification into a historical-equivalence claim.

## Hard boundary

No tolerance is defined.
No production source changes.
No B3/B4/TB7 effect.
No B2 reference is created.
No source formula is changed.
