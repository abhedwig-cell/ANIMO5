# ANIMO-KT03 Reconciliation and Acquisition

## Live starting state

KT03 starts from the closed KT02 head `1f88db4dc87fc4d93075884ac35a59711f0725bf`.

KT02 is closed with verdict:

`QUALIFIED_NONPRODUCTION_MODEL_NEUTRAL_TRANSIENT_RUNTIME_DUAL_CLIENT_PROTOTYPE_NO_PRODUCTION_LIBRARY_OR_MODEL_ADMISSION`.

Its status explicitly permits a separate real-ANIMO adapter workunit and does not permit production promotion or SWAP5-ANIMO production coupling.

No KT03 PR or equivalent real hydrology adapter workunit was found before branch creation.

Branch:

`work/animo-kt03-real-hydrology-adapter`

## Relevant KT02 inheritance

KT03 may consume KT02 only as design and nonproduction runtime evidence. In particular:

- accepted/candidate authority separation is a candidate runtime contract;
- private interval execution and publish-on-exact-completion are available as a nonproduction mechanism;
- scientific admissibility remains model-owned;
- exact time remains a nonproduction candidate rather than SWAP5 production authority;
- no generic transfer/event sidecar is assumed.

KT03 does not reopen KT02 and does not copy SWAP-specific policy into ANIMO.

## Legacy source acquisition

The frozen revision-53 source was inspected directly from the archive identified by SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`.

Three files define the immediate boundary:

- `Animo.for`: timestep orchestration and call order;
- `Input_hydro.for`: dynamic hydrology-file read and normalization;
- `Hydro_detailed.for`: downstream ANIMO detailed-hydrology transformation and water-balance responsibility.

The repository source manifest independently pins the same file identities.

## Observed timestep order

For the detailed hydrology route (`Iwa=2`), the legacy main loop performs, in relevant order:

1. determine/update the timestep length and time coordinates;
2. call `Init` to update ANIMO state variables from the previous step;
3. call `Input_hydro` to read the current hydrology timestep from the hydrology stream;
4. call `Hydro_detailed` to convert/check those hydrology inputs into ANIMO's internal water-state/flux representation;
5. continue with crop, transport, reaction, balance and output processing.

This matters because the safest first adapter seam is between steps 3 and 4. Replacing `Hydro_detailed` would change scientific/model semantics. Replacing only the file read while preserving its normalized outputs leaves that downstream responsibility in legacy authority.

## Selected bounded case

`CranMais` is selected for the first probe.

Observed configuration:

- `HydrologicInput=2`;
- `PhosphorusCycle=0`;
- `MacroPoreOption=0`;
- `GreenHouseGasOption=0`;
- `SoilTempFile=0` as declared by the case input;
- the unformatted hydrology file begins with SWAP-style textual header records rather than the older SWAP 2.x numeric header form seen in RuurloGrass.

This is a deliberate reduction in optional branches. It does not change the eventual need to support other admitted legacy layouts.

## Current verdict

`ACQUIRE_COMPLETE_BOUNDARY_IDENTIFIED_PROTOTYPE_NOT_YET_STARTED`.

The next permitted action is to specify the typed normalized hydrology-step carrier and build a nonproduction file-backed probe for a bounded CranMais record sequence. No production source modification is permitted at this checkpoint.
