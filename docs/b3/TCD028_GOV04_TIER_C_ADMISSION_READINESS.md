# ANIMO-B3B08 — TCD-028 Stable-DOM Plough Event-Accumulator Admission Readiness

## Decision

`TCD-028` is qualified here as a **B3 Class B local implementation correction with GOV04 risk Tier C** for admission-readiness review.

The apparent mismatch is intentional. B3 qualification class describes the correction type; GOV04 risk tier determines review intensity. The candidate is local and atomic, but its scientific question is whether three accumulators are event-local quantities that must be initialized to the additive identity at every plough event rather than cumulative cross-event storage. GOV04 explicitly forces Tier C for initialization semantics and scientific state/source ownership ambiguity.

This workunit is not an independent review, not a B3 admission and not a production authorization.

## Live authority snapshot and collision check

The workunit was created from the current aggregate central-regie authority:

`ANIMO-RG05F@7c61a5031f41d602e996310df6f3958cbd1b511e`

At creation, the authoritative post-RG05F atomic admissions observed were:

- `ANIMO-B3D15@22e48f7e2c1eaa1245f034de2d909191d9cfa227` — TCD-030;
- `ANIMO-B3D16@8650ea9e716336520d8d7df5f9ea2b393d17ab98` — TCD-023.

They are external authority observations only and are not merged or composed into B3B08.

Governance/evidence authorities are:

