program tcd037_a1_source_shaped_probe
  implicit none

  integer, parameter :: nl = 3
  real(8), parameter :: z = 10000.0d0
  real(8), parameter :: cfracom = 0.5d0
  real(8) :: f(3,nl), fp(3,nl)
  real(8) :: q(nl), qp(nl), qzero(nl), qhalf(nl)
  real(8) :: base_ch4(3,nl), base_co2(3,nl)
  real(8) :: physical_state(3), process_flux(2), unrelated_observer

  f(1,:) = (/ 8.0d0, 4.0d0, 4.0d0 /)
  f(2,:) = (/ 4.0d0, 8.0d0, 4.0d0 /)
  f(3,:) = (/ 4.0d0, 4.0d0, 8.0d0 /)

  ! Exact dyadic rates. With St=1/4, Cfracom=1/2 and Z=10000,
  ! all expected synthetic observer values remain exactly representable
  ! in binary64.
  q = (/ 0.00006103515625d0, 0.0001220703125d0, 0.00018310546875d0 /)
  qzero = 0.0d0
  qhalf = 0.5d0 * q

  base_ch4(1,:) = 10.0d0
  base_ch4(2,:) = 20.0d0
  base_ch4(3,:) = 30.0d0
  base_co2(1,:) = 40.0d0
  base_co2(2,:) = 50.0d0
  base_co2(3,:) = 60.0d0

  physical_state = (/ 11.0d0, 22.0d0, 33.0d0 /)
  process_flux = (/ 7.0d0, 13.0d0 /)
  unrelated_observer = 77.0d0

  call run_case('ACTIVE', .true., f, q, 0.25d0, cfracom, base_ch4, base_co2, &
       physical_state, process_flux, unrelated_observer)

  call run_case('ZERO_CH4', .true., f, qzero, 0.25d0, cfracom, base_ch4, base_co2, &
       physical_state, process_flux, unrelated_observer)

  fp(:,1) = f(:,3)
  fp(:,2) = f(:,1)
  fp(:,3) = f(:,2)
  qp(1) = q(3)
  qp(2) = q(1)
  qp(3) = q(2)
  call run_case('PERMUTED', .true., fp, qp, 0.25d0, cfracom, base_ch4, base_co2, &
       physical_state, process_flux, unrelated_observer)

  call run_case('RATE_TIME_EQUIVALENT', .true., f, qhalf, 0.50d0, cfracom, &
       base_ch4, base_co2, physical_state, process_flux, unrelated_observer)

  call run_case('INACTIVE', .false., f, q, 0.25d0, cfracom, base_ch4, base_co2, &
       physical_state, process_flux, unrelated_observer)

contains

  subroutine run_case(case_name, ghg_active, f, qprch4, st, cfracom, base_ch4, base_co2, &
       physical_state, process_flux, unrelated_observer)
    character(len=*), intent(in) :: case_name
    logical, intent(in) :: ghg_active
    real(8), intent(in) :: f(3,nl), qprch4(nl), st, cfracom
    real(8), intent(in) :: base_ch4(3,nl), base_co2(3,nl)
    real(8), intent(inout) :: physical_state(3), process_flux(2), unrelated_observer

    real(8) :: out_ch4(3,nl), out_co2(3,nl)
    real(8) :: btot, omch4, fhlp
    integer :: ln, j

    out_ch4 = base_ch4
    out_co2 = base_co2

    if (ghg_active) then
      do ln = 1, nl
        btot = f(1,ln) + f(2,ln) + f(3,ln)
        omch4 = qprch4(ln) * st / cfracom
        if (btot .gt. 1.0d-9) then
          fhlp = 1.0d0 - z * omch4 / btot
        else
          btot = 1.0d0
          fhlp = 0.0d0
        end if

        do j = 1, 3
          out_ch4(j,ln) = out_ch4(j,ln) + z * f(j,ln) / btot * omch4
          out_co2(j,ln) = out_co2(j,ln) + f(j,ln) * fhlp
        end do
      end do
    end if

    do ln = 1, nl
      write(*,'(A,1X,I0,1X,18(ES24.16E3,1X))') trim(case_name), ln, &
           f(1,ln), f(2,ln), f(3,ln), qprch4(ln), st, cfracom, &
           out_ch4(1,ln), out_ch4(2,ln), out_ch4(3,ln), &
           out_co2(1,ln), out_co2(2,ln), out_co2(3,ln), &
           physical_state(1), physical_state(2), physical_state(3), &
           process_flux(1), process_flux(2), unrelated_observer
    end do
  end subroutine run_case

end program tcd037_a1_source_shaped_probe
