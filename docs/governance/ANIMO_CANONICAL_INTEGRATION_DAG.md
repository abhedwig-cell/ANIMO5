# ANIMO5 canonical integration DAG

Work units: `ANIMO-RG02`, reconciled by `ANIMO-GOV02`

This DAG is an integration plan, not a scientific admission decision. No edge below means that a branch is safe to merge wholesale unless the edge explicitly says so.

## GOV02 scope reconciliation

RG02 originally rendered G6 before G7 and described PREP02R as a serial B2 gate. GOV02 narrows that statement to its intended claim scope.

- G6 remains the serial historical-fidelity B2 acquisition/comparison gate.
- A `HISTORICAL_FIDELITY_CLAIM`, historical Intel/runtime equivalence claim, historical-output acceptance oracle, or representation-equivalence claim against historical behaviour remains blocked until a qualified B2 reference exists for the relevant scope.
- G7 remains process-scoped B3 qualification. A non-historical scientific claim may only reach G7 without B2 through `INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY`, and only after PREP02R has genuinely reached `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT` plus the stricter B3Q01/GOV02 scientific-evidence contract.
- Such a no-B2 scientific disposition does not mark G6 passed. It must carry `historical_behaviour_status=UNKNOWN` into composition, B4 records and release claims.
- Whole-model historical equivalence remains B2-dependent.

At the GOV02 authority snapshot PREP02R still records `external_request_sent=false`. Its current policy state is therefore `B2_ACQUISITION_STILL_ACTIVE`; the historical-uncertainty route is not currently eligible.

The detailed policy is in `ANIMO5_EVIDENCE_DAG_RECONCILIATION.md`, `B2_REQUIREMENT_SCOPE.md`, `HISTORICAL_UNCERTAINTY_ADMISSION_POLICY.md` and `PREP02R_BOUNDED_ACQUISITION_CLOSURE.md`.

## 1. Evidence and governance roots

```text
main
  |
  +--> PREP01-05 stabilized B0/B1 evidence anchor
  |      baseline/animo-prep01-05-evidence @ 9df84bd...
  |        |
  |        +--> PREP02R historical reference recovery [B2 historical-fidelity gate, BLOCKED]
  |        |
  |        +--> PREP06 conserved state and transfer ledger [qualified preparatory evidence]
  |        |
  |        +--> EB01 B0-B4 evidence semantics [canonical governance semantics]
  |
  +--> RG01 stabilized preparatory governance anchor
         baseline/animo-rg01-preparatory-stabilized @ 662bca8...
           |
           +--> EG01 controlled B0 retention
           |
           +--> RG02 branch authority and integration governance
```

EB01 and RG01 are not substitutes for each other. EB01 owns evidence semantics. RG01/RG02 own repository convergence and integration policy. EG01 owns controlled B0 retention.

RG02 completed the governance-only convergence of those roles on its own branch. The EB01 evidence-model artifacts and EG01 retention/proof artifacts were transplanted with exact blob identity. The overlapping `DEVELOPMENT_GOVERNANCE.md` was manually composed under RG ownership, and the stale pre-EB01 `MIGRATION_DAG.md` terminology was replaced with the B0-B4 semantics. This did not merge EB01 or EG01 branches and did not alter scientific registers.

GOV02 further reconciles the evidence dependencies without changing the B0-B4 meanings owned by EB01.

## 2. Preparatory evidence convergence

```text
PREP06
  |
  +--> PREP07 transfer-edge-audit [AUTHORITATIVE PREP07]
  |      |
  |      +--> PREP08 causal-management-probes [AUTHORITATIVE PREP08]
  |      |
  |      +--> PREP08 transfer-probes [SUPPLEMENTAL PACKET]
  |             |
  |             +--> PREP09 element-transfer-and-slow-sorption [AUTHORITATIVE PREP09]
  |                    |
  |                    +--> PREP10 stable-dom-plough-accumulators [AUTHORITATIVE PREP10]
  |                           |
  |                           +--> PREP10C re-anchored event-reset [AUTHORITATIVE PREP10C review]
  |                           |
  |                           +--> B3 TCD-028 intake [reservation only]
  |
  +--> PREP07 transfer-species-identity [SUPPLEMENTAL PACKET, divergent]
```

Two substantive reused work-unit lines have non-colliding RG02 reservations for rehome only:

```text
work/animo-prep09-option-contract-audit
    -> ANIMO-PREP11 [RG02_RESERVED_NOT_STARTED]

work/animo-prep10-restart-state-continuity
    -> ANIMO-PREP12 [RG02_RESERVED_NOT_STARTED]
```

No PREP11 or PREP12 branch had been created at the RG02 snapshot. They must start from the governance-converged RG02 evidence base, not by renaming or merging the divergent source branches.

### Required preparatory consolidation

Before a single preparatory evidence aggregate can be produced:

