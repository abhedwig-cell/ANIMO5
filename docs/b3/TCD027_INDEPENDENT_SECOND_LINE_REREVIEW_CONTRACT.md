# ANIMO-B3A01R2 — TCD-027 Independent Second-Line Re-Review Contract

## Purpose

Perform a new, genuinely separate second-line re-review of TCD-027 after qualified frozen-B0 source evidence remediation.

This contract is handoff metadata only. It is not reviewer evidence, does not change the prior ANIMO-B3A01R result `INCOMPLETE`, and does not admit TCD-027.

## Independence boundary

ANIMO-B3A01R2 must be executed in a new ChatGPT context, separate from:

- ANIMO-B3A01R review authoring;
- ANIMO-B3A01E evidence-remediation authoring;
- ANIMO-B3A01 readiness authoring;
- ANIMO-B3D10 disposition authoring.

The reviewer must independently assess the evidence and fail closed. Record only separate-context independence. Do not claim organizational or human independence unless it actually exists.

## Clean branch

`review/animo-b3a01r2-tcd027-independent-second-line-rereview`

Source-bound base:

`ANIMO-B3A01E@5232ef5fa6daafa2296401b19fd9e866a34152bd`

B3A01E final validation:

- GitHub Actions run `34459737928`
- conclusion `success`

## Authorities

- readiness: `ANIMO-B3A01@b2bac82512fef0fa232e759f0c68b472567c11d5`
- formal route reconciliation: `ANIMO-B3D10@a7b11b334f8b2604d5036edc04365006800944e0`
- historical route: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`
- B3 framework: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`
- prior independent review, history/evidence only: `ANIMO-B3A01R@510c9313926457cd9bfd8e71a551255297bdfbb3`, result `INCOMPLETE`
- evidence remediation: `ANIMO-B3A01E@5232ef5fa6daafa2296401b19fd9e866a34152bd`

## Frozen B0 identities

- source SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- `Outbal_calc.for` exact member SHA-256: `4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981`
- `Outbal_write.for` exact member SHA-256: `cdc0a9738216d8a97d3c35f9862b78fc94fec385aaf0691d6778a73031ac74ea`

Primary byte-authoritative remediation evidence:

`integration/animo-b3/TCD027_FROZEN_B0_SOURCE_EVIDENCE_MANIFEST.json`

Supporting remediation report:

`docs/b3/TCD027_FROZEN_B0_SOURCE_EVIDENCE_REMEDIATION.md`

Extraction/verifier:

`tools/extract_verify_tcd027_frozen_b0.py`

Do not accept B3A01E prose interpretations as reviewer conclusions. Independently decode the manifest `exact_bytes_base64`, verify each neighbourhood SHA-256/line range/offset identity, and derive the source conclusions from those bytes.

## Atomic claim

Source routine: `Outbal_calc.for`

Legacy:

```fortran
Bafop(24,Ly)=Bafop(25,Ly)+Dum
```

Candidate:

```fortran
Bafop(24,Ly)=Bafop(24,Ly)+Dum
```

Scope only: detailed organic-P reporting accumulator slot 24, `redis_EXP`.

No organic-P physics, physical-state correction, process-flux correction, numerical-policy change or other TCD is in scope.

## Required independent re-review

Re-run the complete original second-line surface, not only the previously incomplete items.

At minimum verify independently:

1. frozen source/testbank identities and exact source-member identities;
2. exact legacy and candidate expressions and local `Dum` construction, including `Dum = Adexpl(I,Ln)*Pofrex*Z` at the disputed seam;
3. exact `Outbal_write.for` mapping: slot 24 `redis_EXP`, 25 `redis_OP`, 26 `redis_DOP`, 27 `redis_HUP`, rederived from frozen source bytes;
4. `Bafop` is a detailed reporting accumulator and not a physical organic-P state owner;
5. OM/N slot-24 analogues and exact organic-P slot-25/26/27 self-accumulator statements;
6. natural activation in `LWKM_gras_1040.2021.2045`, period 1997;
7. diagnostic discriminator only: legacy `redis_EXP` approximately `-7.0644 kg/ha P`, candidate `0.0 kg/ha P`;
8. exact changed-output whitelist: `transfopGP.Out`, `transfopRP.Out`, `transfopTP.Out`;
9. physical state trajectory unchanged;
10. process flux trajectory unchanged;
11. total organic-P balance unchanged;
12. total mass balance unchanged;
13. `redis_OP` unchanged;
14. `redis_DOP` unchanged;
15. `redis_HUP` unchanged;
16. ordinary non-reporting outputs unchanged across the cited 58 common top-level outputs;
17. GOV03 remains live and valid;
18. no qualified B2 has appeared since B3D10/B3A01E;
19. historical revision-53 behaviour remains `UNKNOWN`;
20. independently reassess B3Q01 historical-uncertainty route sufficiency for this atomic Class-A claim;
21. PREP06 and B3A01 remain B1 diagnostic/readiness evidence only and are never promoted to B2;
22. ANIMO 4.0 user guide is not exact revision-53 slot-algebra authority;
23. TCD-017, TCD-026, TCD-028 and every other correction remain outside scope;
24. no composition, production patch, B4, central-regie update or admission is performed.

Any unresolved required item means `FAIL` or `INCOMPLETE`, not `PASS` by inference.

## Result contract

Semantic result exactly one of:

- `PASS`
- `FAIL`
- `INCOMPLETE`

Persist:

- human-readable independent re-review report;
- machine-readable result;
- exact reviewed heads and evidence identities;
- explicit residual uncertainties;
- validator;
- review-only scope guard;
- GitHub Actions validation;
- issue #43 update with result and exact validated head.

A `PASS` is review evidence only. It does not admit TCD-027. Stop before admission. A later separate admission-closeout workunit must reconcile any passing re-review with B3Q01 and GOV03 while retaining historical uncertainty.
