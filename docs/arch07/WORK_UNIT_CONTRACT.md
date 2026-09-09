# ANIMO-ARCH07 — External Adapter Qualification Test Specification

Status: `CANDIDATE_QUALIFICATION_SPECIFICATION_ONLY`.

## Purpose

Translate the ARCH05 external hydrology/crop exchange contracts and ARCH06 normalized configuration identities into an executable, fail-closed adapter qualification test specification.

ARCH07 defines **what a future concrete adapter must prove**. It does not implement or qualify a SWAP, WOFOST or other runtime adapter.

## Starting point

ARCH07 starts exactly from ANIMO-ARCH06 head `ce3ea8089902dbc4bcbe3ff0224d30c2f8daf3a4` and decision `QUALIFIED_CANDIDATE_NORMALIZED_MODEL_CONFIGURATION_AND_IDENTITY_ARCHITECTURE`.

The final-head ARCH06 CI retest may still be queued because of repository-wide Actions backlog. The architecture registries and golden vectors themselves passed checkout CI at head `901cf8bb2c7e63d8c6d8f2531526624c61cec5aa`; the later ARCH06 commits added evidence/status only.

## In scope

- conformance tests for all 42 ARCH05 exchange fields;
- qualification coverage for all 18 ARCH05 transaction rules;
- hydrology field presence, conditional presence, units, shape, sign, geometry and generation checks;
- external crop ownership, demand/result, state-observation and explicit event-bundle checks;
- immutable-frame and stale-frame rejection cases;
- ARCH06 feature/layout/exchange/configuration identity mismatch cases;
- reject, retry and logical coupled commit-barrier test requirements;
- MassLedger/typed-event linkage requirements where ARCH03/ARCH05 already define them;
- explicit future split-run and coupled rollback behavioural test specifications;
- blocked macropore extension tests under TCD-025;
- machine-readable exact field/rule coverage and a structural audit.

## Out of scope

- production adapter implementation;
- canonical EX admission;
- generic TIME acceptance, retry cadence, substep or convergence policy;
- numerical tolerance definition;
- scientific parameter defaults or calibration;
- correction of TCD-018 or TCD-025;
- active macropore qualification;
- reference equivalence claims;
- legacy source or testcase changes.

## Qualification boundary

Passing the ARCH07 structural audit qualifies only the **test specification**.

A future adapter can be called qualified only after the relevant runtime-required cases have been executed against an admitted adapter implementation and their required evidence has been persisted. Cases that require historical/reference or scientific admission remain blocked even if runtime conformance passes.

## Hard rules

1. Every ARCH05 exchange field must map to at least one positive or negative qualification case and to generic unit/shape/conditional-presence validation.
2. Every ARCH05 transaction rule must map to at least one explicit qualification case.
3. Invalid unit, shape, geometry, layout, schema, configuration or accepted-generation bindings fail closed.
4. Adapter-specific sign conventions must be normalized at the adapter boundary and must not leak into ANIMO kernel semantics.
5. Exchange frames are immutable under their IDs.
6. Rejected trials contribute no physical state commit and no committed physical ledger events.
7. External crop persistent state remains externally owned.
8. Realized crop uptake results must be linked to typed transfer events; residue/export semantics cannot be inferred from crop-state deltas.
9. Diagnostics may observe transactions but cannot become physical coupling state.
10. Macropore fields remain a blocked extension until an admission identity and active qualification evidence exist.
11. No arbitrary floating-point tolerance may be invented by this workunit.
12. Structural specification PASS must never be reported as adapter or scientific qualification.

## Maximum decision

`QUALIFIED_CANDIDATE_EXTERNAL_ADAPTER_QUALIFICATION_TEST_SPECIFICATION`
