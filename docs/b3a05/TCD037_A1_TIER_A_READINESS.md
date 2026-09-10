# TCD-037-A1 CH4 layer-formation observer Tier-A readiness

Work unit: `ANIMO-B3A05`

Decision: `QUALIFIED_TCD037_A1_TIER_A_ADMISSION_READINESS_WAIVER_PREDICATE_PASS_NO_ADMISSION`

## 1. Atomic claim

B3I07 canonically atomized parent `TCD-037` into four sibling claims and routes A1 to B3A05. A1 alone is:

> In the active GHG layer-formation accounting branch, the CH4 amount used to partition ordinary organic-matter dissimilation between CH4 and CO2 observer fields is the source-owned accepted-timestep layer amount `QPrCH4(Ln) * St`.

A1 does not include the index-0 CH4 formation/emission split (A2), N2O denitrification formation (A3), N2O atmosphere emission (A4), or any TCD-032..036 correction.

## 2. Source and ownership basis

RUNTIMEQ02 established that legacy `Outbal_calc` locally reads `AmCH4(Ln)` without any source producer and that persistence cannot repair the missing fresh writer. RUNTIMEQ03 then qualified the intended layer accounting owner as `QPrCH4(Ln) * St` and separated that layer-formation meaning from atmosphere-boundary CH4 emission.

For A1 this removes the source-meaning ambiguity that previously forced parent TCD-037 to GOV04 Tier C. The A1 source quantity is a current accepted-timestep process amount supplied to an observer; it is not persistent model state, restart state, solver state or a new physical store.

Frozen identities consumed here:

- source archive SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- `Outbal_calc.for` SHA-256 `4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981`.

## 3. Exact accounting identity

SYNQ02 independently implemented the bounded A1 observer calculation and used exact rational arithmetic as its oracle. For an active non-degenerate layer:

`M_CH4 = 10000 * QPrCH4(Ln) * St / Cfracom`

`Btot = Ffom + Fahu + Fdom`

`CH4_i = F_i / Btot * M_CH4`

`CO2_i = F_i - CH4_i`

The exact identities are:

`sum_i(CH4_i) = M_CH4`

and

`sum_i(CH4_i + CO2_i) = Btot`.

The synthetic values were chosen so the expected values are exactly representable in binary64. No empirical tolerance was introduced. The exact-final SYNQ02 head `1975eda3586d79033be6af745994bb6181a825fc` passed GitHub Actions run `34538344680`.

## 4. Activation and independence

The supplied `GHGMais` testcase is not revision-53 compatible, so a natural active-GHG B1 case remains unavailable. That absence is documented as `BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH`; no testcase translation is permitted as evidence fabrication.

GOV04 allows a purpose-built synthetic activation when natural activation is not reasonably available, provided absence is documented and the synthetic activation is independently qualified for causality and scope. SYNQ02 was authored after the RUNTIMEQ03 semantic qualification, uses a separate source-shaped target and an independently implemented exact-rational oracle, and does not reuse ANIMO source code in that oracle.

SYNQ02 covers:

- active nonzero CH4 formation;
- active zero-CH4 negative control;
- asymmetric layer permutation;
- rate/timestep metamorphic equivalence for the same `QPrCH4*St` amount;
- inactive-GHG negative control.

This evidence remains `B1_SYNTHETIC_NOT_B2`. Historical revision-53 behaviour remains `UNKNOWN`.

## 5. Expected-difference contract

The allowed observer-only difference surface is exactly:

- `Bfom(CH4f)`;
- `Bahu(CH4f)`;
- `Bdom(CH4f)`;
- `Bfom(CO2f)`;
- `Bahu(CO2f)`;
- `Bdom(CO2f)`.

Expected differences outside this surface are `NONE`, including:

- physical state;
- GHG process fluxes;
- hydrology;
- restart/checkpoint state;
- solver state;
- tolerances or numerical policy;
- unrelated observer fields;
- A2, A3 and A4 surfaces.

RUNTIMEQ03 froze this structural surface before B3A05, and SYNQ02 independently exercised it. The B3A05 decision does not add a new difference class.

## 6. B3 route

No qualified B2 historical executable reference exists. GOV03 has qualified the bounded acquisition result as `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT` and the G6U route as eligible subject to claim-scoped B3 requirements.

Therefore A1's only available later admission route is:

`INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY`.

