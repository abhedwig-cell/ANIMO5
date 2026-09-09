# TCD-026 independent second-line review packet

Request: `ANIMO-B3A04-TCD026-SECOND-LINE-REVIEW`

This is a handoff, not a completed review. ANIMO-B3A04 authoring, execution and evidence production do not count as independent second-line review.

## 1. Review target

Review exactly one Class-A claim:

`Ex(Ln)` is existing root-exudate organic-matter state. Revision 53 includes result state `Rsex(Ln)` in final fresh-OM storage but omits `Ex(Ln)` from beginning `Bfom` storage. The only candidate correction is:

```fortran
Bfom(Inip_x,Ly) = Bfom(Inip_x,Ly) + Ex(Ln) * P
```

Do not compose any other organic-matter discrepancy.

## 2. Pinned basis

- canonical base `work/animo-b3i01-canonical-register-append@383c7a83e84a578969f92113280dc715b7bdddb4`
- B0 source SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- B0 testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- PREP06 `work/animo-prep06-conserved-state-ledger@9b1f1ea51c24fb82823290193651830dc61ea3c8`
- PREP06 defect blob `bbb7cd88c2beaa758e786e14e234a975b361b387`
- PREP06 machine evidence blob `0e60d8aaf526c0b0127da1143b68c9c8235e9fe3`
- PREP06 state inventory blob `838f224fc67a72371437c6d5b6e75cd03f5c8d51`
- B3Q01 `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`
- GOV02 `db7add6f9561730bbf352aa7fd3f3968405cfaa3`
- SYNQ01 `842f72300fd03ede0b9024537a7ee6126722a121`
- STATEQ02 `cb7c23524df6560e65a5bdc1ed19e0b6e3bd46c6`
- latest PREP02R observed before final closeout `a2fda49871ee3c7104daf7e06cd8dffdac06b125`

B3A04 evidence files:

- `integration/animo-b3/TCD026_EXPECTED_DIFFERENCE.json`
- `integration/animo-b3/TCD026_CLASS_A_READINESS.json`
- `integration/animo-b3/TCD026_MODEL_PRODUCED_STATE_REPLAY.json`
- `integration/animo-b3/TCD026_CHRONOLOGICAL_RESTART_PROBE.json`
- `integration/animo-b3/TCD026_CHRONOLOGICAL_RESTART_PROBE_PLAN.json`

Recheck live authorities before recording a final review outcome.

## 3. Core source and conservation checks

Record PASS, FAIL or INCOMPLETE for each:

| Gate | Required check |
| --- | --- |
| B0 identity | Frozen source/testbank hashes match. |
| canonical scope | TCD-026 remains the initial Ex/fresh-OM ledger omission only. |
| atomicity | Candidate is exactly one beginning `Bfom` observation. |
| physical owner | `Ex` is accepted/start state, `Rsex` result state, `Init` promotes `Ex=Rsex`, restart persists `Rsex`. |
| final ledger | Current final `Bfom` includes `Rsex(Ln)*Z`. |
| beginning ledger | Current initial `Bfom` omits `Ex(Ln)*P`. |
| N/P control | Bano/Bapo already observe initial Ex through Nifrex/Pofrex and must remain unchanged. |
| conservation | Beginning and ending C-EX storage represent the same persistent store across the accepted boundary. |

## 4. PREP06 causal discriminator

Independent reviewer should verify:

- controlled `Ex(1)=1e-3 kg/m2` equals `10 kg/ha`;
- frozen legacy first fresh-OM residual is exactly `-10 kg/ha`;
- adding only `Ex(Ln)*P` removes that deterministic residual to recorded floating-scale values;
- those small residuals are not a tolerance;
- PREP06 72-output comparison changes only the six recorded fresh-OM balance files.

## 5. Model-produced state replay

Review the earlier CranMais replay separately from the chronological probe.

Expected evidence:

- producer `INITIAL.OUT` SHA-256 `254fa48dfd1349f6b0d2079b6dc0ca8ec16c35ea80bcd5b8eb464bd60b770a86`;
- model-produced Ex total `5989.6594 kg/ha`, layers 1 through 9 nonzero;
- legacy replay first fresh-OM deviation approximately `-5.99E+03 kg/ha`;
- candidate beginning FOM increment `5989.66 kg/ha`;
- candidate deviation `-7.28e-12 kg/ha`;
- legacy/candidate resulting `Output/initial.out` byte-identical;
- after known volatile normalization only `ani_omMP.Bal`, `ani_omTP.Bal`, `baomMP.Out`, `baomTP.Out` change.

Required scope classification:

`MODEL_PRODUCED_RESTART_FORMAT_STATE_REPLAY_NOT_CHRONOLOGICAL_SPLIT_RUN`

If it is presented as chronological split-run or B2, review must fail that claim.

## 6. Chronological 1974 to 1975 probe

This is the strongest naturalistic TCD-026 activation in B3A04 and must be reviewed carefully.

### Segment A

