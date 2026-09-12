#!/usr/bin/env python3
from decimal import Decimal, getcontext

getcontext().prec = 50

M = Decimal("1.3880242022597072e-5")  # kg N m-2
FU = Decimal("4.1184400265397315e-10")  # m d-1
ST = Decimal("1")  # d
ZERO = Decimal("0")

# Active control 1: a non-zero mass cannot be represented by C*V when V=0
# for any finite C. The topology therefore needs a mass coordinate that is
# independent of aqueous volume if the mass remains inside the control volume.
for finite_c in (Decimal("0"), Decimal("1"), Decimal("1e6"), Decimal("1e30")):
    assert finite_c * ZERO == ZERO
    assert finite_c * ZERO != M

# Active control 2: the proposed areic continuation owner carries the exact
# residual without a concentration or water-volume coordinate.
m_cont = M
assert m_cont == M

# Active control 3: explicit internal transfer is exactly conservative.
m_aq_before = M
transfer = M
m_aq_after = m_aq_before - transfer
m_cont_after = ZERO + transfer
assert m_aq_after == ZERO
assert m_cont_after == M
assert m_aq_before == m_aq_after + m_cont_after

# Active control 4: restart/checkpoint serialization of the areic mass as its
# exact decimal identity is lossless in this bounded oracle.
serialized = format(m_cont_after, "E")
restored = Decimal(serialized)
assert restored == m_cont_after

# Negative control: closing the event by forcing all residual mass through the
# observed tiny water outflow creates a pathological concentration. This is a
# diagnostic rejection, not a numerical tolerance.
forced_concentration = M / (FU * ST)
assert forced_concentration > Decimal("3e4")

print("SQ02 TCD016-C1 topology oracle PASS")
print("residual_mass_kgN_m2", M)
print("zero_water_finite_concentration_carries_residual", "false")
print("areic_continuation_owner_exact", "true")
print("internal_transfer_identity", "PASS")
print("restart_decimal_roundtrip", "PASS")
print("tiny_outflow_forced_concentration_kgN_m3", forced_concentration)
print("specific_phase_qualified", "false")
print("dry_chemistry_qualified", "false")
print("rewetting_law_qualified", "false")
print("model_tolerance", "NONE")
print("historical_behavior", "UNKNOWN_WITHOUT_B2")
print("B3_admitted", "false")
print("production_authorized", "false")
