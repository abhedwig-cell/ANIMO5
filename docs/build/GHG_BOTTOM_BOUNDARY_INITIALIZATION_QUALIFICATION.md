# ANIMO-BUILDQ04 — GHG bottom-boundary first-use initialization qualification

Status: `QUALIFIED_ZERO_BOTTOM_AIR_ADVECTIVE_BOUNDARY_CONTRACT_LOCAL_INITIALIZATION_DEFECT_CANDIDATE_HISTORICAL_INTEL_OPEN`

## Scope

Target local finding inherited from BUILDQ03:

`BUILDQ03-LCL-GHGASSES-FLAIR-NLPLUS1-UNINITIALIZED`

BUILDQ04 qualifies the source topology, boundary meaning and controlled materiality of the revision-53 `GHGasses` read of `Flair(Nl+1)`. It does not change frozen source, admit corrected legacy behaviour or allocate a canonical TCD.

Base:

`work/animo-buildq03-ghg-task-context-qualification@5e06473bc2bb1df6cf4e449d8d6aa04da35c7d47`

Frozen source ZIP SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Frozen testbank ZIP SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Relevant frozen source-file hashes:

- `ghgasses.for`: `4bf5906f571a586d4312d8e7b0d57f6df3b4b6c2073410335616f3d3c042da93`;
- `ghgtransport.for`: `d86e420952c43aaa6e730235f5820802310dd14a0019dc890537d9acd95fcff6`;
- `ghgtranssub.for`: `48d5e45d0b68b87c1d32bc16a867fe36f2f440e0d2c0ca8c95bf605f9f24ea6c`.

Diagnostic compiler: GNU Fortran 14.2.0 under the established eight-byte-default-REAL diagnostic contract.

## 1. BUILDQ03 topology statement is sharpened

BUILDQ03 correctly found that `Flair(Nl+1)` can be read without assignment, but its wording treated this as conditional on a possible final state `La < Nl` and noted a hypothetical `La=Nl` case.

Full source-control-flow reconstruction shows that the post-update `La=Nl` state is not reachable for an ordinary profile with `Nl >= 1`.

Revision 53 does:

1. initialize `La` to 1, or set it to 0 under the ponding-airflow suppression branch;
2. while `La > 0`, `La < Nl` and the current layer remains in the air-flow search, increment `La` by one;
3. execute `La = Max(0,La-1)`;
4. assign `Flair(La+1)=0.0`;
5. fill `Flair(La:1)` backwards;
6. fill `Flair(La+2:Nl)` with zero;
7. for every `Ln=1..Nl`, read `Flair(Ln+1)`.

Immediately before step 3, `La <= Nl`. Therefore after step 3:

`0 <= La <= Nl-1`

for every `Nl >= 1`.

Consequently:

- `Flair(La+1)` can initialize at most through `Flair(Nl)`;
- the forward zero loop also ends at `Flair(Nl)`;
- no assignment in the Task-1 air-flow block reaches `Flair(Nl+1)`;
- the bottom-layer transformation nevertheless reads `Flair(Nl+1)`.

Qualified topology classification:

`UNCONDITIONAL_TASK1_FIRST_READ_WITHOUT_SOURCE_ASSIGNMENT_FOR_NL_GE_1`

This is an evidence refinement of BUILDQ03, not a production-source change.

## 2. Interface meaning of `Flair`

The source itself defines the interface orientation.

`Flair(Ln)` is the air flux across the upper face of compartment `Ln`, positive downward. This follows directly from the transformation:

- `Flaiib(Ln) = Max(0,Flair(Ln))`, labelled influx from above;
- `Flaiio(Ln) = -Min(0,Flair(Ln+1))`, labelled influx from below;
- `Flaiou(Ln)` combines positive outflow through the lower face with negative outflow through the upper face.

Thus `Flair(Nl+1)` is the advective air flux through the lower external face of the modeled soil column.

The Task-1 recurrence anchors air flow at zero at the first saturated interface and states in its comment that below the first saturated zone there is no air flow. Once `La` has been reduced by one, the source zeroes interface fluxes through `Flair(Nl)` but omits the final lower external interface `Flair(Nl+1)`.

