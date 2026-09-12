# ANIMO-GHG05 TCD-034 plant-growth temperature selector requalification

Work unit: `ANIMO-GHG05`

Target: `TCD-034`

Branch: `work/animo-ghg05-tcd034-plant-growth-temperature-selector-requalification`

Base authority: `ANIMO-B3Q06@11e9bcdc6654e63f84875bf1f28dc54abe725700`

Current aggregate at authoring start: `ANIMO-RG05O@bc9e6ed997a078336645210ebb4d99ae976893fe`

This workunit does not modify production source, the frozen B0 archive, the canonical TCD register, the central queue, or any admitted TCD. It requalifies the scientific/source premise of TCD-034 only.

## 1. Why this workunit is necessary

TCD-034 entered the post-G5 queue from the GHG01 local finding labelled `CH4 plant-growth temperature use-before-definition`. B3I01 preserved that wording when it reserved TCD-034. The current B3Q06 queue still carries TCD-034 as unadmitted and explicitly says its old `WAITING_ON_THEORY` queue label was not revalidated there.

A fresh source reconstruction shows that the old causal wording is wrong. The `Ln` used in `Te50 = Te(Ln)` is not read before any assignment. In the frozen revision-53 source, `Ln` is the control variable of a preceding root-zone loop. Because `Nuroup` is constrained to `1..Nl`, that loop has at least one iteration. After normal completion, standard/current Fortran loop-control semantics leave `Ln = LnRoot + 1`, where `LnRoot = Nuroup`.

The source expression therefore resolves, under normal loop completion, to:

`Te50 = Te(Nuroup + 1)`

The scientifically unresolved question is not whether `Ln` has a value. It is why plant-growth modulation for CH4 plant-mediated transport is driven by the temperature of the compartment immediately below the active root zone, and whether that selector is intended for all valid root/profile geometries.

## 2. Frozen source identity

The frozen source archive is pinned by SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

The repository source manifest and the locally verified frozen archive agree on the relevant files:

| File | SHA-256 | Relevant fact |
| --- | --- | --- |
| `ghg_ch4.for` | `00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98` | root loop, `Te50 = Te(Ln)`, `fGrow`, `K1plant` |
| `input1.for` | `041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95` | `Nl` and `Nuroup` bounds; `Tegr` meaning |
| `Param.inc` | `20d85ed8bca9e0060d3b51c2f800ff02fdf0bc3ebb8c834baf4afca870a33475` | `Manl = 50` |
| `Temper.for` | `643e4460a897ec629068dc97ab4589a745304b8fa7adb7597dfadc1a9a9d41e5` | internal temperature model writes `Te(0:Nl)` |
| `Input_hydro.for` | `5f07ce68969d749308595d6b4f9f789b6b3646ae226c233e2f8e49565a7dad64` | hydrologic-temperature route writes `Te(1:Nl)` and separately `Te(0)` |

No source byte is copied into the repository by this workunit. The source facts are hash-bound reconstruction evidence.

## 3. Exact source reconstruction

In `ghg_ch4.for`, the relevant order is:

1. `LnRoot = Nuroup`.
2. `Do Ln = 1, LnRoot` accumulates root mass and root-zone thickness.
3. If root mass is effectively zero, a second `Do Ln = 1, LnRoot` assigns an even root distribution.
4. After those loops, `Te50 = Te(Ln)` is evaluated.
5. `fGrow` is calculated from `Te50` and `Tegr`.
6. For root-zone compartments, `K1plant(Ln) = Kpl * FvegCH4 * fRoot * fGrow`.

`input1.for` constrains `1 <= Nuroup <= Nl <= Manl`, with `Manl = 50`. Hence the first root loop cannot have zero iterations. On normal loop completion its control variable is the value immediately after the final iteration. With unit positive stride this gives `LnRoot + 1`.

The fallback root loop, when entered, has the same bounds and the same post-loop value. It therefore does not restore `Ln` to `LnRoot`.

The earlier GHG01 claim that `Ln` was used before first assignment is rejected by the source order.

## 4. Bounds and population analysis

The revised selector has three distinct geometry cases:

- `Nuroup < Nl`: `Nuroup + 1 <= Nl`; the selector addresses the first soil compartment below the active root zone and lies inside the temperature range populated by both supported temperature routes.
- `Nuroup = Nl < Manl`: the selector addresses `Te(Nl+1)`. This is inside the declared array bound `0:Manl`, but outside the `0:Nl` range populated by `Temper` and outside the `1:Nl` plus `Te(0)` range populated by `Input_hydro`. Its value is therefore not established by those producer routes for the current step.
- `Nuroup = Nl = Manl`: the selector becomes `Te(Manl+1)`, outside the declared `Te(0:Manl)` bound.

The second and third cases are source-level reachability statements derived from the admitted input bounds. This workunit does not claim that either case occurred in a historical production run.

## 5. Testbank activation audit

The frozen testbank archive is pinned by SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

A full testbank input scan found one `>GhgCH4:` block, in `GHGMais/Input/soil.inp`, SHA-256 `6a07157f64c0913f977487c1719794c1126416646b0b329ce39940935601f760`. Its plant-transport parameter line is:

