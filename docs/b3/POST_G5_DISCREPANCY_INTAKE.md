# ANIMO-B3I01 Post-G5 discrepancy canonical intake

Status target: `QUALIFIED_POST_G5_DISCREPANCY_CANONICAL_INTAKE_AND_ROUTING_NO_ADMISSIONS`

This workunit is an intake and routing layer only. It does not correct frozen source, alter production code, admit corrected legacy behaviour, establish a B3 baseline, or increase the evidence strength of any upstream finding.

## Authority and live evidence pins

Canonical discrepancy allocation remains owned by ANIMO B3 governance. B3Q01 remains the classification and admission authority. RG02 G5 is used as the integration authority for independent streams, but its attachment does not promote B1 evidence to B2 or B3.

Live heads used by this intake:

| Workunit | Branch | Evidence head |
| --- | --- | --- |
| RG02 G5 | `work/animo-rg02-g5-independent-stream-attachment` | `5c278152eacc33660f1c5870c7d419b8041b20a9` |
| B3Q01 | `work/animo-b3q01-scientific-admission-framework` | `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54` |
| NQ02 | `work/animo-nq02-tcd019-nonlinear-p-qualification` | `40a41089020f78ee1d5181b8afc7bdb511af3193` |
| SQ01 | `work/animo-sq01-tcd016-dry-solute-state` | `26d0c74aa440bd73c23709d313e24ea8af2a0bcd` |
| MP01 | `work/animo-mp01-macropore-qualification` | `7b5979dd6301b9d55d23e8c22948a0dba24b229b` |
| MP02 | `work/animo-mp02-whole-case-activation` | `6b0f2e7470f13baeb6612b0bddb662a497dea528` |
| GHG01 | `work/animo-ghg01-ghg-qualification` | `dac7b7b5c591b781b82ec968896edb5957664c88` |
| PREP10 | `work/animo-prep10-stable-dom-plough-accumulators` | `65cd4a65a3ea27cd4ce004f505d5022fdb08b9ab` |
| PREP10C | `work/animo-prep10c-stable-dom-event-reset-authoritative` | `549545921dc8175f01d86c283647acd470c14290` |
| TCD-028 intake | `work/animo-b3-tcd028-stable-dom-intake` | `7f38b79d88c05fd86c89fbdd7a5794b90ffba2bf` |

The central discrepancy register observed by this workunit ends at `TCD-027`. `TCD-028` was already reserved fail-closed and was not yet appended. Live searches found no TCD-029 allocation and no `TCD-03*` code or branch allocation before B3I01 reserved new identifiers. Those searches are collision-avoidance observations, not transactional locks.

## Intake rules applied

A local finding does not become canonical because its branch gives it a name. Independent observations of the same physical or numerical phenomenon are deduplicated. Different phenomena are kept separate even if they occur in the same routine. B3Q01 Class A through F describes the correction mechanism, so a pure build/runtime hazard or unresolved theory/provenance conflict does not receive an A through F class until it becomes a correction candidate.

New top-level identifiers are first reserved in `integration/animo-b3/POST_G5_TCD_RESERVATIONS.json`. B3I01 does not append these reservations silently to the pre-existing `THEORY_CODE_DISCREPANCY_REGISTER.csv`. The routing register therefore distinguishes `EXISTING_CANONICAL_TCD`, `PREEXISTING_FAIL_CLOSED_RESERVATION`, `RESERVED_BY_B3I01_NOT_REGISTER_ROW`, and child atoms. A later explicit register-integration commit can append TCD-028 through TCD-037 while preserving the historical B3Q01 snapshot and without implying B3 admission.

## Canonical reconciliation

### NQ02

`NQ02-LCL-IFLSOL4-DETCOEF-CANCELLATION` is not part of TCD-019. NQ02 shows it is upstream and cross-cutting, occurs in the Iflsol=4 analytical coefficient route, and can materially alter a natural-case trajectory. It does not uniformly improve the TCD-019 mass residual. That makes merging it into TCD-019 scientifically misleading. B3I01 reserves `TCD-029`, provisional Class E, and routes qualification to proposed `ANIMO-NQ03`.

The distinction from TCD-024 is also retained. TCD-024 is a wrong-index defect in slow Langmuir site kinetics. TCD-029 concerns numerical evaluation of generic analytical transport coefficients.

### SQ01 and TCD-016

TCD-016 cannot remain one admission unit. SQ01 already reconstructed two mechanisms:

- `TCD-016-C1`, Class C: the missing continuation-state owner for surface NH4 mass across ponding deactivation.
- `TCD-016-E1`, Class E: the numerical activation/export policy around the low-storage transition.

These are child qualification atoms, not new top-level TCDs. C1 must be scientifically fixed before E1 can be judged. The 1 mm `UBoundconc` dry-deposition threshold and the `Transca` layer0 parameter-initialization seam remain `INSUFFICIENT_EVIDENCE`; neither is folded into TCD-016 merely because it is nearby in the surface path.

### MP01 and MP02

MP01 and MP02 strengthen TCD-025 but do not create a second macropore ledger discrepancy. TCD-025 remains the one Class A main-ledger integration phenomenon. MP02's complete-case B1 evidence confirms symptoms but does not provide B2 or a corrected-ledger admission basis.

Two additional macropore phenomena are separate:

- `TCD-030`, provisional Class B: `mapoinput` reads initial macropore NO3 but the labelled range check is applied to NH4 values.
- `TCD-031`, provisional Class C: persistent macropore solute restart serialization is incomplete. MP01 and MP02 found the same phenomenon, so it receives one ID.

