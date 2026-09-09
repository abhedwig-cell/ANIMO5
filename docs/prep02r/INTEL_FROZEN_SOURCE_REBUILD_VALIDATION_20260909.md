# ANIMO-PREP02R — Frozen-source Intel rebuild validation, 2026-09-09

Status: `FROZEN_SOURCE_INTEL_REBUILD_VALIDATED_ON_LWKM_RUURLO_RECEIVED_BINARY_DISCREPANCY_LOCALIZED`

## Purpose

Validate a newly rebuilt Intel x64 Debug executable produced from the frozen ANIMO 4.1.5 revision-53 source tree with the supplied Visual Fortran project metadata, before any observer instrumentation is introduced.

The validation deliberately uses only the untouched frozen testbank and compares ordinary executable behaviour against the previously received Intel-native `animo41.exe` capture.

## Artifact identities

Frozen testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Previously received Intel executable:

- SHA-256: `40e29853a0431cc7e2b787dfeb1870f44e1ff402b5aaebd6f56c8365fc5b178d`
- size: `6,778,368` bytes
- PE timestamp: `2026-05-27T13:41:28Z`
- embedded source/PDB root: `D:\USR\5200048928_SWAP_ANIMO\ANIMO\src_develop_for_20260519` / `x64\Debug`

New frozen-source rebuild:

- SHA-256: `da51093a9da7bd99caee9898c713ab78eda972e3ce6e4bf5b2b2cb66bdab9e0e`
- size: `8,536,064` bytes
- PE timestamp: `2026-09-09T14:19:47Z`
- embedded PDB path: `R:\AbV\intel_base\ANIMO_4.1.5.53\x64\Debug\animo41.pdb`
- embedded model identity includes `ANIMO: 4.1` and `file:///V:/svn_Animo/tags/animo4.1.5`
- embedded Intel RTL catalog string remains `V20.0-001 Jan 10 2019`
- linker major/minor remains 14.35 and imported DLL surface remains `KERNEL32.dll` plus `imagehlp.dll`

Validation ZIP SHA-256:

`5ee49ff81ebde22f41fb2db6daae24331371968f44388212ea597bef0e83b2b5`

## Cases

Two high-value frozen cases were run from a fresh extraction using the rebuilt executable:

1. `RuurloGrass`
2. `LWKM_gras_1040.2021.2045`

Both completed with legacy success `STOP 100` / process exit 100.

## LWKM comparison

The rebuilt executable reproduces the previously received Intel executable on the complete LWKM case tree.

The two case trees contain the same 67 files:

- 59 are raw byte-identical;
- 8 differ only in explicit runtime metadata lines;
- after normalizing those metadata lines, all 67 files are equal;
- no numerical tolerance and no scientific-value normalization are used.

The eight metadata-only files are:

- `Animoinputs.Out` — file-created timestamp only;
- `ammonium.out` — run-start timestamp only;
- `animointermediate.Out` — file-created timestamp only;
- `message.out` — run start, run end and elapsed time only;
- `miner-N.out` — run-start timestamp only;
- `nitrate.out` — run-start timestamp only;
- `pal-P.out` — run-start timestamp only;
- `pw-P.out` — run-start timestamp only.

Therefore the frozen-source rebuild is ordinary-output equivalent to the received Intel executable for the natural LWKM path relevant to TCD-015.

This materially strengthens the basis for a subsequent *derived observer build*: extra unrounded diagnostics can be added to the frozen source only after preserving this uninstrumented baseline identity.

It still does not itself create B2 or a historical reference.

## Ruurlo comparison

The rebuild changes the interpretation of the earlier Ruurlo finding.

Previously received executable:

- deterministic `STOP 1410` on day 1;
- upper-boundary `FLAB(0)` deviation `0.002400241 m/d`.

Frozen-source rebuild:

- deterministic successful completion through the full case horizon;
- `STOP 100`;
- no `FLAB(0)` interruption.

The rebuilt case produces 37 additional output files because execution proceeds beyond day 1.

This means the earlier finding must **not** be described generically as an `Intel-versus-GNU` discrepancy. A current Intel rebuild from the frozen revision-53 source completes the same Ruurlo case. The discrepancy is more narrowly:

`received 2026 Intel executable` versus `frozen-source Intel rebuild`.

The received executable's embedded source root `src_develop_for_20260519`, its different image size, and the behavioural mismatch materially reinforce the unresolved source-byte/build-provenance concern.

## Runinu source hazard

Frozen `Hydro_detailed.for` still contains a real runtime-semantics hazard:

- when `Ru < 0`, `Runinu = -Ru`;
- when `Ru > approximately 0`, `Runinu = 0` in the ordinary positive branch;
- in the near-zero branch `-1e-8 < Ru < 1e-8`, `Rupr`, `Rurv` and `Ruso` are assigned but `Runinu` is not assigned;
- `Runinu` is then consumed by the upper-boundary water-balance equations.

However, the successful frozen-source x64 Debug rebuild means this source hazard is **not yet proven** to be the internal cause of the received executable's Ruurlo stop. The supplied Debug x64 project metadata also requests saved local storage and zero initialization of saved scalars, which can suppress an uninitialized-local manifestation.

Therefore the correct current classification is a build/provenance-sensitive runtime hazard and causal hypothesis, not a proven Ruurlo root cause and not an automatically allocated scientific TCD.

## TCD-015 consequence

For TCD-015 the important result is positive:

- the frozen-source Intel rebuild completes LWKM;
- its complete ordinary LWKM case tree is equal to the received Intel executable after metadata-only normalization;
- the earlier native legacy nitrate symptom therefore survives reconstruction from the frozen source/build route on the affected natural case.

The next justified step is a narrowly derived observer build that exposes unrounded `Transsub` quantities while retaining an unmodified baseline executable for comparison.

No correction to `Reko`, clipping policy, transport physics, tolerance or state is admitted by this result.

## Decision

`FROZEN_SOURCE_INTEL_REBUILD_VALIDATED_ON_LWKM_RUURLO_RECEIVED_BINARY_DISCREPANCY_LOCALIZED`

Historical B2 remains fail-closed. The observer route is now substantially better founded because an uninstrumented frozen-source Intel build has first been behaviourally validated on LWKM.