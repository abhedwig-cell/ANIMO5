program test_hydroq01_resolved_upper_hydrology
  use iso_fortran_env, only: int64, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_value, ieee_quiet_nan
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate
  use mod_animo_resolved_upper_hydrology_contract, only: &
    resolved_upper_hydrology_t, make_resolved_upper_hydrology, &
    validate_tcd042_resolved_upper_hydrology
  implicit none

  call test_valid_contract()
  call test_fail_closed_fields()
  call test_exact_interval_binding()
  print *, 'PASS_HYDROQ01_RESOLVED_UPPER_HYDROLOGY_CONTRACT'

contains

  subroutine assert_true(value, message)
    logical, intent(in) :: value
    character(len=*), intent(in) :: message
    if (.not. value) then
      print *, 'ASSERTION FAILED: ', trim(message)
      error stop 1
    end if
  end subroutine assert_true

  subroutine make_day(day, value)
    integer(int64), intent(in) :: day
    type(TimeCoordinate), intent(out) :: value
    logical :: ok
    call make_time_coordinate('ANIMO_TEST_CALENDAR', day, 0_int64, 1_int64, value, ok)
    call assert_true(ok, 'make day')
  end subroutine make_day

  subroutine test_valid_contract()
    type(TimeCoordinate) :: t0, t1
    type(resolved_upper_hydrology_t) :: h
    logical :: ok
    character(len=64) :: reason

    call make_day(10_int64, t0)
    call make_day(20_int64, t1)
    call make_resolved_upper_hydrology('HYDRO-EXEC-001', t0, t1, 0, 2.5e-9_real64, &
      0.0_real64, h, ok, reason)
    call assert_true(ok, 'construct valid resolved hydrology')
    call validate_tcd042_resolved_upper_hydrology(h, t0, t1, ok, reason)
    call assert_true(ok, 'bind valid resolved hydrology')
  end subroutine test_valid_contract

  subroutine test_fail_closed_fields()
    type(TimeCoordinate) :: t0, t1
    type(resolved_upper_hydrology_t) :: h
    logical :: ok
    character(len=64) :: reason
    real(real64) :: nan_value

    call make_day(0_int64, t0)
    call make_day(1_int64, t1)

    call make_resolved_upper_hydrology('', t0, t1, 0, 0.0_real64, 0.0_real64, h, ok, reason)
    call assert_true(.not. ok, 'missing execution id rejected')

    call make_resolved_upper_hydrology('X', t0, t1, 1, 0.0_real64, 0.0_real64, h, ok, reason)
    call assert_true(.not. ok, 'ponding branch rejected')

    call make_resolved_upper_hydrology('X', t0, t1, 0, -1.0e-9_real64, 0.0_real64, h, ok, reason)
    call assert_true(.not. ok, 'negative Flib rejected')

    call make_resolved_upper_hydrology('X', t0, t1, 0, 0.0_real64, 1.0e-15_real64, h, ok, reason)
    call assert_true(.not. ok, 'nonzero Rurv rejected')

    nan_value = ieee_value(0.0_real64, ieee_quiet_nan)
    call make_resolved_upper_hydrology('X', t0, t1, 0, nan_value, 0.0_real64, h, ok, reason)
    call assert_true(.not. ok, 'NaN Flib rejected')
  end subroutine test_fail_closed_fields

  subroutine test_exact_interval_binding()
    type(TimeCoordinate) :: t0, t1, other, subday
    type(resolved_upper_hydrology_t) :: h
    logical :: ok
    character(len=64) :: reason

    call make_day(100_int64, t0)
    call make_day(110_int64, t1)
    call make_day(111_int64, other)

    call make_resolved_upper_hydrology('X', t0, t1, 0, 0.0_real64, 0.0_real64, h, ok, reason)
    call assert_true(ok, 'construct interval fixture')
    call validate_tcd042_resolved_upper_hydrology(h, t0, other, ok, reason)
    call assert_true(.not. ok, 'endpoint mismatch rejected')

    call make_time_coordinate('ANIMO_TEST_CALENDAR', 100_int64, 1_int64, 2_int64, subday, ok)
    call assert_true(ok, 'construct exact subday coordinate')
    call make_resolved_upper_hydrology('X', subday, t1, 0, 0.0_real64, 0.0_real64, h, ok, reason)
    call assert_true(.not. ok, 'subday carrier rejected in current bounded envelope')
  end subroutine test_exact_interval_binding

end program test_hydroq01_resolved_upper_hydrology