- case `CranMais`
- period `1974-01-01` through `1974-12-31`
- frozen testbank archive unchanged
- execution-copy management bounded to the first 1974 management period
- successful completion
- generated `INITIAL.OUT` SHA-256 `6578e35e7b5bd39927569ff4f004afbe164d2ce20c98a6d75dc75b7ab536764b`
- model-produced Ex total `642.718929 kg/ha`, layers 1 through 9 nonzero

### Segment B

- period `1975-01-01` through `1975-12-31`
- `INITIAL.INP` byte-identical to Segment-A `INITIAL.OUT`
- hydrology payload unchanged from prepared frozen case
- material payload unchanged from prepared frozen case
- management execution-copy retains original 1975 maize/addition chronology
- original 1975 additions are rebased from absolute-simulation days 469, 479, 482 to local days 104, 114, 117 after removing completed 365-day Segment A
- frozen testbank archive unchanged

The reviewer must verify that this is a bounded execution-copy chronology transformation, not a physical or scientific-input modification to the frozen archive.

### Ledger discriminator

Expected printed values:

- legacy beginning fresh OM `12209.622 kg/ha`
- candidate beginning fresh OM `12852.341 kg/ha`
- increment `642.719 kg/ha`
- model-produced Ex `642.718929 kg/ha`

The increment must be interpreted as the same mass subject only to legacy report formatting, not a fitted tolerance.

Expected first-period deviation:

- legacy detailed balance approximately `-642.7 kg/ha`
- legacy scientific report approximately `-643 kg/ha`
- candidate `1.82e-12 kg/ha`

### Candidate non-interference

Legacy and candidate final `INITIAL.OUT` SHA-256 must both be:

`e6c240ae46edfb7d0a4577dfb70106fb10e37b78982f93d2a116130f9685ca42`

Twenty-three scientific/model outputs were compared after only known timestamp/CPU normalization:

- 19 identical;
- exactly four changed;
- zero unexpected changes.

Allowed changed surfaces in this probe:

- `ani_omMP.Bal`
- `ani_omTP.Bal`
- `baomMP.Out`
- `baomTP.Out`

Any candidate-caused state/process/N/P/water/unrelated-OM difference fails Class A.

## 7. Formatted restart negative result

The same chronological campaign compared continuous 1974 to 1975 execution against the legacy formatted restart path.

Expected result:

- final formatted restart state not byte-identical;
- 564 printed numeric tokens compared;
- 32 differ;
- maximum absolute printed difference `1.0e-6`.

This is deliberately retained as a negative control and scope boundary.

Do not:

- call legacy formatted restart exact;
- introduce a tolerance to force equality;
- infer the precise cause without separate evidence.

Permitted interpretation is only that the formatted path is not an exact whole-model checkpoint in this probe. The small drift may be consistent with formatted serialization and/or other legacy restart-surface limitations, but B3A04 did not isolate it.

## 8. STATEQ02 cross-stream evidence

STATEQ02 independently qualified restricted-core exact checkpoint semantics at splits 66, 67, 68, 71 and 72 with exact bitwise comparisons and no tolerance. Split 67 reproduced all 833 remaining accepted records exactly.

Its persistent-state matrix classifies `ORG-004 root exudate organic mass` as a core C/N/P accepted owner, mandatory for checkpointing and exact restore.

Allowed use in this review:

`independent support for C-EX physical ownership and continuation relevance`.

Disallowed use:

- TCD-026 beginning-ledger oracle;
- B2 historical reference;
- substitute for review independence;
- proof that legacy formatted `INITIAL.OUT/IN` is exact.

STATEQ02's qualification-only exact checkpoint and B3A04's legacy formatted restart probe are different restart mechanisms and are not contradictory.

## 9. Natural activation classification

The final classification must preserve all three layers:

1. supplied ordinary model starts: `STRUCTURALLY_UNREACHABLE_ZERO_INITIAL_EX`;
2. PREP06 synthetic causal activation: PASS;
3. model-produced chronological formatted restart activation: PASS for the TCD-026 ledger path only.

Do not promote item 3 to whole-model split-run identity.

## 10. SYNQ01 boundary

Current SYNQ01 does not register a TCD-026 oracle. Do not substitute `SYNQ-O003`, which is an interception-water control-volume oracle.

No B3A04-authored experiment is an independent SYNQ01 oracle.

## 11. Route boundary

At the latest B3A04 check PREP02R still had:

- `normal_B2_reference_available=false`
- `historical_uncertainty_route_eligible=false`
- `reference_qualified=false`

A scientific second-line PASS therefore cannot itself admit corrected legacy behaviour. Route eligibility must be rechecked live.

## 12. Independence and final outcome

The reviewer must record:

- reviewer/workunit identity;
- exact B3A04 head reviewed;
- authority heads rechecked;
- PASS/FAIL/INCOMPLETE for every required gate;
- whether the chronological probe was independently reproduced or evidence-reviewed only;
- any contradiction or unresolved provenance concern;
- live route state;
- exactly one outcome:
  - `PASS_INDEPENDENT_REVIEW`
  - `FAIL_INDEPENDENT_REVIEW`
  - `INCOMPLETE_REVIEW`

A review PASS satisfies only the second-line prerequisite. It must not set `admitted=true`, create a production correction or compose another TCD.
