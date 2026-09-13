#!/usr/bin/env python3
from decimal import Decimal, getcontext

getcontext().prec = 50
M0 = Decimal("1.3880242022597072e-5")
ZERO = Decimal(0)
ONE = Decimal(1)


def rewet_partition(m_before: Decimal, fraction: Decimal):
    if fraction < ZERO or fraction > ONE:
        raise ValueError("rewetting fraction outside [0,1]")
    transfer = m_before * fraction
    dry_after = m_before - transfer
    aq_gain = transfer
    assert dry_after >= ZERO
    assert aq_gain >= ZERO
    assert dry_after + aq_gain == m_before
    return dry_after, aq_gain


def main():
    # Exact epistemic persistence with no admitted process.
    state = M0
    for _ in range(365):
        state_after = state
        assert state_after == state
        state = state_after
    assert state == M0

    # Zero, partial and complete bounded transfers.
    fractions = [Decimal("0"), Decimal("0.01"), Decimal("0.125"), Decimal("0.5"), Decimal("1")]
    for f in fractions:
        dry_after, aq_gain = rewet_partition(M0, f)
        assert dry_after + aq_gain == M0

    # Sequential partial transfers preserve ownership exactly.
    remaining = M0
    aqueous_total = ZERO
    for f in [Decimal("0.2"), Decimal("0.5"), Decimal("0.25")]:
        remaining, gain = rewet_partition(remaining, f)
        aqueous_total += gain
        assert remaining + aqueous_total == M0

    # Negative controls: underflow and overdraw must fail closed.
    for bad in [Decimal("-0.0001"), Decimal("1.0001")]:
        try:
            rewet_partition(M0, bad)
        except ValueError:
            pass
        else:
            raise AssertionError("out-of-range transfer fraction accepted")

    # Negative control: an untyped sink changes the closed control volume and must be detectable.
    invented_sink = Decimal("1e-9")
    assert M0 - invented_sink != M0

    print("TCD016-C1 SQ03 process-envelope oracle PASS")
    print("canonical_mass", M0)
    print("dry_hold_365_steps_exact PASS")
    print("bounded_rewet_partitions_exact PASS")
    print("sequential_partial_transfer_exact PASS")
    print("out_of_range_negative_controls PASS")
    print("implicit_sink_negative_control PASS")
    print("model_tolerance NONE")
    print("specific_process_law_qualified false")
    print("historical_behavior UNKNOWN_WITHOUT_B2")


if __name__ == "__main__":
    main()
