program test_kt16_accepted_application_checkpoint
  use iso_fortran_env, only: int64, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_value, ieee_quiet_nan
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
    same_kt15_application_config, initialize_kt15_application_state, &
    execute_kt15_atomic_interval, kt15_application_generation, kt15_application_time, &
    snapshot_kt15_science_payload, snapshot_kt15_continuation, snapshot_kt15_application_config
  use mod_animo_accepted_application_checkpoint, only: &
    kt16_application_checkpoint_t, encode_kt16_application_checkpoint, &
    validate_kt16_application_checkpoint, restore_kt16_application_checkpoint
  implicit none

  call test_split_run_matches_uninterrupted_exactly()
  call test_corrupt_checkpoint_rejected()
  call test_wrong_expected_config_rejected()
  print *, 'PASS_KT16_ACCEPTED_APPLICATION_CHECKPOINT_RESTART'

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

  subroutine make_config(hash,load_channel,config)
    character(len=*),intent(in)::hash
    integer,intent(in)::load_channel
    type(kt15_application_config_t),intent(out)::config
    type(kt15_static_hydrology_config_t)::hydro
    logical::ok
    character(len=128)::reason

    hydro=kt15_static_hydrology_config_t()
    hydro%he_top=1.0_real64
    hydro%lefrrv=0.0_real64
    hydro%lefrso=0.0_real64
    call make_kt15_application_config('ANIMO_PG_86400_NOLEAPSECONDS_V1',0_int64,hydro, &
      hash,2000,load_channel,config,ok,reason)
    call assert_true(ok,'make KT15A config')
  end subroutine make_config

  subroutine initialize_application(lineage,t0,c0,config,state)
    character(len=*),intent(in)::lineage
    type(TimeCoordinate),intent(in)::t0
    real(real64),intent(in)::c0
    type(kt15_application_config_t),intent(in)::config
    type(kt15_application_state_t),intent(out)::state
    type(accepted_store_t)::store
    type(detailed_hydrology_origin_state_t)::origin
    type(boundary_year_cursor_t)::cursor
    type(composite_accepted_continuation_t)::cont
    real(real64)::mofro(1)
    logical::ok
    character(len=128)::reason

    mofro=[0.5_real64]
    call initialize_tcd042_store(store,lineage,t0,c0,ok)
    call assert_true(ok,'initialize science store')
    call make_detailed_hydrology_origin_state(0.0_real64,0.0_real64,0.0_real64,mofro,origin,ok,reason)
    call assert_true(ok,'initialize hydrology origin')
    call initialize_boundary_year_cursor(cursor)
    ! Synthetic first-call Runinu=0 is a test fixture only; no historical claim.
    call initialize_composite_continuation(lineage,t0,origin,0.0_real64,cursor,cont,ok,reason)
    call assert_true(ok,'initialize continuation')
    call initialize_kt15_application_state(store,cont,config,state,ok,reason)
    call assert_true(ok,'initialize application')
  end subroutine initialize_application

  subroutine science_concentration(state,c)
    type(kt15_application_state_t),intent(in)::state
    real(real64),intent(out)::c
    class(transient_payload_t),allocatable::copy
    logical::ok
    call snapshot_kt15_science_payload(state,copy,ok)
    call assert_true(ok,'snapshot science')
    select type(typed=>copy)
    type is(tcd042_top_state_t)
      c=typed%concentration
    class default
      call assert_true(.false.,'wrong science payload')
    end select
  end subroutine science_concentration

  subroutine assert_time_equal_exact(a,b,message)
    type(TimeCoordinate),intent(in)::a,b
    character(len=*),intent(in)::message
    call assert_true(trim(a%calendar_contract_id)==trim(b%calendar_contract_id),trim(message)//' calendar')
    call assert_true(a%day_index==b%day_index,trim(message)//' day')
    call assert_true(a%subday_numerator==b%subday_numerator,trim(message)//' numerator')
    call assert_true(a%subday_denominator==b%subday_denominator,trim(message)//' denominator')
  end subroutine assert_time_equal_exact

  subroutine assert_continuation_equal_exact(a,b)
    type(composite_accepted_continuation_t),intent(in)::a,b
    integer::i
    call assert_true(trim(a%lineage_id)==trim(b%lineage_id),'continuation lineage exact')
    call assert_true(a%generation==b%generation,'continuation generation exact')
    call assert_time_equal_exact(a%accepted_time,b%accepted_time,'continuation time')
    call assert_true(size(a%hydrology_origin%mofro)==size(b%hydrology_origin%mofro),'Mofro size exact')
    call assert_true(transfer(a%hydrology_origin%pn,0_int64)==transfer(b%hydrology_origin%pn,0_int64), &
      'Pn exact')
    call assert_true(transfer(a%hydrology_origin%sic,0_int64)==transfer(b%hydrology_origin%sic,0_int64), &
      'Sic exact')
    call assert_true(transfer(a%hydrology_origin%snla,0_int64)==transfer(b%hydrology_origin%snla,0_int64), &
      'Snla exact')
    do i=1,size(a%hydrology_origin%mofro)
      call assert_true(transfer(a%hydrology_origin%mofro(i),0_int64)== &
        transfer(b%hydrology_origin%mofro(i),0_int64),'Mofro exact')
    end do
    call assert_true(transfer(a%runinu_call_entry,0_int64)==transfer(b%runinu_call_entry,0_int64), &
      'Runinu exact')
    call assert_true(a%boundary_cursor%initialized .eqv. b%boundary_cursor%initialized, &
      'cursor initialized exact')
    call assert_true(a%boundary_cursor%active_year==b%boundary_cursor%active_year,'cursor year exact')
    call assert_true(a%boundary_cursor%active_slot==b%boundary_cursor%active_slot,'cursor slot exact')
  end subroutine assert_continuation_equal_exact

  subroutine test_split_run_matches_uninterrupted_exactly()
    type(TimeCoordinate)::t0,t1,t2,ta,tb
    type(hydrology_step_t)::p1,p2
    type(static_boundary_chemistry_t)::boundary
    type(kt15_application_config_t)::config,ca,cb
    type(kt15_application_state_t)::continuous,split,restored
    type(kt15_atomic_trace_t)::trace
    type(kt16_application_checkpoint_t)::checkpoint
    type(composite_accepted_continuation_t)::cont_a,cont_b
    logical::ok,success
    character(len=128)::reason
    real(real64)::conc_a,conc_b
    real(real64),parameter::tiny=2.0_real64**(-30)
    character(len=*),parameter::hash='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    call make_day(730119_int64,t0)
    call make_day(730120_int64,t1)
    call make_day(730121_int64,t2)
    call make_packet(tiny,730120_int64,p1)
    call make_packet(tiny,730121_int64,p2)
    call read_boundary(boundary)
    call make_config(hash,1,config)
    call initialize_application('KT16-SPLIT',t0,1.0_real64,config,continuous)
    call initialize_application('KT16-SPLIT',t0,1.0_real64,config,split)

    call execute_kt15_atomic_interval(continuous,p1,t1,'CONT-I1',boundary,trace,success,reason)
    call assert_true(success,'continuous interval 1')
    call execute_kt15_atomic_interval(continuous,p2,t2,'CONT-I2',boundary,trace,success,reason)
    call assert_true(success,'continuous interval 2')

    call execute_kt15_atomic_interval(split,p1,t1,'SPLIT-I1',boundary,trace,success,reason)
    call assert_true(success,'split interval 1')
    call encode_kt16_application_checkpoint(split,checkpoint,ok,reason)
    call assert_true(ok,'encode accepted checkpoint')
    call restore_kt16_application_checkpoint(checkpoint,config,restored,ok,reason)
    call assert_true(ok,'restore accepted checkpoint')
    call execute_kt15_atomic_interval(restored,p2,t2,'SPLIT-I2',boundary,trace,success,reason)
    call assert_true(success,'restored interval 2')

    call assert_true(kt15_application_generation(continuous)==2_int64,'continuous gen 2')
    call assert_true(kt15_application_generation(restored)==2_int64,'restored gen 2')
    call kt15_application_time(continuous,ta,ok); call assert_true(ok,'continuous time')
    call kt15_application_time(restored,tb,ok); call assert_true(ok,'restored time')
    call assert_time_equal_exact(ta,tb,'final accepted time')
    call science_concentration(continuous,conc_a)
    call science_concentration(restored,conc_b)
    call assert_true(transfer(conc_a,0_int64)==transfer(conc_b,0_int64),'final science exact split-run')

    call snapshot_kt15_continuation(continuous,cont_a,ok); call assert_true(ok,'continuous continuation')
    call snapshot_kt15_continuation(restored,cont_b,ok); call assert_true(ok,'restored continuation')
    call assert_continuation_equal_exact(cont_a,cont_b)

    call snapshot_kt15_application_config(continuous,ca,ok); call assert_true(ok,'continuous config')
    call snapshot_kt15_application_config(restored,cb,ok); call assert_true(ok,'restored config')
    call assert_true(same_kt15_application_config(ca,cb),'final config exact split-run')
  end subroutine test_split_run_matches_uninterrupted_exactly

  subroutine test_corrupt_checkpoint_rejected()
    type(TimeCoordinate)::t0,t1
    type(hydrology_step_t)::p1
    type(static_boundary_chemistry_t)::boundary
    type(kt15_application_config_t)::config
    type(kt15_application_state_t)::state,restored
    type(kt15_atomic_trace_t)::trace
    type(kt16_application_checkpoint_t)::base,bad
    logical::ok,success
    character(len=128)::reason
    real(real64),parameter::tiny=2.0_real64**(-30)
    character(len=*),parameter::hash='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'

    call make_day(730119_int64,t0)
    call make_day(730120_int64,t1)
    call make_packet(tiny,730120_int64,p1)
    call read_boundary(boundary)
    call make_config(hash,1,config)
    call initialize_application('KT16-CORRUPT',t0,1.0_real64,config,state)
    call execute_kt15_atomic_interval(state,p1,t1,'CORRUPT-I1',boundary,trace,success,reason)
    call assert_true(success,'prepare corrupt checkpoint state')
    call encode_kt16_application_checkpoint(state,base,ok,reason)
    call assert_true(ok,'encode base checkpoint')

    bad=base
    bad%schema_id='BROKEN'
    call validate_kt16_application_checkpoint(bad,ok,reason)
    call assert_true(.not.ok,'schema corruption rejected')

    bad=base
    bad%record_kind='TRIAL'
    call validate_kt16_application_checkpoint(bad,ok,reason)
    call assert_true(.not.ok,'trial-like checkpoint rejected')

    bad=base
    bad%generation=bad%generation+1_int64
    call restore_kt16_application_checkpoint(bad,config,restored,ok,reason)
    call assert_true(.not.ok,'generation corruption rejected')

    bad=base
    bad%lineage_id='OTHER-LINEAGE'
    call restore_kt16_application_checkpoint(bad,config,restored,ok,reason)
    call assert_true(.not.ok,'lineage corruption rejected')

    bad=base
    bad%accepted_time%day_index=bad%accepted_time%day_index+1_int64
    call restore_kt16_application_checkpoint(bad,config,restored,ok,reason)
    call assert_true(.not.ok,'accepted-time corruption rejected')

    bad=base
    bad%layer_count=bad%layer_count+1
    call validate_kt16_application_checkpoint(bad,ok,reason)
    call assert_true(.not.ok,'geometry extent corruption rejected')

    bad=base
    bad%tcd042_concentration=ieee_value(0.0_real64,ieee_quiet_nan)
    call validate_kt16_application_checkpoint(bad,ok,reason)
    call assert_true(.not.ok,'nonfinite science payload rejected')
  end subroutine test_corrupt_checkpoint_rejected

  subroutine test_wrong_expected_config_rejected()
    type(TimeCoordinate)::t0
    type(kt15_application_config_t)::config,wrong
    type(kt15_application_state_t)::state,restored
    type(kt16_application_checkpoint_t)::checkpoint
    logical::ok
    character(len=128)::reason
    character(len=*),parameter::hash='cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc'

    call make_day(730119_int64,t0)
    call make_config(hash,1,config)
    call make_config(hash,2,wrong)
    call initialize_application('KT16-CONFIG',t0,1.0_real64,config,state)
    call encode_kt16_application_checkpoint(state,checkpoint,ok,reason)
    call assert_true(ok,'encode config mismatch fixture')
    call restore_kt16_application_checkpoint(checkpoint,wrong,restored,ok,reason)
    call assert_true(.not.ok,'wrong expected config rejected')
  end subroutine test_wrong_expected_config_rejected

end program test_kt16_accepted_application_checkpoint
