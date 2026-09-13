#!/usr/bin/env python3
from decimal import Decimal, getcontext
getcontext().prec=60

M=Decimal('0.000013880242022597072')
ZERO=Decimal(0)

def storage(aq,complex_,cont):
    return aq+complex_+cont

# Active control: wet-to-continuation stays inside a selected control volume that owns both states.
before=storage(M,ZERO,ZERO)
after=storage(ZERO,ZERO,M)
assert before==after

# Active controls: receiver-neutral rewetting when receiver belongs to same selected control volume.
for frac in (Decimal('0'),Decimal('0.125'),Decimal('0.5'),Decimal('1')):
    t=M*frac
    cont=M-t
    receiver=t
    assert cont+receiver==M

# Active control: when the receiver is outside the selected control volume, the same transfer is a typed boundary output.
t=M*Decimal('0.375')
source_after=M-t
boundary_output=t
assert M==source_after+boundary_output
receiving_volume_gain=t
assert receiving_volume_gain==boundary_output

# Negative control: omitting continuation storage loses represented mass.
assert storage(ZERO,ZERO,ZERO)!=M

# Negative control: counting one same-CV internal transfer again as boundary output creates a false imbalance.
t=M/Decimal(2)
same_cv_storage_after=(M-t)+t
false_boundary_output=t
assert same_cv_storage_after+false_boundary_output!=M

# Negative control: a boundary transfer cannot disappear merely because the receiver is outside the observed volume.
assert source_after!=M
assert source_after+ZERO!=M

# Exact one-time unit conversion kg N m-2 -> kg N ha-1.
ha_factor=Decimal('10000')
assert M*ha_factor==Decimal('0.138802420225970720000')

print('MASSQ04 TCD016-C1 balance ontology oracle PASS')
print('canonical_mass_kg_N_m2',M)
print('canonical_mass_kg_N_ha',M*ha_factor)
print('same_control_volume_internal_transfer PASS')
print('receiver_neutral_same_volume_cases 4')
print('cross_control_volume_typed_boundary_transfer PASS')
print('omit_continuation_negative_control PASS')
print('internal_boundary_double_count_negative_control PASS')
print('missing_boundary_output_negative_control PASS')
print('tolerance NONE')
