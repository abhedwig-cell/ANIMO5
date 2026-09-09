# TCD-026 Class-A admission readiness

Work unit: `ANIMO-B3A04`

Target: `TCD-026`

Class: `A_ACCOUNTING_REPORTING_ONLY`

Status: `QUALIFIED_TCD026_CLASS_A_ADMISSION_READINESS_ROUTE_AND_INDEPENDENT_REVIEW_PENDING`

This work unit qualifies only admission readiness. It does not admit corrected legacy behaviour, patch physical state, change initialization physics, introduce a tolerance or authorize production migration.

## 1. Atomic claim

The only claim is that revision-53 beginning fresh-organic-matter accounting omits an already-existing root-exudate store:

```fortran
Bfom(Inip_x,Ly) = Bfom(Inip_x,Ly) + Ex(Ln) * P
```

`Ex(Ln)` is physical state. `Bfom` is an observer/ledger. No other organic-matter discrepancy is composed into TCD-026.

## 2. Frozen and governance basis

Canonical base:

`work/animo-b3i01-canonical-register-append@383c7a83e84a578969f92113280dc715b7bdddb4`

Frozen B0:

- source SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

Canonical TCD classification:

`CONFIRMED_LEGACY_INITIAL_STORAGE_LEDGER_OMISSION`

B3Q01 classification:

`A | ATOMIC_INITIAL_STORAGE_LEDGER_CLAIM | UNRESOLVED_NOT_ADMITTED`

The ANIMO 4.0 user documentation is conceptual corroboration only. Exact revision-53 ledger semantics are source-bound.

## 3. Physical owner and accepted-boundary identity

PREP06 identifies C-EX as:

`root exudate organic matter | Ex -> Rsex | kg/m2 OM | Addit + Resp_miner | Init: Ex=Rsex`

The lifecycle is:

1. `Ex(Ln)` is the accepted/start exudate-organic-matter state.
2. Model processes evolve it to result state `Rsex(Ln)`.
3. `Init.for` promotes accepted continuation by `Ex(Ln)=Rsex(Ln)`.
4. `Output_Init.for` persists `Rsex` into restart-format state.
5. `Bfom`, `Bano` and `Bapo` observe mass; they do not own it.

The accepted-boundary identity is therefore:

`Ex_next(Ln) = Rsex_previous(Ln)`.

STATEQ02 independently strengthens the state-ownership side of this claim. Its persistent-state matrix classifies `ORG-004 root exudate organic mass` as a core C/N/P accepted owner, mandatory for checkpointing and requiring exact accepted areic-mass restore. STATEQ02 itself remains a restricted-core checkpoint qualification, not a TCD-026 ledger oracle and not B2 evidence.

## 4. Exact ledger asymmetry

Beginning fresh-OM storage in `Outbal_Init.for` includes the existing fresh fractions and humus stores but omits `Ex(Ln)`.

Final fresh-OM storage in `Outbal_calc.for` includes:

```fortran
Bfom(Finp_x,Ly) = Bfom(Finp_x,Ly) + Rsex(Ln) * Z
```

Organic-N and organic-P beginning ledgers already include the same exudate store through:

```fortran
Ex(Ln) * Nifrex(Ln) * P
Ex(Ln) * Pofrex(Ln) * P
```

The missing fresh-OM beginning observation is therefore exactly:

```fortran
Ex(Ln) * P
```

`P` and `Z` remain the legacy beginning/end conversion or weighting factors in their respective contexts. This work unit does not redefine them.

## 5. Conservation identity

For the C-EX component:

`fresh_OM_begin = existing_begin_terms + sum(Ex(Ln)*P)`

`fresh_OM_end = existing_end_terms + sum(Rsex(Ln)*Z)`

With physical sources, sinks and internal transformations unchanged, omission of beginning `Ex` produces a deterministic accounting residual containing the negative omitted beginning mass.

This identity is component-local and does not authorize correction of any other OM ledger term.

