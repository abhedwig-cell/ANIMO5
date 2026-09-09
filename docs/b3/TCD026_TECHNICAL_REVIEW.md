# TCD-026 technical review

Work unit: `ANIMO-B3A04R`

Target: `TCD-026`

Reviewed candidate branch: `work/animo-b3a04-tcd026-class-a-readiness`

Reviewed candidate head: `5eaf02298603b85f802d8e35d6a63941d0878879`

Technical disposition:

`PASS_TCD026_CLASS_A_TECHNICAL_READINESS_REVIEWED`

Governance disposition:

`UNRESOLVED_NOT_ADMITTED_INDEPENDENT_SECOND_LINE_AND_VALID_ROUTE_STILL_REQUIRED`

This work unit deliberately does **not** claim the B3Q01 independent-second-line gate. It is executed from the same ChatGPT authoring context that prepared ANIMO-B3A04. Re-fetching, cross-checking and technically reviewing the evidence strengthens the dossier, but does not create genuine reviewer independence.

## 1. Frozen identities and canonical scope

The reviewed dossier pins frozen B0 to:

- source ZIP SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

The canonical TCD register was re-fetched at `383c7a83e84a578969f92113280dc715b7bdddb4`. TCD-026 remains the fresh-organic-matter initial exudate-storage finding and remains classified `CONFIRMED_LEGACY_INITIAL_STORAGE_LEDGER_OMISSION`.

B3Q01 was re-fetched at `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`. TCD-026 remains:

- provisional class `A`;
- atomicity `ATOMIC_INITIAL_STORAGE_LEDGER_CLAIM`;
- current B2 status `NOT_ESTABLISHED`;
- disposition `UNRESOLVED_NOT_ADMITTED`.

Result: `PASS`.

## 2. Exact physical owner and ledger asymmetry

PREP06 was re-fetched at `9b1f1ea51c24fb82823290193651830dc61ea3c8`.

Its source-bound ownership chain remains:

1. `Ex(Ln)` is read as persistent root-exudate organic-matter state;
2. `Resp_miner` evolves it to `Rsex(Ln)`;
3. `Init.for` commits `Ex(Ln)=Rsex(Ln)`;
4. `Output_Init.for` persists `Rsex` for restart.

The exact ledger asymmetry also remains source-bound:

- ending `Bfom(Finp_x,Ly)` includes `Rsex(Ln)*Z`;
- beginning `Bfom(Inip_x,Ly)` omits `Ex(Ln)*P`;
- beginning organic-N already includes `Ex*Nifrex*P`;
- beginning organic-P already includes `Ex*Pofrex*P`.

Therefore the only reviewed Class-A candidate remains:

```fortran
Bfom(Inip_x,Ly) = Bfom(Inip_x,Ly) + Ex(Ln) * P
```

No physical owner, state transition, initialization rule or process equation is changed by that observation.

Result: `PASS`.

## 3. Closed component conservation identity

For the C-EX component the accepted-boundary state identity is:

`Ex_next(Ln) = Rsex_previous(Ln)`.

The corresponding beginning/end fresh-OM ledger identity requires observation of the same persistent store on both accounting boundaries:

- beginning contribution `sum(Ex(Ln)*P)`;
- ending contribution `sum(Rsex(Ln)*Z)`.

The candidate therefore repairs only beginning-storage coverage. It does not create, destroy or redistribute organic matter.

Result: `PASS_FOR_ATOMIC_COMPONENT`.

## 4. Causal activation evidence

Three evidence levels are now consistent with the same atomic claim.

### PREP06 synthetic discriminator

A diagnostic RuurloGrass copy changed only `Ex(1)` to `1.0e-3 kg/m2`, equivalent to `10.0 kg/ha` OM.

Observed legacy first fresh-OM residual: `-10.0 kg/ha`.

The Bfom-only candidate reduces the maximum period residual to approximately `6.55e-11 kg/ha` and cumulative residual to approximately `9.09e-11 kg/ha`.

### Model-produced restart-format replay

ANIMO-B3A04 produced nonzero CranMais exudate state itself, totalling `5989.6594 kg/ha`, persisted it in `INITIAL.OUT`, and replayed the exact bytes through the normal `INITIAL.INP` path.

Legacy first-period fresh-OM deviation printed approximately `-5990 kg/ha`; the Bfom-only candidate increased beginning storage by the printed `5989.66 kg/ha` and reduced the printed deviation to `-7.28e-12 kg/ha`.

### Chronological formatted restart activation

ANIMO-B3A04 then executed CranMais 1974 as Segment A and used its exact model-produced `INITIAL.OUT` bytes as Segment-B `INITIAL.INP` for 1975.

The year-boundary restart state contained `642.718929 kg/ha` Ex. The candidate increased printed beginning fresh-OM storage by `642.719 kg/ha`. Legacy first-period deviation was approximately `-642.7` to `-643 kg/ha`; candidate deviation was `1.82e-12 kg/ha`.

All three activation paths exhibit the same causal signature: the legacy residual equals the omitted beginning exudate store subject only to legacy report formatting.

Result: `PASS`.

## 5. No-tolerance boundary

No numerical acceptance tolerance is introduced.

