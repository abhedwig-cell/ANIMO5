# ANIMO-STATEQ02 restricted-core executable split-run qualification

Status: `QUALIFIED_RESTRICTED_CORE_EXECUTABLE_CHECKPOINT_SEMANTICS_CANONICAL_STATE_ADMISSION_PENDING`

Branch: `work/animo-stateq02-restricted-core-executable-split-run`

Base: `ANIMO-STATEQ01@4adae99576eb56978da71f7c8a250e4445fd3bc4`

External canonical-intake authority checked: `work/animo-b3i01-canonical-register-append@383c7a83e84a578969f92113280dc715b7bdddb4`.

## Decision

A restricted C/N/P profile now has direct executable evidence for:

`run -> accepted boundary -> exact checkpoint -> restore -> continue`.

The qualified profile is deliberately narrower than whole-model ANIMO. The natural witness is `LWKM_gras_1040.2021.2045` with detailed external hydrology, P active, external crop forcing, GHG off, macropores off, P-class selection inactive and stable-DOM state inactive. Surface ponding and the canonical `TCD-040` nonzero layer-0 restart path are excluded by exact guards.

The result qualifies restricted-core executable checkpoint semantics. It does **not** admit canonical STATE globally, does not admit optional blocked features, does not create a production checkpoint implementation and is not B2/reference evidence.

## Frozen executable evidence

B0 inputs:

- source archive SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank archive SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

Qualification executable SHA-256:

`ecb38aa4de825b4f4017c68c4870dd38c7c916d337404147193e7c0fe332cb31`

Build contract follows PREP01's deterministic GNU diagnostic path:

- GNU Fortran;
- free-form legacy source compatibility;
- eight-byte default REAL/DOUBLE semantics;
- static local storage via `-fno-automatic`;
- deterministic link build-id suppression;
- existing GNU compatibility transforms only.

Supplementary user-supplied historical project evidence was inspected but is not promoted to B0. `animo41.vfproj` SHA-256 `f8ac40ea91df926a035396b0afe8584ea0d9c19711535a12b4f12634ce688b2a` specifies `RealKIND="realKIND8"` and `LocalVariableStorage="localStorageSave"` in all four Win32/x64 Debug/Release configurations. The supplied historical executable SHA-256 is `40e29853a0431cc7e2b787dfeb1870f44e1ff402b5aaebd6f56c8365fc5b178d`. This narrows earlier uncertainty about intended project storage/precision settings, but STATEQ02 does not infer scientific correctness from compiler settings.

## Qualification-only checkpoint route

The executable copy adds no production physics. At an accepted boundary, before `Outbal_calc`, Stage A writes an exact unformatted checkpoint containing the restricted profile's accepted physical owners and accepted continuation state.

The checkpoint includes:

- C/N/P accepted physical state;
- explicit fast-site, slow-site and precipitated P state;
- NH4 aqueous state with adsorbed NH4 deterministically reconstructed from the already qualified relation;
- six upper-boundary addition reservoirs;
- accepted management cursor and active material-composition continuation cache;
- external-crop cumulative actual/potential N/P continuation;
- accepted time and layout/cardinality identity.

Stage B restores those coordinates, reconstructs only already qualified derived views, rebinds the external hydrology by replaying the immutable input stream to the exact accepted frame index, reconstructs year-scoped forcing caches from immutable annual inputs and accepted time, and then resumes ordinary execution.

`INITIAL.OUT` is not used as the canonical checkpoint and no formatted restart output is edited to force equality.

## Exact comparison policy

No tolerance was introduced. The NQ01 policy does not permit STATEQ02 to invent one. Every admitted comparison in this campaign is therefore exact/bitwise.

For each split:

1. the Stage-B restore echo is byte-identical to the uninterrupted accepted trace record at the split boundary;
2. every compared post-restore accepted physical trace record is byte-identical to uninterrupted execution;
3. maximum observed absolute difference is exactly `0`.

The trace contains accepted time, hydrology frame coordinates, six upper reservoirs, crop continuation, aqueous C/N/P, NH4 adsorbed reconstruction, P site-resolved state, organic pools, stable-DOM guard state and layer-0 guard coordinates.

## Boundary matrix

