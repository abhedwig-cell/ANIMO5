program test_stateq11_composite_accepted_continuation
  use iso_fortran_env, only: int64, real32, real64
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate
  use mod_transient_contracts, only: transient_payload_t
  use mod_transient_transactions, only: accepted_store_t, initialize_accepted_store, &
    reconstruct_accepted_store_trusted
  use mod_animo_tcd042_upper_boundary_client, only: tcd042_top_state_t
  use mod_animo_static_boundary_year_binding, only: &
    boundary_year_cursor_t, initialize_boundary_year_cursor, BOUNDQ02_CURSOR_SCHEMA
  use mod_animo_first_detailed_hydrology_origin, only: &
    first_detailed_hydrology_origin_t, make_first_detailed_hydrology_origin
  use mod_animo_composite_accepted_continuation, only: &
    composite_accepted_continuation_t, initialize_composite_from_first_origin, &
    prepare_next_composite_continuation, validate_composite_continuation, &
    validate_composite_against_accepted_store
  implicit none

  call test_first_origin_composite_matches_store()
  call test_next_candidate_advances_all_sidecar_state()
  call test_stale_generation_rejected()
  call test_time_mismatch_rejected()
  call test_invalid_next_cursor_rejected()
  print *, 'PASS_STATEQ11_COMPOSITE_ACCEPTED_CONTINUATION'

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
    call make_time_coordinate('ANIMO_PG_86400_NOLEAPSECONDS_V1',day,0_int64,1_int64,value,ok)
    call assert_true(ok,'make day')
  end subroutine make_day

  subroutine make_first(value)
    type(first_detailed_hydrology_origin_t),intent(out)::value
    real(real32)::m(2)
    logical::ok
    character(len=128)::reason
    m=[0.25_real32,0.30_real32]
    call make_first_detailed_hydrology_origin(m,0.01_real32,0.02_real32,0.03_real32, &
      value,ok,reason)
    call assert_true(ok,'make first origin')
  end subroutine make_first

  subroutine make_store(lineage,time,generation,store)
    character(len=*),intent(in)::lineage
    type(TimeCoordinate),intent(in)::time
    integer(int64),intent(in)::generation
    type(accepted_store_t),intent(out)::store
    type(tcd042_top_state_t)::payload
    logical::ok

    payload%concentration=1.0_real64
    if(generation==0_int64)then
      call initialize_accepted_store(lineage,time,payload,store,ok)
    else
      call reconstruct_accepted_store_trusted(lineage,generation,time,payload,store,ok)
    end if
    call assert_true(ok,'make accepted store')
  end subroutine make_store

  subroutine test_first_origin_composite_matches_store()
    type(TimeCoordinate)::t0
    type(first_detailed_hydrology_origin_t)::first
    type(boundary_year_cursor_t)::cursor
    type(composite_accepted_continuation_t)::state
    type(accepted_store_t)::store
    logical::ok
    character(len=128)::reason
    real(real64),parameter::runinu=2.0_real64**(-30)

    call make_day(730119_int64,t0)
    call make_first(first)
    call initialize_boundary_year_cursor(cursor)
    call initialize_composite_from_first_origin('STATEQ11-LINEAGE',t0,first,runinu,cursor, &
      state,ok,reason)
    call assert_true(ok,'initialize first composite')
    call make_store('STATEQ11-LINEAGE',t0,0_int64,store)
    call validate_composite_against_accepted_store(state,store,ok,reason)
    call assert_true(ok,'first composite matches accepted store')
    call assert_true(transfer(state%runinu_call_entry,0_int64)==int(z'3E10000000000000',int64), &
      'explicit first Runinu preserved without invention')
    call assert_true(.not.state%boundary_cursor%initialized,'first cursor remains uninitialized')
  end subroutine test_first_origin_composite_matches_store

  subroutine test_next_candidate_advances_all_sidecar_state()
    type(TimeCoordinate)::t0,t1
    type(first_detailed_hydrology_origin_t)::first
    type(boundary_year_cursor_t)::cursor,next_cursor
    type(composite_accepted_continuation_t)::state,next
    type(accepted_store_t)::next_store
    real(real64)::mofrt(2)
    logical::ok
    character(len=128)::reason
    real(real64),parameter::runinu_next=2.0_real64**(-29)

    call make_day(730119_int64,t0); call make_day(730120_int64,t1)
    call make_first(first)
    call initialize_boundary_year_cursor(cursor)
    call initialize_composite_from_first_origin('STATEQ11-LINEAGE',t0,first,0.0_real64,cursor, &
      state,ok,reason)
    call assert_true(ok,'initialize origin composite')

    next_cursor=cursor
    next_cursor%schema_id=BOUNDQ02_CURSOR_SCHEMA
    next_cursor%initialized=.true.
    next_cursor%active_year=2000
    next_cursor%active_slot=1
    mofrt=[0.40_real64,0.50_real64]

    call prepare_next_composite_continuation(state,t1,0.04_real64,0.05_real64,0.06_real64, &
      mofrt,runinu_next,next_cursor,next,ok,reason)
    call assert_true(ok,'prepare next composite')
    call assert_true(next%generation==1_int64,'generation advanced')
    call assert_true(next%accepted_time%day_index==730120_int64,'time advanced')
    call assert_true(transfer(next%hydrology_origin%pn,0_int64)== &
      transfer(0.04_real64,0_int64),'Pn from accepted Pnt')
    call assert_true(transfer(next%hydrology_origin%sic,0_int64)== &
      transfer(0.05_real64,0_int64),'Sic from accepted Sict')
    call assert_true(transfer(next%hydrology_origin%snla,0_int64)== &
      transfer(0.06_real64,0_int64),'Snla from accepted Snt')
    call assert_true(all(transfer(next%hydrology_origin%mofro,[0_int64,0_int64])== &
      transfer(mofrt,[0_int64,0_int64])),'Mofro from accepted Mofrt')
    call assert_true(transfer(next%runinu_call_entry,0_int64)==int(z'3E20000000000000',int64), &
      'Runinu continuation advanced')
    call assert_true(next%boundary_cursor%active_year==2000 .and. &
      next%boundary_cursor%active_slot==1,'boundary cursor advanced')

    call make_store('STATEQ11-LINEAGE',t1,1_int64,next_store)
    call validate_composite_against_accepted_store(next,next_store,ok,reason)
    call assert_true(ok,'next composite matches next accepted store')
  end subroutine test_next_candidate_advances_all_sidecar_state

  subroutine test_stale_generation_rejected()
    type(TimeCoordinate)::t0
    type(first_detailed_hydrology_origin_t)::first
    type(boundary_year_cursor_t)::cursor
    type(composite_accepted_continuation_t)::state
    type(accepted_store_t)::store
    logical::ok
    character(len=128)::reason

    call make_day(1_int64,t0); call make_first(first); call initialize_boundary_year_cursor(cursor)
    call initialize_composite_from_first_origin('STALE',t0,first,0.0_real64,cursor,state,ok,reason)
    call assert_true(ok,'stale fixture')
    call make_store('STALE',t0,1_int64,store)
    call validate_composite_against_accepted_store(state,store,ok,reason)
    call assert_true(.not.ok,'stale generation rejected')
  end subroutine test_stale_generation_rejected

  subroutine test_time_mismatch_rejected()
    type(TimeCoordinate)::t0,t1
    type(first_detailed_hydrology_origin_t)::first
    type(boundary_year_cursor_t)::cursor
    type(composite_accepted_continuation_t)::state
    type(accepted_store_t)::store
    logical::ok
    character(len=128)::reason

    call make_day(1_int64,t0); call make_day(2_int64,t1)
    call make_first(first); call initialize_boundary_year_cursor(cursor)
    call initialize_composite_from_first_origin('TIME',t0,first,0.0_real64,cursor,state,ok,reason)
    call assert_true(ok,'time fixture')
    call make_store('TIME',t1,0_int64,store)
    call validate_composite_against_accepted_store(state,store,ok,reason)
    call assert_true(.not.ok,'time mismatch rejected')
  end subroutine test_time_mismatch_rejected

  subroutine test_invalid_next_cursor_rejected()
    type(TimeCoordinate)::t0,t1
    type(first_detailed_hydrology_origin_t)::first
    type(boundary_year_cursor_t)::cursor,bad
    type(composite_accepted_continuation_t)::state,next
    logical::ok
    character(len=128)::reason
    real(real64)::mofrt(2)

    call make_day(1_int64,t0); call make_day(2_int64,t1)
    call make_first(first); call initialize_boundary_year_cursor(cursor)
    call initialize_composite_from_first_origin('CURSOR',t0,first,0.0_real64,cursor,state,ok,reason)
    call assert_true(ok,'cursor fixture')
    bad=cursor
    mofrt=[0.2_real64,0.3_real64]
    call prepare_next_composite_continuation(state,t1,0.0_real64,0.0_real64,0.0_real64, &
      mofrt,0.0_real64,bad,next,ok,reason)
    call assert_true(.not.ok,'uninitialized next cursor rejected')
  end subroutine test_invalid_next_cursor_rejected

end program test_stateq11_composite_accepted_continuation
