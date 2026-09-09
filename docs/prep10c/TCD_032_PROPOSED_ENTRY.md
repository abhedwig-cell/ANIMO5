# Proposed TCD-032 register entry

This entry is prepared for later integration into `docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv`. PREP10C keeps it separate to avoid mutating the shared discrepancy register while parallel preparatory branches remain active.

| field | value |
|---|---|
| ID | `TCD-032` |
| process | stable-DOM/DON/DOP redistribution during ploughing |
| theory | every event-local redistribution accumulator must be initialized from the current event only; an internal ploughing redistribution must not inherit mass from a prior management event |
| documentation | supplied ANIMO 4.0 guide does not document the revision-53 separate stable-DOM state family or this accumulator implementation |
| legacy implementation | revision-53 `Addit.for` declares `SuStdiorma`, `SuStdiorni`, `SuStdiorpo`; first plough-branch assignments self-read them at lines 475, 477 and 479 with no explicit preceding definition/reset; redistributed `CoStdior*` state then consumes those totals |
| ANIMO5 implementation | not started |
| difference | event-local accumulators can retain previous-event values under storage semantics that preserve local state |
| impact | controlled B0-derived diagnostic descendants show inter-event carryover and changed later outputs for C, N and conditional P under the current GNU diagnostic contract |
| classification | `CONFIRMED_LEGACY_EVENT_TRANSACTION_STATE_DEFECT_CURRENT_GNU_CAUSAL_HISTORICAL_NATIVE_OPEN` |
| evidence | `Addit.for`; `PREP10_STABLE_DOM_PLOUGH_ACCUMULATOR_AUDIT.json`; `PREP10_STABLE_DOM_CAUSAL_ACTIVATION_MATRIX.json`; PREP10 GNU storage-semantics probe |
| decision | retain frozen behavior as defect evidence; require historical or independently admitted reference contract before starting corrected-legacy lineage; candidate event reset must be admitted separately and reconciled with conserved-state/transfer-ledger evidence |
| status | `OPEN` |

The proposed identifier is based on the current live shared register ending at `TCD-031`. If another workstream allocates `TCD-032` before integration, this entry must be renumbered rather than overwriting that work.