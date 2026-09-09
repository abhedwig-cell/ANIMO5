# ANIMO5 canonical integration DAG

Work unit: `ANIMO-RG02`

This DAG is an integration plan, not a scientific admission decision. No edge below means that a branch is safe to merge wholesale unless the edge explicitly says so.

## 1. Evidence and governance roots

```text
main
  |
  +--> PREP01-05 stabilized B0/B1 evidence anchor
  |      baseline/animo-prep01-05-evidence @ 9df84bd...
  |        |
  |        +--> PREP02R historical reference recovery [B2 gate, BLOCKED]
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

RG02 has now completed the governance-only convergence of those roles on its own branch. The EB01 evidence-model artifacts and EG01 retention/proof artifacts were transplanted with exact blob identity. The overlapping `DEVELOPMENT_GOVERNANCE.md` was manually composed under RG ownership, and the stale pre-EB01 `MIGRATION_DAG.md` terminology was replaced with the B0-B4 semantics. This did not merge EB01 or EG01 branches and did not alter scientific registers.

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

No PREP11 or PREP12 branch has yet been created. They must start from the governance-converged RG02 evidence base, not by renaming or merging the divergent source branches.

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

## 3. Theory, testing and numerical lines

```text
EB01
  |
  +--> TH01 revision-53 theory/provenance
  |      |
  |      +--> TH02 revision-4.1 lineage recovery
  |             |
  |             +--> GHG01 [in progress]
  |             +--> MP01 reservation [no own persisted work at RG02 snapshot]
  |
  +--> TQ01 testcase lineage and process coverage

PREP02R [B2 acquisition blocked]
  |
  +--> NQ01 numerical qualification architecture
          |
          +--> first real B1/B2 comparison only after provenance-qualified B2 receipt

PREP06
  |
  +--> TS01 temporal semantics [in progress]
```

TH01, TH02, TQ01 and NQ01 are mergeable only as evidence/governance artifacts after their bases are reconciled. Their branches must not drag an older copy of canonical registers over newer governance state.

NQ01 is qualified architecture for comparison and capture, not numerical equivalence. PREP02R remains the serial B2 gate.

## 4. B3 admission line

```text
PREP06 evidence + EB01 evidence semantics
             |
             v
          B3Q01 framework
           /   \
          /     \
     B3A01       TCD-028 intake
  readiness       reservation
       |               |
       +------- future per-TCD B3 dispositions -------+
                                                       |
                                                       v
                                      qualified scientific legacy baseline B3
                                      [NOT ESTABLISHED BY RG02]
