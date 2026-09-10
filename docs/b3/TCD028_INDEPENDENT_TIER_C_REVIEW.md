# ANIMO-B3B08R: Independent Tier-C Second-Line Review of TCD-028

Review result: `PASS`

Target: `TCD-028`, stable DOM plough redistribution accumulator lifecycle.

This review is a genuinely separate second-line scientific assessment of the frozen `ANIMO-B3B08` readiness object. It does not inherit the scientific conclusion of B3B08, PREP10 or PREP10C. Immutable source and evidence pins are reused only at their recorded strength. No B3 admission is performed here.

## 1. Live authority recheck

The review started from the clean review-contract head `71340e036504695ba7177f31c0be9345895680b3`, whose parent is the frozen readiness candidate `310d7117da739d19eebb718129ac9494cac854a1`.

Live authority state checked before the scientific decision:

- aggregate central regie: `ANIMO-RG05F@7c61a5031f41d602e996310df6f3958cbd1b511e`;
- post-RG05F atomic admission 1: `ANIMO-B3D15@22e48f7e2c1eaa1245f034de2d909191d9cfa227`, TCD-030;
- post-RG05F atomic admission 2: `ANIMO-B3D16@8650ea9e716336520d8d7df5f9ea2b393d17ab98`, TCD-023;
- no B3D17+ branch and no RG05G+ aggregate branch was present in the live branch search;
- `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`;
- `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`;
- `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- `ANIMO-B3I01@383c7a83e84a578969f92113280dc715b7bdddb4`;
- `ANIMO-B3I03@814ea660d367494432beb63ea78298d1f6cd73d7`;
- authoritative `ANIMO-PREP10@65cd4a65a3ea27cd4ce004f505d5022fdb08b9ab`;
- authoritative `ANIMO-PREP10C@549545921dc8175f01d86c283647acd470c14290`.

Issue #46 had no comments. Issue #8 and all current comments were read. The live TCD-028 search and branch inventory exposed no newer TCD-028 review, candidate, issue, evidence authority or routing object that supersedes the frozen review object. The B3B08 branch has a later status-only head `215f3800df5afa5811c1105cec2fb4f77a5548c2`; its frozen review object remains `310d7117da739d19eebb718129ac9494cac854a1`.

The canonical TCD-028 row remains `OPEN`. B3I03 appended TCD-042 without changing pre-existing logical rows, so no later canonical-register mutation changes TCD-028.

## 2. Reviewed identities

Frozen readiness authority: `ANIMO-B3B08@310d7117da739d19eebb718129ac9494cac854a1`.

Validated substantive evidence head: `0145b80e7e308d82995f783cc4febb3b4c9da6ad`.

Readiness CI: run `34490160286`, job `102914502580`, conclusion `success`.

Frozen source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`.

Frozen testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

Frozen `ANIMO_4.1.5.53/Addit.for` SHA-256: `e3cf8f427e9a4b3743742039c89aae57864cb7268893e45797c7a17427dc8f5d`.

Pinned `Inicalc.for` SHA-256 used for the `Bo` definition: `306dd3be262a9eaa293520c754190931bc54e76e7d84b3145efe5663a3e523e1`.

Candidate `Addit.for` SHA-256: `a1993aa2d22c8f2c13fc169e78f9121587c8f14a122ef7d3f757cc24a58a54ae`.

Candidate current-GNU executable SHA-256: `f3518bbca36989960fbe02785d64cca873d5e45494baa4e0c0a9a7c026a717db`.

The candidate change is exactly three event-start initializations inside `Pl(I)>0`, before the stable-pool accumulation loop:

```fortran
SuStdiorma = 0.0
SuStdiorni = 0.0
If (Ipo.Eq.1) SuStdiorpo = 0.0
```

## 3. Independent source and ownership reconstruction

The exact hash-bound source audit identifies `SuStdiorma`, `SuStdiorni` and `SuStdiorpo` as scalar locals in `Addit.for`. The active plough branch starts at source line 449. Their first assignments inside that transaction are self-reading accumulation expressions at lines 475, 477 and 479, with the P expression conditional on `Ipo.Eq.1`. No explicit definition or zero assignment precedes those first reads.

