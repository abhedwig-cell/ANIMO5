# ANIMO-RG05 Project Regie

Work unit: `ANIMO-RG05`

Branch: `work/animo-rg05-late-wave-authority-refresh`

Starting parent: `ANIMO-RG04@cf9975ded20fa64bb8125b3241f2609cbb5b51b3`

Status target: `QUALIFIED_POST_RG04_LATE_WAVE_AUTHORITY_REFRESH_ATOMIC_QUEUE_RESET_NO_ADMISSIONS`

Production migration: `NOT_ADMITTED`

## Purpose and authority rule

RG05 is a governance-only reconciliation checkpoint. It refreshes RG04 after the PREP02R internal-recovery stop decision, STATEQ02/B3I04 closure, TCD-042 atomization through B3I05, and later atomic/numerical/input work that advanced while RG05 was being assembled.

Authority is selected by content, ancestry, explicit status/decision records and validation evidence. Branch names, timestamps and last-writer-wins ordering are not authority. RG05 does not merge work branches and does not promote evidence strength by integration.

Frozen B0 remains:

- source ZIP `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- supplied documentation `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`.

RG05 modifies none of those bytes, no revision-53 source and no canonical TCD row.

## Historical fidelity and G6

Latest PREP02R authority is `a2fda49871ee3c7104daf7e06cd8dffdac06b125`, with planning decision:

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

UBQ01 qualified the exact-zero mechanism as Class B. UBQ02 separately qualified the finite-positive `0 < Flux < 1.0d-8` seam as Class E. B3I05 is closed at `7fa0162415e02a6f0167e71b48ae38177a9e06e0` with:

`QUALIFIED_TCD042_CANONICAL_CHILD_ROUTING_NO_NEW_TCD_NO_ADMISSIONS`

The children remain qualification identities under the existing parent:

- `TCD-042-B1`, exact zero, Class B;
- `TCD-042-E1`, finite positive subthreshold, Class E.

Later work has now qualified both child-specific pre-admission packages without admitting either child. `B3B02@c4eb36e5ece7ab2354b628192662ab8ce80b12fd` records qualified atomic Class-B readiness for B1, with route and independent review fail closed. `NQ03@8dcdcf09304f50c83d77abbdc8ef35126d3dcbb6` qualifies a restricted natural-envelope binary64 policy for E1, with independent numerical review still pending and no B3 policy admission.

NQ03's selected scope is `Flpn=0`, `0<Flux<1e-8`, `Hetop>0`, and `0<P<=3.8510200002999744e-7`, with `P=St*Flux/Hetop`. Its qualification does not silently extend beyond that envelope and does not modify B1.

Parent TCD-042 therefore remains `WAITING_ON_CHILDREN`: the mechanistic work is qualified, but the applicable child review/route gates are not complete. Parent admission and B4 use remain forbidden.

## Atomic B3 queue reset

RG05 retains 25 top-level entries and zero scientific admissions.

Material changes from RG04 are:

- TCD-024 now has qualified Class-B readiness under `B3B03@446f57f3aeff6e7db56ce473f0724bdb58cad94f`; its historical route remains blocked, historical prevalence is `UNKNOWN`, and independent second-line review is pending;
- TCD-026 now has qualified Class-A readiness under `B3A04@2097e1e1c83c60b683d850d7c944e8da795ca8ac`; route and independent review remain pending;
- TCD-040 has an active `B3B04@c87ed020a8b4a4685e76f701364b560c8f9c7aef` restore-identity workunit, but qualification is still pending; STATEQ02 split 282 is not reinterpreted as TCD-040 qualification;
- TCD-042 is atomized and both child qualification packages have advanced, but both remain non-admissions;
- TCD-015, TCD-017, TCD-018 and TCD-027 remain completed readiness packages that should not be redone merely because route/review gates are closed.

The full queue is `integration/animo-reg/RG05_B3_QUEUE.json`.

## Parallel workstream governance

Readiness, numerical work, input-contract qualification, independent review and the PREP02R external acquisition action may proceed in parallel when atomic ownership is preserved.

Shared semantic owners require explicit separation. B3B02 and NQ03 share parent TCD-042 but remain distinct atoms. NQ02 and B3B03 share the phosphorus/sorption subsystem, but TCD-019 and TCD-024 cannot be composed for admission and one defect's improved residual cannot define the other's acceptance policy.

Canonical STATE, TIME, MASS and EX admissions are serialized owning-gate decisions. TCD-042 parent disposition is serialized after both children satisfy their applicable review/route gates. B4 is serialized after every included scientific and canonical gate is admitted. Production remains downstream of B4.

The detailed rules are in `integration/animo-reg/RG05_PARALLELISM_MATRIX.csv`.

## Remaining active work at this snapshot

RG05 observes but does not promote:

- `B3B04@c87ed020a8b4a4685e76f701364b560c8f9c7aef`: TCD-040 evidence persisted, qualification pending;
- `IO02@fdf6a27feefcb1d1afb9faff0aaab2f5363073c9`: strict GENERAL.INP representation observer and contract tests are persisted, but qualification remains fail closed. Workflow `34383556997` compiled the observer/test code successfully and then failed in the unittest step. The authoritative IO02 checkpoint therefore remains `IN_PROGRESS_PERSISTED_SOURCE_CONTRACT_EXTRACTION` and `NOT_YET_QUALIFIED`.

Later advances after this snapshot require another explicit content/state reconciliation. They are not silently part of RG05.

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

1. Complete B3B04 TCD-040 restore-identity qualification without broadening canonical STATE.
2. Run genuinely independent reviews for TCD-015, TCD-017, TCD-018, TCD-024, TCD-026, TCD-027, TCD-042-B1 and the NQ03 TCD-042-E1 numerical policy. Keep all admission decisions fail closed while claim-scoped route requirements are unmet.
3. Execute the real external archival/provenance acquisition action if progress on G6U is desired.
4. Fix IO02's failing contract tests and continue representation-only qualification until its full grammar, negative probes, natural projection and validation are green.
5. Open TCD-023, TCD-030, TCD-038 and TCD-041 atomic readiness work as capacity allows.
6. Continue NQ02/TCD-019 and TCD-029 as separate numerical-policy work.
7. Do not start B4 composition or production migration from readiness-only evidence.

## RG05 non-admissions

RG05 performs no B3 scientific admission, corrected-legacy admission, numerical-policy admission, canonical STATE/TIME/MASS/EX admission, B4 admission or production migration. It modifies no frozen source/testcase and no canonical discrepancy row.
