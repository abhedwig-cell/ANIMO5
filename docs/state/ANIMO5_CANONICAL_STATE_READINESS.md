# ANIMO-STATEQ01 canonical state readiness

Work unit: `ANIMO-STATEQ01`

Status: `QUALIFIED_CANONICAL_STATE_READINESS_MATRIX_STATE_ADMISSION_STILL_BLOCKED`

Canonical STATE admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## 1. Scope and decision

This work unit defines a feature-scoped readiness model for persistent ANIMO5 state at an accepted transaction boundary. It does not admit canonical STATE, change physics, repair a legacy restart path, or implement production state containers.

The central conclusion remains that the state problem can be decomposed without allowing one incomplete optional subsystem to poison every configuration. A minimal `CORE_CNP` profile can be specified as a candidate owner/checkpoint set while macropores, GHG, stable DOM, surface-reservoir continuation and crop-continuation gaps remain separately guarded. Any profile enabling a blocked feature fails closed.

The evidence is sufficient to define the readiness matrix and checkpoint completeness predicate. It is not sufficient to claim trajectory-equivalent portable restart or B3 STATE admission.

## 2. Evidence heads consumed

STATEQ01 was started from the RG02-G5 attachment head:

`work/animo-rg02-g5-independent-stream-attachment@5c278152eacc33660f1c5870c7d419b8041b20a9`

The matrix is a reconciliation of independent qualified streams, not an evidence-strength upgrade:

- PREP06 conserved state: `work/animo-prep06-conserved-state-ledger@9b1f1ea51c24fb82823290193651830dc61ea3c8`;
- PREP12 restart-state evidence rehome: `work/animo-prep12-restart-state-continuity-rehome@3d86de057247adcfeefb82c11d7cf7d5b2cbdf73`;
- ARCH01 ownership: `work/animo-arch01-state-ownership-typed-transfers@24f57d8daab828f88446a79bd6a276f2925c828b`;
- ARCH02 checkpoint sufficiency: `work/animo-arch02-restart-checkpoint-sufficiency@a079d93c965f6073586c55ee4b3544dd8873b723`;
- ARCH04 feature/state allocation: `work/animo-arch04-feature-activation-state-allocation@87930bbdfc413ad626176ce119f52ea409198f1d`;
- TS01 temporal semantics: `work/animo-ts01-temporal-semantics@ed12a678cfba19ce851eb2f380e6da3f49203fe4`;
- TIME01 transaction contract: `work/animo-time01-generic-time-transaction-contract@246128dd14732173a6f27c15c923970d50c14e2a`;
- ARCHG01 consolidation: `work/animo-archg01-candidate-architecture-consolidation@981de99811806da362244440502218a84754157b`;
- ARCHG02 temporal revalidation: `work/animo-archg02-temporal-revalidation@db8183802631902f41aa5bec518a3c2e63e03ab7`;
- MP02 complete-case macropore evidence: `work/animo-mp02-whole-case-activation@6b0f2e7470f13baeb6612b0bddb662a497dea528`;
- GHG01 qualification: `work/animo-ghg01-ghg-qualification@dac7b7b5c591b781b82ec968896edb5957664c88`;
- SQ01 TCD-016 state analysis: `work/animo-sq01-tcd016-dry-solute-state@26d0c74aa440bd73c23709d313e24ea8af2a0bcd`.

PREP12 preserves PREP10 evidence without scientific requalification. Its source-local labels `TCD-032`, `TCD-033` and `TCD-034` have `canonical_tcd_id = null`. STATEQ01 therefore consumes their RG02 reconciliation keys and does not allocate canonical TCD numbers. The dedicated reconciliation note is `docs/state/PREP12_RESTART_EVIDENCE_RECONCILIATION.md`.

## 3. State classes

The machine-readable matrix uses the following classes.

`CORE_STATE_READY_CANDIDATE` means source/evidence supports an ANIMO-owned persistent coordinate needed by the core profile. Candidate does not mean B3 admitted.

`OPTIONAL_FEATURE_STATE_READY_CANDIDATE` means the quantity is a credible persistent feature-owned coordinate when its feature is enabled and separately admitted. It may be a physical stock or a continuation-critical scientific coordinate; the matrix states which.

`FEATURE_STATE_BLOCKED` means the quantity belongs to an optional feature whose persistent-state or science contract is incomplete. Enabling that feature must fail closed for canonical-state admission/checkpoint qualification.

