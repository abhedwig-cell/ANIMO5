# TCD-026 Independent Second-Line Review

Work unit: `ANIMO-B3A04R2`

Result: `PASS`

This result is independent second-line review evidence only. It is not B3 admission, does not authorize a production patch, and does not perform B4 or production migration.

## Independence and reviewed object

This review was performed in a separate ChatGPT context from the B3A04, B3A04R and B3D07 authoring contexts. No organizational or human independence is claimed.

The clean review branch was checked immediately before writing and was still exactly at:

`review/animo-b3a04r2-tcd026-independent-second-line@bd19ee247ba910eee234c67ec74def28d376c779`

That handoff commit has parent `21766eaf3443bcf432f05fbf6ba89d365bc70988`, the B3D07 route-reconciliation head. GitHub issue #28 was read first and had no comments at review start.

The review independently rechecked the source-bound evidence rather than accepting the B3A04 readiness conclusion, the B3A04R technical PASS, or the B3D07 route reconciliation as proof of the atomic claim.

## Atomic claim reviewed

Candidate observation:

```fortran
Bfom(Inip_x,Ly) = Bfom(Inip_x,Ly) + Ex(Ln) * P
```

The claim is only that the already-existing initial root-exudate organic-matter state `Ex(Ln)` belongs in the beginning fresh-organic-matter storage ledger `Bfom(Inip_x,Ly)` with the existing kg/m2 to kg/ha factor `P`.

The review does not change or qualify initialization physics, physical state, process fluxes, restart state, forcing, numerical policy, or any other organic-matter TCD.

## Frozen B0 identity

The repository sidecars at the reviewed authorities match the required frozen identities exactly:

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

The PREP06 source-reverification record is bound to the same source archive and reports an identity match. The source-audit implementation itself rejects a source zip whose SHA-256 differs from the frozen source identity before parsing it.

The licensed source archive bytes are not republished in GitHub. Because this workunit is intentionally GitHub-connector-only, this review does not claim a new raw-byte parse in this chat. It independently inspected the exact hash-bound audit implementation and the persisted source-reverification result. This limitation does not create a historical behavioural reference and is retained under residual uncertainty.

## Source and ownership recheck

The PREP06 conserved-state inventory identifies `Ex(:) -> Rsex(:)` as physical root-exudate organic matter, unit kg OM m-2, owned as a soil-layer physical storage. `INITIAL orgexu` supplies the current state. Root, Addit and Resp_miner paths can mutate it. `Init.for` commits the accepted boundary with `Ex(Ln) = Rsex(Ln)`, and restart output persists the result state.

The source-bound `audit_transfer_ledger_symmetry.py` implementation independently checks the relevant asymmetry by parsing uncommented Fortran statements. It tests all of the following against the frozen archive:

- beginning `Bfom(Inip_x,...)` contains no `Ex(Ln)`;
- ending `Bfom(Finp_x,...)` contains `Rsex(Ln)`;
- beginning organic-N storage includes `Ex(Ln)` with `Nifrex`;
- beginning organic-P storage includes `Ex(Ln)` with `Pofrex`.

The persisted PREP06 source-reverification result confirms that exact asymmetric source pattern. The narrow omitted fresh-OM beginning-storage term is therefore `Ex(Ln)*P`.

This is a Class-A shape under B3Q01: an already represented physical storage is omitted from a ledger surface, while the candidate write is confined to that ledger. No new state model, process algebra, restart semantics or numerical policy is introduced.

## Independent causal and non-interference evidence

The PREP06 synthetic discriminator changes only `Ex(1)` to `1.0e-3 kg m-2`, equivalent to exactly `10.0 kg ha-1`. The legacy first fresh-OM residual is `-10.0 kg ha-1`. Adding only the candidate beginning-storage observation removes that discriminator, with recorded residuals around `1e-10 kg ha-1`. Those small values are diagnostic floating-point effects, not an acceptance tolerance and not a whole-model equivalence threshold.

The model-produced CranMais restart replay supplies nonzero root-exudate state in layers 1 through 9 totaling `5989.6594 kg ha-1`. Candidate and legacy runs start from identical formatted restart bytes. The candidate increases the printed beginning fresh-OM store by `5989.66 kg ha-1`, final restart output remains byte-identical candidate versus legacy, and only the four declared fresh-OM balance/report surfaces differ.

The chronological CranMais activation is stronger because it produces the restart naturally in the preceding segment. The 1974 `INITIAL.OUT` is fed byte-identically into the 1975 segment. It contains `642.718929 kg ha-1` root-exudate mass over layers 1 through 9. The candidate adds `642.719 kg ha-1` to the printed beginning fresh-OM storage, candidate versus legacy final restart output is byte-identical, and only the four declared restart-case balance/report surfaces change.

The correct interpretation is narrow: candidate versus legacy restart-state identity from the same restart input supports Class-A non-interference. It does not prove that formatted restart is an exact checkpoint of uninterrupted execution.

The independent negative crosscheck confirms that uninterrupted CranMais and the formatted-restart route are not exactly identical. Of 564 compared numeric restart tokens, 32 differ, with maximum printed absolute difference `1.0e-6`. This remains a negative scope boundary. It is not converted into a tolerance, a restart equivalence claim, or a whole-model identity claim.

## Expected-difference contract

For the PREP06 synthetic discriminator, the observed and allowed changed outputs are exactly:

- `ani_omGP.Bal`;
- `ani_omRP.Bal`;
- `ani_omTP.Bal`;
- `baomGP.Out`;
- `baomRP.Out`;
- `baomTP.Out`.

For the two CranMais restart activations, the observed changed subset is exactly:

