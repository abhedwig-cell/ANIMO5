# ANIMO-PREP07 — Direct C/N/P species-identity audit

Status: `SOURCE_BOUND_STRONG_IDENTITY_SCAN_IMPLEMENTED_TESTED_NO_NEW_ACTIVE_DIRECT_DEFECT`.

The frozen revision-53 source and supplied testcases remain unchanged.

## Purpose

The first PREP07 pass asks a narrow question: where does an assignment or local subroutine call bind a strongly species-identified C, N or P variable to a variable from another conserved species family?

This is deliberately narrower than a general scientific audit. Mixed-species formulas can be correct when an explicit ratio or stoichiometric conversion is intended. The tool therefore separates:

- already confirmed discrepancies;
- explicitly interpretable stoichiometric/ratio conversions;
- dormant or latent bindings whose state path is not operational in revision 53;
- unresolved candidates, which fail the audit closed.

## Reproducible tool

`tools/audit_species_identity.py`

The tool refuses a source ZIP whose SHA-256 differs from:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`.

It joins source continuations, scans assignment statements, classifies only strong species-name patterns and separately parses local `SUBROUTINE`/`CALL` interfaces.

Synthetic unit tests in `tests/test_species_identity_audit.py` verify:

1. TCD-023 is detected as an existing P-from-N discrepancy;
2. an explicit P:N content conversion is not treated as a defect;
3. the stable layer-0 DON binding is kept latent/dormant;
4. an unknown direct P-from-N assignment fails closed;
5. a synthetic local call with an N formal and P actual is detected;
6. a matching N-to-N call is not flagged.

All six tests pass in the PREP07 diagnostic workspace.

## Revision-53 scan result

The exact source scan reports:

```text
Fortran source members:                 60
assignment statements scanned:       9117
strong cross-species assignments:      13
unresolved direct candidates:            0
local subroutine definitions:           114
CALL statements:                       1354
aligned local calls:                   1347
strong formal/actual species pairs:     450
strong formal/actual mismatches:          0
```

### Existing confirmed defect rediscovered

Two assignments in `resp_miner.for` are exactly the already confirmed TCD-023 pattern:

```fortran
Transfop(19,Ln) = (1.0-AsfaSDO) * Transfon(17,Ln)
Transfop(20,Ln) = AsfaSDO * Transfon(17,Ln)
```

PREP04 already established the causal effect and correction. PREP07 therefore does not create a duplicate discrepancy.

### Explicit ratio/stoichiometric conversions

Seven strong mixed-species assignments are source-contextual conversions rather than direct wrong-species reuse. They include:

- shoot/root P content estimated from P:N content ratios and organic-N mass in `Grassprd.for` and `Uptpar_Grass.for`;
- humus P fraction scaled by a humus N ratio in `Inicalc.for`;
- DON:DOC and DOP:DOC ratios used when partitioning the CH4-related DOM sink in `Rates.for`.

These are not silently declared scientifically qualified. They are classified only as structurally intentional cross-species conversions because the source expression itself contains the conversion ratio needed to map the target constituent.

### Dormant stable-surface bindings

Four expressions in `Outsel.for` and `Outselorg.for` use `AvcoStdiorma(0)` in layer-0 `Rudon` or `Rudop` output formulas. The N/P-specific analogues would be `AvcoStdiorni(0)` and `AvcoStdiorpo(0)`.

PREP06 established, however, that stable DOM/DON/DOP layer 0 is parser/restart representable but dynamically dormant in revision 53. The process solve skips layer 0, no dynamic nonzero producer was found and all supplied cases initialize the layer-0 stable states to zero.

PREP07 therefore records these expressions as:

`LATENT_DORMANT_STABLE_SURFACE_DON_BINDING`

and

`LATENT_DORMANT_STABLE_SURFACE_DOP_BINDING`.

They are not promoted to active testbank discrepancies.

## Local procedure interface result

The tool reconstructed 114 local subroutine definitions and 1,354 calls. Of 1,347 calls with an argument count matching a local definition, 450 formal/actual positions have a strong C/N/P identity on both sides.

Observed strong species mismatches:

`0`.

This does not prove the long argument lists are semantically correct. It does establish that the simplest class of N-array-passed-to-P-formal or P-array-passed-to-N-formal error is not present among the strongly named local interfaces recognized by this audit.

## Current conclusion

Decision:

`NO_NEW_ACTIVE_DIRECT_CROSS_SPECIES_DEFECT_FROM_STRONG_IDENTITY_SCAN`

This is a scoped negative result, not whole-source scientific qualification. PREP07 must still audit subtler wrong-pool and analogue-symmetry errors where both variables belong to the same elemental species or where a generic variable name hides the constituent identity.

The historical reference blocker remains unchanged. Production migration remains `NOT_ADMITTED`.