`EXTERNAL_OWNER_REFERENCE` means the physical quantity is owned outside ANIMO. The ANIMO checkpoint binds the exact external accepted generation/frame rather than duplicating the state as ANIMO-owned storage.

`DERIVED_RECOMPUTABLE` means the quantity may be reconstructed deterministically from admitted accepted state, configuration and bound external frames. A derived quantity can still represent real physical storage; this class says only that it is not an independent checkpoint degree of freedom.

`NUMERICAL_CONTINUATION` means future behaviour depends on accepted-boundary continuation metadata or state that is not itself an independently conserved physical stock. Management cursors and persistent demand-reference quantities can fall here.

`DIAGNOSTIC_ONLY` means reporting/observer continuation. It never becomes the physical owner merely because a legacy balance accumulator persists.

`UNRESOLVED_SCIENTIFIC_STATE` means evidence shows a missing or ambiguous scientific state contract. It is deliberately excluded from canonical state until the corresponding scientific governance closes it.

## 4. Accepted-boundary semantics

TIME01 provides the governing boundary: the accepted state at `t0` is immutable while a trial executes. Same-step management mutation belongs to `G_MUTATED_EVENT`; potential-pass results belong to `G_PROVISIONAL`; only the completed actual result may become `G_ACTUAL_RESULT` and then the next accepted generation.

TS01 is important at the final interval. Legacy revision 53 does not perform another ordinary `Init` after the last actual calculation. It serializes final result fields directly. STATEQ01 therefore defines the logical accepted boundary independently of that legacy call sequence: after the actual final interval satisfies acceptance requirements, the actual result is the candidate accepted state at `t1`, and checkpoint serialization observes that accepted state. Serialization is not the operation that creates acceptance.

A retry never restores from provisional or report state. It restarts from the unchanged accepted generation.

## 5. Core inherited physical state

PREP06 supports persistent ownership for fresh organic matter fractions, humus, exudate-derived humus, exudates, dissolved organic families, aqueous mineral N, aqueous and site-resolved mineral P, precipitated P and their result-to-next-step continuation. Site-resolved P state is canonical at the configured site cardinality. Summed sorbed P, mineral N totals, total N/P and similar aggregates are derived views, not additional owners.

PREP12 strengthens the checkpoint interpretation for NH4 adsorption. Adsorbed NH4 is real physical nitrogen storage, but revision 53 reconstructs it from NH4 solution concentration plus sorption state/parameters rather than serializing it as an independent restart coordinate. STATEQ01 therefore classifies the checkpoint coordinate as `DERIVED_RECOMPUTABLE`: the physical adsorbed amount remains in the N control volume, but it is not a second independent checkpoint degree of freedom if deterministic reconstruction is admitted and later split-run qualified.

Hydrology-facing physical state is different. Soil water, ponding, snow/interception coordinates, temperature and interval water fluxes belong to the hydrology owner. ANIMO accepted state therefore stores identity references to the exact compatible accepted hydrology generation/frame. It must not create a competing ANIMO-owned water state merely because legacy arrays mirror hydrological values.

PREP12 finds source-level read/write symmetry for the major core restart families. That is useful readiness evidence but still not portable split-run qualification.

## 6. Phosphorus restart shape

For P-active state, the candidate canonical accepted shape is explicit: aqueous PO4, every configured fast site, every configured slow site, precipitated P and DOP. `Output_Init` writes this explicit shape using `Inpo=1` even when input accepts `Inpo=2/3` initialization modes.

STATEQ01 does not add duplicate owners for those alternative initialization modes. It does, however, keep a qualification boundary: trajectories initialized through `Inpo=2/3` have not been shown split-run equivalent after the legacy 2/3-to-1 restart canonicalization. That is an initialization/restart qualification issue, not a reason to change the accepted-state topology.

## 7. Surface and management continuation

Management has two layers. The event schedule/configuration is immutable identity; progression through that schedule is continuation metadata. TS01 shows that legacy reader/cursor state such as `Adnr` and `Tinead` is not represented by `INITIAL.OUT`, while same-row addition/ploughing order is temporally material. A canonical checkpoint must therefore carry an explicit next-event identity/cursor or prove a deterministic reconstruction from accepted time plus schedule identity. That exact reconstruction still needs split-run qualification.