- `ani_omMP.Bal`;
- `ani_omTP.Bal`;
- `baomMP.Out`;
- `baomTP.Out`.

No unexpected scientific-output differences were observed in those probes. Physical state trajectories, process flux trajectories, initialization physics, candidate-versus-legacy restart state from identical restart input, forcing, numerical policy, `Bano`, `Bapo`, unrelated organic-matter ledgers and all non-whitelisted outputs remain outside the allowed difference surface.

Unexpected differences remain fail-closed. No numerical tolerance is used to enlarge this whitelist.

## SYNQ01, STATEQ02 and prior-review boundaries

The complete qualified SYNQ01 oracle register contains 12 oracles and no occurrence targeting `TCD-026`. There is therefore no TCD-026-specific SYNQ01 oracle. PREP06 and the CranMais activations must not be relabelled as SYNQ01 or as B2.

STATEQ02 is relevant only because it independently supports ownership of accepted physical continuation state and exact restore semantics within its restricted core. It explicitly is not a historical B2 reference and it does not make report accumulators part of physical continuation state. This review does not use STATEQ02 as a TCD-026 ledger oracle, a whole-model formatted-restart oracle, B2, or admission evidence.

B3A04R explicitly records its review type as `TECHNICAL_REVIEW_SAME_AUTHORING_CONTEXT_NOT_INDEPENDENT_SECOND_LINE` and keeps `independent_second_line_qualified=false`. Its technical PASS is therefore evidence input only and is not counted as this second line.

## Historical route and live validity

The relevant live route heads were rechecked:

- B3D07 remains exactly `21766eaf3443bcf432f05fbf6ba89d365bc70988`;
- GOV03 remains exactly `cbd262bdabe92923113b7326f2f42822ce9a971c`.

GOV03 records `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT` and only makes the historical-uncertainty route eligible subject to claim-scoped B3 requirements. It does not qualify historical behaviour. B3D07 remains `UNRESOLVED_NOT_ADMITTED` with independent second-line review as the blocking gate at the reviewed route head.

Because no qualified B2 historical behavioural reference exists, historical revision-53 behaviour remains `UNKNOWN`. This review makes no historical fidelity claim.

## Required check disposition

| # | Required independent check | Result |
|---|---|---|
| 1 | Exact frozen B0 source/testbank identity | PASS |
| 2 | `Ex(Ln)` physical ownership and lifecycle | PASS |
| 3 | `Bfom(Inip_x,Ly)` beginning-storage ownership | PASS |
| 4 | Exact omitted term `Ex(Ln)*P` | PASS |
| 5 | Class-A reporting-only atomicity | PASS |
| 6 | PREP06 synthetic 10.0 kg/ha discriminator | PASS |
| 7 | Model-produced CranMais restart activation | PASS |
| 8 | Chronological CranMais 1974 to 1975 formatted restart activation | PASS |
| 9 | Candidate-vs-legacy restart-state identity interpreted narrowly | PASS |
| 10 | Continuous-vs-formatted restart retained as negative scope boundary | PASS |
| 11 | Exact expected-difference whitelist and non-interference | PASS |
| 12 | No TCD-026-specific SYNQ01 oracle | PASS |
| 13 | STATEQ02 restricted to continuation-state ownership relevance | PASS |
| 14 | Same-context B3A04R technical PASS not counted as independent | PASS |
| 15 | GOV03 and B3D07 remain live valid | PASS |
| 16 | Historical revision-53 behaviour remains UNKNOWN | PASS |
| 17 | No historical fidelity claim | PASS |
| 18 | No composition, B4, production patch or production migration | PASS |
| 19 | This review performs no admission | PASS |

No required check remains unresolved.

## Evidence identities reviewed

Primary reviewed heads:

- `ANIMO-B3A04@5eaf02298603b85f802d8e35d6a63941d0878879`;
- `ANIMO-B3A04R@27b1700a330959d1b5eae23a2094cad579630f14`, evidence input only;
- `ANIMO-B3D07@21766eaf3443bcf432f05fbf6ba89d365bc70988`;
- `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`;
- `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- `ANIMO-STATEQ02@cb7c23524df6560e65a5bdc1ed19e0b6e3bd46c6`;
- `ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121`.

Selected exact evidence blobs:

- PREP06 exudate defect JSON: `0e60d8aaf526c0b0127da1143b68c9c8235e9fe3`;
- PREP06 source reverification: `bd0ec232f3de269c0f4251c30761b528a8d28e65`;
- PREP06 conserved-state inventory: `7893a1567a1c38eeadd08aaf4b571c1cf639bfa8`;
- frozen source audit tool: `5a07994d14979e23f6be8696e6c9f2391473c4d0`;
- B3Q01 qualification-class definition: `b67b46eff837ae03732e97dd43a3d6e1f1c220ed`;
- SYNQ01 oracle register: `4c215d19844614de8868380fb03f93268ea4c5d8`;
- B3A04R status: `69208a014b90d56d963f43763d8efab3f3582998`;
- B3D07 disposition: `9bc79b746aec21f541ead7db744623f666e57ba0`;
- B3D07 status: `d46c4ea7b0cd0744537a3908039bafa2e44477a5`;
- GOV03 status: `b85af297731f8bd84feddaf3aa23685549129496`.

The detailed machine-readable evidence and all 19 check findings are persisted in `integration/animo-b3/TCD026_INDEPENDENT_SECOND_LINE_REVIEW.json`.

## Decision

`PASS`

The atomic TCD-026 readiness claim survives independent second-line review within the stated boundaries. The result may be used as independent review evidence by a separate admission-closeout workunit. ANIMO-B3A04R2 itself performs no admission and stops here before any admission, composition, B4 work, production patch or production migration.
