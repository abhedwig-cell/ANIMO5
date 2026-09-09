# TCD-026 Class-A admission readiness

Work unit: `ANIMO-B3A04`

Target: `TCD-026`

Class: `A_ACCOUNTING_REPORTING_ONLY`

Status: `QUALIFIED_TCD026_CLASS_A_ADMISSION_READINESS_ROUTE_AND_INDEPENDENT_REVIEW_PENDING`

This work unit does not admit corrected legacy behaviour, does not patch physical state, does not change initialization physics and does not authorize production migration.

## 1. Atomic claim

The only claim qualified here is:

> `Ex(Ln)` is an already-existing, restartable root-exudate organic-matter store. Revision 53 includes the corresponding result state `Rsex(Ln)` in final fresh-organic-matter storage, but `Outbal_Init.for` omits `Ex(Ln)` from the beginning fresh-organic-matter ledger `Bfom(Inip_x,Ly)`. The candidate correction is therefore a ledger observation only: add `Ex(Ln) * P` to `Bfom(Inip_x,Ly)`.

No other organic-matter discrepancy is composed into this claim.

## 2. Frozen identities and canonical authority

The work unit starts from canonical branch `work/animo-b3i01-canonical-register-append` at `383c7a83e84a578969f92113280dc715b7bdddb4`.

Frozen B0 identities are:

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

The canonical TCD register classifies TCD-026 as `CONFIRMED_LEGACY_INITIAL_STORAGE_LEDGER_OMISSION`. B3Q01 classifies it as Class A with atomic claim `ATOMIC_INITIAL_STORAGE_LEDGER_CLAIM` and disposition `UNRESOLVED_NOT_ADMITTED` until the admission route and independent review gates are satisfied.

The supplied ANIMO 4.0 documentation is corroborating conceptual evidence only. It describes exudates as a distinct organic-matter pool and exposes initial `EX(NL)` in `INITIAL.INP`; it does not define the exact revision-53 beginning-storage ledger implementation. Exact ledger semantics therefore remain source-bound to frozen B0 and PREP06 evidence.

## 3. Exact physical owner

PREP06 conserved-state inventory identifies one relevant conserved state family:

`C-EX | root exudate organic matter | Ex -> Rsex | kg/m2 OM | Addit + Resp_miner | Init: Ex=Rsex | Bfom; Bano/Bapo via Nifrex/Pofrex`

The ownership chain is therefore:

1. `Ex(Ln)` is the current/start physical exudate-organic-matter state;
2. `Resp_miner` evolves the exudate store into result state `Rsex(Ln)`;
3. `Init.for` commits the accepted boundary by `Ex(Ln) = Rsex(Ln)`;
4. `Output_Init.for` persists the result state for restart;
5. `Bfom`, `Bano` and `Bapo` are observers/ledgers, not owners of physical mass.

The Class-A candidate must write only the observer `Bfom(Inip_x,Ly)`. It must not write `Ex`, `Rsex`, any initialization input or any process state.

## 4. Beginning/end storage identity

The physical accepted-boundary identity is:

`Ex_next(Ln) = Rsex_previous(Ln)`.

The corresponding fresh-organic-matter ledger must represent the same conserved store at both sides of its accounting interval:

- beginning contribution: `Ex(Ln) * P` into `Bfom(Inip_x,Ly)`;
- final contribution already present in revision 53: `Rsex(Ln) * Z` into `Bfom(Finp_x,Ly)`.

`P` and `Z` are retained as the legacy beginning/end ledger weighting/conversion factors used in their respective source contexts. This work unit does not infer or redefine them.

The exact omitted term is therefore:

```fortran
Bfom(Inip_x,Ly) = Bfom(Inip_x,Ly) + Ex(Ln) * P
```

This is an accounting observation of an existing store. It is not creation, deletion, redistribution or re-initialization of organic matter.

## 5. Conservation identity

For any selected fresh-organic-matter balance control volume, every persistent store owned by that control volume must be represented on both accounting boundaries. For the C-EX component this means:

