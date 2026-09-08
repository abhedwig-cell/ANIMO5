# ANIMO-PREP06 — Organic-P detailed redistribution accumulator defect

Status: `CONFIRMED_LEGACY_DETAILED_LEDGER_ACCUMULATOR_DEFECT_ACCOUNTING_ONLY`.

The frozen revision-53 source and supplied testcases remain unchanged. The correction probe used only a temporary diagnostic source copy.

## Source defect

In the ploughing redistribution block of `Outbal_calc.for`, the organic-matter and nitrogen detailed ledgers accumulate exudate redistribution into their own slot:

```fortran
Bafom(24,Ly) = Bafom(24,Ly) + Adexpl(I,Ln)*Z
Bafon(24,Ly) = Bafon(24,Ly) + Dum
```

The phosphorus analogue instead reads:

```fortran
Bafop(24,Ly) = Bafop(25,Ly) + Dum
```

where slot 24 is documented as exudate redistribution and slot 25 as fresh-organic-matter redistribution.

Thus every update of the P exudate-redistribution accumulator is seeded from the wrong detailed-ledger slot rather than from its own prior value.

The total organic-P ledger `Bapo(Redi,Ly)` is updated separately with the correct `Dum` and is not affected by this accumulator typo.

## Natural reachability

The supplied LWKM case naturally reaches the affected route. In `transfopGP.Out`, the 1997 ploughing period reports:

```text
redis_EXP = -7.0644 kg/ha P
redis_OP  ≈ 8.49e-15 kg/ha P
redis_DOP = +0.044113 kg/ha P
redis_HUP ≈ -7.28e-14 kg/ha P
```

The same erroneous `redis_EXP` value occurs in the corresponding RP and TP detailed transformation outputs.

For a balance volume containing the complete ploughed region, exudate redistribution is an internal transfer and its net detailed redistribution term should cancel.

## One-expression causal probe

A temporary diagnostic build changed exactly:

```text
Bafop(24,Ly)=Bafop(25,Ly)+Dum
```

to:

```text
Bafop(24,Ly)=Bafop(24,Ly)+Dum
```

The LWKM case completed successfully.

After normalizing only the already admitted volatile timestamp/CPU metadata, 58 common top-level generated files were compared.

Exactly three changed:

- `transfopGP.Out`;
- `transfopRP.Out`;
- `transfopTP.Out`.

All total organic-P balance outputs (`bapo*.Out`, `ani_p*.Bal`), ordinary state/process outputs and other balance families remained identical.

For 1997 in GP/RP/TP:

```text
legacy redis_EXP: -7.0644 kg/ha P
corrected redis_EXP: 0.0 kg/ha P
```

`redis_OP`, `redis_DOP` and `redis_HUP` remain unchanged.

## Classification

`CONFIRMED_LEGACY_DETAILED_LEDGER_ACCUMULATOR_DEFECT`

Proposed corrected-legacy class:

`A_ACCOUNTING_ONLY_DETAILED_TRANSFER_REPORTING`

Properties:

```text
physics_changed = false
state_trajectory_changed = false
total_mass_balance_changed = false
detailed_transfer_reporting_corrected = true
reference_qualification_required = true
production_migration_admitted = false
```

## ANIMO5 requirement

Detailed diagnostic ledgers must be derived from the same typed transfer events used by the total conserved ledger. Parallel hand-maintained slot arrays must not allow one process family to accumulate from another process slot.

Qualification should assert both total conservation and process-ledger decomposition identities.
