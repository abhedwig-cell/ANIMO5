# ANIMO-KT01 Provenance and Authority Map

## SWAP5 source-of-reuse

Repository: `abhedwig-cell/SWAP5`

Canonical authority: `integration/f-ci-canonical@992a5c657bfe10a10100f92e0cb77c4825ae65b6`

Pinned Status-A scientific production source authority: `50346642bd565f79134ea17d5462e544b354998c`

The required files have identical blobs at the pinned production source and the live canonical authority:

| Source path | Blob SHA |
| --- | --- |
| `src/transaction/mod_transaction_reference.f90` | `d5a71a526efaebd82054580c3186f8e3545db331` |
| `src/kernel/mod_kernel_transactions.f90` | `e4db4ede8162c8be877c8cad9f1babd57ba451b6` |
| `src/kernel/mod_kernel_committed_persistence.f90` | `ffd886c3401fc12739a456fe60a8741c12b9848b` |
| `src/runtime/mod_canonical_contracts.f90` | `3962c270a7579b7403764674302445fe15ef5f72` |
| `src/runtime/mod_canonical_interval_runtime.f90` | `0b50dda5caf3b73a82561d7b0ba1e92386a08fee` |
| `src/runtime/mod_a23bu_worker_execution_context.f90` | `f96a66c0185d96ba48258f8560db275fa7fed58c` |

These pins identify source provenance only. They do not transfer SWAP5 scientific, numerical or release authority to ANIMO5.

## ANIMO authority map actually relied upon

- central governance and B3/B4 boundary: `ANIMO-GOV06@7a7d3a1f5a5c07bf36b7e6e2915338dabde20660`
- historical evidence separation: `GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`
- review/admission policy: `GOV04@1bbe4c211197590f346803106e45dca5faae79fc`
- same-agent adversarial review policy: `GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`
- transaction/state ownership: `ARCH01@24f57d8daab828f88446a79bd6a276f2925c828b`
- restart/checkpoint sufficiency: `ARCH02@a079d93c965f6073586c55ee4b3544dd8873b723`
- mass/conservation observer separation: `ARCH03@bc27bd7cf0c8148b38768315d2fa54014f5a6cf9`
- feature/layout compatibility: `ARCH04@87930bbdfc413ad626176ce119f52ea409198f1d`
- external/coupled transaction boundary: `ARCH05@99b6098a19db405ce34928af89bb78b856dce7cd`
- normalized configuration identities: `ARCH06@ce3ea8089902dbc4bcbe3ff0224d30c2f8daf3a4`
- adapter qualification boundary: `ARCH07@7e6f7bcb492cd36bf7a852235e93b796a6d2a8f6`
- consolidated candidate architecture: `ARCHG01@981de99811806da362244440502218a84754157b`
- temporal architecture revalidation: `ARCHG02@db8183802631902f41aa5bec518a3c2e63e03ab7`
- synthetic transaction-runtime evidence: `TIMEQ01@ddd5de478165d51a53352033bc92c55ce672d3aa`
- concrete exact time candidate: `TIME02@b4d78cf32cb149cf50aa2b0a0fbefee571eee6b8`
- observed current state-family authority: `STATEQ07@26f6e61da328a5578b9c4b332de04eb99a3ac04f`
- observed current mass-family authority: `MASSQ04@3e0f8254d9cd7966a4491b3068d0239b8ccda5f9`
- observed current runtime-family authority: `RUNTIMEQ03@a3e822f8e97fe1312a7dfa73601a49ae7375163e`
- numerical qualification architecture: `NQ01@e558dff12b127e0662cad62beea7527b42ad89ac`
- B3 closure gate: `B3Q06@11e9bcdc6654e63f84875bf1f28dc54abe725700`, negative

## Authority/non-authority statements

`TIME02` is candidate time semantics, not canonical TIME admission.

`TIMEQ01` is synthetic nonproduction runtime evidence, not B2 historical evidence.

`ARCH01` through `ARCH07` and `ARCHG01/G02` constrain architecture compatibility; they do not themselves open B4.

`B3Q06` remains negative and GOV06 records B4 closed. KT01 does not mutate that state.

SWAP5 Status-A, its scientific production baseline and the pinned SWAP blobs are source-of-reuse evidence only. ANIMO remains responsible for its own semantic adaptation and qualification.
