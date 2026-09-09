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
  |      |      |
  |      |      +--> PREP09 option-contract-audit [SUPPLEMENTAL, renumber before integration]
  |      |
  |      +--> PREP08 transfer-probes [SUPPLEMENTAL]
  |             |
  |             +--> PREP09 element-transfer-and-slow-sorption [AUTHORITATIVE PREP09]
  |                    |
  |                    +--> PREP10 stable-dom-plough-accumulators [AUTHORITATIVE PREP10]
  |                           |
  |                           +--> PREP10C re-anchored event-reset [AUTHORITATIVE PREP10C review]
  |                           |
  |                           +--> B3 TCD-028 intake [reservation only]
  |
  +--> PREP07 transfer-species-identity [SUPPLEMENTAL, divergent]
         |
         +--> PREP08 restart-state-continuity [SUPERSEDED reservation]
```

A second PREP10 branch, `work/animo-prep10-restart-state-continuity`, contains unique evidence but reused the PREP10 identifier. It is outside the authoritative PREP10 lineage and must be transplanted into a newly numbered evidence work unit before canonical integration.

### Required preparatory consolidation

Before a single preparatory evidence branch can be produced:

1. Freeze the authoritative PREP06 snapshot.
2. Transplant unique PREP07 species-identity evidence into a new supplemental evidence packet without its conflicting PREP07 status file.
3. Transplant unique PREP08 transfer-probe evidence without importing its local post-027 TCD numbers as canonical IDs.
4. Transplant PREP09 option-contract evidence under a new work-unit identifier.
5. Transplant PREP10 restart evidence under a new work-unit identifier.
6. Reconcile every local post-027 TCD label through the B3-owned ID map.
7. Only then construct a canonical preparatory evidence aggregate.

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

B3Q01 is the owner of B3 classification contracts. Canonical TCD allocation from 028 onward is controlled by the B3 governance line. Preparatory local IDs are input to reconciliation, not direct register entries.

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

The observed `work/animo-archg01-candidate-architecture-consolidation` ref is currently identical to ARCH07 and has no independent ARCHG01 status artifact. It is therefore only a reservation at this RG02 snapshot.

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

### Cherry-pick or transplant only

- PREP07 species-identity supplemental evidence
- PREP08 transfer-probes supplemental evidence
- PREP09 option-contract evidence
- PREP10 restart/state-continuity evidence
- any useful material from PREP10C superseded branches that is not already present in the re-anchored PREP10C branch

These commits must be selected path-by-path. Do not import same-name work-unit status files or a divergent `THEORY_CODE_DISCREPANCY_REGISTER.csv`.

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
G2  duplicate PREP07-10 evidence transplanted under unique identifiers
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

At the RG02 snapshot, G0 is substantially complete as repository governance, but G1 and G2 are blocked by unresolved local-ID and duplicate-lineage content mapping. G6 and G7 are also independently blocked or incomplete. Therefore no direct canonical merge is authorized.

## 8. Immediate safe actions after RG02

The next safe integration work is governance-only:

- create a canonical local-ID reconciliation ledger for all post-027 preparatory TCD labels;
- assign new work-unit identifiers to PREP09 option-contract and PREP10 restart evidence before transplant;
- persist an ARCHG01 contract before using the existing ARCHG01 ref as an architecture consolidation surface;
- keep PREP02R acquisition and NQ01 comparison readiness independent;
- keep B3 admissions separate from branch convergence.

No merge was performed by RG02.

`scientific_baseline_changed=false`

`corrected_legacy_admitted=false`

`production_migration_admitted=false`
