# TCD-027 Independent Second-Line Review Contract

Review workunit: `ANIMO-B3A01R`

Target: `TCD-027`

Class: `A_ACCOUNTING_REPORTING_ONLY`

## Review object

Perform a genuinely separate second-line review of the atomic TCD-027 Class-A readiness and route-open disposition.

Do not accept conclusions from B3A01 or B3D10 merely because they are already persisted. Recheck the frozen source, retained diagnostic evidence, output semantics, non-interference and route logic independently and fail closed.

This branch is a handoff only. No independent review has been performed on it by the B3D10 authoring context.

## Authorities to inspect live

- readiness: `ANIMO-B3A01@b2bac82512fef0fa232e759f0c68b472567c11d5`
- route reconciliation: `ANIMO-B3D10@a7b11b334f8b2604d5036edc04365006800944e0`
- B3D10 final validation: GitHub Actions run `34449532126`, success
- historical-route authority: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`
- B3 framework: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`
- PREP06 TCD-027 evidence blob: `5bc14b350b1b60f870ab568d4c8a127275ca8a84`

Frozen B0 identities:

- source SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

## Atomic claim

Source routine:

`Outbal_calc.for`

Legacy:

```fortran
Bafop(24,Ly)=Bafop(25,Ly)+Dum
```

Candidate:

```fortran
Bafop(24,Ly)=Bafop(24,Ly)+Dum
```

The claim is limited to detailed organic-P reporting accumulator slot 24, identified as `redis_EXP`. No organic-P physics, physical state, process flux, numerical policy, production source or other TCD correction is part of the review object.

## Required fail-closed checks

Independently verify every item below from the underlying source and evidence rather than from B3A01/B3D10 prose alone.

1. Recompute or otherwise verify the frozen B0 source and testbank identities used for the review object.
2. Verify the exact `Outbal_calc.for` legacy expression and candidate expression, including the `Dum` contribution in the same source context.
3. Verify the exact `Outbal_write.for` output ordering and establish that `Bafop(24)` is `redis_EXP`, `Bafop(25)` is `redis_OP`, `Bafop(26)` is `redis_DOP`, and `Bafop(27)` is `redis_HUP`.
4. Verify that the `Bafop` vector is a detailed organic-P reporting accumulator written to `transfop<profile>.Out`, not a physical organic-P state owner.
5. Verify the orthogonal accumulator evidence: organic-matter slot 24 self-accumulates, organic-N slot 24 self-accumulates, and organic-P slots 25 through 27 self-accumulate. Determine independently whether this supports the narrow wrong-index interpretation.
6. Verify natural activation in the supplied `LWKM_gras_1040.2021.2045` path for period 1997 and recheck the provenance of that activation evidence.
7. Verify the numerical discriminator without promoting its magnitude to a tolerance: legacy `redis_EXP` approximately `-7.0644 kg/ha P`, candidate `0.0 kg/ha P`.
8. Verify that the complete declared changed-output whitelist is exactly `transfopGP.Out`, `transfopRP.Out` and `transfopTP.Out`, and that the change is limited to the intended detailed organic-P reporting content.
9. Verify physical-state trajectory non-interference for the bounded comparison.
10. Verify process-flux trajectory non-interference for the bounded comparison.
11. Verify that total organic-P balance and total mass-balance surfaces are unchanged.
12. Verify that `redis_OP`, `redis_DOP` and `redis_HUP` remain unchanged and that ordinary non-reporting outputs remain unchanged across the cited 58 common top-level outputs.
13. Recheck GOV03 live. Confirm that no qualified B2 has appeared, that `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT` and `G6U = ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS` remain the applicable route authority, and that historical revision-53 behaviour remains `UNKNOWN`.
14. Re-evaluate whether the source identity, writer mapping, natural causal discriminator and non-interference package are scientifically sufficient for route opening under B3Q01. Do not treat the B3D10 authoring-context source cross-check as this independent second-line review.
15. Verify atomicity. TCD-017, TCD-026, TCD-028 and every other organic-P or stable-DOM correction must remain outside the claim. No broader organic-P physics may be inferred from the slot-24 result.
16. Verify governance boundaries: no production patch, no B4, no central-regie update, no composition and no TCD-027 admission may be performed by this review workunit.

Any unresolved item means `FAIL` or `INCOMPLETE`, never `PASS`.

## Evidence interpretation boundaries

PREP06 and B3A01 are B1 diagnostic/readiness evidence. They are not historical B2 and may not be used to claim historical fidelity.

The ANIMO 4.0 user guide may support the existence and purpose of detailed organic-transformation outputs, but it does not define the exact revision-53 `Bafop` slot-24 algebra. Do not use it to close that source-specific question.

A smaller residual or a visually improved output is not sufficient evidence by itself. The review must establish the index/slot identity and reporting ownership independently.

No numerical tolerance is created by the `-7.0644` versus `0.0` discriminator.

## Result contract

Persist both a human-readable independent report and a machine-readable review result on this review branch.

The semantic result must be exactly one of:

- `PASS`
- `FAIL`
- `INCOMPLETE`

A `PASS` is independent review evidence only. It is not TCD-027 admission and does not authorize production code or B4.

If the result is `PASS`, record the exact reviewed heads, source/testbank identities, PREP06 evidence identity, route authority, review scope, all gate outcomes and remaining historical uncertainty. Then stop. A later separate admission-closeout workunit must reconcile the review with B3Q01 and GOV03.

If the result is `FAIL` or `INCOMPLETE`, record the exact failing or unresolved gates and stop without admission.

## Independence boundary

Execute this review in a separate ChatGPT context from the B3D10 disposition authoring context. Record only separate-context independence. Do not claim organizational or human independence unless that actually exists.
