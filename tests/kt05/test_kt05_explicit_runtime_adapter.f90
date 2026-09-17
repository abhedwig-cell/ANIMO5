program test_kt05_explicit_runtime_adapter
  use iso_fortran_env, only: int64, real64
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate, time_equal
  use mod_transient_contracts, only: transient_payload_t
  use mod_transient_transactions, only: accepted_store_t, &
    accepted_store_generation, accepted_store_time, snapshot_accepted_payload
  use mod_transient_interval_runtime, only: attempt_request_t, &
    runtime_trace_t, run_interval
  use mod_animo_explicit_hydrology_runtime_adapter, only: &
    BINDING_CONTRACT_ID, SOURCE_SCHEMA_ID, SOURCE_UNIT_ID, &
    SOURCE_AUTHORITY_ID, animo_runtime_probe_state_t, &
    animo_explicit_hydrology_client_t, initialize_probe_store
  implicit none

  character(len=*), parameter :: RUNTIME_CALENDAR_ID = 'ANIMO_LWKM_DAILY_V1'
  type(TimeCoordinate) :: t0, t5, t10, t10half
  logical :: ok

  call make_time_coordinate( &
    RUNTIME_CALENDAR_ID, 0_int64, 0_int64, 1_int64, t0, ok)
  call assert_true(ok, 't0 construction')
  call make_time_coordinate( &
    RUNTIME_CALENDAR_ID, 5_int64, 0_int64, 1_int64, t5, ok)
  call assert_true(ok, 't5 construction')
  call make_time_coordinate( &
    RUNTIME_CALENDAR_ID, 10_int64, 0_int64, 1_int64, t10, ok)
  call assert_true(ok, 't10 construction')
  call make_time_coordinate( &
    RUNTIME_CALENDAR_ID, 10_int64, 1_int64, 2_int64, t10half, ok)
  call assert_true(ok, 't10half construction')

  call test_real_fixture_binding_commits(t0, t10)
  call test_endpoint_mismatch_fails_closed(t0, t10)
  call test_missing_explicit_state_fails_closed(t0, t10)
  call test_fractional_producer_metadata_fails_closed(t0, t10)
  call test_calendar_binding_fails_closed(t0, t10)
  call test_unpinned_source_contract_fails_closed(t0, t10)
  call test_subday_runtime_mapping_fails_closed(t0, t10half)
  call test_single_forcing_cannot_publish_partial_multistep(t0, t5, t10)

  print *, 'KT05 explicit-state runtime adapter tests: PASS'

