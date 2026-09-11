# ANIMO-B3D24 — TCD-037-A2 CH4 Index-0 Formation/Emission Split GOV05 Tier-A Atomic Admission Decision

## Purpose

Make the bounded B3 scientific disposition/admission decision for canonical child atom `TCD-037-A2` after `ANIMO-B3A06` qualified the complete Tier-A waiver predicate at readiness scope.

This workunit must independently re-evaluate the exact pinned evidence, atomic claim, expected-difference surface, GOV03 historical-uncertainty route and every retained GOV04 Tier-A predicate under current GOV05 governance. If every predicate remains PASS, it may grant the final Tier-A review waiver and admit only `TCD-037-A2` under historical uncertainty.

## Exact starting point

`ANIMO-B3A06@466718167b22a643b26ee5035a18514987b6e289`

B3A06 exact-final workflow: run `34547418205`, `completed/success` on the exact head above.

## Required authorities

- aggregate snapshot: `ANIMO-RG05H@3e4247928bb43f30def951fa8804560636affbef`
- canonical routing: `ANIMO-B3I07@54679c7555a963133dfd686648af334f479c5808`
- runtime semantics: `ANIMO-RUNTIMEQ03@a3e822f8e97fe1312a7dfa73601a49ae7375163e`
- independent synthetic activation: `ANIMO-SYNQ03@0ca6b31dc8d003ab2b86ced29a2ff8923496ee38`
- SYNQ03 exact-final workflow: run `34544980891`, success
- synthetic policy: `ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121`
- current review governance: `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`
- GOV05 exact-final workflow: run `34546470484`, success
- retained Tier-A predicate: `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`
- historical uncertainty route: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`
- B3 disposition framework: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`
- child-atom carrier governance: `ANIMO-B3Q02@1db63b17cb5f48cbd8ae28116a2e716b4bdaadf3`

GOV05 explicitly retains the GOV04 Tier-A waiver without weakening. Therefore no separate review phase is required for this Tier-A atom if and only if every retained Tier-A predicate is PASS. No independence claim is made for the waived review gate.

## Exact atomic claim

`TCD-037-A2` separates the two source-owned accepted-timestep meanings that the legacy CH4 index-0 observer path overloads:

- formation total for the existing formation-side organic-matter dissimilation complement:
  `F_CH4 = sum(QPrCH4(1:Nl) * St)`;
- atmosphere-boundary emission total for the CH4 emission observer:
  `E_CH4 = (QEmCH4Dif + QEmCH4Ebl + QEmCH4Flw + QEmCH4Plt) * St`.

The only admissible changed reporting surface is:

- `Btom(CH4e)`;
- `Btom(CO2e)` only as the existing formation-side dissimilation complement.

No physical state, GHG process flux, restart/checkpoint state, solver/numerical-policy quantity, sibling atom, unrelated observer or model-wide CO2 ledger is admitted to change.

## Accounting relations

`Delta Btom(CH4e) = 10000 * E_CH4 / Cfracom`

`Delta Btom(CO2e) = D_OM - 10000 * F_CH4 / Cfracom`

SYNQ03 qualifies the causal distinction with exact-rational oracle arithmetic, exact binary64 dyadic synthetic values, divergent/formation-only/emission-only controls, an equal-total semantic control, rate-time equivalence and inactive/scope sentinels.

## Historical uncertainty

No qualified B2 historical executable reference exists. Historical revision-53 behaviour remains `UNKNOWN`. The natural active-GHG testcase route remains `BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH`; no testcase translation was performed.

Synthetic evidence remains `B1_SYNTHETIC_NOT_B2` and is used only as independently qualified causality/scope activation evidence under the retained Tier-A synthetic-activation alternative.

## Child carrier

The formal disposition must use the additive B3Q02 `FORMAL_DISPOSITION` carrier. The embedded B3Q01 record uses `tcd_ids: ["TCD-037"]` as lineage only and binds the actual disposition with exact decision scope:

`CANONICAL_CHILD_ATOM:TCD-037-A2`

Admission of A2 must not imply admission of parent `TCD-037` or siblings A1, A3 or A4. A1's existing separate admission remains unaffected.

## Tier-A review-waiver representation

If every predicate passes, the B3Q01 independent-review evidence block records `status: INCOMPLETE`, `result: NOT_REVIEWED`, `independent_from_correction_authoring: false`. The corresponding gate is `PASS / NOT_APPLICABLE` with explicit GOV05/GOV04 Tier-A waiver evidence. This records applicability only; it does not claim that an independent review occurred.

## Hard boundaries

No production source or frozen B0 modification; no parent or sibling admission; no TCD-032..036 composition; no canonical top-level register change; no new top-level TCD; no governance mutation; no B4; no production migration; no historical-fidelity claim; no B1-to-B2 promotion; no testcase translation; no model-wide CO2-ledger closure.

## Allowed PASS result

Formal disposition:

`HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY`

Bounded decision:

`ADMIT_TCD037_A2_CH4_INDEX0_FORMATION_EMISSION_SPLIT_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_A_WAIVER`

After an exact-final-head PASS, central aggregation is re-evaluated separately from the atomic admission authority.
