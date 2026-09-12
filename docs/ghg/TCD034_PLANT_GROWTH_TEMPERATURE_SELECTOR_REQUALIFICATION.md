# ANIMO-GHG05 TCD-034 plant-growth temperature selector requalification

Work unit: `ANIMO-GHG05`

Target: `TCD-034`

Branch: `work/animo-ghg05-tcd034-plant-growth-temperature-selector-requalification`

Base authority: `ANIMO-B3Q06@11e9bcdc6654e63f84875bf1f28dc54abe725700`

Current aggregate at authoring start: `ANIMO-RG05O@bc9e6ed997a078336645210ebb4d99ae976893fe`

This workunit does not modify production source, the frozen B0 archive, the canonical TCD register, the central queue, or any admitted TCD. It requalifies the scientific/source premise of TCD-034 only.

## 1. Why this workunit is necessary

TCD-034 entered the post-G5 queue from the GHG01 local finding labelled `CH4 plant-growth temperature use-before-definition`. B3I01 preserved that wording when it reserved TCD-034. The current B3Q06 queue still carries TCD-034 as unadmitted and explicitly says its old `WAITING_ON_THEORY` queue label was not revalidated there.

A fresh source reconstruction shows that the old causal wording is wrong. The `Ln` used in `Te50 = Te(Ln)` is the control variable of a preceding root-zone loop. Under current standard Fortran semantics the selector resolves to `Te(Nuroup+1)`, including the zero-root case described below. The unresolved scientific question is therefore the identity of the intended temperature selector, not a simple use-before-definition defect.

## 2. Frozen source identity

Frozen source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

The repository source manifest and locally verified frozen archive agree on the relevant files:

| File | SHA-256 | Relevant fact |
| --- | --- | --- |
| `ghg_ch4.for` | `00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98` | root loop, `Te50 = Te(Ln)`, `fGrow`, `K1plant` |
| `input1.for` | `041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95` | input-time `Nl` and `Nuroup` bounds; `Tegr` meaning |
| `Param.inc` | `20d85ed8bca9e0060d3b51c2f800ff02fdf0bc3ebb8c834baf4afca870a33475` | `Manl = 50` |
| `Temper.for` | `643e4460a897ec629068dc97ab4589a745304b8fa7adb7597dfadc1a9a9d41e5` | internal temperature model writes `Te(0:Nl)` |
| `Input_hydro.for` | `5f07ce68969d749308595d6b4f9f789b6b3646ae226c233e2f8e49565a7dad64` | hydrologic-temperature route writes `Te(1:Nl)` and separately `Te(0)` |
| `root_plant.for` | `07adda92e78a21bde08e137d1cb09bb40d9c63c4f19dcdeeef0d3e263b107816` | SWATRE route can reset `Nuroup` to 0 and then raise it from active transpiration layers |
| `root_grass.for` | `cad5cc713e72b7fac01cbba63caa25560fcabd243c73d9fc06ab7130de4d0661` | same dynamic `Nuroup` reconstruction |
| `root_extern.for` | `063a754fac2fe1b1c4b60fab1e395b8b65a9a03a5d89ace03e08868e1774f0e9` | same dynamic `Nuroup` reconstruction |
| `Animo.for` | `352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7` | root update occurs before the GHG call |

No frozen source byte is copied into the repository by this workunit. The reconstruction is hash-bound.

## 3. Exact control-flow reconstruction

The relevant sequence is:

1. The applicable root routine executes before `GHGasses` in `Animo.for`.
2. On the SWATRE route, each root routine explicitly sets `Nuroup = 0` and then scans `Ln = 1..Nl`; the deepest layer with `Flev(Ln) >= 1e-7` becomes `Nuroup`.
3. Therefore the runtime range admitted by source is `0 <= Nuroup <= Nl`. The input-time check `1 <= Nuroup <= Nl` is not a persistent runtime invariant.
4. In `ghg_ch4.for`, `LnRoot = Nuroup`.
5. `Do Ln = 1, LnRoot` accumulates root mass and root-zone thickness. If root mass is effectively zero, a second loop with the same bounds distributes roots evenly.
6. `Te50 = Te(Ln)` follows those loops.
7. `fGrow` is computed from `Te50` and `Tegr`.
8. `K1plant` receives `fGrow` only for `1 <= Ln <= LnRoot`.

For `LnRoot > 0`, normal loop exhaustion leaves the control variable at `LnRoot+1`. For `LnRoot = 0`, the loop has zero iterations but current standard/GNU semantics establish the control variable at the initial value 1. The fallback loop has the same bounds. In both cases the following selector is therefore:

`Te50 = Te(Nuroup + 1)`

The earlier GHG01 statement that `Ln` is read before first source assignment is rejected.

A further non-interference fact follows for `Nuroup = 0`: `fGrow` is still calculated from `Te(1)`, but no compartment satisfies `Ln <= LnRoot`, so `K1plant` remains zero everywhere. The selector cannot affect plant-mediated CH4 transport on that timestep through `K1plant`.

## 4. Bounds and population analysis

The selector has four distinct runtime cases:

