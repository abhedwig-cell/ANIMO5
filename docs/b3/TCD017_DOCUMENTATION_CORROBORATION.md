# TCD-017 documentation corroboration

Work unit relation: `ANIMO-B3A02`

Target: `TCD-017`

Purpose: add documentation-level corroboration without changing the frozen B3A02 admission-readiness object, without performing independent second-line review, and without admitting corrected legacy behaviour.

Base B3A02 head:

`21d093f563264743942275d9effa6e0251badad7`

Frozen primary review object remains:

`3ff8f4bda77c631b82110b83317c6a9b42b867ad`

## Documentation identity

Source:

Renaud, L.V., Roelsma, J. and Groenendijk, P. (2005), *User's guide of the ANIMO 4.0 nutrient leaching model*, Alterra Report 224.

SHA-256 of the supplied PDF:

`ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`

This is the same documentation identity already recorded by PREP02R.

The guide documents ANIMO 4.0, not revision 4.1.5 revision 53. It is therefore used only as documentation corroboration of model semantics and output ownership. It is not B2 historical executable evidence and does not override frozen B0 source evidence.

## 1. Top reservoir and ploughing semantics

The guide describes an extra artificial reservoir on top of the compartment discretization for manure and fertilizer additions. Dissolved substances can reside in this top reservoir before entering the soil profile.

In the MANAGEMENT.INP specification, the ploughing parameter `PL(x)` is described as the number of model compartments to be redistributed, and the guide states that compartment 0 is always emptied when `PL(x) > 0`.

This independently corroborates the B3A02 source interpretation that a ploughing event can remove dissolved organic P from the separate top reservoir and redistribute it into soil compartments.

It does not by itself prove the exact revision-53 algebra. That remains source-bound to `Addit.for` and the measured PREP01/PREP02 evidence.

## 2. Organic-P mass-balance ownership

Annex 2, Table 22, defines the organic-phosphorus mass balance. It explicitly distinguishes:

- beginning and ending dissolved organic-P storage (`BAPOST`, `BAPOSTT`);
- beginning and ending solid organic-P storage (`BAPOSD`, `BAPOSDT`);
- organic-P balance deviation (`BAPODV`) and cumulative deviation (`BAPODVCU`);
- input/output terms accumulated over the selected balance period.

The same table includes an organic-P balance input term `BAPOIC`, described as `incorporation`, alongside additions, crop residues and exudates.

Separately, example balance output in the guide exposes a `Redistrib` line for both organic P and PO4-P. This shows that redistribution/incorporation bookkeeping is an intended reporting surface of the phosphorus balance, not an implicit physical source or sink.

The guide does not expose the internal array name `Bapo(Redi,Ly)` or the revision-53 `Addiorpotoppl` omission. Therefore this evidence corroborates the ledger category and control-volume meaning, but the exact TCD-017 defect remains source- and runtime-qualified by PREP01/PREP02.

## 3. Balance accumulation is reporting logic

Annex 5 states that `OUTBAL_CALC` accumulates mass-balance terms for water, organic matter, nitrate-N, ammonium-N, organic-N, mineral-P and organic-P, while `OUTBAL_WRITE` writes those terms to output files.

This documentation supports the B3A02 Class-A boundary: `Outbal_calc.for` is a reporting/accounting accumulation surface. A one-line addition to the organic-P balance accumulator is therefore structurally distinct from the physical redistribution that occurs in `ADDIT`.

Again, this is corroboration only. The non-interference proof still depends on the revision-53 source write set and the natural activated comparison.

## 4. Example output confirms separation of physical storage and ledger terms

The guide's phosphorus balance example reports, separately:

- `Redistrib`;
- `Incorporation`;
- additions and crop residues;
- final and initial physical storage;
- storage change;
- input-output difference;
- balance deviation.

This separation is consistent with the B3A02 interpretation that redistribution is represented in the public ledger as a bookkeeping term while physical storage is measured independently at the beginning and end of the balance period.

A missing side of an internal redistribution can therefore create a balance deviation without implying that physical total P changed.

## 5. Consequence for TCD-017 readiness

The documentation adds three useful cross-checks:

1. compartment 0 is explicitly part of the management/ploughing semantics and is emptied during ploughing;
2. organic-P redistribution/incorporation is an intended mass-balance reporting category;
3. `OUTBAL_CALC` is documented as the accumulator for balance terms, distinct from model-state evolution.

These observations are consistent with the frozen B3A02 causal claim:

`Addiorpotoppl source loss + layer Addiorpopl redistribution = internal transfer`, while the public `Bapo` redistribution ledger currently omits the top-reservoir side.

No contradictory documentation evidence was found in the reviewed ANIMO 4.0 guide.

## Limits

This document does not establish:

- historical revision-53 executable behaviour;
- exact equality between ANIMO 4.0 and revision-53 implementation details;
- a new B2 route;
- independent second-line review;
- corrected-legacy admission;
- permission to patch production source.

The governing B3A02 status therefore remains:

`QUALIFIED_TCD017_CLASS_A_ADMISSION_READINESS_ROUTE_AND_INDEPENDENT_REVIEW_PENDING`
