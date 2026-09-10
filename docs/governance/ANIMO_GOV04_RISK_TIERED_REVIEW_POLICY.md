# ANIMO-GOV04 Risk-Tiered Scientific Review and Admission Governance

Work unit: `ANIMO-GOV04`

Branch: `work/animo-gov04-risk-tiered-review-policy`

Authoring base: `ANIMO-RG05D@f3d6b9780631bd627f8bca0658a8e3878746e666`

Current central regie at closeout: `ANIMO-RG05E@eed822037ed8d906a2ab424220597cffac9cca73`

B3 framework authority: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`

Historical uncertainty route authority: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`

Scope: governance only. GOV04 admits no TCD, opens no B4 work, changes no production source and does not rewrite any historical review, admission or RG05 snapshot.

## Concurrent central-regie advance

GOV04 was branched from the then-current RG05D authority. During authoring, `ANIMO-RG05E@eed822037ed8d906a2ab424220597cffac9cca73` qualified the fifth atomic B3 admission integration for TCD-015. GOV04 therefore retains RG05D as immutable authoring base but treats RG05E as the current central-regie authority at closeout. No rebase or historical rewrite is required because GOV04 changes only five governance files and validates RG05E as an external pinned authority.

RG05E records five atomic scientific admissions, `TCD-017`, `TCD-018`, `TCD-024`, `TCD-026` and `TCD-015`. B3 remains incomplete, B4 remains closed and production migration remains closed.

## Decision principle

GOV04 introduces:

`RISK_TIERED_REVIEW_INTENSITY`

The purpose is not to reduce scientific gates. The purpose is to allocate review effort according to scientific and implementation risk, reuse immutable evidence safely, automate mechanical checks and escalate ambiguous work before admission.

Five activities remain conceptually distinct:

1. evidence qualification;
2. technical review;
3. genuinely independent second-line review;
4. admission decision;
5. central project-regie integration.

They do not always require five separate workunits. Separation is mandatory only where the risk tier or another governance rule requires it.

Risk tier is independent of B3 qualification class. Qualification class describes the kind of discrepancy. Risk tier determines review intensity. The strictest applicable risk trigger wins.

## Tier A: low-risk accounting and reporting only

Default candidate class: `A_ACCOUNTING_REPORTING_ONLY`.

A separate independent second-line review may be omitted only if every Tier A waiver condition is explicitly PASS:

- exact source seam is pinned;
- physical and accounting ownership are unambiguous;
- the claim is atomic;
- an exact conservation or accounting identity is stated and satisfied;
- the expected-difference contract is pinned before qualification;
- physical state non-interference is demonstrated;
- process flux non-interference is demonstrated;
- no numerical-policy change occurs;
- no solver or tolerance change occurs;
- no restart, initialization or state semantic change occurs;
- no composition is present;
- no unresolved scientific or source-meaning ambiguity remains;
- a reproducible validator exists and passes;
- a scope guard exists and passes;
- natural activation is used where reasonably available, or absence of natural coverage is documented and a purpose-built synthetic activation is independently qualified for causality and scope;
- when no qualified B2 exists, historical behaviour remains exactly `UNKNOWN`;
- GOV03 route conditions remain satisfied where the historical-uncertainty route is used;
- no production source, canonical TCD register, B4 object or finalized governance snapshot is modified.

If any condition is false or unknown, the independent-review waiver is unavailable. The claim is escalated to the tier implied by the unresolved risk. State ownership ambiguity, restart semantics, numerical policy and solver behaviour force Tier C. Composition or production-bound scope forces Tier D.

When all Tier A conditions PASS, technical review plus automated qualification may satisfy review governance. Evidence qualification, technical review, disposition and admission closeout may be combined in one bounded workunit. The record must still show each scientific gate separately. Combining ceremonies never combines or removes scientific gates.

### B3Q01 schema compatibility for Tier A

GOV04 does not edit the finalized B3Q01 schema. For a Tier A waiver under the existing `B3_DISPOSITION_SCHEMA.json`, the independent-review evidence block records that the review requirement was evaluated and waived by GOV04. It must use `result: NOT_REVIEWED` and must not claim independence. The corresponding gate is `status: PASS` with `applicability: NOT_APPLICABLE`, with an explicit GOV04 Tier A waiver reference. This is a governance applicability decision, not a claim that an independent review occurred.

Any downstream validator that sees `NOT_REVIEWED` on an admitted Class A record must fail unless the full GOV04 Tier A waiver predicate is machine-verified.

## Tier B: local algebra, index or species correction

Default class: `B_LOCAL_ALGEBRA_INDEX_SPECIES`.

Tier B requires one genuinely independent second-line review. After a qualified PASS, no second independent review and no second disposition ceremony are required when the route, claim, pins and all gates remain unchanged. A single post-review workunit may combine formal disposition and admission closeout.

If a Tier B review fails because evidence or provenance is incomplete, remediation repairs only the failed evidence gates. A targeted re-review may verify those repaired gates plus regression guards if all prior PASS gates are immutable and their source, testcase and evidence identities still match.

Any change to the scientific claim, source meaning, numerical policy, state semantics or scope invalidates this shortcut and causes escalation or full review.

