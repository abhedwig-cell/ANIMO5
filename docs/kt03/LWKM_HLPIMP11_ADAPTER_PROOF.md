# ANIMO-KT03 LWKM Hlpimp=11 Adapter Proof

Status: `BOUNDED_REAL_FILE_ADAPTER_EVIDENCE`.

## Purpose

CranMais established the first real file-to-typed reconstruction path but exposed a legacy `Hlpimp=1` ambiguity: the producer record does not carry `Sict`, while downstream `Hydro_detailed` consumes the interception-storage change.

KT03 does not resolve that scientific/source ambiguity by invention. Instead, the second bounded proof uses a supplied case whose legacy layout actually carries the required state.

Selected case:

`LWKM_gras_1040.2021.2045`

Frozen hydrology member:

`ANIMO_testbank/LWKM_gras_1040.2021.2045/input/SWATRE.UNF`

SHA-256:

`b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c`

## Byte-derived layout

The frozen file contains:

- 23417 logical PowerStation records;
- 17 static/header records;
- `Hlpimp=11`;
- 30 layers;
- 30 horizons;
- 5 drainage systems;
- a dynamic group size of 13 records per timestep;
- 1800 complete dynamic timesteps;
- a producer-temperature record that activates the `Ioptte=1` path.

The first dynamic record therefore has the 19-value SWAP3 layout that explicitly includes `sSict` between groundwater level and ponding storage.

## Interval evidence

This case is materially stronger than the daily CranMais probe because its producer timestep is variable.

The parsed interval sequence begins:

- `Tiwa=10`, `St=10`;
- `Tiwa=20`, `St=10`;
- `Tiwa=31`, `St=11`.

It ends at:

- `Tiwa=18263`, `St=11`.

Across all 1800 packets, exact decimal reconstruction of `Tiwa-St` equals the preceding accepted producer endpoint. The observed step-duration set is:

`{8, 9, 10, 11}` days.

This proves that the typed carrier is not intrinsically a daily-file abstraction. It can preserve a variable external interval identity without moving timestep-selection policy into the carrier or the model-neutral runtime.

## Defined downstream seam

All 1800 Hlpimp=11 packets contain an explicit interception-storage endpoint. Therefore the typed packet can expose the complete file-derived subset needed by the current `Hydro_detailed` call surface, including:

- surface and atmospheric water terms;
- `Flab`;
- five `Fldr` rows of 30 layers each;
- `Flev`;
- `Mofrt`;
- ponding and snow storage;
- timestep duration;
- `Sict`.

All 1800 packets pass the prototype's `hydro_detailed_boundary()` completeness gate. No groundwater sentinel below `-9.98` occurs in the frozen file.

The temperature record is also present for all packets and is represented separately from the `Hydro_detailed` file-derived projection because temperature is not part of that subroutine's argument surface.

## Provenance anchors

Dynamic logical-payload SHA-256:

`de32500b518da0994d4578ff7e92388c170b63c9df2e5f4820cf3304a1378c9a`

First dynamic record-group SHA-256:

`2e5e8ff7c088ddd94f91aeb663ea10abdecfda0ac4cd418a8bf90be955389ec7`

Last dynamic record-group SHA-256:

`37cf898001765e1524b4427c87f39cf88a01c3be4367a68db44f91b2db921b7e`

The full machine-readable probe is stored in:

`reference/kt03/LWKM_HYDROLOGY_PROBE.json`.

## Evidence boundary

The adapter's REAL(4)-to-working-value conversion uses the same diagnostic `Dble_trunc` reimplementation as the first KT03 probe. This remains:

`B1_DIAGNOSTIC_ADAPTER_PROBE_NOT_B2`

KT03 does not claim independently recovered historical Intel numerical semantics from this evidence.

## Consequence for KT03-F01

The Hlpimp=11 proof changes the architectural interpretation of KT03-F01.

KT03-F01 remains a real unresolved source/layout gap for `Hlpimp=1`. It must remain fail-closed and may require a separate scientific/source disposition before that legacy layout can be driven through the complete typed downstream seam.

It is no longer a blocker to proving the architecture itself, because the supplied Hlpimp=11 case demonstrates that the same typed contract can carry a complete real legacy hydrology packet into the unchanged `Hydro_detailed` boundary when the producer data are actually defined.

No correction to `Hlpimp=1` is implied by this result.
