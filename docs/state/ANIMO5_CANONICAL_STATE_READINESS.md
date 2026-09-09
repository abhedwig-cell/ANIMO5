# ANIMO-STATEQ01 canonical state readiness

Work unit: `ANIMO-STATEQ01`

Status: `QUALIFIED_CANONICAL_STATE_READINESS_MATRIX_STATE_ADMISSION_STILL_BLOCKED`

Canonical STATE admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## 1. Scope and decision

STATEQ01 defines a state-readiness and checkpoint-completeness model for ANIMO5 accepted boundaries. It does not admit canonical STATE, change physics, repair legacy restart behaviour or implement production state containers.

The first executable candidate is deliberately narrow: `CORE_CNP_SUBSURFACE_ONLY`. That profile is valid only under a source-qualified fail-closed envelope with exactly zero layer-0 surface storage at accepted and candidate boundaries and exactly zero layer-0 restart state.

General `CORE_CNP` remains blocked. It includes layer-0 surface transport and therefore inherits both the unresolved TCD-016-C1 scientific continuation gap and the independent layer-0 restart initialization zeroing finding.

## 2. Evidence basis

STATEQ01 reconciles RG02-G5, PREP06, PREP12, ARCH01, ARCH02, ARCH04, TS01, TIME01, ARCHG01/02, MP02, GHG01 and SQ01 without increasing their evidence strength.

PREP12 source-local labels `TCD-032`, `TCD-033` and `TCD-034` are not canonical TCD allocations. STATEQ01 consumes their RG02 reconciliation keys only.

A new local source finding produced by STATEQ01 is likewise not allocated a canonical TCD:

`RG02-LCL-LAYER0-AQUEOUS-RESTART-INIT-ZEROING`.

Its canonical disposition belongs to B3 governance.

## 3. State classes

The readiness model uses:

- `CORE_STATE_READY_CANDIDATE`;
- `OPTIONAL_FEATURE_STATE_READY_CANDIDATE`;
- `FEATURE_STATE_BLOCKED`;
- `EXTERNAL_OWNER_REFERENCE`;
- `DERIVED_RECOMPUTABLE`;
- `NUMERICAL_CONTINUATION`;
- `DIAGNOSTIC_ONLY`;
- `UNRESOLVED_SCIENTIFIC_STATE`.

These are architecture/readiness labels, not admission labels.

## 4. Accepted-boundary semantics

TIME01 supplies the modern transaction boundary: accepted state is immutable during a trial, trial mutation is isolated and only the completed actual result can become the next accepted generation.

TS01 shows that revision 53 implements analogous generations implicitly. Middle-step continuation is staged by the next `Init`; the final result is serialized without another ordinary `Init`. STATEQ01 therefore treats serialization as observation of an already accepted logical boundary, not as the operation that creates acceptance.

## 5. Core soil and hydrology ownership

PREP06/PREP12 support persistent soil-layer state for organic matter, dissolved organic C/N/P, aqueous mineral N and site-resolved mineral P. Hydrological water, ponding, snow/interception and required temperature coordinates remain external-owner state bound by exact accepted frame identity.

Adsorbed NH4 remains physical nitrogen storage, but PREP12 supports candidate deterministic reconstruction from accepted aqueous NH4 plus the admitted sorption/hydrology/configuration inputs. Its omission from the independent checkpoint payload remains subject to split-run qualification.

Site-resolved P is the candidate checkpoint representation. Legacy `Inpo=2/3` origins canonicalized to explicit `Inpo=1` restart state remain unqualified until split-run evidence exists.

## 6. Layer-0 activation is now source-qualified

For aggregated hydrology, revision 53 sets `Flpn=1` if current or end ponding exceeds `1.0d-4`.

For detailed hydrology, `Flpn=1` if either `Pn+Snla` or `Pnt+Snt` exceeds `1.0d-4`; snow therefore participates in the surface transport compartment definition.

`MODFLUX` and the standard transport routines start at compartment `1-Flpn`. Thus `Flpn=1` includes layer 0 in ordinary dissolved-solute transport and `Flpn=0` starts at soil layer 1.

The restricted core uses a stronger envelope than the legacy threshold:

```text
aggregated: Pn == 0 and Pnt == 0

detailed:   Pn + Snla == 0 and Pnt + Snt == 0
```

This prevents positive low-storage surface state from being hidden below the legacy activation threshold.

## 7. Upper-boundary reservoirs are core continuation

The `Conhtop`, `Conitop`, `Codiormatop`, `Codiornitop`, and P-active `Copotop/Codiorpotop` families are not an optional management-only feature.

`UBoundconc` evolves them when `Flpn=0`, and the standard transport path uses their average concentration as the upper boundary for soil layer 1. They therefore remain core persistent state even in `CORE_CNP_SUBSURFACE_ONLY`.

The earlier candidate profile `CORE_CNP_WITH_ADDITION_RESERVOIRS` is withdrawn.

