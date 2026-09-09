# ANIMO-PREP10 — Stable-DOM plough accumulator audit

Status: `PERSISTED_SOURCE_CHECKPOINT_DYNAMIC_CAUSALITY_OPEN`.

## Purpose

PREP10 follows the revision-53 stable dissolved-organic matter ploughing path in `Addit.for`, with particular attention to whether event-local redistribution accumulators are reset before each management event.

Frozen source and supplied testcase bytes remain immutable. No production correction is admitted.

## Frozen identity

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

## Source finding

`Addit.for` declares scalar local accumulators:

```fortran
Real :: SuStdiorma, SuStdiorni, SuStdiorpo
```

During every `Pl(I)>0` event the routine accumulates stable DOM/DON/DOP mass into them:

```fortran
SuStdiorma = SuStdiorma + CoStdiorma(Ln)*He(Ln)*(mofro(Ln)+socfsdo(Ln)*Rhbd(Ln))
SuStdiorni = SuStdiorni + CoStdiorni(Ln)*He(Ln)*(mofro(Ln)+socfsdo(Ln)*Rhbd(Ln))
SuStdiorpo = SuStdiorpo + CoStdiorpo(Ln)*He(Ln)*(mofro(Ln)+socfsdo(Ln)*Rhbd(Ln))
```

and redistributes the resulting totals back to `CoStdior*`.

Unlike the adjacent event-local accumulators `Sumo`, `Suex`, `Suhuex`, `Suhuos`, `Suhuosni`, `Suhuospo`, `Supopr`, `Supocxfa` and `Supocxsl`, no explicit assignment to zero has been found for `SuStdiorma`, `SuStdiorni` or `SuStdiorpo` anywhere in `Addit.for`.

This is a potentially material state/transaction defect, but PREP10 does not yet promote it. Its behaviour depends on local-variable storage/initialization semantics and on whether stable DOM is non-zero at repeated plough events. The next step is a diagnostic observer and controlled activation under the already documented GNU diagnostic contract, followed by a build-semantics sensitivity check.