The active surface addition/ponding reservoir contains real dissolved state coordinates. However TCD-016 prevents the surface NH4 representation from being called complete across wet-to-dry deactivation. SQ01's preferred `M_surface_NH4_non_aqueous_continuation [kg N m-2]` is a review-ready model-extension hypothesis, not admitted ANIMO physics. STATEQ01 records it only as `UNRESOLVED_SCIENTIFIC_STATE`. It is not created, initialized, restored or treated as canonical by this work unit.

SQ01 also demonstrates that the low-storage seam is structurally shared by other surface solute routes, but only NH4 has the qualified natural deletion finding. STATEQ01 therefore does not widen TCD-016 to every solute.

## 8. Crop state and continuation

ANIMO-owned crop shoot/root dry matter and actual plant N/P are persistent optional physical-owner candidates when `crop_mode=animo`. External-crop mode instead binds an external crop frame and must not duplicate its owner state.

PREP12 makes two restart-continuity blockers explicit.

First, cumulative actual plant N/P values are present in `>orgpla:` but the restart initialization direction is wrong for nontrivial values. STATEQ01 records this by reconciliation key:

`RG02-LCL-PLANT-ACTUAL-UPTAKE-RESTART-DIRECTION`

The PREP12 source-local label is `TCD-033`, but no canonical TCD is allocated by STATEQ01.

Second, cumulative potential N/P uptake is scientifically active continuation state. It is carried between ordinary timesteps and used in potential-minus-actual demand logic, but it has no restart representation and is reset on restart. STATEQ01 records:

`RG02-LCL-PLANT-POTENTIAL-UPTAKE-RESTART-STATE`

The PREP12 source-local label is `TCD-034`, again without canonical allocation here.

Potential uptake is not treated as a conserved crop stock. It is continuation-critical state. Additional demand/deficit/stage continuation variables identified by TS01 remain to be minimized. Therefore `CORE_CNP_WITH_CROP` is blocked by concrete restart findings and by any still-unresolved continuation family, not merely by a vague lack of crop metadata.

The negative crop-P `Output_Init` clamp remains a separate serializer-purity concern and is not adopted as checkpoint semantics.

## 9. Macropores

MP02 confirms that active macropore water storage changes process conditions and cannot be dismissed as reporting state. Water remains hydrology-owned and must be bound through the compatible macropore hydrology frame. Macropore solute storage is ANIMO process state.

Two blockers must remain separate.

`TCD-025` concerns the incomplete public/main macropore control volume and transfer integration.

The persistent solute restart writer omission is a different PREP12 finding:

`RG02-LCL-MACROPORE-SOLUTE-RESTART-WRITER`

Its source-local PREP10/PREP12 label is `TCD-032`, with no canonical TCD allocated. Revision 53 reads `>MPnitr:`, `>MPorgs:` and conditional `>MPphos:` persistent state, but the writer blocks are commented out. MP02 confirms the omission in complete active cases.

STATEQ01 repairs neither issue. `CORE_CNP_WITH_MACROPORES` therefore fails closed because of both the control-volume gap and the independent restart-state omission, plus missing B2/B3 feature admission.

## 10. GHG state

GHG01 establishes `CsCH4` and `CsN2O` as total gas-system concentration owner coordinates in revision 53. It also shows why matching `>methan:` and `>nitoxi:` read/write labels do not prove a sufficient restart. An uninterrupted run carries dissolved phase state differently from the `INITIAL.OUT` restore, which reconstructs soil-layer phase partition using `Terf`; layer-0 ponding reconstruction is additionally incomplete.

A future canonical checkpoint need not duplicate both total and dissolved phase coordinates if an admitted deterministic reconstruction from total state plus accepted hydrology/thermodynamic state exists. That reconstruction contract is not yet qualified. GHG total owner state is therefore `FEATURE_STATE_BLOCKED`; dissolved/gas views are marked derived only conditionally on a future admitted reconstruction contract.

GHG01 also finds unsaved cross-call task locals used by active CH4/N2O calculations. STATEQ01 does not label those locals as intended physical state. They are recorded as unresolved trial scientific/numerical continuation. They are not accepted-boundary checkpoint fields unless future scientific evidence proves cross-boundary persistence is required.

## 11. Numerical continuation versus accepted physical state

TIME01 identities such as `accepted_generation_id`, `configuration_identity`, `physical_layout_id`, calendar/time identity, event schedule identity and external frame identities are required checkpoint metadata. They are not conserved physical stocks.

