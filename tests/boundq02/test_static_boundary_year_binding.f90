program test_boundq02_static_boundary_year_binding
  use iso_fortran_env, only: int64, real64
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate
  use mod_animo_static_boundary_chemistry_adapter, only: &
    static_boundary_chemistry_t, read_rev53_static_boundary_chemistry, BOUNDQ01_OK
  use mod_animo_static_boundary_year_binding, only: &
    boundary_year_cursor_t, static_boundary_interval_frame_t, &
    initialize_boundary_year_cursor, bind_static_boundary_interval, &
    validate_static_boundary_interval_frame
  implicit none

  call test_first_interval_midyear_selects_origin_year()
  call test_exact_january_first_refreshes_slot()
  call test_skipped_january_first_preserves_legacy_cursor()
  call test_phosphorus_binding_and_dry_dep_separation()
  call test_interval_and_calendar_fail_closed()
  print *, 'PASS_BOUNDQ02_STATIC_BOUNDARY_YEAR_BINDING'

contains

  subroutine assert_true(value,message)
    logical,intent(in)::value
    character(len=*),intent(in)::message
    if(.not.value)then
      print *,'ASSERTION FAILED: ',trim(message)
      error stop 1
    end if
  end subroutine assert_true

  subroutine make_day(index,value)
    integer(int64),intent(in)::index
    type(TimeCoordinate),intent(out)::value
    logical::ok
    call make_time_coordinate('ANIMO_PG_86400_NOLEAPSECONDS_V1',index,0_int64,1_int64,value,ok)
    call assert_true(ok,'make canonical day')
  end subroutine make_day

  subroutine read_no_p(boundary)
    type(static_boundary_chemistry_t),intent(out)::boundary
    integer::status
    call read_rev53_static_boundary_chemistry('tests/boundq01/fixtures/static_no_p.inp',3,0,boundary,status)
    call assert_true(status==BOUNDQ01_OK,'read no-P boundary fixture')
  end subroutine read_no_p

  subroutine read_p(boundary)
    type(static_boundary_chemistry_t),intent(out)::boundary
    integer::status
    call read_rev53_static_boundary_chemistry('tests/boundq01/fixtures/static_p.inp',2,1,boundary,status)
    call assert_true(status==BOUNDQ01_OK,'read P boundary fixture')
  end subroutine read_p

  subroutine test_first_interval_midyear_selects_origin_year()
    type(static_boundary_chemistry_t)::boundary
    type(boundary_year_cursor_t)::cursor,next
    type(static_boundary_interval_frame_t)::frame
    type(TimeCoordinate)::t0,t1
    logical::ok
    character(len=128)::reason

    call read_no_p(boundary)
    call initialize_boundary_year_cursor(cursor)
    call make_day(730301_int64,t0) ! 2000-07-01
    call make_day(730302_int64,t1)

    call bind_static_boundary_interval(boundary,'STATIC-BOUNDARY',2000,cursor,t0,t1,frame,next,ok,reason)
    call assert_true(ok,'first midyear interval binding')
    call assert_true(frame%selected_year==2000 .and. frame%selected_slot==1,'first interval selects slot one')
    call assert_true(transfer(frame%chemistry%precipitation%nh,0_int64)== &
      transfer(0.001_real64,0_int64),'slot-one precipitation NH')
    call assert_true(transfer(frame%dry_deposition_nh,0_int64)== &
      transfer(10.0_real64,0_int64),'slot-one dry deposition kept separate')
    call assert_true(next%initialized .and. next%active_slot==1,'cursor initialized')
  end subroutine test_first_interval_midyear_selects_origin_year

  subroutine test_exact_january_first_refreshes_slot()
    type(static_boundary_chemistry_t)::boundary
    type(boundary_year_cursor_t)::cursor,next
    type(static_boundary_interval_frame_t)::frame
    type(TimeCoordinate)::t0,t1
    logical::ok
    character(len=128)::reason

    call read_no_p(boundary)
    call initialize_boundary_year_cursor(cursor)
    cursor%initialized=.true.; cursor%active_year=2000; cursor%active_slot=1
    call make_day(730485_int64,t0) ! 2001-01-01
    call make_day(730486_int64,t1)

    call bind_static_boundary_interval(boundary,'STATIC-BOUNDARY',2000,cursor,t0,t1,frame,next,ok,reason)
    call assert_true(ok,'Jan-1 refresh')
    call assert_true(frame%selected_year==2001 .and. frame%selected_slot==2,'Jan-1 selects slot two')
    call assert_true(transfer(frame%chemistry%precipitation%nh,0_int64)== &
      transfer(0.002_real64,0_int64),'slot-two precipitation NH')
    call assert_true(transfer(frame%dry_deposition_ni,0_int64)== &
      transfer(21.0_real64,0_int64),'slot-two dry deposition NI')
  end subroutine test_exact_january_first_refreshes_slot

  subroutine test_skipped_january_first_preserves_legacy_cursor()
    type(static_boundary_chemistry_t)::boundary
    type(boundary_year_cursor_t)::cursor,next
    type(static_boundary_interval_frame_t)::frame
    type(TimeCoordinate)::t0,t1
    logical::ok
    character(len=128)::reason

    call read_no_p(boundary)
    call initialize_boundary_year_cursor(cursor)
    cursor%initialized=.true.; cursor%active_year=2000; cursor%active_slot=1
    call make_day(730486_int64,t0) ! 2001-01-02
    call make_day(730487_int64,t1)

    call bind_static_boundary_interval(boundary,'STATIC-BOUNDARY',2000,cursor,t0,t1,frame,next,ok,reason)
    call assert_true(ok,'skipped-Jan1 source-faithful binding')
    call assert_true(frame%selected_slot==1 .and. frame%selected_year==2000, &
      'non-Jan1 origin preserves prior source cursor exactly')
    call assert_true(transfer(frame%chemistry%precipitation%nh,0_int64)== &
      transfer(0.001_real64,0_int64),'prior-year chemistry retained')
  end subroutine test_skipped_january_first_preserves_legacy_cursor

  subroutine test_phosphorus_binding_and_dry_dep_separation()
    type(static_boundary_chemistry_t)::boundary
    type(boundary_year_cursor_t)::cursor,next
    type(static_boundary_interval_frame_t)::frame
    type(TimeCoordinate)::t0,t1
    logical::ok
    character(len=128)::reason

    call read_p(boundary)
    call initialize_boundary_year_cursor(cursor)
    call make_day(730485_int64,t0) ! 2001-01-01, simulation starts 2000 -> slot2
    call make_day(730486_int64,t1)

    call bind_static_boundary_interval(boundary,'BOUNDARY-P',2000,cursor,t0,t1,frame,next,ok,reason)
    call assert_true(ok,'P year binding')
    call assert_true(frame%chemistry%phosphorus_enabled,'P presence bound')
    call assert_true(transfer(frame%chemistry%precipitation%po,0_int64)== &
      transfer(0.006_real64,0_int64),'slot-two precipitation P')
    call assert_true(transfer(frame%chemistry%runon%dop,0_int64)== &
      transfer(0.60_real64,0_int64),'static runon DOP')
    call assert_true(transfer(frame%dry_deposition_nh,0_int64)== &
      transfer(2.0_real64,0_int64),'dry deposition carried separately')
  end subroutine test_phosphorus_binding_and_dry_dep_separation

  subroutine test_interval_and_calendar_fail_closed()
    type(static_boundary_chemistry_t)::boundary
    type(boundary_year_cursor_t)::cursor,next
    type(static_boundary_interval_frame_t)::frame
    type(TimeCoordinate)::t0,t1,wrong,subday
    logical::ok
    character(len=128)::reason

    call read_no_p(boundary)
    call initialize_boundary_year_cursor(cursor)
    call make_day(730119_int64,t0)
    call make_day(730120_int64,t1)

    call bind_static_boundary_interval(boundary,'STATIC-BOUNDARY',2000,cursor,t1,t0,frame,next,ok,reason)
    call assert_true(.not.ok,'backward interval rejected')

    call make_time_coordinate('OTHER_CALENDAR',730119_int64,0_int64,1_int64,wrong,ok)
    call assert_true(ok,'wrong-calendar fixture')
    call bind_static_boundary_interval(boundary,'STATIC-BOUNDARY',2000,cursor,wrong,t1,frame,next,ok,reason)
    call assert_true(.not.ok,'wrong calendar rejected')

    call make_time_coordinate('ANIMO_PG_86400_NOLEAPSECONDS_V1',730119_int64,1_int64,2_int64,subday,ok)
    call assert_true(ok,'subday fixture')
    call bind_static_boundary_interval(boundary,'STATIC-BOUNDARY',2000,cursor,subday,t1,frame,next,ok,reason)
    call assert_true(.not.ok,'subday year selection rejected')

    call bind_static_boundary_interval(boundary,'STATIC-BOUNDARY',1997,cursor,t0,t1,frame,next,ok,reason)
    call assert_true(.not.ok,'year slot beyond Nuyr rejected after first selection')

    call bind_static_boundary_interval(boundary,'STATIC-BOUNDARY',2000,cursor,t0,t1,frame,next,ok,reason)
    call assert_true(ok,'valid frame for mismatch test')
    call validate_static_boundary_interval_frame(frame,t0,wrong,ok,reason)
    call assert_true(.not.ok,'frame endpoint identity mismatch rejected')
  end subroutine test_interval_and_calendar_fail_closed

end program test_boundq02_static_boundary_year_binding
