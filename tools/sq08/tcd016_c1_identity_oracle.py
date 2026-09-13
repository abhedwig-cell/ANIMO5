#!/usr/bin/env python3
from decimal import Decimal

OWNER = "M_surface_NH4_non_aqueous_continuation"
UNIT = "kg N m-2"


def carry(value):
    m = Decimal(str(value))
    return (OWNER, UNIT, m, "UNRESOLVED", "UNRESOLVED", False)


def main():
    a = carry("0")
    b = carry("0.00125")
    assert a[0] == b[0] == OWNER
    assert a[1] == b[1] == UNIT
    assert a[2] == Decimal("0")
    assert b[2] == Decimal("0.00125")
    assert a[3:] == ("UNRESOLVED", "UNRESOLVED", False)
    assert b[3:] == ("UNRESOLVED", "UNRESOLVED", False)
    print("SQ08_IDENTITY_ORACLE_PASS")


if __name__ == "__main__":
    main()