## 6. PREP06 causal discriminator

PREP06 changed only one initial value in a diagnostic RuurloGrass copy:

`Ex(1)=1.0e-3 kg/m2 = 10.0 kg/ha OM`.

Frozen legacy source then produced a first fresh-OM residual of exactly:

`-10.0 kg/ha`.

A temporary ledger-only diagnostic adding only `Ex(Ln)*P` reduced:

- maximum period residual from `10.0` to about `6.55e-11 kg/ha`;
- cumulative residual to about `9.09e-11 kg/ha`.

These small residuals are observations, not tolerances.

PREP06 compared 72 generated outputs after only volatile timestamp/CPU normalization. Exactly six OM balance files changed and no ordinary state/process output changed:

- `ani_omGP.Bal`
- `ani_omRP.Bal`
- `ani_omTP.Bal`
- `baomGP.Out`
- `baomRP.Out`
- `baomTP.Out`

## 7. Supplied natural-start coverage

PREP06 found all supplied `>orgexu:` initial values exactly zero. The ordinary supplied natural starts therefore cannot activate TCD-026 because the omitted term is exactly zero.

This is classified as:

`STRUCTURALLY_UNREACHABLE_ZERO_INITIAL_EX_IN_SUPPLIED_NATURAL_TESTBANK`

It is not silently counted as a natural PASS.

## 8. Model-produced restart-format replay

B3A04 first established that ANIMO itself can generate a relevant nonzero restart-format state.

A normal CranMais diagnostic run produced nonzero persisted exudate state in layers 1 through 9, total:

`5989.6594 kg/ha`.

Producer `INITIAL.OUT` SHA-256:

`254fa48dfd1349f6b0d2079b6dc0ca8ec16c35ea80bcd5b8eb464bd60b770a86`

Those exact bytes were replayed through the ordinary `INITIAL.INP` parser in legacy and ledger-only diagnostic runs.

Observed beginning FOM:

- legacy `10943.275 kg/ha`;
- candidate `16932.935 kg/ha`;
- increment `5989.66 kg/ha`, the reported form of model-produced `5989.6594 kg/ha`.

First fresh-OM deviation:

- legacy approximately `-5990 kg/ha`;
- candidate `-7.28e-12 kg/ha`.

Legacy and candidate final `Output/initial.out` were byte-identical. Across 22 normalized scientific surfaces only these four changed:

- `ani_omMP.Bal`
- `ani_omTP.Bal`
- `baomMP.Out`
- `baomTP.Out`

This replay was not chronological because original hydrology and management chronology were replayed from their original origin. It is retained only as model-produced state-path and non-interference evidence.

Machine evidence:

`integration/animo-b3/TCD026_MODEL_PRODUCED_STATE_REPLAY.json`

## 9. Chronological 1974 to 1975 formatted-restart activation

B3A04 then executed a stronger bounded chronological probe on CranMais.

### 9.1 Segment A

Segment A ran:

`1974-01-01 -> 1974-12-31`

The frozen testbank archive remained unchanged. An execution-copy management file was bounded to the first 1974 management period so that the shortened simulation remained internally valid.

Segment A completed and generated `INITIAL.OUT` SHA-256:

`6578e35e7b5bd39927569ff4f004afbe164d2ce20c98a6d75dc75b7ab536764b`

The model-produced exudate state was nonzero in layers 1 through 9 and summed to:

`0.0642718929 kg/m2 = 642.718929 kg/ha`.

### 9.2 Segment B

Segment B ran:

`1975-01-01 -> 1975-12-31`

Its `INITIAL.INP` was byte-for-byte the Segment-A `INITIAL.OUT` above. No Ex value was manually synthesized.

The prepared hydrology payload and material payload remained unchanged. The management execution-copy retained the original 1975 maize period and the original 1975 additions, with their local relative-day origin rebased from the completed 365-day 1974 segment. The frozen testbank archive was not modified.

