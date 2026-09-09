# ANIMO-B3I02 Post-B3I01 incremental runtime, state and mass discrepancy intake

Status: `QUALIFIED_INCREMENTAL_CANONICAL_DISCREPANCY_INTAKE_NO_ADMISSIONS`

Canonical admission: `NONE`

Production migration: `NONE`

## 1. Scope and authority

B3I02 is an incremental intake only. It does not reopen the full B3I01 register and it does not assign a new identifier to a phenomenon already absorbed by the authoritative B3I01 branch.

The authoritative base remains:

- branch: `work/animo-b3i01-canonical-register-append`;
- head: `383c7a83e84a578969f92113280dc715b7bdddb4`;
- canonical register tail observed at the base: `TCD-041`.

Existing canonical routes preserved by B3I02 are:

- STATEQ01 layer-0 aqueous restart initialization zeroing -> `TCD-040`;
- BUILDQ04 `Flair(Nl+1)` lower GHG air-boundary initialization omission -> `TCD-041`;
- BUILDQ03 hidden cross-call/storage-duration dependency -> existing `TCD-011` where canonical routing is required.

TCD-028 through TCD-037 remain unavailable for reuse by unrelated phenomena.

## 2. Incremental evidence refresh

Completed post-B3I01 evidence consumed by the current B3I02 head is:

- STATEQ01 external-crop split-run evidence at `4adae99576eb56978da71f7c8a250e4445fd3bc4`;
- RG03 post-G5 gate reconciliation at `b67a6cac325fe3f838aedc9df106e120fd5a3d0f`;
- MASSQ02 residual causality reconciliation and typed-event projection at `56a11b524d03c33ee4ab9b1cd13b2cd523d543fc`.

STATEQ02 remains excluded because its branch is still at the pre-execution checkpoint `0875f7f5c0976f8b0b3ae70d00fd2f48b31697d5`.

MASSQ02 closes with:

`QUALIFIED_TYPED_MASS_EVENT_PROJECTION_AND_RESIDUAL_RECONCILIATION_MASS_ADMISSION_PENDING`

It classifies all fifteen formerly unexplained MASSQ01 residuals as source/process-local `NEW_CAUSAL_FINDING`, with `UNEXPLAINED = 0`. B3I02 nevertheless keeps a stricter canonical-identity threshold: source localization is necessary but does not by itself prove an atomic discrepancy mechanism or identity with an existing TCD.

## 3. BUILDQ04 lower GHG air boundary

BUILDQ04 qualified the `Flair(Nl+1)` first-use omission against the connected closed lower-air-boundary contract. B3I01 Supplement 04 already registered the phenomenon as:

`TCD-041`

Atomic scope:

`ONE_LOWER_EXTERNAL_AIR_INTERFACE_INITIALIZATION_OMISSION`

B3I02 disposition remains:

`EXISTING_TCD = TCD-041`

No new identifier is allocated.

## 4. STATEQ01 layer-0 aqueous restart zeroing

STATEQ01 shows that `Inicalc.for` zeroes represented layer-0 restart coordinates:

- `Conh(0)`;
- `Coni(0)`;
- `Codiorma(0)`;
- `Codiorni(0)`;
- `Codiorpo(0)`.

B3I01 Supplement 02 already registered one shared initialization transaction as:

`TCD-040`

Atomicity:

`ONE_CAUSAL_INITIALIZATION_TRANSACTION_MULTI_COORDINATE_SCOPE`

The mechanism remains distinct from TCD-016 wet-to-dry dissolved-solute continuation loss. No species-specific child atoms are created here.

## 5. BUILDQ03 runtime handoff

BUILDQ03 separates hidden task, solver and phase continuation from accepted persistent physical state. Runtime context families remain scoped runtime context, not blanket checkpoint state.

B3I02 preserves:

- existing canonical relation `TCD-011` for the cross-call/storage-duration dependency;
- `RUNTIME_HAZARD_WITHOUT_NEW_SCIENTIFIC_TCD` for qualified runtime-context families that do not establish a separate scientific discrepancy.

The separate `Flair(Nl+1)` source-contract omission remains TCD-041 and is not folded into TCD-011.

## 6. MASSQ02 reconciliation of the fifteen formerly unexplained residuals

MASSQ02 materially strengthens the evidence. The fifteen rows are no longer merely unexplained observer residuals. Each is localized to a source/process surface. B3I02 then performs a second decision: whether the exact mechanism is bounded enough for existing-TCD identity, child-atom identity or a new top-level TCD.

The resulting canonical intake is intentionally narrower than the MASSQ02 `NEW_CAUSAL_FINDING` class.

### 6.1 Fourteen findings remain below canonical identity threshold

Fourteen rows are retained as:

`INSUFFICIENT_EVIDENCE_PENDING_CAUSAL_ISOLATION`

This does not undo MASSQ02 causality. It means the available evidence identifies a local nonclosure surface but not yet an atomic canonical mechanism or exact existing-TCD identity.

The retained cases are:

