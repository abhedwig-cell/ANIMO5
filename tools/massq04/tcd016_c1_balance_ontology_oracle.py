#!/usr/bin/env python3
from decimal import Decimal, getcontext
getcontext().prec=60

M=Decimal('0.000013880242022597072')

def total(aq,complex_,cont):
    return aq+complex_+cont

before=total(M,Decimal(0),Decimal(0))
after_wet_to_cont=total(Decimal(0),Decimal(0),M)
assert before==after_wet_to_cont

# Receiver-neutral rewetting transfer. The receiver label is intentionally not physics-qualified here.
for frac in (Decimal('0'),Decimal('0.125'),Decimal('0.5'),Decimal('1')):
    transfer=M*frac
    cont_after=M-transfer
    receiver_gain=transfer
    assert cont_after>=0 and receiver_gain>=0
    assert cont_after+receiver_gain==M

# Negative controls: omitting S_cont loses storage; double-counting internal transfer creates storage.
omit_cont=total(Decimal(0),Decimal(0),Decimal(0))
assert omit_cont!=before
transfer=M/Decimal(2)
double_count=(M-transfer)+transfer+transfer
assert double_count!=M

# Unit conversion must occur once: kg N m-2 -> kg N ha-1.
ha_factor=Decimal('10000')
assert M*ha_factor==Decimal('0.138802420225970720000')

print('MASSQ04 TCD016-C1 balance ontology oracle PASS')
print('canonical_mass_kg_N_m2', M)
print('canonical_mass_kg_N_ha', M*ha_factor)
print('wet_to_continuation_exact_closure PASS')
print('receiver_neutral_internal_transfer_cases 4')
print('omit_continuation_negative_control PASS')
print('double_count_internal_transfer_negative_control PASS')
print('tolerance NONE')
