program test_hydroexec01_bounded_upper_hydrology
  use iso_fortran_env, only: int64, real64
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate
  use mod_animo_hydrology_adapter, only: hydro_detailed_external_t
  use mod_animo_resolved_upper_hydrology_contract, only: resolved_upper_hydrology_t
  use mod_animo_tcd042_runoff_load_context, only: tcd042_runoff_load_context_t
  use mod_animo_bounded_no_ponding_upper_hydrology, only: &
    hydroexec01_start_context_t, hydroexec01_diagnostics_t, &
    make_hydroexec01_start_context, resolve_rev53_no_ponding_upper_hydrology
  implicit none

  call test_near_zero_preserves_runinu_call_entry()
  call test_negative_runoff()
  call test_positive_runoff()
  call test_ponding_rejected()
  call test_step_mismatch_rejected()
  call test_partition_singularity_rejected()
  print *, 'PASS_HYDROEXEC01_BOUNDED_NO_PONDING_UPPER_HYDROLOGY'

contains

  subroutine assert_true(value,message)
    logical,intent(in)::value
    character(len=*),intent(in)::message
    if(.not.value)then
      print *,'ASSERTION FAILED: ',trim(message)
      error stop 1
    end if
  end subroutine assert_true

  subroutine make_day(day,value)
    integer(int64),intent(in)::day
    type(TimeCoordinate),intent(out)::value
    logical::ok
    call make_time_coordinate('ANIMO_TEST_CALENDAR',day,0_int64,1_int64,value,ok)
    call assert_true(ok,'make day')
  end subroutine make_day

  subroutine base_projection(value)
    type(hydro_detailed_external_t),intent(out)::value
    value=hydro_detailed_external_t()
    value%layer_count=1
    value%drainage_count=0
    allocate(value%mofrt(1),value%flev(1),value%flab(2),value%fldr(0,1))
    value%mofrt(1)=0.5_real64
    value%flev(1)=0.0_real64
    value%flab=0.0_real64
    value%st=1.0_real64
  end subroutine base_projection

  subroutine base_start(runinu_entry,value)
    real(real64),intent(in)::runinu_entry
    type(hydroexec01_start_context_t),intent(out)::value
    logical::ok
    character(len=96)::reason
    call make_hydroexec01_start_context(0.0_real64,0.0_real64,0.0_real64, &
      0.5_real64,1.0_real64,0.0_real64,0.0_real64,runinu_entry,value,ok,reason)
    call assert_true(ok,'base start context')
  end subroutine base_start

  subroutine run_case(p,start,resolved,runoff,diag,ok,reason)
    type(hydro_detailed_external_t),intent(in)::p
    type(hydroexec01_start_context_t),intent(in)::start
    type(resolved_upper_hydrology_t),intent(out)::resolved
    type(tcd042_runoff_load_context_t),intent(out)::runoff
    type(hydroexec01_diagnostics_t),intent(out)::diag
    logical,intent(out)::ok
    character(len=*),intent(out)::reason
    type(TimeCoordinate)::t0,t1
    call make_day(0_int64,t0); call make_day(1_int64,t1)
    call resolve_rev53_no_ponding_upper_hydrology('HYDROEXEC-TEST',t0,t1,p,start, &
      resolved,runoff,diag,ok,reason)
  end subroutine run_case

  subroutine test_near_zero_preserves_runinu_call_entry()
    type(hydro_detailed_external_t)::p
    type(hydroexec01_start_context_t)::start
    type(resolved_upper_hydrology_t)::resolved
    type(tcd042_runoff_load_context_t)::runoff
    type(hydroexec01_diagnostics_t)::diag
    logical::ok
    character(len=96)::reason
    real(real64),parameter::tiny=2.0_real64**(-30)

    call base_projection(p)
    call base_start(tiny,start)
    p%ru=0.0_real64

    call run_case(p,start,resolved,runoff,diag,ok,reason)
    call assert_true(ok,'near-zero run')
    call assert_true(transfer(runoff%runinu,0_int64)==int(z'3E10000000000000',int64), &
      'Runinu call-entry preserved')
    call assert_true(transfer(resolved%flib_top,0_int64)==int(z'3E10000000000000',int64), &
      'near-zero resolved Flib exact')
    call assert_true(transfer(diag%evso_resolved,0_int64)==int(z'3E10000000000000',int64), &
      'near-zero Evso correction exact')
  end subroutine test_near_zero_preserves_runinu_call_entry

  subroutine test_negative_runoff()
    type(hydro_detailed_external_t)::p
    type(hydroexec01_start_context_t)::start
    type(resolved_upper_hydrology_t)::resolved
    type(tcd042_runoff_load_context_t)::runoff
    type(hydroexec01_diagnostics_t)::diag
    logical::ok
    character(len=96)::reason
    real(real64),parameter::tiny=2.0_real64**(-30)

    call base_projection(p)
    call base_start(0.0_real64,start)
    p%ru=-tiny

    call run_case(p,start,resolved,runoff,diag,ok,reason)
    call assert_true(ok,'negative runoff run')
    call assert_true(transfer(runoff%runinu,0_int64)==int(z'3E10000000000000',int64), &
      'negative runoff becomes Runinu')
    call assert_true(transfer(runoff%rupr,0_int64)==0_int64,'negative runoff Rupr zero')
  end subroutine test_negative_runoff

  subroutine test_positive_runoff()
    type(hydro_detailed_external_t)::p
    type(hydroexec01_start_context_t)::start
    type(resolved_upper_hydrology_t)::resolved
    type(tcd042_runoff_load_context_t)::runoff
    type(hydroexec01_diagnostics_t)::diag
    logical::ok
    character(len=96)::reason
    real(real64),parameter::ru=2.0_real64**(-20)
    real(real64),parameter::tiny=2.0_real64**(-30)

    call base_projection(p)
    call base_start(0.0_real64,start)
    p%ru=ru
    p%prr=ru+tiny
    start%lefrrv=0.0_real64
    start%lefrso=0.0_real64

    call run_case(p,start,resolved,runoff,diag,ok,reason)
    call assert_true(ok,'positive runoff run')
    call assert_true(transfer(runoff%rupr,0_int64)==transfer(ru,0_int64),'positive Rupr exact')
    call assert_true(transfer(runoff%runinu,0_int64)==0_int64,'positive Runinu zero')
    call assert_true(transfer(resolved%flib_top,0_int64)==int(z'3E10000000000000',int64), &
      'positive runoff resolved Flib exact and TCD042-scale')
  end subroutine test_positive_runoff

  subroutine test_ponding_rejected()
    type(hydro_detailed_external_t)::p
    type(hydroexec01_start_context_t)::start
    type(resolved_upper_hydrology_t)::resolved
    type(tcd042_runoff_load_context_t)::runoff
    type(hydroexec01_diagnostics_t)::diag
    logical::ok
    character(len=96)::reason

    call base_projection(p); call base_start(0.0_real64,start)
    p%pnt=2.0e-4_real64
    call run_case(p,start,resolved,runoff,diag,ok,reason)
    call assert_true(.not.ok,'ponding rejected')
  end subroutine test_ponding_rejected

  subroutine test_step_mismatch_rejected()
    type(hydro_detailed_external_t)::p
    type(hydroexec01_start_context_t)::start
    type(resolved_upper_hydrology_t)::resolved
    type(tcd042_runoff_load_context_t)::runoff
    type(hydroexec01_diagnostics_t)::diag
    logical::ok
    character(len=96)::reason

    call base_projection(p); call base_start(0.0_real64,start)
    p%st=2.0_real64
    call run_case(p,start,resolved,runoff,diag,ok,reason)
    call assert_true(.not.ok,'producer/KT02 step mismatch rejected')
  end subroutine test_step_mismatch_rejected

  subroutine test_partition_singularity_rejected()
    type(hydro_detailed_external_t)::p
    type(hydroexec01_start_context_t)::start
    type(resolved_upper_hydrology_t)::resolved
    type(tcd042_runoff_load_context_t)::runoff
    type(hydroexec01_diagnostics_t)::diag
    logical::ok
    character(len=96)::reason

    call base_projection(p); call base_start(0.0_real64,start)
    p%ru=2.0_real64**(-20)
    p%prr=1.0_real64
    start%lefrrv=1.0_real64
    start%lefrso=0.0_real64
    call run_case(p,start,resolved,runoff,diag,ok,reason)
    call assert_true(.not.ok,'partition singularity rejected')
  end subroutine test_partition_singularity_rejected

end program test_hydroexec01_bounded_upper_hydrology
