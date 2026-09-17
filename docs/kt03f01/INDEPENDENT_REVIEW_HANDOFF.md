# ANIMO-KT03F01 Independent Second-Line Review Handoff

Status: `READY_FOR_GENUINELY_INDEPENDENT_TIER_C_REVIEW`.

This file is a handoff package only. It does not perform, simulate or approve the independent review.

## Governing requirement

ANIMO-GOV04 classifies missing/redefined physical state, initialization semantics and scientific state/source ownership ambiguity as Tier C. Tier C requires one genuinely independent second-line review. The same authoring context may not approve that gate.

GOV06 additionally requires same-agent review to remain labelled `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

KT03F01 therefore remains unqualified until a reviewer outside the authoring context records a result against the exact pinned candidate.

## Immutable review target

Review target:

`ANIMO-KT03F01@36024e5b8cd62203b03b9b72c0d08e4c797612bb`

Candidate disposition:

`HLPIMP1_INTERCEPTION_STORAGE_NOT_PART_OF_PRODUCER_EXCHANGE_STATE_CONTRACT`

Bounded scope:

`Iopthyvs=1 AND Hlpimp=1`

The reviewer must not broaden the result to Hlpimp=2, Hlpimp=11, production migration, whole-model equivalence, B2 historical behaviour or B3/B4 admission.

Suggested independent review branch:

`review/animo-kt03f01-hlpimp1-independent-second-line`

A separate branch is recommended for traceability. Independence is established by a genuinely separate review context, not by branch naming alone.

## Authorities to pin

- GOV04: `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`
- GOV06: current unified programme governance as consumed by KT03F01
- KT03 closeout: `ANIMO-KT03@c5d4c14fbd4ce77ed5ef369bb8ecaee0709ea3b8`
- frozen KT03 payload/contract implementation: `e844c7658a95819fc0463c55737f9bd41b29a6da`
- KT03F01 authoring evidence head: `9e31afe36ca1bc8f4c90dab024c811c87337cbc0`
- KT03F01 same-agent review/old closeout history: `0bd8e3f2fe84837e85c45c44ec2e8201f81cef12`
- governance-corrected review target: `36024e5b8cd62203b03b9b72c0d08e4c797612bb`

The old same-agent PASS at `0bd8e3...` is evidence input only. It is not an independent decision.

## Evidence package

The reviewer should read at minimum:

- `docs/kt03f01/SOURCE_AND_INTERFACE_EVIDENCE.md`
- `docs/kt03f01/ADVERSARIAL_REVIEW.md`
- `reference/kt03f01/HLPIMP_INTERCEPTION_BALANCE_PROBE.json`
- `tools/kt03f01/interception_balance_probe.py`
- `tests/kt03f01/test_interception_balance_probe.py`
- `integration/animo-kt03f01/ANIMO-KT03F01_CHECKPOINT.json`
- KT03 `TYPED_HYDROLOGY_STEP_CONTRACT.md`
- GOV04 risk-tiered review policy and Tier C matrix.

Relevant source evidence is already pinned in the workunit. The review may verify source neighbourhoods independently, but evidence reuse is permitted only under GOV04 `VERIFY_AND_REUSE`: pins, scope compatibility and absence of superseding evidence must be checked.

## Scientific claim to challenge

The candidate says that legacy Hlpimp=1 producer exchange does not contain an interception-storage state. Consequently corrected adapter semantics would not fabricate `Sic/Sict` and would omit the absent `Sict-Sic` contribution from the affected Hlpimp=1 transformation identities.

The independent reviewer must challenge, not merely restate, that claim.

At minimum answer all of the following:

1. Does any pinned source, producer record, initialization path, documentation or lifecycle establish a hidden or implicit Hlpimp=1 interception-storage state?
2. Is the observed whole-profile closure without `Sict-Sic` causally probative, or could another omitted/misinterpreted term create the same apparent closure?
3. Is the Hlpimp=11 contrast a valid control for the state-ownership distinction?
4. Does omission of `Sict-Sic` preserve the scientific meaning of the revision-53 top-boundary transformation, rather than merely improving an accounting residual?
5. Do the recovered project/build artifacts materially support or contradict the candidate? Do not promote them to B2.
6. Is the causal chain `Dif -> Evso -> Flab(1) -> Modflux` correctly understood, including clamp/boundary cases?
7. Is Hlpimp=1 sufficiently separated from Hlpimp=2 and Hlpimp=11 that the disposition can remain atomic?
8. Are there edge cases in which an absent interception state still requires a carry-forward, reset or other explicit state transition?
9. Is any source/testcase identity changed or superseded relative to the pinned evidence?
10. Does the evidence support PASS, FAIL, or INCOMPLETE under the exact Tier C scope?

## Required reviewer outputs

The independent review must record:

- reviewer context is genuinely separate from the authoring context;
- exact reviewed head;
- exact evidence/authority pins;
- whether evidence was independently replayed or verified/reused;
- findings classified by severity;
- any failed gate classified as scientific falsification, evidence insufficiency, provenance insufficiency, tooling failure or scope ambiguity;
- a single final result: `PASS`, `FAIL`, or `INCOMPLETE`;
- residual uncertainty and explicit nonclaims.

A PASS may authorize a later formal KT03F01 disposition workunit. It does not itself modify production source, admit B3/B4, close KT04 or authorize SWAP5 coupling.

A FAIL or INCOMPLETE is a valid review result and must remain fail-closed.

## Acceptance gate for KT03F01

KT03F01 may proceed beyond REVIEW only when the independent result:

1. targets exactly `36024e5b8cd62203b03b9b72c0d08e4c797612bb` or a later authoring head whose scientific claim is demonstrably unchanged;
2. satisfies GOV04 Tier C independence;
3. pins the evidence identities it reused;
4. contains no unresolved material finding for a PASS;
5. does not widen the claim.

Until then, KT04 Hlpimp=1 execution remains blocked.
