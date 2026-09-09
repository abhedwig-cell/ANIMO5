# ANIMO-RG05 Project Regie

Work unit: `ANIMO-RG05`

Branch: `work/animo-rg05-late-wave-authority-refresh`

Starting parent: `ANIMO-RG04@cf9975ded20fa64bb8125b3241f2609cbb5b51b3`

Status target: `QUALIFIED_POST_RG04_LATE_WAVE_AUTHORITY_REFRESH_ATOMIC_QUEUE_RESET_NO_ADMISSIONS`

Production migration: `NOT_ADMITTED`

## Purpose and authority rule

RG05 is a governance-only reconciliation checkpoint. It refreshes RG04 after the later PREP02R stop decision, completion of the TCD-042 atomization chain through B3I05, new atomic readiness work and newly started numerical/input/state workstreams.

Authority is selected by content, ancestry, explicit status/decision records and qualified validation evidence. Branch names, timestamps and last-writer-wins ordering are never sufficient authority. RG05 does not merge work branches and does not increase evidence strength by integrating their conclusions.

The frozen B0 identities remain:

- source ZIP: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- supplied documentation: `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`.

RG05 changes none of those bytes, changes no revision-53 source, creates no correction, and modifies no canonical TCD row.

## Historical fidelity and G6

Latest PREP02R authority is `a2fda49871ee3c7104daf7e06cd8dffdac06b125`.

Its planning decision is:

`STOP_FURTHER_INTERNAL_REFERENCE_RECOVERY_AND_PROCEED_WITH_AVAILABLE_EVIDENCE_WITHIN_EXISTING_GOV02_SCOPE`

This means additional internal archaeology is no longer an open-ended project task. It does **not** mean historical reference acquisition has been exhausted. The prepared external WUR archival/provenance action is still unsent, no provenance-qualified historical ANIMO 4.1.5 revision-53 executable or output bundle has been obtained, and the received 2026 native executable remains diagnostic rather than historical B2.

Therefore RG05 records:

- `G6H = HISTORICAL_B2_NOT_PASSED_INTERNAL_RECOVERY_STOPPED`;
- `G6U = NOT_ELIGIBLE_ACQUISITION_NOT_EXHAUSTED_EXTERNAL_ACTION_UNSENT`.

RG05 explicitly forbids reclassifying this state as `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`. Only a real bounded external acquisition action and its documented outcome may alter that GOV02 route state.

## State, time, mass, exchange and architecture gates

`STATEQ02@cb7c23524df6560e65a5bdc1ed19e0b6e3bd46c6` remains strong executable evidence for the restricted C/N/P profile. Five accepted split boundaries reproduce uninterrupted execution exactly with no tolerance, with up to 833 post-restore records. The claim remains profile-scoped and excludes GHG, macropores, TCD-016-C1, the nonzero TCD-040 path, unresolved internal-crop continuation state, active stable-DOM state and active PCLASS state. Canonical STATE is therefore not admitted.

`TIME02@b4d78cf32cb149cf50aa2b0a0fbefee571eee6b8` remains a qualified exact-rational civil-time candidate with exact executable vectors. Canonical TIME is not admitted.

`MASSQ02@56a11b524d03c33ee4ab9b1cd13b2cd523d543fc` remains qualified for residual causality and the candidate typed-event projection. The current evidence set has zero unexplained nonzero residual records, but the projection is not an implemented or admitted canonical runtime journal. Canonical MASS is not admitted.

`ARCH05@99b6098a19db405ce34928af89bb78b856dce7cd` and the synthetic adapter fixtures support a candidate exchange contract, not real producer adapters. GEX remains blocked on concrete producer-specific qualification and canonical state/time binding.

`ARCHG02@db8183802631902f41aa5bec518a3c2e63e03ab7` remains the qualified candidate architecture revalidation. It is design authority only and performs no canonical or production admission.

## TCD-042 authority refresh

The canonical top-level register remains append-only at:

`work/animo-b3i03-canonical-register-append@814ea660d367494432beb63ea78298d1f6cd73d7`

with tail `TCD-042`. No `TCD-043` is reserved.

UBQ01 qualified the exact-zero mechanism as a Class-B local algebra atom. UBQ02 separately qualified the finite-positive `0 < Flux < 1.0d-8` seam as Class E requiring numerical-policy selection.

B3I05 is now fully closed at `7fa0162415e02a6f0167e71b48ae38177a9e06e0` with status:

`QUALIFIED_TCD042_CANONICAL_CHILD_ROUTING_NO_NEW_TCD_NO_ADMISSIONS`

The canonical qualification children are:

- `TCD-042-B1`: exact zero, Class B;
- `TCD-042-E1`: finite positive subthreshold, Class E.

They are child qualification identities under parent TCD-042, not new top-level TCD rows.

