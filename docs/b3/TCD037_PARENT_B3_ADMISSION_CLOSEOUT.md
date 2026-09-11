# ANIMO-B3D27 — TCD-037 parent B3 admission closeout

## Decision

The qualified parent disposition is:

`ADMIT_TCD037_PARENT_GHG_OBSERVER_COMPOSITION_WITH_HISTORICAL_UNCERTAINTY_GOV05_TIER_D`

This decision becomes authoritative only when the B3D27 exact-head workflow is green on the final closeout commit. Until that exact-final check succeeds, the machine-readable status remains `PERSISTED_VALIDATION_PENDING`.

The admission is narrow. TCD-037 is admitted as a composed observer-accounting correction contract, not as a complete GHG process model, climate CO2-equivalent ledger, whole-model conservation theorem, restart theorem, B4 decision or production authorization.

## Qualified composition

- CH4 layer formation uses `QPrCH4(Ln)*St` in the layer formation/partition observer fields.
- CH4 atmosphere exchange uses the signed sum of `QEmCH4Dif`, `QEmCH4Ebl`, `QEmCH4Flw` and `QEmCH4Plt` times `St` for `Btom(CH4e)`.
- The existing `Btom(CO2e)` dissimilation complement uses total CH4 formation, not atmosphere exchange; no full CO2 ledger is claimed.
- N2O denitrification formation uses `QPrN2Oden(Ln)*St` for `Bani(N2Od)`.
- N2O atmosphere exchange uses the signed sum of `QEmN2ODif` and `QEmN2OFlw` times `St` for `Bani(N2Oe)`.
- Existing nitrification production and the `QRdN2O` reduction sink remain distinct and unchanged.

Negative atmosphere exchange remains valid and means uptake by the soil. Carbon/organic-matter and nitrogen balance units remain separate. No cross-element GHG total is introduced.

## Governance result

The strictest applicable GOV04 trigger is Tier D because this is parent-level composition of four admitted child atoms. The immutable composition authoring head is `17387b7282a6f5b40fec290bd4c28cc6cef8f767`. It passed a GOV05 same-agent adversarial review persisted at `f2d209754b0f96ac20b9642de91bcfbda1116cab`.

That review is `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`; it is not genuinely independent.

A first authoring checkpoint was deliberately superseded before review disposition because a pre-review attack identified the absence of a separate executable parent-composition proof. The refrozen authoring package therefore includes an exact-rational oracle that tests semantic independence, signed exchange, rate-time amount equivalence and noninterference without claiming B2 or natural-runtime strength.

## Residual uncertainty

Historical reference behaviour remains unknown. The supplied active-GHG testcase is still source-lineage incompatible with the frozen revision-53 parser. Neither uncertainty is promoted away by the synthetic parent oracle. Complete GHG carbon/N2O closure and arbitrary split-run identity of balance-reporting accumulators are not admitted.

## Hard stop

No production source, B0, child admission, TCD registry, RG05I aggregate, B4 surface or production-migration authority is changed in B3D27.

If the final exact-head CI is green, B3D25, B3D26 and B3D27 form a three-admission post-RG05I batch. The only next aggregate action is therefore an explicit handoff to a separate `ANIMO-RG05J` workunit. RG05J is not created or executed here.
