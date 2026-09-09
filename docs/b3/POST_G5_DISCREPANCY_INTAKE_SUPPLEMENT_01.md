# ANIMO-B3I01 live post-G5 intake supplement 01

Status: canonical intake and routing supplement. No correction or B3 admission.

This supplement extends the original B3I01 checkpoint with authoritative work that appeared later on 2026-09-09. It does not reinterpret source-local numbers as canonical TCD IDs. The canonical register had already been extended through TCD-037 before this supplement was opened.

## Checked live heads

- `ANIMO-PREP12` at `3d86de057247adcfeefb82c11d7cf7d5b2cbdf73`;
- underlying restart source evidence `ANIMO-PREP10` at `761db23269b45ba79df3be97ea85289682e57106`;
- `ANIMO-STATEQ01` at `5a5e0785b6f4a9cb4f67d1fa10d79b184d7d41e9`;
- `ANIMO-BUILDQ01` at `bf5c932753518c883d868c372c6c26bcdcacec68`;
- `ANIMO-TIME02` at `b4d78cf32cb149cf50aa2b0a0fbefee571eee6b8`;
- `ANIMO-MASSQ01` at `79f8f806b293ce9e249e59fe4835ff6866026c4f`;
- `ANIMO-SYNQ01` at `95ae5b8d4627f8c12f732dd8116ba2fb50ef0f50`;
- `ANIMO-GOV02` at `474e4e2b5198c0ecaf3c03d519d5270f88852327`;
- `ANIMO-IO01` at `38a576135d5f63b2561b4dbe180f7121fa3f336a`.

TIME02 supplies a concrete-time candidate but no new discrepancy allocation request at the checked head. MASSQ01 is still a persisted in-progress checkpoint and therefore contributes no completed intake candidate yet. SYNQ01 strengthens oracle evidence for existing TCDs without introducing a new phenomenon. GOV02 strengthens admission rules, not the discrepancy set. IO01 qualifies the revision-53 text-input contract and TTUTIL suitability boundary, but does not qualify a runtime TTUTIL adapter and introduces no new post-G5 defect candidate. Its GHGMais, parser compatibility and provenance constraints remain within already known input/provenance governance rather than constituting a new canonical TCD.

## PREP12 local-number reconciliation

PREP12 deliberately rehomes three source-local labels with `canonical_tcd_id = null`. Their numbers must therefore be ignored during canonical allocation.

`PREP12 source-local TCD-032` is `RG02-LCL-MACROPORE-SOLUTE-RESTART-WRITER`. The phenomenon is the omitted persistent `>MPnitr:`, `>MPorgs:` and conditional `>MPphos:` writer path. B3I01 had already allocated that phenomenon as canonical `TCD-031` after deduplicating MP01 and MP02. PREP12 is additional evidence for TCD-031, not another discrepancy.

`PREP12 source-local TCD-033` is `RG02-LCL-PLANT-ACTUAL-UPTAKE-RESTART-DIRECTION`. This is distinct from canonical GHG `TCD-033`. Nonzero actual crop N/P uptake is represented by the restart interface, but `Inicalc` copies accepted state toward the restart variable instead of restoring accepted state from the restart value. PREP10 supplies natural multi-case reachability and a minimal causal probe. This is reserved as canonical `TCD-038`, provisional Class B.

`PREP12 source-local TCD-034` is `RG02-LCL-PLANT-POTENTIAL-UPTAKE-RESTART-STATE`. This is distinct from canonical GHG `TCD-034`. Potential cumulative crop N/P uptake persists between ordinary accepted timesteps and affects later demand, but the restart surface has no representation and `Inicalc` resets it. This is reserved as canonical `TCD-039`, provisional Class C.

The Class C assignment for TCD-039 is deliberately provisional. STATEQ01 classifies potential uptake as continuation-critical rather than an independently conserved crop stock. Qualification must therefore first decide whether an explicit accepted-boundary owner is required or whether deterministic reconstruction is scientifically complete. If reconstruction eliminates the missing degree of freedom, reclassification is allowed before admission. The intake does not prejudge that result.

## BUILDQ01 routing

BUILDQ01 confirms two additional MAPOHYDRO runtime phenomena.

`LnBoMpMx` is an unsaved scalar INTEGER used across task invocations. GNU automatic-storage probes can terminate or skip a required Task-4 reset, while static storage preserves the observed protocol. BUILDQ01 also concludes that the value is derivable task context rather than a scientific state candidate. This is therefore routed to the existing `TCD-011` local-storage/build-contract family. It does not receive a new scientific TCD and does not justify blanket `SAVE` or static-storage policy.

The MAPOHYDRO wet-domain predicate can access second-dimension index zero before the lower-bound conjunct is evaluated. A GNU bounds-checking build terminates. This is a runtime-language and evaluation-order hazard. It is kept as `BUILD_RUNTIME_HAZARD_NOT_TCD` and explicitly not merged into TCD-025. A later scientific TCD would require independent evidence of a distinct state or flux discrepancy under a qualified execution contract.

BUILDQ01 also closes the earlier generic zero-scale balance-division suspicion for TRANSPORT, Transgen and GHGtransport by source control-flow reinspection. Closed suspicions are not allocated IDs.

## Canonical allocation and append order

The canonical register tail was TCD-037 before this supplement. Collision checks found no competing TCD-038 or TCD-039 allocation in the checked register, branch inventory, issue search, commit search or default-branch code search. The fail-closed reservation artifact was committed before the register append.

Allocation sequence:

1. reserve TCD-038 and TCD-039 fail-closed;
2. persist the crosswalk and routing supplement;
3. prepare exact register rows;
4. append two rows only to the canonical register;
5. verify `2 additions, 0 deletions` for the register append;
6. validate both the original TCD-028..037 append and the TCD-038..039 supplement.

Register presence is canonical identity and routing only. It is not B3 admission.

## Resulting routes

| Finding | Canonical disposition | Class | Owner |
| --- | --- | --- | --- |
| PREP12 macropore solute restart writer | `MAP_TO_EXISTING_TCD` -> TCD-031 | C | proposed ANIMO-MP04 |
| plant actual uptake restart direction | `NEW_CANONICAL_TCD_CANDIDATE` -> TCD-038 | B | proposed ANIMO-STATEQ02 |
| plant potential uptake restart representation | `NEW_CANONICAL_TCD_CANDIDATE` -> TCD-039 | C provisional | proposed ANIMO-STATEQ02 |
| MAPOHYDRO `LnBoMpMx` lifetime | `MAP_TO_EXISTING_TCD` -> TCD-011 | not scientific B3 class | proposed ANIMO-BUILDQ02 |
| MAPOHYDRO index-0 bounds order | `BUILD_RUNTIME_HAZARD_NOT_TCD` | not scientific B3 class | proposed ANIMO-BUILDQ02 |
| IO01 parser and TTUTIL contract findings | no new allocation | not applicable | ANIMO-IO follow-up |

No source, testcase or production implementation is changed by this supplement.

`new_corrections_admitted=false`

`b3_baseline_established=false`

`production_migration_admitted=false`
