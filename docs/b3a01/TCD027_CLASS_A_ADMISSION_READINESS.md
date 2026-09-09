# TCD-027 Class A Admission Readiness

Work unit: `ANIMO-B3A01`

Target discrepancy: `TCD-027`

Current result: `READINESS_QUALIFIED_ADMISSION_BLOCKED_BY_B2_ROUTE`

## 1. What is being qualified

TCD-027 concerns a detailed organic-P reporting accumulator in `Outbal_calc.for`.

Legacy expression:

`Bafop(24,Ly)=Bafop(25,Ly)+Dum`

Candidate corrected-legacy expression used only in the earlier diagnostic probe:

`Bafop(24,Ly)=Bafop(24,Ly)+Dum`

The claim under qualification is narrow: slot 24 must accumulate from its own prior slot value. This is not a claim about organic-P process physics, total balance algebra, sorption, redistribution physics, numerical policy, or ANIMO5 state representation.

## 2. Why this is provisionally Class A

ANIMO-B3Q01 defines Class A for accounting or reporting-only corrections where physical state and process flux trajectories are already represented and the defect is confined to a ledger, accumulator, reporting balance, or balance interface.

PREP06 evidence matches that pattern:

- source defect is a detailed reporting accumulator update;
- natural activation exists in `LWKM_gras_1040.2021.2045`, period 1997;
- `redis_EXP` changes from `-7.0644 kg/ha P` to `0.0 kg/ha P` in the probe;
- only three detailed transfer output files change;
- total organic-P balance outputs do not change;
- ordinary state/process outputs do not change;
- state trajectory does not change;
- total mass balance does not change.

Class A remains conditional. If later unrounded reference capture shows a physical state or process flux change caused by the candidate correction, this classification is invalid and admission must fail or be reclassified.

## 3. B0 identity

The readiness package is bound to:

- source archive SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- supplied documentation SHA-256 `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`.

The documentation is ANIMO 4.0 material and does not by itself specify the exact revision-53 accumulator slot algebra. The strongest basis here is therefore the source-bound accumulator identity, cross-species/analogue accumulator structure, and non-interference evidence, not a claim that the guide explicitly documents slot 24.

## 4. B1 evidence and limitation

Primary B1 evidence:

`integration/animo-prep/PREP06_ORGANIC_P_DETAILED_ACCUMULATOR_DEFECT.json`

The diagnostic GNU environment is reproducible but remains `DIAGNOSTIC_NOT_REFERENCE`.

B1 establishes:

- exact source expression;
- causal effect of the one-expression probe;
- natural activation under one supplied case;
- observed reporting-only difference surface within that diagnostic scope.

B1 does not establish actual historical executable behaviour and therefore cannot independently support `PRESERVE_HISTORICAL_BEHAVIOUR` or `ADMIT_CORRECTED_LEGACY_BEHAVIOUR`.

## 5. B2 status

PREP02R currently reports:

`BLOCKED_HISTORICAL_REFERENCE_ARTIFACT_NOT_YET_OBTAINED`.

No independently trusted revision-53 executable, qualified 4.1.x historical executable, executable-linked historical output, or original build metadata has yet been obtained.

The prepared WUR archival request is ready but has not been sent. This matters for both routes:

### Normal route

Cannot pass. B2 is not available.

### Historical uncertainty route

Cannot yet pass. ANIMO-B3Q01 requires a documented reasonable historical-reference acquisition effort that has actually failed. A prepared but unsent request is not a completed acquisition effort and cannot be treated as such.

Therefore this workunit deliberately does not instantiate a schema-valid admitted B3 disposition record.

## 6. Accounting identity

The local reporting identity is an accumulator self-update identity:

`new_slot24 = old_slot24 + current_slot24_increment`

Using slot 25 as the prior value cross-seeds one reporting channel from a different reporting channel. The analogous detailed organic-matter and organic-N accumulator updates cited in PREP06 both accumulate their own slot-24 histories, supporting the interpretation that the P statement is a reporting accumulator defect rather than a process transfer.

This identity is local to detailed reporting. It does not justify any broader organic-P correction.

## 7. Expected difference contract

Expected changed surfaces for the candidate correction:

- `transfopGP.Out`;
- `transfopRP.Out`;
- `transfopTP.Out`;
- specifically the detailed `redis_EXP` reporting quantity associated with the defective accumulator.

Expected unchanged surfaces:

- physical organic-P state trajectory;
- process flux trajectory;
- total organic-P balances;
- total mass balance;
- `redis_OP`;
- `redis_DOP`;
- `redis_HUP`;
- ordinary non-reporting model outputs.

Any future admission test that observes a change outside the declared reporting surface must fail closed until explained and reclassified.

## 8. Coverage

Natural diagnostic activation is present in the supplied LWKM case for 1997. This is stronger than synthetic-only branch activation for causal coverage.

However, natural B1 activation is still not B2 historical evidence. Once B2 is available, the same relevant path must be shown to execute under the historical reference or the historical relevance of the difference must remain explicitly uncertain.

## 9. Conservation and non-interference

The candidate correction is not intended to change conservation of physical P because the defect is in a detailed reporting accumulator only.

The existing diagnostic probe reports:

- total organic-P balance unchanged;
- total mass balance unchanged;
- state trajectory unchanged;
- ordinary process outputs unchanged.

This is necessary Class A evidence, but eventual admission should preserve an independent observation surface for state and flux equivalence. A future correction implementation must not prove non-interference only by reading back the same reporting accumulator it changes.

## 10. Independent review gate

No corrected-legacy admission is made here.

Before `admitted=true`, a second-line review must verify at least:

- source expression and slot semantics;
- absence of hidden state or flux mutation through the reporting code path;
- changed-output whitelist;
- unchanged total-balance and state/flux surfaces;
- B2 result or legitimate historical-uncertainty route;
- residual uncertainty statement.

## 11. Current disposition

Current provisional disposition:

`UNRESOLVED_NOT_ADMITTED`

Reason: the scientific/accounting case is strong enough for Class A readiness, but neither legal admission route is currently complete.

This is not a negative judgment on the candidate correction. It is a deliberate separation between a well-supported causal correction candidate and a B3 admission decision.

## 12. What can happen next

The most direct route is:

1. complete the PREP02R historical-reference acquisition action;
2. if B2 is obtained, run the natural LWKM path and capture the relevant detailed P reporting plus unrounded independent state/flux surfaces;
3. populate a B3 disposition record against `B3_DISPOSITION_SCHEMA.json`;
4. obtain independent review;
5. admit or reject TCD-027 atomically;
6. only after that consider composition with any other Class A or organic-P correction.

Until those gates pass, production migration remains `NOT_ADMITTED`.
