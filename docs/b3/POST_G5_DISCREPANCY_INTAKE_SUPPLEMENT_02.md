# ANIMO-B3I01 live post-G5 intake supplement 02

Status: canonical intake and routing supplement. No correction or B3 admission.

This supplement consumes one remaining authoritative local finding from `ANIMO-STATEQ01` that had not yet been allocated by B3 governance after supplement 01.

## Source authority

- `ANIMO-STATEQ01` head `5a5e0785b6f4a9cb4f67d1fa10d79b184d7d41e9`;
- source-local reconciliation key `RG02-LCL-LAYER0-AQUEOUS-RESTART-INIT-ZEROING`;
- frozen source SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- frozen testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

STATEQ01 explicitly left canonical allocation to ANIMO B3 governance.

## Finding

Revision 53 represents layer-0 aqueous restart state on both reader and writer surfaces, but `Inicalc` unconditionally sets the following input coordinates to zero before the first timestep:

- `Conh(0)`;
- `Coni(0)`;
- `Codiorma(0)`;
- `Codiorni(0)`;
- `Codiorpo(0)`.

No preservation handoff is established before that zeroing block. STATEQ01 also demonstrates supplied-case natural reachability for nonzero `Conh(0)`, `Coni(0)`, `Codiorma(0)` and `Codiorni(0)` in GrassPeat.

`Copo(0)` is explicitly outside this finding because it is not zeroed by the cited unconditional block.

## Reconciliation with existing TCDs

This finding is not merged into `TCD-016`. TCD-016 concerns runtime wet-to-low-storage NH4 continuation where no admitted non-aqueous owner exists. Here the affected aqueous state is already represented by the restart interface and accepted-state model, but an initialization operation destroys the restored value.

It is also distinct from:

- `TCD-014`, coupled PO4 initialization consistency and mass accounting;
- `TCD-038`, crop actual-uptake restart assignment direction;
- `TCD-039`, crop potential-uptake continuation absent from the restart representation.

## Atomicity and provisional class

B3I01 allocates one top-level record, `TCD-040`, because the five coordinates are erased by the same unconditional initialization transaction under the same represented layer-0 aqueous restore contract.

Qualification must nevertheless exercise each coordinate independently. If later evidence proves species-specific intended zeroing, a separate trigger or a distinct state-model requirement, the atomicity must be reconsidered.

The provisional B3 class is `B`. The state already exists in the reader, writer and accepted-owner representation, so the present candidate is a local initialization operation defect. This classification must be revisited if qualification shows that a new physical state or numerical policy is required.

## Fail-closed allocation sequence

The canonical register tail was `TCD-039` before reservation. Live collision checks found no competing TCD-040 allocation in the checked register, default-branch code search, issue search, commit search or matching branch refs.

The sequence was:

1. reserve TCD-040 in `POST_G5_TCD_RESERVATIONS_SUPPLEMENT_02.json`;
2. persist crosswalk and routing artifacts;
3. persist the exact prepared register row;
4. append one row to the canonical register;
5. verify `1 addition, 0 deletions` for the register append;
6. persist append reconciliation;
7. extend structural validators and CI through TCD-040.

Register presence establishes canonical identity and routing only. It does not admit a correction or corrected legacy behaviour.

## Qualification handoff

Proposed owner: `ANIMO-STATEQ02`.

Qualification must at minimum:

- prove read-to-accepted-owner restore identity per affected coordinate;
- retain GrassPeat natural reachability without changing B0 bytes;
- use synthetic coverage where natural reachability is absent;
- compare unrounded affected state and downstream flux trajectories;
- execute continuous-versus-split restart tests;
- keep `Copo(0)` and `TCD-016-C1` outside the correction scope;
- obtain independent B3 review before admission.

`new_corrections_admitted=false`

`b3_baseline_established=false`

`production_migration_admitted=false`
