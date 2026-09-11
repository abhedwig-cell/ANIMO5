# ANIMO-B3A06 — TCD-037-A2 CH4 Index-0 Formation/Emission Split Tier-A Readiness

## Purpose

Qualify admission readiness for canonical child atom `TCD-037-A2` only. This workunit consumes qualified source semantics and independently qualified synthetic activation. It evaluates the complete retained GOV04 Tier-A waiver predicate under current GOV05 governance. It does **not** grant the final waiver and does not perform scientific admission.

## Exact authorities

- base/evidence handoff: `ANIMO-SYNQ03@0ca6b31dc8d003ab2b86ced29a2ff8923496ee38`
- current aggregate snapshot: `ANIMO-RG05H@3e4247928bb43f30def951fa8804560636affbef`
- admitted sibling A1: `ANIMO-B3D21@331f6ed91d4a1c15a23ae0c1ad75d1b540f61858`
- canonical routing: `ANIMO-B3I07@54679c7555a963133dfd686648af334f479c5808`
- runtime/source semantics: `ANIMO-RUNTIMEQ03@a3e822f8e97fe1312a7dfa73601a49ae7375163e`
- synthetic policy: `ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121`
- current review governance: `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`, exact-head run `34546470484` success
- retained Tier-A predicate authority: `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`
- historical-uncertainty governance: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`
- B3 framework: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`

GOV05 qualified during B3A06 authoring. It explicitly retains the GOV04 Tier-A waiver without weakening, keeps `STRICTEST_APPLICABLE_RISK_TRIGGER_WINS`, and reduces no scientific evidence gate. B3A06 therefore consumes GOV05 while evaluating the same full Tier-A technical predicate.

## Atomic scientific object

A2 separates two accepted-timestep CH4 observer quantities with distinct source owners:

- formation total: `F_CH4 = sum(QPrCH4(1:Nl) * St)`;
- atmosphere-boundary emission total: `E_CH4 = (QEmCH4Dif + QEmCH4Ebl + QEmCH4Flw + QEmCH4Plt) * St`.

Allowed observer surface:

- `Btom(CH4e)`;
- `Btom(CO2e)` only as the existing formation-side dissimilation complement.

No model-wide CO2-ledger claim is made.

## Exact accounting relations

`Delta Btom(CH4e) = 10000 * E_CH4 / Cfracom`

`Delta Btom(CO2e) = D_OM - 10000 * F_CH4 / Cfracom`

The quantities remain semantically distinct even when numerically equal. SYNQ03 independently qualified this causality/scope split using exact-rational oracle arithmetic and exact binary64 dyadic cases. Evidence remains `B1_SYNTHETIC_NOT_B2`; natural revision-53 active-GHG execution remains `BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH`; no testcase translation occurred; historical executable behaviour remains `UNKNOWN`.

## Tier-A readiness rule

Every retained Tier-A predicate must PASS. Any false or unknown predicate fails closed. Readiness does not grant the final waiver; the later atomic admission decision must re-evaluate authorities, evidence, scope and all predicates.

## Identifier collision record

Live closeout checks found:

- `ANIMO-B3D22` already allocated to the separate TCD-031 Tier-C formal disposition;
- `ANIMO-B3D23` subsequently allocated to the separate TCD-031 GOV05 Tier-C admission lane;
- `ANIMO-B3D24` had no branch or open issue at the last B3A06 collision check.

B3A06 reserves none of these identifiers. The later admission workunit must live-check `ANIMO-B3D24` again before creating it; if it has become occupied, use the next free identifier without reopening the scientific readiness decision.

## Hard boundaries

No admission, final waiver, production-source change, frozen-B0 change, canonical-register change, new top-level TCD, parent/sibling admission, TCD-032..036 composition, B4, production migration, aggregate update, historical-fidelity claim, B1-to-B2 promotion, testcase translation or full carbon-ledger closure.

## Next route if qualified

Candidate identifier after current collision checks:

`ANIMO-B3D24 — TCD-037-A2 CH4 Index-0 Formation/Emission Split Tier-A Atomic Admission Decision`
