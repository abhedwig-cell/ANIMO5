# TCD-026 Independent Second-Line Review Contract

## Review object

Perform a genuinely separate second-line review of the atomic TCD-026 Class-A readiness claim.

Do not accept conclusions from B3A04, the same-context B3A04R technical review, or B3D07 merely because they are already persisted. Recheck the source-bound evidence and fail closed.

## Authorities to inspect live

- readiness: `ANIMO-B3A04@5eaf02298603b85f802d8e35d6a63941d0878879`
- same-context technical review, evidence input only: `ANIMO-B3A04R@27b1700a330959d1b5eae23a2094cad579630f14`
- route reconciliation: `ANIMO-B3D07@21766eaf3443bcf432f05fbf6ba89d365bc70988`
- historical-route authority: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`
- B3 framework: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`
- STATEQ02 support boundary: `ANIMO-STATEQ02@cb7c23524df6560e65a5bdc1ed19e0b6e3bd46c6`
- SYNQ01 register: `ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121`

Frozen B0 identities:

- source SHA256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank SHA256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

## Atomic claim

Candidate observation:

```fortran
Bfom(Inip_x,Ly) = Bfom(Inip_x,Ly) + Ex(Ln) * P
```

Claim: the already-existing initial root-exudate organic-matter state `Ex(Ln)` contributes `Ex(Ln)*P` to the fresh-organic-matter initial reporting/storage ledger `Bfom(Inip_x,Ly)` only. The claim must not change initialization physics, physical state, process fluxes, restart state, numerical policy, forcing or unrelated organic-matter TCDs.

## Required fail-closed checks

Independently verify all of the following:

1. frozen B0 source/testbank identities are the exact qualified identities;
2. `Ex(Ln)` physical ownership and lifecycle are correctly identified;
3. the begin-storage owner `Bfom(Inip_x,Ly)` and the exact omitted term `Ex(Ln)*P` are source-bound;
4. the candidate is truly `A_ACCOUNTING_REPORTING_ONLY`, with no physical-state or process-flux write path;
5. PREP06 synthetic activation really discriminates the omission with the `10.0 kg/ha` witness;
6. the model-produced CranMais replay genuinely activates nonzero initial Ex and supports the bounded claim;
7. the chronological CranMais 1974-to-1975 formatted restart probe genuinely activates the claim and its candidate/legacy restart-state comparison is interpreted correctly;
8. the formatted-restart continuous-versus-split differences remain a negative scope boundary and are not converted into a tolerance or whole-model identity claim;
9. the declared output-difference whitelist is complete and reporting-only, and non-whitelisted physical/scientific outputs remain unchanged in the cited evidence;
10. no TCD-026-specific SYNQ01 oracle exists, and no SYNQ01 evidence is falsely promoted to such an oracle or to B2;
11. STATEQ02 is used only for root-exudate continuation-state ownership relevance, never as TCD-026 ledger oracle, whole-model restart oracle or B2;
12. the same-context B3A04R technical review is supporting evidence only and does not count as the independent second line;
13. GOV03 and B3D07 still support the historical-uncertainty route, while historical revision-53 behaviour remains `UNKNOWN` and historical fidelity is not claimed;
14. the review does not compose TCD-026 with other organic-matter TCDs, does not authorize B4, production source changes or production migration, and does not perform admission.

Any unresolved item means FAIL or INCOMPLETE, not PASS.

## Result contract

Persist a machine-readable review result and a human-readable independent report on this review branch.

Use one unambiguous review result state chosen after inspecting any current review tooling/schema on the branch. Do not invent a result string that conflicts with a validator or pre-existing schema. The semantic result must be exactly one of `PASS`, `FAIL`, or `INCOMPLETE`.

A PASS is review evidence only. It is not TCD-026 admission.

## Independence boundary

This review must be executed in a separate ChatGPT context from B3A04/B3A04R/B3D07 authoring. Record that this establishes separate-context review only. Do not claim organizational or human independence unless that actually exists.
