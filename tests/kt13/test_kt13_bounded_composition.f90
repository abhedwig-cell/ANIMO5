program test_kt13_bounded_composition
  use iso_fortran_env, only: int64, real64
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate
  use mod_transient_contracts, only: transient_payload_t
  use mod_transient_transactions, only: accepted_store_t, accepted_store_generation, &
    accepted_store_time, snapshot_accepted_payload
  use mod_animo_hydrology_adapter, only: hydrology_step_t, HYDROLOGY_SCHEMA_ID, &
    HYDROLOGY_UNIT_CONTRACT_ID
  use mod_animo_bounded_no_ponding_upper_hydrology, only: &
    hydroexec01_start_context_t, make_hydroexec01_start_context
  use mod_animo_tcd042_upper_solute_load_resolver, only: &
    tcd042_precip_chemistry_t, tcd042_six_channel_chemistry_t, &
    tcd042_upper_chemistry_forcing_t, make_tcd042_upper_chemistry_forcing
  use mod_animo_tcd042_upper_boundary_client, only: &
    tcd042_top_state_t, initialize_tcd042_store, TCD042_BRANCH_E1_NQ03
  use mod_animo_tcd042_bounded_composition, only: &
    kt13_composition_trace_t, execute_bounded_tcd042_composed_interval
  implicit none

  call test_finite_positive_end_to_end_commit()
  call test_runinu_continuation_is_material()
  call test_kt06_binding_failure_preserves_store()
  call test_tcd042_scope_reject_preserves_store()
  print *, 'PASS_KT13_BOUNDED_TCD042_END_TO_END_COMPOSITION'

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

  subroutine make_packet(prr,ru,endpoint,step)
    real(real64),intent(in)::prr,ru
    real(real64),intent(in)::endpoint
    type(hydrology_step_t),intent(out)::step

    step=hydrology_step_t()
    step%schema_id=HYDROLOGY_SCHEMA_ID
    step%unit_contract_id=HYDROLOGY_UNIT_CONTRACT_ID
    step%layer_count=1
    step%drainage_count=0
    step%producer_endpoint_day=endpoint
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
    step%runoff=ru
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

  subroutine make_start(runinu_entry,start,ok)
    real(real64),intent(in)::runinu_entry
    type(hydroexec01_start_context_t),intent(out)::start
    logical,intent(out)::ok
    character(len=96)::reason
    call make_hydroexec01_start_context(0.0_real64,0.0_real64,0.0_real64, &
      0.5_real64,1.0_real64,0.0_real64,0.0_real64,runinu_entry,start,ok,reason)
  end subroutine make_start

  subroutine make_chemistry(precip_nh,runin_nh,chem,ok)
    real(real64),intent(in)::precip_nh,runin_nh
    type(tcd042_upper_chemistry_forcing_t),intent(out)::chem
    logical,intent(out)::ok
    type(tcd042_precip_chemistry_t)::pr
    type(tcd042_six_channel_chemistry_t)::irr,ron,rin
    character(len=96)::reason

    pr=tcd042_precip_chemistry_t()
    irr=tcd042_six_channel_chemistry_t()
    ron=tcd042_six_channel_chemistry_t()
    rin=tcd042_six_channel_chemistry_t()
    pr%nh=precip_nh
    rin%nh=runin_nh
    call make_tcd042_upper_chemistry_forcing('KT13-CHEM',.false.,pr,irr,ron,rin,chem,ok,reason)
  end subroutine make_chemistry

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
      call assert_true(.false.,'accepted payload is not TCD042 top state')
    end select
  end subroutine accepted_concentration

  subroutine assert_store_origin(store,day,c_expected)
    type(accepted_store_t),intent(in)::store
    integer(int64),intent(in)::day
    real(real64),intent(in)::c_expected
    type(TimeCoordinate)::t
    logical::ok
    real(real64)::c
    call assert_true(accepted_store_generation(store)==0_int64,'generation preserved')
    call accepted_store_time(store,t,ok)
    call assert_true(ok .and. t%day_index==day,'accepted time preserved')
    call accepted_concentration(store,c)
    call assert_true(transfer(c,0_int64)==transfer(c_expected,0_int64),'accepted concentration preserved')
  end subroutine assert_store_origin

  subroutine test_finite_positive_end_to_end_commit()
    type(TimeCoordinate)::t0,t1,t
    type(hydrology_step_t)::packet
    type(hydroexec01_start_context_t)::start
    type(tcd042_upper_chemistry_forcing_t)::chem
    type(accepted_store_t)::store
    type(kt13_composition_trace_t)::trace
    logical::ok,success
    character(len=128)::reason
    real(real64)::c
    real(real64),parameter::tiny=2.0_real64**(-30)

    call make_day(0_int64,t0); call make_day(1_int64,t1)
    call make_packet(tiny,0.0_real64,1.0_real64,packet)
    call make_start(0.0_real64,start,ok); call assert_true(ok,'start context')
    call make_chemistry(2.0_real64,0.0_real64,chem,ok); call assert_true(ok,'chemistry')
    call initialize_tcd042_store(store,'KT13-E1',t0,1.0_real64,ok)
    call assert_true(ok,'initialize KT13 store')

    call execute_bounded_tcd042_composed_interval(store,packet,'ANIMO_TEST_CALENDAR',0_int64, &
      t0,t1,'KT13-E1-EXEC',start,chem,1,1.0_real64,trace,success,reason)

    call assert_true(success,'finite-positive end-to-end commit')
    call assert_true(trace%kt06_binding_passed,'KT06 binding passed')
    call assert_true(trace%hydroexec_passed,'HYDROEXEC01 passed')
    call assert_true(trace%load_resolution_passed,'UBFORCE02 passed')
    call assert_true(trace%science_runtime_committed,'KT12/KT02 committed')
    call assert_true(trace%tcd042_branch==TCD042_BRANCH_E1_NQ03,'E1 branch selected')
    call assert_true(transfer(trace%flib_top,0_int64)==int(z'3E10000000000000',int64),'Flib exact tiny')
    call assert_true(transfer(trace%selected_load_rate,0_int64)==int(z'3E20000000000000',int64),'load exact 2*tiny')
    call assert_true(trace%commit_count==1,'one atomic commit')
    call assert_true(accepted_store_generation(store)==1_int64,'accepted generation one')
    call accepted_store_time(store,t,ok)
    call assert_true(ok .and. t%day_index==1_int64,'accepted endpoint')
    call accepted_concentration(store,c)
    call assert_true(c>1.0_real64,'finite-positive composition changes state')
  end subroutine test_finite_positive_end_to_end_commit

  subroutine test_runinu_continuation_is_material()
    type(TimeCoordinate)::t0,t1
    type(hydrology_step_t)::packet
    type(hydroexec01_start_context_t)::start
    type(tcd042_upper_chemistry_forcing_t)::chem
    type(accepted_store_t)::store
    type(kt13_composition_trace_t)::trace
    logical::ok,success
    character(len=128)::reason
    real(real64),parameter::tiny=2.0_real64**(-30)

    call make_day(10_int64,t0); call make_day(11_int64,t1)
    call make_packet(0.0_real64,0.0_real64,11.0_real64,packet)
    call make_start(tiny,start,ok); call assert_true(ok,'Runinu continuation start')
    call make_chemistry(0.0_real64,2.0_real64,chem,ok); call assert_true(ok,'runin chemistry')
    call initialize_tcd042_store(store,'KT13-RUNINU',t0,1.0_real64,ok)
    call assert_true(ok,'initialize Runinu store')

    call execute_bounded_tcd042_composed_interval(store,packet,'ANIMO_TEST_CALENDAR',0_int64, &
      t0,t1,'KT13-RUNINU-EXEC',start,chem,1,1.0_real64,trace,success,reason)

    call assert_true(success,'Runinu continuation composition commit')
    call assert_true(transfer(trace%runinu,0_int64)==int(z'3E10000000000000',int64), &
      'Runinu continuation preserved exactly')
    call assert_true(transfer(trace%flib_top,0_int64)==int(z'3E10000000000000',int64), &
      'Runinu affects resolved upper hydrology')
    call assert_true(transfer(trace%selected_load_rate,0_int64)==int(z'3E20000000000000',int64), &
      'Runinu affects upper solute load')
  end subroutine test_runinu_continuation_is_material

  subroutine test_kt06_binding_failure_preserves_store()
    type(TimeCoordinate)::t0,t1
    type(hydrology_step_t)::packet
    type(hydroexec01_start_context_t)::start
    type(tcd042_upper_chemistry_forcing_t)::chem
    type(accepted_store_t)::store
    type(kt13_composition_trace_t)::trace
    logical::ok,success
    character(len=128)::reason

    call make_day(20_int64,t0); call make_day(21_int64,t1)
    call make_packet(0.0_real64,0.0_real64,22.0_real64,packet)
    call make_start(0.0_real64,start,ok); call assert_true(ok,'binding-fail start')
    call make_chemistry(0.0_real64,0.0_real64,chem,ok); call assert_true(ok,'binding-fail chemistry')
    call initialize_tcd042_store(store,'KT13-BINDFAIL',t0,3.0_real64,ok)
    call assert_true(ok,'binding-fail store')

    call execute_bounded_tcd042_composed_interval(store,packet,'ANIMO_TEST_CALENDAR',0_int64, &
      t0,t1,'KT13-BINDFAIL-EXEC',start,chem,1,1.0_real64,trace,success,reason)

    call assert_true(.not.success,'KT06 binding mismatch rejects')
    call assert_true(.not.trace%kt06_binding_passed,'binding trace remains false')
    call assert_store_origin(store,20_int64,3.0_real64)
  end subroutine test_kt06_binding_failure_preserves_store

  subroutine test_tcd042_scope_reject_preserves_store()
    type(TimeCoordinate)::t0,t1
    type(hydrology_step_t)::packet
    type(hydroexec01_start_context_t)::start
    type(tcd042_upper_chemistry_forcing_t)::chem
    type(accepted_store_t)::store
    type(kt13_composition_trace_t)::trace
    logical::ok,success
    character(len=128)::reason
    real(real64),parameter::too_large=2.0_real64**(-26)

    call make_day(30_int64,t0); call make_day(31_int64,t1)
    call make_packet(too_large,0.0_real64,31.0_real64,packet)
    call make_start(0.0_real64,start,ok); call assert_true(ok,'scope-fail start')
    call make_chemistry(0.0_real64,0.0_real64,chem,ok); call assert_true(ok,'scope-fail chemistry')
    call initialize_tcd042_store(store,'KT13-SCOPEFAIL',t0,4.0_real64,ok)
    call assert_true(ok,'scope-fail store')

    call execute_bounded_tcd042_composed_interval(store,packet,'ANIMO_TEST_CALENDAR',0_int64, &
      t0,t1,'KT13-SCOPEFAIL-EXEC',start,chem,1,1.0_real64,trace,success,reason)

    call assert_true(.not.success,'TCD042 out-of-scope flux rejects')
    call assert_true(trace%kt06_binding_passed,'binding still passed')
    call assert_true(trace%hydroexec_passed,'hydrology still resolved')
    call assert_true(trace%load_resolution_passed,'load resolution still passed')
    call assert_true(.not.trace%science_runtime_committed,'science did not commit')
    call assert_store_origin(store,30_int64,4.0_real64)
  end subroutine test_tcd042_scope_reject_preserves_store

end program test_kt13_bounded_composition
