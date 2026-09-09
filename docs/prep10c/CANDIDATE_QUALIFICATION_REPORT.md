# ANIMO-PREP10C — Event-reset corrected-legacy candidate qualification

Status: `QUALIFIED_CORRECTED_LEGACY_CANDIDATE_CURRENT_GNU_NONINTERFERENCE_AND_CAUSAL_CONVERGENCE_B3_ADMISSION_OPEN`.

## Scope

PREP10C turns the PREP10 diagnostic reset counterfactual into a deterministic corrected-legacy **candidate** while preserving the admission boundary. It does not change B0, does not create a B2 reference, does not admit B3, and does not authorize ANIMO5 migration.

The parent checkpoint is `0a174fcee84865f027abab3dde491470c7a04afa` on `work/animo-prep10-stable-dom-causal-activation`.

## Atomic candidate

The frozen revision-53 `Addit.for` member has SHA-256:

`e3cf8f427e9a4b3743742039c89aae57864cb7268893e45797c7a17427dc8f5d`

`tools/make_prep10c_corrected_addit.py` accepts only that exact member and inserts three event-start definitions inside `Pl(I)>0`:

```fortran
SuStdiorma = 0.0
SuStdiorni = 0.0
If (Ipo.Eq.1) SuStdiorpo = 0.0
```

The resulting candidate member is 35,719 bytes, retains CRLF layout, and has SHA-256:

`a1993aa2d22c8f2c13fc169e78f9121587c8f14a122ef7d3f757cc24a58a54ae`

That is byte-identical to the PREP10 event-reset counterfactual already used in the DOM, DON and DOP causal experiments. Under the same GNU Fortran 14.2.0 diagnostic build contract, the resulting executable is likewise byte-identical to the qualified reset-counterfactual executable:

`f3518bbca36989960fbe02785d64cca873d5e45494baa4e0c0a9a7c026a717db`

This removes ambiguity about whether PREP10C is testing a different fix from the causal counterfactual.

## Provisional B3Q01 class

The candidate is provisionally classified as B3Q01 **Class B**, a local algebra/index/species correction. The correction does not add a physical state, alter a governing equation, alter a solver tolerance, or change numerical precision policy. It removes stale carryover in three event-local redistribution accumulators.

Classification is not admission.

## Conservation reconciliation

The conservation argument is source-bound to the exact frozen `Addit.for` and `Inicalc.for` members. `Inicalc.for` SHA-256 is:

`306dd3be262a9eaa293520c754190931bc54e76e7d84b3145efe5663a3e523e1`

It defines:

```fortran
Bo(0) = 0.0
Bo(Ln) = Bo(Ln-1) + He(Ln)
```

Therefore `Bo(Pl)` is the cumulative thickness `sum(He(Ln), Ln=1..Pl)`.

In `Addit.for`, the current plough event sums stable DOM/DON/DOP mass over `Ln=0..Pl(I)` into `SuStdiorma`, `SuStdiorni` and `SuStdiorpo`. The redistribution loop then uses:

```text
Help = He(Ln)/Bo(Pl(I)) / local_storage_capacity
CoStdior*(Ln) = Help * SuStdior*
```

Multiplying the redistributed concentration by the same local storage-capacity factor yields layer mass:

`M_new(Ln) = He(Ln)/Bo(Pl) * S_event`.

Summing over `Ln=1..Pl` gives exactly `S_event`. Thus the redistribution is closed for the current event only if the accumulator entering the summation is zero. Without the reset, a persistent `S_prior` produces `S_event = S_prior + S_current`, so prior-event mass is redistributed again. PREP10 directly observed that carryover under the current GNU contract. The candidate removes only `S_prior`; it leaves the current-event summation and redistribution equations unchanged.

`tools/audit_prep10c_plough_conservation.py` hash-pins the source archive and the two relevant members before checking these source facts. Public CI tests the fail-closed parsing helpers without republishing B0 source bytes.

## Frozen-testbank non-interference

The exact frozen testbank SHA-256 is:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Baseline and candidate were run from the same prepared case copies under the established GNU diagnostic compatibility contract. Comparison normalizes only declared volatile creation/run timestamps and elapsed CPU seconds. No scientific-number tolerance is applied.

Eight supplied historical cases complete under both executables. Across those eight runs:

- 550 common files were compared;
- 450 were byte-identical;
- 100 differed only by the declared volatile metadata normalization;
- 0 scientific or structural files differed;
- 0 candidate files were missing;
- 0 unexpected candidate files appeared.

Per-case common-file counts were 54 CranGrass, 43 CranMais, 82 GrassPeat, 74 LWKM, 102 Puitmijn, 92 RuurloGrass, 66 STONE and 37 Zuiderzeeland.

`GHGMais` remains outside the successful matrix. Baseline and candidate both terminate with return code 203 because of the already documented supplied-testcase versus revision-53 input-contract/lineage mismatch. PREP10C does not reinterpret that failure as evidence for or against the correction.

The frozen-testbank result is therefore strong non-interference evidence for the currently executable supplied cases. It is not proof of general harmlessness because the unmodified testbank is already known to be non-discriminating for this defect.

## Causal convergence

PREP10 separately qualified current-GNU causal effects for stable DOM, DON and DOP using controlled diagnostic descendants. PREP10C's candidate `Addit.for` and executable are byte-identical to the reset counterfactual used in those experiments. The candidate therefore converges exactly to the already qualified correction mechanism for the same inputs and environment.

The relevant evidence remains:

- `integration/animo-prep/PREP10_STABLE_DOM_CAUSAL_ACTIVATION.json` for CranMais DOM and DON;
- `integration/animo-prep/PREP10_STABLE_DOP_CAUSAL_ACTIVATION.json` for phosphorus-enabled LWKM DOP.

Those synthetic descendants are causal evidence only. They are not historical B2 cases.

## Expected-difference contract

When a nonzero stable pool reaches repeated plough events, the candidate is expected to change stable DOM/DON/DOP redistributed concentrations, restart state, and downstream outputs causally dependent on those states. When all three accumulators remain zero at every plough event, scientific outputs are expected to remain unchanged.

Non-plough paths, unrelated routines, input compatibility transforms, process ordering, precision policy and convergence policy are outside the intended changed surface.

## B3 admission boundary

The current candidate evidence is sufficient to qualify the implementation candidate under the current GNU diagnostic environment. It is not sufficient for B3 admission.

At this checkpoint:

- a provenance-qualified B2 reference for the affected path is not available;
- the historical-uncertainty route has not been opened as a substitute;
- independent second-line B3 review is not complete;
- corrected legacy is not admitted;
- B3 composition is not admitted;
- ANIMO5 production migration is not admitted.

The fail-closed B3 disposition therefore remains `UNRESOLVED_NOT_ADMITTED` even though the candidate itself is qualified for further review.

## Next gate

The next useful action is no longer another implementation experiment. It is an independent B3Q01 review of this atomic Class B candidate, coordinated with PREP02R so that a recovered historical native reference can be incorporated without rewriting the candidate evidence. If B2 remains unavailable, the stricter historical-uncertainty route may only be considered after its documented acquisition precondition is genuinely satisfied.