The decisive point is not merely use-before-definition. The surrounding dataflow defines one plough transaction. The code first reduces the stable DOM, DON and, when enabled, DOP material over `Ln=0..Pl(I)`. It then writes redistributed stable-pool state into `Ln=1..Pl(I)` using the current plough-depth control volume. `Bo(Pl(I))` is the cumulative thickness of the current selected soil layers.

I independently classify the three `SuStd...` scalars as current-event transaction accumulators, not as scientific cross-event storage. The reason is causal ownership. After event 1, the redistributed material has already been written into the physical `CoStdiorma`, `CoStdiorni` and conditional `CoStdiorpo` state. At event 2, the current-state reduction therefore already sees whatever event-1 material physically remains in the selected control volume. A separately surviving `S_prior` has no independent physical owner. Adding it again to the event-2 reduction counts a prior transaction total a second time.

A cumulative interpretation would require a distinct scientific storage meaning, an explicit initialization contract and a lifecycle that explains why the cumulative quantity is added again after its material has already been represented in the physical stable-pool arrays. No such ownership contract is present in the reviewed evidence. The local scalar form and the absence of explicit initialization are inconsistent with treating these variables as intentional conserved cross-event stores.

This ownership conclusion does not depend on current GNU persistence. GNU persistence only exposes one runtime manifestation of the undefined lifecycle. Historical revision-53 Intel/native manifestation remains a separate question.

## 4. Control volume and conservation determination

The reviewed source-bound facts establish the following current-event structure:

1. `Bo(Pl(I))` represents the current plough-depth layer-thickness total.
2. Current material is collected over `Ln=0..Pl(I)`, including the surface/reservoir coordinate and the selected plough layers.
3. Redistribution is applied to `Ln=1..Pl(I)` using the current plough-depth normalization.
4. The layer fractions close over the current selected plough control volume.
5. The same temporal ownership applies independently to C and N, and to P only when the phosphorus path is enabled.

Let `S_current` denote the stable-pool transaction total reconstructed from the current physical state at an event. With a properly initialized transaction accumulator, the redistributed transaction is based on `S_event = S_current`. If a previous local value persists, the source instead evaluates the equivalent temporal form `S_event = S_prior + S_current`. Because `S_prior` is a prior transaction total whose material was already written into physical state, that term is stale and is redistributed again. Zero initialization removes exactly `S_prior`; it does not remove or alter any term in the current-event reduction.

The conservation conclusion is therefore claim-scoped: the additive identity zero is required at the start of every `Pl(I)>0` event for these three transaction accumulators. This is stronger than saying the reset improves a balance. It follows from the ownership and control-volume structure.

I also checked a limitation of the existing source-bound conservation checker: its final temporal identity is encoded rather than obtained from a symbolic parser of the entire Fortran expression. I do not use that encoded conclusion as independent proof. The review conclusion instead follows from the pinned first-read/update seam, the current-state reduction domain, the current-control-volume redistribution, and the fact that the prior transaction is already materialized in the physical stable-pool state. The omitted historical runtime question does not change that temporal ownership identity.

## 5. Causal evidence, species separation and negative control

The evidence is reused at B1 diagnostic strength only.

Under controlled B0-derived activation in the current GNU diagnostic contract, event 1 creates nonzero C and N accumulators and the exact values remain present immediately before event 2. A phosphorus-enabled controlled case shows the same carryover for conditional P. The reset counterfactual changes scientific or structural outputs after activation.

The isolated-species corroboration is directionally consistent with the same mechanism: C-only and N-only activation produce downstream differences. P-only activation in a phosphorus-enabled case produces P-path differences and a persistent event-1 value before event 2. The phosphorus-disabled P negative control produces no scientific differences. This is the expected branch-specific behavior and argues against a generic unrelated perturbation.