Both legacy and ledger-only candidate executions completed.

### 9.3 TCD-026 discriminator

Legacy Segment-B beginning FOM:

`12209.622 kg/ha`

Candidate beginning FOM:

`12852.341 kg/ha`

Difference:

`642.719 kg/ha`

That equals the model-produced `642.718929 kg/ha` beginning Ex subject only to legacy report formatting.

Legacy first-period FOM deviation is reported as approximately:

- `-642.7 kg/ha` in the detailed balance;
- `-643 kg/ha` in the scientific-format report.

Candidate first-period deviation:

`1.82e-12 kg/ha`.

Again, the tiny residual is not a tolerance.

### 9.4 Class-A non-interference

Legacy and candidate Segment-B final restart state are byte-identical:

`e6c240ae46edfb7d0a4577dfb70106fb10e37b78982f93d2a116130f9685ca42`

Twenty-three generated scientific/model outputs were compared after only known volatile timestamp/CPU normalization:

- 19 normalized-identical;
- exactly four changed;
- zero unexpected changes.

Changed surfaces:

- `ani_omMP.Bal`
- `ani_omTP.Bal`
- `baomMP.Out`
- `baomTP.Out`

This directly strengthens the physical-state, process-output and changed-output-whitelist non-interference evidence for the narrow Class-A candidate.

Machine evidence:

`integration/animo-b3/TCD026_CHRONOLOGICAL_RESTART_PROBE.json`

## 10. Important restart limitation

The chronological probe also compared a continuous 1974 to 1975 CranMais execution with the legacy formatted 1974/1975 restart route.

The final formatted restart states were not byte-identical.

Across 564 printed numeric tokens:

- 32 differed;
- maximum absolute printed difference was `1.0e-6`.

B3A04 does not hide this with a tolerance and does not promote the legacy `INITIAL.OUT/INITIAL.INP` route to an exact whole-model checkpoint.

The observed small drift is compatible with finite formatted serialization and/or other legacy restart-surface limitations, but this work unit did not isolate the cause. It is therefore recorded as a scope limitation rather than explained away.

This finding does not falsify TCD-026. The TCD-026 discriminator is the missing beginning `Ex` ledger observation and is orders of magnitude larger, exactly tied to the model-produced beginning Ex mass, and removed by an observer-only change while the compared legacy/candidate restart state is identical.

## 11. Relation to STATEQ02

STATEQ02 independently qualified a different restart mechanism:

`run -> accepted boundary -> exact qualification-only checkpoint -> restore -> continue`

within a restricted C/N/P profile. Five split boundaries were exact bitwise with no tolerance, including an 833-record entire remaining-horizon witness from split 67.

Relevant to TCD-026, STATEQ02 treats root-exudate OM as accepted checkpoint state. This corroborates state ownership and continuation relevance.

It does not qualify the TCD-026 beginning `Bfom` observation because STATEQ02 uses a qualification-only exact checkpoint and resumes ordinary execution after restore rather than using the legacy formatted initial-balance path as a TCD-026 oracle.

Therefore:

- STATEQ02 supports C-EX ownership and restart relevance;
- STATEQ02 is not a TCD-026 independent ledger oracle;
- STATEQ02 is not B2 historical-reference evidence;
- B3A04's formatted-restart drift does not contradict STATEQ02's exact custom checkpoint result.

## 12. Non-interference decision

The candidate write set is limited to `Bfom(Inip_x,Ly)`.

Physical state non-interference: `PASS_FOR_READINESS`.

Process-flux non-interference: `PASS_FOR_READINESS`.

Total physical mass non-interference: `PASS_FOR_READINESS`.

Evidence basis now includes:

- PREP06 72-output synthetic causal comparison;
- B3A04 model-produced restart-format replay;
- B3A04 chronological 1974 to 1975 formatted-restart activation;
- byte-identical legacy/candidate final restart state in both B3A04 activation probes.

## 13. Changed-output whitelist

