program test_kt18_provider_backed_application
  use iso_fortran_env, only: int64, real64
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate
  use mod_transient_contracts, only: transient_payload_t
  use mod_transient_transactions, only: accepted_store_t
  use mod_animo_hydrology_adapter, only: hydrology_step_t, HYDROLOGY_SCHEMA_ID, &
    HYDROLOGY_UNIT_CONTRACT_ID
  use mod_animo_multi_packet_hydrology_provider, only: &
    animo_multi_packet_hydrology_runtime_probe_client_t, initialize_multi_packet_client, &
    select_multi_packet_hydrology_step_copy
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
  implicit none

  character(len=*),parameter::CAL='ANIMO_PG_86400_NOLEAPSECONDS_V1'
  character(len=*),parameter::BOUNDARY_HASH = &
    '629a94972504c2865f8f0cbae9960e1354f6acd09e39ef663cc8f74375a7a169'

  call test_out_of_order_provider_two_interval_application()
  call test_missing_provider_packet_preserves_application()
  call test_provider_application_offset_mismatch_preserves_application()
  call test_selected_copy_is_nonowning_and_repeatable()
  print *, 'PASS_KT18_MULTI_PACKET_PROVIDER_ACCEPTED_APPLICATION'

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
    call assert_true(ok,'make day')
  end subroutine make_day

  subroutine make_packet(endpoint_day,prr,packet)
    integer(int64),intent(in)::endpoint_day
    real(real64),intent(in)::prr
    type(hydrology_step_t),intent(out)::packet

    packet=hydrology_step_t()
    packet%schema_id=HYDROLOGY_SCHEMA_ID
    packet%unit_contract_id=HYDROLOGY_UNIT_CONTRACT_ID
    packet%layer_count=1
    packet%drainage_count=0
    packet%producer_endpoint_day=real(endpoint_day,real64)
    packet%producer_step_days=1.0_real64
    packet%prr=prr
    packet%prsn=0.0_real64
    packet%prirr=0.0_real64
    packet%evicpr=0.0_real64
    packet%evicirr=0.0_real64
    packet%evsn=0.0_real64
    packet%evso=0.0_real64
    packet%evpn=0.0_real64
    packet%evsoma=0.0_real64
    packet%evtrma=0.0_real64
    packet%runon=0.0_real64
    packet%runoff=0.0_real64
    packet%groundwater_level=1.0_real64
    packet%ponding_end=0.0_real64
    packet%snow_storage_end=0.0_real64
    packet%water_balance_aeration=0.0_real64
    allocate(packet%sc(1),packet%mofrt(1),packet%flev(1),packet%flab(2))
    allocate(packet%fldr(0,1),packet%soil_temperature(0))
    packet%sc(1)=-1.0_real64
    packet%mofrt(1)=0.5_real64
    packet%flev(1)=0.0_real64
    packet%flab=0.0_real64
    packet%has_interception_storage_end=.true.
    packet%interception_storage_end=0.0_real64
    packet%has_soil_temperature=.false.
  end subroutine make_packet

  subroutine read_boundary(boundary)
    type(static_boundary_chemistry_t),intent(out)::boundary
    integer::status
    call read_rev53_static_boundary_chemistry('tests/boundq01/fixtures/static_no_p.inp',3,0,boundary,status)
    call assert_true(status==BOUNDQ01_OK,'read static boundary fixture')
  end subroutine read_boundary

  subroutine make_config(offset,config)
    integer(int64),intent(in)::offset
    type(kt15_application_config_t),intent(out)::config
    type(kt15_static_hydrology_config_t)::hydro
    logical::ok
    character(len=128)::reason

    hydro=kt15_static_hydrology_config_t()
    hydro%he_top=1.0_real64
    hydro%lefrrv=0.0_real64
    hydro%lefrso=0.0_real64
    call make_kt15_application_config(CAL,offset,hydro,BOUNDARY_HASH,2000,1,config,ok,reason)
    call assert_true(ok,'make application config')
  end subroutine make_config

  subroutine initialize_application(lineage,config,state)
    character(len=*),intent(in)::lineage
    type(kt15_application_config_t),intent(in)::config
    type(kt15_application_state_t),intent(out)::state

    type(TimeCoordinate)::t0
    type(accepted_store_t)::store
    type(detailed_hydrology_origin_state_t)::origin
    type(boundary_year_cursor_t)::cursor
    type(composite_accepted_continuation_t)::cont
    real(real64)::mofro(1)
    logical::ok
    character(len=128)::reason

    call make_day(730119_int64,t0)
    call initialize_tcd042_store(store,lineage,t0,1.0_real64,ok)
    call assert_true(ok,'init science store')
    mofro=[0.5_real64]
    call make_detailed_hydrology_origin_state(0.0_real64,0.0_real64,0.0_real64,mofro,origin,ok,reason)
    call assert_true(ok,'init hydro origin')
    call initialize_boundary_year_cursor(cursor)
    call initialize_composite_continuation(lineage,t0,origin,0.0_real64,cursor,cont,ok,reason)
    call assert_true(ok,'init continuation')
    call initialize_kt15_application_state(store,cont,config,state,ok,reason)
    call assert_true(ok,'init accepted app')
  end subroutine initialize_application

  subroutine snapshot_concentration(state,value)
    type(kt15_application_state_t),intent(in)::state
    real(real64),intent(out)::value
    class(transient_payload_t),allocatable::copy
    logical::ok
    call snapshot_kt15_science_payload(state,copy,ok)
    call assert_true(ok,'snapshot science')
    select type(typed=>copy)
    type is(tcd042_top_state_t)
      value=typed%concentration
    class default
      call assert_true(.false.,'wrong science type')
    end select
  end subroutine snapshot_concentration

  subroutine assert_state_unchanged(state,expected_generation,expected_day,expected_conc)
    type(kt15_application_state_t),intent(in)::state
    integer(int64),intent(in)::expected_generation,expected_day
    real(real64),intent(in)::expected_conc
    type(TimeCoordinate)::t
    logical::ok
    real(real64)::c
    call assert_true(kt15_application_generation(state)==expected_generation,'generation unchanged')
    call kt15_application_time(state,t,ok)
    call assert_true(ok .and. t%day_index==expected_day,'accepted time unchanged')
    call snapshot_concentration(state,c)
    call assert_true(transfer(c,0_int64)==transfer(expected_conc,0_int64),'science unchanged')
  end subroutine assert_state_unchanged

  subroutine test_out_of_order_provider_two_interval_application()
    type(hydrology_step_t)::packets(2)
    type(animo_multi_packet_hydrology_runtime_probe_client_t)::provider
    type(kt15_application_config_t)::config
    type(kt15_application_state_t)::state
    type(static_boundary_chemistry_t)::boundary
    type(TimeCoordinate)::t1,t2,tfinal
    type(kt18_provider_application_trace_t)::trace
    logical::ok,success
    character(len=160)::reason
    real(real64),parameter::tiny=2.0_real64**(-30)

    ! Deliberately reverse storage order. Provider key identity, not array order,
    ! determines the packet.
    call make_packet(730121_int64,tiny,packets(1))
    call make_packet(730120_int64,tiny,packets(2))
    call initialize_multi_packet_client(provider,packets,CAL,0_int64,ok,reason)
    call assert_true(ok,'provider init out-of-order')

    call make_config(0_int64,config)
    call initialize_application('KT18-TWO',config,state)
    call read_boundary(boundary)
    call make_day(730120_int64,t1)
    call make_day(730121_int64,t2)

    call execute_provider_backed_application_interval(provider,state,t1,'KT18-I1',boundary, &
      trace,success,reason)
    call assert_true(success,'provider-backed interval 1')
    call assert_true(trace%provider_packet_selected,'interval1 packet selected')
    call assert_true(trace%application_interval_committed,'interval1 application committed')
    call assert_true(transfer(trace%selected_producer_endpoint_day,0_int64)== &
      transfer(real(730120_int64,real64),0_int64),'interval1 endpoint selected exactly')

    call execute_provider_backed_application_interval(provider,state,t2,'KT18-I2',boundary, &
      trace,success,reason)
    call assert_true(success,'provider-backed interval 2')
    call assert_true(kt15_application_generation(state)==2_int64,'two application generations')
    call kt15_application_time(state,tfinal,ok)
    call assert_true(ok .and. tfinal%day_index==730121_int64,'two interval final time')
  end subroutine test_out_of_order_provider_two_interval_application

  subroutine test_missing_provider_packet_preserves_application()
    type(hydrology_step_t)::packets(1)
    type(animo_multi_packet_hydrology_runtime_probe_client_t)::provider
    type(kt15_application_config_t)::config
    type(kt15_application_state_t)::state
    type(static_boundary_chemistry_t)::boundary
    type(TimeCoordinate)::t1
    type(kt18_provider_application_trace_t)::trace
    logical::ok,success
    character(len=160)::reason

    call make_packet(730121_int64,0.0_real64,packets(1))
    call initialize_multi_packet_client(provider,packets,CAL,0_int64,ok,reason)
    call assert_true(ok,'missing provider init')
    call make_config(0_int64,config)
    call initialize_application('KT18-MISSING',config,state)
    call read_boundary(boundary)
    call make_day(730120_int64,t1)

    call execute_provider_backed_application_interval(provider,state,t1,'KT18-MISSING-I1', &
      boundary,trace,success,reason)
    call assert_true(.not.success,'missing provider packet rejected')
    call assert_true(.not.trace%provider_packet_selected,'missing packet never selected')
    call assert_true(.not.trace%application_interval_committed,'missing packet no application commit')
    call assert_state_unchanged(state,0_int64,730119_int64,1.0_real64)
  end subroutine test_missing_provider_packet_preserves_application

  subroutine test_provider_application_offset_mismatch_preserves_application()
    type(hydrology_step_t)::packets(1)
    type(animo_multi_packet_hydrology_runtime_probe_client_t)::provider
    type(kt15_application_config_t)::config
    type(kt15_application_state_t)::state
    type(static_boundary_chemistry_t)::boundary
    type(TimeCoordinate)::t1
    type(kt18_provider_application_trace_t)::trace
    logical::ok,success
    character(len=160)::reason
    real(real64),parameter::tiny=2.0_real64**(-30)

    ! Provider maps runtime endpoint 730120 to producer endpoint 730121.
    ! The application config remains offset zero, so nested KT06 must reject
    ! the selected packet before publication.
    call make_packet(730121_int64,tiny,packets(1))
    call initialize_multi_packet_client(provider,packets,CAL,1_int64,ok,reason)
    call assert_true(ok,'offset mismatch provider init')
    call make_config(0_int64,config)
    call initialize_application('KT18-OFFSET',config,state)
    call read_boundary(boundary)
    call make_day(730120_int64,t1)

    call execute_provider_backed_application_interval(provider,state,t1,'KT18-OFFSET-I1', &
      boundary,trace,success,reason)
    call assert_true(.not.success,'provider/application offset mismatch rejected')
    call assert_true(trace%provider_packet_selected,'provider selected its own mapped packet')
    call assert_true(.not.trace%application_interval_committed,'offset mismatch no application commit')
    call assert_state_unchanged(state,0_int64,730119_int64,1.0_real64)
  end subroutine test_provider_application_offset_mismatch_preserves_application

  subroutine test_selected_copy_is_nonowning_and_repeatable()
    type(hydrology_step_t)::packets(1),copy1,copy2
    type(animo_multi_packet_hydrology_runtime_probe_client_t)::provider
    type(TimeCoordinate)::t0,t1
    logical::ok
    character(len=160)::reason
    real(real64),parameter::tiny=2.0_real64**(-30)

    call make_packet(730120_int64,tiny,packets(1))
    call initialize_multi_packet_client(provider,packets,CAL,0_int64,ok,reason)
    call assert_true(ok,'copy provider init')
    call make_day(730119_int64,t0)
    call make_day(730120_int64,t1)

    call select_multi_packet_hydrology_step_copy(provider,t0,t1,copy1,ok,reason)
    call assert_true(ok,'first selection copy')
    copy1%prr=123.0_real64

    call select_multi_packet_hydrology_step_copy(provider,t0,t1,copy2,ok,reason)
    call assert_true(ok,'second selection copy')
    call assert_true(transfer(copy2%prr,0_int64)==transfer(tiny,0_int64), &
      'mutating returned copy cannot mutate provider-owned forcing')
  end subroutine test_selected_copy_is_nonowning_and_repeatable

end program test_kt18_provider_backed_application