`fresh_OM_begin = existing_begin_terms + sum(Ex(Ln) * P)`

and

`fresh_OM_end = existing_end_terms + sum(Rsex(Ln) * Z)`.

With all physical sources, sinks and internal transformations unchanged, omission of the beginning C-EX term creates an accounting residual equal to the negative omitted beginning mass.

PREP06 gives the causal discriminator. A RuurloGrass diagnostic with only `Ex(1)=1.0e-3 kg/m2`, equivalent to 10 kg/ha initial exudate OM, produces a first fresh-OM balance residual of exactly `-10.0 kg/ha`. A temporary ledger-only observation of `Ex(Ln)*P` reduces the maximum period residual from `10.0 kg/ha` to about `6.55e-11 kg/ha` and the cumulative residual to about `9.09e-11 kg/ha`.

Those tiny residuals are evidence of the causal effect only. They are not used as a tolerance and are not an admission criterion.

## 6. Physical state non-interference

The narrow candidate is structurally Class A because its write set is limited to `Bfom(Inip_x,Ly)`.

PREP06 independently of this work unit performed a temporary ledger-only diagnostic and compared 72 generated outputs after normalization of volatile timestamp/CPU metadata. Exactly six organic-matter balance files changed:

- `ani_omGP.Bal`;
- `ani_omRP.Bal`;
- `ani_omTP.Bal`;
- `baomGP.Out`;
- `baomRP.Out`;
- `baomTP.Out`.

No ordinary state/process output changed.

ANIMO-B3A04 added a second, stronger activation check using model-produced restart-format state. A frozen-source GNU diagnostic CranMais run produced `Output/initial.out` with nonzero persisted exudate state in layers 1 through 9, totalling `5989.6594 kg/ha`. Those exact `INITIAL.OUT` bytes, SHA-256 `254fa48dfd1349f6b0d2079b6dc0ca8ec16c35ea80bcd5b8eb464bd60b770a86`, were replayed as `Input/initial.inp` in both the legacy and ledger-only diagnostic runs.

The legacy replay showed a first-period fresh-OM deviation printed as `-5.99E+03 kg/ha`. The ledger-only candidate increased printed beginning fresh-OM storage from `10943.275` to `16932.935 kg/ha`, an increment of `5989.66 kg/ha`, and reduced the printed first-period deviation to `-7.28E-12 kg/ha`. The difference between the exact model-produced `5989.6594 kg/ha` and the printed `5989.66 kg/ha` increment is report rounding, not a tolerance.

The resulting `Output/initial.out` files from legacy and candidate replay were byte-identical with SHA-256 `f1a3d8f600675d4f6ac3da4039b3625f416d7bbfb699152a092f4f2c4df3bc9b`. Across 22 scientific output surfaces compared after only known volatile timestamp/CPU normalization, exactly four fresh-OM balance surfaces changed: `ani_omMP.Bal`, `ani_omTP.Bal`, `baomMP.Out` and `baomTP.Out`. No unexpected surface changed.

This replay is deliberately classified as `MODEL_PRODUCED_RESTART_FORMAT_STATE_REPLAY_NOT_CHRONOLOGICAL_SPLIT_RUN`. It proves model-produced state-path activation and non-interference, but does not claim accepted-boundary chronological continuation or split-run identity.

Result for readiness: `PASS_FOR_READINESS`.

Machine evidence: `integration/animo-b3/TCD026_MODEL_PRODUCED_STATE_REPLAY.json`.

## 7. Process-flux non-interference

The candidate does not recompute or mutate mineralization, organic transformation, transport, hydrology, crop, management or boundary fluxes. `Ex` and `Rsex` continue to follow the frozen physical process path.

PREP06 found no unintended ordinary output differences outside the fresh-OM balance surfaces. The B3A04 model-produced-state replay independently retained all non-whitelisted normalized scientific surfaces and produced byte-identical restart output state.

Result for readiness: `PASS_FOR_READINESS`.

## 8. Total physical mass non-interference

