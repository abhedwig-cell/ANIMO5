program tcd037_a3_source_shaped_probe
  implicit none

  integer, parameter :: nl = 3
  real(8), parameter :: z = 10000.0d0
  real(8) :: qpr(nl), qpr_zero(nl), qpr_half(nl), qpr_perm(nl)
  real(8) :: physical_state(3), process_flux(2)
  real(8) :: a1_observer, a2_observer, a4_observer, unrelated_observer

  qpr = (/ 0.00006103515625d0, 0.0001220703125d0, 0.00018310546875d0 /)
  qpr_zero = 0.0d0
  qpr_half = 0.5d0 * qpr
  qpr_perm = (/ qpr(3), qpr(1), qpr(2) /)

  physical_state = (/ 11.0d0, 22.0d0, 33.0d0 /)
  process_flux = (/ 7.0d0, 13.0d0 /)
  a1_observer = 31.0d0
  a2_observer = 41.0d0
  a4_observer = 51.0d0
  unrelated_observer = 77.0d0

  call run_case('ACTIVE_NONZERO', .true., qpr, 0.25d0, physical_state, process_flux, &
       a1_observer, a2_observer, a4_observer, unrelated_observer)

  call run_case('ZERO_DENI', .true., qpr_zero, 0.25d0, physical_state, process_flux, &
       a1_observer, a2_observer, a4_observer, unrelated_observer)

  call run_case('PERMUTED', .true., qpr_perm, 0.25d0, physical_state, process_flux, &
       a1_observer, a2_observer, a4_observer, unrelated_observer)

  call run_case('RATE_TIME_EQUIVALENT', .true., qpr_half, 0.50d0, physical_state, process_flux, &
       a1_observer, a2_observer, a4_observer, unrelated_observer)

  call run_case('INACTIVE', .false., qpr, 0.25d0, physical_state, process_flux, &
       a1_observer, a2_observer, a4_observer, unrelated_observer)

contains

  subroutine run_case(case_name, ghg_active, qprn2oden, st, physical_state, process_flux, &
       a1_observer, a2_observer, a4_observer, unrelated_observer)
    character(len=*), intent(in) :: case_name
    logical, intent(in) :: ghg_active
    real(8), intent(in) :: qprn2oden(nl), st
    real(8), intent(inout) :: physical_state(3), process_flux(2)
    real(8), intent(inout) :: a1_observer, a2_observer, a4_observer, unrelated_observer

    real(8) :: bani_n2od(nl)
    integer :: ln

    bani_n2od = 100.0d0

    if (ghg_active) then
      do ln = 1, nl
        bani_n2od(ln) = bani_n2od(ln) + z * qprn2oden(ln) * st
      end do
    end if

    write(*,'(A,1X,16(ES24.16E3,1X))') trim(case_name), &
         qprn2oden(1), qprn2oden(2), qprn2oden(3), st, &
         bani_n2od(1), bani_n2od(2), bani_n2od(3), &
         physical_state(1), physical_state(2), physical_state(3), &
         process_flux(1), process_flux(2), &
         a1_observer, a2_observer, a4_observer, unrelated_observer
  end subroutine run_case

end program tcd037_a3_source_shaped_probe
