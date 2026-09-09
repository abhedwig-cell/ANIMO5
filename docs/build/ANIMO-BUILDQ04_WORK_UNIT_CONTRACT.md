# ANIMO-BUILDQ04 — GHG bottom-boundary first-use initialization qualification

Status: `STARTED_PERSISTED_BEFORE_EXTENDED_QUALIFICATION`

## Target

Local runtime finding inherited from BUILDQ03:

`BUILDQ03-LCL-GHGASSES-FLAIR-NLPLUS1-UNINITIALIZED`

Revision-53 `GHGasses` can read `Flair(Nl+1)` while constructing bottom-layer `Flaiio(Nl)` and `Flaiou(Nl)` without a preceding source assignment when the air-flow topology yields `La < Nl`.

## Authority

Base:

`work/animo-buildq03-ghg-task-context-qualification@5e06473bc2bb1df6cf4e449d8d6aa04da35c7d47`

Canonical relation:

- hidden GHG cross-call context remains existing `TCD-011` scope;
- this bottom-boundary finding is a separate conditional first-use initialization mechanism;
- BUILDQ03 requested B3 runtime intake but did not request a new TCD.

Frozen evidence:

- source ZIP SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- diagnostic compiler GNU Fortran 14.2.0.

## Questions

BUILDQ04 will determine, without changing production source:

1. the exact topology in which `Flair(Nl+1)` is first-read without assignment;
2. whether independent ANIMO-specific theory or source identities define the lower air-flow boundary value;
3. whether zero is derivable from the governing boundary/control-volume identity rather than merely a convenient initializer;
4. whether the first-use value is control-flow, state, flux or output material in controlled GHG transport diagnostics;
5. whether the phenomenon is best kept as a build/runtime hazard, mapped to an existing discrepancy family, or handed to B3 as a new scientific discrepancy candidate;
6. what explicit initialization/boundary contract a future implementation must satisfy.

## Hard boundaries

- no frozen source or testbank mutation;
- no assumption that compiler initialization is intended semantics;
- no assumption that `Flair(Nl+1)=0` is scientifically correct until independently derived;
- no blanket initialization flags as a fix;
- no automatic merge with TCD-011 or GHG TCD-032..037;
- no production correction, corrected-legacy admission or B3 admission.

## Planned evidence

- exact source-control-flow reconstruction;
- ANIMO-specific GHG gas-transport theory cross-check where available;
- controlled boundary-value sensitivity matrix separated from hidden-storage effects;
- downstream transport-coefficient/state materiality probe;
- fail-closed B3 handoff.

`production_migration_admitted=false`

`corrected_legacy_admitted=false`
