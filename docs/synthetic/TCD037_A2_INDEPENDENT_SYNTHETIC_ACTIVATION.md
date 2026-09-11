# TCD-037-A2 independent synthetic activation qualification

Work unit: `ANIMO-SYNQ03`

Target: canonical child atom `TCD-037-A2`

Branch: `work/animo-synq03-tcd037-a2-independent-ghg-index0-activation`

Evidence class: `B1_SYNTHETIC_NOT_B2`

Independence class: `INDEPENDENT_IMPLEMENTATION_AND_ALGEBRAIC_ORACLE_FOR_CAUSALITY_AND_SCOPE`

## Purpose

SYNQ03 supplies the purpose-built synthetic activation evidence required to test the exact causal and scope claim for TCD-037-A2 when no compatible natural active-GHG revision-53 testcase is reasonably available.

It does **not** grant the GOV04 Tier-A waiver, does not admit A2, does not modify production code, and does not create historical reference evidence. A later `ANIMO-B3A06` must re-evaluate the complete Tier-A predicate against then-live authorities.

## Pinned authorities

- base: `ANIMO-B3D21@331f6ed91d4a1c15a23ae0c1ad75d1b540f61858`;
- aggregate: `ANIMO-RG05H@3e4247928bb43f30def951fa8804560636affbef`;
- canonical routing: `ANIMO-B3I07@54679c7555a963133dfd686648af334f479c5808`;
- accounting semantics: `ANIMO-RUNTIMEQ03@a3e822f8e97fe1312a7dfa73601a49ae7375163e`;
- synthetic-oracle policy: `ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121`;
- review governance: `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`.

Frozen source archive SHA-256 remains `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`; frozen testbank SHA-256 remains `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`; frozen `Outbal_calc.for` SHA-256 remains `4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981`. No frozen source bytes are redistributed by this workunit.

## Atomic semantic claim

RUNTIMEQ03 and B3I07 distinguish two source-owned CH4 timestep quantities:

`CH4_FORMATION_TOTAL = sum(QPrCH4(1:Nl) * St)`

and

`CH4_ATMOSPHERE_EMISSION_TOTAL = (QEmCH4Dif + QEmCH4Ebl + QEmCH4Flw + QEmCH4Plt) * St`.

They are not generally the same quantity. Dynamic CH4 storage and oxidation can separate formation from atmosphere transfer. Therefore one overloaded `AmCH4(0)` scalar cannot be the explicit owner of both meanings.

Within A2 only, the source-shaped observer target is:

`Btom(CH4e) increment = 10000 * CH4_ATMOSPHERE_EMISSION_TOTAL / Cfracom`

while the existing legacy total-dissimilation complement is represented by:

`Btom(CO2e) increment = D_OM - 10000 * CH4_FORMATION_TOTAL / Cfracom`.

The second expression is the **formation-side dissimilation complement only**. It is not a model-wide CO2 ledger and SYNQ03 makes no claim that it closes all carbon storage, oxidation, atmosphere transfer or other GHG carbon terms.

## Why a purpose-built synthetic activation is necessary

The supplied active-GHG `GHGMais` material remains incompatible with the frozen revision-53 parser/input lineage. SYNQ03 performs no translation and does not fabricate a natural revision-53 case.

Natural activation therefore remains:

`BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH`.

GOV04 permits a Tier-A activation predicate to be supported, where natural coverage is not reasonably available, by documented absence plus a purpose-built synthetic activation independently qualified for causality and scope. SYNQ03 addresses only that evidence predicate. Historical revision-53 behaviour remains exactly `UNKNOWN`.

## Independent discriminator design

The Fortran target in `tools/synq03/tcd037_a2_source_shaped_probe.f90` implements only the bounded A2 observer equations. The Python oracle in `tools/synq03/validate_tcd037_a2_synthetic.py` derives expected results independently with `fractions.Fraction`; it does not reuse ANIMO source code. Chosen inputs are dyadic, so expected outputs are exactly representable in binary64 and no empirical tolerance is needed.

The active discriminator uses `St=1/4`, `Cfracom=1/2`, `D_OM=16`, layer CH4 formation rates `[1/16384, 1/8192, 3/16384]`, and atmosphere-emission component rates `[1/32768, 1/16384, 1/32768, 0]`.

This gives:

- CH4 formation amount `3/32768`;
- CH4 atmosphere-emission amount `1/32768`;
- formation-side organic-matter equivalent `1875/1024`;
- emission-side organic-matter equivalent `625/1024`.

The two owners are therefore deliberately unequal in the primary case.

## Synthetic cases

`DIVERGENT_ACTIVE` activates both owners with unequal values. `FORMATION_ONLY` retains the same formation but sets atmosphere emission to zero. `EMISSION_ONLY` retains the same atmosphere emission but sets formation to zero. `EQUAL_TOTALS_CONTROL` makes the two independently supplied amounts numerically equal without treating their semantic ownership as identical. `RATE_TIME_EQUIVALENT` halves all rates and doubles the timestep, preserving both timestep amounts. `INACTIVE` supplies nonzero source values while disabling the observer branch.

The decisive causal relations are:

- `DIVERGENT_ACTIVE` versus `FORMATION_ONLY`: identical formation must preserve `Btom(CO2e)`, while changed atmosphere emission changes `Btom(CH4e)`;
- `DIVERGENT_ACTIVE` versus `EMISSION_ONLY`: identical atmosphere emission must preserve `Btom(CH4e)`, while changed formation changes `Btom(CO2e)`;
- `RATE_TIME_EQUIVALENT` must reproduce both target outputs exactly;
- `INACTIVE` must leave both target fields at their baselines.

These relations discriminate the two source owners directly rather than merely demonstrating that two arbitrary totals can differ.

## Expected-difference surface

Only these A2 observer surfaces may differ in an eventual correction:

- `Btom(CH4e)`;
- `Btom(CO2e)` formation-side dissimilation complement only.

The probe carries immutable sentinels for physical state, process flux, the already-admitted A1 observer surface, A3, A4 and an unrelated observer. Every sentinel must remain unchanged under every case. Restart state, solver behaviour and numerical policy are outside this correction and must not change.

## Evidence boundary

SYNQ03 is evidence qualification only. It does not:

- admit `TCD-037-A2` or parent `TCD-037`;
- alter the already admitted A1 object;
- admit A3 or A4;
- grant a Tier-A waiver;
- promote synthetic evidence to B2;
- claim historical fidelity or historical equivalence;
- translate the incompatible GHG testcase;
- modify production source or frozen B0;
- modify the canonical TCD register or reserve a new top-level TCD;
- compose TCD-032 through TCD-036;
- claim a full carbon-ledger closure;
- open B4, production migration or aggregate integration.

If exact-head CI qualifies this package, the only downstream conclusion is that the purpose-built A2 activation has been independently qualified for causality and scope at B1 synthetic evidence strength. `ANIMO-B3A06` must then recheck all live GOV04 Tier-A predicates before any waiver or admission route can advance.