1. Use the RG02 governance-converged branch as the integration-policy base.
2. Rehome unique PREP07 species-identity evidence as supplemental packet `RG02-SUPP-P07-SPECIES-001`, without its conflicting PREP07 status/contract ownership.
3. Rehome unique PREP08 transfer-probe evidence as supplemental packet `RG02-SUPP-P08-TRANSFER-001`, without its local TCD register or PREP08 status.
4. Rehome PREP09 option-contract evidence as `ANIMO-PREP11`; do not import the old PREP09 status or local `TCD-030` identity as canonical.
5. Rehome PREP10 restart evidence as `ANIMO-PREP12`; do not import the old PREP10 contract, local `TCD-032/033/034` reservation file or divergent TCD register.
6. Use `integration/animo-reg/ANIMO_LOCAL_TCD_RECONCILIATION.json` for all post-027 local finding identities until B3 governance allocates canonical IDs.
7. Only after readback verification of those rehomes construct a canonical preparatory evidence aggregate.

The exact include/exclude plan is persisted in `integration/animo-reg/ANIMO_SUPPLEMENTAL_EVIDENCE_TRANSPLANT_PLAN.json`.

This is evidence convergence, not scientific requalification. Existing findings retain their original evidence class and source provenance.

## 3. Theory, testing, synthetic-oracle and numerical lines

```text
EB01
  |
  +--> TH01 revision-53 theory/provenance
  |      |
  |      +--> TH02 revision-4.1 lineage recovery
  |             |
  |             +--> GHG01
  |             +--> MP01/MP02 feature qualification
  |
  +--> TQ01 testcase lineage and process coverage
  |
  +--> SYNQ01 independent synthetic-oracle layer

PREP02R [B2 historical-reference acquisition]
  |
  +--> historical fidelity evidence when a reference is recovered and qualified

PREP06
  |
  +--> NQ01/NQ02 numerical qualification evidence
  +--> TS01 temporal source-semantics evidence
  +--> SQ01 scientific-state qualification evidence
```

These streams are independent evidence contributors. Source semantics, theory, conservation identities, analytical oracles, synthetic causal tests, metamorphic tests, independent numerical/high-precision calculations and empirical validation where applicable may support scientific B3 qualification. None is promoted to B2 merely because it is independent scientific evidence.

NQ01/NQ02 provide numerical qualification evidence, not historical equivalence. TQ01 provides lineage/path coverage evidence, not a universal reference. TS01 provides source-bound temporal semantics, not a historical runtime oracle. SYNQ01's oracle taxonomy is scientific evidence taxonomy and synthetic evidence remains non-B2.

## 4. B3 admission line

```text
PREP evidence + EB01 semantics + theory/scientific-oracle evidence + B1 causality
             |                                      |
             |                                      +--> relevant B2, when available/required
             |                                      |
             |                                      +--> strict historical-uncertainty route only after bounded B2 acquisition closure
             v
          B3Q01 framework
           /   \
          /     \
     B3A01       TCD-028 intake
  readiness       reservation
       |               |
       +------- future atomic per-TCD/process B3 dispositions -------+
                                                                     |
                                                                     v
                                               qualified scientific legacy B3 scopes
                                               [NO GLOBAL B3 BASELINE ESTABLISHED]
```

B3Q01 owns B3 classification contracts and the qualified central discrepancy register. At the RG02 snapshot its qualified register ended at `TCD-027` with blob `224acc350fde69d3c4aebed8628c0f945e0b3367`.

The observed later preparatory labels are governance-reconciled through RG02 local keys. They are not canonical IDs. In particular:

- local `TCD-028` on the transfer lineage is not central `TCD-028`;
- two different findings used local `TCD-030` on divergent branches;
- local `TCD-032` was used both by a restart branch and by a superseded PREP10C proposal;
- the PREP10 restart branch's statement that its local register tail was `TCD-031` is not a project-canonical register assertion.

The central B3 intake branch reserves `TCD-028` only for the stable-DOM plough accumulator event-reset finding. That reservation is not a canonical register append or B3 admission.

The RG02 branch itself still contains its inherited historical discrepancy-register file. That physical file is not promoted by RG02 into the canonical B3 register. Canonical TCD authority remains on B3Q01 until a later explicit register-convergence operation.

B3A01 is admission-readiness evidence only and remains blocked. GOV02 does not change that status or admit TCD-027.

## 5. Candidate architecture line

```text
PREP06
  |
  +--> ARCH01 state ownership and typed transfers
         |
         +--> ARCH02 restart/checkpoint sufficiency
                |
                +--> ARCH03 mass-ledger observer
                       |
                       +--> ARCH04 feature activation/state allocation
                              |
                              +--> ARCH05 external exchange contracts
                                     |
                                     +--> ARCH06 normalized configuration
                                            |
                                            +--> ARCH07 adapter qualification spec
```

This is a coherent candidate-design chain. It is not eligible for production integration merely because internal design checks pass.

Canonical architecture admission remains downstream of the exact admitted B3 process contracts and their uncertainty provenance. Candidate STATE, TIME, MASS and EX contracts do not gain admission from GOV02.

## 6. Integration classes

### Governance-converged

