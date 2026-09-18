program test_boundq02b_immutable_boundary_frame
  use iso_fortran_env, only: int64, real64
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate
  use mod_animo_static_boundary_chemistry_adapter, only: &
    static_boundary_chemistry_t, read_rev53_static_boundary_chemistry, BOUNDQ01_OK
  use mod_animo_static_boundary_year_binding, only: &
    boundary_year_cursor_t, initialize_boundary_year_cursor
  use mod_animo_tcd042_upper_solute_load_resolver, only: &
    tcd042_upper_chemistry_forcing_t
  use mod_animo_immutable_static_boundary_frame, only: &
    immutable_static_boundary_interval_frame_t, &
    make_immutable_static_boundary_interval_frame, &
    validate_immutable_static_boundary_interval_frame, &
    inspect_immutable_static_boundary_interval_frame
  implicit none

  character(len=*), parameter :: FIXTURE_SHA = &
    '629a94972504c2865f8f0cbae9960e1354f6acd09e39ef663cc8f74375a7a169'

  call test_content_bound_frame()
  call test_accessor_returns_copy_not_mutable_frame()
  call test_content_identity_changes_forcing_identity()
  call test_bad_content_identity_rejected()
  call test_exact_interval_identity_rejected_when_stale()
  print *, 'PASS_BOUNDQ02B_IMMUTABLE_BOUNDARY_FRAME'

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
    call assert_true(ok,'make TIME02 day')
  end subroutine make_day

  subroutine read_boundary(boundary)
    type(static_boundary_chemistry_t),intent(out)::boundary
    integer::status
    call read_rev53_static_boundary_chemistry( &
      'tests/boundq01/fixtures/static_no_p.inp',3,0,boundary,status)
    call assert_true(status==BOUNDQ01_OK,'read BOUNDQ01 fixture')
  end subroutine read_boundary

  subroutine inspect(frame,t0,t1,content_id,start_year,nuyr,selected_year,selected_slot, &
      chemistry,dry_nh,dry_ni,ok)
    type(immutable_static_boundary_interval_frame_t),intent(in)::frame
    type(TimeCoordinate),intent(in)::t0,t1
    character(len=64),intent(out)::content_id
    integer,intent(out)::start_year,nuyr,selected_year,selected_slot
    type(tcd042_upper_chemistry_forcing_t),intent(out)::chemistry
    real(real64),intent(out)::dry_nh,dry_ni
    logical,intent(out)::ok
    character(len=128)::reason

    call inspect_immutable_static_boundary_interval_frame(frame,t0,t1,content_id, &
      start_year,nuyr,selected_year,selected_slot,chemistry,dry_nh,dry_ni,ok,reason)
  end subroutine inspect

  subroutine make_frame(content_id,t0,t1,frame,cursor,next,ok)
    character(len=*),intent(in)::content_id
    type(TimeCoordinate),intent(in)::t0,t1
    type(immutable_static_boundary_interval_frame_t),intent(out)::frame
    type(boundary_year_cursor_t),intent(out)::cursor,next
    logical,intent(out)::ok
    type(static_boundary_chemistry_t)::boundary
    character(len=128)::reason

    call read_boundary(boundary)
    call initialize_boundary_year_cursor(cursor)
    call make_immutable_static_boundary_interval_frame(boundary,content_id,2000,cursor, &
      t0,t1,frame,next,ok,reason)
  end subroutine make_frame

  subroutine test_content_bound_frame()
    type(TimeCoordinate)::t0,t1
    type(immutable_static_boundary_interval_frame_t)::frame
    type(boundary_year_cursor_t)::cursor,next
    type(tcd042_upper_chemistry_forcing_t)::chemistry
    character(len=64)::content_id
    integer::start_year,nuyr,selected_year,selected_slot
    real(real64)::dry_nh,dry_ni
    logical::ok
    character(len=128)::reason

    call make_day(730119_int64,t0)
    call make_day(730120_int64,t1)
    call make_frame(FIXTURE_SHA,t0,t1,frame,cursor,next,ok)
    call assert_true(ok,'immutable frame construction')

    call validate_immutable_static_boundary_interval_frame(frame,t0,t1,ok,reason)
    call assert_true(ok,'immutable frame validates')
    call inspect(frame,t0,t1,content_id,start_year,nuyr,selected_year,selected_slot, &
      chemistry,dry_nh,dry_ni,ok)
    call assert_true(ok,'immutable frame inspection')
    call assert_true(content_id==FIXTURE_SHA,'content sha preserved')
    call assert_true(start_year==2000 .and. nuyr==3,'source envelope preserved')
    call assert_true(selected_year==2000 .and. selected_slot==1,'selected year/slot preserved')
    call assert_true(trim(chemistry%forcing_id)== &
      'SHA256='//FIXTURE_SHA//':SLOT=1','forcing identity is content-bound')
    call assert_true(transfer(chemistry%precipitation%nh,0_int64)== &
      transfer(0.001_real64,0_int64),'selected chemistry exact')
    call assert_true(transfer(dry_nh,0_int64)==transfer(10.0_real64,0_int64), &
      'dry deposition copied separately')
    call assert_true(next%initialized .and. next%active_slot==1,'candidate cursor returned')
  end subroutine test_content_bound_frame

  subroutine test_accessor_returns_copy_not_mutable_frame()
    type(TimeCoordinate)::t0,t1
    type(immutable_static_boundary_interval_frame_t)::frame
    type(boundary_year_cursor_t)::cursor,next
    type(tcd042_upper_chemistry_forcing_t)::chemistry1,chemistry2
    character(len=64)::content_id
    integer::start_year,nuyr,selected_year,selected_slot
    real(real64)::dry_nh,dry_ni
    logical::ok

    call make_day(730119_int64,t0)
    call make_day(730120_int64,t1)
    call make_frame(FIXTURE_SHA,t0,t1,frame,cursor,next,ok)
    call assert_true(ok,'copy test frame')

    call inspect(frame,t0,t1,content_id,start_year,nuyr,selected_year,selected_slot, &
      chemistry1,dry_nh,dry_ni,ok)
    call assert_true(ok,'first inspect')
    chemistry1%precipitation%nh=999.0_real64
    chemistry1%forcing_id='MUTATED-COPY'

    call inspect(frame,t0,t1,content_id,start_year,nuyr,selected_year,selected_slot, &
      chemistry2,dry_nh,dry_ni,ok)
    call assert_true(ok,'second inspect')
    call assert_true(transfer(chemistry2%precipitation%nh,0_int64)== &
      transfer(0.001_real64,0_int64),'returned chemistry mutation cannot alter frame')
    call assert_true(trim(chemistry2%forcing_id)== &
      'SHA256='//FIXTURE_SHA//':SLOT=1','frame forcing identity remains immutable')
  end subroutine test_accessor_returns_copy_not_mutable_frame

  subroutine test_content_identity_changes_forcing_identity()
    type(TimeCoordinate)::t0,t1
    type(immutable_static_boundary_interval_frame_t)::frame_a,frame_b
    type(boundary_year_cursor_t)::cursor_a,next_a,cursor_b,next_b
    type(tcd042_upper_chemistry_forcing_t)::chem_a,chem_b
    character(len=64)::content_a,content_b
    integer::sy,ny,y,s
    real(real64)::dn,di
    logical::ok
    character(len=*),parameter::OTHER_SHA= &
      '729a94972504c2865f8f0cbae9960e1354f6acd09e39ef663cc8f74375a7a169'

    call make_day(730119_int64,t0)
    call make_day(730120_int64,t1)
    call make_frame(FIXTURE_SHA,t0,t1,frame_a,cursor_a,next_a,ok)
    call assert_true(ok,'frame A')
    call make_frame(OTHER_SHA,t0,t1,frame_b,cursor_b,next_b,ok)
    call assert_true(ok,'frame B')

    call inspect(frame_a,t0,t1,content_a,sy,ny,y,s,chem_a,dn,di,ok)
    call assert_true(ok,'inspect A')
    call inspect(frame_b,t0,t1,content_b,sy,ny,y,s,chem_b,dn,di,ok)
    call assert_true(ok,'inspect B')
    call assert_true(trim(chem_a%forcing_id)/=trim(chem_b%forcing_id), &
      'changed declared content identity changes forcing identity')
  end subroutine test_content_identity_changes_forcing_identity

  subroutine test_bad_content_identity_rejected()
    type(TimeCoordinate)::t0,t1
    type(immutable_static_boundary_interval_frame_t)::frame
    type(boundary_year_cursor_t)::cursor,next
    logical::ok

    call make_day(730119_int64,t0)
    call make_day(730120_int64,t1)
    call make_frame('NOT-A-SHA256',t0,t1,frame,cursor,next,ok)
    call assert_true(.not.ok,'noncanonical content identity rejected')
    call make_frame('629A94972504C2865F8F0CBAE9960E1354F6ACD09E39EF663CC8F74375A7A169', &
      t0,t1,frame,cursor,next,ok)
    call assert_true(.not.ok,'uppercase noncanonical content identity rejected')
  end subroutine test_bad_content_identity_rejected

  subroutine test_exact_interval_identity_rejected_when_stale()
    type(TimeCoordinate)::t0,t1,t2
    type(immutable_static_boundary_interval_frame_t)::frame
    type(boundary_year_cursor_t)::cursor,next
    logical::ok
    character(len=128)::reason

    call make_day(730119_int64,t0)
    call make_day(730120_int64,t1)
    call make_day(730121_int64,t2)
    call make_frame(FIXTURE_SHA,t0,t1,frame,cursor,next,ok)
    call assert_true(ok,'stale fixture frame')

    call validate_immutable_static_boundary_interval_frame(frame,t0,t2,ok,reason)
    call assert_true(.not.ok,'stale endpoint rejected exactly')
  end subroutine test_exact_interval_identity_rejected_when_stale

end program test_boundq02b_immutable_boundary_frame
