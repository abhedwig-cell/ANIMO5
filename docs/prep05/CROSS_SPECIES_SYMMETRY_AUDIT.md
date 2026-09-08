# PREP05 - Cross-species N/P sibling symmetry audit

Status: `SOURCE_BOUND_AUDIT_REPRODUCES_TCD023_NO_NEW_HIGH_CONFIDENCE_FINDING`.

## Purpose

TCD-023 showed that a phosphorus transformation branch in `Resp_miner` used the corresponding nitrogen quantity in two assignments. A broad search for N and P names produces too many legitimate nutrient-coupling expressions to be useful. This audit therefore uses a deliberately narrow structural rule.

It asks whether:

1. nearby assignments exist for matching N and P left-hand-side sibling variables;
2. transforming the N right-hand side to known P sibling identifiers produces an expression structurally very close to the actual P right-hand side;
3. the actual P assignment nevertheless retains an N sibling identifier;
4. the pair is not reciprocal cross-coupling, where the N expression intentionally depends on P and the P expression intentionally depends on N.

Static candidates remain evidence only. They are not automatically classified as defects.

## Tool

`tools/audit_cross_species_symmetry.py`

The tool is bound to frozen source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

It reconstructs continued assignment statements, infers conservative N/P sibling-name pairs from identifiers present in the source, and compares nearby N/P assignments with a structural-similarity threshold of `0.90`.

## Frozen-source result

Fortran files scanned: `60`.

Inferred N/P sibling pairs: `99`.

High-confidence candidate statements: `2`.

Both are the already causally confirmed TCD-023 statements in `resp_miner.for`:

```fortran
Transfon(19,Ln) = (1.0-AsfaSDO) * Transfon(17,Ln)
Transfop(19,Ln) = (1.0-AsfaSDO) * Transfon(17,Ln)
```

and:

```fortran
Transfon(20,Ln) = AsfaSDO * Transfon(17,Ln)
Transfop(20,Ln) = AsfaSDO * Transfon(17,Ln)
```

Structural similarities with the expected P-sibling forms are approximately `0.966` and `0.957`.

The audit therefore maps both statements to one existing discrepancy:

`TCD-023`.

No additional independent high-confidence cross-species discrepancy is produced.

## Reviewed non-defect coupling

The scan also encounters the plant uptake cross-limitation logic in `Upintg_Plant`. There, an N shortage proportionally reduces potential P uptake and a P shortage proportionally reduces potential N uptake. The dependency is reciprocal by design in the source structure, so the audit keeps it as contextual cross-coupling rather than promoting it to a defect candidate.

Likewise, relationships such as:

```fortran
Pofrhu(Ln) = Pofrhuma * Nifrhu(Ln) / Nifrhuma
```

are not promoted. This expression explicitly derives the humus P fraction from the layer N fraction and the material N/P ratio and does not have the sibling-assignment asymmetry pattern being audited.

## Tests

`tests/test_cross_species_symmetry_audit.py` covers:

- a TCD-023-style stale N sibling in a P assignment, which must be flagged;
- the corrected P-sibling form, which must not be flagged;
- reciprocal N/P coupling, which must not be promoted;
- an isolated N/P ratio relationship, which must not be promoted.

Equivalent local checks passed before persistence, and the complete frozen source scan reproduced only the two TCD-023 statements.

## Interpretation

This is useful negative evidence. Within the narrow class of nearby high-symmetry N/P assignments that this tool can assess, revision 53 does not expose another independent high-confidence cross-species typo beyond TCD-023.

It does not prove absence of all possible C/N/P coupling defects. More complex errors can involve different variable names, nonlocal state transfer, parameter tables, or scientifically intentional stoichiometric relationships that require theory rather than lexical symmetry to evaluate.

No new TCD is opened from this audit.

Production migration remains `NOT_ADMITTED` and historical-reference qualification remains blocked.
