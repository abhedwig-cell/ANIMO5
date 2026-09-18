program test_ubforce01_upper_solute_load_contract
  use iso_fortran_env, only: int64, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_value, ieee_quiet_nan
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate
  use mod_animo_tcd042_upper_solute_load_contract, only: &
    tcd042_upper_loads_t, make_tcd042_upper_loads, validate_tcd042_upper_loads, &
    select_tcd042_load_channel
  implicit none

  call test_core_only_contract()
  call test_phosphorus_contract()
  call test_fail_closed_contract()
  print *, 'PASS_UBFORCE01_TCD042_UPPER_SOLUTE_LOAD_CONTRACT'

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
    call assert_true(ok, 'make time')
  end subroutine make_day

  subroutine test_core_only_contract()
    type(TimeCoordinate) :: t0,t1
    type(tcd042_upper_loads_t) :: loads
    logical :: ok
    character(len=64) :: reason
    real(real64) :: selected

    call make_day(0_int64,t0)
    call make_day(1_int64,t1)
    call make_tcd042_upper_loads('FORCING-1',t0,t1,1.0e-5_real64,2.0e-5_real64, &
      3.0e-5_real64,4.0e-5_real64,.false.,0.0_real64,0.0_real64,loads,ok,reason)
    call assert_true(ok,'core-only carrier')
    call validate_tcd042_upper_loads(loads,t0,t1,ok,reason)
    call assert_true(ok,'core-only interval binding')
    call select_tcd042_load_channel(loads,2,selected,ok,reason)
    call assert_true(ok,'select channel 2')
    call assert_true(transfer(selected,0_int64)==transfer(2.0e-5_real64,0_int64),'channel 2 exact')
    call select_tcd042_load_channel(loads,5,selected,ok,reason)
    call assert_true(.not.ok,'inactive P channel rejected')
  end subroutine test_core_only_contract

  subroutine test_phosphorus_contract()
    type(TimeCoordinate) :: t0,t1
    type(tcd042_upper_loads_t) :: loads
    logical :: ok
    character(len=64) :: reason
    real(real64) :: selected

    call make_day(10_int64,t0)
    call make_day(20_int64,t1)
    call make_tcd042_upper_loads('FORCING-P',t0,t1,1.0_real64,2.0_real64, &
      3.0_real64,4.0_real64,.true.,5.0_real64,6.0_real64,loads,ok,reason)
    call assert_true(ok,'P carrier')
    call select_tcd042_load_channel(loads,6,selected,ok,reason)
    call assert_true(ok,'select P channel')
    call assert_true(transfer(selected,0_int64)==transfer(6.0_real64,0_int64),'P channel exact')
  end subroutine test_phosphorus_contract

  subroutine test_fail_closed_contract()
    type(TimeCoordinate) :: t0,t1,t2,subday
    type(tcd042_upper_loads_t) :: loads
    logical :: ok
    character(len=64) :: reason
    real(real64) :: nan_value, selected

    call make_day(100_int64,t0)
    call make_day(101_int64,t1)
    call make_day(102_int64,t2)

    call make_tcd042_upper_loads('',t0,t1,1.0_real64,2.0_real64,3.0_real64,4.0_real64, &
      .false.,0.0_real64,0.0_real64,loads,ok,reason)
    call assert_true(.not.ok,'missing execution id rejected')

    call make_tcd042_upper_loads('X',t0,t1,1.0_real64,2.0_real64,3.0_real64,4.0_real64, &
      .false.,1.0_real64,0.0_real64,loads,ok,reason)
    call assert_true(.not.ok,'inactive P nonzero rejected')

    nan_value=ieee_value(0.0_real64,ieee_quiet_nan)
    call make_tcd042_upper_loads('X',t0,t1,nan_value,2.0_real64,3.0_real64,4.0_real64, &
      .false.,0.0_real64,0.0_real64,loads,ok,reason)
    call assert_true(.not.ok,'NaN rejected')

    call make_tcd042_upper_loads('X',t0,t1,1.0_real64,2.0_real64,3.0_real64,4.0_real64, &
      .false.,0.0_real64,0.0_real64,loads,ok,reason)
    call assert_true(ok,'valid mismatch fixture')
    call validate_tcd042_upper_loads(loads,t0,t2,ok,reason)
    call assert_true(.not.ok,'endpoint mismatch rejected')

    call select_tcd042_load_channel(loads,7,selected,ok,reason)
    call assert_true(.not.ok,'invalid channel rejected')

    call make_time_coordinate('ANIMO_TEST_CALENDAR',100_int64,1_int64,2_int64,subday,ok)
    call assert_true(ok,'subday fixture')
    call make_tcd042_upper_loads('X',subday,t1,1.0_real64,2.0_real64,3.0_real64,4.0_real64, &
      .false.,0.0_real64,0.0_real64,loads,ok,reason)
    call assert_true(.not.ok,'subday rejected')
  end subroutine test_fail_closed_contract

end program test_ubforce01_upper_solute_load_contract