- `Nuroup = 0`: selector `Te(1)` is populated, while plant-mediated transport is disabled by the empty root-zone condition.
- `0 < Nuroup < Nl`: selector `Te(Nuroup+1)` is populated and addresses the first compartment below the active root zone.
- `Nuroup = Nl < Manl`: selector `Te(Nl+1)` is within declared `Te(0:Manl)` bounds but outside the current-step producer ranges demonstrated in `Temper` and `Input_hydro`.
- `Nuroup = Nl = Manl`: selector `Te(Manl+1)` is outside the declared bound.

The last two are source-reachable states under the root update and declared input geometry. This workunit does not claim that either occurred in a historical production run.

## 5. Testbank activation audit

Frozen testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

A full frozen-testbank input scan found one `>GhgCH4:` block, in `GHGMais/Input/soil.inp`, SHA-256 `6a07157f64c0913f977487c1719794c1126416646b0b329ce39940935601f760`. Its plant-transport parameters are `FvegCH4 = 0.0`, `Tegr = 7.0`, `PvCH4Ox = 0.5`.

Because `K1plant` is multiplied by `FvegCH4`, this natural GHG testcase is not a positive control for plant-mediated CH4 transport. The existing frozen testbank therefore does not demonstrate a behavioural effect from the TCD-034 selector.

The testbank comment calls `Tegr` a dimensionless temperature factor, while the frozen source input contract defines it as the temperature at which the plant starts to grow in degrees C. This workunit uses the source contract for variable identity and does not promote the testbank comment into theory.

## 6. Theory status

The frozen ANIMO 4.0 user guide was searched for CH4, methane, greenhouse-gas plant transport, `Tegr`, and plant-mediated methane transport. It does not define the later revision-53 CH4 plant-growth temperature selector.

GHG01 recovered authoritative N2O theory evidence but explicitly recorded that exact CH4 kinetics were substantially less documented. The cited 2011 ANIMO greenhouse-gas modelling report is not frozen as a full-text design authority in the repository. Public bibliographic traces establish citation/existence only, not which soil temperature `Te50` must represent.

The variable name `Te50` is suggestive but is not treated as proof of a fixed 50 cm selector. No recovered authority defines it. Root-zone mean temperature, deepest-root temperature, first-below-root temperature, fixed-depth temperature and air/surface temperature all remain hypotheses.

## 7. Mechanistic control and evidence boundary

`tools/ghg05/tcd034_post_do_probe.f90` checks two language-control cases with current GNU Fortran:

- positive trip count: `lnroot=3` leaves `ln=4`;
- zero trip count: `lnroot=0` leaves `ln=1`.

A negative control explicitly resets `ln=lnroot` to demonstrate that selecting the deepest rooted compartment would require an assignment absent from the frozen TCD-034 path.

This is current-GNU mechanistic evidence only. It is not B2 and does not establish historical Intel behaviour or intended ANIMO physics.

## 8. Adversarial counter-hypotheses

The strongest alternatives are:

1. **First-below-root temperature is intentional.** Source semantics support this when `0 < Nuroup < Nl`, but no ANIMO-specific theory recovered here establishes intent.
2. **`Te50` means fixed 50 cm temperature.** The name alone is insufficient and the implementation is tied to dynamic root depth.
3. **The intended line is `Te(LnRoot)`.** Plausible, but unsupported by qualified theory or historical reference.
4. **The issue is harmless because `FvegCH4=0` in GHGMais.** This proves only that the frozen natural GHG case does not activate the pathway effect.
5. **TCD-034 should be deleted because the old use-before-definition premise is false.** Too strong. The reconstructed selector has unresolved scientific identity, lacks an active reference case, and has source-reachable bottom-boundary states that require disposition.
6. **Input validation guarantees `Nuroup>=1`.** Rejected. The root routines can reset `Nuroup=0` before the GHG call.

The sixth counter-hypothesis was discovered during the adversarial pass over the initial authoring package and caused a substantive authoring remediation. The earlier green checkpoint is not used as the reviewed checkpoint.

## 9. Qualification decision

The bounded candidate decision is:

`QUALIFY_TCD034_SOURCE_RECONSTRUCTION_AND_REJECT_USE_BEFORE_DEFINITION_PREMISE; KEEP_TCD034_UNADMITTED_BECAUSE_INTENDED_PLANT_GROWTH_TEMPERATURE_SELECTOR_AND_ACTIVE_REFERENCE_BEHAVIOUR_ARE_UNQUALIFIED`

This is a scientific evidence correction, not a production/source correction and not a B3 admission. The old provisional Class B remains a routing hypothesis only. No replacement index is admitted or even preferred by this workunit.

Historical behaviour remains `UNKNOWN_WITHOUT_B2`.

## 10. Resume conditions

TCD-034 can advance only after obtaining a defensible selector authority and active pathway evidence. Minimum future evidence is:

- ANIMO-specific theory, design history, or equivalent scientific authority defining the plant-growth temperature for CH4 plant-mediated transport;
- a positive-control case with `FvegCH4 > 0`;
- coverage of `Nuroup = 0`, `0 < Nuroup < Nl`, `Nuroup = Nl < Manl`, and the maximum-boundary case, or a scientifically justified application-envelope exclusion;
- a declared B2 route under GOV03/B3Q01;
- expected-difference and non-interference contracts for any proposed correction;
- a new immutable authoring checkpoint and GOV05 review if the scientific claim changes.

Until then, `TCD-034` remains `UNRESOLVED_NOT_ADMITTED` and cannot close B3 composition.
