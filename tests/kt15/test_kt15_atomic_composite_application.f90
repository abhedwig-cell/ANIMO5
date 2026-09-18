program test_kt15_atomic_composite_application
  use iso_fortran_env, only: int64, real64
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate
  use mod_transient_contracts, only: transient_payload_t
  use mod_transient_transactions, only: accepted_store_t
  use mod_animo_hydrology_adapter, only: hydrology_step_t, HYDROLOGY_SCHEMA_ID, &
    HYDROLOGY_UNIT_CONTRACT_ID
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
    kt15_application_state_t, kt15_atomic_trace_t, make_kt15_application_config, &
    validate_kt15_application_config, same_kt15_application_config, &
    initialize_kt15_application_state, validate_kt15_application_state, &
    execute_kt15_atomic_interval, kt15_application_generation, kt15_application_time, &
    snapshot_kt15_science_payload, snapshot_kt15_continuation, &
    snapshot_kt15_application_config
  implicit none

  call test_two_interval_atomic_progression()
  call test_science_reject_preserves_full_application_state()
  call test_invalid_config_rejected_before_application_state()
  call test_config_is_immutable_across_intervals()
  print *, 'PASS_KT15A_IMMUTABLE_CONFIG_ATOMIC_COMPOSITE_APPLICATION'

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

  subroutine read_boundary(boundary)
    type(static_boundary_chemistry_t),intent(out)::boundary
    integer::status
    call read_rev53_static_boundary_chemistry('tests/boundq01/fixtures/static_no_p.inp',3,0,boundary,status)
    call assert_true(status==BOUNDQ01_OK,'read BOUNDQ01 fixture')
  end subroutine read_boundary

  subroutine make_static_config(value)
    type(kt15_static_hydrology_config_t),intent(out)::value
    value=kt15_static_hydrology_config_t()
    value%he_top=1.0_real64
    value%lefrrv=0.0_real64
    value%lefrso=0.0_real64
  end subroutine make_static_config

  subroutine initialize_application(lineage,t0,c0,runinu,hash,state,config)
    character(len=*),intent(in)::lineage,hash
    type(TimeCoordinate),intent(in)::t0
    real(real64),intent(in)::c0,runinu
    type(kt15_application_state_t),intent(out)::state
    type(kt15_application_config_t),intent(out)::config
    type(accepted_store_t)::store
    type(detailed_hydrology_origin_state_t)::origin
    type(boundary_year_cursor_t)::cursor
    type(composite_accepted_continuation_t)::cont
    type(kt15_static_hydrology_config_t)::hydro_cfg
    real(real64)::mofro(1)
    logical::ok
    character(len=128)::reason

    mofro=[0.5_real64]
    call initialize_tcd042_store(store,lineage,t0,c0,ok)
    call assert_true(ok,'initialize science store')
    call make_detailed_hydrology_origin_state(0.0_real64,0.0_real64,0.0_real64,mofro,origin,ok,reason)
    call assert_true(ok,'initialize hydrology origin')
    call initialize_boundary_year_cursor(cursor)
    call initialize_composite_continuation(lineage,t0,origin,runinu,cursor,cont,ok,reason)
    call assert_true(ok,'initialize composite continuation')
    call make_static_config(hydro_cfg)
    call make_kt15_application_config('ANIMO_PG_86400_NOLEAPSECONDS_V1',0_int64,hydro_cfg, &
      hash,2000,1,config,ok,reason)
    call assert_true(ok,'make immutable application config')
    call initialize_kt15_application_state(store,cont,config,state,ok,reason)
    call assert_true(ok,'initialize KT15A application')
  end subroutine initialize_application

  subroutine science_concentration(state,c)
    type(kt15_application_state_t),intent(in)::state
    real(real64),intent(out)::c
    class(transient_payload_t),allocatable::copy
    logical::ok
    call snapshot_kt15_science_payload(state,copy,ok)
    call assert_true(ok,'snapshot KT15 science')
    select type(typed=>copy)
    type is(tcd042_top_state_t)
      c=typed%concentration
    class default
      call assert_true(.false.,'wrong KT15 science payload')
    end select
  end subroutine science_concentration

  subroutine test_two_interval_atomic_progression()
    type(TimeCoordinate)::t0,t1,t2,t
    type(hydrology_step_t)::p1,p2
    type(static_boundary_chemistry_t)::boundary
    type(kt15_application_config_t)::cfg
    type(kt15_application_state_t)::state
    type(kt15_atomic_trace_t)::tr1,tr2
    type(composite_accepted_continuation_t)::cont
    logical::ok,success
    character(len=128)::reason
    real(real64)::c
    real(real64),parameter::tiny=2.0_real64**(-30)
    character(len=*),parameter::hash='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    call make_day(730119_int64,t0)
    call make_day(730120_int64,t1)
    call make_day(730121_int64,t2)
    call make_packet(tiny,730120_int64,p1)
    call make_packet(tiny,730121_int64,p2)
    call read_boundary(boundary)
    call initialize_application('KT15-TWO',t0,1.0_real64,0.0_real64,hash,state,cfg)
    call validate_kt15_application_config(cfg,ok,reason)
    call assert_true(ok,'two-interval config valid')

    call execute_kt15_atomic_interval(state,p1,t1,'KT15-I1',boundary,tr1,success,reason)
    call assert_true(success,'first atomic interval')
    call assert_true(tr1%boundary_bound .and. tr1%working_science_committed .and. &
      tr1%next_continuation_ready .and. tr1%external_group_published,'first atomic trace')
    call assert_true(tr1%origin_generation==0_int64 .and. tr1%published_generation==1_int64, &
      'first generation transition')
    call assert_true(trim(tr1%boundary_content_sha256)==hash,'content identity retained')
    call assert_true(tr1%selected_boundary_year==2000 .and. tr1%selected_boundary_slot==1, &
      'first boundary slot')
    call assert_true(kt15_application_generation(state)==1_int64,'state generation one')
    call snapshot_kt15_continuation(state,cont,ok)
    call assert_true(ok,'snapshot continuation after first')
    call assert_true(cont%generation==1_int64,'continuation generation one')
    call assert_true(cont%boundary_cursor%initialized .and. cont%boundary_cursor%active_slot==1, &
      'boundary cursor published with science')
    call assert_true(transfer(cont%hydrology_origin%mofro(1),0_int64)== &
      transfer(0.5_real64,0_int64),'hydrology endpoint published as next origin')

    call execute_kt15_atomic_interval(state,p2,t2,'KT15-I2',boundary,tr2,success,reason)
    call assert_true(success,'second atomic interval')
    call assert_true(tr2%origin_generation==1_int64 .and. tr2%published_generation==2_int64, &
      'second generation transition')
    call assert_true(tr2%selected_boundary_slot==1,'non-Jan1 interval retains slot one')
    call assert_true(kt15_application_generation(state)==2_int64,'state generation two')
    call kt15_application_time(state,t,ok)
    call assert_true(ok .and. t%day_index==730121_int64,'state time reaches second endpoint')
    call snapshot_kt15_continuation(state,cont,ok)
    call assert_true(ok .and. cont%generation==2_int64,'continuation generation two')
    call assert_true(cont%accepted_time%day_index==730121_int64,'continuation time second endpoint')
    call science_concentration(state,c)
    call assert_true(c<1.0_real64 .and. c>0.0_real64,'science state advanced over two intervals')
    call validate_kt15_application_state(state,ok,reason)
    call assert_true(ok,'final application aggregate coherent')
  end subroutine test_two_interval_atomic_progression

  subroutine test_science_reject_preserves_full_application_state()
    type(TimeCoordinate)::t0,t1,t
    type(hydrology_step_t)::packet
    type(static_boundary_chemistry_t)::boundary
    type(kt15_application_config_t)::cfg
    type(kt15_application_state_t)::state
    type(kt15_atomic_trace_t)::trace
    type(composite_accepted_continuation_t)::before,after
    logical::ok,success
    character(len=128)::reason
    real(real64)::c
    real(real64),parameter::too_large=2.0_real64**(-26)
    character(len=*),parameter::hash='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'

    call make_day(730119_int64,t0)
    call make_day(730120_int64,t1)
    call make_packet(too_large,730120_int64,packet)
    call read_boundary(boundary)
    call initialize_application('KT15-REJECT',t0,4.0_real64,0.0_real64,hash,state,cfg)
    call validate_kt15_application_config(cfg,ok,reason)
    call assert_true(ok,'reject config valid')
    call snapshot_kt15_continuation(state,before,ok)
    call assert_true(ok,'snapshot before reject')

    call execute_kt15_atomic_interval(state,packet,t1,'KT15-REJECT-I1',boundary,trace,success,reason)

    call assert_true(.not.success,'out-of-scope science rejects group')
    call assert_true(trace%boundary_bound,'boundary candidate was prepared')
    call assert_true(.not.trace%external_group_published,'external group not published')
    call assert_true(kt15_application_generation(state)==0_int64,'generation unchanged')
    call kt15_application_time(state,t,ok)
    call assert_true(ok .and. t%day_index==730119_int64,'time unchanged')
    call science_concentration(state,c)
    call assert_true(transfer(c,0_int64)==transfer(4.0_real64,0_int64),'science unchanged')
    call snapshot_kt15_continuation(state,after,ok)
    call assert_true(ok,'snapshot after reject')
    call assert_true(after%generation==before%generation,'continuation generation unchanged')
    call assert_true(.not.after%boundary_cursor%initialized,'boundary cursor candidate not published')
    call assert_true(after%accepted_time%day_index==before%accepted_time%day_index, &
      'continuation time unchanged')
  end subroutine test_science_reject_preserves_full_application_state

  subroutine test_invalid_config_rejected_before_application_state()
    type(kt15_static_hydrology_config_t)::hydro_cfg
    type(kt15_application_config_t)::config
    logical::ok
    character(len=128)::reason

    call make_static_config(hydro_cfg)
    call make_kt15_application_config('ANIMO_PG_86400_NOLEAPSECONDS_V1',0_int64,hydro_cfg, &
      'NOT-A-SHA256',2000,1,config,ok,reason)
    call assert_true(.not.ok,'invalid boundary content identity rejected by config')

    call make_kt15_application_config('',0_int64,hydro_cfg, &
      'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',2000,1,config,ok,reason)
    call assert_true(.not.ok,'missing calendar rejected by config')

    call make_kt15_application_config('ANIMO_PG_86400_NOLEAPSECONDS_V1',0_int64,hydro_cfg, &
      'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',2000,7,config,ok,reason)
    call assert_true(.not.ok,'invalid load channel rejected by config')
  end subroutine test_invalid_config_rejected_before_application_state

  subroutine test_config_is_immutable_across_intervals()
    type(TimeCoordinate)::t0,t1,t2
    type(hydrology_step_t)::p1,p2
    type(static_boundary_chemistry_t)::boundary
    type(kt15_application_state_t)::state
    type(kt15_application_config_t)::initial_cfg,after_cfg
    type(kt15_atomic_trace_t)::tr
    logical::ok,success
    character(len=128)::reason
    real(real64),parameter::tiny=2.0_real64**(-30)
    character(len=*),parameter::hash='cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc'

    call make_day(730119_int64,t0)
    call make_day(730120_int64,t1)
    call make_day(730121_int64,t2)
    call make_packet(tiny,730120_int64,p1)
    call make_packet(tiny,730121_int64,p2)
    call read_boundary(boundary)
    call initialize_application('KT15A-CONFIG',t0,1.0_real64,0.0_real64,hash,state,initial_cfg)

    call execute_kt15_atomic_interval(state,p1,t1,'KT15A-CONFIG-I1',boundary,tr,success,reason)
    call assert_true(success,'config interval one')
    call execute_kt15_atomic_interval(state,p2,t2,'KT15A-CONFIG-I2',boundary,tr,success,reason)
    call assert_true(success,'config interval two')
    call snapshot_kt15_application_config(state,after_cfg,ok)
    call assert_true(ok,'snapshot immutable config')
    call assert_true(same_kt15_application_config(initial_cfg,after_cfg), &
      'accepted application config unchanged across intervals')
    call validate_kt15_application_config(after_cfg,ok,reason)
    call assert_true(ok,'persisted config remains valid')
  end subroutine test_config_is_immutable_across_intervals

end program test_kt15_atomic_composite_application
