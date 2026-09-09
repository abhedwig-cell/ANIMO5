# Initial ANIMO5 migration dependency DAG

This is a first dependency map, not an authorization to start production migration.

```mermaid
flowchart TD
    P1[PREP01 evidence and governance baseline]
    S0[Authoritative source ingest and freeze]
    D0[Authoritative documentation ingest and freeze]
    T0[Testbank freeze and provenance]
    B0[Reproducible legacy build]
    TA[Compiler and interface audit]
    IO[I/O and dataflow audit]
    TC[Testcase execution and capture]
    TH[Theory-code discrepancy analysis]
    CR[Corrected legacy reference]
    QM[Qualified migration baseline]
    STATE[Canonical state/data ownership]
    TIME[Generic time and transaction contract]
    MASS[Mass accounting contract]
    EX[SWAP/WOFOST exchange contracts]
    PROC[Process migrations on admitted contracts]
    INT[Integrated qualification]
    A[Status A]
    AA[Status AA maturation]

    P1 --> S0
    P1 --> D0
    P1 --> T0
    S0 --> B0
    S0 --> TA
    S0 --> IO
    T0 --> TC
    B0 --> TC
    D0 --> TH
    S0 --> TH
    TC --> TH
    TH --> CR
    CR --> QM
    QM --> STATE
    STATE --> TIME
    TIME --> MASS
    MASS --> EX
    EX --> PROC
    PROC --> INT
    INT --> A
    A --> AA
```

## Parallel candidates after missing evidence is ingested

- documentation inventory/reconciliation preparation;
- compiler/interface audit tooling;
- testcase harness development;
- process/dataflow inventory;
- Status A/AA gap analysis.

## Serial shared-semantic gates

- source freeze before behavioural correction;
- corrected reference before migration qualification;
- canonical state ownership before broad process migration;
- time/transaction semantics before coupled trial execution;
- mass accounting before coupled qualification;
- shared exchange interfaces before SWAP/WOFOST integration.