That is an off-by-one initialization gap in the boundary-interface array, not missing persistent state.

## 3. Lower gas-transport boundary contract from source

The connected gas-transport source independently constrains the intended lower boundary.

At `Ln=Nl`, revision-53 `GHGtransport`:

- contains no lower-neighbour gas concentration term;
- omits `AvCa(Nl+1)*Flaiio(Nl)` from the bottom advection balance;
- contains no lower-boundary diffusion term.

`GHGtranssub` independently enforces the same lower-boundary structure:

- `Y2(Nl)=0.0`, removing lower-face inflow coupling;
- `P2(Nl)=0.0`, removing lower-face diffusion coupling;
- the tridiagonal lower coefficient is forced to zero at `Ln=Nl`.

The GHG public source interface provides atmospheric gas concentration as the external gas boundary input. No corresponding external bottom-air concentration or bottom-air flux boundary input exists.

Finally, CH4 and N2O air-flow emissions are calculated at the atmosphere-soil boundary only from `FlaiAtmos` and `Flaiib(1)`.

Together these source identities establish a closed lower air-advection boundary for the modeled GHG column. A positive arbitrary `Flair(Nl+1)` would create an unconfigured bottom gas sink, while a negative value has no corresponding modeled bottom concentration source.

Qualified source boundary contract:

`FLAIR_NLPLUS1_EQUALS_ZERO_FOR_CLOSED_LOWER_GHG_AIR_BOUNDARY`

This result does not rely on compiler initialization.

## 4. Independent ANIMO-specific theory cross-check

Stolk et al. (2011), *Modelling the effect of aggregates on N2O emission from denitrification in an agricultural peat soil*, Biogeosciences 8, 2649-2663, DOI `10.5194/bg-8-2649-2011`, gives the original ANIMO N2O conservation-and-transport equation. It includes vertical air advection through air flux `q_a` and describes gas emission to the atmosphere as diffusion plus advection across the atmosphere-soil boundary.

The publication does not provide an explicit revision-53 discrete lower air-boundary assignment. Therefore it is supporting process authority, not by itself proof that the exact discrete value must be zero.

The exact zero result above is derived primarily from the revision-53 connected source contract: interface indexing, saturated-zone zero-airflow rule, absence of a lower external gas boundary input, and the one-sided bottom transport equations.

Theory/source result:

`INDEPENDENT_THEORY_CONSISTENT_SOURCE_INTERNAL_ZERO_BOUNDARY_IDENTITY_STRONG`

## 5. Controlled first-read compiler sensitivity

A compact diagnostic preserves the revision-53 `La` update and `Flair` fill pattern and then reads the bottom interface exactly as the transformation does.

Probe:

`tools/buildq04/buildq04_uninitialized_first_read_probe.f90`

Source SHA-256:

`12d3b924c4d5b456b8e6dee5f5e5937f2be2a25cd0ab382cf1ccf792232eb4d5`

For `Nl=1..4`, the probe confirms final `La=Nl-1` in the continuously unsaturated search case, and `Flair(Nl+1)` remains unassigned in every case.

Observed GNU examples:

- `-O0 -fautomatic` happened to read zero in the tested process image;
- `-O2 -fautomatic` read small positive nonzero stack values for several cases;
- `-O0 -fautomatic -finit-real=snan` propagated NaN through `Flaiio/Flaiou`;
- `-O2 -fautomatic -finit-real=snan` retained NaN in the slot while optimization happened to produce zero in the `MIN/MAX` transformation;
- `-fno-automatic` often happened to expose zero from static storage, but explicit signalling-NaN initialization again proves that zero is not a Fortran-language initialization contract.

The optimization-dependent `MIN/MAX` behaviour is additional compiler sensitivity. It is not used to define science.

Historical Intel manifestation remains:

`UNKNOWN`

## 6. Controlled boundary-value materiality matrix

A second probe assigns only the otherwise missing lower-interface value diagnostically, then executes the revision-53 air-flow transformation and the exact bottom advection/coefficient identities used downstream.

Probe:

`tools/buildq04/buildq04_boundary_sensitivity_probe.f90`

