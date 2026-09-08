# ANIMO-PREP10 — Restart and State-Continuity Audit

Status: `WORK_UNIT_RESERVED_SOURCE_BOUND_AND_DIAGNOSTIC_AUDIT_ONLY`.

## Purpose

Establish whether every restartable revision-53 ANIMO state has a coherent lifecycle across:

```text
input/restart read
-> accepted/start state
-> trial/result state
-> accepted-step commit
-> restart/output write
-> subsequent restart read
```

The workunit is evidence-first and does not modernize the legacy implementation.

## Parent

PREP09 qualified closeout:

`0ae0e2180cf0569f8ea22319aa9ccb54ebca3210`

Source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

## Audit scope

PREP10 will inventory and reconcile at least:

- persistent organic-matter and exudate stores;
- dissolved labile and stable C/N/P concentrations and sorbed states;
- NH4, NO3 and PO4 states;
- fast/slow/precipitated phosphorus stores;
- management/restart state required to continue a trajectory;
- GHG state where the source contract can be established without translating GHGMais;
- macropore state as source-bound only because the supplied testbank has no active macropore case;
- any state represented by accepted/result array pairs;
- initialization modes that canonicalize or transform restart representation.

## Questions

For each state family:

1. Is it read from an initial/restart file?
2. Is the read value actually used as the accepted/start state?
3. Is there a distinct result/trial state?
4. Where is result committed back to accepted state?
5. Is the committed state written by `Output_Init` or another restart writer?
6. Can the emitted restart representation be read back without loss of information or semantic reinterpretation?
7. Are option-dependent dimensions/site counts preserved?
8. Are any persistent solver/history states required but omitted from restart?

## Hard rules

- Frozen source and testbank bytes remain unchanged.
- A parser asymmetry is not automatically a scientific defect.
- Intentional canonicalization is distinguished from information loss.
- Zero-valued supplied states are not accepted as proof of continuity.
- Synthetic nonzero probes may be used only on execution copies and remain `DIAGNOSTIC_NOT_REFERENCE`.
- Historical reference qualification remains a separate PREP02 blocker.
- Production migration remains `NOT_ADMITTED`.

## Exit

A PREP10 source-bound qualification may be issued only when the state lifecycle inventory is machine-readable, audit tooling is tested, unresolved asymmetries are classified, and any promoted discrepancy is backed by causal or otherwise sufficient source-bound evidence.
