# ANIMO-B3A01 — TCD-027 Class A Corrected-Legacy Admission Readiness

## Purpose

Prepare one atomic Class A B3 admission package for `TCD-027`, the organic-P detailed redistribution accumulator defect, without admitting the correction before the historical-reference gate is legitimately available.

This workunit is intentionally narrower than ANIMO-B3Q01. It applies the B3 governance framework to one discrepancy and tests whether the existing evidence is sufficient to reach an admission decision.

## Source-bound starting point

Repository: `abhedwig-cell/ANIMO5`

Framework base commit: `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`

Framework decision: `QUALIFIED_B3_SCIENTIFIC_ADMISSION_FRAMEWORK_NO_LEGACY_CORRECTIONS_ADMITTED`

Frozen source SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Frozen testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Supplied documentation SHA-256: `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`

## Target discrepancy

`TCD-027` is currently classified as `CONFIRMED_LEGACY_DETAILED_LEDGER_ACCUMULATOR_DEFECT`.

The source-bound expression is:

`Bafop(24,Ly)=Bafop(25,Ly)+Dum`

The diagnostic ledger-only probe is:

`Bafop(24,Ly)=Bafop(24,Ly)+Dum`

Existing PREP06 evidence reports a naturally activated LWKM 1997 case in which only `transfopGP.Out`, `transfopRP.Out`, and `transfopTP.Out` change, while total organic-P balances, ordinary physical outputs, process outputs, state trajectories, and total mass balance remain unchanged.

## Qualification class

Primary class: `A_ACCOUNTING_REPORTING_ONLY`.

This classification is conditional on continued proof that the candidate correction changes no physical state and no process flux. Any later evidence of state or flux change forces reclassification and blocks Class A admission.

## Hard boundaries

This workunit shall not:

- modify frozen source bytes;
- modify frozen testcase bytes;
- implement production ANIMO5 code;
- change model physics;
- change numerical policy;
- mark TCD-027 as B3-admitted while B2 is unavailable and the historical-uncertainty fallback precondition is unmet;
- treat the GNU B1 diagnostic executable as B2;
- treat the natural diagnostic run as independent historical evidence;
- hide the historical incorrect `redis_EXP` report value after any future corrected-legacy admission.

Temporary diagnostic evidence already produced in PREP06 may be cited, but no new correction patch is necessary in this readiness workunit.

## Route state

At workunit start, PREP02R reports:

`BLOCKED_HISTORICAL_REFERENCE_ARTIFACT_NOT_YET_OBTAINED`.

The prepared WUR archival request has not yet been sent. Therefore:

- the normal route cannot pass because B2 is unavailable;
- the historical-uncertainty route cannot yet be invoked because the documented reasonable acquisition effort has not reached a legitimate stopping point.

The correct result may therefore be a qualified admission-readiness package with `UNRESOLVED_NOT_ADMITTED` disposition and an explicit B2 blocker.

## Required evidence gates

The readiness assessment shall record:

1. B0 source, testcase, and documentation identity.
2. B1 causal evidence and its diagnostic limitation.
3. Current B2 status and why no admission route is presently complete.
4. The detailed accumulator identity.
5. Proof that the correction is reporting-only.
6. Exact changed and unchanged output surfaces.
7. Natural path activation evidence.
8. Conservation and total-balance non-interference evidence.
9. Residual uncertainty.
10. Independent-review requirement for any eventual admission.

## Deliverables

- `docs/b3a01/TCD027_CLASS_A_ADMISSION_READINESS.md`
- `integration/animo-b3/TCD027_CLASS_A_READINESS.json`
- `integration/animo-b3/ANIMO-B3A01_STATUS.json`
- `tools/validate_b3a01_tcd027.py`
- `.github/workflows/animo-b3a01-tcd027.yml`

## Decision rule

This workunit may close as readiness-qualified when the evidence package is internally consistent, source-bound, machine-readable, and fail-closed.

It may not close as corrected-legacy admission unless a later, explicit admission record satisfies the ANIMO-B3Q01 disposition schema through either:

- `NORMAL_B2_AVAILABLE`; or
- `INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY` after the acquisition-effort precondition is genuinely met.

Expected current production migration state: `NOT_ADMITTED`.
