# ANIMO-KT03 Work Unit Contract

Workunit: `ANIMO-KT03 — Real ANIMO Hydrology-Step Adapter Boundary Qualification`.

Execution discipline: `RECONCILE -> ACQUIRE -> SPECIFY -> PROTOTYPE -> QUALIFY -> CLOSE`.

This is a bounded real-model adapter workunit. It may create nonproduction adapter/probe code, tests, CI and evidence. It may not modify ANIMO scientific equations, alter historical hydrology semantics, open B4, admit production migration, create SWAP5-ANIMO production coupling or extract a separately versioned shared runtime library.

## Purpose

KT02 proved that one model-neutral transient runtime can serve two materially different synthetic clients. KT03 is the first real-model test of that abstraction.

The question is deliberately narrower than full ANIMO migration:

> Can the legacy per-timestep SWAP/SWATRE hydrology input boundary be represented as an explicit typed ANIMO adapter contract, while keeping downstream ANIMO hydrology transformation and scientific process semantics unchanged and preserving a file-backed legacy path?

A positive KT03 result is evidence that the shared runtime abstraction survives contact with one real ANIMO boundary. It is not evidence that all ANIMO state is transactional or that online SWAP5 coupling is ready.

## Frozen consumed authorities and evidence

- closed KT02 handoff: `ANIMO-KT02@1f88db4dc87fc4d93075884ac35a59711f0725bf`;
- KT02 frozen executable: `1909709e7a244b5d0ee53342a26bab74815c118c`;
- KT02 qualification CI: run `35278517691`, `SUCCESS`;
- legacy ANIMO source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- legacy ANIMO testbank archive SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- `Animo.for` SHA-256: `352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7`;
- `Input_hydro.for` SHA-256: `5f07ce68969d749308595d6b4f9f789b6b3646ae226c233e2f8e49565a7dad64`;
- `Hydro_detailed.for` SHA-256: `f3b8adc7ae56fc6f7002ce667c15288511984423e66ca619ccb4e90622bfbf5d`.

These source hashes agree with `reference/source/source_manifest.csv` for the revision-53 archive.

## First bounded testcase

The first adapter proof targets `CranMais` because it is a supplied multi-layer detailed-hydrology case with a SWAP-style unformatted hydrology file and without active P, macropore or GHG options in `GENERAL.INP`.

Pinned testcase members:

- `CranMais/Input/Swatre.unf`: SHA-256 `538827d517f7be4c060e2d62131e1942f8e0e76fdeae49dc0268486984cc9eaf`;
- `CranMais/Input/GENERAL.INP`: SHA-256 `e514e50020f7d73d2695b359c4b956117b0161d862c375f03a3ae8b95ca43029`;
- `CranMais/animo.ini`: SHA-256 `5d1f62faf62747b7d91d3e9199e33954e3038ddd005259f32a8bca95f0c82bb8`.

The case is selected to reduce optional-feature confounding, not because its scientific outputs are automatically a qualified historical behavioural reference.

## Owned semantic surface

KT03 may own only:

- a typed representation of one normalized legacy hydrology timestep delivered to ANIMO;
- a file-backed adapter that reconstructs that representation from the frozen legacy `SWATRE.UNF` grammar for the bounded case;
- an in-memory/provider seam that can later receive the same typed representation without file I/O;
- provenance and exact interval identity needed to relate the hydrology packet to the transient runtime;
- tests proving file-backed versus typed reconstruction equivalence for the bounded input boundary;
- adapter-local validation of dimensions, finite values, record completeness and option/layout identity.

## Must remain legacy/scientific authority

KT03 must not silently move or rewrite:

- `Hydro_detailed` water-balance and hydrology transformation semantics;
- transport, reaction, uptake, crop, aeration, P, GHG or macropore process equations;
- ANIMO process ordering;
- scientific acceptance tolerances;
- SWAP5 solver or timestep policy;
- model-wide restart/state ownership;
- legacy option meanings or sentinel handling without an explicit qualification decision.

## Required proof before positive close

At minimum KT03 must demonstrate:

1. exact source-to-field provenance for the selected SWATRE timestep representation;
2. a typed hydrology-step carrier with no ANIMO chemical/process state;
3. a file-backed adapter and an independently supplied typed packet that are field-equivalent for bounded captured records;
4. downstream call compatibility with the existing `Hydro_detailed` input responsibility, without changing its scientific equations;
5. exact or explicitly classified differences in a bounded CranMais replay or probe;
6. no hidden file handle, parser cursor or adapter scratch in accepted scientific continuation state;
7. no dependency from the model-neutral KT02 runtime core on ANIMO/SWAP file grammar;
8. fail-closed behaviour on dimension/layout/provenance mismatch.

## Explicit nonclaims

A positive KT03 result does not by itself qualify:

- complete ANIMO production migration;
- a shared production runtime library;
- SWAP5 production adoption of KT02 exact time;
- online SWAP5-ANIMO coupling;
- joint timestep acceptance/rollback across SWAP5 and ANIMO;
- historical equivalence outside the bounded case and record/layout envelope;
- Status A or Status AA.