The omitted quantity already exists physically before the candidate observation and remains physically present after it. The candidate neither adds nor removes mass from `Ex`, `Rsex` or any other store.

The model-produced-state replay strengthens this claim because the same model-produced initial-state bytes were consumed by legacy and candidate runs and their resulting `Output/initial.out` bytes were identical.

The physical mass trajectory is therefore invariant within the observed replay. Only the bookkeeping representation of beginning storage changes.

Result for readiness: `PASS_FOR_READINESS`.

## 9. Changed-output whitelist

The semantic whitelist is declared before any future admission implementation:

Allowed to change:

- `Bfom(Inip_x,Ly)` for balance profiles containing nonzero initial `Ex`;
- fresh-organic-matter balance deviations and report fields causally derived from that beginning-storage ledger;
- organic-matter balance files derived from those affected Bfom balance sets.

Must remain unchanged:

- all physical states, including `Ex` and `Rsex`;
- all initialization and restart-state values;
- all process fluxes;
- total physical OM mass trajectory;
- all nitrogen ledgers including `Bano`;
- all phosphorus ledgers including `Bapo`;
- all water ledgers;
- all ordinary state/process outputs;
- all unrelated organic-matter ledger terms.

Any unexpected difference fails closed. No numerical tolerance is introduced for the whitelist or non-interference claim.

Machine-readable contract: `integration/animo-b3/TCD026_EXPECTED_DIFFERENCE.json`.

## 10. Natural B1 activation, structural start-state unreachability and model-produced state activation

Ordinary natural activation at the supplied model start is not available.

PREP06 audited the supplied `>orgexu:` initial conditions and found every initial exudate value zero. Therefore the TCD-026 beginning-storage omission is structurally unobservable in the ordinary supplied natural starts: the omitted term evaluates exactly to zero.

ANIMO-B3A04 then tested whether the model itself can generate a nonzero persisted exudate state rather than manually inventing one. It can. A normal CranMais diagnostic execution produced nonzero `Rsex` persisted through `Output_Init` into restart-format `INITIAL.OUT`; layers 1 through 9 were nonzero and summed to `5989.6594 kg/ha`. Replaying those exact bytes through the ordinary `INITIAL.INP` path activated the TCD-026 omission exactly as predicted.

This is stronger naturalistic path evidence than the manually seeded PREP06 microcase, but it is not a true chronological restart. Hydrology and management chronology were replayed from the original case start. Therefore ANIMO-B3A04 does not claim split-run identity, continuation equivalence or historical restart behaviour.

Result:

- ordinary supplied natural start activation: `STRUCTURALLY_UNREACHABLE_ZERO_INITIAL_EX`;
- dedicated synthetic causal activation: `PASS_PREP06_SYNTHETIC`;
- model-produced restart-format state activation: `PASS_CRANMAIS_REPLAY_NOT_CHRONOLOGICAL_SPLIT_RUN`;
- historical B2 activation: `NOT_AVAILABLE`.

## 11. Negative controls

Four negative controls bind the claim:

1. **Zero-Ex control.** With all initial `Ex(Ln)=0`, the candidate term is exactly zero. The ordinary CranMais frozen-input first-period fresh-OM deviation remained only `-1.46E-11 kg/ha`, so the large replay discrepancy requires nonzero initial Ex rather than appearing generically.
2. **N/P control.** Revision-53 organic-N and organic-P beginning ledgers already include the same physical exudate store through `Ex*Nifrex*P` and `Ex*Pofrex*P`. TCD-026 must not modify `Bano` or `Bapo`.
3. **Other-organic-store control.** `Os`, `Huos`, `Huex`, DOM and other organic-matter stores retain their existing ownership and accounting. TCD-026 must not absorb any other organic-matter discrepancy.
4. **Ordinary-output control.** When nonzero model-produced Ex activates the candidate observation, ordinary state/process outputs and restart state must remain identical. PREP06 and the B3A04 model-produced-state replay both support this.

## 12. SYNQ01 applicability

