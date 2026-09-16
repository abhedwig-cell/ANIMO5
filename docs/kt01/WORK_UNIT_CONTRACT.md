# ANIMO-KT01 Work Unit Contract

Workunit: `ANIMO-KT01 — SWAP5 Runtime Substrate Reuse Qualification & Nonproduction ANIMO Transaction Prototype`

Execution discipline: `RECONCILE -> CLASSIFY -> PROTOTYPE -> QUALIFY -> CLOSE`.

This is a bounded architecture/runtime-reuse workunit. It has no B3, B4 or production ADMIT phase.

## Scope

KT01 may inspect qualified SWAP5 runtime mechanics and materialize only a scientifically neutral, ANIMO-native executable prototype under `prototype/kt01/`. It may add focused tests, CI, provenance, review and qualification records. It may not modify ANIMO scientific production source or introduce a runtime dependency on SWAP5.

Research maturity: `RESEARCH_ISOLATED` until KT01 itself closes. A positive KT01 closeout may qualify only the isolated nonproduction runtime substrate prototype. No transition to `PRODUCTION_ADMITTED` is permitted here.

## Frozen consumed authorities

- central regie base: `ANIMO-GOV06@7a7d3a1f5a5c07bf36b7e6e2915338dabde20660`
- governance: `GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`, `GOV04@1bbe4c211197590f346803106e45dca5faae79fc`, `GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`
- architecture: `ARCH01@24f57d8daab828f88446a79bd6a276f2925c828b`, `ARCH02@a079d93c965f6073586c55ee4b3544dd8873b723`, `ARCH03@bc27bd7cf0c8148b38768315d2fa54014f5a6cf9`, `ARCH04@87930bbdfc413ad626176ce119f52ea409198f1d`, `ARCH05@99b6098a19db405ce34928af89bb78b856dce7cd`, `ARCH06@ce3ea8089902dbc4bcbe3ff0224d30c2f8daf3a4`, `ARCH07@7e6f7bcb492cd36bf7a852235e93b796a6d2a8f6`, `ARCHG01@981de99811806da362244440502218a84754157b`, `ARCHG02@db8183802631902f41aa5bec518a3c2e63e03ab7`
- synthetic runtime evidence: `TIMEQ01@ddd5de478165d51a53352033bc92c55ce672d3aa`
- candidate exact time semantics: `TIME02@b4d78cf32cb149cf50aa2b0a0fbefee571eee6b8`, with `canonical_time_admitted=false`
- current observed qualification-family authorities relevant to KT01: `STATEQ07@26f6e61da328a5578b9c4b332de04eb99a3ac04f`, `MASSQ04@3e0f8254d9cd7966a4491b3068d0239b8ccda5f9`, `RUNTIMEQ03@a3e822f8e97fe1312a7dfa73601a49ae7375163e`, `NQ01@e558dff12b127e0662cad62beea7527b42ad89ac`
- current B3 closure gate: `B3Q06@11e9bcdc6654e63f84875bf1f28dc54abe725700`, qualified negative; B4 remains closed
- SWAP5 canonical: `integration/f-ci-canonical@992a5c657bfe10a10100f92e0cb77c4825ae65b6`
- SWAP5 Status-A scientific production source authority: `50346642bd565f79134ea17d5462e544b354998c`

TIME02 is newer evidence/authority consumed by pin; it is not used to redefine the GOV06 branch base. The KT01 branch therefore starts from the legitimate current central regie authority, not from a merely newer unrelated branch.

## Owned semantic surface

KT01 owns only an isolated prototype representation of generic runtime mechanics: exact bounded time backend, accepted/trial/checkpoint carriers, transaction publication/rollback mechanics, generic acceptance hooks, interval orchestration, committed-only persistence and worker-local scratch. Those contracts are prototype-local and do not mutate the central ANIMO production authority surface.

## Must not own

KT01 must not own or change scientific process equations, process ordering, B3 admission, B4, production migration, canonical TIME admission, final conserved-quantity registry, numerical tolerances, hydrology/crop physics, SWAP physics, shared cross-model runtime libraries, or historical ANIMO behaviour.

## Explicit exclusions

No Richards/HeadCalc or hydraulic constitutive laws; groundwater/MODFLOW; EB; Snow; ROSS/RossFast; WOFOST/crop, ET, drainage or surface-water physics; SWAP energy-ledger or water-specific acceptance; SWAP fallback/step-doubling policy; SWAP calendar/file formats/persistent physical layout; ANIMO NH4/NO3/P/C/OM/GHG/crop/transport equations; production source changes; B2 claims; Status A/AA claims.

## Fail-closed rule

Any semantic reuse that would require weakening TIME02, inventing ANIMO science, importing SWAP-specific physics/policy, opening B4, or treating evidence as authority is rejected or retained as design-only. Negative reuse classification is a valid KT01 result.
