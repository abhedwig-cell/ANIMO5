# ANIMO-RG05 Project Regie

Work unit: `ANIMO-RG05`

Branch: `work/animo-rg05-late-wave-authority-refresh`

Starting parent: `ANIMO-RG04@cf9975ded20fa64bb8125b3241f2609cbb5b51b3`

Status target: `QUALIFIED_POST_RG04_LATE_WAVE_AUTHORITY_REFRESH_ATOMIC_QUEUE_RESET_NO_ADMISSIONS`

Production migration: `NOT_ADMITTED`

## Purpose and authority rule

RG05 is a governance-only reconciliation checkpoint. It refreshes RG04 after the PREP02R internal-recovery stop decision, STATEQ02/B3I04 closure, MASSQ02/B3I03, TCD-042 atomization through B3I05, and later atomic, numerical, review and input work that continued while RG05 was being assembled.

Authority is selected by content, ancestry, explicit status/decision records and validation evidence. Branch names, timestamps and last-writer-wins ordering are not authority. A later branch may supersede an earlier conclusion only when its content explicitly does so. RG05 does not merge work branches and does not promote evidence strength by integration.

Frozen B0 remains:

- source ZIP `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- supplied documentation `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`.

RG05 modifies none of those bytes, no revision-53 source and no canonical TCD row.

## Historical fidelity and G6

Latest PREP02R authority remains `a2fda49871ee3c7104daf7e06cd8dffdac06b125`, with planning decision:

`STOP_FURTHER_INTERNAL_REFERENCE_RECOVERY_AND_PROCEED_WITH_AVAILABLE_EVIDENCE_WITHIN_EXISTING_GOV02_SCOPE`

This ends open-ended internal archaeology. It does **not** mean historical reference acquisition has been exhausted. The prepared external WUR archival/provenance action is still unsent, no provenance-qualified historical revision-53 executable/output bundle has been obtained, and the received 2026 native executable remains cross-runtime diagnostic evidence rather than historical B2.

RG05 therefore records:

- `G6H = HISTORICAL_B2_NOT_PASSED_INTERNAL_RECOVERY_STOPPED`;
- `G6U = NOT_ELIGIBLE_ACQUISITION_NOT_EXHAUSTED_EXTERNAL_ACTION_UNSENT`.

RG05 explicitly forbids reclassifying this as `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`. Only an actual bounded external acquisition action and documented outcome may change the GOV02 route state.

## Canonical state, time, mass, exchange and architecture

`STATEQ02@cb7c23524df6560e65a5bdc1ed19e0b6e3bd46c6` qualifies exact continuous-versus-split checkpoint semantics for the restricted C/N/P external-crop profile. Five accepted boundaries pass exact bitwise comparison, with up to 833 post-restore records. GHG, macropores, TCD-016-C1, the nonzero TCD-040 path, unresolved internal-crop continuation state, active stable-DOM state and active PCLASS state remain excluded. Canonical STATE is not admitted.

`TIME02@b4d78cf32cb149cf50aa2b0a0fbefee571eee6b8` remains a qualified exact-rational civil-time candidate. Canonical TIME is not admitted.

`MASSQ02@56a11b524d03c33ee4ab9b1cd13b2cd523d543fc` retains zero unexplained records in the current nonzero-residual evidence set and a qualified candidate typed-event projection. That projection is not an implemented/admitted runtime journal, so canonical MASS is not admitted.

`ARCH05@99b6098a19db405ce34928af89bb78b856dce7cd` plus synthetic adapter fixtures support a candidate external-exchange contract, not real producer adapters. GEX remains blocked on producer-specific qualification and canonical state/time binding.

`ARCHG02@db8183802631902f41aa5bec518a3c2e63e03ab7` remains the qualified candidate architecture revalidation. It is design authority only.

## TCD-042 authority refresh

Canonical discrepancy identity remains append-only at `work/animo-b3i03-canonical-register-append@814ea660d367494432beb63ea78298d1f6cd73d7`, tail `TCD-042`. No `TCD-043` is reserved.

UBQ01 qualified the exact-zero mechanism as Class B evidence. UBQ02 separately qualified the finite-positive `0 < Flux < 1.0d-8` seam as Class E. B3I05 is closed at `7fa0162415e02a6f0167e71b48ae38177a9e06e0` with:

`QUALIFIED_TCD042_CANONICAL_CHILD_ROUTING_NO_NEW_TCD_NO_ADMISSIONS`

The children remain qualification identities under the existing parent:

- `TCD-042-B1`, exact zero, Class B;
- `TCD-042-E1`, finite-positive subthreshold, Class E.

### B1 supersession and zero-thickness domain

The earlier RG05 snapshot still treated `B3B02@c4eb36e5ece7ab2354b628192662ab8ce80b12fd` as full atomic B1 readiness. That conclusion has now been explicitly superseded by the domain-refined closeout at `B3B02@412bf889ce959d85c651c3b9180dec0a6ff9bb61`.

The reason is substantive. Frozen revision-53 input validation accepts `Hetop = 0`. The positive-Hetop exact-zero limit contains division by `Hetop`. B3B02 therefore retains qualification only for the subdomain `Hetop > 0` and withdraws full readiness for the requested trigger `Flpn = 0 AND Flux = 0`.

Current B1 decision:

`PARTIAL_TCD042_B1_CLASS_B_READINESS_HETOP_ZERO_DOMAIN_UNRESOLVED_ROUTE_AND_REVIEW_FAIL_CLOSED`

The positive-Hetop exact-zero limit and its conservation identity remain qualified evidence. The complete child domain is not admission-ready. RG05 does not silently add `Hetop > 0` as a new input guard and does not reinterpret parser acceptance as a typo.

### E1 numerical review and Class-E readiness

`NQ03@8dcdcf09304f50c83d77abbdc8ef35126d3dcbb6` qualified a restricted binary64 policy only for `Flpn=0`, `0<Flux<1e-8`, `Hetop>0` and `0<P<=3.8510200002999744e-7`, where `P=St*Flux/Hetop`.

`NQ03R@0153779e9045c6527b7c31156f2295ff44b57eeb` then completed a methodologically independent 120-digit reconstruction and passed the restricted policy. This is a numerical second-line review. Organizational independence is explicitly not claimed. NQ03R also found that literal coefficient evaluation order differs at roundoff scale on 129 probe points, so bitwise production binding still requires a frozen evaluation order or a separately qualified equation-derived ulp bound.

`B3E01@41e43c6a6888aac5b5b52041bcdd088c7afc68f1` carries that reviewed policy into Class-E readiness and remains deliberately partial:

`PARTIAL_TCD042_E1_CLASS_E_READINESS_POSITIVE_HETOP_POLICY_QUALIFIED_FULL_CHILD_DOMAIN_AND_ADMISSION_ROUTE_FAIL_CLOSED`

The frozen user guide confirms that `HETOP` has documented range `[0.0, 0.2]`. Thus zero is not merely parser-admissible, it is also inside the pinned documented range. No reviewed documentation has yet supplied a qualified special transport rule for zero thickness. The full E1 child trigger is therefore not covered by the positive-Hetop numerical policy.

B3E01 also records two governance blockers independent of the numerical method: the current formal B3 disposition schema does not directly encode child keys such as `TCD-042-E1`, and the claim-scoped B2 route remains closed. Parent-only substitution is not allowed.

### Shared semantic owner

The parser-admissible and documented `Hetop = 0` case is now a shared semantic owner for both TCD-042 children. B1 and E1 may continue independent evidence work on their positive-Hetop subdomains, but any decision about zero-thickness meaning must be serialized across both children. RG05 therefore adds a distinct `TCD-042_HETOP_ZERO_DOMAIN` owner to the parallelism matrix.

Parent `TCD-042` remains `WAITING_ON_CHILDREN`. It cannot be admitted, composed into B4 or replaced by a parent-only disposition while either child domain remains unresolved.

## Other late-wave reconciliation

`B3A04` advanced after the first RG05 closeout to `1192ee77eda47149af1e31a752e09d343edd9273`. TCD-026 remains qualified Class-A readiness, now with a model-produced CranMais restart-format state replay that strongly exercises the nonzero exudate storage ledger. That replay is explicitly not a chronological split-run and not historical B2. Route and genuinely independent review remain pending.

`B3B03` remains qualified TCD-024 readiness at `446f57f3aeff6e7db56ce473f0724bdb58cad94f`. A technical second-line workunit at `02ce1f49582d2b8cb794c3bfb9d674481a2eea1e` reconfirmed the atomic readiness with green validation, but it came from the same ChatGPT authoring context and explicitly does not satisfy reviewer independence. The separate handoff branch `review/animo-b3b03r-tcd024-independent-second-line@11db97289ffafdd6281b83f0aa0e96b544d6eb5a` remains `REQUEST_PREPARED_NOT_COMPLETED`.

`B3B04@c87ed020a8b4a4685e76f701364b560c8f9c7aef` remains in progress for TCD-040. STATEQ02 split 282 remains only activation/rejection evidence and is not TCD-040 qualification.

`IO02@302d53050d51dacfb68e1ea8d1cc7dd64e985cf3` is now qualified after the contract-test repair, with workflow `34385801249` successful. Its bounded decision is:

`QUALIFIED_BOUNDED_REV53_GENERAL_NORMALIZED_REPRESENTATION_WITH_EXPLICIT_LEGACY_HAZARD_EXCLUSIONS`

The qualification covers admitted revision-53-compatible non-GHG `GENERAL.INP` files while preserving ordered parser semantics, source-observed defaults, repeated structures, lexical provenance and feature conditions. It explicitly does not claim byte round-trip identity and does not manufacture meanings for undefined legacy storage state. GHGMais GENERAL, the non-revision-53-compatible GrassPeat WFPS insertion, optional/whole-profile undefined `OutseLn` storage artifacts, malformed uncontrolled paths, binary hydrology, INITIAL/restart parsing and production migration remain outside the qualified scope.

## Atomic B3 queue reset

RG05 retains 25 top-level entries and zero scientific admissions. The canonical top-level tail remains TCD-042.

The main queue consequences of the post-closeout reconciliation are:

- TCD-024 remains `WAITING_ON_ROUTE_AND_REVIEW`; technical reconfirmation does not satisfy independence.
- TCD-026 remains `WAITING_ON_ROUTE_AND_REVIEW`; the stronger model-produced state replay does not create B2 or admission.
- TCD-040 remains `IN_PROGRESS_ADMISSION_READINESS`.
- TCD-042 remains `WAITING_ON_CHILDREN`, but both child records now surface `Hetop=0` as an upstream domain blocker.
- `TCD-042-B1` is no longer represented as full qualified readiness. Only its positive-Hetop subdomain is qualified.
- `TCD-042-E1` has a qualified and independently reconstructed positive-Hetop policy, plus qualified partial B3E01 readiness, but the full child domain is not ready.

The full queue is `integration/animo-reg/RG05_B3_QUEUE.json`.

## Parallel workstream governance

Readiness, numerical work, bounded input-contract qualification, independent review and the PREP02R external acquisition action may proceed in parallel when atomic ownership is preserved.

Shared semantic owners require explicit serialization. B3B02 and B3E01 share parent TCD-042 and now also share the unresolved `Hetop=0` semantic domain. Positive-Hetop evidence may proceed independently. Any zero-thickness semantic decision, new guard, domain refinement or parent composition must be serialized under that shared owner.

NQ02 and B3B03 share the phosphorus/sorption subsystem, but TCD-019 and TCD-024 cannot be composed for admission and one defect's improved residual cannot define the other's acceptance policy.

IO02 is now a completed bounded representation qualification and may be used as input-contract evidence within its declared scope. Any production parser migration, broader `ModelConfiguration` integration, GHG GENERAL support or excluded legacy-hazard semantics remains a separate serialized qualification problem rather than an implicit extension of IO02.

Canonical STATE, TIME, MASS and EX admissions are serialized owning-gate decisions. TCD-042 parent disposition is serialized after the shared domain and both child-specific gates close. B4 is serialized after every included scientific and canonical gate is admitted. Production remains downstream of B4.

The detailed rules are in `integration/animo-reg/RG05_PARALLELISM_MATRIX.csv`.

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
| TCD042_PARENT | `WAITING_ON_CHILDREN` |
| B4 | `NOT_ADMITTED` |
| PRODUCTION | `NOT_ADMITTED` |

## Recommended next wave

1. Open a dedicated bounded zero-thickness semantic qualification for `Hetop=0` that owns both TCD-042 children. Do not silently exclude zero or add a production guard.
2. Complete B3B04 TCD-040 restore-identity qualification without broadening canonical STATE.
3. Continue genuinely independent B3 reviews for the qualified readiness dossiers. NQ03R is a passed numerical review, not a substitute for every later B3 disposition review.
4. Define a formal atomic B3 disposition carrier for B3I05 child keys without reserving `TCD-043` and without collapsing a child into the parent.
5. Execute the real external archival/provenance acquisition action if progress on G6U is desired.
6. Keep IO02's qualified scope bounded. Open separate work only for excluded GENERAL families/hazards or later production binding rather than broadening IO02 silently.
7. Keep B4 composition and production migration closed.

## RG05 non-admissions

RG05 performs no B3 scientific admission, corrected-legacy admission, numerical-policy admission, canonical STATE/TIME/MASS/EX admission, B4 admission or production migration. It modifies no frozen source/testcase and no canonical discrepancy row.