- CranGrass TITO=724 water: the observer residual is reproduced by `Hydro_detailed.for:235-247` as `Badev`, but reproducing the whole-profile balance equation does not isolate which accepted storage or boundary term creates the nonclosure;
- CranGrass TITO=726 N: mixed DON/NH4/NO3 `TRANSPORT` nonclosure is reproduced locally, but the precise `Transsub` mechanism is not isolated;
- CranMais TITO=1036, GrassPeat TITO=5224, LWKM TITO=8531, STONE TITO=2382 and Zuiderzeeland TITO=637: nitrate-local nonclosures overlap the TCD-015 process family but do not prove activation of the exact duplicated-`Hv` mechanism;
- Puitmijn TITO=1490 N: the known NH4 component remains TCD-016, while the additional layer-0 NO3 component is localized but has no canonical mechanism yet;
- GrassPeat TITO=10, STONE TITO=10 and Zuiderzeeland TITO=1 P: first-step P partition/`Transgen` evidence overlaps the TCD-014 family, but parent identity versus a separate child atom is not yet proven;
- LWKM TITO=4503 and Puitmijn TITO=1490 P: local PO4 `Transgen` nonclosure is reproduced, but the documented TCD-019 probe does not establish identity for the target events;
- LWKM TITO=3073 bounded soil-organic-C: dissolved-organic-matter transport reproduces the source-defined `Cfracom=0.58` projection scale, but no exact branch mechanism is isolated and no whole-system elemental-C claim is made.

No numerical magnitude, repeated symptom or common routine name is used as a shortcut to canonical identity.

### 6.2 RuurloGrass TITO=1915 crosses the causal and atomicity threshold

MASSQ02 R016 provides stronger evidence than the other fourteen rows.

At RuurloGrass TITO=1915:

- `Iopthyvs = 0`;
- `Flib(1) = 0`;
- `Rurv = 0`;
- `Flux = Max(0, Flib(1)+Rurv) = 0`;
- the `UBoundconc.for:110-132` zero-throughflow branch therefore uses `A1=1`, `A2=0`;
- incoming NH4/NO3 `Load` terms do not enter the represented top-reservoir concentration update;
- `Outbal_calc.for:766-784` nevertheless books precipitation/deposition input of `0.005069031338 kg/ha NH4-N` and `0.00168034188 kg/ha NO3-N`;
- the booked total `0.006749373218 kg/ha N` matches the MassLedger residual `0.0067493732130969875 kg/ha N` without an acceptance epsilon.

This is one cross-interface discrepancy mechanism, not separate NH4 and NO3 defects. Both species are affected by the same zero-throughflow branch and the same external-input/state-transfer mismatch.

B3I02 atomicity:

`ONE_ZERO_TOP_THROUGHFLOW_EXTERNAL_N_INPUT_STATE_TRANSFER_SEAM_MULTI_SPECIES_SCOPE`

Live collision checks found no TCD-042 in the authoritative B3I01 register and no competing B3I branch/commit allocation at the reservation point. B3I02 therefore reserves:

`TCD-042`

Provisional correction-class interpretation is deliberately not admitted. The primary concern is Class C style missing/incomplete retained physical-state semantics at zero throughflow, while a narrower Class A ledger-input interpretation remains a possible alternative until the intended external-input semantics are scientifically qualified. The discrepancy identity is reserved; the correction is not selected.

Disposition:

`NEW_TCD_RESERVED_PENDING_CANONICAL_REGISTER_APPEND`

No canonical register row is appended in this reservation checkpoint.

## 7. New STATEQ01 external-crop split evidence

STATEQ01 external-crop split evidence still has two behavioural observations:

- first post-restart `Pn = 5e-5 m` versus uninterrupted `Pn = 0.0 m`, with later compared surface records matching;
- final restart-state differences in `ammoni`, `humorg`, `inipho`, `nitrat`, `orgfsh` and `orgsol`.

STATEQ01 explicitly does not prove one source cause. B3I02 therefore retains both as:

`INSUFFICIENT_EVIDENCE_PENDING_CAUSAL_ISOLATION`

No TCD is allocated from those symptoms.

## 8. RG03 reconciliation result

RG03 closed with:

`QUALIFIED_POST_G5_CANONICAL_GATE_RECONCILIATION_NO_SCIENTIFIC_ADMISSIONS`

B3I02 records:

`GOVERNANCE_RECONCILIATION_NO_NEW_DISCREPANCY`

RG03 does not promote evidence strength, perform scientific admission or create a discrepancy identity.

## 9. Collision scan and reservation result

The authoritative B3I01 register still ends at TCD-041. Before reservation, TCD-042 was absent from that register. A live B3I branch/commit collision check likewise found no competing TCD-042 allocation.

The completed MASSQ02 intake now provides one finding that meets both the causal and atomicity threshold.

Current reservation result:

`reservations = [TCD-042]`

Reservation status:

`RESERVED_PENDING_CANONICAL_REGISTER_APPEND_NOT_ADMITTED`

The reservation is not a repository-wide transactional lock and does not itself append the canonical register. A later append step must re-check the collision immediately before writing the canonical row.

No TCD-043 reservation is made by this workunit.

## 10. Admission boundary and final disposition

B3I02 changes no scientific admission state, corrected-legacy admission state or production migration state.

Current results are:

- existing TCD routes retained: TCD-011, TCD-040 and TCD-041;
- MASSQ02 formerly unexplained residuals consumed: 15;
- new top-level reservation: TCD-042 for the RuurloGrass zero-top-throughflow external-N input/state-transfer seam;
- remaining MASSQ02 findings below canonical identity threshold: 14;
- new child atoms: zero;
- STATEQ01 external-crop behavioural symptoms: still pending causal isolation;
- canonical register append for TCD-042: required but not yet performed;
- scientific admissions: zero;
- corrected-legacy admissions: zero;
- production changes: zero;
- acceptance tolerance introduced: zero.

Final status remains:

`QUALIFIED_INCREMENTAL_CANONICAL_DISCREPANCY_INTAKE_NO_ADMISSIONS`
