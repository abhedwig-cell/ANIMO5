# ANIMO-PREP10C — Independent B3Q01 review packet

Status: `READY_FOR_INDEPENDENT_REVIEW_NOT_REVIEWED_NOT_ADMITTED`.

This packet is deliberately prepared by the candidate workunit and therefore does **not** count as independent second-line review. The reviewer must be separate from candidate authoring and must record a review result explicitly. Silence, CI success, candidate qualification or agreement with this packet is not a review.

## Review object

- candidate branch: `work/animo-prep10c-stable-dom-event-reset-authoritative`
- authoritative PREP10 parent: `65cd4a65a3ea27cd4ce004f505d5022fdb08b9ab`
- candidate `Addit.for` SHA-256: `a1993aa2d22c8f2c13fc169e78f9121587c8f14a122ef7d3f757cc24a58a54ae`
- frozen `Addit.for` SHA-256: `e3cf8f427e9a4b3743742039c89aae57864cb7268893e45797c7a17427dc8f5d`
- provisional B3Q01 class: Class B
- B3 intake reservation: `TCD-028`, draft PR #10, reservation only
- candidate PR: draft PR #14
- current disposition: `UNRESOLVED_NOT_ADMITTED`

## Evidence the reviewer should inspect

Authoritative PREP10 evidence:

1. `integration/animo-prep/PREP10_STABLE_DOM_PLOUGH_ACCUMULATOR_AUDIT.json`
2. `integration/animo-prep/PREP10_GNU_STABLE_DOM_OBSERVER_MATRIX.json`
3. `integration/animo-prep/PREP10_STABLE_DOM_CAUSAL_ACTIVATION_MATRIX.json`
4. `integration/animo-prep/PREP10_PARALLEL_CAUSAL_EVIDENCE_RECONCILIATION.json`
5. `integration/animo-prep/PREP10_STABLE_DOM_B3_HANDOFF.json`

PREP10C evidence:

1. `docs/prep10c/WORK_UNIT_CONTRACT.md`
2. `docs/prep10c/CANDIDATE_QUALIFICATION_REPORT.md`
3. `integration/animo-prep/PREP10C_EVENT_RESET_CANDIDATE.json`
4. `tools/make_prep10c_corrected_addit.py`
5. `tools/audit_prep10c_plough_conservation.py`
6. corresponding PREP10C unit tests and CI

B3 governance basis:

- `docs/governance/B3_SCIENTIFIC_ADMISSION_FRAMEWORK.md` on qualified B3Q01 head `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`
- `docs/governance/B3_QUALIFICATION_CLASSES.md`
- `integration/animo-b3/B3_DISPOSITION_SCHEMA.json`

## Questions that must be answered independently

### Atomicity and class

The reviewer must decide whether the proposed correction is genuinely one atomic Class B mechanism. In particular, confirm that it only initializes three event-local accumulators to the additive identity before the existing event summation and does not smuggle in a new state definition, solver policy, threshold, process order or unrelated ledger repair.

If the candidate is compound or changes another qualification class, mark review `FAIL_OR_RECLASSIFY`; do not broaden Class B to fit the implementation.

### Event-local scientific intent

Independently determine whether `SuStdiorma`, `SuStdiorni` and conditional `SuStdiorpo` are intended to represent current-plough-event totals rather than cumulative cross-event storage. Check the source-bound redistribution identity and relevant theory/documentation where available. PREP10/PREP10C author interpretation alone is insufficient.

### Conservation identity

Verify the control volume and algebra independently:

- `Bo(Pl)` is the cumulative thickness over redistributed layers;
- current-event mass is summed before redistribution;
- redistributed layer fractions sum to one;
- a retained `S_prior` is therefore counted again in a later event;
- zeroing the event-local accumulator removes stale prior-event mass without deleting current-event mass.

Reject the candidate if this identity is incomplete or if another intended storage term is omitted.

### Causal evidence

Confirm that authoritative PREP10 establishes, under the stated GNU diagnostic contract:

- source use-before-definition/missing reset;
- inter-event carryover when controlled stable pools are activated;
- C and N causal discrimination;
- conditional P causal discrimination in a phosphorus-enabled case;
- observer non-interference for compared outputs.

Keep controlled descendants classified as B1-style causal evidence, never B2 historical reference.

### Expected changed and unchanged surfaces

Review whether the declared expected-difference contract is sufficiently narrow. A passing frozen-testbank matrix is supporting non-interference evidence only. It cannot prove general harmlessness because the frozen successful plough cases are already non-discriminating for this defect.

### Historical route

Confirm that a provenance-qualified B2 historical-native result for the affected path is not currently established. Do not open `INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY` merely because the candidate is causal and conservative. That route is eligible only after the documented reasonable B2 acquisition effort is formally exhausted.

### Independence

The reviewer must state their identity or independent workunit identity, review scope, date/commit reviewed, and conflicts/overlap with candidate authoring. A review authored by the PREP10C correction work itself does not satisfy the gate.

## Allowed review outcomes

- `PASS_CLASS_B_AND_EVIDENCE_READY_FOR_ROUTE_EVALUATION`: class/atomicity/evidence are independently accepted, but B3 admission still depends on an eligible route and all mandatory B3 gates.
- `PASS_WITH_OPEN_EVIDENCE_REQUIREMENT`: basic candidate/class accepted but one or more explicitly listed evidence gates remain open.
- `FAIL_OR_RECLASSIFY`: candidate/class/identity/conservation/causality is not independently supported as stated.

None of these outcomes alone is corrected-legacy admission. A B3 disposition record must separately satisfy the canonical schema and route requirements before `admitted=true` is possible.

## Current open facts supplied to the reviewer

- B2 affected-path reference: not established.
- historical-uncertainty route: not opened.
- TCD-028: reserved in draft intake, canonical append not proven.
- candidate frozen-testbank current-GNU comparison: 8 completing cases, 550 common files, 0 scientific/structural differences after declared volatile-only normalization.
- GHGMais: return code 203 in baseline and candidate because of the pre-existing lineage/input-contract mismatch.
- candidate source and executable hashes match authoritative PREP10's event-reset counterfactual hashes.
- corrected legacy/B3/B4 admission: all false.