The approximately `1e-11` to `1e-12 kg/ha` post-candidate residuals are recorded results, not epsilons. Likewise, printed `5989.66` versus exact `5989.6594`, and printed `642.719` versus exact `642.718929`, are legacy formatting effects rather than acceptance bands.

Result: `PASS`.

## 6. Physical-state, flux and mass non-interference

The candidate write set is restricted to the beginning `Bfom` ledger observer.

PREP06 compared 72 generated outputs and found exactly six fresh-OM balance/report differences with no ordinary state/process differences.

In the model-produced replay, legacy and candidate resulting `Output/initial.out` were byte-identical and only four fresh-OM balance/report surfaces changed after declared volatile normalization.

In the chronological 1975 Segment-B comparison, legacy and candidate final `INITIAL.OUT` were again byte-identical at:

`e6c240ae46edfb7d0a4577dfb70106fb10e37b78982f93d2a116130f9685ca42`

Of 23 compared scientific/model outputs, 19 were normalized-identical and exactly four changed:

- `ani_omMP.Bal`;
- `ani_omTP.Bal`;
- `baomMP.Out`;
- `baomTP.Out`.

Unexpected changed outputs: `0`.

This is consistent with:

- physical-state non-interference;
- process-flux non-interference;
- total physical OM mass non-interference;
- the predeclared changed-output whitelist.

Result: `PASS_FOR_READINESS`.

## 7. Formatted-restart negative control retained

The chronological probe also compared a continuous 1974-1975 execution with the legacy formatted `INITIAL.OUT -> INITIAL.INP` split path.

The formatted path is **not** exact whole-model restart identity:

- numeric tokens compared: `564`;
- printed tokens different: `32`;
- maximum absolute printed difference: `1.0e-6`;
- final restart-state files are not byte-identical.

ANIMO-B3A04 correctly retained this as a negative scope boundary instead of hiding it with a tolerance.

This does not falsify the TCD-026 Class-A claim because the relevant candidate-versus-legacy Segment-B experiment begins from identical restart bytes and ends with byte-identical physical restart state while only whitelisted Bfom-derived outputs change.

It does mean that B3A04 may not be cited as qualification of the legacy formatted restart mechanism as an exact whole-model checkpoint.

Result: `PASS_SCOPE_BOUNDARY_RETAINED`.

## 8. STATEQ02 cross-stream evidence

STATEQ02 was re-fetched at `cb7c23524df6560e65a5bdc1ed19e0b6e3bd46c6`.

It remains a B0-hash-pinned diagnostic split-run qualification with exact bitwise continuation inside a restricted qualification-only checkpoint representation. Its evidence supports the general proposition that core C/N/P continuation state must be explicitly checkpointed and restored exactly.

ANIMO-B3A04 uses STATEQ02 only as cross-stream support for continuation-state ownership/relevance. It does not promote STATEQ02 to:

- a TCD-026 Bfom ledger oracle;
- a historical B2 reference;
- proof that the legacy formatted restart file is exact.

Result: `PASS_SCOPE_USE`.

## 9. SYNQ01 boundary

SYNQ01 was re-fetched at `842f72300fd03ede0b9024537a7ee6126722a121`.

Its qualified coverage matrix contains TCD-015, TCD-017, TCD-018, TCD-019, TCD-023, TCD-024 and TCD-025. It contains no TCD-026-specific oracle.

No unrelated oracle may be substituted as independent TCD-026 evidence.

Result: `PASS_NO_FALSE_ORACLE_CLAIM`.

## 10. Live admission-route recheck

PREP02R was rechecked live at:

`a2fda49871ee3c7104daf7e06cd8dffdac06b125`

Status remains:

`PARTIAL_RECOVERY_WINDOWS_NATIVE_CAPTURE_READY_HISTORICAL_REFERENCE_STILL_BLOCKED`

It still records:

- `normal_B2_reference_available=false`;
- `historical_uncertainty_route_eligible=false`;
- `historical_reference_artifact_obtained=false`;
- `reference_qualified=false`;
- `external_request_sent=false`.

Therefore no GOV02-valid corrected-legacy admission route is open.

Result: `FAIL_PENDING_NO_VALID_ROUTE`.

## 11. Reviewer-independence gate

This technical review was produced in the same ChatGPT authoring context that prepared ANIMO-B3A04.

That is not genuine second-line independence under B3Q01. A separate branch alone does not create reviewer independence.

Result: `FAIL_NOT_INDEPENDENT`.

This is a governance failure, not a reversal of the technical PASS findings.

## 12. Atomic exclusions

This review does not authorize or compose:

- any physical-state change;
- initialization-physics change;
- exudate process change;
- another organic-matter TCD;
- a numerical tolerance;
- exact whole-model legacy formatted restart qualification;
- corrected-legacy admission;
- production migration.

## Final decision

The TCD-026 Class-A technical readiness case survives direct technical review and is stronger than the original PREP06-only dossier because it now includes model-produced and chronological restart activation with candidate-versus-legacy non-interference.

However, admission remains fail-closed because both governance gates remain unsatisfied:

1. no valid GOV02/PREP02R admission route is open;
2. genuinely independent second-line review is still missing.

Final workunit disposition:

`TECHNICAL_REVIEW_PASS_BUT_INDEPENDENT_SECOND_LINE_AND_ROUTE_GATES_NOT_SATISFIED_TCD026_NOT_ADMITTED`
