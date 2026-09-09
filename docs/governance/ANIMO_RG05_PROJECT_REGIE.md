# ANIMO-RG05 Project Regie

Work unit: `ANIMO-RG05`

Branch: `work/animo-rg05-late-wave-authority-refresh`

Starting parent: `ANIMO-RG04@cf9975ded20fa64bb8125b3241f2609cbb5b51b3`

Target state: `QUALIFIED_POST_RG04_LATE_WAVE_AUTHORITY_REFRESH_ATOMIC_QUEUE_RESET_NO_ADMISSIONS`

Production migration: `NOT_ADMITTED`

## Authority rule

RG05 is governance-only. Authority is selected by content, ancestry, explicit status/decision records and validation evidence. A branch name, timestamp or last-writer-wins ordering is never sufficient. A later record supersedes an earlier conclusion only when the later content explicitly establishes that supersession.

RG05 does not merge work branches, does not modify legacy production source and does not promote evidence strength by integration.

Frozen B0 remains unchanged:

- source ZIP `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- documentation `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`.

The canonical discrepancy register remains append-only at `work/animo-b3i03-canonical-register-append@814ea660d367494432beb63ea78298d1f6cd73d7`, with tail `TCD-042`. No `TCD-043` is reserved.

## Historical reference route

Latest PREP02R authority remains `a2fda49871ee3c7104daf7e06cd8dffdac06b125` with decision:

`STOP_FURTHER_INTERNAL_REFERENCE_RECOVERY_AND_PROCEED_WITH_AVAILABLE_EVIDENCE_WITHIN_EXISTING_GOV02_SCOPE`

This ends open-ended internal archaeology. It does **not** mean historical reference acquisition has been exhausted. The prepared external WUR archival/provenance action has not been sent and no provenance-qualified historical revision-53 executable/output bundle has been recovered.

Therefore:

- `G6H = HISTORICAL_B2_NOT_PASSED_INTERNAL_RECOVERY_STOPPED`;
- `G6U = NOT_ELIGIBLE_ACQUISITION_NOT_EXHAUSTED_EXTERNAL_ACTION_UNSENT`.

RG05 explicitly forbids reclassification to `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT` until a real bounded external acquisition action has been executed and its outcome documented.

## Canonical gates

`STATEQ02@cb7c23524df6560e65a5bdc1ed19e0b6e3bd46c6` qualifies exact continuous-versus-split checkpoint semantics only for its restricted C/N/P profile. TCD-040, TCD-016, unresolved crop continuation state, GHG, macropores, active stable-DOM state and active PCLASS remain outside that profile. `GSTATE` is not admitted.

`TIME02@b4d78cf32cb149cf50aa2b0a0fbefee571eee6b8` remains the qualified exact-rational civil-time candidate. `GTIME` is not admitted.

`MASSQ02@56a11b524d03c33ee4ab9b1cd13b2cd523d543fc` remains qualified for residual causality and the candidate typed-event projection. No canonical runtime mass journal is admitted.

`ARCH05@99b6098a19db405ce34928af89bb78b856dce7cd` remains candidate exchange-contract architecture. Real producer adapters and canonical state/time binding are still absent, so `GEX` is not admitted.

`ARCHG02@db8183802631902f41aa5bec518a3c2e63e03ab7` remains qualified candidate architecture only.

## TCD-040 restart identity

`B3B04@19e38ae0dfc211e88fe782b4b7d6e42b1b7f5865` is now qualified for the atomic TCD-040 restart identity claim:

`QUALIFIED_ATOMIC_CLASS_B_RESTART_IDENTITY_READINESS_ONLY_NO_B3_ADMISSION`

The evidence demonstrates exact raw IEEE754 preservation/restoration identity on the qualified restart fixture, including an exact corrected-path full trace. The first legacy divergence occurs immediately after restore for the targeted layer-0 aqueous species.

This result is deliberately narrow. It does not turn STATEQ02 split 282 into TCD-040 qualification, does not admit canonical STATE, does not authorize unconditional deletion of the legacy `Inicalc` zeroing, and does not perform a B3 admission. A later implementation must preserve an explicit cold-start versus restart distinction.

TCD-040 therefore moves to `WAITING_ON_ROUTE_AND_REVIEW`.

## TCD-026 readiness

`B3A04@5eaf02298603b85f802d8e35d6a63941d0878879` remains:

`QUALIFIED_TCD026_CLASS_A_ADMISSION_READINESS_ROUTE_AND_INDEPENDENT_REVIEW_PENDING`

The package includes the model-produced restart-format state replay and now also a green structural validator. That structural validation confirms persisted evidence consistency and scope, but it is explicitly not scientific reexecution and not an independent second-line review. The replay is not historical B2 and not a qualified chronological whole-model split-run.

TCD-026 remains `WAITING_ON_ROUTE_AND_REVIEW`.

## TCD-024 readiness and review independence

`B3B03@446f57f3aeff6e7db56ce473f0724bdb58cad94f` remains qualified atomic readiness for the slow-Langmuir site-indexing claim.

The technical recheck `B3B03R-TECH@02ce1f49582d2b8cb794c3bfb9d674481a2eea1e` passed technically but came from the same ChatGPT authoring context and therefore does not satisfy the independent-review gate.

The separate handoff `review/animo-b3b03r-tcd024-independent-second-line@11db97289ffafdd6281b83f0aa0e96b544d6eb5a` remains `REQUEST_PREPARED_NOT_COMPLETED`.

TCD-024 remains `WAITING_ON_ROUTE_AND_REVIEW`.

## TCD-042 child authority

`B3I05@7fa0162415e02a6f0167e71b48ae38177a9e06e0` remains the routing authority:

`QUALIFIED_TCD042_CANONICAL_CHILD_ROUTING_NO_NEW_TCD_NO_ADMISSIONS`

The qualification children remain:

- `TCD-042-B1`, exact-zero Class B;
- `TCD-042-E1`, finite-positive subthreshold Class E.

They are child qualification identities under canonical parent TCD-042, not new top-level TCD rows.

### B1

The earlier broad B3B02 readiness conclusion is superseded. Current B3B02 head is `690868409aae11297c966eb55419f62ff977c619` with status:

`PARTIAL_TCD042_B1_CLASS_B_READINESS_HETOP_ZERO_DOMAIN_UNRESOLVED_ROUTE_AND_REVIEW_FAIL_CLOSED`

The positive-Hetop exact-zero limit remains qualified evidence. Full-domain readiness is not qualified because revision-53 input validation and the pinned user guide admit `Hetop=0` while the positive-Hetop algebra divides by `Hetop`.

B3B02 now also contains B0-hash-pinned executable blocker evidence. A natural Ruurlo variant with the only scientific input change `Hetop 0.02 -> 0.0` produces IEEE invalid/divide-by-zero behaviour and, in the trap build, `SIGFPE` at `UBoundconc.for:114`, expression `P = St*Flux/Hetop`, in the pre-existing ordinary positive-flow path. This is runtime blocker evidence, not B2 and not a definition of intended zero-thickness semantics.

### E1

`NQ03@8dcdcf09304f50c83d77abbdc8ef35126d3dcbb6` qualifies a restricted binary64 policy only for `Hetop>0` and its declared natural `P` envelope.

`NQ03R@0153779e9045c6527b7c31156f2295ff44b57eeb` independently reconstructs that restricted numerical policy at high precision and passes it. Organizational independence is not claimed, and production bitwise binding still needs an explicit evaluation-order contract or separately qualified ulp policy.

`B3E01@41e43c6a6888aac5b5b52041bcdd088c7afc68f1` remains:

`PARTIAL_TCD042_E1_CLASS_E_READINESS_POSITIVE_HETOP_POLICY_QUALIFIED_FULL_CHILD_DOMAIN_AND_ADMISSION_ROUTE_FAIL_CLOSED`

The full child domain is not closed because `Hetop=0` is documented and parser-admissible but has no qualified transport semantics. The current formal B3 disposition schema also does not directly encode child key `TCD-042-E1`.

### Shared zero-thickness owner

RG05 therefore treats `TCD-042_HETOP_ZERO_DOMAIN` as a shared semantic owner for both B1 and E1. Positive-Hetop work can remain separate. Any decision on zero-thickness input meaning, runtime policy, guard semantics or parent composition must be serialized across both children.

The runtime `SIGFPE` strengthens the blocker. It does not justify silently inserting `Hetop>0` as a new admissibility rule.

Parent TCD-042 remains `WAITING_ON_CHILDREN` and is not admitted.

## GENERAL.INP input contract

`IO02@ea2a5fcce7baaddb80b02fe6ca4334e262f3d60d` is the current qualified bounded GENERAL.INP authority. Its latest workflow `34386845106` is green. The qualification remains:

`QUALIFIED_BOUNDED_REV53_GENERAL_NORMALIZED_REPRESENTATION_WITH_EXPLICIT_LEGACY_HAZARD_EXCLUSIONS`

The latest descendant reconciles the canonical input-contract matrix row with the qualified grammar: top-level `Findadr` blocks may be relocated because lookup rewinds, while ordered records inside a located block remain strict and sequential. Source-observed defaults and `ReadTs` semantics must not be relaxed.

Qualified scope remains revision-53-compatible non-GHG GENERAL representation only. GHG schema, GrassPeat WFPS divergence, undefined selector-storage hazards, malformed uncontrolled paths, binary hydrology, INITIAL/restart and production migration remain outside IO02.

## Queue and parallelism

The top-level queue still contains 25 TCD entries and zero scientific admissions. Current counts are:

- `READY_FOR_ADMISSION_READINESS`: 4;
- `IN_PROGRESS_ADMISSION_READINESS`: 0;
- `WAITING_ON_ROUTE_AND_REVIEW`: 7;
- `WAITING_ON_THEORY`: 4;
- `WAITING_ON_NUMERICS`: 2;
- `WAITING_ON_STATE`: 5;
- `WAITING_ON_RUNTIME`: 2;
- `WAITING_ON_CHILDREN`: 1;
- `NOT_READY`: 0.

Safe parallel work includes independent reviews, bounded input-contract work and atom-specific research that does not modify a shared semantic owner.

Shared-owner changes are serialized. In particular, zero-Hetop semantics across TCD-042-B1/E1, canonical STATE/TIME/MASS/EX admissions, TCD-042 parent disposition, B4 composition and production migration are serialized decisions.

The authoritative details are in:

- `integration/animo-reg/RG05_WORKUNIT_AUTHORITY.csv`;
- `integration/animo-reg/RG05_GATE_MATRIX.csv`;
- `integration/animo-reg/RG05_B3_QUEUE.json`;
- `integration/animo-reg/RG05_PARALLELISM_MATRIX.csv`.

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

1. Qualify the shared `Hetop=0` input/runtime semantics for TCD-042 without silently adding a guard.
2. Run genuinely independent B3 disposition reviews for qualified readiness dossiers, including TCD-040 and TCD-026.
3. Define a formal B3 disposition carrier for B3I05 child keys without reserving TCD-043 or collapsing children into the parent.
4. Execute the real external archival/provenance acquisition action if progress on G6U is desired.
5. Keep IO02 bounded and open separate work for excluded GENERAL families or later production binding.
6. Keep B4 composition and production migration closed.

## Non-admissions

RG05 performs no scientific B3 admission, corrected-legacy admission, canonical STATE/TIME/MASS/EX admission, B4 admission or production migration. It changes no frozen source/testcase and no canonical discrepancy row.
