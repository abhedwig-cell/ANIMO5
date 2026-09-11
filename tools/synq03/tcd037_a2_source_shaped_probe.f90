program tcd037_a2_source_shaped_probe
  implicit none

  integer, parameter :: nl = 3
  real(8), parameter :: z = 10000.0d0
  real(8), parameter :: cfracom = 0.5d0
  real(8), parameter :: d_om = 16.0d0
  real(8) :: qpr(nl), qpr_zero(nl), qpr_half(nl)
  real(8) :: qem(4), qem_zero(4), qem_half(4), qem_equal(4)
  real(8) :: physical_state(3), process_flux(2)
  real(8) :: a1_observer, a3_observer, a4_observer, unrelated_observer

  ! Exact dyadic synthetic rates. They deliberately make total CH4 formation
  ! different from total atmosphere emission in the active discriminator.
  qpr = (/ 0.00006103515625d0, 0.0001220703125d0, 0.00018310546875d0 /)
  qpr_zero = 0.0d0
  qpr_half = 0.5d0 * qpr

  qem = (/ 0.000030517578125d0, 0.00006103515625d0, &
            0.000030517578125d0, 0.0d0 /)
  qem_zero = 0.0d0
  qem_half = 0.5d0 * qem
  qem_equal = (/ 0.0001220703125d0, 0.0001220703125d0, &
                  0.0001220703125d0, 0.0d0 /)

  physical_state = (/ 11.0d0, 22.0d0, 33.0d0 /)
  process_flux = (/ 7.0d0, 13.0d0 /)
  a1_observer = 31.0d0
  a3_observer = 41.0d0
  a4_observer = 51.0d0
  unrelated_observer = 77.0d0

  call run_case('DIVERGENT_ACTIVE', .true., qpr, qem, 0.25d0, d_om, cfracom, &
       physical_state, process_flux, a1_observer, a3_observer, a4_observer, unrelated_observer)

  call run_case('FORMATION_ONLY', .true., qpr, qem_zero, 0.25d0, d_om, cfracom, &
       physical_state, process_flux, a1_observer, a3_observer, a4_observer, unrelated_observer)

  call run_case('EMISSION_ONLY', .true., qpr_zero, qem, 0.25d0, d_om, cfracom, &
       physical_state, process_flux, a1_observer, a3_observer, a4_observer, unrelated_observer)

  call run_case('EQUAL_TOTALS_CONTROL', .true., qpr, qem_equal, 0.25d0, d_om, cfracom, &
       physical_state, process_flux, a1_observer, a3_observer, a4_observer, unrelated_observer)

  call run_case('RATE_TIME_EQUIVALENT', .true., qpr_half, qem_half, 0.50d0, d_om, cfracom, &
       physical_state, process_flux, a1_observer, a3_observer, a4_observer, unrelated_observer)

  call run_case('INACTIVE', .false., qpr, qem, 0.25d0, d_om, cfracom, &
       physical_state, process_flux, a1_observer, a3_observer, a4_observer, unrelated_observer)

contains

  subroutine run_case(case_name, ghg_active, qprch4, qemch4, st, d_om, cfracom, &
       physical_state, process_flux, a1_observer, a3_observer, a4_observer, unrelated_observer)
    character(len=*), intent(in) :: case_name
    logical, intent(in) :: ghg_active
    real(8), intent(in) :: qprch4(nl), qemch4(4), st, d_om, cfracom
    real(8), intent(inout) :: physical_state(3), process_flux(2)
    real(8), intent(inout) :: a1_observer, a3_observer, a4_observer, unrelated_observer

    real(8) :: ch4_formation_total, ch4_emission_total
    real(8) :: out_ch4e, out_co2e

    out_ch4e = 100.0d0
    out_co2e = 200.0d0

    if (ghg_active) then
      ch4_formation_total = sum(qprch4) * st
      ch4_emission_total = sum(qemch4) * st

      ! A2 split: atmosphere emission owns CH4e, while the existing legacy
      ! total-dissimilation complement uses formation-side CH4 amount.
      out_ch4e = out_ch4e + z * ch4_emission_total / cfracom
      out_co2e = out_co2e + d_om - z * ch4_formation_total / cfracom
    end if

    write(*,'(A,1X,21(ES24.16E3,1X))') trim(case_name), &
         qprch4(1), qprch4(2), qprch4(3), &
         qemch4(1), qemch4(2), qemch4(3), qemch4(4), &
         st, d_om, cfracom, out_ch4e, out_co2e, &
         physical_state(1), physical_state(2), physical_state(3), &
         process_flux(1), process_flux(2), &
         a1_observer, a3_observer, a4_observer, unrelated_observer
  end subroutine run_case

end program tcd037_a2_source_shaped_probe