- `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`;
- `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`;
- `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- `ANIMO-B3I01@383c7a83e84a578969f92113280dc715b7bdddb4` for post-G5 routing;
- `ANIMO-B3I03@814ea660d367494432beb63ea78298d1f6cd73d7` for the later canonical register state;
- `ANIMO-PREP10@65cd4a65a3ea27cd4ce004f505d5022fdb08b9ab`;
- authoritative `ANIMO-PREP10C@549545921dc8175f01d86c283647acd470c14290`.

No `ANIMO-B3B08` or later dedicated TCD-028 readiness/review branch was found before branch creation. GitHub issue #8 remains the earlier PREP10 intake issue.

The diverged branch `work/animo-prep10c-stable-dom-reset-readiness@f88b8a4ca65bff4a3d9c4132a7f384c2ae698087` is explicitly superseded. Its old proposed `TCD-032` identity must not be used or merged. Canonical identity for this phenomenon is `TCD-028`.

## Canonical claim

The later canonical register records TCD-028 as:

`stable DOM plough redistribution accumulator lifecycle`

with the scientific requirement that stable-DOM redistribution conserve **event-local transferred mass**. It remains `OPEN` and records unresolved historical revision-53 event-accumulator semantics.

The atomic candidate is restricted to initialization of these existing event accumulators at the beginning of each active `Pl(I) > 0` plough event:

```fortran
SuStdiorma = 0.0
SuStdiorni = 0.0
If (Ipo.Eq.1) SuStdiorpo = 0.0
```

The conditional phosphorus semantics are preserved. No new physical state is introduced.

## Frozen identity and exact seam

Pinned frozen identities:

- source archive SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank archive SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- frozen `Addit.for` SHA-256 `e3cf8f427e9a4b3743742039c89aae57864cb7268893e45797c7a17427dc8f5d`, size 35,615 bytes.

The PREP10 source audit pins the active plough-event branch at line 449 and the first self-read assignments of `SuStdiorma`, `SuStdiorni` and `SuStdiorpo` at lines 475, 477 and 479 respectively. No explicit definition or zero initialization precedes those first self-reads in the frozen source.

The authoritative PREP10C transform produces candidate `Addit.for` SHA-256:

`a1993aa2d22c8f2c13fc169e78f9121587c8f14a122ef7d3f757cc24a58a54ae`

and current-GNU candidate executable SHA-256:

`f3518bbca36989960fbe02785d64cca873d5e45494baa4e0c0a9a7c026a717db`.

These identities are evidence pins only. No source is modified in B3B08.

## Scientific identity and conservation

The relevant control-volume identity is event-local. `Bo(Pl)` is cumulative layer thickness over the redistribution depth. Stable DOM/DON/DOP is summed for the current plough event and then redistributed over layers in fractions proportional to `He(Ln)/Bo(Pl(I))`. Those fractions sum to one.

For each applicable species, the event accumulator must therefore satisfy:

`S_event(start) = 0`

and after the summation:

`S_event = S_current_event`.

If stale prior-event storage survives, the effective quantity becomes:

`S_event = S_prior + S_current_event`

and `S_prior` is redistributed a second time. The candidate removes exactly that stale cross-event term while leaving current-event summation and redistribution algebra unchanged.

This does not prove historical compiler manifestation. It defines the scientific event-local identity that the independent reviewer must accept or reject.

## Causal evidence and coverage

Under GOV04 `VERIFY_AND_REUSE_WITH_HIGH_RISK_SCOPE_CHECK`, B3B08 reuses the immutable PREP10/PREP10C evidence at its original strength.

The frozen testbank contains four successful plough-active cases and 31 observed plough events, but those cases are non-discriminating because the observed stable-DOM accumulators remain zero. This is not evidence that the defect is harmless.

Controlled B0-derived diagnostic descendants deliberately activate nonzero stable DOM/DON/DOP. Under the pinned current-GNU diagnostic contract, PREP10 observes inter-event carryover and reset discrimination for C and N and, in a phosphorus-enabled case, conditional P. The reset counterfactual changes 12 scientific/structural files in controlled CranMais and 8 in phosphorus-enabled Zuiderzeeland. A phosphorus-disabled negative control is also available.

These are B1-style causal and scope data. They are not B2 and do not establish historical prevalence or realistic field magnitude.

PREP10C additionally reports a frozen-testbank candidate non-interference surface of eight completing cases, 550 common files, 450 raw-equal and 100 volatile-only-equal files, with zero scientific/structural differences, no missing or unexpected outputs, and no scientific numeric tolerance. Because the frozen cases are non-discriminating, this is supporting non-interference evidence only.

## GOV04 risk classification

B3Q01 Class B remains appropriate because the correction is local, does not add or redefine a physical state model, and does not change the numerical solver, tolerance or precision policy.

GOV04 risk Tier B is nevertheless **not sufficient**. The strictest trigger wins. Two Tier-C triggers apply:

1. `INITIALIZATION_SEMANTICS`: the candidate defines the start value and lifetime boundary of quantities used in a scientific redistribution event;
2. `SCIENTIFIC_STATE_OR_SOURCE_OWNERSHIP_AMBIGUITY`: the key scientific question is precisely whether these values are event-local scratch/transaction accumulators or intentionally cumulative cross-event storage.

Therefore the formal risk classification is:

`GOV04_TIER_C__B3_CLASS_B_LOCAL_EVENT_ACCUMULATOR_INITIALIZATION`

The candidate may change downstream physical state, dependent fluxes, balances and restart output/state because physical state after redistribution changes. It does **not** itself change restart serialization/checkpoint representation, solver policy or numerical policy. Those surfaces remain excluded.

Tier C requires one genuinely independent second-line review in a separate context. Because state/initialization semantics are involved, separate later disposition and admission workunits are preferred rather than automatically combining them.

## Historical route reconciliation

PREP10C was authored before GOV03 closed reasonable B2 acquisition effort and therefore recorded the historical-uncertainty route as not yet eligible. That route-state observation is now superseded by governance, not by changing PREP10C evidence.

Current GOV03 records:

`B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`

and makes the historical-uncertainty route eligible subject to claim-scoped B3 requirements.

No B2 has thereby been created. Historical revision-53 local-storage manifestation remains:

`UNKNOWN_WITHOUT_B2`.

Current-GNU persistence evidence is not historical Intel/native evidence. Independent Tier-C review must still establish whether the event-local scientific intent is sufficiently unambiguous for admission under historical uncertainty.

## Expected-difference contract

When the defect is causally active, the correction may change stable dissolved-organic C/N/P plough redistribution, the physical state fed by that redistribution, causally dependent process fluxes, balances/reports and restart output/state as a downstream image of changed physical state.

It must not, as part of TCD-028, change management event timing/selection, the plough trigger, unrelated process order, restart serialization or checkpoint representation, solver/tolerance policy, precision policy, unrelated ledger definitions, or frozen source/testcase identity.

No whole-model trajectory equivalence or general harmlessness claim is made.

## Residual uncertainty and independent-review gate

The following remain deliberately open for the independent reviewer:

- historical Intel/native manifestation is unknown without B2;
- frozen successful plough cases do not discriminate the defect;
- controlled activation proves causality and conservation scope but not field prevalence or realistic magnitude;
- event-local versus intentionally cumulative scientific ownership must be established independently rather than inherited from PREP10/PREP10C authoring.

A PASS must therefore be a real Tier-C scientific review, not a restatement of candidate evidence.

## Hard boundary

B3B08 does not modify production source, frozen B0, the canonical TCD register, central RG05, B4, production migration or any other TCD. It does not merge B3D15/B3D16, the superseded PREP10C branch or any sibling correction. It does not perform the required independent review.

Subject to a green machine gate, the readiness decision is:

`QUALIFIED_CLASS_B_ADMISSION_READINESS_GOV04_TIER_C_HISTORICAL_UNCERTAINTY_REVIEW_REQUIRED`

The only scientific next gate is exactly one genuinely independent Tier-C second-line review of this frozen readiness object.