The word `INDEPENDENT` in that route does not convert SYNQ02 into historical evidence. It refers to the scientific basis and cross-check requirements. GOV04 can waive a separate second-line review only if every Tier-A waiver predicate remains PASS at the later admission decision.

## 7. GOV04 strictest-risk evaluation

A1 is evaluated independently of the parent and siblings. No Tier C trigger remains at A1 scope:

- no restart or cold-start semantics;
- no initialization semantics;
- no canonical state ownership change;
- no checkpoint change;
- no missing physical state;
- no numerical policy, tolerance or solver change;
- no physical runtime branch change;
- no singular-domain or exact-zero policy;
- no unresolved source/accounting ownership ambiguity.

No Tier D trigger applies because this is not composition and no production source is modified.

A1 therefore remains a `GOV04 Tier A` candidate at readiness scope.

## 8. Tier-A waiver predicate audit

All GOV04 Tier-A predicate components evaluate PASS at readiness scope:

| Predicate | Result | Basis |
| --- | --- | --- |
| exact source seam pinned | PASS | RUNTIMEQ02/RUNTIMEQ03 frozen-source pins |
| physical/accounting ownership unambiguous | PASS | RUNTIMEQ03 A1 owner `QPrCH4*St` |
| atomic claim | PASS | B3I07 canonical A1 routing |
| exact accounting identity | PASS | SYNQ02 exact-rational oracle |
| expected difference pinned before qualification | PASS | RUNTIMEQ03 then SYNQ02 |
| physical-state non-interference | PASS | source ownership graph plus SYNQ02 sentinels |
| process-flux non-interference | PASS | source ownership graph plus SYNQ02 sentinels |
| no numerical-policy change | PASS | observer-only contract |
| no solver/tolerance change | PASS | observer-only contract |
| no restart/init/state semantic change | PASS | RUNTIMEQ02/RUNTIMEQ03 |
| no composition | PASS | A1 isolated |
| no unresolved scientific/source ambiguity | PASS | RUNTIMEQ03 A1 semantic qualification |
| reproducible validator | PASS | SYNQ02 plus B3A05 validator |
| scope guard | PASS when B3A05 CI passes | B3A05 path allowlist |
| natural or independently qualified synthetic activation | PASS | natural absence documented; SYNQ02 qualified |
| historical behaviour remains UNKNOWN without B2 | PASS | SYNQ01/SYNQ02/GOV03 |
| GOV03 route conditions retained | PASS | GOV03 G6U eligibility |
| no production/register/B4/governance-snapshot mutation | PASS | B3A05 scope guard |

This establishes `TIER_A_WAIVER_PREDICATE_PASS_AT_READINESS` but **does not grant the final waiver**. The admission workunit must recheck the exact same predicate against then-live authority and must fail closed if any pin, claim, scope or evidence changes.

## 9. B3Q01 child-schema compatibility

The finalized B3 disposition schema restricts `tcd_ids` to top-level IDs matching `TCD-NNN`. It therefore cannot place `TCD-037-A1` directly in `tcd_ids` without a governance/schema change.

No schema change is required. B3Q01 explicitly allows one atomic record to cite the parent TCD while the admitted correction itself remains one atomic causal claim. A later A1 record should therefore use:

- `tcd_ids: ["TCD-037"]`;
- an A1-specific `record_id`;
- `atomicity: ATOMIC`;
- the canonical child identity `TCD-037-A1` in scope/class-specific evidence;
- only the A1 expected-difference surface.

This preserves the finalized B3Q01 schema and prevents parent-level or sibling admission from being inferred.

## 10. Residual uncertainty

The historical executable behaviour of the disconnected `AmCH4` local remains unknown. The natural active-GHG revision-53 testcase gap also remains. Those uncertainties are retained explicitly and do not become historical-equivalence claims.

The qualified claim is narrower: the A1 accounting owner and accounting identity are independently sufficient for a bounded scientific disposition under historical uncertainty, subject to an admission-time recheck of every GOV04 Tier-A predicate.

## 11. Closeout

B3A05 performs no scientific admission, no production patch and no aggregate update.

If the exact B3A05 final head passes its validator and scope guard, the next atomic route is:

`ANIMO-B3D21 — TCD-037-A1 CH4 Layer Formation Observer GOV04 Tier-A Atomic Admission Decision`

B3D21 may combine formal disposition, Tier-A review-waiver applicability and admission closeout only if all pins and gates remain unchanged. Otherwise it must fail closed or escalate. A2, A3 and A4 remain separate sibling lanes.