contains

  subroutine assert_true(condition, label)
    logical, intent(in) :: condition
    character(len=*), intent(in) :: label
    if (.not. condition) then
      print *, 'ASSERTION FAILED: ', trim(label)
      error stop 1
    end if
  end subroutine assert_true

  subroutine configure_lwkm_first_interval(client)
    type(animo_explicit_hydrology_client_t), intent(out) :: client

    client%forcing_present = .true.
    client%runtime_calendar_contract_id = RUNTIME_CALENDAR_ID
    client%producer_day_offset = 0_int64
    client%forcing%binding_contract_id = BINDING_CONTRACT_ID
    client%forcing%source_schema_id = SOURCE_SCHEMA_ID
    client%forcing%source_unit_contract_id = SOURCE_UNIT_ID
    client%forcing%source_authority_id = SOURCE_AUTHORITY_ID

    ! Derived from the first dynamic interval of the pinned LWKM Hlpimp=11
    ! SWATRE.UNF envelope: producer endpoint=10 d, step=10 d, explicit Sict=0.
    client%forcing%producer_endpoint_day = 10.0_real64
    client%forcing%producer_step_days = 10.0_real64
    client%forcing%has_interception_storage_end = .true.
    client%forcing%interception_storage_end = 0.0_real64
  end subroutine configure_lwkm_first_interval

  subroutine assert_store_time(store, expected, label)
    type(accepted_store_t), intent(in) :: store
    type(TimeCoordinate), intent(in) :: expected
    character(len=*), intent(in) :: label
    type(TimeCoordinate) :: actual
    logical :: ok, equal, compare_ok

    call accepted_store_time(store, actual, ok)
    call assert_true(ok, trim(label)//' available')
    call time_equal(actual, expected, equal, compare_ok)
    call assert_true(compare_ok .and. equal, label)
  end subroutine assert_store_time

  subroutine assert_state_token(store, expected, label)
    type(accepted_store_t), intent(in) :: store
    integer(int64), intent(in) :: expected
    character(len=*), intent(in) :: label
    class(transient_payload_t), allocatable :: payload
    logical :: ok

    call snapshot_accepted_payload(store, payload, ok)
    call assert_true(ok, trim(label)//' snapshot')
    select type (typed => payload)
    type is (animo_runtime_probe_state_t)
      call assert_true(typed%state_token == expected, label)
    class default
      call assert_true(.false., trim(label)//' payload type')
    end select
  end subroutine assert_state_token

  subroutine run_one(store, client, target, success, reason)
    type(accepted_store_t), intent(inout) :: store
    type(animo_explicit_hydrology_client_t), intent(inout) :: client
    type(TimeCoordinate), intent(in) :: target
    logical, intent(out) :: success
    character(len=*), intent(out) :: reason
    type(attempt_request_t) :: requests(1)
    type(runtime_trace_t) :: trace

    requests(1)%endpoint_time = target
    requests(1)%retry_permitted_after_reject = .false.
    call run_interval(store, client, target, requests, 1, trace, success, reason)
  end subroutine run_one

  subroutine test_real_fixture_binding_commits(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(accepted_store_t) :: store
    type(animo_explicit_hydrology_client_t) :: client
    logical :: ok, success
    character(len=64) :: reason

    call initialize_probe_store( &
      store, 'ANIMO_KT05_LWKM_FIRST', t_start, 7_int64, ok)
    call assert_true(ok, 'LWKM store initialize')
    call configure_lwkm_first_interval(client)
    call run_one(store, client, t_end, success, reason)

    call assert_true(success, 'LWKM interval success')
    call assert_true( &
      trim(reason) == 'INTERVAL_COMMITTED', 'LWKM interval reason')
    call assert_true( &
      accepted_store_generation(store) == 1_int64, 'LWKM generation')
    call assert_store_time(store, t_end, 'LWKM exact runtime target')
    call assert_state_token(store, 7_int64, 'forcing not accepted state')
  end subroutine test_real_fixture_binding_commits

  subroutine test_endpoint_mismatch_fails_closed(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(accepted_store_t) :: store
    type(animo_explicit_hydrology_client_t) :: client
    logical :: ok, success
    character(len=64) :: reason

    call initialize_probe_store( &
      store, 'ANIMO_KT05_ENDPOINT', t_start, 11_int64, ok)
    call assert_true(ok, 'endpoint store initialize')
    call configure_lwkm_first_interval(client)
    client%forcing%producer_endpoint_day = 11.0_real64
    call run_one(store, client, t_end, success, reason)

    call assert_true(.not. success, 'endpoint mismatch rejected')
    call assert_true( &
      trim(reason) == 'CLIENT_ATTEMPT_FAILED', 'endpoint runtime reason')
    call assert_true( &
      accepted_store_generation(store) == 0_int64, &
      'endpoint generation unchanged')
    call assert_store_time(store, t_start, 'endpoint time unchanged')
    call assert_state_token(store, 11_int64, 'endpoint payload unchanged')
  end subroutine test_endpoint_mismatch_fails_closed

  subroutine test_missing_explicit_state_fails_closed(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(accepted_store_t) :: store
    type(animo_explicit_hydrology_client_t) :: client
    logical :: ok, success
    character(len=64) :: reason

    call initialize_probe_store( &
      store, 'ANIMO_KT05_SICT', t_start, 13_int64, ok)
    call assert_true(ok, 'Sict store initialize')
    call configure_lwkm_first_interval(client)
    client%forcing%has_interception_storage_end = .false.
    call run_one(store, client, t_end, success, reason)

    call assert_true(.not. success, 'missing explicit state rejected')
    call assert_true( &
      accepted_store_generation(store) == 0_int64, &
      'Sict generation unchanged')
    call assert_store_time(store, t_start, 'Sict time unchanged')
  end subroutine test_missing_explicit_state_fails_closed

  subroutine test_fractional_producer_metadata_fails_closed(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(accepted_store_t) :: store
    type(animo_explicit_hydrology_client_t) :: client
    logical :: ok, success
    character(len=64) :: reason

    call initialize_probe_store( &
      store, 'ANIMO_KT05_META', t_start, 17_int64, ok)
    call assert_true(ok, 'metadata store initialize')
    call configure_lwkm_first_interval(client)
    client%forcing%producer_endpoint_day = 10.5_real64
    call run_one(store, client, t_end, success, reason)

    call assert_true(.not. success, 'fractional metadata rejected')
    call assert_true( &
      accepted_store_generation(store) == 0_int64, &
      'metadata generation unchanged')
    call assert_store_time(store, t_start, 'metadata time unchanged')
  end subroutine test_fractional_producer_metadata_fails_closed

  subroutine test_calendar_binding_fails_closed(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(accepted_store_t) :: store
    type(animo_explicit_hydrology_client_t) :: client
    logical :: ok, success
    character(len=64) :: reason

    call initialize_probe_store( &
      store, 'ANIMO_KT05_CAL', t_start, 23_int64, ok)
    call assert_true(ok, 'calendar store initialize')
    call configure_lwkm_first_interval(client)
    client%runtime_calendar_contract_id = 'UNQUALIFIED_CALENDAR'
    call run_one(store, client, t_end, success, reason)

    call assert_true(.not. success, 'calendar mismatch rejected')
    call assert_true( &
      accepted_store_generation(store) == 0_int64, &
      'calendar generation unchanged')
    call assert_store_time(store, t_start, 'calendar time unchanged')
  end subroutine test_calendar_binding_fails_closed

  subroutine test_unpinned_source_contract_fails_closed(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(accepted_store_t) :: store
    type(animo_explicit_hydrology_client_t) :: client
    logical :: ok, success
    character(len=64) :: reason

    call initialize_probe_store( &
      store, 'ANIMO_KT05_SOURCE', t_start, 29_int64, ok)
    call assert_true(ok, 'source store initialize')
    call configure_lwkm_first_interval(client)
    client%forcing%source_authority_id = 'UNPINNED_SOURCE'
    call run_one(store, client, t_end, success, reason)

    call assert_true(.not. success, 'unpinned source rejected')
    call assert_true( &
      accepted_store_generation(store) == 0_int64, &
      'source generation unchanged')
    call assert_store_time(store, t_start, 'source time unchanged')
  end subroutine test_unpinned_source_contract_fails_closed

  subroutine test_subday_runtime_mapping_fails_closed(t_start, target)
    type(TimeCoordinate), intent(in) :: t_start, target
    type(accepted_store_t) :: store
    type(animo_explicit_hydrology_client_t) :: client
    logical :: ok, success
    character(len=64) :: reason

    call initialize_probe_store( &
      store, 'ANIMO_KT05_SUBDAY', t_start, 19_int64, ok)
    call assert_true(ok, 'subday store initialize')
    call configure_lwkm_first_interval(client)
    call run_one(store, client, target, success, reason)

    call assert_true(.not. success, 'subday mapping rejected')
    call assert_true( &
      accepted_store_generation(store) == 0_int64, &
      'subday generation unchanged')
    call assert_store_time(store, t_start, 'subday time unchanged')
  end subroutine test_subday_runtime_mapping_fails_closed

  subroutine test_single_forcing_cannot_publish_partial_multistep( &
      t_start, t_middle, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_middle, t_end
    type(accepted_store_t) :: store
    type(animo_explicit_hydrology_client_t) :: client
    type(attempt_request_t) :: requests(2)
    type(runtime_trace_t) :: trace
    logical :: ok, success
    character(len=64) :: reason

    call initialize_probe_store( &
      store, 'ANIMO_KT05_ATOMIC', t_start, 31_int64, ok)
    call assert_true(ok, 'atomic store initialize')
    call configure_lwkm_first_interval(client)

    ! Recast the single forcing as a valid 0->5 packet. Reusing it for the
    ! second 5->10 request must fail on endpoint identity. The first working
    ! commit must never publish externally because the full interval failed.
    client%forcing%producer_endpoint_day = 5.0_real64
    client%forcing%producer_step_days = 5.0_real64
    requests(1)%endpoint_time = t_middle
    requests(2)%endpoint_time = t_end
    requests(1)%retry_permitted_after_reject = .false.
    requests(2)%retry_permitted_after_reject = .false.

    call run_interval( &
      store, client, t_end, requests, 2, trace, success, reason)

    call assert_true(.not. success, 'partial multistep interval rejected')
    call assert_true(trace%commit_count == 1, 'working first step committed')
    call assert_true( &
      accepted_store_generation(store) == 0_int64, &
      'partial multistep external generation unchanged')
    call assert_store_time(store, t_start, 'partial multistep time unchanged')
    call assert_state_token(store, 31_int64, 'partial payload unchanged')
  end subroutine test_single_forcing_cannot_publish_partial_multistep

end program test_kt05_explicit_runtime_adapter
