# ANIMO-BUILDQ04 diagnostic reproduction

These assets qualify the revision-53 `GHGasses` lower air-boundary first-use seam. They are B1 diagnostics only and do not alter frozen source or admit a correction.

Frozen identities:

- source ZIP SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

Local qualification compiler: GNU Fortran 14.2.0 with eight-byte default REAL.

## First-read probe

`buildq04_uninitialized_first_read_probe.f90` preserves the revision-53 `La` update and `Flair` fill pattern and reads the same lower slot used by the transformation.

Representative commands:

```text
gfortran -O0 -fautomatic -finit-real=snan -fdefault-real-8 -fdefault-double-8 \
  tools/buildq04/buildq04_uninitialized_first_read_probe.f90 -o buildq04_uninit_O0.exe
./buildq04_uninit_O0.exe

gfortran -O2 -fautomatic -fdefault-real-8 -fdefault-double-8 \
  tools/buildq04/buildq04_uninitialized_first_read_probe.f90 -o buildq04_uninit_O2.exe
./buildq04_uninit_O2.exe
```

The source SHA-256 is:

`12d3b924c4d5b456b8e6dee5f5e5937f2be2a25cd0ab382cf1ccf792232eb4d5`

The qualification does not require a specific garbage value. The semantic point is that no source assignment exists and observed values depend on build/runtime conditions.

## Explicit boundary sensitivity probe

`buildq04_boundary_sensitivity_probe.f90` assigns only the otherwise missing lower interface value diagnostically and evaluates the revision-53 air-flow transformation plus the exact connected bottom advection and `Y3` identities.

```text
gfortran -O0 -fautomatic -finit-real=snan -fdefault-real-8 -fdefault-double-8 \
  tools/buildq04/buildq04_boundary_sensitivity_probe.f90 -o buildq04_boundary_O0.exe
./buildq04_boundary_O0.exe > buildq04_boundary_O0.out

gfortran -O2 -fautomatic -finit-real=snan -fdefault-real-8 -fdefault-double-8 \
  tools/buildq04/buildq04_boundary_sensitivity_probe.f90 -o buildq04_boundary_O2.exe
./buildq04_boundary_O2.exe > buildq04_boundary_O2.out
cmp buildq04_boundary_O0.out buildq04_boundary_O2.out
```

The qualified GNU 14.2.0 outputs contain 60 rows and are byte-identical, with SHA-256:

`fb98a0d17f3e9295f919c60f2decf7bde584a4f8fdccee85ce0501b5240ce756`

Probe source SHA-256:

`55d075a53338108e257c95c9f18722b5e69adcf22d477c76c2863b592e7ad5c3`

The tested boundary values are diagnostic sensitivity values. They are not historical ANIMO inputs. The scientifically qualified local source contract is the zero lower air-advection boundary described in `docs/build/GHG_BOTTOM_BOUNDARY_INITIALIZATION_QUALIFICATION.md`.

## CI boundary

The GitHub workflow recompiles the persisted probes on the runner and checks structural properties such as O0/O2 equality for the explicit-value matrix and NaN exposure in the O0 signalling-NaN first-read probe. It does not promote the runner compiler to historical reference status.