| Split | Boundary evidence | Restore | Future comparison |
|---:|---|---|---|
| 66 | management-adjacent; `Adnr 48 -> 49`; P active; zero ponding; nonzero upper reservoir | exact | 24 records, steps 67-90, exact |
| 67 | ordinary interior; P active; zero ponding; nonzero upper reservoir | exact | 833 records, steps 68-900, **entire remaining horizon exact** |
| 68 | P-active zero-surface negative control; nonzero upper reservoir | exact | 42 records, steps 69-110, exact |
| 71 | year-adjacent; zero ponding; nonzero upper reservoir | exact | 24 records, steps 72-95, exact |
| 72 | accepted year boundary `1993-01-01`; P active; zero ponding; nonzero upper reservoir | exact | 28 records, steps 73-100, exact |

The longest and strongest witness is split 67: all 833 remaining accepted records through step 900 are bitwise identical after restore.

## Required surfaces

### Accepted physical state

The restore echo is exact at all five qualified boundaries. No physical coordinate is zero-filled on restore. NH4 adsorbed storage is not serialized as an independent owner; it is reconstructed from accepted aqueous NH4 and the previously qualified sorption relation.

### Management continuation

Split 66 is immediately adjacent to a real management progression. The uninterrupted run moves from `Adnr=48` at the accepted split to `Adnr=49` on the next accepted record. The restored trajectory follows the same progression exactly. Dynamic `Fr/FrCA/FrNH/FrNI/FrPO/FrOR` material composition is carried as management-derived continuation cache, not classified as a conserved stock.

### Upper-boundary reservoirs

All qualified splits preserve nonzero upper reservoirs exactly. The largest absolute reservoir coordinate at split 67 is approximately `1.2704037934301091e-2`; no reservoir is reconstructed as zero.

### P site-resolved state

P is active (`IPO=1`). The witness has one fast site and three slow sites. Aqueous PO4, each fast/slow site, precipitated P and the derived site totals are compared in the exact restore/future trace. No P mode-2/3 canonicalization claim is made.

### External hydrology frame identity

The earlier STATEQ01 first-post-restart `Pn=5e-5` seam is absent in this route. Stage B does not invent or tail-edit hydrology. It replays the frozen hydrology reader to the exact accepted frame index before resuming. `Pnt`, `Snt`, `Sict`, `Walet` and all `Mofrt` values are exact at restore and in every compared future record.

### External crop continuation

The natural witness uses the external-crop mode. Cumulative actual and potential N/P uptake are carried as accepted continuation; `Nuptdef` and `Puptdef` are reconstructed exactly from those cumulative values. The campaign therefore qualifies this external-crop restricted profile only. It does not admit the unresolved internal-crop restart profile.

### Report non-interference

Stage A checkpoints before `Outbal_calc`. Stage B does not restore report accumulators into physical state. Exact future physical trajectories therefore demonstrate that legacy balance/report accumulators are not required to reproduce the exercised physical continuation.

## Fail-closed rejection sentinel

At natural step 282 the witness has:

- `Pnt = 0.001674652 m`;
- nonzero layer-0 dissolved restart coordinates.

Stage A exits with code `95` before creating a checkpoint. No value is clipped, zeroed or tolerated. This is the required positive-surface/TCD-040 activation rejection sentinel.

## Resp_miner diagnostic follow-up

During intermediate debugging a provisional hidden-context hypothesis was raised around `Resp_miner`. It is **not** retained as a STATEQ02 blocker. The final hash-pinned campaign above reproduces exact accepted restore and exact future trajectory, including an 833-record remainder. STATEQ02 therefore does not allocate or infer a new TCD from that intermediate diagnostic observation. Any independent source-quality concern remains owned by the BUILDQ/B3 intake process.

## Scope boundary

Still excluded from this qualification:

- GHG, including `TCD-041`;
- macropores;
- `TCD-016-C1` dry-solute continuation;
- any nonzero `TCD-040` layer-0 aqueous restart path;
- internal-crop restart state;
- active stable-DOM state;
- active P-class state;
- report-period accumulators as physical state.

Consequently:

`restricted-core executable checkpoint semantics = QUALIFIED`

`canonical STATE admission = PENDING`

`whole-model STATE claim = false`

`production implementation = NONE`

Final status:

`QUALIFIED_RESTRICTED_CORE_EXECUTABLE_CHECKPOINT_SEMANTICS_CANONICAL_STATE_ADMISSION_PENDING`
