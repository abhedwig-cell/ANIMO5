# PREP07 pool-slot and generic transport binding gates

Status: `SOURCE_BOUND_NEGATIVE_GATES_NO_NEW_ACTIVE_DEFECT`.

## Same-array numeric cross-slot scan

`tools/audit_pool_slot_identity.py` scans the frozen source for assignments of the form:

```text
Array(slot_a,...) = ... Array(slot_b,...) ...
```

where both slots are integer literals and `slot_a != slot_b`.

Revision-53 result:

```text
same-array cross-slot findings: 19
intentional transfer partitions: 18
existing confirmed discrepancy:  1
unresolved candidates:            0
```

The eighteen intentional cases are the repeated stable-DOM partition pattern in `resp_miner.for`:

```text
Transf*(19) <- (1-AsfaSDO) * Transf*(17)
Transf*(20) <- AsfaSDO     * Transf*(17)
```

The sole ledger accumulator reading a different same-array slot is:

```fortran
Bafop(24,Ly)=Bafop(25,Ly) + Dum
```

which is already the causally confirmed TCD-027 finding from PREP06. No duplicate discrepancy is created.

Four fail-closed unit tests verify recognition of TCD-027, the intentional transfer partition, and rejection of a synthetic unknown balance-slot cross-reference.

## Named generic transport binding scan

Generic transport procedures use formal names such as `Co`, `Reko` and `Rsco`, so formal-name species checks alone cannot establish whether the caller passed the correct constituent family.

`tools/audit_named_transport_species.py` therefore derives the expected conserved constituent from literal substance names passed to:

- `Transport`;
- `Transsub`;
- `Transgen`.

The admitted labels in this scan include:

- `AMMONIUM`;
- `NITRATE`;
- `PHOSPHORUS`;
- soluble organic matter;
- soluble organic nitrogen;
- soluble organic phosphorus.

Calls whose first argument is itself a runtime `Substname` variable are not guessed and remain outside this direct check.

Revision-53 result:

```text
named transport calls audited:      12
strong species actuals checked:      35
strong species mismatches:            0
```

Three unit tests verify matching P transport, deliberate P/N mismatch detection and fail-safe non-classification of runtime substance labels.

## Relation to earlier findings

The scan does not erase or weaken:

- TCD-015 transport algebra defect;
- TCD-019 PO4 numerical-conservation policy defect;
- TCD-023 cross-species SDO-to-humus P partition defect;
- TCD-024 slow-Langmuir site-index defect;
- TCD-027 detailed organic-P accumulator defect.

Those defects live below or beside the specific binding surfaces tested here.

The `AdStdiorpopl` and `Adhuexpopl` ploughing asymmetries are also not new PREP07 findings. PREP02 already causally activated both and classified them as members of the TCD-017 accounting-only ledger family.

## Conclusion

Within the strong-name and numeric-slot surfaces covered here, PREP07 finds no new active discrepancy beyond already registered defects.

This is useful negative evidence, but not a proof that every long legacy argument list or every same-species pool binding is correct. Generic names, computed indices and undocumented process semantics still require source/theory qualification where they matter.

Historical reference qualification remains blocked. Production migration remains `NOT_ADMITTED`.
