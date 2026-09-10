program runtimeq03_accounting_semantics_probe
  implicit none
  integer, parameter :: nl=2
  real(8), parameter :: st=0.25d0, cfracom=0.58d0
  real(8) :: qprch4(nl), qemch4dif, qemch4ebl, qemch4flw, qemch4plt
  real(8) :: qprn2oden(nl), qprn2onit(nl), qrdn2o(nl), qemn2odif, qemn2oflw
  real(8) :: amch4_form(nl), amch4_form_total, amch4_emit_total
  real(8) :: amn2odeni(nl), amn2onitr(nl), amn2o_prod_total, amn2o_emit_total
  real(8) :: physical_before(4), physical_after(4)
  logical :: p1,p2,p3,p4,p5,p6,p7

  qprch4 = (/ 1.2d-4, 0.8d-4 /)
  qemch4dif = 0.20d-4
  qemch4ebl = 0.05d-4
  qemch4flw = 0.10d-4
  qemch4plt = 0.05d-4

  qprn2oden = (/ 2.0d-5, 1.0d-5 /)
  qprn2onit = (/ 0.4d-5, 0.6d-5 /)
  qrdn2o = (/ 0.3d-5, 0.2d-5 /)
  qemn2odif = 0.30d-5
  qemn2oflw = 0.10d-5

  physical_before = (/ 7.0d0, 11.0d0, 13.0d0, 17.0d0 /)
  physical_after = physical_before

  amch4_form = qprch4 * st
  amch4_form_total = sum(amch4_form)
  amch4_emit_total = (qemch4dif + qemch4ebl + qemch4flw + qemch4plt) * st

  amn2odeni = qprn2oden * st
  amn2onitr = qprn2onit * st
  where (amn2onitr < 1.0d-8) amn2onitr = 0.0d0
  amn2o_prod_total = sum(qprn2oden * st) + sum(qprn2onit * st)
  amn2o_emit_total = (qemn2odif + qemn2oflw) * st

  p1 = all(amch4_form == qprch4*st)
  p2 = abs(amch4_form_total-amch4_emit_total) > 1.0d-12
  p3 = all(amn2odeni == qprn2oden*st)
  p4 = abs(amn2o_prod_total-amn2o_emit_total) > 1.0d-12
  p5 = abs(sum(amn2onitr)-sum(qprn2onit*st)) < 1.0d-18
  p6 = all(physical_before == physical_after)
  p7 = p1 .and. p2 .and. p3 .and. p4 .and. p5 .and. p6

  write(*,'(A,1X,L1)') 'CH4_LAYER_FORMATION_OWNER',p1
  write(*,'(A,1X,L1)') 'CH4_INDEX0_FORMATION_VS_EMISSION_SPLIT',p2
  write(*,'(A,1X,L1)') 'N2O_DENI_LAYER_FORMATION_OWNER',p3
  write(*,'(A,1X,L1)') 'N2O_PRODUCTION_VS_EMISSION_SPLIT',p4
  write(*,'(A,1X,L1)') 'N2O_NITR_LAYER_CURRENT_SEMANTICS',p5
  write(*,'(A,1X,L1)') 'OBSERVER_PHYSICAL_NONINTERFERENCE',p6
  write(*,'(A,1X,L1)') 'PARENT_REQUIRES_SEMANTIC_ATOMIZATION',p7
  write(*,'(A,1X,ES24.16)') 'CH4_FORM_TOTAL',amch4_form_total
  write(*,'(A,1X,ES24.16)') 'CH4_EMIT_TOTAL',amch4_emit_total
  write(*,'(A,1X,ES24.16)') 'N2O_PROD_TOTAL',amn2o_prod_total
  write(*,'(A,1X,ES24.16)') 'N2O_EMIT_TOTAL',amn2o_emit_total
  write(*,'(A,1X,ES24.16)') 'N2O_REDUCTION_TOTAL',sum(qrdn2o*st)
  write(*,'(A,1X,ES24.16)') 'CH4_FORM_OM_EQUIV',amch4_form_total/cfracom
  write(*,'(A,1X,ES24.16)') 'CH4_EMIT_OM_EQUIV',amch4_emit_total/cfracom
end program runtimeq03_accounting_semantics_probe
