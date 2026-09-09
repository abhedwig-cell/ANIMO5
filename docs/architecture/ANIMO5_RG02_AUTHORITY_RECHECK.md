# ANIMO5 ARCHG01 RG02 authority recheck

Work unit: `ANIMO-ARCHG01`

Status: `LIVE_AUTHORITY_RECHECK_RG02_G5_PENDING`

## Current RG02 state

The live RG02 branch `work/animo-rg02-branch-authority-integration` is now at `ec8709cd6a37c985ab7452bc0f2e6e64a430db6a` with decision:

`QUALIFIED_BRANCH_AUTHORITY_GOVERNANCE_CONVERGENCE_AND_PREPARATORY_AGGREGATE_G5_PENDING`

RG02 is therefore no longer globally blocked by the earlier PREP07 through PREP10 lineage collisions. It has completed the observed local-ID reconciliation, governance-only consolidation, provenance-qualified supplemental evidence transplant and a provenance-qualified preparatory aggregate. None of those actions constitutes B2, B3, B4 or production admission.

## ARCH01 through ARCH07 authority

RG02 confirms the same authoritative candidate-design branches and heads used by ARCHG01:

| Work unit | Branch | Head |
|---|---|---|
| ARCH01 | `work/animo-arch01-state-ownership-typed-transfers` | `24f57d8daab828f88446a79bd6a276f2925c828b` |
| ARCH02 | `work/animo-arch02-restart-checkpoint-sufficiency` | `a079d93c965f6073586c55ee4b3544dd8873b723` |
| ARCH03 | `work/animo-arch03-mass-ledger-observer` | `bc27bd7cf0c8148b38768315d2fa54014f5a6cf9` |
| ARCH04 | `work/animo-arch04-feature-activation-state-allocation` | `87930bbdfc413ad626176ce119f52ea409198f1d` |
| ARCH05 | `work/animo-arch05-external-exchange-contracts` | `99b6098a19db405ce34928af89bb78b856dce7cd` |
| ARCH06 | `work/animo-arch06-normalized-model-configuration` | `ce3ea8089902dbc4bcbe3ff0224d30c2f8daf3a4` |
| ARCH07 | `work/animo-arch07-adapter-qualification-spec` | `7e6f7bcb492cd36bf7a852235e93b796a6d2a8f6` |

## Historical ARCHG01 entry

RG02 still records ARCHG01 among refs that were unresolved at its earlier authority snapshot. That statement is explicitly historical. At that snapshot the ARCHG01 branch had not yet persisted an independent work-unit result.

ARCHG01 subsequently persisted its initial consolidation at `92812896b6a91b422fcbd9bf5e843da5cfc0f278`, hardened it at `5cef7969ee921acd2044521cc7636d388aa02efe`, and now performs post-TS01 revalidation.

RG02's current status explicitly states that ARCHG01 requires a live authority refresh in G5 if independent persisted work now exists.

## G5 consequence

RG02 identifies the next safe gate as:

`G5_INDEPENDENT_THEORY_TESTING_NUMERICAL_TEMPORAL_SCIENCE_STREAM_ATTACHMENT`

ARCHG01 should therefore not rewrite RG02's historical authority register or merge itself into RG02. The safe action is to provide a provenance-explicit G5 attachment packet containing:

- exact ARCHG01 branch and head;
- exact candidate decision and non-admissions;
- exact ARCH01 through ARCH07 lineage references;
- qualified TS01 temporal closeout reference;
- theory, testcase, numerical and B3 governance references used by the architecture;
- frozen B0 identities;
- unresolved B2/B3/production gates;
- file-level attachment manifest.

The packet is provided in `integration/animo-architecture/ANIMO-ARCHG01_G5_ATTACHMENT.json` with a human-readable companion note.

## Governance boundary

The G5 packet is suitable for live RG02 authority refresh and stream attachment. It is not a branch merge, does not change the canonical TCD register, does not upgrade evidence strength and does not admit a canonical architecture, B3 baseline, B4 baseline or production migration.