Allowed to change:

- beginning `Bfom` where nonzero initial Ex activates the term;
- fresh-OM balance deviations derived from that beginning storage;
- Bfom-derived fresh-OM balance/report files.

Must remain unchanged:

- `Ex`, `Rsex` and every physical state;
- initialization/restart-state values;
- all process fluxes;
- total physical OM trajectory;
- `Bano` and all N ledgers;
- `Bapo` and all P ledgers;
- water ledgers;
- ordinary state/process outputs;
- unrelated OM ledger terms.

Any unexpected difference fails closed. No tolerance is part of this contract.

## 14. Negative controls

1. Zero Ex: candidate term is exactly zero. Supplied natural starts remain unaffected.
2. N/P: Bano and Bapo already include the exudate store and must not change.
3. Other OM stores: no other fresh, humus, DOM or ploughing discrepancy is included.
4. Ordinary outputs: non-Bfom state/process surfaces remain unchanged in causal probes.
5. Formatted restart exactness: continuous-versus-formatted-restart identity is explicitly not qualified. The observed `1e-6` printed-state drift is retained, not tolerated away.

## 15. SYNQ01 boundary

Current SYNQ01 has no TCD-026 oracle. `SYNQ-O003` is an interception-water oracle and cannot be substituted.

PREP06, B3A04 replay, B3A04 chronological probe and STATEQ02 are not relabelled as a TCD-026 SYNQ oracle.

## 16. Route gate

At the latest live check PREP02R remains:

`PARTIAL_RECOVERY_WINDOWS_NATIVE_CAPTURE_READY_HISTORICAL_REFERENCE_STILL_BLOCKED`

with:

- `normal_B2_reference_available=false`;
- `historical_uncertainty_route_eligible=false`;
- `reference_qualified=false`.

Therefore:

`valid_admission_route = PENDING_BLOCKED`

No corrected-legacy admission is authorized.

## 17. Independent second-line review

An independent reviewer must recheck at least:

- frozen B0 identity;
- canonical atomic TCD-026 scope;
- C-EX ownership and `Ex -> Rsex -> Ex_next` lifecycle;
- exact beginning/end Bfom asymmetry;
- exact candidate `Ex(Ln)*P`;
- PREP06 10 kg/ha causal discriminator;
- model-produced replay evidence;
- chronological 1974/1975 evidence and its management-tail provenance;
- exact `642.718929 -> 642.719 kg/ha` causal match subject only to reporting precision;
- byte-identical legacy/candidate final restart state;
- output whitelist and negative controls;
- the explicit continuous-versus-formatted-restart non-identity result;
- STATEQ02 only as ownership/continuation cross-support, never as a TCD-026 ledger oracle;
- SYNQ01 non-applicability;
- live GOV02/PREP02R route state;
- non-composition with other OM TCDs.

ANIMO-B3A04 authoring and execution do not count as independent review.

## 18. Atomic exclusions

Excluded:

- physical-state patching;
- initialization-physics changes;
- exudate process changes;
- other organic-matter ledger corrections;
- TCD composition;
- numerical tolerance;
- promotion of legacy formatted restart to an exact whole-model checkpoint;
- corrected-legacy admission;
- production migration.

## 19. Readiness decision

The narrow hypothesis is supported rather than falsified:

`TCD-026 is an accounting/reporting-only omission of existing beginning C-EX storage from Bfom.`

The chronological probe materially strengthens applicability because the omitted store was generated by an earlier real model segment, persisted by the model, consumed at the next chronological year boundary and reproduced the predicted accounting residual. The observer-only candidate removes that residual while preserving the compared physical restart state and ordinary outputs.

The work unit remains deliberately short of admission because two external gates remain open:

1. independent second-line review;
2. a GOV02-valid admission route.

Final status:

`QUALIFIED_TCD026_CLASS_A_ADMISSION_READINESS_ROUTE_AND_INDEPENDENT_REVIEW_PENDING`