`FvegCH4 = 0.0`, `Tegr = 7.0`, `PvCH4Ox = 0.5`.

Because `K1plant` is multiplied by `FvegCH4`, this natural GHG testcase does not provide a positive control for plant-mediated CH4 transport. The existing testbank therefore does not establish a behavioural defect caused by the TCD-034 selector.

The testbank soil comment describes `Tegr` as a dimensionless "temperature factor", but the frozen source input contract describes it as the temperature at which the plant starts to grow in degrees C. The source contract is used for this reconstruction. The testbank comment is not promoted into scientific theory.

## 6. Theory status

The frozen ANIMO 4.0 user guide was searched for CH4, methane, greenhouse-gas plant transport, `Tegr`, and plant-mediated methane transport. It does not provide the later CH4 plant-transport selector used by revision 53.

GHG01 recovered authoritative N2O theory evidence but explicitly recorded that the exact CH4 kinetics were substantially less documented. The cited 2011 ANIMO greenhouse-gas modelling report was not frozen as a full-text design authority in the repository. Public bibliographic traces establish only that the work was cited; they do not establish which soil temperature the `Te50` selector must use.

The variable name `Te50` is not treated as proof that the intended selector is a fixed 50 cm temperature. No authoritative source recovered in this workunit defines that name.

Therefore no scientifically qualified replacement index is available. Candidate alternatives such as root-zone mean temperature, deepest root-zone temperature, temperature below the root zone, fixed-depth temperature, or surface/air temperature remain hypotheses only.

## 7. Current-GNU mechanistic probe

`tools/ghg05/tcd034_post_do_probe.f90` is an active control for one narrow compiler-language fact: after normal completion of `do ln = 1, lnroot` with `lnroot=3`, current GNU Fortran must expose `ln=4` to the following statement. A negative control explicitly resets `ln=lnroot` and proves that this alternative selector is not the result of the unmodified loop.

This probe is not B2, does not reproduce historical Intel behaviour, and does not establish the intended ANIMO physics. Its only purpose is to prevent the old `use-before-definition` premise from re-entering the qualification chain.

## 8. Adversarial counter-hypotheses

The strongest plausible alternatives were considered before disposition:

1. **The source intentionally selects the first compartment below the root zone.** This is compatible with normal source semantics when `Nuroup < Nl`, but no authoritative ANIMO theory recovered here proves that this is the intended plant-growth temperature.
2. **`Te50` means temperature at a fixed 50 cm depth.** The variable name is suggestive but not evidence. The code uses an index tied to root depth, not an explicit geometric 50 cm lookup.
3. **The line was intended to use the deepest rooted compartment, `Te(LnRoot)`.** This would eliminate the post-loop offset, but no source comment, theory equation or qualified historical reference supports changing the index this way.
4. **The issue is harmless because the canonical GHG testcase has `FvegCH4=0`.** That only proves the supplied natural test does not activate the plant-mediated pathway. It does not prove the pathway is scientifically correct for valid nonzero `FvegCH4` inputs.
5. **The old TCD should be deleted as a false positive.** The original causal description is false, but the reconstructed source still exposes an unqualified scientific selector and reachable edge cases. Without theory or activated historical evidence, deleting the canonical TCD would be stronger than the evidence supports.

## 9. Qualification decision

The bounded GHG05 decision is:

`QUALIFY_TCD034_SOURCE_RECONSTRUCTION_AND_REJECT_USE_BEFORE_DEFINITION_PREMISE; KEEP_TCD034_UNADMITTED_BECAUSE_INTENDED_PLANT_GROWTH_TEMPERATURE_SELECTOR_AND_ACTIVE_REFERENCE_BEHAVIOUR_ARE_UNQUALIFIED`

This is a scientific evidence correction, not a source correction and not a B3 admission.

The old provisional Class B remains only a routing hypothesis. A concrete Class B correction cannot be qualified until the intended selector is defined by authoritative theory or an otherwise unambiguous scientific identity. If the eventual evidence requires a new process formulation rather than selection of an existing temperature state, the class must be reconsidered instead of being forced into Class B.

Historical behaviour remains `UNKNOWN_WITHOUT_B2`.

## 10. Resume conditions

TCD-034 can advance only if at least one defensible selector authority is obtained and the active pathway is tested. Minimum future evidence is:

- authoritative ANIMO-specific theory, design history, or equivalent scientific authority defining the plant-growth temperature used in CH4 plant-mediated transport;
- a positive-control case with `FvegCH4 > 0` that exercises the pathway and identifies the expected changed and unchanged surfaces;
- explicit coverage of `Nuroup < Nl`, `Nuroup = Nl < Manl`, and the maximum-boundary case or a scientifically justified application-envelope exclusion;
- a declared B2 route under GOV03/B3Q01;
- non-interference and exact comparison policy appropriate to the eventual correction;
- a new immutable authoring checkpoint and GOV05 review if the scientific claim changes.

Until then, `TCD-034` remains `UNRESOLVED_NOT_ADMITTED` and cannot be used to close B3 composition.
