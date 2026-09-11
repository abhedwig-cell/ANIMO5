# ANIMO-GOV05 Single-Agent Adversarial Scientific Review Policy

Work unit: `ANIMO-GOV05`

Branch: `work/animo-gov05-single-agent-adversarial-review`

Policy state: prospective governance change. This work unit does not admit a TCD, modify production source, modify frozen B0, or modify the canonical TCD register.

## 1. Purpose and assurance change

GOV05 replaces the prospective GOV04 requirement `MANDATORY_SEPARATE_CONTEXT_INDEPENDENT_REVIEW` for Tier B, Tier C, and eligible Tier D work with `MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW`.

The new review mode is:

`SINGLE_AGENT_ADVERSARIAL_REVIEW`

Its mandatory assurance label is:

`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`

A same-agent review is never genuinely independent. It must not be described as an independent second-line review, organizationally independent review, or human independent review. The assurance change is deliberate: same-agent review has lower independence assurance than the GOV04 separate-context process. GOV05 does not claim equivalence of independence assurance.

The scientific evidence gates themselves are not reduced. GOV05 changes who performs the second pass and how the review boundary is enforced. It does not relax source, causal, conservation, state, restart, numerical, coverage, expected-difference, non-interference, historical-evidence, or production gates.

GOV04 remains historically valid for work completed under it. Existing genuinely separate reviews retain their recorded status and wording.

## 2. Authorities and compatibility

GOV05 is layered over, and does not rewrite, these pinned authorities:

- `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`
- `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`
- `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`
- current aggregate at authoring start: `ANIMO-RG05H@3e4247928bb43f30def951fa8804560636affbef`
- latest qualified atomic descendant observed at authoring start: `ANIMO-B3D21@331f6ed91d4a1c15a23ae0c1ad75d1b540f61858`

B3Q01's historical machine schema contains a field named `independent_review`. GOV05 does not rename or rewrite that finalized schema because doing so would create avoidable historical churn. For a future GOV05 same-agent workunit, that field is a compatibility slot only. It must record `independent_from_correction_authoring=false`; a PASS in that slot may only represent satisfaction of the GOV05 review-process gate when a pinned GOV05 internal-adversarial-review artifact is also present. The field name itself must never be used as evidence that the review was independent.

Workunit-specific GOV04 validators that require a separate context remain valid for the historical workunit they validated. They are not retroactively weakened or rewritten. New GOV05 workunits must use the GOV05 assurance contract.

## 3. Mandatory review boundary

Before a same agent may start the review phase, all of the following are mandatory and ordered:

1. Persist the complete authoring and evidence package.
2. Freeze an immutable authoring Git head.
3. Record source, testbank, and evidence identities or cryptographic hashes.
4. Complete the authoring phase. No substantive authoring continues after the boundary.
5. Review the exact frozen authoring head, never a moving branch or working tree.

The review record must pin the reviewed authoring SHA. If remediation changes any substantive claim, evidence, policy, source interpretation, expected-difference contract, state interpretation, or scientific conclusion, the changed package becomes a new immutable authoring checkpoint and the full applicable adversarial review restarts against that new head.

Purely administrative closeout metadata may be added after a passing review, but the validator must prove that substantive reviewed files did not change after the reviewed checkpoint.

## 4. Mandatory adversarial second pass

The second pass must reconstruct rather than restate. For every applicable scientific claim it must:

- reconstruct the claim from pinned source and evidence without inheriting the authoring conclusion as a premise;
- actively search for counterexamples and contradictory or superseding evidence;
- formulate and test the strongest plausible alternative interpretation;
- verify scientific ownership, variable identity, units, sign, lifecycle, first read and first write, or restore direction as applicable;
- verify expected-difference and non-interference contracts;
- inspect active controls and negative controls;
- inspect the regression surface and the scope guard;
- verify conservation or accounting identities where applicable;
- verify state, initialization, restart, checkpoint, numerical, solver, tolerance, and failure semantics whenever the risk tier makes them applicable;
- classify residual uncertainty explicitly;
- fail closed on contradictory, unpinned, incomplete, or insufficient evidence.

A review report that merely paraphrases the authoring report is invalid.

## 5. Evidence reuse

GOV04 `VERIFY_AND_REUSE` remains in force. Immutable PASS evidence may be reused only after the second pass verifies:

- exact pin identity;
- scope compatibility with the current claim;
- immutable provenance of the reused artifact;
- absence of superseding or contradictory evidence;
- no evidence-strength promotion.

Mechanically immutable evidence need not be rerun merely to create ceremony. Reuse does not waive interpretation, scope, contradiction, or risk-tier checks.

## 6. Risk tiers

### Tier A

The GOV04 Tier-A waiver is retained without weakening. No separate review phase is required only when every GOV04 Tier-A waiver predicate passes. `STRICTEST_APPLICABLE_RISK_TRIGGER_WINS` remains controlling. Failure of any waiver predicate escalates to the applicable higher tier.

### Tier B

Tier B requires `ONE_MANDATORY_INTERNAL_ADVERSARIAL_REVIEW` after the immutable authoring checkpoint. The same agent may proceed to disposition or admission in the same workunit after a PASS, provided all other B3Q01, GOV03, routing, evidence, and scope gates pass.

