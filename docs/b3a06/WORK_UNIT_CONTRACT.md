# ANIMO-B3A06 — TCD-037-A2 CH4 Index-0 Formation/Emission Split Tier-A Readiness

## Purpose

Qualify admission readiness for the canonical child atom `TCD-037-A2` only.

This workunit consumes the already-qualified source semantics and the independently qualified synthetic activation for the CH4 index-0 semantic split. It evaluates the complete Tier-A waiver predicate at readiness scope. It does **not** grant the final waiver and does not perform scientific admission.

## Exact authorities

- base/evidence handoff: `ANIMO-SYNQ03@0ca6b31dc8d003ab2b86ced29a2ff8923496ee38`
- current aggregate snapshot: `ANIMO-RG05H@3e4247928bb43f30def951fa8804560636affbef`
- latest atomic sibling admission at start: `ANIMO-B3D21@331f6ed91d4a1c15a23ae0c1ad75d1b540f61858`
- canonical routing: `ANIMO-B3I07@54679c7555a963133dfd686648af334f479c5808`
- runtime/source semantics: `ANIMO-RUNTIMEQ03@a3e822f8e97fe1312a7dfa73601a49ae7375163e`
- synthetic evidence policy: `ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121`
- current review governance at closeout: `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`
- GOV05 exact-head CI: run `34546470484`, success
- retained Tier-A predicate authority: `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`
- historical-uncertainty governance: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`
- B3 framework: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`

At branch creation, GOV05 was still unqualified. Before B3A06 closeout it qualified on exact final head `f65a47724e4a4fca7f2d8b8d6de9eeee51867904`. B3A06 therefore consumes GOV05 as current governance authority. GOV05 explicitly retains the GOV04 Tier-A waiver without weakening and keeps `STRICTEST_APPLICABLE_RISK_TRIGGER_WINS`; no extra review phase is required for Tier A when every GOV04 Tier-A waiver predicate passes.

## Atomic scientific object

The exact A2 claim is that two accepted-timestep CH4 observer quantities have distinct source owners and must not be represented by one overloaded index-0 scalar:

- formation total for the formation-side organic-matter dissimilation complement:
  `F_CH4 = sum(QPrCH4(1:Nl) * St)`;
- atmosphere-boundary emission total for the CH4 emission observer:
  `E_CH4 = (QEmCH4Dif + QEmCH4Ebl + QEmCH4Flw + QEmCH4Plt) * St`.

The allowed observer surface is limited to:

- `Btom(CH4e)`;
- `Btom(CO2e)` only as the existing formation-side dissimilation complement.

This workunit makes no model-wide CO2-ledger claim.

## Exact accounting relations

Within the qualified active-GHG observer contract:

`Delta Btom(CH4e) = 10000 * E_CH4 / Cfracom`

`Delta Btom(CO2e) = D_OM - 10000 * F_CH4 / Cfracom`

where `D_OM` is the ordinary organic-matter dissimilation amount already owned by the legacy balance calculation.

The two relations are independent: changing emission while holding formation fixed may change only the CH4-emission observer; changing formation while holding emission fixed may change only the formation-side CO2 complement. Numerical equality when `F_CH4 = E_CH4` is not semantic identity.

## Evidence

`ANIMO-SYNQ03` independently qualified purpose-built synthetic activation for causality and scope with exact-rational oracle arithmetic and exact binary64 dyadic test values. Its exact final head workflow `34544980891` passed on `0ca6b31dc8d003ab2b86ced29a2ff8923496ee38`.

Evidence strength remains `B1_SYNTHETIC_NOT_B2`.

Natural revision-53 active-GHG execution remains `BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH`; no testcase translation was performed. Historical revision-53 executable behaviour remains `UNKNOWN`.

## Tier-A readiness decision rule

GOV05 leaves the GOV04 Tier-A waiver unchanged. Every Tier-A waiver predicate must therefore still be explicitly PASS at readiness. If any predicate is false or unknown, this workunit must fail closed and escalate rather than declare readiness.

A readiness PASS still does not grant the final waiver. A later atomic admission decision must recheck the exact authorities, claim, evidence identities, expected-difference contract and all Tier-A predicates before granting any final waiver.

## Hard boundaries

No production source modification. No frozen B0 modification. No canonical TCD register change. No new top-level TCD. No parent `TCD-037` admission. No A1/A3/A4 admission. No TCD-032..036 composition. No B4. No production migration. No aggregate update. No historical-fidelity claim. No B1-to-B2 promotion. No testcase translation. No full carbon-ledger closure claim.

## Next route if qualified

`ANIMO-B3D22 — TCD-037-A2 CH4 Index-0 Formation/Emission Split Tier-A Atomic Admission Decision`