The MP02 GNU invalid-operation flag at `MAPOTRANSPORT.FOR:670` is not a scientific TCD. It is localized to `Abs(BaDev/BaMx)` in a balance-warning guard. Historical Intel behaviour and model-state or flux materiality are unproven. Its disposition is `BUILD_RUNTIME_HAZARD_NOT_TCD` and it routes to build-contract qualification.

### PREP10 and TCD-028

The PREP10/10C stable-DOM plough accumulator finding remains `TCD-028`. The prior B3 reservation is authoritative. B3I01 does not allocate another identifier. Provisional Class B is retained because the candidate concerns an event-local accumulator identity using existing state, not a new physical state or numerical policy. Historical local-storage semantics and B2 route eligibility remain open.

### GHG01

GHG01 deliberately handed local findings to B3 without allocating canonical IDs. B3I01 separates them as follows.

| Local finding | Disposition | B3 class | Canonical relation |
| --- | --- | --- | --- |
| Methanogenesis source-pool transfer path | new candidate | B | `TCD-032` reserved |
| CH4 production component partition nonclosure | new candidate | B | `TCD-033` reserved |
| CH4 fresh-OM weighting index | insufficient evidence | provisional B only | no ID |
| CH4 plant-growth temperature use-before-definition | new candidate | B | `TCD-034` reserved |
| Hidden GHG task-state persistence | map to existing build-contract family | none yet | `TCD-011` |
| GHG restart phase partition | new candidate | C | `TCD-035` reserved |
| Ponding layer0 GHG restart reconstruction | new candidate | C | `TCD-036` reserved |
| GHG Outbal working-array interface | new candidate | A | `TCD-037` reserved |
| Gas-store C/N control-volume gap | atomize existing accounting umbrella | A | `TCD-009-GHG-GAS-STORE` |
| N2O nitrification temperature sign publication/source conflict | theory/provenance gap | none | TCD-008 family |
| N2O reduction aeration-factor publication/source conflict | theory/provenance gap | none | TCD-008 family |

`TCD-032` and `TCD-033` are intentionally distinct. Both touch CH4 production, but one concerns withdrawals from source pools and the other concerns algebraic partition of production components. Likewise `TCD-035` and `TCD-036` remain distinct because the first concerns soil-layer phase reconstruction and the second concerns the ponding layer0 control volume.

The GHG hidden task-state finding does not get a new TCD because the controlling uncertainty is the same local-storage compiler contract already represented by TCD-011. If a historically qualified build contract later proves a separate physical-state defect beyond storage-duration semantics, B3 can reopen atomicity then.

The two N2O equation conflicts remain provenance/theory questions under TCD-008. External or publication agreement with one side is not enough to declare either revision-53 source or the publication wrong for the exact release.

## New fail-closed reservations

B3I01 reserved the following top-level identifiers only after checking the canonical tail, the existing TCD-028 reservation, branch allocations, and default-branch code search:

| ID | Phenomenon | Provisional class | Qualification owner |
| --- | --- | --- | --- |
| TCD-029 | Iflsol4 Detcoef/Coefdc coefficient cancellation | E | proposed ANIMO-NQ03 |
| TCD-030 | macropore initial NO3 validation seam | B | proposed ANIMO-MP03 |
| TCD-031 | macropore solute persistent restart omission | C | proposed ANIMO-MP04 |
| TCD-032 | methanogenesis source-pool transfer path | B | proposed ANIMO-GHG02 |
| TCD-033 | CH4 production component partition nonclosure | B | proposed ANIMO-GHG02 |
| TCD-034 | CH4 plant-growth temperature use-before-definition | B | proposed ANIMO-GHG02 |
| TCD-035 | GHG restart phase partition discontinuity | C | proposed ANIMO-GHG03 |
| TCD-036 | ponding layer0 GHG restart reconstruction gap | C | proposed ANIMO-GHG03 |
| TCD-037 | GHG Outbal working-array interface defect | A | proposed ANIMO-GHG04 |

A shared qualification workunit does not merge the TCDs it owns. For example proposed GHG02 may qualify TCD-032 through TCD-034 in one controlled work surface while keeping independent claims, evidence matrices and dispositions.

The proposed workunit names are routing assignments only. No branch for NQ03, MP03 or GHG02 existed in the live branch checks performed during intake, and B3I01 does not create those downstream workunits.

## Dependency routing

Class A candidates still require proof that the candidate changes reporting/accounting only and leaves physical states and process fluxes unchanged. Class B candidates need a closed local mathematical or species identity plus historical comparison or the formal historical-uncertainty route. Class C candidates need a complete state owner, initialization, persistence, restart and transition contract before numerical equivalence can be judged. Class E candidates need equation-derived convergence, precision and sensitivity evidence rather than a chosen tolerance.

The crosswalk in `POST_G5_LOCAL_FINDING_CROSSWALK.csv` records theory, B2, numerical and build-contract dependencies separately. A blocked dependency does not change the intake classification into stronger evidence.

## Non-admissions

This workunit changes governance artifacts only. It does not change frozen ANIMO source or testbank bytes. It performs no source correction and defines no production tolerance. `new_corrections_admitted=false`, `b3_baseline_established=false`, and `production_migration_admitted=false` remain hard outputs.

The intended closeout state is therefore `QUALIFIED_POST_G5_DISCREPANCY_CANONICAL_INTAKE_AND_ROUTING_NO_ADMISSIONS`, subject only to structural readback and cross-artifact consistency checks of the governance artifacts themselves.