Source SHA-256:

`55d075a53338108e257c95c9f18722b5e69adcf22d477c76c2863b592e7ad5c3`

Matrix dimensions:

- `Nl = 1..4`;
- three air-flow/saturation topology patterns;
- controlled lower-boundary values `-1e-3`, `-1e-6`, `0`, `+1e-6`, `+1e-3`;
- 60 output rows.

GNU O0 and O2 outputs are byte-identical with SHA-256:

`fb98a0d17f3e9295f919c60f2decf7bde584a4f8fdccee85ce0501b5240ce756`

The result is sign-asymmetric because the connected bottom transport equations themselves are one-sided:

- a negative controlled boundary value creates `Flaiio(Nl)>0`, but the bottom transport equations deliberately do not couple a lower-neighbour inflow concentration;
- a positive controlled boundary value creates `Flaiou(Nl)>0` and therefore a direct bottom gas sink;
- zero removes both artificial lower-face terms.

For a positive diagnostic value `q_b`, the exact bottom advection contribution changes by:

`Delta ToFl = -AvCa(Nl) * q_b * St`

and the bottom disappearance coefficient contains the corresponding term:

`Delta Y3 = ReBuAv(Nl) * q_b / He(Nl)`

for the ordinary non-top-unsaturated branch used in the controlled matrix.

Representative `Nl=4`, `q_b=1e-3` result:

- `Flaiou(4)=1e-3`;
- `Delta ToFl=-3e-5` in the chosen diagnostic concentration state;
- `Delta Y3=8e-3` per day under the chosen geometry/partition values.

The magnitude is diagnostic and is not a historical prevalence estimate. The important result is causal: the missing first-use value can directly change gas flux and gas-state evolution.

Runtime materiality classification:

`FLUX_MATERIAL | STATE_MATERIAL | OUTPUT_MATERIAL_POTENTIAL | HISTORICAL_EFFECT_UNKNOWN`

No separate control-flow effect is required for the defect classification.

## 7. Scientific and B3 classification

The finding is no longer adequately described as only a generic compiler/runtime hazard.

BUILDQ04 establishes:

1. a source-unconditional first read without assignment for `Nl>=1`;
2. an exact interface identity for the missing coordinate;
3. a source-consistent closed lower air boundary;
4. independent ANIMO-specific theory consistent with surface atmospheric gas exchange and vertical air advection;
5. controlled flux and state materiality;
6. no missing physical state and no numerical-policy change.

The smallest correction candidate is local: explicitly establish the already implied zero lower boundary before the transformation, or equivalently make the zeroing range cover the lower external interface. BUILDQ04 does not implement either production change.

Provisional B3 class:

`B — LOCAL_INDEX_OR_INITIALIZATION_BOUNDARY_CORRECTION`

Relationship to existing discrepancies:

- distinct from `TCD-011`, whose mechanism is cross-call storage duration;
- distinct from `TCD-032..037`, which cover separate GHG process, partition, restart and observer phenomena;
- not a new physical-state model and therefore not Class C;
- not a numerical policy change and therefore not Class E.

Recommended B3 action:

`NEW_CANONICAL_TCD_CANDIDATE_PENDING_CENTRAL_COLLISION_CHECK_AND_RESERVATION`

BUILDQ04 itself does not allocate the canonical ID.

## 8. Migration contract

A future explicit GHG implementation must represent air fluxes on a defined interface domain including both external faces.

For the revision-53 corrected-legacy candidate qualified here:

- the lower external air-advection face is explicitly zero;
- no compiler initialization or retained stack/static storage may supply that boundary;
- any future nonzero deep-gas boundary condition would be physics/model evolution and would require separate qualification;
- the boundary value is not persistent `ModelState`.

## Gate

`QUALIFIED_ZERO_BOTTOM_AIR_ADVECTIVE_BOUNDARY_CONTRACT_LOCAL_INITIALIZATION_DEFECT_CANDIDATE_HISTORICAL_INTEL_OPEN`

`new_canonical_tcd_allocated=false`

`corrected_legacy_admitted=false`

`b3_scientific_admitted=false`

`production_migration_admitted=false`