SYNQ01 is qualified as an independent synthetic-oracle layer, but its current TCD coverage matrix has explicit entries for TCD-015, TCD-017, TCD-018, TCD-019, TCD-023, TCD-024 and TCD-025 only. It contains no TCD-026 oracle.

No SYNQ01 oracle is therefore claimed as independent authority for this work unit. Reusing the interception-storage oracle `SYNQ-O003` would be an invalid scope substitution because its conserved quantity and control volume are water/interception, not exudate organic matter.

The closed C-EX storage identity is source/conservation evidence. The PREP06 causal probe and B3A04 model-produced-state replay are supporting causal/non-interference evidence. None is relabelled as an independent SYNQ01 oracle or independent second-line review.

## 13. Route gate

GOV02 requires a valid historical-reference route or a properly closed historical-uncertainty route for Class-A admission.

Live PREP02R status at head `a2fda49871ee3c7104daf7e06cd8dffdac06b125` remains:

`PARTIAL_RECOVERY_WINDOWS_NATIVE_CAPTURE_READY_HISTORICAL_REFERENCE_STILL_BLOCKED`.

It explicitly records:

- `normal_B2_reference_available=false`;
- `historical_uncertainty_route_eligible=false`;
- `external_request_sent=false`;
- `reference_qualified=false`.

Therefore ANIMO-B3A04 cannot admit corrected-legacy behaviour.

Route gate: `PENDING_BLOCKED`.

## 14. Independent review handoff

An independent second-line reviewer must verify at minimum:

- frozen B0 identities and canonical TCD-026 scope;
- C-EX physical ownership and `Ex -> Rsex -> Ex_next` lifecycle;
- exact beginning/end Bfom asymmetry;
- exact omitted term `Ex(Ln)*P`;
- 10 kg/ha PREP06 causal discriminator without treating the post-correction residual as a tolerance;
- the CranMais model-produced state replay, including the `5989.6594 kg/ha` generated Ex state, same replay-input bytes, legacy `-5.99E+03 kg/ha` printed deviation and candidate-only fresh-OM balance changes;
- the explicit boundary that this replay is not a chronological split-run or B2 reference;
- physical state, process-flux and total-mass non-interference;
- output whitelist and all negative controls;
- structural reason ordinary supplied start activation is unavailable;
- absence of a currently applicable SYNQ01 oracle;
- GOV02/PREP02R route state;
- non-composition with other organic-matter TCDs.

The authoring and additional replay work performed in ANIMO-B3A04 are not independent review and must not be counted as such.

Review packet: `docs/b3/TCD026_SECOND_LINE_REVIEW_PACKET.md`.

Machine request: `integration/animo-b3/TCD026_SECOND_LINE_REVIEW_REQUEST.json`.

## 15. Atomic exclusions

Explicitly excluded:

- any change to `Ex`, `Rsex` or other physical state;
- any INITIAL.INP parsing or initialization physics change;
- any change to exudate production/decomposition/mineralization;
- any correction of other fresh-OM, humus, dissolved-OM or ploughing ledgers;
- composition with any other organic-matter TCD;
- any numerical tolerance policy;
- chronological restart/split-run qualification;
- corrected-legacy admission;
- production migration.

## 16. Readiness decision

The narrow Class-A hypothesis is supported rather than falsified:

`TCD-026 is an accounting/reporting-only beginning-storage omission for the existing C-EX physical store within the qualified scope.`

The evidence is sufficient to qualify admission readiness. The physical owner, exact omitted term, conservation identity, synthetic causal activation, model-produced restart-format state activation, non-interference surfaces, output whitelist, ordinary-start structural unreachability and negative controls are explicit.

It is not sufficient for corrected-legacy admission. The route gate remains blocked and independent second-line review has not occurred. The model-produced state replay also does not substitute for a true chronological split-run qualification or a historical B2 reference.

Final status:

`QUALIFIED_TCD026_CLASS_A_ADMISSION_READINESS_ROUTE_AND_INDEPENDENT_REVIEW_PENDING`
