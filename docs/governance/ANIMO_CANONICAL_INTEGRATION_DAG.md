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

EB01 and RG01 are not substitutes for each other. EB01 owns evidence semantics. RG01/RG02 own repository convergence and integration policy. EG01 owns controlled B0 retention. A future governance consolidation must transplant these disjoint governance artifacts onto one integration branch without replacing their source authority.

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

Two substantive reused work-unit lines have now been given non-colliding RG02 reservations for rehome only:

```text
work/animo-prep09-option-contract-audit
    -> ANIMO-PREP11 [RG02_RESERVED_NOT_STARTED]

work/animo-prep10-restart-state-continuity
    -> ANIMO-PREP12 [RG02_RESERVED_NOT_STARTED]
```

No PREP11 or PREP12 branch has been created by RG02. The reservations exist so a later path-level transplant cannot silently create another PREP09/PREP10 authority.

### Required preparatory consolidation

Before a single preparatory evidence branch can be produced:

1. Freeze the authoritative PREP06 snapshot.
2. Rehome unique PREP07 species-identity evidence as supplemental packet `RG02-SUPP-P07-SPECIES-001`, without its conflicting PREP07 status/contract ownership.
3. Rehome unique PREP08 transfer-probe evidence as supplemental packet `RG02-SUPP-P08-TRANSFER-001`, without its local TCD register or PREP08 status.
4. Rehome PREP09 option-contract evidence as `ANIMO-PREP11`; do not import the old PREP09 status or local `TCD-030` identity.
5. Rehome PREP10 restart evidence as `ANIMO-PREP12`; do not import the old PREP10 contract, local `TCD-032/033/034` reservation file or divergent TCD register.
6. Use `integration/animo-reg/ANIMO_LOCAL_TCD_RECONCILIATION.json` for all post-027 local finding identity until B3 governance allocates canonical IDs.
7. Only then construct a canonical preparatory evidence aggregate.

The exact path-level include/exclude plan is persisted in `integration/animo-reg/ANIMO_SUPPLEMENTAL_EVIDENCE_TRANSPLANT_PLAN.json`.

This is a consolidation operation, not a scientific requalification. Existing findings retain their original evidence class and source branch.

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

TH01, TH02, TQ01 and NQ01 are mergeable only as evidence/governance artifacts after their bases are reconciled. Their branches must not be used to drag an older copy of canonical registers over newer governance state.

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

B3Q01 is the owner of B3 classification contracts and the qualified central discrepancy register. Its qualified register ends at `TCD-027` with blob `224acc350fde69d3c4aebed8628c0f945e0b3367`.

The observed later preparatory labels are now governance-reconciled through RG02 local keys. They are not canonical IDs. In particular:

- local `TCD-028` on the transfer lineage is not central `TCD-028`;
- two different findings used local `TCD-030` on divergent branches;
- local `TCD-032` was used both by a restart branch and by a superseded PREP10C proposal;
- the PREP10 restart branch's statement that its local register tail was `TCD-031` is not a project-canonical register assertion.

The central B3 intake branch still reserves `TCD-028` only for the stable-DOM plough accumulator event-reset finding, and that reservation is not yet a canonical register append or B3 admission.

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

The observed `work/animo-archg01-candidate-architecture-consolidation` ref is currently identical to ARCH07 and had no independent ARCHG01 status artifact at the RG02 authority snapshot. It therefore did not receive authority from its branch name.

Canonical architecture admission remains downstream of the evidence gates required by the existing migration policy. In particular, candidate STATE, TIME, MASS and EX contracts remain unadmitted while B2/B3 and related scientific gates are unresolved.

## 6. Integration classes

### Mergeable after governance-only rebase or transplant

- EB01 governance documents
- EG01 controlled-retention governance
- RG02 authority model and registers
- TH/TQ/NQ documentation and machine evidence that do not overwrite canonical registers
- ARCH candidate-design artifacts in their own namespaces

"Mergeable" here means semantically mergeable after base reconciliation. It does not authorize a direct branch merge.

### Evidence-only until later admission

- PREP diagnostic and source-bound findings
- GHG01, SQ01 and TS01 while in progress
- B3A01 readiness artifacts
- TCD-028 B3 intake reservation
- all ARCH01 to ARCH07 candidate designs

### Path-level transplant only

- PREP07 species-identity supplemental evidence
- PREP08 transfer-probes supplemental evidence
- PREP09 option-contract evidence, rehomed as PREP11
- PREP10 restart/state-continuity evidence, rehomed as PREP12
- any useful material from PREP10C superseded branches that is not already present in the re-anchored PREP10C branch

These commits must not be imported wholesale. Use the RG02 path-level include/exclude plan and preserve source blob provenance. Do not import same-name work-unit status files or a divergent `THEORY_CODE_DISCREPANCY_REGISTER.csv`.

### Never merge as branches

- EB01 copy/pr/review aliases
- NQ01 `final`, `ignore`, `copy`, `packet-temp`, `stop` aliases
- TQ01 shadow, shadow2 and shadow3
- TH02 release-lineage-recovery no-op alias
- PREP08 restart-state-continuity reservation under the reused identifier
- PREP10 stable-DOM causal branch as a competing PREP10 line, because its evidence is already reconciled by authoritative PREP10
- PREP10C old candidate and reset-readiness branches as PREP10C integration lines

Their historical commits remain evidence where relevant. `NEVER_MERGE` does not mean delete evidence.

## 7. Required convergence gates

```text
G0  RG02 branch authority register complete
 |
G1  canonical TCD/local-ID reconciliation complete
 |
G2  duplicate PREP07-10 evidence transplanted under unique packet/workunit identities
 |
G3  governance artifacts consolidated: RG + EB + EG
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
- G2: `PLANNED_NOT_EXECUTED`;
- G3: `PLANNED_NOT_EXECUTED`;
- G4: `NOT_READY`;
- G6: independently blocked by PREP02R;
- G7 onward: not admitted.

G1 completion does not assign any new canonical TCD number. It only makes the local identity collisions explicit and machine-readable.

## 8. Immediate safe actions after the current checkpoint

The next safe integration work remains governance/evidence-only:

- execute the two supplemental packet rehomes path-by-path;
- instantiate PREP11 and PREP12 from a governance-approved canonical evidence base rather than from their divergent source branch heads;
- preserve source branch/head/blob provenance for every transplanted artifact;
- validate that no old PREP07/PREP08/PREP09/PREP10 status or local TCD register entered the rehome branches;
- consolidate RG, EB and EG governance only after G2 readback passes;
- keep PREP02R acquisition and NQ01 comparison readiness independent;
- keep B3 admissions separate from branch convergence.

No merge was performed by RG02.

`scientific_baseline_changed=false`

`corrected_legacy_admitted=false`

`production_migration_admitted=false`
