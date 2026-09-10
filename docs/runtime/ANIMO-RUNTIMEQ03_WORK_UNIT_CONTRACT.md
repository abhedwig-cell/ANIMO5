# ANIMO-RUNTIMEQ03 — TCD-037 GHG Balance Observer Accounting-Semantics & Index-0 Producer Mapping Qualification

Branch: `work/animo-runtimeq03-tcd037-ghg-balance-accounting-semantics`

Authoring base: `ANIMO-RUNTIMEQ02@45e8073fa95035b3565bd8b373ac327915cf1af5`

Aggregate authority checked at start: `ANIMO-RG05G@4551b6b4c3f987b1247571d59f8489b2f1a71ba6`

Canonical routing authority checked at start: `ANIMO-B3I06@8f01f0cb366dfa8cc63a184d6f885100899a8cd9`

Governance authority: `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`

## Purpose

RUNTIMEQ03 consumes the qualified RUNTIMEQ02 ownership result for canonical `TCD-037` and determines the exact accounting meaning of the disconnected GHG observer inputs. The target is not production source correction. The target is to separate source-owned physical production, source-owned atmosphere-boundary emission, observer-local timestep amounts and overloaded index-0 meanings so that later B3 routing can be atomic and fail closed.

## Required questions

RUNTIMEQ03 must determine, from frozen/source-bound evidence:

1. what quantity is required by each `AmCH4` consumer;
2. what quantity is required by each `AmN2Odeni` consumer;
3. whether `AmN2Onitr(0)` has the same semantics as its consumer at `Bani(N2Oe)`;
4. which existing GHG process variables own production, reduction and atmosphere emission;
5. whether layer elements and index 0 can legitimately share one producer/lifetime contract;
6. whether a correction remains accounting/reporting-only;
7. whether the parent TCD is atomic enough for a GOV04 Tier-A path or requires child-atom routing first.

## Evidence requirements

Use exact frozen source identities and the existing source-complete RUNTIMEQ02 writer/reader inventory. At minimum reconcile:

- `Outbal_calc.for` GHG declarations, local nitrification amount construction, CH4 formation accounting, CH4/CO2 atmosphere reporting and N2O evolution/emission accounting;
- `outbal2.inc` slot meanings;
- `Outbal_write.for` human-readable balance labels and units;
- `Outsel.for` independent GHG output calculations for production, reduction and atmosphere emission;
- `ghg_ch4.for` physical CH4 production and atmosphere-emission owners;
- `ghg_n2o.for` physical N2O production, reduction and atmosphere-emission owners;
- GHG01 ledger and theory reconciliation;
- MASSQ02 observer/state ownership boundary;
- GOV04 risk-tier rules.

A bounded executable B1 discriminator may be used to prove that formation and atmosphere emission are independently variable and therefore cannot share one undifferentiated index-0 semantic owner. Such a probe is causal evidence only and is not B2 historical reference evidence.

## Hard boundaries

RUNTIMEQ03 must not:

- edit frozen or production source;
- compose or correct TCD-032 through TCD-036;
- repair GHG source-pool conservation, GHG restart state, lower air boundary or other GHG TCDs;
- change the canonical TCD register;
- allocate canonical child atoms itself;
- admit any TCD or child atom;
- open B4;
- create RG05H;
- fabricate a revision-53-compatible active GHG historical testcase;
- promote B1 evidence to B2;
- infer historical Intel output values.

## Decision rule

If source semantics prove that the disconnected working arrays actually combine more than one physical/accounting meaning, RUNTIMEQ03 must explicitly reject a single-array/single-owner correction contract and hand off a bounded atomization proposal to the next canonical routing workunit.

If all later correction candidates are genuinely observer-only, their risk tier may be re-evaluated under GOV04 after the source-meaning ambiguity has been removed. Tier-A waiver eligibility must still fail closed on atomicity, activation evidence, expected-difference and all other GOV04 predicates.

## Stop condition

Stop after:

- exact semantic producer mapping;
- index-0 collision disposition;
- expected-difference surface definition;
- provisional GOV04 risk classification at the atomic candidate level;
- validator and scope guard;
- green CI;
- exact next routing workunit.

No production patch and no scientific admission are permitted in RUNTIMEQ03.
