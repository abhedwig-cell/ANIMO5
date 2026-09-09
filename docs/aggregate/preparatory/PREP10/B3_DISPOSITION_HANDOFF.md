# PREP10 stable-DOM plough accumulator B3 disposition handoff

Status: `READY_FOR_B3_INTAKE_NOT_ADMITTED`.

## Scope

This handoff packages the PREP10 stable-DOM plough accumulator finding for the separate ANIMO-B3Q01 scientific-admission process. It does not create a corrected-legacy branch, does not assign a canonical TCD identifier, and admits no corrected behaviour.

The current B3Q01 canonical input register is explicitly frozen through `TCD-027`. Because PREP10 was qualified later and parallel work may also allocate identifiers, this workunit deliberately uses the local intake key:

`PREP10-SDOM-PLOUGH-ACCUMULATOR-RESET`

Canonical TCD assignment belongs to the central discrepancy/admission register.

## Frozen identity

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank archive SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- `Addit.for` SHA-256: `e3cf8f427e9a4b3743742039c89aae57864cb7268893e45797c7a17427dc8f5d`

## Atomic causal claim

Inside the `Pl(I) > 0` plough branch, the three local stable dissolved-organic redistribution accumulators

- `SuStdiorma`,
- `SuStdiorni`,
- `SuStdiorpo`

are first assigned through self-reading expressions and have no explicit definition/reset before those reads. Under the current GNU diagnostic contract with `-fno-automatic`, values accumulated during one plough event remain present when a later plough event starts.

The proposed atomic correction mechanism for later qualification is therefore only:

> define the three event-local accumulators as zero at the beginning of each plough event, with the P reset conditional only insofar as required by the existing P branch semantics.

No other `Addit.for` logic belongs to this atomic candidate.

## Provisional B3 class

Provisional class: `B`.

Rationale: B3Q01 Class B covers a local implementation defect for which the intended local mathematical operation can be identified without adding a physical state or changing numerical policy. PREP10 has isolated one event-local accumulation identity. The reset counterfactual changes downstream state/output trajectories when the path is activated, so the item cannot be Class A reporting-only. It does not add a new physical state and does not alter solver/tolerance policy, so Class C or E is not presently indicated.

This classification is provisional. B3Q01 or its successor must confirm it before admission.

## B1 causal evidence already available

PREP10 has two distinct causal evidence layers.

### Natural frozen-testbank observation

Four successful plough-active frozen cases exercised 31 events in total. All observed stable-DOM/DON/DOP accumulators were zero before and after the relevant loop. Baseline and event-reset counterfactual model outputs therefore did not discriminate for those frozen inputs.

This is useful negative applicability evidence: the available frozen cases are dormant for this defect under the current GNU diagnostic environment.

### Controlled activation descendants

Two explicit B0-derived diagnostic descendants made selected initial stable-DOM/DON/DOP values nonzero while preserving parent identity and transform lineage.

For CranMais, C/N values generated at event 1 were still present before event 2 and the explicit event reset changed 12 generated files scientifically or structurally.

For the phosphorus-enabled Zuiderzeeland case, C/N/P values generated at event 1 were still present before event 2 and the reset changed 8 generated files scientifically or structurally. This independently exercises the conditional phosphorus path.

Observer builds were non-intrusive for the compared generated outputs in both activated cases.

These controlled descendants establish B1-style causality and branch coverage. They are not historical B2 evidence and their activation amplitudes are not claimed to represent field-realistic states.

## Expected-difference contract for a future corrected-legacy candidate

The candidate must declare before evaluation that the following may change after a repeated plough event with nonzero stable DOM/DON/DOP:

- stable dissolved-organic C/N/P redistribution values affected by the plough operation;
- downstream state variables fed by those redistributed quantities;
- dependent balance and reporting outputs;
- later fluxes only where they are causally downstream of the changed state.

The following must remain unchanged except for floating-point propagation demonstrably downstream of the declared affected states:

- physical processes outside the plough/stable-DOM redistribution dependency surface;
- management event timing and selection;
- hydrology forcing and hydrology state not coupled through changed chemistry;
- source/testcase B0 identities;
- numerical solver/tolerance policy;
- unrelated ledger definitions.

No global numerical tolerance may be invented to satisfy this contract. Unrounded affected state/flux comparison is required wherever report precision can hide differences.

## Conservation and local-identity requirement

A future Class B admission must demonstrate the event-local identity independently of the proposed patch:

1. each plough event starts its stable-DOM/DON/DOP summation from the neutral additive identity zero;
2. after the accumulation loop, each accumulator equals only the mass contribution from the current event's selected plough layers/reservoirs;
3. no contribution from an earlier plough event is present in the current-event redistribution total;
4. C, N and conditional P branches are checked separately;
5. whole-case element conservation and relevant transfer ledgers are checked before and after the correction.

The current controlled experiment proves carryover and discrimination but does not yet constitute independent scientific review of this identity.

## B2 route

Preferred route: `NORMAL_B2_AVAILABLE` if PREP02R obtains a provenance-qualified historical ANIMO 4.1.x native executable/build and the path can be exercised.

Current B2 status: `NOT_ESTABLISHED`.

Until the documented historical-reference acquisition effort is formally exhausted, PREP10 does not invoke the B3 historical-uncertainty fallback route.

If that fallback is later considered, B3Q01 requires an authoritative or unambiguous closed identity, at least one dedicated causal test plus an independent cross-check, stronger coverage, independent second-line review, and explicit propagation of historical uncertainty.

## Independent review still required

The authoring diagnostic and reset counterfactual cannot serve as their own second-line review. Before any `ADMIT_CORRECTED_LEGACY_BEHAVIOUR` disposition, a separate review must confirm at minimum:

- provisional Class B is correct;
- the accumulator is event-local by model intent, not intentionally cumulative;
- the reset location and P conditional semantics are correct;
- expected changed and unchanged surfaces are complete;
- conservation evidence is sufficient;
- B2 or historical-uncertainty route prerequisites are satisfied.

## Evidence package

Primary PREP10 artifacts:

- `docs/prep10/WORKING_FINDINGS.md`
- `integration/animo-prep/PREP10_STABLE_DOM_PLOUGH_ACCUMULATOR_AUDIT.json`
- `integration/animo-prep/PREP10_GNU_STABLE_DOM_OBSERVER_MATRIX.json`
- `integration/animo-prep/PREP10_STABLE_DOM_CAUSAL_ACTIVATION_MATRIX.json`
- `tools/audit_stable_dom_plough_accumulators.py`
- `tools/audit_stable_dom_plough_activation.py`
- `tools/probe_prep10_local_storage_semantics.py`
- `tools/make_prep10_addit_variants.py`
- `tools/make_prep10_sdomin_activation.py`

B3 governance basis inspected from `work/animo-b3q01-scientific-admission-framework`:

- `docs/governance/B3_SCIENTIFIC_ADMISSION_FRAMEWORK.md`
- `docs/governance/B3_QUALIFICATION_CLASSES.md`
- `integration/animo-b3/B3_EXISTING_TCD_CLASSIFICATION.csv`

## Disposition now

Current disposition remains:

`UNRESOLVED_NOT_ADMITTED`

with intake readiness:

`READY_FOR_B3_INTAKE_NOT_ADMITTED`.

The next valid action is central B3 intake and independent qualification. Implementing the reset in frozen source or treating the GNU counterfactual as corrected legacy would be premature.