## Tier C: high-risk state, restart, runtime or numerical semantics

Tier C includes, regardless of a legacy class label:

- restart or cold-start discrimination;
- initialization semantics;
- canonical state ownership;
- checkpoint semantics;
- missing or redefined physical state;
- numerical policy;
- solver or tolerance changes;
- runtime branching that can alter model behaviour;
- exact-zero or singular-domain semantics;
- ambiguous domain contracts;
- state or source ownership ambiguity with scientific consequences.

Tier C retains genuinely independent second-line review and full fail-closed treatment. Separate disposition and admission workunits are preferred when they improve traceability, especially for state, restart and numerical-policy decisions.

Targeted re-review after remediation is allowed only when the failed gates are isolatable and every reused PASS gate is immutable, provenance-pinned, scope-compatible and not superseded. Otherwise a full review is required. A reviewer may always choose full review when interaction risk cannot be excluded.

## Tier D: composition, multi-TCD and production-bound changes

Tier D is the highest review tier. It includes:

- composition of multiple admitted TCDs;
- cross-module coupling;
- production source migration;
- B4 qualification or authorization;
- whole-model baseline claims;
- any production-bound change that depends on more than one admitted scientific object.

Tier D requires independent review, separate composition qualification where applicable, integration qualification and explicit production authorization. Atomic admission never promotes automatically to composition, B4 or production.

B3 Class D representation-only modernization is not automatically risk Tier D. It defaults to risk Tier C when ownership, process order, restart, state layout, runtime or numerical semantics are touched. It may be risk Tier B only when equivalence to an already admitted target is fully pinned and none of those higher-risk triggers applies.

## Evidence reuse: VERIFY_AND_REUSE

The default downstream policy is:

`VERIFY_AND_REUSE`

not:

`REPERFORM_EVERYTHING`

A prior PASS evidence item may be reused only when all conditions hold:

- exact same source and testcase identity applies;
- claim scope has not widened or changed;
- the evidence artifact is byte-identical or otherwise immutable by a pinned identity;
- provenance is fully pinned;
- no superseding or contradictory evidence exists.

The downstream reviewer or validator must still verify the pin, verify scope compatibility and verify that no superseding evidence exists. Reuse preserves the original evidence strength. It cannot promote B1 to B2, synthetic evidence to historical reference evidence, or process independence to organizational or human independence.

## Review failure and remediation

GOV04 establishes:

`REVIEW_FAIL != AUTOMATIC_FULL_REVIEW_RESET`

Every failed or incomplete review must classify its cause as one or more of:

- `SCIENTIFIC_FALSIFICATION`;
- `EVIDENCE_INSUFFICIENCY`;
- `PROVENANCE_INSUFFICIENCY`;
- `TOOLING_VALIDATOR_FAILURE`;
- `SCOPE_AMBIGUITY`.

`SCIENTIFIC_FALSIFICATION` requires full substantive reassessment before any later admission attempt.

A scope change or scope mutation also requires full substantive reassessment. `SCOPE_AMBIGUITY` may use targeted clarification only when the resolved scope is demonstrably identical to the previously pinned claim. If clarification changes the claim, the review resets substantively.

`EVIDENCE_INSUFFICIENCY`, `PROVENANCE_INSUFFICIENCY` and `TOOLING_VALIDATOR_FAILURE` may use targeted re-review. The targeted review is limited to failed gates plus regression guards and is permitted only when all reused PASS gates remain immutable, compatible and unsuperseded.

A tooling failure is never silently converted into scientific PASS. A green validator confirms the encoded decision; it does not by itself prove the scientific claim.

## Independence policy

Separate ChatGPT context is process independence only. It is not organizational or human independence.

Tier A low-risk work does not require a separate ChatGPT context when every strengthened Tier A technical and automated gate passes.

Tier B and Tier C require one genuinely independent review context under GOV04. Tier D requires independent review appropriate to the composition or production-bound object. A future downgrade may occur only through a separately qualified governance decision. GOV04 itself provides no generic downgrade for Tier B or higher.

When an independent-review gate is required, the same authoring context may not approve that gate. Existing same-context technical review may be evidence input, but cannot substitute for the required independent decision.

## Admission workunit combination

Tier A: evidence qualification, technical review, disposition and admission closeout may be combined when every Tier A waiver gate passes.

Tier B: the independent review remains separate. After PASS, disposition and admission closeout may be combined.

Tier C: combination is not the default. It may occur only when the independent review explicitly covers the exact final disposition object and traceability is not reduced. State, restart and numerical-policy cases should normally keep a distinct admission decision.

Tier D: composition, integration and production authorization remain separate qualification surfaces even if some mechanical steps share a workflow.

No workunit may approve its own required independent-review gate.

## Central regie aggregation

GOV04 replaces the practical convention of creating a new RG05 letter after nearly every atomic admission.

The normal central-regie cadence is a batch of 3 to 5 new atomic admissions. Aggregate integration must occur earlier when any real project gate changes, including:

- B3 completeness;
- B4 eligibility;
- production eligibility;
- canonical routing;
- a cross-TCD dependency that changes downstream work eligibility;
- a governance authority change that downstream work must consume immediately.

