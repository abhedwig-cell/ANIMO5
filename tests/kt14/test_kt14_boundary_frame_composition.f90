program test_kt14_boundary_frame_composition
  use iso_fortran_env, only: int64, real64
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate
  use mod_transient_contracts, only: transient_payload_t
  use mod_transient_transactions, only: accepted_store_t, accepted_store_generation, &
    accepted_store_time, snapshot_accepted_payload
  use mod_animo_hydrology_adapter, only: hydrology_step_t, HYDROLOGY_SCHEMA_ID, &
    HYDROLOGY_UNIT_CONTRACT_ID
  use mod_animo_bounded_no_ponding_upper_hydrology, only: &
    hydroexec01_start_context_t, make_hydroexec01_start_context
  use mod_animo_static_boundary_chemistry_adapter, only: &
    static_boundary_chemistry_t, read_rev53_static_boundary_chemistry, BOUNDQ01_OK
  use mod_animo_static_boundary_year_binding, only: &
    boundary_year_cursor_t, initialize_boundary_year_cursor
  use mod_animo_immutable_static_boundary_frame, only: &
    immutable_static_boundary_interval_frame_t, make_immutable_static_boundary_interval_frame
  use mod_animo_tcd042_upper_boundary_client, only: &
    tcd042_top_state_t, initialize_tcd042_store
  use mod_animo_tcd042_boundary_frame_composition, only: &
    kt14_composition_trace_t, execute_boundary_frame_tcd042_interval
  implicit none

  call test_valid_opaque_frame_commits()
  call test_stale_opaque_frame_rejects_before_science()
  call test_content_identity_is_bound_and_science_value_stable()
  call test_dry_deposition_is_not_wet_advective_forcing()
  print *, 'PASS_KT14B_OPAQUE_BOUNDARY_FRAME_TCD042_COMPOSITION'

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

  subroutine make_packet(prr, endpoint_day, step)
    real(real64),intent(in)::prr
    integer(int64),intent(in)::endpoint_day
    type(hydrology_step_t),intent(out)::step

    step=hydrology_step_t()
    step%schema_id=HYDROLOGY_SCHEMA_ID
    step%unit_contract_id=HYDROLOGY_UNIT_CONTRACT_ID
    step%layer_count=1
    step%drainage_count=0
    step%producer_endpoint_day=real(endpoint_day,real64)
    step%producer_step_days=1.0_real64
    step%prr=prr
    step%prsn=0.0_real64
    step%prirr=0.0_real64
    step%evicpr=0.0_real64
    step%evicirr=0.0_real64
    step%evsn=0.0_real64
    step%evso=0.0_real64
    step%evpn=0.0_real64
    step%evsoma=0.0_real64
    step%evtrma=0.0_real64
    step%runon=0.0_real64
    step%runoff=0.0_real64
    step%groundwater_level=1.0_real64
    step%ponding_end=0.0_real64
    step%snow_storage_end=0.0_real64
    step%water_balance_aeration=0.0_real64
    allocate(step%sc(1),step%mofrt(1),step%flev(1),step%flab(2))
    allocate(step%fldr(0,1),step%soil_temperature(0))
    step%sc(1)=-1.0_real64
    step%mofrt(1)=0.5_real64
    step%flev(1)=0.0_real64
    step%flab=0.0_real64
    step%has_interception_storage_end=.true.
    step%interception_storage_end=0.0_real64
    step%has_soil_temperature=.false.
  end subroutine make_packet

  subroutine make_start(value)
    type(hydroexec01_start_context_t),intent(out)::value
    logical::ok
    character(len=96)::reason
    call make_hydroexec01_start_context(0.0_real64,0.0_real64,0.0_real64, &
      0.5_real64,1.0_real64,0.0_real64,0.0_real64,0.0_real64,value,ok,reason)
    call assert_true(ok,'make HYDROEXEC01 start context')
  end subroutine make_start

  subroutine read_boundary(boundary)
    type(static_boundary_chemistry_t),intent(out)::boundary
    integer::status
    call read_rev53_static_boundary_chemistry('tests/boundq01/fixtures/static_no_p.inp',3,0,boundary,status)
    call assert_true(status==BOUNDQ01_OK,'read BOUNDQ01 fixture')
  end subroutine read_boundary

  subroutine make_frame(t0,t1,hash,boundary,frame)
    type(TimeCoordinate),intent(in)::t0,t1
    character(len=*),intent(in)::hash
    type(static_boundary_chemistry_t),intent(in)::boundary
    type(immutable_static_boundary_interval_frame_t),intent(out)::frame
    type(boundary_year_cursor_t)::cursor,next
    logical::ok
    character(len=128)::reason

    call initialize_boundary_year_cursor(cursor)
    call make_immutable_static_boundary_interval_frame(boundary,hash,2000,cursor, &
      t0,t1,frame,next,ok,reason)
    call assert_true(ok,'bind BOUNDQ02B opaque frame')
  end subroutine make_frame

  subroutine accepted_concentration(store,c)
    type(accepted_store_t),intent(in)::store
    real(real64),intent(out)::c
    class(transient_payload_t),allocatable::copy
    logical::ok
    call snapshot_accepted_payload(store,copy,ok)
    call assert_true(ok,'snapshot accepted payload')
    select type(typed=>copy)
    type is(tcd042_top_state_t)
      c=typed%concentration
    class default
      call assert_true(.false.,'accepted payload is not TCD042 state')
    end select
  end subroutine accepted_concentration

  subroutine assert_store_unchanged(store,origin_day,expected_c)
    type(accepted_store_t),intent(in)::store
    integer(int64),intent(in)::origin_day
    real(real64),intent(in)::expected_c
    type(TimeCoordinate)::t
    logical::ok
    real(real64)::c
    call assert_true(accepted_store_generation(store)==0_int64,'store generation unchanged')
    call accepted_store_time(store,t,ok)
    call assert_true(ok .and. t%day_index==origin_day,'store time unchanged')
    call accepted_concentration(store,c)
    call assert_true(transfer(c,0_int64)==transfer(expected_c,0_int64),'store concentration unchanged')
  end subroutine assert_store_unchanged

  subroutine test_valid_opaque_frame_commits()
    type(TimeCoordinate)::t0,t1
    type(hydrology_step_t)::packet
    type(hydroexec01_start_context_t)::start
    type(static_boundary_chemistry_t)::boundary
    type(immutable_static_boundary_interval_frame_t)::frame
    type(accepted_store_t)::store
    type(kt14_composition_trace_t)::trace
    logical::ok,success
    character(len=128)::reason
    real(real64)::c
    real(real64),parameter::tiny=2.0_real64**(-30)
    character(len=*),parameter::hash='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    call make_day(730119_int64,t0)
    call make_day(730120_int64,t1)
    call make_packet(tiny,730120_int64,packet)
    call make_start(start)
    call read_boundary(boundary)
    call make_frame(t0,t1,hash,boundary,frame)
    call initialize_tcd042_store(store,'KT14B-VALID',t0,1.0_real64,ok)
    call assert_true(ok,'initialize valid store')

    call execute_boundary_frame_tcd042_interval(store,packet, &
      'ANIMO_PG_86400_NOLEAPSECONDS_V1',0_int64,t0,t1,'KT14B-VALID-EXEC', &
      frame,1,1.0_real64,start,trace,success,reason)

    call assert_true(success,'valid opaque frame composition commits')
    call assert_true(trace%boundary_frame_validated,'opaque frame validated before science')
    call assert_true(trim(trace%boundary_content_sha256)==hash,'content hash propagated')
    call assert_true(trace%boundary_simulation_start_year==2000 .and. trace%boundary_nuyr==3, &
      'boundary metadata propagated')
    call assert_true(trace%boundary_selected_year==2000 .and. trace%boundary_selected_slot==1, &
      'year slot propagated')
    call assert_true(trace%science%science_runtime_committed,'KT13A science committed')
    call assert_true(trace%science%commit_count==1,'exactly one KT02 commit')
    call assert_true(transfer(trace%dry_deposition_nh,0_int64)==transfer(10.0_real64,0_int64), &
      'dry deposition remains separately visible')
    call accepted_concentration(store,c)
    call assert_true(transfer(trace%science%selected_load_rate,0_int64)== &
      int(z'3D70624DD2F1A9FC',int64),'slot-1 NH wet load exact')
    call assert_true(transfer(c,0_int64)==int(z'3FEFFFFFFF8020C5',int64), &
      'chemistry-bearing TCD042 end state exact')
    call assert_true(transfer(trace%science%average_concentration,0_int64)== &
      int(z'3FEFFFFFFFC01062',int64),'chemistry-bearing TCD042 average exact')
  end subroutine test_valid_opaque_frame_commits

  subroutine test_stale_opaque_frame_rejects_before_science()
    type(TimeCoordinate)::t0,t1,t2
    type(hydrology_step_t)::packet
    type(hydroexec01_start_context_t)::start
    type(static_boundary_chemistry_t)::boundary
    type(immutable_static_boundary_interval_frame_t)::frame
    type(accepted_store_t)::store
    type(kt14_composition_trace_t)::trace
    logical::ok,success
    character(len=128)::reason
    character(len=*),parameter::hash='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'

    call make_day(730119_int64,t0)
    call make_day(730120_int64,t1)
    call make_day(730121_int64,t2)
    call make_packet(0.0_real64,730121_int64,packet)
    call make_start(start)
    call read_boundary(boundary)
    call make_frame(t0,t1,hash,boundary,frame)
    call initialize_tcd042_store(store,'KT14B-STALE',t0,2.0_real64,ok)
    call assert_true(ok,'initialize stale-frame store')

    call execute_boundary_frame_tcd042_interval(store,packet, &
      'ANIMO_PG_86400_NOLEAPSECONDS_V1',0_int64,t0,t2,'KT14B-STALE-EXEC', &
      frame,1,1.0_real64,start,trace,success,reason)

    call assert_true(.not.success,'stale opaque interval frame rejected')
    call assert_true(.not.trace%boundary_frame_validated,'stale frame rejected before science')
    call assert_store_unchanged(store,730119_int64,2.0_real64)
  end subroutine test_stale_opaque_frame_rejects_before_science

  subroutine test_content_identity_is_bound_and_science_value_stable()
    type(TimeCoordinate)::t0,t1
    type(hydrology_step_t)::packet1,packet2
    type(hydroexec01_start_context_t)::start
    type(static_boundary_chemistry_t)::boundary
    type(immutable_static_boundary_interval_frame_t)::frame1,frame2
    type(accepted_store_t)::store1,store2
    type(kt14_composition_trace_t)::trace1,trace2
    logical::ok,success1,success2
    character(len=128)::reason
    real(real64)::c1,c2
    real(real64),parameter::tiny=2.0_real64**(-30)
    character(len=*),parameter::hash1='cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc'
    character(len=*),parameter::hash2='dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd'

    call make_day(730119_int64,t0)
    call make_day(730120_int64,t1)
    call make_packet(tiny,730120_int64,packet1)
    call make_packet(tiny,730120_int64,packet2)
    call make_start(start)
    call read_boundary(boundary)
    call make_frame(t0,t1,hash1,boundary,frame1)
    call make_frame(t0,t1,hash2,boundary,frame2)
    call initialize_tcd042_store(store1,'KT14B-HASH-A',t0,1.0_real64,ok)
    call assert_true(ok,'initialize hash A')
    call initialize_tcd042_store(store2,'KT14B-HASH-B',t0,1.0_real64,ok)
    call assert_true(ok,'initialize hash B')

    call execute_boundary_frame_tcd042_interval(store1,packet1, &
      'ANIMO_PG_86400_NOLEAPSECONDS_V1',0_int64,t0,t1,'KT14B-HASH-A-EXEC', &
      frame1,1,1.0_real64,start,trace1,success1,reason)
    call execute_boundary_frame_tcd042_interval(store2,packet2, &
      'ANIMO_PG_86400_NOLEAPSECONDS_V1',0_int64,t0,t1,'KT14B-HASH-B-EXEC', &
      frame2,1,1.0_real64,start,trace2,success2,reason)

    call assert_true(success1 .and. success2,'both content identities commit')
    call assert_true(trim(trace1%boundary_content_sha256)==hash1,'hash1 trace identity')
    call assert_true(trim(trace2%boundary_content_sha256)==hash2,'hash2 trace identity')
    call accepted_concentration(store1,c1)
    call accepted_concentration(store2,c2)
    call assert_true(transfer(c1,0_int64)==transfer(c2,0_int64), &
      'same chemistry yields same science despite distinct content identities')
  end subroutine test_content_identity_is_bound_and_science_value_stable

  subroutine test_dry_deposition_is_not_wet_advective_forcing()
    type(TimeCoordinate)::t0,t1
    type(hydrology_step_t)::packet1,packet2
    type(hydroexec01_start_context_t)::start
    type(static_boundary_chemistry_t)::boundary1,boundary2
    type(immutable_static_boundary_interval_frame_t)::frame1,frame2
    type(accepted_store_t)::store1,store2
    type(kt14_composition_trace_t)::trace1,trace2
    logical::ok,success1,success2
    character(len=128)::reason
    real(real64)::c1,c2
    real(real64),parameter::tiny=2.0_real64**(-30)
    character(len=*),parameter::hash1='eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
    character(len=*),parameter::hash2='ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'

    call make_day(730119_int64,t0)
    call make_day(730120_int64,t1)
    call make_packet(tiny,730120_int64,packet1)
    call make_packet(tiny,730120_int64,packet2)
    call make_start(start)
    call read_boundary(boundary1)
    boundary2=boundary1
    boundary2%dry_deposition_nh(1)=99.0_real64
    boundary2%dry_deposition_ni(1)=88.0_real64
    call make_frame(t0,t1,hash1,boundary1,frame1)
    call make_frame(t0,t1,hash2,boundary2,frame2)
    call initialize_tcd042_store(store1,'KT14B-DRY-A',t0,1.0_real64,ok)
    call assert_true(ok,'initialize dry A')
    call initialize_tcd042_store(store2,'KT14B-DRY-B',t0,1.0_real64,ok)
    call assert_true(ok,'initialize dry B')

    call execute_boundary_frame_tcd042_interval(store1,packet1, &
      'ANIMO_PG_86400_NOLEAPSECONDS_V1',0_int64,t0,t1,'KT14B-DRY-A-EXEC', &
      frame1,1,1.0_real64,start,trace1,success1,reason)
    call execute_boundary_frame_tcd042_interval(store2,packet2, &
      'ANIMO_PG_86400_NOLEAPSECONDS_V1',0_int64,t0,t1,'KT14B-DRY-B-EXEC', &
      frame2,1,1.0_real64,start,trace2,success2,reason)

    call assert_true(success1 .and. success2,'both dry-deposition variants commit')
    call accepted_concentration(store1,c1)
    call accepted_concentration(store2,c2)
    call assert_true(transfer(c1,0_int64)==transfer(c2,0_int64), &
      'dry deposition does not enter wet/advective TCD042 forcing')
    call assert_true(transfer(trace1%science%selected_load_rate,0_int64)== &
      transfer(trace2%science%selected_load_rate,0_int64),'load rate independent of dry deposition')
    call assert_true(transfer(trace1%dry_deposition_nh,0_int64)/= &
      transfer(trace2%dry_deposition_nh,0_int64),'dry deposition remains separately observable')
  end subroutine test_dry_deposition_is_not_wet_advective_forcing

end program test_kt14_boundary_frame_composition