Within-step potential passes, nonlinear iteration arrays, transport coefficient scratch and mixed-generation helper views are not checkpointed merely because legacy routines retain them across calls. When scientifically required within one trial they must become explicit trial-owned solver state or be deterministically recomputed. A portable accepted-boundary checkpoint never resumes halfway through such a trial in this contract.

Persistent crop potential-uptake values are different: PREP12 shows they survive ordinary accepted-step transitions and affect later demand. They are therefore accepted-boundary continuation, not disposable within-step scratch.

## 12. `INITIAL.OUT` is not the canonical checkpoint

Legacy `INITIAL.OUT` is useful evidence because it serializes many final profile result fields and can seed another run. It is not a canonical checkpoint contract.

The evidence now shows the following limitations:

- it does not bind configuration, layout, schema, exact external hydrology/crop generation or event-schedule identity;
- it omits management cursor continuation;
- it has an actual-plant-uptake restart direction defect;
- it omits persistent potential-uptake continuation;
- it omits persistent macropore solute state;
- it canonicalizes P restart representation to `Inpo=1` without split-run qualification for 2/3-origin trajectories;
- GHG phase restoration is not behaviourally sufficient;
- report-period accumulators are separate from it;
- no authoritative portable split-run equivalence has qualified it as a canonical restart.

There is also a serializer side effect in `Output_Init`: a negative final crop P value can be clamped to zero before writing. A canonical checkpoint serializer must be a pure observer of the accepted state. STATEQ01 neither adopts nor repairs that legacy clamp.

## 13. Report-period accumulators

`Bawa`, organic/N/P balance accumulator families and detailed transformation accumulators belong to `G_REPORT_ONLY`. They are not physical state owners and cannot be used to repair missing conservation ownership.

If exact mid-report-period output continuity is promised, diagnostic continuation must be serialized in a separate observer section. If that promise is not made, physical checkpoint completeness does not require the report accumulators. Report reset/rollover never creates a physical acceptance boundary.

## 14. Feature-scoped profiles

The state profile matrix defines at least:

- `CORE_CNP`, with optional surface reservoir, stable DOM, crop, macropores and GHG disabled;
- `CORE_CNP_WITH_SURFACE_RESERVOIR`, blocked by TCD-016-C1 for complete wet/dry NH4 continuation;
- `CORE_CNP_WITH_CROP`, blocked by the PREP12 crop restart findings and remaining continuation minimization;
- `CORE_CNP_WITH_EXTERNAL_CROP`, which replaces internal crop ownership with a bound external crop frame;
- `CORE_CNP_WITH_STABLE_DOM`, blocked on existing stable-DOM discrepancy/qualification gaps;
- `CORE_CNP_WITH_MACROPORES`, fail closed on TCD-025 plus `RG02-LCL-MACROPORE-SOLUTE-RESTART-WRITER` and missing feature admission;
- `CORE_CNP_WITH_GHG`, fail closed on GHG restart phase-state and hidden task-state qualification gaps;
- `CORE_CNP_WITH_REPORT_CONTINUITY`, which adds diagnostic continuation without changing the physical owner profile.

A profile name is not a science-admission statement. It is a declarative list of required owners, references and blockers.

## 15. Admission consequence

STATEQ01 can qualify the matrix architecture without admitting STATE because the following remain open at different scopes:

1. no canonical portable split-run equivalence has yet admitted even the minimal profile;
2. management continuation requires explicit cursor/reconstruction qualification;
3. P 2/3-to-explicit restart canonicalization remains unqualified for affected legacy trajectories;
4. crop-enabled checkpoint continuation has concrete actual/potential uptake restart defects and still needs final minimization;
5. TCD-016-C1 is blocked pending science and is not a canonical field;
6. TCD-025 leaves the macropore main control volume unqualified, while a separate local PREP12 finding leaves macropore solute restart incomplete;
7. GHG phase reconstruction, ponding layer-0 state and hidden task-state semantics remain unadmitted;
8. stable-DOM feature discrepancies remain independently governed;
9. PREP12 local discrepancy labels still require canonical B3 intake/allocation.

These blockers do not erase the core owner model. They constrain which profiles can move to later admission testing.

Final disposition:

`QUALIFIED_CANONICAL_STATE_READINESS_MATRIX_STATE_ADMISSION_STILL_BLOCKED`

`CANONICAL_STATE_ADMISSION = NOT_ADMITTED`

`PRODUCTION_MIGRATION = NOT_ADMITTED`