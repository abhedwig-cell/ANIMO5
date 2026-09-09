# PREP08/PREP09 discrepancy-lineage reconciliation

Status: `RECONCILED_WITHOUT_HISTORY_REWRITE`.

## Problem

Two parallel preparatory lineages allocated `TCD-030` independently after a common TCD-028/TCD-029 ancestor.

### Sibling lineage A

Branch:

`work/animo-prep08-transfer-probes`

Closeout:

`340db9d91e71c906143efe877313149c5af36a24`

Its branch-local `TCD-030` is:

`SOURCE_CONFIRMED_EXUDATE_HUMUS_ELEMENT_FRACTION_REDISPATCH_SEQUENCING_GAP_TESTBANK_UNEXERCISED`.

Primary evidence:

- `docs/prep08/TRANSFER_EDGE_DIAGNOSTIC_PROBES.md`, blob `fc8b02659bf9aa08f8ba6e84cb8123286aa8eac7`;
- `integration/animo-prep/PREP08_TRANSFER_EDGE_PROBES.json`, blob `82176353810bf72697544a0406003d7864b18bda`.

### Canonical lineage B

PREP09 branch:

`work/animo-prep09-option-contract-audit`

Closeout:

`0ae0e2180cf0569f8ea22319aa9ccb54ebca3210`

This lineage allocated `TCD-030` to the independently confirmed AerationModel=2 semantic alias to option 0. PREP10 starts from this PREP09 closeout.

## Resolution

No closed branch is rewritten.

Canonical numbering from PREP10 onward is:

- `TCD-030`: aeration option 2 semantic alias to option 0;
- `TCD-031`: exudate-humus N/P element-fraction redistribution sequencing gap.

Therefore:

```text
work/animo-prep08-transfer-probes:TCD-030
    -> canonical:TCD-031
```

The old identifier remains valid only as a historical branch-local reference to the frozen sibling-branch evidence. It must not be used as the canonical identifier in new evidence.

## Why TCD-031 remains a distinct finding

The sequencing gap is not a duplicate of TCD-028.

TCD-028 concerns duplicate generic `Adhuexpl` bookkeeping during ploughing.

The TCD-031 source algebra concerns the temporal side of the N/P fraction used for exudate-derived humus storage:

```text
physical state before = old_Huex * old_fraction
physical state after  = new_Huex * new_fraction
```

Revision-53 explicit element transfer arrays are updated before the redistributed `Nifrhu/Pofrhu` values are recomputed, yielding the form:

```text
new_Huex * old_fraction - old_Huex * old_fraction
```

while generic post-hoc reconstruction yields:

```text
(new_Huex - old_Huex) * new_fraction
```

Neither is generally equal to the exact state difference when the pre-plough element fractions are spatially non-uniform.

The existing PREP08 activation had effectively uniform differentiating fractions and therefore did not measure a behavioural magnitude for this seam. The finding remains source-confirmed and testbank-unexercised pending a controlled non-uniform pre-plough fraction probe.

## Governance consequence

Discrepancy identifiers are globally unique only on the canonical lineage, not automatically across concurrent unmerged branches. Future parallel workunits must either reserve IDs centrally before use or persist branch-local provisional identifiers that are explicitly reconciled before serial continuation.

Production migration remains `NOT_ADMITTED`.
