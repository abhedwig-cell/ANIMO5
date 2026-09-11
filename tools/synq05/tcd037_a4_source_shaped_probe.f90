program tcd037_a4_source_shaped_probe
  implicit none

  real(8), parameter :: z = 10000.0d0
  real(8) :: physical_state(2), process_flux(1)
  real(8) :: n2od_observer, n2on_observer, qrdn2o_sink
  real(8) :: a1_observer, a2_observer, a3_observer, unrelated_observer

  physical_state = (/ 11.0d0, 22.0d0 /)
  process_flux = (/ 7.0d0 /)
  n2od_observer = 51.0d0
  n2on_observer = 61.0d0
  qrdn2o_sink = 71.0d0
  a1_observer = 31.0d0
  a2_observer = 41.0d0
  a3_observer = 46.0d0
  unrelated_observer = 77.0d0

  call run_case('EMISSION_NONZERO_PRODUCTION_ZERO', .true., &
       0.00006103515625d0, 0.000030517578125d0, 0.0d0, 0.0d0, 0.25d0, &
       physical_state, process_flux, n2od_observer, n2on_observer, qrdn2o_sink, &
       a1_observer, a2_observer, a3_observer, unrelated_observer)

  call run_case('PRODUCTION_NONZERO_EMISSION_ZERO', .true., &
       0.0d0, 0.0d0, 0.000244140625d0, 0.0001220703125d0, 0.25d0, &
       physical_state, process_flux, n2od_observer, n2on_observer, qrdn2o_sink, &
       a1_observer, a2_observer, a3_observer, unrelated_observer)

  call run_case('COMPONENT_PERMUTED', .true., &
       0.000030517578125d0, 0.00006103515625d0, 0.0d0, 0.0d0, 0.25d0, &
       physical_state, process_flux, n2od_observer, n2on_observer, qrdn2o_sink, &
       a1_observer, a2_observer, a3_observer, unrelated_observer)

  call run_case('RATE_TIME_EQUIVALENT', .true., &
       0.000030517578125d0, 0.0000152587890625d0, 0.0d0, 0.0d0, 0.50d0, &
       physical_state, process_flux, n2od_observer, n2on_observer, qrdn2o_sink, &
       a1_observer, a2_observer, a3_observer, unrelated_observer)

  call run_case('SIGNED_UPTAKE', .true., &
       -0.00006103515625d0, 0.000030517578125d0, 0.0d0, 0.0d0, 0.25d0, &
       physical_state, process_flux, n2od_observer, n2on_observer, qrdn2o_sink, &
       a1_observer, a2_observer, a3_observer, unrelated_observer)

  call run_case('INACTIVE', .false., &
       0.00006103515625d0, 0.000030517578125d0, 0.000244140625d0, 0.0001220703125d0, 0.25d0, &
       physical_state, process_flux, n2od_observer, n2on_observer, qrdn2o_sink, &
       a1_observer, a2_observer, a3_observer, unrelated_observer)

contains

  subroutine run_case(case_name, seam_active, qem_dif, qem_flw, prod_deni, prod_nit, st, &
       physical_state, process_flux, n2od_observer, n2on_observer, qrdn2o_sink, &
       a1_observer, a2_observer, a3_observer, unrelated_observer)
    character(len=*), intent(in) :: case_name
    logical, intent(in) :: seam_active
    real(8), intent(in) :: qem_dif, qem_flw, prod_deni, prod_nit, st
    real(8), intent(inout) :: physical_state(2), process_flux(1)
    real(8), intent(inout) :: n2od_observer, n2on_observer, qrdn2o_sink
    real(8), intent(inout) :: a1_observer, a2_observer, a3_observer, unrelated_observer

    real(8) :: bani_n2oe_candidate, bani_n2oe_native_bad

    bani_n2oe_candidate = 100.0d0
    bani_n2oe_native_bad = 100.0d0

    if (seam_active) then
      bani_n2oe_candidate = bani_n2oe_candidate + z * (qem_dif + qem_flw) * st
      bani_n2oe_native_bad = bani_n2oe_native_bad + z * (prod_deni + prod_nit) * st
    end if

    write(*,'(A,1X,17(ES24.16E3,1X))') trim(case_name), &
         qem_dif, qem_flw, prod_deni, prod_nit, st, &
         bani_n2oe_candidate, bani_n2oe_native_bad, &
         n2od_observer, n2on_observer, qrdn2o_sink, &
         physical_state(1), physical_state(2), process_flux(1), &
         a1_observer, a2_observer, a3_observer, unrelated_observer
  end subroutine run_case

end program tcd037_a4_source_shaped_probe