## 8. Local layer-0 restart initialization finding

Revision 53 explicitly reads layer-0 NH4, NO3, labile DOM and DON from `INITIAL.INP` and serializes corresponding layer-0 result fields in `INITIAL.OUT`.

However `Inicalc.for` unconditionally sets:

```text
Conh(0)
Coni(0)
Codiorma(0)
Codiorni(0)
Codiorpo(0)
```

to zero before the first timestep.

The supplied `GrassPeat` initial file naturally contains nonzero layer-0 NH4, NO3, DOM and DON, so this is not merely a hypothetical parser path.

Current classification:

`SOURCE_CONFIRMED_NATURALLY_REACHABLE_LAYER0_DISSOLVED_RESTART_INITIALIZATION_ZEROING`.

It is separate from TCD-016 and has no canonical TCD allocation yet.

## 9. Surface science boundary

TCD-016-C1 remains the unresolved runtime wet-to-low-storage NH4 continuation problem. The SQ01 proposed non-aqueous continuation mass remains `UNRESOLVED_SCIENTIFIC_STATE` and is forbidden as a canonical field until scientifically admitted.

General `CORE_CNP` is therefore blocked by two independent seams:

1. missing/unfinished low-storage NH4 state science;
2. explicit layer-0 restart initialization zeroing.

## 10. Crop continuation

Crop root/shoot dry matter and cumulative actual N/P are owner candidates when `crop_mode=animo`.

PREP12 identifies:

- `RG02-LCL-PLANT-ACTUAL-UPTAKE-RESTART-DIRECTION`;
- `RG02-LCL-PLANT-POTENTIAL-UPTAKE-RESTART-STATE`.

Potential uptake is continuation-critical even though it is not a conserved stock. Additional crop demand/deficit/stage/rotation continuation still needs minimization. Crop checkpoint admission remains blocked.

## 11. Management continuation

Event schedule identity is immutable configuration. Progress through that schedule is accepted continuation metadata.

A checkpoint must serialize exact next-event identity/cursor state or use a deterministic reconstruction rule that is separately split-run qualified. Event replay or skipping is a hard failure.

## 12. Macropores

Macropore water is external hydrology-owner state; macropore solutes are ANIMO persistent state when active.

Two blockers remain distinct:

- TCD-025: public/main macropore control-volume and transfer/direct-drainage integration gap;
- `RG02-LCL-MACROPORE-SOLUTE-RESTART-WRITER`: persistent solute restart writer omission.

The second is PREP12 source-local `TCD-032`, not a canonical allocation.

## 13. GHG state

GHG total CH4/N2O owner coordinates are source-supported, but restart phase reconstruction, layer-0 ponding restoration and hidden cross-call task-state semantics remain unadmitted. GHG profile admission therefore fails closed.

## 14. `INITIAL.OUT` is evidence, not the canonical checkpoint

Legacy `INITIAL.OUT` serializes many final result fields but does not bind complete schema/configuration/layout/external-frame/continuation identity and does not prove portable split-run equivalence.

`Output_Init` also contains a negative crop-P clamp that mutates result state before writing. Canonical checkpoint serialization must be observationally pure.

## 15. Current profiles

Current profile set:

- `CORE_CNP_SUBSURFACE_ONLY`: source guard qualified, executable fail-closed sentinel and split-run suite still missing;
- `CORE_CNP`: blocked on TCD-016-C1 plus `RG02-LCL-LAYER0-AQUEOUS-RESTART-INIT-ZEROING`;
- `CORE_CNP_WITH_CROP`: blocked by crop restart/continuation findings;
- `CORE_CNP_WITH_EXTERNAL_CROP`: restricted-core candidate requiring external crop frame admission;
- `CORE_CNP_WITH_STABLE_DOM`: blocked on stable-DOM science/discrepancy work;
- `CORE_CNP_WITH_MACROPORES`: blocked on TCD-025 plus independent restart-writer finding;
- `CORE_CNP_WITH_GHG`: blocked on GHG restart/phase/task-state semantics;
- `CORE_CNP_WITH_REPORT_CONTINUITY`: physical restricted core plus separate observer continuation.

## 16. Admission consequence

Canonical STATE remains `NOT_ADMITTED` because:

1. restricted-core fail-closed executable sentinels have not been run;
2. no uninterrupted-versus-split B3-admitted checkpoint equivalence exists;
3. management continuation is not qualified;
4. P `Inpo=2/3` origin conversion remains unqualified when those modes are in scope;
5. general core surface state remains blocked on science and restart continuity;
6. optional feature profiles retain independent blockers;
7. local findings still require B3 canonical intake.

Final disposition:

`QUALIFIED_CANONICAL_STATE_READINESS_MATRIX_STATE_ADMISSION_STILL_BLOCKED`

`CANONICAL_STATE_ADMISSION = NOT_ADMITTED`

`PRODUCTION_MIGRATION = NOT_ADMITTED`