Five pending atomic admissions is the normal upper bound before an aggregate integration is required. An earlier aggregate update is always allowed when it materially reduces ambiguity.

The following distinction is authoritative:

`atomic admission authority != latest aggregate regie snapshot`

until the next aggregate integration has incorporated that admission.

Every admitted atomic object is authoritative from its own qualified admission record. Pending aggregate integration must retain at least the exact admission workunit, commit identity, admission record identity, disposition, historical-uncertainty state and the last aggregate-regie snapshot. Central batching may delay aggregate reporting. It may not delay or erase atomic traceability.

The qualified RG05E snapshot is the final pre-GOV04 atomic-by-atomic integration snapshot and becomes the starting aggregate-regie reference for future GOV04-controlled admissions. Historical `RG05`, `RG05A`, `RG05B`, `RG05C`, `RG05D` and finalized `RG05E` remain immutable.

## Transitional rules

GOV04 is prospective. It does not invalidate or rewrite completed reviews or admissions.

Existing finalized reviews remain valid evidence at their original scope and strength. Existing admissions remain valid. Existing FAIL and INCOMPLETE records remain historically true and are never rewritten to PASS by this policy.

Open workunits may use GOV04 only after GOV04 itself is qualified. An independent review already in progress may continue when completion is cheaper or safer than switching. Switching is allowed only when the new tier is determined from live evidence and no scientific gate is lost.

GOV03 remains authoritative for historical-reference acquisition closure. Where no qualified B2 exists, historical behaviour remains `UNKNOWN`. GOV04 does not fabricate B2 and does not convert historical uncertainty to historical fidelity.

## Live transition decisions at GOV04 closeout

### TCD-015

TCD-015 remains risk Tier B, but its lane completed concurrently with GOV04. `ANIMO-B3D12@5e33c195174e41ea949d5a828d30bb7b9e313a5d` admitted the atomic nitrate-only, GHG-off correction with historical behaviour `UNKNOWN`, using the qualified independent review `ANIMO-B3B01R@a6880282e9ed743f97a3435b55e4fb54f7d55a44`. `ANIMO-RG05E@eed822037ed8d906a2ab424220597cffac9cca73` then integrated that fifth admission centrally. GOV04 performs no further TCD-015 action and does not reopen it.

For future Tier B cases, this chain can be shorter: retain one genuinely independent second-line review, then combine post-review disposition and admission closeout when pins and route are unchanged. Central regie need not update after each such atomic admission.

### TCD-027

TCD-027 remains a Class A candidate and is eligible for the Tier A path, but GOV04 does not admit it. The existing second-line result `ANIMO-B3A01R@510c9313926457cd9bfd8e71a551255297bdfbb3` remains `INCOMPLETE` due to evidence insufficiency, not scientific falsification.

The concurrent remediation `ANIMO-B3A01E@5232ef5fa6daafa2296401b19fd9e866a34152bd` has now persisted and structurally validated the three missing frozen-source neighbourhoods: local `Dum` construction, Outbal_write slot 24 to 27 mapping and organic-P slot 25/26/27 self-accumulators. It explicitly did not perform a new independent review and did not admit TCD-027.

Under GOV04, the old instruction in B3A01E to start a new B3A01R2 is superseded prospectively only if a new bounded Tier A qualification/admission workunit verifies all GOV04 waiver predicates against B3A01, B3D10 and B3A01E with compatible immutable pins. If every Tier A condition passes, no separate B3A01R2 context is required. If source meaning, ownership, state or flux non-interference remains ambiguous, the waiver fails and TCD-027 escalates.

### TCD-040

TCD-040 is risk Tier C because its scientific surface is restart and initialization semantics, regardless of its local legacy class label. Its independent review `ANIMO-B3B04R@bb001129578457ca8435e39deb2b8586e7ebc6a2` remains fail closed with `FAIL_CLOSED_INDEPENDENT_EVIDENCE_REPLAY_INCOMPLETE`; the scientific claim was not falsified.

The live evidence-remediation lane `ANIMO-B3B04E1@b3f509806119ea2c2aaf0694c08d4a5bb13e6ca3` has a local reconstructed replay PASS but still fails closed because controlled immutable B0 acquisition and independent CI replay are not proven. The E3 branch is still only a reservation at the E2 head and has no unique E3 work yet.

Tier C therefore remains unchanged: independent review is required. After controlled B0 evidence remediation succeeds, targeted independent re-review may focus on the failed replay/provenance gates plus regression guards only if prior PASS gates, claim scope and source identities are unchanged. Otherwise full re-review is required.

## Hard invariants

GOV04 does not:

- remove a scientific gate;
- fabricate B2;
- turn historical uncertainty into historical fidelity;
- rewrite an existing FAIL or INCOMPLETE result;
- withdraw an existing admission;
- open B4;
- open production migration;
- change the canonical TCD register;
- change production source;
- define away an open scientific blocker;
- compose admitted TCDs;
- admit any TCD itself.

Review reduction is allowed only through better risk allocation, stronger evidence reuse, automation and explicit escalation rules.