None of these controlled descendants is a historical reference. Their amplitudes are diagnostic and are not evidence of realistic field magnitude or frequency.

## 6. Frozen-testbank non-interference and its limitation

The candidate comparison over the eight completing frozen cases examined 550 common generated files: 450 were raw-equal and 100 became equal after declared volatile timestamp/CPU normalization. There were zero scientific or structural differences, zero missing candidate files and zero unexpected candidate files. No scientific-number tolerance was used.

This is supporting scope/non-interference evidence only. It is not a discriminating correctness test for TCD-028. In the four successful frozen cases that actually reached the plough branch, all three observed accumulators remained zero over all 31 observed plough events. Baseline and reset are therefore expected to coincide in those frozen runs.

The frozen matrix cannot be used to infer that the defect is harmless when stable DOM/DON/DOP is nonzero at repeated plough events.

## 7. Expected-difference surface

Allowed differences for this exact candidate are restricted to repeated active plough events where a nonzero affected stable pool reaches the transaction. They may include:

- stable DOM, DON and conditional DOP redistribution state;
- downstream physical state causally fed by that redistribution;
- downstream process fluxes caused by the changed state;
- dependent C, N and P balances and reports;
- restart output/state only as a downstream image of already changed physical state.

The candidate must not change the plough trigger or event timing, restart serialization/checkpoint representation, unrelated process order, numerical precision policy, solver/tolerance policy, unrelated ledger definitions, frozen input identity or non-plough source semantics. When the affected event accumulators are zero, scientific output equality is the expected result.

No global tolerance is part of this review. Affected quantities require unrounded comparison when report precision could hide differences.

## 8. B3 class and GOV04 risk tier

B3 qualification class: `B_LOCAL_ALGEBRA_INDEX_SPECIES`.

I retain Class B because the accepted scientific interpretation is a local transaction-reduction initialization correction. The candidate adds no physical state, does not redefine persistent state, does not change numerical policy, solver behavior, tolerance policy or process equations, and does not compose another TCD.

GOV04 risk tier: `C`.

The strictest applicable triggers are:

- `INITIALIZATION_SEMANTICS`;
- `SCIENTIFIC_STATE_OR_SOURCE_OWNERSHIP_AMBIGUITY`.

Those triggers require the independent Tier-C review even though the implementation patch is only three local assignments. There is no stronger Tier-D trigger in the reviewed object: no composition, cross-module coupling, B4 scope, production-bound migration, whole-model claim or multi-TCD dependency is introduced. No numerical-policy or solver trigger appears.

## 9. Historical-uncertainty boundary

GOV03 currently records `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT` and opens `ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS`.

That route does not create B2. The current GNU `-fno-automatic` persistence observation is not historical Intel/native evidence. The historical revision-53 manifestation remains exactly:

`UNKNOWN_WITHOUT_B2`

This PASS is therefore a scientific ownership/conservation review under explicit historical uncertainty. It is not a claim that a historical Intel executable necessarily carried the stale value, nor a claim of historical behavioral fidelity.

## 10. Residual uncertainties

The following remain open but do not falsify or leave ambiguous the claim-scoped transaction identity:

- historical Intel/native manifestation of the undefined local lifecycle;
- realistic field frequency and magnitude of nonzero affected stable pools at repeated plough events;
- a future provenance-qualified B2 artifact, if one is discovered;
- whole-model or production-composed behavior, which is outside this review.

A newly discovered credible historical artifact would reopen the B2 question under GOV03. Any candidate widening into restart serialization, physical-state redesign, numerical policy, composition or production migration would require a new risk/scope assessment and is not covered by this PASS.

## 11. Independent review decision

`PASS`

The independent Tier-C scientific review gate is satisfied for the exact frozen TCD-028 readiness object and the exact candidate identity stated above.

This review performs no B3 admission, no production-source modification, no frozen-B0 modification, no canonical TCD register edit, no TCD composition, no B4 opening, no production migration and no central-regie update.

The next permissible workunit after validated PASS is a separate Tier-C formal-disposition workunit. This review does not perform that disposition.
