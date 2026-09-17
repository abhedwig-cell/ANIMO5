# ANIMO-KT05 Work Unit Contract

Workunit: `ANIMO-KT05 — Explicit-State HydrologyStep to ANIMO Hydrology Call-Boundary Adapter`.

Execution discipline: `RECONCILE -> IMPLEMENT -> QUALIFY -> REVIEW -> CLOSE`.

## Purpose

Build the first compiled Fortran adapter boundary that consumes the frozen, file-independent KT03 hydrology-step contract and projects its **explicit interception-state** form onto the external hydrology values required by revision-53 `Hydro_detailed`.

KT05 is deliberately independent of the unresolved Hlpimp=1 scientific disposition. It uses only the explicit-state semantics already evidenced by the Hlpimp=11 path.

The intended architecture remains:

`producer -> ANIMO_HYDROLOGY_STEP_V1 -> ANIMO-specific adapter -> Hydro_detailed responsibility`

The producer may ultimately be a legacy file adapter or an in-memory SWAP5 provider. The ANIMO adapter must not know PowerStation framing, `Hlpimp`, source-record hashes or SWAP solver policy.

## Frozen inputs

- KT03 closeout: `ANIMO-KT03@c5d4c14fbd4ce77ed5ef369bb8ecaee0709ea3b8`;
- frozen KT03 contract implementation: `e844c7658a95819fc0463c55737f9bd41b29a6da`;
- normalized schema: `ANIMO_HYDROLOGY_STEP_V1`;
- normalized unit contract: `ANIMO_HYDROLOGY_UNITS_V1`;
- revision-53 `Hydro_detailed.for` source SHA-256: `f3b8adc7ae56fc6f7002ce667c15288511984423e66ca619ccb4e90622bfbf5d`.

KT04 and KT03F01 are not scientific dependencies for KT05. Their explicit-state implementation work may be used only as non-authoritative design/test evidence.

## Owned surface

KT05 owns only:

1. a Fortran representation of the frozen normalized hydrology-step schema;
2. validation of schema identity, units, dimensions, finite values and explicit interception-state availability;
3. a typed ANIMO-specific projection containing only the file/producer-derived values that cross the `Hydro_detailed` call boundary;
4. tests proving that this projection is independent of legacy file grammar and rejects incomplete explicit-state input.

The projected values are the bounded external subset:

`Evicirr, Evicpr, Evpn, Evsn, Evso, Evsoma, Evtrma, Flab, Fldr, Flev, Mofrt, Pnt, Prirr, Prr, Prsn, Ru, Runon, Sict, Snt, St`.

## Scientific ownership

KT05 does **not** reimplement `Hydro_detailed` science.

In particular it does not own:

- runoff partitioning;
- `Dif` correction;
- `Evso` adjustment;
- accepted `Mofro`, `Pn`, `Snla` or `Sic`;
- macropore state;
- `Modflux`;
- water-balance acceptance;
- solute transport;
- timestep selection or retry policy.

Those remain ANIMO scientific/state responsibilities or separate qualified surfaces.

## Required proof

KT05 must establish:

1. the Fortran schema and unit identities remain aligned with KT03;
2. every projected field comes from the typed hydrology step and no legacy provenance leaks into the projected physical carrier;
3. explicit interception storage is mandatory for this workunit;
4. dimensions for `Mofrt/Flev/Flab/Fldr` fail closed;
5. non-finite values fail closed;
6. the frozen KT03 adapter tests remain green;
7. the Fortran adapter compiles under strict `gfortran -std=f2008 -Wall -Wextra -Werror`;
8. production `src/` and KT02 model-neutral runtime are untouched.

## Exclusions

No Hlpimp=1 or Hlpimp=2 semantic claim, no production source change, no full `Hydro_detailed` execution equivalence, no B2 historical compiler claim, no KT02 runtime integration yet, no SWAP5 production coupling, no B3/B4 admission and no Status A/AA claim.
