# ANIMO-GHG08: TCD-034 Parent Scientific Closure & Separate-Admission Readiness Synthesis

## Scope

GHG08 is a synthesis and closure-readiness workunit for the parent object `TCD-034` after the completed GHG05, GHG06, GHG06A and GHG07 chain. It introduces no new methane physics, no new selector, no new calibration, no production patch and no B3 admission.

The exact predecessor is `ANIMO-GHG07@f8969334f648ca28ceb93a2a55bb4eedd478e1dc`, whose exact-final workflow run `34844249959` succeeded.

This workunit owns only `TCD034_PARENT_SCIENTIFIC_CLOSURE_READINESS`. It leaves frozen B0, the canonical TCD register, the central B3 queue, RG aggregate authority, routing authority and the central testbank registry unchanged.

## Evidence family being composed

### GHG05: legacy source reconstruction

GHG05 rejected the old use-before-definition premise. The current revision-53 execution semantics for positive root depth are reconstructed as `Te(Nuroup+1)`, with the zero-root path evaluating `Te(1)` while plant transfer remains zero. The source reconstruction is qualified, but the intended scientific selector identity is not.

### GHG06: selector provenance

GHG06 found strong provenance support that the conceptual quantity is daily mean soil temperature at 0.50 m depth, but classified the external literature correctly as new model-evolution evidence rather than historical ANIMO authority. No exact historical ANIMO depth-to-layer operator could be recovered. Historical selector identity therefore remains unresolved.

### GHG06A: bounded Class-F model-evolution selector

GHG06A qualified one new bounded scientific contract: `TCD034_T50_0P50M_DEPTH_OPERATOR_V1`. It linearly interpolates between adjacent layer-centre temperatures that bracket 0.50 m, preserves exact nodes, is affine-exact within its bracket, is root-independent and fails closed without extrapolation. It explicitly does not claim historical revision-53 interpolation semantics.

### GHG07: active plant-mediated CH4 reachability

GHG07 qualified synthetic `FvegCH4>0` reachability against the GHG06A selector. It demonstrated positive plant-mediated CH4 transfer, growth and vegetation switches, root normalization, zero-root-mass fallback, fail-closed selector unavailability and the bounded partition identity `Qox + Qem = Qplant`. This evidence is synthetic model-evolution evidence, not B2 historical behavior and not whole-model methane validation.

## Parent split

The evidence no longer supports treating TCD-034 as one undifferentiated correction candidate. It has two scientifically different tracks.

### Track L: historical/corrected-legacy interpretation

Track L asks whether revision-53 contains a proven local implementation defect whose intended historical selector can be reconstructed sufficiently to admit corrected legacy behavior.

That answer remains **no**. The executed expression is known, but the intended ANIMO-specific selector is not. No active historical B2 reference exists for the plant-mediated branch because the frozen natural GHG testcase has `FvegCH4=0`. The model-evolution T50 operator cannot be substituted as historical evidence.

Track L disposition remains:

`UNRESOLVED_NOT_ADMITTED`.

### Track F: explicit model evolution

Track F asks whether a new, explicitly versioned 0.50 m selector and active plant-mediated CH4 pathway can be qualified independently from historical revision-53 intent.

GHG06A and GHG07 materially advance this track. They are sufficient to establish a bounded candidate formulation and synthetic reachability, but they do not satisfy all Class-F admission requirements in B3Q01.

## Class-F gate assessment

B3Q01 requires a Class-F item to define scientific rationale and authoritative theory, relationship to the preserved B3 baseline, calibration and parameter implications, conservation implications, validation evidence appropriate to the process, expected changes across the intended application envelope and independent scientific review.

GHG08 assesses those gates as follows.

1. **Scientific rationale / theory: PASS_BOUNDED.** The physical target T50 at 0.50 m is scientifically motivated and the discrete operator is explicitly defined as model evolution. The qualification is bounded and does not erase provenance uncertainty.
2. **Relationship to preserved B3 baseline: PARTIAL.** The historical revision-53 behavior is characterized at source level, but the parent TCD remains unadmitted and global B3 composition is still incomplete under B3Q06. A separate evolution admission must therefore preserve this uncertainty explicitly rather than claim a corrected-legacy transition.
3. **Calibration and parameter implications: MATERIAL_GAP.** Changing the temperature selector changes `fGrow` and can therefore change effective plant transfer for existing `Tegr`, `FvegCH4`, `Kpl` and `PvCH4Ox`. No sensitivity or recalibration assessment across realistic profiles has yet been qualified.
4. **Conservation implications: PASS_BOUNDED_ONLY.** GHG07 proves the internal plant partition identity, but does not establish whole-model CH4 or carbon conservation after introducing the new selector in an executable integrated model.
5. **Validation evidence appropriate to the process: MATERIAL_GAP.** Existing evidence is synthetic. There is no qualified active natural testcase, field comparison, observational validation or other process-scale validation envelope for the evolved pathway.
6. **Expected changes across intended application envelope: MATERIAL_GAP.** The direction and magnitude of differences between `Te(Nuroup+1)` and the 0.50 m operator have not been quantified across representative meshes, root depths, seasons, temperature profiles and vegetation settings.
7. **Independent scientific review: MATERIAL_GAP.** GOV05 same-agent adversarial review is explicitly `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`. GOV05 also states that scientific gates are not reduced. It therefore cannot by itself satisfy the Class-F independent scientific review requirement.

## Closure decision

The parent TCD-034 is not ready for legacy B3 admission and is not yet ready for separate Class-F scientific admission.

The qualified parent-level synthesis is:

`QUALIFIED_TCD034_PARENT_DUAL_TRACK_CLOSURE_LEGACY_UNRESOLVED_MODEL_EVOLUTION_NOT_READY_FOR_SEPARATE_CLASS_F_ADMISSION`.

This is a negative readiness decision, not a regression of GHG06A or GHG07. Their bounded model-evolution contracts remain qualified and reusable.

## Minimal remaining scientific work

The next work should not reopen the selector-design question. The minimum material evidence package is now narrower:

- an application-envelope sensitivity and expected-difference study comparing current revision-53 selector behavior with the GHG06A 0.50 m operator across representative layer geometries, root depths, seasons and temperature profiles;
- an explicit calibration/parameter-impact assessment for `Tegr`, `FvegCH4`, `Kpl` and `PvCH4Ox`, including whether existing parameter interpretation remains transferable;
- at least one process-appropriate validation route with active plant-mediated methane transport, clearly classified as observational, experimental, literature-derived or synthetic;
- integrated methane/carbon conservation evidence after the evolved selector is connected to the executable pathway;
- genuinely independent scientific review of the Class-F package, unless later governance explicitly and scientifically supersedes that requirement.

Only after those gates are passed should a separate Class-F scientific-admission workunit be opened. That future admission must remain distinct from corrected-legacy B3 admission and must carry forward the unresolved historical selector status.
