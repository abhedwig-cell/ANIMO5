# ANIMO-RUNTIMEQ02 Work Unit Contract

Work unit: `ANIMO-RUNTIMEQ02`

Title: `TCD-037 GHG Balance Working-Array Producer, Lifetime & Observer Ownership Qualification`

Branch: `work/animo-runtimeq02-tcd037-ghg-balance-array-lifetime`

Authoring base: `ANIMO-RG05G@4551b6b4c3f987b1247571d59f8489b2f1a71ba6`

## Purpose

Qualify the revision-53 runtime and ownership semantics of the GHG balance working-array interface recorded as canonical `TCD-037` before any arithmetic correction or scientific admission is considered.

The work unit answers only:

- who writes `AmCH4`, `AmN2Odeni` and the comparison array `AmN2Onitr`;
- when the arrays are initialized relative to first read;
- whether their valid lifetime is event-local, timestep-local, iteration-local or persistent;
- who consumes them;
- whether `Outbal_calc` observes physical process state or mutates it through this seam;
- whether stale or undefined values are source-reachable;
- whether restart/checkpoint ownership is implicated;
- which GOV04 risk tier follows from the qualified ownership result.

## Authorities rechecked before branch creation

- aggregate central regie: `ANIMO-RG05G@4551b6b4c3f987b1247571d59f8489b2f1a71ba6`;
- risk-tier governance: `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`;
- scientific admission framework: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- GHG source qualification: `ANIMO-GHG01@dac7b7b5c591b781b82ec968896edb5957664c88`;
- BUILDQ01: `5e5c4c2bc678a11e87f358ac6163ba13409ee565`;
- BUILDQ02: `e7c675c6654026d5c12836f36f2fd347e9d547c2`;
- BUILDQ03: `5e06473bc2bb1df6cf4e449d8d6aa04da35c7d47`;
- BUILDQ04: `0ae1e58f80ca01c1b6eced7ac0d6e5c031827676`;
- MASSQ02: `56a11b524d03c33ee4ab9b1cd13b2cd523d543fc`;
- current canonical routing authority: `ANIMO-B3I06@8f01f0cb366dfa8cc63a184d6f885100899a8cd9`.

The current routing chain was also rechecked through B3I01, B3I02, B3I03, B3I04 and B3I05. The machine-readable matrix records the exact observed heads.

No dedicated TCD-037 or RUNTIMEQ02 branch existed before this branch was created. GitHub issue #17 remains the umbrella intake issue through which TCD-028..037 were appended. No dedicated issue matching `AmCH4`, `AmN2Odeni` or GHG balance observer ownership was found at intake.

## Frozen evidence

Source evidence is bound to B0 object `ANIMO-B0-SRC-41553-R53`, supplied filename `ANIMO_4.1.5.53(3).zip`, SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

The relevant frozen `Outbal_calc.for` SHA-256 is:

`4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981`

The public repository does not receive the raw B0 source bytes.

EG01 remains an evidence-retention contract with external controlled-storage implementation pending. This work unit therefore uses the frozen digest identity and source coordinates, not a claim that public Git storage is the B0 custodian.

## Evidence requirements

The work unit must fail closed unless it records and validates:

1. complete active writer inventory for all three working arrays;
2. complete active reader inventory;
3. first-write-before-first-read status;
4. caller/control-flow reachability;
5. active-GHG and inactive-GHG discrimination;
6. a multi-call lifetime discriminator;
7. a counterfactual persistent-storage discriminator to expose stale-value risk without treating persistence as intended semantics;
8. physical-state non-interference for the scoped observer seam;
9. restart/checkpoint ownership classification;
10. an expected-difference contract;
11. GOV04 tier classification after, not before, ownership qualification;
12. a scope guard that prevents production source, canonical register, B4, RG05H or unrelated TCD composition changes.

A revision-53-compatible natural active-GHG case is preferred but is not silently manufactured. The supplied `GHGMais` case is lineage-incompatible with revision 53 according to GHG01 and remains unusable as natural B1 qualification evidence. A source-shaped synthetic runtime discriminator may be used only as B1 causal evidence.

## Hard exclusions

This work unit does not:

- change production Fortran source;
- repair TCD-037 arithmetic or interfaces;
- compose `TCD-032` through `TCD-036`;
- reopen or broaden TCD-011;
- allocate a new TCD;
- perform scientific admission;
- open B4;
- update or create RG05H;
- claim historical Intel numerical behaviour;
- promote compiler-local persistence to model state;
- translate the incompatible GHGMais testcase.

## Closeout rule

The work unit may close as a runtime/ownership qualification if the source ownership and lifetime question is resolved even when the intended accounting mapping remains unresolved. In that case it must remain fail closed for admission readiness and route the exact remaining accounting-semantics question to a separate atomic work unit.

A Tier-A combined readiness/admission route is allowed only if every GOV04 Tier-A waiver predicate is demonstrably PASS. If exact accounting ownership or expected-difference semantics remains unknown, Tier A is unavailable.