The later work has already advanced further. `B3B02` now records qualified atomic Class-B readiness for TCD-042-B1, but the valid route and genuinely independent review remain fail closed. `NQ03` is actively qualifying TCD-042-E1 and has persisted numerical evidence, but its status remains `IN_PROGRESS_PERSISTED_NUMERICAL_STUDY_PENDING`. Parent TCD-042 therefore remains `WAITING_ON_CHILDREN` and cannot be admitted or used as admitted B4 scope.

## Atomic B3 queue reset

RG05 retains 25 top-level entries. Scientific admissions remain zero.

Important deltas from RG04 are:

- TCD-026 moved from ready-to-start into qualified Class-A readiness under B3A04, with route and independent review still pending;
- TCD-024 has an active B3B03 readiness workunit with persisted evidence and validation pending;
- TCD-040 has an active B3B04 restore-identity workunit with persisted evidence and qualification pending;
- TCD-042 is no longer waiting on atomization. It is atomized and waits on child-specific completion;
- TCD-042-B1 has qualified readiness but no admission route/review completion;
- TCD-042-E1 has active NQ03 numerical-policy work;
- TCD-015, TCD-017, TCD-018 and TCD-027 remain completed readiness packages and should not be redone merely because admission is blocked.

The full machine-readable queue is `integration/animo-reg/RG05_B3_QUEUE.json`.

## Parallel workstream governance

RG05 separates parallel research from serialized authority changes.

Safe parallel examples include NQ03, B3B03, B3B04, IO02, independent reviews, and claim-scoped readiness work when they preserve atomic ownership and do not edit shared production semantics. PREP02R external acquisition is also independent and may proceed in parallel.

Shared-semantic-owner cases require stronger guards. B3B02 and NQ03 share parent TCD-042 but must remain separate children. NQ02 and B3B03 share the phosphorus/sorption subsystem but may not compose TCD-019 and TCD-024 or define one atom's acceptance from the other's improved residual.

Canonical STATE, TIME, MASS and EX admissions are serialized owning-gate decisions. TCD-042 parent disposition is serialized after both children satisfy their applicable gates. B4 is serialized after every included scientific and canonical gate is admitted. Production remains downstream of B4 and separately qualified implementation.

The detailed matrix is `integration/animo-reg/RG05_PARALLELISM_MATRIX.csv`.

## In-progress work at the RG05 snapshot

RG05 observes but does not promote the following later work:

- `NQ03`: persisted and still in progress for TCD-042-E1;
- `IO02`: persisted source-contract extraction for strict GENERAL.INP representation, not yet qualified;
- `B3B03`: persisted TCD-024 readiness evidence with validation pending;
- `B3B04`: persisted TCD-040 restart-readiness evidence with qualification pending.

B3A04 and B3B02 have already produced qualified readiness decisions, but neither decision is an admission.

Because these streams may continue after this governance snapshot, later evidence must be reconciled by explicit content/state checks rather than silently treated as part of RG05.

## Gate reading

| Gate | RG05 state |
|---|---|
| G6H | `HISTORICAL_B2_NOT_PASSED_INTERNAL_RECOVERY_STOPPED` |
| G6U | `NOT_ELIGIBLE_ACQUISITION_NOT_EXHAUSTED_EXTERNAL_ACTION_UNSENT` |
| G7 | `NO_ATOMIC_SCIENTIFIC_ADMISSIONS` |
| GSTATE | `RESTRICTED_CORE_EXECUTABLE_SPLIT_RUN_QUALIFIED_ADMISSION_PENDING` |
| GTIME | `CONCRETE_CANDIDATE_QUALIFIED_CANONICAL_ADMISSION_NOT_PERFORMED` |
| GMASS | `TYPED_EVENT_AND_RESIDUAL_CAUSALITY_QUALIFIED_ADMISSION_PENDING` |
| GEX | `SYNTHETIC_CONTRACT_FIXTURE_QUALIFIED_REAL_ADAPTER_BLOCKED` |
| GARCH | `QUALIFIED_CANDIDATE_ARCHITECTURE_REVALIDATED` |
| B4 | `NOT_ADMITTED` |
| PRODUCTION | `NOT_ADMITTED` |

## Recommended next wave

1. Complete NQ03 without coupling finite-positive policy to the B1 exact-zero correction.
2. Complete validation/qualification of B3B03 and B3B04.
3. Run genuine independent reviews for qualified readiness dossiers, including TCD-015, TCD-017, TCD-018, TCD-026, TCD-027 and TCD-042-B1, while keeping admission fail closed until a valid claim-scoped route exists.
4. Execute the real external archival/provenance acquisition action if the project wants to make progress on G6U.
5. Continue IO02 as a representation-only input contract stream.
6. Open TCD-023, TCD-030, TCD-038 and TCD-041 atomic readiness work as capacity allows.
7. Do not start B4 composition or production migration from readiness-only evidence.

## RG05 non-admissions

RG05 performs no scientific admission, corrected-legacy admission, numerical-policy admission, canonical STATE/TIME/MASS/EX admission, B4 admission or production migration. It modifies no frozen source/testcase and no canonical discrepancy row.
