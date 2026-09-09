# ANIMO-PREP10C — Event-reset corrected-legacy candidate qualification

Status: `QUALIFIED_CORRECTED_LEGACY_CANDIDATE_REANCHORED_TO_AUTHORITATIVE_PREP10_B3_ADMISSION_OPEN`.

## Scope and lineage correction

PREP10C turns the PREP10 event-reset diagnostic counterfactual into a deterministic corrected-legacy **candidate** while preserving the admission boundary. It does not change B0, create a B2 reference, admit B3 or authorize ANIMO5 migration.

The authoritative parent is now:

- branch: `work/animo-prep10-stable-dom-plough-accumulators`;
- commit: `65cd4a65a3ea27cd4ce004f505d5022fdb08b9ab`.

An earlier PREP10C branch was created from `work/animo-prep10-stable-dom-causal-activation`. That branch later became supplemental corroboration rather than the authoritative PREP10 lineage. PREP10C has therefore been re-anchored by transplanting only its candidate-specific files onto the authoritative PREP10 head. No merge from the superseded parallel causal history was used.

## Atomic candidate identity

Frozen revision-53 `Addit.for` SHA-256:

`e3cf8f427e9a4b3743742039c89aae57864cb7268893e45797c7a17427dc8f5d`

`tools/make_prep10c_corrected_addit.py` accepts only that exact member and inserts:

```fortran
SuStdiorma = 0.0
SuStdiorni = 0.0
If (Ipo.Eq.1) SuStdiorpo = 0.0
```

at the beginning of each `Pl(I)>0` event.

The candidate member SHA-256 is:

`a1993aa2d22c8f2c13fc169e78f9121587c8f14a122ef7d3f757cc24a58a54ae`

The current-GNU candidate executable SHA-256 is:

`f3518bbca36989960fbe02785d64cca873d5e45494baa4e0c0a9a7c026a717db`

Both identities match the event-reset counterfactual recorded by authoritative PREP10 in `PREP10_STABLE_DOM_CAUSAL_ACTIVATION_MATRIX.json`. This binds the candidate to the correction mechanism that PREP10 actually exercised, rather than merely to a similar source edit.

## Authoritative PREP10 causal basis

Authoritative PREP10 records controlled B0-derived diagnostic descendants for CranMais and phosphorus-enabled Zuiderzeeland. Under the established GNU diagnostic contract, the first plough event creates nonzero stable-pool accumulator values and those values remain present before the next event. The reset counterfactual changes scientific outputs for both the C/N path and the conditional P path. The same record explicitly classifies this as diagnostic causality evidence, not B2 reference evidence.

Supplemental isolated-species results from the earlier parallel branch remain available only through `PREP10_PARALLEL_CAUSAL_EVIDENCE_RECONCILIATION.json`. PREP10C does not make that branch its ancestry and does not count parallel corroboration as independent second-line review.

## Conservation reconciliation

The source-bound audit uses exact frozen `Addit.for` plus `Inicalc.for` SHA-256 `306dd3be262a9eaa293520c754190931bc54e76e7d84b3145efe5663a3e523e1`.

`Inicalc.for` defines `Bo(Pl)` as cumulative layer thickness. The plough code forms a stable DOM/DON/DOP event accumulator over `Ln=0..Pl(I)` and redistributes it to `Ln=1..Pl(I)` in fractions proportional to `He(Ln)/Bo(Pl(I))`. The redistributed fractions sum to one. Therefore the redistribution is closed for the current event only when the accumulator starts from the additive identity zero.

If a previous event value persists, the code forms `S_event = S_prior + S_current` and redistributes `S_prior` again. The candidate removes only that stale cross-event term. It does not alter the current-event summation, redistribution equations, state definition or numerical solver policy.

`tools/audit_prep10c_plough_conservation.py` encodes these exact source-bound checks and fails closed on unexpected source identity or source structure.

## Frozen-testbank non-interference

The candidate qualification run used the exact frozen testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

For the eight supplied cases that complete under the established GNU diagnostic compatibility contract, baseline versus candidate compared 550 common generated files:

- 450 raw-equal;
- 100 equal after declared volatile timestamp/CPU normalization;
- 0 scientific or structural differences;
- 0 missing candidate files;
- 0 unexpected candidate files.

No scientific-number tolerance was used. `GHGMais` terminates with return code 203 for both baseline and candidate because of the pre-existing supplied-testcase/revision-53 lineage/input-contract mismatch and is not treated as qualification evidence for the correction.

The lineage re-anchor does not reinterpret these model runs as newly executed. Their candidate source and executable identities are unchanged and are explicitly hash-bound. Public CI validates tooling and machine-readable evidence but does not receive restricted B0 bytes.

## Expected-difference contract

When a nonzero stable pool reaches repeated plough events, the candidate may change stable DOM/DON/DOP redistributed state, restart state and causally downstream process/balance output. When the event accumulators remain zero, scientific outputs are expected to remain unchanged.

Non-plough paths, unrelated routines, input compatibility transforms, process ordering, precision policy and convergence policy remain outside the intended changed surface.

## B3Q01 and TCD-028 boundary

The candidate remains provisionally B3Q01 Class B. Central B3 intake draft PR #10 separately reserves `TCD-028` for the stable-DOM plough accumulator event-reset defect. That reservation is `RESERVED_PENDING_CANONICAL_REGISTER_APPEND_NOT_ADMITTED`; it is not itself canonical registration or admission.

At this checkpoint:

- B2 historical-native evidence for the affected path is not established;
- the historical-uncertainty route is not open;
- independent second-line review is not complete;
- corrected legacy is not admitted;
- B3 composition is not admitted;
- B4/production migration is not admitted.

The fail-closed disposition therefore remains `UNRESOLVED_NOT_ADMITTED` even though the implementation candidate is qualified for independent review.

## Next gate

The useful next action is an independent B3Q01 review against the authoritative PREP10 evidence and TCD-028 reservation, coordinated with PREP02R. A recovered provenance-qualified historical native reference must be incorporated. If B2 remains unavailable, the stricter historical-uncertainty route may only be considered after the documented acquisition precondition is genuinely exhausted.
