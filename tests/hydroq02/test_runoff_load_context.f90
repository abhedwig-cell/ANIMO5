program test_hydroq02_runoff_load_context
  use iso_fortran_env, only: int64, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_value, ieee_quiet_nan
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate
  use mod_animo_tcd042_runoff_load_context, only: &
    tcd042_runoff_load_context_t, make_tcd042_runoff_load_context, &
    validate_tcd042_runoff_load_context
  implicit none

  call test_valid_capture()
  call test_exact_identity_guards()
  call test_no_reconstruction_assumption()
  print *, 'PASS_HYDROQ02_TCD042_RUNOFF_LOAD_CONTEXT'

contains

  subroutine assert_true(v,msg)
    logical,intent(in)::v
    character(len=*),intent(in)::msg
    if(.not.v) then
      print *,'ASSERTION FAILED: ',trim(msg)
      error stop 1
    end if
  end subroutine assert_true

  subroutine make_day(day,t)
    integer(int64),intent(in)::day
    type(TimeCoordinate),intent(out)::t
    logical::ok
    call make_time_coordinate('ANIMO_TEST_CALENDAR',day,0_int64,1_int64,t,ok)
    call assert_true(ok,'make day')
  end subroutine make_day

  subroutine test_valid_capture()
    type(TimeCoordinate)::t0,t1
    type(tcd042_runoff_load_context_t)::c
    logical::ok
    character(len=80)::reason

    call make_day(0_int64,t0); call make_day(1_int64,t1)
    call make_tcd042_runoff_load_context('HYDRO-EXEC-1',t0,t1,0.001_real64,0.002_real64,c,ok,reason)
    call assert_true(ok,'construct valid context')
    call validate_tcd042_runoff_load_context(c,t0,t1,'HYDRO-EXEC-1',ok,reason)
    call assert_true(ok,'bind valid context')
    call assert_true(transfer(c%rupr,0_int64)==transfer(0.001_real64,0_int64),'Rupr preserved exactly')
    call assert_true(transfer(c%runinu,0_int64)==transfer(0.002_real64,0_int64),'Runinu preserved exactly')
  end subroutine test_valid_capture

  subroutine test_exact_identity_guards()
    type(TimeCoordinate)::t0,t1,t2,subday
    type(tcd042_runoff_load_context_t)::c
    logical::ok
    character(len=80)::reason
    real(real64)::nanv

    call make_day(10_int64,t0); call make_day(11_int64,t1); call make_day(12_int64,t2)
    call make_tcd042_runoff_load_context('HYDRO-X',t0,t1,0.0_real64,0.0_real64,c,ok,reason)
    call assert_true(ok,'identity fixture')
    call validate_tcd042_runoff_load_context(c,t0,t2,'HYDRO-X',ok,reason)
    call assert_true(.not.ok,'endpoint mismatch rejected')
    call validate_tcd042_runoff_load_context(c,t0,t1,'OTHER',ok,reason)
    call assert_true(.not.ok,'execution mismatch rejected')

    call make_time_coordinate('ANIMO_TEST_CALENDAR',10_int64,1_int64,2_int64,subday,ok)
    call assert_true(ok,'subday fixture')
    call make_tcd042_runoff_load_context('HYDRO-X',subday,t1,0.0_real64,0.0_real64,c,ok,reason)
    call assert_true(.not.ok,'subday rejected')

    nanv=ieee_value(0.0_real64,ieee_quiet_nan)
    call make_tcd042_runoff_load_context('HYDRO-X',t0,t1,nanv,0.0_real64,c,ok,reason)
    call assert_true(.not.ok,'NaN rejected')
  end subroutine test_exact_identity_guards

  subroutine test_no_reconstruction_assumption()
    type(TimeCoordinate)::t0,t1
    type(tcd042_runoff_load_context_t)::c
    logical::ok
    character(len=80)::reason

    call make_day(20_int64,t0); call make_day(21_int64,t1)

    ! Representation intentionally permits any finite captured pair.
    ! This proves HYDROQ02 is not silently deriving Runinu from current raw Ru.
    call make_tcd042_runoff_load_context('HYDRO-CAPTURE',t0,t1,0.0_real64,0.123_real64,c,ok,reason)
    call assert_true(ok,'captured Runinu retained without local reconstruction')
  end subroutine test_no_reconstruction_assumption

end program test_hydroq02_runoff_load_context
