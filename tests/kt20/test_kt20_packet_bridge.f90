program test_kt20_packet_bridge
  use iso_fortran_env, only: int64, real64
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate
  use mod_transient_contracts, only: transient_payload_t
  use mod_transient_transactions, only: accepted_store_t
  use mod_animo_hydrology_adapter, only: hydrology_step_t
  use mod_animo_multi_packet_hydrology_provider, only: &
    animo_multi_packet_hydrology_runtime_probe_client_t, initialize_multi_packet_client
  use mod_animo_static_boundary_chemistry_adapter, only: &
    static_boundary_chemistry_t, read_rev53_static_boundary_chemistry, BOUNDQ01_OK
  use mod_animo_static_boundary_year_binding, only: &
    boundary_year_cursor_t, initialize_boundary_year_cursor
  use mod_animo_detailed_hydrology_origin_state, only: &
    detailed_hydrology_origin_state_t, make_detailed_hydrology_origin_state
  use mod_animo_composite_accepted_continuation, only: &
    composite_accepted_continuation_t, initialize_composite_continuation
  use mod_animo_tcd042_upper_boundary_client, only: &
    tcd042_top_state_t, initialize_tcd042_store
  use mod_animo_atomic_composite_application, only: &
    kt15_static_hydrology_config_t, kt15_application_config_t, &
    kt15_application_state_t, make_kt15_application_config, &
    initialize_kt15_application_state, kt15_application_generation, &
    kt15_application_time, snapshot_kt15_science_payload
  use mod_animo_provider_backed_application, only: &
    kt18_provider_application_trace_t, execute_provider_backed_application_interval
  use mod_animo_kt20_hydrology_packet_frame, only: read_kt20_hydrology_packet_frame
  implicit none

  character(len=*), parameter :: CAL='ANIMO_PG_86400_NOLEAPSECONDS_V1'
  character(len=*), parameter :: BOUNDARY_HASH = &
    '629a94972504c2865f8f0cbae9960e1354f6acd09e39ef663cc8f74375a7a169'
  character(len=*), parameter :: FIRST_TYPED = &
    'eeeb862839cce8111535fae86220d8574240804b9f6f029f7ec8e07ceb65da1c'

  call test_real_source_packet_reaches_kt18_and_fails_closed()
  call test_synthetic_control_frame_commits_through_kt18()
  print *, 'PASS_KT20_KT19_PACKET_FRAME_TO_KT18_APPLICATION'

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
    call make_time_coordinate(CAL,day,0_int64,1_int64,value,ok)
    call assert_true(ok,'make exact day')
  end subroutine make_day

  subroutine read_boundary(boundary)
    type(static_boundary_chemistry_t),intent(out)::boundary
    integer::status
    call read_rev53_static_boundary_chemistry('tests/boundq01/fixtures/static_no_p.inp',3,0,boundary,status)
    call assert_true(status==BOUNDQ01_OK,'read bounded chemistry fixture')
  end subroutine read_boundary

  subroutine initialize_application(lineage,packet,state)
    character(len=*),intent(in)::lineage
    type(hydrology_step_t),intent(in)::packet
    type(kt15_application_state_t),intent(out)::state
    type(TimeCoordinate)::t0
    type(accepted_store_t)::store
    type(detailed_hydrology_origin_state_t)::origin
    type(boundary_year_cursor_t)::cursor
    type(composite_accepted_continuation_t)::cont
    type(kt15_static_hydrology_config_t)::hydro
    type(kt15_application_config_t)::config
    real(real64),allocatable::mofro(:)
    logical::ok
    character(len=128)::reason

    call make_day(0_int64,t0)
    call initialize_tcd042_store(store,lineage,t0,1.0_real64,ok)
    call assert_true(ok,'initialize accepted science store')

    allocate(mofro(packet%layer_count))
    mofro=0.5_real64
    call make_detailed_hydrology_origin_state(0.0_real64,0.0_real64,0.0_real64, &
      mofro,origin,ok,reason)
    call assert_true(ok,'initialize explicit hydrology origin')

    call initialize_boundary_year_cursor(cursor)
    call initialize_composite_continuation(lineage,t0,origin,0.0_real64,cursor,cont,ok,reason)
    call assert_true(ok,'initialize composite continuation')

    hydro=kt15_static_hydrology_config_t()
    hydro%he_top=1.0_real64
    hydro%lefrrv=0.0_real64
    hydro%lefrso=0.0_real64
    call make_kt15_application_config(CAL,0_int64,hydro,BOUNDARY_HASH,1,1,config,ok,reason)
    call assert_true(ok,'initialize immutable application config')

    call initialize_kt15_application_state(store,cont,config,state,ok,reason)
    call assert_true(ok,'initialize accepted application')
  end subroutine initialize_application

  subroutine snapshot_concentration(state,value)
    type(kt15_application_state_t),intent(in)::state
    real(real64),intent(out)::value
    class(transient_payload_t),allocatable::copy
    logical::ok
    call snapshot_kt15_science_payload(state,copy,ok)
    call assert_true(ok,'snapshot science payload')
    select type(typed=>copy)
    type is(tcd042_top_state_t)
      value=typed%concentration
    class default
      call assert_true(.false.,'unexpected science payload type')
    end select
  end subroutine snapshot_concentration

  subroutine assert_application_origin_unchanged(state)
    type(kt15_application_state_t),intent(in)::state
    type(TimeCoordinate)::t
    real(real64)::c
    logical::ok
    call assert_true(kt15_application_generation(state)==0_int64,'application generation unchanged')
    call kt15_application_time(state,t,ok)
    call assert_true(ok .and. t%day_index==0_int64,'application time unchanged')
    call snapshot_concentration(state,c)
    call assert_true(transfer(c,0_int64)==transfer(1.0_real64,0_int64),'science state unchanged')
  end subroutine assert_application_origin_unchanged

  subroutine test_real_source_packet_reaches_kt18_and_fails_closed()
    type(hydrology_step_t)::packet,packets(1)
    type(animo_multi_packet_hydrology_runtime_probe_client_t)::provider
    type(kt15_application_state_t)::state
    type(static_boundary_chemistry_t)::boundary
    type(kt18_provider_application_trace_t)::trace
    type(TimeCoordinate)::endpoint
    logical::ok,success
    character(len=160)::reason
    character(len=64)::digest

    call read_kt20_hydrology_packet_frame('build/kt20/real_first_packet.frame', &
      packet,digest,ok,reason)
    call assert_true(ok,'decode real-source-derived packet frame')
    call assert_true(trim(digest)==FIRST_TYPED,'real packet typed identity preserved')
    call assert_true(packet%layer_count==30 .and. packet%drainage_count==5,'real LWKM dimensions')
    call assert_true(transfer(packet%producer_endpoint_day,0_int64)== &
      transfer(10.0_real64,0_int64),'real producer endpoint exact')
    call assert_true(transfer(packet%producer_step_days,0_int64)== &
      transfer(10.0_real64,0_int64),'real producer duration exact')

    packets(1)=packet
    call initialize_multi_packet_client(provider,packets,CAL,0_int64,ok,reason)
    call assert_true(ok,'initialize KT11 provider from KT20 real packet')
    call initialize_application('KT20-REAL',packet,state)
    call read_boundary(boundary)
    call make_day(10_int64,endpoint)

    call execute_provider_backed_application_interval(provider,state,endpoint, &
      'KT20-REAL-I1',boundary,trace,success,reason)

    call assert_true(trace%provider_packet_selected,'KT18 selected decoded real packet')
    call assert_true(.not.success,'real first packet stays outside bounded admitted application')
    call assert_true(.not.trace%application_interval_committed,'real first packet not published')
    call assert_application_origin_unchanged(state)
  end subroutine test_real_source_packet_reaches_kt18_and_fails_closed

  subroutine test_synthetic_control_frame_commits_through_kt18()
    type(hydrology_step_t)::packet,packets(1)
    type(animo_multi_packet_hydrology_runtime_probe_client_t)::provider
    type(kt15_application_state_t)::state
    type(static_boundary_chemistry_t)::boundary
    type(kt18_provider_application_trace_t)::trace
    type(TimeCoordinate)::endpoint,t
    logical::ok,success
    character(len=160)::reason
    character(len=64)::digest
    real(real64)::c

    call read_kt20_hydrology_packet_frame('build/kt20/synthetic_commit_control.frame', &
      packet,digest,ok,reason)
    call assert_true(ok,'decode synthetic commit-control frame')
    packets(1)=packet
    call initialize_multi_packet_client(provider,packets,CAL,0_int64,ok,reason)
    call assert_true(ok,'initialize KT11 provider from synthetic KT20 frame')

    call initialize_application('KT20-CONTROL',packet,state)
    call read_boundary(boundary)
    call make_day(1_int64,endpoint)

    call execute_provider_backed_application_interval(provider,state,endpoint, &
      'KT20-CONTROL-I1',boundary,trace,success,reason)

    call assert_true(success,'synthetic frame commits through KT18')
    call assert_true(trace%provider_packet_selected,'control packet selected')
    call assert_true(trace%application_interval_committed,'control application published')
    call assert_true(kt15_application_generation(state)==1_int64,'control generation advanced')
    call kt15_application_time(state,t,ok)
    call assert_true(ok .and. t%day_index==1_int64,'control accepted endpoint')
    call snapshot_concentration(state,c)
    call assert_true(c>0.0_real64,'control science state finite positive after commit')
  end subroutine test_synthetic_control_frame_commits_through_kt18

end program test_kt20_packet_bridge
