#!/usr/bin/env python3
from decimal import Decimal, getcontext

getcontext().prec = 50
M0 = Decimal("1.3880242022597072e-5")
ZERO = Decimal(0)
ONE = Decimal(1)


def bounded_transfer(m_before: Decimal, fraction: Decimal):
    if fraction < ZERO or fraction > ONE:
        raise ValueError("transfer fraction outside [0,1]")
    transfer = m_before * fraction
    cont_after = m_before - transfer
    receiver_gain = transfer
    assert cont_after >= ZERO
    assert receiver_gain >= ZERO
    assert cont_after + receiver_gain == m_before
    return cont_after, receiver_gain


def split_receivers(transfer: Decimal, weights):
    weights = [Decimal(str(w)) for w in weights]
    if any(w < ZERO for w in weights):
        raise ValueError("negative receiver weight")
    total = sum(weights, ZERO)
    if total != ONE:
        raise ValueError("receiver weights must sum exactly to 1")
    gains = [transfer * w for w in weights]
    assert sum(gains, ZERO) == transfer
    return gains


def main():
    state = M0
    for _ in range(365):
        state_after = state
        assert state_after == state
        state = state_after
    assert state == M0

    fractions = [Decimal("0"), Decimal("0.01"), Decimal("0.125"), Decimal("0.5"), Decimal("1")]
    for f in fractions:
        cont_after, receiver_gain = bounded_transfer(M0, f)
        assert cont_after + receiver_gain == M0

    transfer = M0 * Decimal("0.6")
    gains = split_receivers(transfer, ["0.25", "0.75"])
    assert gains[0] + gains[1] == transfer
    assert (M0 - transfer) + sum(gains, ZERO) == M0

    remaining = M0
    received_total = ZERO
    for f in [Decimal("0.2"), Decimal("0.5"), Decimal("0.25")]:
        remaining, gain = bounded_transfer(remaining, f)
        received_total += gain
        assert remaining + received_total == M0

    for bad in [Decimal("-0.0001"), Decimal("1.0001")]:
        try:
            bounded_transfer(M0, bad)
        except ValueError:
            pass
        else:
            raise AssertionError("out-of-range transfer fraction accepted")

    for bad_weights in [["0.2", "0.7"], ["1.1", "-0.1"]]:
        try:
            split_receivers(M0, bad_weights)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid receiver partition accepted")

    invented_sink = Decimal("1e-9")
    assert M0 - invented_sink != M0

    print("TCD016-C1 SQ03 process-envelope oracle PASS")
    print("canonical_mass", M0)
    print("dry_hold_365_steps_exact PASS")
    print("bounded_transfer_partitions_exact PASS")
    print("receiver_neutral_partition_exact PASS")
    print("sequential_partial_transfer_exact PASS")
    print("out_of_range_negative_controls PASS")
    print("receiver_partition_negative_controls PASS")
    print("implicit_sink_negative_control PASS")
    print("model_tolerance NONE")
    print("specific_process_law_qualified false")
    print("specific_receiver_qualified false")
    print("historical_behavior UNKNOWN_WITHOUT_B2")


if __name__ == "__main__":
    main()
