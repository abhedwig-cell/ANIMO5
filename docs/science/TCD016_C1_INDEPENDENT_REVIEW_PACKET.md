# TCD-016-C1 independent scientific review packet

Work unit: `ANIMO-SQ01`

Review target: `TCD-016-C1 surface NH4 continuation-state ownership`

Review status: `PREPARED_NOT_REVIEWED`

Candidate status: `MODEL_EXTENSION_HYPOTHESIS_NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## 1. Review purpose

This packet is designed for an independent scientific reviewer. It does not ask the reviewer to approve a code patch. It asks whether the proposed state model is scientifically defensible and what additional theory is required before any model-evolution admission can occur.

The current evidence does **not** support corrected-legacy B3 admission of a dry-solute state.

## 2. Established observations the reviewer may treat as fixed evidence

### 2.1 Frozen source/test evidence

The revision-53 source and supplied historical testbank are hash-controlled and unmodified.

Source SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

### 2.2 Natural NH4 failure

In `Puitmijn_Cranendonck_60` at `TITO=1490`, layer 0, the start surface-water storage is `0.1087117 mm` and the end storage is `0.003256434 mm`.

The represented NH4 mass before the transition is:

`1.3880242022597072e-5 kg N m-2 = 0.13880242022597072 kg N ha-1`.

The frozen `Transsub` control path produces `Rsc=0`, `Avc=0` while neither boundary outflow nor a second state receives that mass.

A standalone call to unmodified `Transsub.for` reproduced the zero-result branch.

### 2.3 Surface-state activation seam

Revision 53 uses `0.1 mm` as a shared surface representation boundary:

- detailed hydrology: ponding active if old or new ponding-plus-snow storage exceeds `1e-4 m`;
- aggregated hydrology: same old-or-new logic for ponding;
- `Transsub`: effective layer-0 low-storage threshold `1e-6*100 = 1e-4 m`.

Because activation uses old **or** new storage, the crossing timestep still processes layer 0. The following timestep can omit it if both old and new storages are below the boundary.

The crossing timestep is therefore the explicit legacy transition at which residual surface solute would need a persistent owner if it remains within the control volume.

### 2.4 Existing ANIMO state owners do not supply that owner

The available ANIMO-specific documentation/source reconstruction establishes:

- layer 0 as the ponding/surface aqueous compartment;
- aqueous NH4 as concentration in water;
- NH4 adsorption as a soil-layer/soil-complex state;
- `Conhtop/Rsconhtop` as a separate additions reservoir with management provenance and its own release law.

No source-defined generic dry surface NH4 state has been found.

## 3. Historical theory boundary

Historical ANIMO theory supports conservation of matter and explicit storage in liquid plus named solid phases.

The available ANIMO 4.0 User Guide and recovered ANIMO 3.5 theory do not establish a generic dry surface NH4 continuation phase or its remobilization law.

The official WUR record for Alterra Report 983 is confirmed, but SQ01 has not fully retrieved the report text. No negative claim is made about uninspected sections of that report.

The origin or physical derivation of the `0.1 mm` representation boundary and the `Fu > 1e-6 m d-1` export threshold has not been recovered.

## 4. Candidate presented for review

Provisional state:

`M_surface_NH4_non_aqueous_continuation`

Unit:

`kg N m-2`

Owner:

surface chemistry / ponding control volume.

The state name is deliberately chemically noncommittal. It represents conserved NH4 mass remaining in the surface control volume when an aqueous concentration state can no longer represent finite mass.

It does **not** claim crystallization, adsorption, precipitation or a residual water film.

## 5. Minimum proposed contract

### Wet to continuation

When the admitted surface-aqueous representation is removed, residual NH4 mass that is neither exported nor transformed must remain in the surface control volume through an explicit internal transfer.

### Hold

In the absence of a separately admitted dry-phase process, the continuation mass is held unchanged. This is a fail-closed modeling rule, not a claim that real dry surface NH4 is chemically inert.

### Remobilization

Any later transfer must be explicit, bounded by available continuation mass and directed to a declared receiving phase. SQ01 has not selected a remobilization kinetic law.

### Restart

The continuation mass must be persistent checkpoint/restart state if the model is admitted.

### Ledger

The MassLedger observes the state and transfers; it does not own or reconstruct them.

## 6. Candidate alternatives already rejected as corrected legacy

The reviewer does not need to reconsider these unless providing new physical evidence.

### Existing soil-sorbed NH4

Rejected because disappearance of ponding does not itself establish delivery to the soil complex or instantaneous adsorption in layer 1.

### Residual-water floor

Rejected because it creates a chemically active water storage not owned by the current hydrology and produces concentration conditioning dependent on an arbitrary floor.

### Existing additions reservoir

Rejected because it aliases generic residual ponding solute with fertilizer/addition provenance and changes release semantics.

### Tiny-outflow closure

Rejected because the canonical event would require an average concentration of order `3.37e4 kg N m-3` and still supplies no continuation state at zero water.

## 7. Shared-representation evidence relevant to architecture

The layer-0 low-storage representation is not unique to NH4.

Source-bound reachability shows:

- NH4: natural defect observed and reproduced;
- mineral phosphorus: direct layer-0 `Transsub` path with explicitly zero reaction/sorption terms, structurally able to encounter the same conservative branch;
- nitrate: same surface route, but reaction terms can alter exact behavior;
- soluble organic M/N/P: same transport route, but layer-0 process-parameter initialization is source-incomplete and runtime behavior is not qualified.

This suggests that a future architecture should not prematurely hard-code the **state-topology mechanism** as NH4-only.

It does not imply common chemistry, common phase identity or common remobilization kinetics across species.

## 8. Questions requiring independent scientific judgment

The reviewer should answer each question separately and identify the evidence basis.

1. Is an areic, chemically noncommittal continuation mass a scientifically acceptable conservative abstraction when the model's aqueous state disappears, or must a specific physical phase be identified before such a state can exist?
2. If a noncommittal continuation state is acceptable as model evolution, what observable physical meaning must be assigned to its residence and release?
3. Is holding the continuation mass unchanged in the absence of admitted dry-phase theory an acceptable fail-closed numerical/scientific policy, or would that itself constitute an unjustified physical assumption?
4. Should rewetting be modeled as instantaneous dissolution, finite-rate dissolution, transfer to soil water, transfer to soil solids, or another mechanism? What theory or measurements support the choice?
5. Is the `0.1 mm` legacy surface activation boundary scientifically usable as the state-transition trigger, usable only as a historical representation boundary, or unsuitable for a future physical model?
6. Does NH4 require a species-specific continuation phase, or is a generic non-aqueous surface-solute state topology scientifically preferable with species-specific process laws?
7. What NH4 transformations remain physically possible while surface ponding is absent, especially volatilization, nitrification, adsorption or exchange with the topsoil?
8. Which state and flux observations would be sufficient to falsify a proposed remobilization law?
9. Does any known ANIMO documentation or implementation lineage establish intended behavior that SQ01 has not recovered?
10. Is Candidate A acceptable for a separate model-evolution qualification route even if it cannot be claimed as corrected historical ANIMO physics?

## 9. Required reviewer disposition

The review should end with one of these dispositions, or an explicitly justified alternative:

`REJECT_CONTINUATION_STATE_CONCEPT`

`REQUIRE_SPECIFIC_PHYSICAL_PHASE_BEFORE_MODELING`

`ACCEPT_NONCOMMITTAL_CONSERVATION_STATE_FOR_MODEL_EVOLUTION_WITH_ADDITIONAL_PROCESS_QUALIFICATION`

`RECOVERED_LEGACY_THEORY_SUPPORTS_SPECIFIC_CONTINUATION_STATE`

A reviewer should not return `B3_ADMITTED` from this packet. B3 admission is a governance decision requiring the full Class-C gate set and independent evidence beyond this review.

## 10. Evidence files for review

Primary SQ01 files:

- `TCD016_DRY_SOLUTE_STATE_RECONSTRUCTION.md`
- `TCD016_CONTINUATION_STATE_CANDIDATES.md`
- `TCD016_CONSERVATION_AND_REWETTING_CONTRACT.md`
- `TCD016_C1_PROPOSED_NONAQUEOUS_STATE_CONTRACT.md`
- `TCD016_SURFACE_STATE_ACTIVATION_SEAM.md`
- `TCD016_SHARED_SOLUTE_REACHABILITY.md`
- `TCD016_HISTORICAL_THEORY_RECOVERY.md`
- `TCD016_THEORY_EVIDENCE_SWEEP.md`

Adjacent source-scope note:

- `TCD016_TRANSCA_LAYER0_PARAMETER_AUDIT.md`

Governance evidence:

- B3Q01 Class-C qualification rules;
- PREP06 conserved-state ownership and transfer-ledger model.

## 11. Current SQ01 disposition

`INDEPENDENT_REVIEW_PACKET = READY`

`INDEPENDENT_REVIEW = NOT_PERFORMED`

`TCD-016-C1 = BLOCKED_INSUFFICIENT_ANIMO_SPECIFIC_PHASE_THEORY`

`TCD-016-E1 = BLOCKED_DEPENDS_ON_TCD016_C1`

`PARENT_TCD016 = UNRESOLVED_NOT_ADMITTED`

`PRODUCTION_MIGRATION = NOT_ADMITTED`