```

B3Q01 owns B3 classification contracts and the qualified central discrepancy register. Its qualified register ends at `TCD-027` with blob `224acc350fde69d3c4aebed8628c0f945e0b3367`.

The observed later preparatory labels are governance-reconciled through RG02 local keys. They are not canonical IDs. In particular:

- local `TCD-028` on the transfer lineage is not central `TCD-028`;
- two different findings used local `TCD-030` on divergent branches;
- local `TCD-032` was used both by a restart branch and by a superseded PREP10C proposal;
- the PREP10 restart branch's statement that its local register tail was `TCD-031` is not a project-canonical register assertion.

The central B3 intake branch reserves `TCD-028` only for the stable-DOM plough accumulator event-reset finding. That reservation is not yet a canonical register append or B3 admission.

The RG02 branch itself still contains its inherited historical discrepancy-register file. That physical file is not promoted by RG02 into the canonical B3 register. Canonical TCD authority remains on B3Q01 until a later explicit register-convergence operation.

SQ01 is a separate scientific-qualification branch based on B3Q01. It may consume pinned theory and PREP evidence, but its results cannot be integrated into B3 until its own admission gates close.

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

This is a coherent sequential candidate-design chain. It is eligible for a separate architecture consolidation branch after an ARCHG work-unit contract is persisted. It is not eligible for production integration merely because its internal design checks pass.

The observed `work/animo-archg01-candidate-architecture-consolidation` ref was identical to ARCH07 and had no independent ARCHG01 status artifact at the RG02 authority snapshot. It therefore did not receive authority from its branch name.

Canonical architecture admission remains downstream of the evidence gates required by the migration policy. Candidate STATE, TIME, MASS and EX contracts remain unadmitted while B2/B3 and related scientific gates are unresolved.

## 6. Integration classes

### Governance-converged on RG02

- EB01 canonical B0-B4 evidence-model document and machine model;
- EG01 B0 retention policy, proof schemas, validator, tests, workflow and status;
- RG development governance and branch authority policy;
- RG-owned migration DAG using B0-B4 terminology.

This is G3 completion only. It does not make RG02 a B3 scientific register branch.

### Evidence-only until later admission

- PREP diagnostic and source-bound findings;
- GHG01, SQ01 and TS01 while in progress;
- B3A01 readiness artifacts;
- TCD-028 B3 intake reservation;
- all ARCH01 to ARCH07 candidate designs.

### Path-level transplant only

- PREP07 species-identity supplemental evidence;
- PREP08 transfer-probes supplemental evidence;
- PREP09 option-contract evidence, rehomed as PREP11;
- PREP10 restart/state-continuity evidence, rehomed as PREP12;
- any useful material from PREP10C superseded branches not already represented in the re-anchored PREP10C branch.

These source branches must not be imported wholesale. Preserve source branch, head and blob provenance. Do not import same-name work-unit status files or divergent `THEORY_CODE_DISCREPANCY_REGISTER.csv` files.

### Never merge as branches

- EB01 copy/pr/review aliases;
- NQ01 `final`, `ignore`, `copy`, `packet-temp`, `stop` aliases;
- TQ01 shadow, shadow2 and shadow3;
- TH02 release-lineage-recovery no-op alias;
- PREP08 restart-state-continuity reservation under the reused identifier;
- PREP10 stable-DOM causal branch as a competing PREP10 line, because its evidence is already reconciled by authoritative PREP10;
- PREP10C old candidate and reset-readiness branches as PREP10C integration lines.

Their historical commits remain evidence where relevant. `NEVER_MERGE` does not mean delete evidence.

## 7. Required convergence gates

The dependency order was corrected after RG02 found that PREP11/PREP12 cannot safely be instantiated before a governance-approved integration base exists.

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
G5  theory + TQ + NQ + temporal/science evidence attached as independent streams
 |
G6  B2 acquisition and comparison gate, if historical reference becomes available
 |
G7  per-discrepancy B3 qualification and admission
 |
G8  candidate architecture qualification against admitted scientific baseline
 |
G9  B4 canonical ANIMO5 baseline admission
 |
G10 production migration
```

Current RG02 state:

- G0: `SUBSTANTIALLY_COMPLETE`;
- G1: `COMPLETE_FOR_OBSERVED_POST_027_PREPARATORY_LINEAGES`;
- G3: `COMPLETE_GOVERNANCE_ONLY`;
- G2: `PLANNED_NOT_EXECUTED`;
- G4: `NOT_READY`;
- G6: independently blocked by PREP02R;
- G7 onward: not admitted.

G1 completion assigns no new canonical TCD number. G3 completion admits no scientific baseline. Both are repository-governance gates only.

## 8. Immediate safe actions after the current checkpoint

The next safe work is G2:

- create PREP11 and PREP12 only from the governance-converged RG02 base;
- execute the PREP07 and PREP08 supplemental packet rehomes path-by-path;
- transplant only the include-listed PREP11/PREP12 evidence paths;
- preserve source branch/head/blob identity for every transplant;
- validate that no old PREP07/PREP08/PREP09/PREP10 status, work-unit contract or local TCD register entered the new authoritative/rehome surfaces;
- keep PREP02R acquisition and NQ01 comparison readiness independent;
- keep B3 admission and canonical TCD allocation separate from branch convergence.

No branch merge was performed by RG02.

`scientific_baseline_changed=false`

`corrected_legacy_admitted=false`

`production_migration_admitted=false`
