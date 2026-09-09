# TCD-017 independent second-line review handoff

Work unit: `ANIMO-B3A02`

Target: `TCD-017`

Class: `A_ACCOUNTING_REPORTING_ONLY`

This file prepares, but does not perform, the independent second-line review required by B3Q01. The authoring context of ANIMO-B3A02 must not count itself as the independent reviewer.

## Review request

A dedicated GitHub review request is now open:

Issue `#25`:

`ANIMO-B3A02R — Independent second-line review of TCD-017 Class-A readiness`

That issue is a coordination object only. Opening it does not satisfy the independent-review gate. The actual reviewer must work in a separate workunit/context and persist independent review evidence.

## Frozen review object

Review the admission-readiness dossier as frozen at commit:

`3ff8f4bda77c631b82110b83317c6a9b42b867ad`

That commit contains the four required ANIMO-B3A02 deliverables and no ANIMO source patch.

Primary review files:

- `docs/b3/TCD017_CLASS_A_ADMISSION_READINESS.md`
- `integration/animo-b3/TCD017_EXPECTED_DIFFERENCE.json`
- `integration/animo-b3/TCD017_CLASS_A_READINESS.json`
- `integration/animo-b3/ANIMO-B3A02_STATUS.json`

Frozen B0 identities:

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

## Atomic claim to review

The review is restricted to the following claim:

1. `Addiorpotoppl(I)` is the already-computed negative top-reservoir dissolved-organic-P loss during ploughing.
2. `Addiorpopl(I,Ln)` is the already-computed net layer dissolved-organic-P redistribution.
3. The physical top-plus-layer redistribution is already conservative for the TCD-017 control volume.
4. `Outbal_calc.for` records the layer term in `Bapo(Redi,Ly)` but omits the top-reservoir term.
5. The candidate correction is exactly:

```fortran
Bapo(Redi,Ly) = Bapo(Redi,Ly) + Addiorpotoppl(I)*Z
```

6. That candidate is accounting/reporting only and must not change physical state, process fluxes, management continuation, transport, hydrology, or total physical P.

The reviewer must not broaden the claim to other organic-P findings.

## Evidence to cross-check independently

The second-line review should verify the following against the cited immutable evidence rather than accepting the B3A02 prose at face value:

- PREP01 causal evidence for the top-reservoir omission and natural LWKM activation;
- PREP02 top-term-only Class-A non-interference evidence only;
- PREP06 `PLOUGH-DOM` internal-transfer ownership;
- B3Q01 Class-A and fail-closed admission contract;
- GOV02 claim-scoped B2 route policy;
- SYNQ01 `SYNQ-O002` closed redistribution oracle.

In particular, re-check the source-level write set and confirm that the proposed statement consumes an existing accounting value without writing any physical state or process-flux surface.

## Required review questions

A passing second-line readiness review must answer yes to all of these questions:

1. Is the source/destination ownership interpretation correct for the exact frozen B0 source?
2. Is the `Bapo` omission demonstrated directly, not inferred only from a lower residual?
3. Does natural LWKM exercise the relevant top-reservoir ploughing path?
4. Does the encompassing TCD-017 control volume close before any reporting correction?
5. Is the proposed change exactly one ledger addition with no physical-state or flux write path?
6. Is the expected-difference whitelist complete and fail-closed?
7. Are `TCD-027`, `TCD-028`, `AdStdiorpopl`, `Adhuexpopl`, `Bafop`, and any physical or numerical organic-P changes excluded?
8. Is SYNQ-O002 used only as an independent conservation oracle and not as B2 historical evidence?
9. Is the route gate still treated independently from scientific readiness?
10. Does the review avoid admitting corrected legacy behaviour while the route gate remains unsatisfied?

Any negative or unresolved answer fails the second-line review.

## Live route state at handoff refresh

The latest checked PREP02R branch is:

`work/animo-prep02r-historical-reference-recovery`

Head:

`9912001a8848bfdafcaef050d7458136564bc3c6`

Its machine-readable status is:

`PARTIAL_RECOVERY_WINDOWS_NATIVE_CAPTURE_READY_HISTORICAL_REFERENCE_STILL_BLOCKED`

The currently supplied artifacts materially improve the build-contract evidence:

- `animo41.vfproj` and `animo41.sln` recover the Visual Studio/Intel Fortran project configuration, including 8-byte default REAL, SAVE/static local storage, FPS-compatible I/O settings, source floating-point model and CVF calling convention;
- all project-selected source units are present in frozen B0, with `input1_1.for` and `Outselorg.for` excluded from the project selection;
- the supplied `animo41.exe` has SHA-256 `40e29853a0431cc7e2b787dfeb1870f44e1ff402b5aaebd6f56c8365fc5b178d` and remains classified as `MODERN_NATIVE_REBUILD_NOT_HISTORICAL_REFERENCE`;
- the frozen `RuurloGrass` native input surface is pinned;
- PREP02R now has a fail-closed genuine-Windows capture harness and an execution handoff ready for two clean native diagnostic runs.

Static executable evidence still includes a 2026 PE timestamp, an x64 Debug PDB path, a modern linker signature and post-2011 Intel runtime evidence. The candidate therefore cannot substitute for the missing historical B2 executable or executable-linked historical output.

At the checked PREP02R head:

- the external archival/provenance request is still not sent;
- no provenance-qualified historical reference artifact has been obtained;
- the modern native candidate has not yet been executed in a genuine Windows capture;
- no native historical reference run has been completed;
- no native-vs-GNU comparison has been completed;
- no historical or equivalent reference has been qualified;
- the historical-uncertainty route is not yet eligible because bounded acquisition is not closed.

Therefore the B3A02 route gate remains pending regardless of the second-line review result.

## Future cross-runtime diagnostic evidence

If the prepared Windows harness is later executed, its result may be useful to the TCD-017 dossier only as explicitly labelled cross-runtime corroboration. It may strengthen confidence that the observed ledger-only difference and unchanged ordinary outputs are not a GNU-specific compiler/runtime artifact.

It must not be used as:

- historical B2 evidence;
- proof of revision-53 release behaviour;
- a route-gate substitute;
- an excuse to weaken the expected-difference whitelist or non-interference requirements.

Even exact modern-native/GNU agreement leaves the route gate unchanged unless GOV02's independent route requirements are satisfied separately.

## Allowed review disposition

The independent reviewer may return a readiness-review result such as:

- `PASS_TCD017_SECOND_LINE_READINESS_REVIEW_ROUTE_STILL_PENDING`, or
- `FAIL_TCD017_SECOND_LINE_READINESS_REVIEW` with explicit failed questions.

A passing second-line readiness review is not itself corrected-legacy admission.

Until a valid B3 route also exists, the governing B3A02 status remains:

`QUALIFIED_TCD017_CLASS_A_ADMISSION_READINESS_ROUTE_AND_INDEPENDENT_REVIEW_PENDING`
