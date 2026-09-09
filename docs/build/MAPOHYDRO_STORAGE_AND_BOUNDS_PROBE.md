# ANIMO-BUILDQ01 — MAPOHYDRO storage-duration and bounds-order probe

Status: `SOURCE_AND_GNU_PROBE_CONFIRMED_RUNTIME_SEMANTIC_HAZARDS_HISTORICAL_INTEL_EFFECT_UNKNOWN`

## Scope

This is a post-closeout strengthening of BUILDQ01. It uses the frozen ANIMO 4.1.5 revision-53 source archive only, SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`. No frozen source was modified and no production correction is proposed.

The target is `MAPOHYDRO.FOR`, called from `Hydro_detailed.for` in four separate calls with `TaskMp=1,2,3,4` during one hydrology timestep.

## 1. Mixed explicit and implicit cross-call storage

`MAPOHYDRO.FOR:36-39` declares local `LnBoMpMx`, `FlMpInTo` and `FlMpOuTo`. Only the two REAL balance totals have explicit `SAVE`:

`Save FlMpInTo, FlMpOuTo`

Task 1 computes:

- `LnBoMpMx = Max(LnBoMp(1),LnBoMp(2))`;
- `FlMpInTo` and `FlMpOuTo` as whole-profile macropore flux totals.

Task 3 later reads the explicitly saved flux totals when calculating `MpDev`.

Task 4 later reads `LnBoMpMx` as the loop upper bound when undoing temporary `Flid` additions:

`Do Ln=1,LnBoMpMx`

`LnBoMpMx` is neither a formal argument nor explicitly `SAVE`d and is not recomputed in Task 4. The source therefore contains an active non-SAVEd scalar INTEGER cross-call dependency in the macropore hydrology path.

This is semantically distinct from persistent physical state. `LnBoMpMx` is derivable from the explicit `LnBoMp(1:2)` task context and should not become checkpoint state merely to imitate stack retention.

Local key:

`BUILDQ01-LCL-MAPOHYDRO-LNBOMPMX-CROSSCALL`

Classification:

`SOURCE_CONFIRMED_ACTIVE_UNSAVED_CROSS_TASK_LOCAL`

## 2. Exact-source GNU storage-duration probe

The frozen `Mapohydro` subroutine was compiled unchanged with a minimal driver. Task 1 was called with a two-layer active macropore setup, followed by stack-clobbering work and then Task 4. The expected Task-4 reset was `Flid(1:2) = [0.9, 0.8]` from initial `[1.0,1.0]` and retained `FlMpOuSoTo(1,1:2)=[0.1,0.2]`.

Observed GNU Fortran 14.2 behavior under the same eight-byte default REAL semantics used by PREP01:

| compile mode | observed Task-4 behavior |
|---|---|
| `-O0 -fautomatic` | segmentation fault inside `Mapohydro` after Task 1 |
| `-O2 -fautomatic` | completed but skipped the required reset, leaving `Flid(1:2)=[1.0,1.0]` |
| `-O0 -fno-automatic` | retained the Task-1 value and produced the expected `[0.9,0.8]` |

This proves that `LnBoMpMx` lifetime is runtime-material under GNU and that different automatic-storage builds can change either continuation or state.

Qualified GNU materiality:

`CONTROL_FLOW_MATERIAL` and `STATE_MATERIAL`

Historical Intel effect:

`HISTORICAL_EFFECT_UNKNOWN`

PREP01's reconstructed Intel default-storage hypothesis is especially relevant here: Intel default `/Qauto-scalar` semantics place non-SAVEd scalar INTEGER variables on automatic storage. That makes `LnBoMpMx` materially different from the CHARACTER-scalar `Outbal_write` case for which Intel-default persistence was a plausible explanation. This does not prove that the historical project used `/Qsave`; it strengthens the need to recover or independently qualify the historical storage contract.

## 3. Bounds/evaluation-order seam in wet-macropore search

A separate exact-source bounds-check probe exposed a second issue before Task 4. `MAPOHYDRO.FOR:78-80` evaluates:

`FrHeWeMpWl(Dn,LnBoMp(Dn)).Lt.1.d-7 .And. LnBoMp(Dn).Ge.1`

while decrementing `LnBoMp(Dn)`. When a domain has no wet macropore layer, the next condition evaluation can reference second-dimension index 0 even though `FrHeWeMpWl` is declared with lower bound 1.

`MAPOHYDRO.FOR:92-94` has the same ordering pattern for `FrHeWeMpWl(2,Ln)` with the `Ln.Ge.1` test second.

GNU with `-fcheck=bounds` terminates at line 78 with:

`Index '0' of dimension 2 of array 'frhewempwl' below lower bound of 1`

The ordinary non-checking diagnostic build may silently read outside the declared array instead. The logical result still includes the false bound conjunct, so no state effect is inferred from source alone, but memory access itself is outside the declared Fortran array domain and runtime behavior is compiler/check-policy dependent.

Local key:

`BUILDQ01-LCL-MAPOHYDRO-BOUND-CHECK-ORDER`

Classification:

`SOURCE_AND_GNU_BOUNDS_CHECK_CONFIRMED_OUT_OF_DECLARED_DOMAIN_READ_HISTORICAL_EFFECT_UNKNOWN`

No scientific correction is admitted. A future implementation must sequence the bound test before the array access rather than rely on `.AND.` evaluation order, but that implementation change belongs to later governed migration.

## 4. Why broad SAVE flags are not a semantic solution

`Mapohydro` is useful because the same routine contains both:

- explicitly `SAVE`d cross-task totals (`FlMpInTo`, `FlMpOuTo`);
- an unsaved but cross-task-used scalar (`LnBoMpMx`).

A blanket static-local compiler option makes both persist, but it cannot tell whether the unsaved lifetime was intended, accidental, or historically dependent on stack reuse. Conversely, automatic storage follows ordinary local semantics but breaks the observed task protocol.

Therefore BUILDQ01 strengthens its rule: storage flags may be diagnostic compatibility controls, but production migration must recover the semantic owner of each retained value individually.

## 5. B3 and architecture routing

No canonical TCD number is allocated here.

- `LnBoMpMx` is a new local runtime-semantic candidate for B3 intake because GNU controlled probing establishes state/control-flow materiality and the active MP02 route depends on `Mapohydro`.
- the bounds-order finding is a separate local runtime-safety/evaluation-order candidate; it should not be merged automatically with TCD-025 or the MP02 balance-warning FPE seam;
- neither finding changes the physical macropore restart omission already qualified by MP02;
- neither value belongs in accepted persistent `ModelState` merely because revision 53 retains or accesses it across calls.

BUILDQ01 final gate remains unchanged:

`QUALIFIED_POST_G5_FORTRAN_RUNTIME_SEMANTIC_HAZARD_AUDIT_PRODUCTION_BLOCKS_EXPLICIT`
