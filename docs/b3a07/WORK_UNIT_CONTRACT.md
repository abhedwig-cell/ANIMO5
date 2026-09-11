# ANIMO-B3A07 — TCD-037-A3 N2O Denitrification Formation Observer Tier-A Readiness

Branch: `work/animo-b3a07-tcd037-a3-tier-a-readiness`

Base/current aggregate: `ANIMO-RG05I@94afe7d649a8c60758a41996f0059de0acddd2fc`.

Purpose: evaluate admission readiness for canonical child atom `TCD-037-A3` only, consuming exact source/accounting semantics and the qualified SYNQ04 synthetic activation evidence. This workunit performs no scientific admission and grants no final Tier-A waiver.

Exact authorities:
- `ANIMO-SYNQ04@31d4ac628edf43501b403f0844dd472bcc12644c`, exact-final run `34548605202:success`;
- `ANIMO-B3I07@54679c7555a963133dfd686648af334f479c5808`;
- `ANIMO-RUNTIMEQ03@a3e822f8e97fe1312a7dfa73601a49ae7375163e`;
- `ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121`;
- `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`;
- retained Tier-A predicate authority `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`;
- `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`;
- `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`.

Atomic claim: the accepted-timestep N2O denitrification formation amount used by the `N2Od` accounting observer is `QPrN2Oden(Ln)*St`. At the existing frozen consumer seam `Z=10000`, the local reporting increment is `10000*QPrN2Oden(Ln)*St` into `Bani(N2Od,Ly)`.

Allowed reporting difference: `Bani(N2Od)` only. No physical state, process flux, restart/checkpoint state, numerical policy, solver/tolerance, `N2On`, `N2Oe`, `QRdN2O`, A1/A2/A4, TCD-032..036, or production difference is admitted by this readiness workunit.

Natural active-GHG revision-53 coverage remains blocked by source-testcase lineage mismatch; no testcase translation is allowed. SYNQ04 remains `B1_SYNTHETIC_NOT_B2` and historical revision-53 executable behavior remains `UNKNOWN`.

If every retained GOV04 Tier-A predicate passes under current GOV05 governance and exact-head CI is green, B3A07 may report readiness only. Any false or unknown predicate fails closed. The next admission decision identifier must be collision-checked live; `ANIMO-B3D25` is only a candidate identifier until that check is repeated.
