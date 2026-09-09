# ANIMO5 ARCHG01 RG02 authority recheck

Work unit: `ANIMO-ARCHG01`

Status: `LIVE_AUTHORITY_RECHECK_AFTER_INITIAL_ARCHG01_CLOSEOUT`

## Why this note exists

The first ARCHG01 consolidation observed `work/animo-rg02-branch-authority-integration` while it still pointed at the inherited RG01 closeout `662bca8aff40f4dca1f6ccdde6bef6274c6bede2`. During this continuation pass the same RG02 branch had advanced to `8d59b0cabf2001d07aa37eee1a76affaad181dbb` and now contained the persisted RG02 authority register and status.

The initial ARCHG01 fallback authority check must therefore be superseded by this later live evidence for ARCH01-ARCH07.

## RG02 result relevant to ARCHG01

RG02 is not globally qualified. Its own decision is `BLOCKED_UNRESOLVED_PARALLEL_LINEAGE_COLLISIONS`, mainly because PREP07-PREP10 and post-TCD027 local/canonical evidence still require reconciliation.

That blocked global status does not make every authority decision unusable. RG02 explicitly classifies each of ARCH01 through ARCH07 as `AUTHORITATIVE_CANDIDATE_DESIGN` at the same heads used by ARCHG01:

| Work unit | RG02 authoritative branch | Head |
|---|---|---|
| ARCH01 | `work/animo-arch01-state-ownership-typed-transfers` | `24f57d8daab828f88446a79bd6a276f2925c828b` |
| ARCH02 | `work/animo-arch02-restart-checkpoint-sufficiency` | `a079d93c965f6073586c55ee4b3544dd8873b723` |
| ARCH03 | `work/animo-arch03-mass-ledger-observer` | `bc27bd7cf0c8148b38768315d2fa54014f5a6cf9` |
| ARCH04 | `work/animo-arch04-feature-activation-state-allocation` | `87930bbdfc413ad626176ce119f52ea409198f1d` |
| ARCH05 | `work/animo-arch05-external-exchange-contracts` | `99b6098a19db405ce34928af89bb78b856dce7cd` |
| ARCH06 | `work/animo-arch06-normalized-model-configuration` | `ce3ea8089902dbc4bcbe3ff0224d30c2f8daf3a4` |
| ARCH07 | `work/animo-arch07-adapter-qualification-spec` | `7e6f7bcb492cd36bf7a852235e93b796a6d2a8f6` |

This independently confirms the ARCH01-ARCH07 authority chain used by the consolidation.

## ARCHG01 entry in the RG02 snapshot

The RG02 authority-register snapshot classified ARCHG01 as `UNRESOLVED_REQUIRES_RECONCILIATION` because, at that snapshot, the ARCHG01 ref was still identical to ARCH07 and no independent ARCHG01 status existed.

That observation was correct for the RG02 snapshot. It is no longer a current statement about the branch after commit `92812896b6a91b422fcbd9bf5e843da5cfc0f278`, which added the independent ARCHG01 contract/deliverables/status.

ARCHG01 does not rewrite RG02 history to hide this timing. Instead it records:

- RG02's ARCH01-ARCH07 authority decisions as current supporting authority evidence;
- RG02's ARCHG01 unresolved entry as snapshot-stale after the later ARCHG01 persistence;
- the need for RG02 to refresh its inventory before it can itself classify the new ARCHG01 head.

Until such a refresh, ARCHG01's own candidate qualification does not claim canonical integration authority beyond its branch.

## Governance consequence

The consolidated architecture remains a candidate design. RG02's blocked convergence state reinforces, rather than weakens, the rule that this branch must not be merged wholesale as a canonical architecture baseline while evidence-lineage collisions remain unresolved.