The review assurance is `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`. No user-created review chat is required.

### Tier C

Tier C requires `ENHANCED_INTERNAL_ADVERSARIAL_REVIEW` with assurance `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT`.

In addition to all ordinary applicable scientific gates, Tier C requires:

- an immutable authoring checkpoint;
- complete source and persistent-state ownership reconstruction;
- first-read/first-write analysis or restore-direction analysis as applicable;
- a documented counter-hypothesis test;
- active controls and negative controls;
- split-run or restart evidence where restart, persistence, or checkpoint semantics are in scope;
- an explicitly justified exact-comparison policy;
- no invented tolerance;
- a regression guard and declared regression surface;
- exact-final-head CI after closeout.

A Tier-C same-agent PASS is not organizational, human, process, or genuinely independent assurance. It is a lower-independence process with strengthened internal adversarial gates.

### Tier D, B4, and production

The same agent may execute the required stages sequentially so the user need not create separate review chats. The decision surfaces remain separate and individually persisted:

1. composition qualification;
2. integration qualification;
3. B4 decision;
4. production authorization.

Each surface requires its own immutable checkpoint and applicable adversarial review. A PASS at one surface does not imply a PASS at a later surface. Production authorization may not be collapsed into ordinary authoring, composition qualification, integration qualification, or B4 decision.

GOV05 itself does not open B4 or production.

## 7. Failure and remediation policy

`SELF_REVIEW_PASS` requires every applicable scientific and governance gate to PASS.

Incomplete or contradictory evidence produces `FAIL_CLOSED`. The agent must not request a new review chat merely to try again. If the missing evidence can be repaired mechanically within the allowed workunit scope, persist the repair as a new immutable authoring head and rerun the applicable adversarial review against that head.

If the scientific claim changes materially, the entire review phase restarts. A previous PASS on the old claim cannot be carried forward as the review conclusion for the new claim.

## 8. Historical uncertainty and GOV03

GOV05 does not change the GOV03 historical-evidence boundary. If no qualified B2 exists for the claim scope, historical revision-53 behaviour remains `UNKNOWN` or `UNKNOWN_WITHOUT_B2` as required by the consuming schema. Current-GNU diagnostics, synthetic activation, source reasoning, or same-agent review must not be promoted to B2.

Discovery of credible new historical evidence reopens B2 qualification for the relevant scope exactly as GOV03 requires.

## 9. User-zero-intervention workflow

The normal prospective workflow is:

`AUTHOR -> PERSIST_IMMUTABLE_CHECKPOINT -> INTERNAL_ADVERSARIAL_REVIEW -> REMEDIATE_IF_NEEDED -> EXACT_HEAD_CI -> DISPOSITION_OR_ADMISSION_WHEN_ELIGIBLE`

The workunit should autonomously continue through every phase it is authorized to perform. The user is not required to create a separate review chat, paste a review prompt, or manually report that a review completed.

A scientific blocker still terminates fail closed. User-zero-intervention is not permission to invent evidence, exceed the workunit's scope, or bypass an authorization boundary.

## 10. Transitional rules

- GOV04 remains historically valid.
- Completed GOV04 independent reviews keep their original status and assurance label.
- Existing admissions remain valid and are not reopened merely to adopt GOV05 style.
- Existing FAIL or INCOMPLETE review records remain historical facts and are never rewritten into PASS.
- An open review handoff may be marked `NOT_REQUIRED_UNDER_GOV05` only after live confirmation that its underlying work is still open, has an immutable qualifying authoring package, and is eligible for the GOV05 route.
- A review already completed independently is closed as completed history, not converted to a GOV05 self-review.
- A review already in flight should normally finish under the governance contract under which it started. If it remains incomplete after GOV05 qualification, transition requires a fresh live check and a new immutable GOV05 authoring checkpoint. The old incomplete review remains intact.
- Finalized scientific work is not reopened solely to replace its review style.

The machine-readable transition snapshot is `integration/animo-governance/GOV05_OPEN_REVIEW_TRANSITION.json`.

## 11. Terminology

Allowed same-agent labels include:

- `INTERNAL_ADVERSARIAL_REVIEW`
- `SAME_AGENT_SECOND_PASS`
- `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`

For same-agent review records, the following claims are prohibited:

- `genuinely independent`
- `independent second-line`
- `organizationally independent`
- `human independent`

Historical artifacts that truthfully describe earlier separate-context reviews are not rewritten by this prohibition.

## 12. GOV05 qualification boundary

GOV05 can reach:

`QUALIFIED_SINGLE_AGENT_ADVERSARIAL_REVIEW_GOVERNANCE_WITH_EXPLICITLY_REDUCED_INDEPENDENCE_ASSURANCE_NO_SCIENTIFIC_GATE_REDUCTION`

only after its own authoring package has been frozen, a same-agent adversarial second pass has reviewed that exact immutable head, all mandatory validator checks pass, and CI succeeds on the exact final head.

That decision is a governance qualification only. It is not a TCD admission, B4 decision, production authorization, scientific correction, or historical-fidelity claim.
