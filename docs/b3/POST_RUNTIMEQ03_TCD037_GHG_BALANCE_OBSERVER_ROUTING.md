# ANIMO-B3I07 — TCD-037 GHG balance observer child-atom routing

Status target: `QUALIFIED_TCD037_CANONICAL_CHILD_ROUTING_TIER_A_CANDIDATES_NO_ADMISSION`

This workunit is a canonical routing and readiness-partition step only. It consumes the qualified RUNTIMEQ03 accounting-semantics result and does not implement or admit a correction.

## Authorities

Canonical routing predecessor:

`ANIMO-B3I06@8f01f0cb366dfa8cc63a184d6f885100899a8cd9`

Scientific/runtime evidence:

`ANIMO-RUNTIMEQ03@a3e822f8e97fe1312a7dfa73601a49ae7375163e`

Aggregate authority observed at start:

`ANIMO-RG05G@4551b6b4c3f987b1247571d59f8489b2f1a71ba6`

Governance:

- `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`
- `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`
- B3Q02 child-atom carrier semantics already present in the B3I06 ancestry.

No B3I07 branch, later TCD-037 routing workunit, or RG05H authority existed at the live start check.

## Routing decision

RUNTIMEQ03 proves that the existing top-level TCD-037 phenomenon is not one atomic correction. The disconnected/overloaded GHG balance observer contains four separable correction claims. B3I07 therefore allocates four canonical child keys under the existing parent and does not allocate a new top-level TCD.

The canonical child map is:

| child | atomic claim | B3 class | GOV04 state | next readiness owner |
| --- | --- | --- | --- | --- |
| `TCD-037-A1` | CH4 layer formation amount drives the `CH4f/CO2f` layer reporting partition | `A_ACCOUNTING_REPORTING_ONLY` | `TIER_A_CANDIDATE` | `ANIMO-B3A05` |
| `TCD-037-A2` | CH4 formation total and atmosphere-emission total are separate index-0 accounting quantities | `A_ACCOUNTING_REPORTING_ONLY` | `TIER_A_CANDIDATE` | `ANIMO-B3A06` |
| `TCD-037-A3` | N2O denitrification layer formation amount drives `N2Od` | `A_ACCOUNTING_REPORTING_ONLY` | `TIER_A_CANDIDATE` | `ANIMO-B3A07` |
| `TCD-037-A4` | total N2O atmosphere emission drives `N2Oe`, not a production-total surrogate | `A_ACCOUNTING_REPORTING_ONLY` | `TIER_A_CANDIDATE` | `ANIMO-B3A08` |

These child keys are canonical qualification targets, not top-level rows in `THEORY_CODE_DISCREPANCY_REGISTER.csv`. The top-level register remains unchanged and its tail remains TCD-042. TCD-043 remains unreserved by this workunit.

Parent TCD-037 becomes:

`ATOMIZED_A1_A2_A3_A4_ACCOUNTING_OBSERVER_CHILDREN_NO_ADMISSION`

The parent is not an admission target because its correction surface is compound.

## Qualified accounting identities retained from RUNTIMEQ03

For `TCD-037-A1`:

`CH4_FORMATION_AMOUNT(Ln) = QPrCH4(Ln) * St`, for `Ln=1..Nl`.

Its structural expected-difference whitelist is limited to `Bfom/Bahu/Bdom(CH4f)` and the associated `Bfom/Bahu/Bdom(CO2f)` partition fields using that same layer formation amount.

For `TCD-037-A2`, two distinct source-owned quantities must not be collapsed into one `AmCH4(0)` value:

`CH4_FORMATION_TOTAL = sum(QPrCH4(1:Nl) * St)`

and

`CH4_ATMOSPHERE_EMISSION_AMOUNT = (QEmCH4Dif + QEmCH4Ebl + QEmCH4Flw + QEmCH4Plt) * St`.

Its allowed observer surface is `Btom(CH4e)` plus `Btom(CO2e)` only insofar as the existing dissimilation complement is separated from the atmosphere-emission scalar and supplied with the formation-side CH4 amount. This does not claim closure of the wider GHG carbon ledger.

For `TCD-037-A3`:

`N2O_DENITRIFICATION_FORMATION_AMOUNT(Ln) = QPrN2Oden(Ln) * St`.

Its allowed observer surface is `Bani(N2Od)`.

For `TCD-037-A4`:

`N2O_ATMOSPHERE_EMISSION_AMOUNT = (QEmN2ODif + QEmN2OFlw) * St`.

Its allowed observer surface is `Bani(N2Oe)`. Existing `Banh(N2On)` layer production accounting and the existing nitrification reporting threshold are outside this atom.

For all four children, the qualified structural contract remains:

- expected physical-state difference: none;
- expected process-flux difference: none;
- expected restart-state difference: none;
- expected solver or numerical-policy difference: none;
- expected differences are observer/reporting only.

`QRdN2O` remains a separate N2O reduction sink and is not routed as a TCD-037 observer producer.

## Why all four are only Tier-A candidates

B3Q01 Class A fits the qualified correction type because the physical GHG states and flux owners already exist and the defect is confined to a balance/reporting interface. GOV04 also allows a Tier-A review waiver only when every strengthened waiver predicate passes.

B3I07 does not grant that waiver. In particular:

1. the parent had to be atomized first, which this workunit now does;
2. no correction candidate has yet demonstrated the exact accounting identity on the corrected path;
3. no correction-specific reproducible validator and scope guard yet exists for any child;
4. natural active-GHG revision-53 execution remains blocked by the source/testcase lineage mismatch;
5. the current RUNTIMEQ03 synthetic B1 discriminator was authored in the qualification context and is not an independently qualified substitute for the GOV04 activation predicate;
6. no qualified B2 exists, so historical revision-53/Intel behaviour remains exactly `UNKNOWN`.

Accordingly each child is routed as `TIER_A_CANDIDATE_WAIVER_NOT_YET_AVAILABLE`, not as an admitted or waived object. A later readiness workunit must re-evaluate every GOV04 Tier-A predicate independently. If a higher-risk trigger appears, the strictest applicable tier wins.

## Readiness partition

The four children proceed separately to avoid silent composition:

- `ANIMO-B3A05 — TCD-037-A1 CH4 Layer Formation Observer Tier-A Readiness`;
- `ANIMO-B3A06 — TCD-037-A2 CH4 Index-0 Formation/Emission Split Tier-A Readiness`;
- `ANIMO-B3A07 — TCD-037-A3 N2O Denitrification Formation Observer Tier-A Readiness`;
- `ANIMO-B3A08 — TCD-037-A4 N2O Atmosphere Emission Observer Tier-A Readiness`.

Each readiness workunit must consume the canonical child map, verify the exact RUNTIMEQ03 evidence pin, freeze a correction-specific expected-difference contract before testing, qualify activation and non-interference, preserve historical behaviour as `UNKNOWN` without B2, and use the B3Q02 child-atom disposition carrier if it later reaches a formal disposition.

A readiness PASS for one child does not admit any sibling or the TCD-037 parent. No composition with TCD-032 through TCD-036 is allowed merely to make a child pass.

## Nonclaims and hard boundaries

B3I07 makes no production source change, no scientific admission, no corrected-legacy admission, no B4 claim, no RG05H update, no numerical-policy change, no restart/state change, no complete GHG C/N-ledger claim and no historical-fidelity claim.

The wider GHG source-pool, storage and process discrepancies remain under their existing canonical identities. This workunit changes only the canonical atomic routing of the already registered TCD-037 observer-interface phenomenon.