- EB01 canonical B0-B4 evidence-model semantics;
- EG01 B0 retention policy and proof artifacts;
- RG development governance and branch authority policy;
- RG-owned migration DAG;
- GOV02 process-scoped B2 requirement, bounded acquisition closure, historical-uncertainty policy and evidence DAG.

This is governance qualification only. It does not create a scientific baseline.

### Evidence-only until later admission

- PREP diagnostic and source-bound findings;
- GHG, MP, SQ and TS findings outside an admitted B3 disposition;
- SYNQ01 scientific-oracle artifacts until individually qualified and bound to a claim;
- B3A01 readiness artifacts;
- TCD-028 B3 intake reservation;
- NQ numerical-policy evidence outside an admitted Class E disposition;
- all candidate architecture designs.

### Path-level transplant only

- PREP07 species-identity supplemental evidence;
- PREP08 transfer-probes supplemental evidence;
- PREP09 option-contract evidence, rehomed as PREP11;
- PREP10 restart/state-continuity evidence, rehomed as PREP12;
- useful material from superseded PREP10C branches not already represented in the re-anchored PREP10C branch.

These source branches must not be imported wholesale. Preserve source branch, head and blob provenance. Do not import same-name work-unit status files or divergent `THEORY_CODE_DISCREPANCY_REGISTER.csv` files.

### Never merge as branches

The RG02 `NEVER_MERGE` decisions for duplicate aliases and divergent reused work-unit lines remain in force. Their historical commits remain evidence where relevant. `NEVER_MERGE` does not mean delete evidence.

## 7. Required convergence gates

GOV02 preserves gate numbers but reconciles G6/G7 semantics so the DAG is claim-scoped rather than globally linear.

```text
G0  RG02 branch authority register substantially complete
 |
G1  local post-TCD027 identity reconciliation complete
 |
G3  RG + EB + EG governance artifacts consolidated
 |
G2  duplicate PREP07-10 evidence transplanted under unique packet/workunit identities
 |
G4  preparatory evidence aggregate assembled without register collisions
 |
G5  theory + TQ + NQ + temporal/science/synthetic-oracle evidence attached as independent streams
 |\
 | +--> G6H  B2 historical-fidelity acquisition/comparison gate
 |            required for historical-fidelity/historical-equivalence claims
 |
 +----> G6U  bounded B2 acquisition closure gate
              only `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`
              can open the strict historical-uncertainty scientific route
               \        /
                \      /
                 v    v
G7  atomic per-process/per-discrepancy B3 scientific qualification and admission
    using the evidence route required by the declared claim type
 |
G8  candidate architecture qualification against admitted B3 scopes plus uncertainty provenance
 |
G9  B4 canonical ANIMO5 baseline admission with inherited uncertainty provenance
 |
G10 production migration
```

`G6H` and `G6U` are scope labels inside the existing G6 governance area, not new release-stage numbers. They make explicit that failure to obtain B2 is not itself a pass condition.

Rules:

1. `HISTORICAL_FIDELITY_CLAIM` always requires G6H/B2.
2. A scientific correction claim without B2 can only enter G7 after G6U has actually reached the unavailable-after-reasonable-effort closure and all stricter independent-science requirements pass.
3. A no-B2 scientific B3 disposition leaves G6H unresolved and carries historical uncertainty permanently.
4. Whole-model historical equivalence cannot be composed from scientifically admitted no-B2 process claims.
5. G8 and G9 inherit historical uncertainty; they cannot upgrade it by composition.

Current state at GOV02 closeout:

- G0: `SUBSTANTIALLY_COMPLETE`;
- G1: `COMPLETE_FOR_OBSERVED_POST_027_PREPARATORY_LINEAGES`;
- G3: `COMPLETE_GOVERNANCE_ONLY`;
- G2/G4/G5: retain their RG02/latest-stream statuses outside GOV02's admission scope;
- G6H: `BLOCKED_NO_QUALIFIED_B2_REFERENCE`;
- G6U: `B2_ACQUISITION_STILL_ACTIVE`, because the prepared PREP02R institutional request is still recorded as unsent;
- G7: no new scientific admissions by GOV02;
- G8 onward: not admitted by GOV02.

GOV02 assigns no new canonical TCD number and establishes no global B3 baseline.

## 8. Immediate safe actions

- keep PREP02R acquisition active and execute the prepared institutional request through a verified WUR route before considering an exhaustion state;
- continue independent scientific qualification streams without representing them as B2;
- require future B3 records to declare claim type, route and historical-reference status atomically;
- bind future individually qualified SYNQ01 oracle artifacts to scoped claims without changing their evidence class;
- preserve historical uncertainty through architecture and migration records;
- if B2 is later recovered, open a new historical-fidelity comparison for any affected B3 scope rather than retroactively rewriting its original scientific disposition.

No production source or scientific register is modified by GOV02.

`B2_devalued=false`

`synthetic_evidence_promoted_to_B2=false`

`new_TCD_admissions=false`

`B3_global_baseline_established=false`

`B4_admitted=false`

`production_migration_admitted=false`
