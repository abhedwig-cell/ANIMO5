program test_kt11_multi_packet_hydrology_provider
  use iso_fortran_env, only: int64, real64
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate, time_equal
  use mod_transient_contracts, only: transient_payload_t, admissibility_t
  use mod_transient_transactions, only: accepted_store_t, &
    accepted_store_generation, accepted_store_time, snapshot_accepted_payload
  use mod_transient_interval_runtime, only: attempt_request_t, runtime_trace_t, run_interval
  use mod_animo_hydrology_adapter, only: hydrology_step_t, &
    HYDROLOGY_SCHEMA_ID, HYDROLOGY_UNIT_CONTRACT_ID
  use mod_animo_explicit_hydrology_runtime_binding, only: &
    animo_runtime_probe_state_t, initialize_probe_store
  use mod_animo_multi_packet_hydrology_provider, only: &
    animo_multi_packet_hydrology_runtime_probe_client_t, &
    initialize_multi_packet_client, multi_packet_client_ready, multi_packet_packet_count
  use mod_kt09_real_lwkm_anchors, only: KT09_ANCHOR_COUNT, KT09_ENDPOINT, &
    KT09_DURATION, make_kt09_anchor_step
  implicit none

  character(len=*), parameter :: CALENDAR_ID = 'ANIMO_LWKM_DAILY_V1'

  call test_three_packet_interval_commits()
  call test_out_of_order_storage_is_key_selected()
  call test_missing_middle_packet_fails_atomic()
  call test_duplicate_key_rejected()
  call test_same_endpoint_different_steps_are_distinct_keys()
  call test_fractional_key_rejected()
  call test_nonzero_offset_multistep()
  call test_repeat_selection_is_stateless()
  call test_provider_owns_deep_copy()
  call test_real_lwkm_anchor_packets_bind()
  call test_missing_real_interval_fails_closed()

  print '(A)', 'KT11 multi-packet hydrology provider tests: PASS'

contains

  subroutine assert_true(condition, label)
    logical, intent(in) :: condition
    character(len=*), intent(in) :: label
    if (.not. condition) then
      write (*, '(A)') 'ASSERTION FAILED: '//trim(label)
      error stop 1
    end if
  end subroutine assert_true

  subroutine make_time(day, value)
    integer(int64), intent(in) :: day
    type(TimeCoordinate), intent(out) :: value
    logical :: ok
    call make_time_coordinate(CALENDAR_ID, day, 0_int64, 1_int64, value, ok)
    call assert_true(ok, 'time construction')
  end subroutine make_time

  subroutine make_step(step, endpoint_day, step_days, marker)
    type(hydrology_step_t), intent(out) :: step
    real(real64), intent(in) :: endpoint_day, step_days, marker

    step%schema_id = HYDROLOGY_SCHEMA_ID
    step%unit_contract_id = HYDROLOGY_UNIT_CONTRACT_ID
    step%layer_count = 2
    step%drainage_count = 1
    step%producer_endpoint_day = endpoint_day
    step%producer_step_days = step_days
    step%prr = marker
    step%has_interception_storage_end = .true.
    step%interception_storage_end = marker / 1000000.0_real64
    step%has_soil_temperature = .false.
    allocate(step%sc(2), step%mofrt(2), step%flev(2), step%flab(3))
    allocate(step%fldr(1,2), step%soil_temperature(0))
    step%sc = marker
    step%mofrt = marker
    step%flev = marker
    step%flab = marker
    step%fldr = marker
  end subroutine make_step

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

  subroutine assert_store_token(store, expected, label)
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
      call assert_true(.false., trim(label)//' type')
    end select
  end subroutine assert_store_token

  subroutine run_three(store, client, t10, t20, t30, success, reason, trace)
    type(accepted_store_t), intent(inout) :: store
    type(animo_multi_packet_hydrology_runtime_probe_client_t), intent(inout) :: client
    type(TimeCoordinate), intent(in) :: t10, t20, t30
    logical, intent(out) :: success
    character(len=*), intent(out) :: reason
    type(runtime_trace_t), intent(out) :: trace
    type(attempt_request_t) :: requests(3)

    requests(1)%endpoint_time = t10
    requests(2)%endpoint_time = t20
    requests(3)%endpoint_time = t30
    call run_interval(store, client, t30, requests, 3, trace, success, reason)
  end subroutine run_three

  subroutine test_three_packet_interval_commits()
    type(hydrology_step_t) :: packets(3)
    type(animo_multi_packet_hydrology_runtime_probe_client_t) :: client
    type(accepted_store_t) :: store
    type(TimeCoordinate) :: t0, t10, t20, t30
    type(runtime_trace_t) :: trace
    logical :: ok, success
    character(len=128) :: reason

    call make_step(packets(1), 10.0_real64, 10.0_real64, 1.0_real64)
    call make_step(packets(2), 20.0_real64, 10.0_real64, 2.0_real64)
    call make_step(packets(3), 30.0_real64, 10.0_real64, 3.0_real64)
    call initialize_multi_packet_client(client, packets, CALENDAR_ID, 0_int64, ok, reason)
    call assert_true(ok, 'three packet provider init')
    call assert_true(multi_packet_client_ready(client), 'three packet provider ready')
    call assert_true(multi_packet_packet_count(client) == 3, 'three packet count')

    call make_time(0_int64, t0)
    call make_time(10_int64, t10)
    call make_time(20_int64, t20)
    call make_time(30_int64, t30)
    call initialize_probe_store(store, 'KT11_THREE', t0, 77_int64, ok)
    call assert_true(ok, 'three store init')

    call run_three(store, client, t10, t20, t30, success, reason, trace)
    call assert_true(success, 'three packet interval succeeds')
    call assert_true(trim(reason) == 'INTERVAL_COMMITTED', 'three packet interval reason')
    call assert_true(trace%attempt_count == 3, 'three packet attempts')
    call assert_true(trace%commit_count == 3, 'three private commits')
    call assert_true(accepted_store_generation(store) == 3_int64, 'three external generation')
    call assert_store_time(store, t30, 'three external target')
    call assert_store_token(store, 77_int64, 'forcing excluded from accepted state')
  end subroutine test_three_packet_interval_commits

  subroutine test_out_of_order_storage_is_key_selected()
    type(hydrology_step_t) :: packets(3)
    type(animo_multi_packet_hydrology_runtime_probe_client_t) :: client
    type(accepted_store_t) :: store
    type(TimeCoordinate) :: t0, t10, t20, t30
    type(runtime_trace_t) :: trace
    logical :: ok, success
    character(len=128) :: reason

    call make_step(packets(1), 30.0_real64, 10.0_real64, 3.0_real64)
    call make_step(packets(2), 10.0_real64, 10.0_real64, 1.0_real64)
    call make_step(packets(3), 20.0_real64, 10.0_real64, 2.0_real64)
    call initialize_multi_packet_client(client, packets, CALENDAR_ID, 0_int64, ok, reason)
    call assert_true(ok, 'unordered provider init')

    call make_time(0_int64, t0)
    call make_time(10_int64, t10)
    call make_time(20_int64, t20)
    call make_time(30_int64, t30)
    call initialize_probe_store(store, 'KT11_UNORDERED', t0, 81_int64, ok)
    call assert_true(ok, 'unordered store init')
    call run_three(store, client, t10, t20, t30, success, reason, trace)
    call assert_true(success, 'unordered storage succeeds')
    call assert_true(trace%commit_count == 3, 'unordered three commits')
    call assert_store_time(store, t30, 'unordered target')
  end subroutine test_out_of_order_storage_is_key_selected

  subroutine test_missing_middle_packet_fails_atomic()
    type(hydrology_step_t) :: packets(2)
    type(animo_multi_packet_hydrology_runtime_probe_client_t) :: client
    type(accepted_store_t) :: store
    type(TimeCoordinate) :: t0, t10, t20, t30
    type(runtime_trace_t) :: trace
    logical :: ok, success
    character(len=128) :: reason

    call make_step(packets(1), 10.0_real64, 10.0_real64, 1.0_real64)
    call make_step(packets(2), 30.0_real64, 10.0_real64, 3.0_real64)
    call initialize_multi_packet_client(client, packets, CALENDAR_ID, 0_int64, ok, reason)
    call assert_true(ok, 'missing provider init')

    call make_time(0_int64, t0)
    call make_time(10_int64, t10)
    call make_time(20_int64, t20)
    call make_time(30_int64, t30)
    call initialize_probe_store(store, 'KT11_MISSING', t0, 83_int64, ok)
    call assert_true(ok, 'missing store init')
    call run_three(store, client, t10, t20, t30, success, reason, trace)

    call assert_true(.not. success, 'missing packet fails')
    call assert_true(trim(reason) == 'CLIENT_ATTEMPT_FAILED', 'missing packet runtime reason')
    call assert_true(trace%attempt_count == 2, 'missing packet attempts')
    call assert_true(trace%commit_count == 1, 'first private commit before missing packet')
    call assert_true(accepted_store_generation(store) == 0_int64, 'missing external generation atomic')
    call assert_store_time(store, t0, 'missing external time atomic')
    call assert_store_token(store, 83_int64, 'missing external payload atomic')
  end subroutine test_missing_middle_packet_fails_atomic

  subroutine test_duplicate_key_rejected()
    type(hydrology_step_t) :: packets(2)
    type(animo_multi_packet_hydrology_runtime_probe_client_t) :: client
    logical :: ok
    character(len=128) :: reason

    call make_step(packets(1), 10.0_real64, 10.0_real64, 1.0_real64)
    call make_step(packets(2), 10.0_real64, 10.0_real64, 2.0_real64)
    call initialize_multi_packet_client(client, packets, CALENDAR_ID, 0_int64, ok, reason)
    call assert_true(.not. ok, 'duplicate rejected')
    call assert_true(trim(reason) == 'DUPLICATE_PRODUCER_INTERVAL_KEY', 'duplicate reason')
    call assert_true(.not. multi_packet_client_ready(client), 'duplicate provider not ready')
    call assert_true(multi_packet_packet_count(client) == 0, 'invalid provider count is zero')
  end subroutine test_duplicate_key_rejected

  subroutine test_same_endpoint_different_steps_are_distinct_keys()
    type(hydrology_step_t) :: packets(2)
    type(animo_multi_packet_hydrology_runtime_probe_client_t) :: client
    type(accepted_store_t) :: store
    type(TimeCoordinate) :: t0, t10, t20
    type(attempt_request_t) :: request(1)
    type(runtime_trace_t) :: trace
    logical :: ok, success
    character(len=128) :: reason

    call make_step(packets(1), 20.0_real64, 20.0_real64, 1.0_real64)
    call make_step(packets(2), 20.0_real64, 10.0_real64, 2.0_real64)
    call initialize_multi_packet_client(client, packets, CALENDAR_ID, 0_int64, ok, reason)
    call assert_true(ok, 'same endpoint distinct-step provider init')
    call assert_true(multi_packet_packet_count(client) == 2, 'same endpoint distinct-step count')

    call make_time(0_int64, t0)
    call make_time(10_int64, t10)
    call make_time(20_int64, t20)

    call initialize_probe_store(store, 'KT11_PAIR20', t0, 111_int64, ok)
    call assert_true(ok, 'pair step20 store init')
    request(1)%endpoint_time = t20
    call run_interval(store, client, t20, request, 1, trace, success, reason)
    call assert_true(success, 'endpoint20 step20 selects exact pair')
    call assert_store_token(store, 111_int64, 'pair step20 token')

    call initialize_probe_store(store, 'KT11_PAIR10', t10, 113_int64, ok)
    call assert_true(ok, 'pair step10 store init')
    request(1)%endpoint_time = t20
    call run_interval(store, client, t20, request, 1, trace, success, reason)
    call assert_true(success, 'endpoint20 step10 selects exact pair')
    call assert_store_token(store, 113_int64, 'pair step10 token')
  end subroutine test_same_endpoint_different_steps_are_distinct_keys

  subroutine test_fractional_key_rejected()
    type(hydrology_step_t) :: packets(1)
    type(animo_multi_packet_hydrology_runtime_probe_client_t) :: client
    logical :: ok
    character(len=128) :: reason

    call make_step(packets(1), 10.5_real64, 10.0_real64, 1.0_real64)
    call initialize_multi_packet_client(client, packets, CALENDAR_ID, 0_int64, ok, reason)
    call assert_true(.not. ok, 'fractional key rejected')
    call assert_true(trim(reason) == 'NONEXACT_PACKET_TIME_METADATA', 'fractional key reason')
  end subroutine test_fractional_key_rejected

  subroutine test_nonzero_offset_multistep()
    type(hydrology_step_t) :: packets(2)
    type(animo_multi_packet_hydrology_runtime_probe_client_t) :: client
    type(accepted_store_t) :: store
    type(TimeCoordinate) :: t0, t10, t20
    type(attempt_request_t) :: requests(2)
    type(runtime_trace_t) :: trace
    logical :: ok, success
    character(len=128) :: reason

    call make_step(packets(1), 1010.0_real64, 10.0_real64, 1.0_real64)
    call make_step(packets(2), 1020.0_real64, 10.0_real64, 2.0_real64)
    call initialize_multi_packet_client(client, packets, CALENDAR_ID, 1000_int64, ok, reason)
    call assert_true(ok, 'offset provider init')

    call make_time(0_int64, t0)
    call make_time(10_int64, t10)
    call make_time(20_int64, t20)
    call initialize_probe_store(store, 'KT11_OFFSET', t0, 89_int64, ok)
    call assert_true(ok, 'offset store init')
    requests(1)%endpoint_time = t10
    requests(2)%endpoint_time = t20
    call run_interval(store, client, t20, requests, 2, trace, success, reason)
    call assert_true(success, 'offset multistep succeeds')
    call assert_true(trace%commit_count == 2, 'offset commits')
    call assert_store_time(store, t20, 'offset target')
  end subroutine test_nonzero_offset_multistep

  subroutine test_repeat_selection_is_stateless()
    type(hydrology_step_t) :: packets(1)
    type(animo_multi_packet_hydrology_runtime_probe_client_t) :: client
    type(accepted_store_t) :: store
    type(TimeCoordinate) :: t0, t10
    class(transient_payload_t), allocatable :: origin, candidate
    type(admissibility_t) :: admissibility
    logical :: ok
    character(len=128) :: reason

    call make_step(packets(1), 10.0_real64, 10.0_real64, 1.0_real64)
    call initialize_multi_packet_client(client, packets, CALENDAR_ID, 0_int64, ok, reason)
    call assert_true(ok, 'repeat provider init')
    call make_time(0_int64, t0)
    call make_time(10_int64, t10)
    call initialize_probe_store(store, 'KT11_REPEAT', t0, 97_int64, ok)
    call assert_true(ok, 'repeat store init')
    call snapshot_accepted_payload(store, origin, ok)
    call assert_true(ok, 'repeat origin snapshot')

    call client%execute_attempt(origin, t0, t10, candidate, admissibility, ok, reason)
    call assert_true(ok .and. admissibility%admissible, 'repeat first selection')
    call assert_candidate_token(candidate, 97_int64, 'repeat first token')

    call client%execute_attempt(origin, t0, t10, candidate, admissibility, ok, reason)
    call assert_true(ok .and. admissibility%admissible, 'repeat second selection')
    call assert_candidate_token(candidate, 97_int64, 'repeat second token')
  end subroutine test_repeat_selection_is_stateless


  subroutine test_provider_owns_deep_copy()
    type(hydrology_step_t) :: packets(1)
    type(animo_multi_packet_hydrology_runtime_probe_client_t) :: client
    type(accepted_store_t) :: store
    type(TimeCoordinate) :: t0, t10
    type(attempt_request_t) :: request(1)
    type(runtime_trace_t) :: trace
    logical :: ok, success
    character(len=128) :: reason

    call make_step(packets(1), 10.0_real64, 10.0_real64, 1.0_real64)
    call initialize_multi_packet_client(client, packets, CALENDAR_ID, 0_int64, ok, reason)
    call assert_true(ok, 'deep-copy provider init')

    ! Mutate the caller-owned source after initialization. Provider behaviour
    ! must remain governed by its internal immutable copy.
    packets(1)%schema_id = 'CALLER_MUTATED'
    packets(1)%producer_endpoint_day = 999.0_real64
    packets(1)%producer_step_days = 999.0_real64
    packets(1)%prr = 999.0_real64
    packets(1)%sc = 999.0_real64

    call make_time(0_int64, t0)
    call make_time(10_int64, t10)
    call initialize_probe_store(store, 'KT11_DEEPCOPY', t0, 101_int64, ok)
    call assert_true(ok, 'deep-copy store init')
    request(1)%endpoint_time = t10
    call run_interval(store, client, t10, request, 1, trace, success, reason)

    call assert_true(success, 'deep-copy provider unaffected by caller mutation')
    call assert_true(trace%commit_count == 1, 'deep-copy commit')
    call assert_store_time(store, t10, 'deep-copy target')
    call assert_store_token(store, 101_int64, 'deep-copy accepted payload unchanged')
  end subroutine test_provider_owns_deep_copy

  subroutine assert_candidate_token(candidate, expected, label)
    class(transient_payload_t), allocatable, intent(in) :: candidate
    integer(int64), intent(in) :: expected
    character(len=*), intent(in) :: label
    call assert_true(allocated(candidate), trim(label)//' allocated')
    select type (typed => candidate)
    type is (animo_runtime_probe_state_t)
      call assert_true(typed%state_token == expected, label)
    class default
      call assert_true(.false., trim(label)//' type')
    end select
  end subroutine assert_candidate_token

  subroutine test_real_lwkm_anchor_packets_bind()
    type(hydrology_step_t) :: packets(KT09_ANCHOR_COUNT)
    type(animo_multi_packet_hydrology_runtime_probe_client_t) :: client
    type(accepted_store_t) :: store
    type(TimeCoordinate) :: origin_time, endpoint_time
    type(attempt_request_t) :: request(1)
    type(runtime_trace_t) :: trace
    integer :: i
    integer(int64) :: origin_day, endpoint_day
    logical :: ok, success
    character(len=128) :: reason

    do i = 1, KT09_ANCHOR_COUNT
      call make_kt09_anchor_step(i, packets(i))
    end do
    call initialize_multi_packet_client(client, packets, CALENDAR_ID, 0_int64, ok, reason)
    call assert_true(ok, 'real anchor provider init')
    call assert_true(multi_packet_packet_count(client) == KT09_ANCHOR_COUNT, 'real anchor count')

    do i = 1, KT09_ANCHOR_COUNT
      endpoint_day = nint(KT09_ENDPOINT(i), kind=int64)
      origin_day = endpoint_day - nint(KT09_DURATION(i), kind=int64)
      call make_time(origin_day, origin_time)
      call make_time(endpoint_day, endpoint_time)
      call initialize_probe_store(store, 'KT11_REAL', origin_time, int(i,int64), ok)
      call assert_true(ok, 'real anchor store init')
      request(1)%endpoint_time = endpoint_time
      call run_interval(store, client, endpoint_time, request, 1, trace, success, reason)
      call assert_true(success, 'real anchor runtime bind')
      call assert_true(trace%commit_count == 1, 'real anchor commit')
      call assert_store_time(store, endpoint_time, 'real anchor target')
      call assert_store_token(store, int(i,int64), 'real anchor payload unchanged')
    end do
  end subroutine test_real_lwkm_anchor_packets_bind

  subroutine test_missing_real_interval_fails_closed()
    type(hydrology_step_t) :: packets(KT09_ANCHOR_COUNT)
    type(animo_multi_packet_hydrology_runtime_probe_client_t) :: client
    type(accepted_store_t) :: store
    type(TimeCoordinate) :: t0, t9
    type(attempt_request_t) :: request(1)
    type(runtime_trace_t) :: trace
    integer :: i
    logical :: ok, success
    character(len=128) :: reason

    do i = 1, KT09_ANCHOR_COUNT
      call make_kt09_anchor_step(i, packets(i))
    end do
    call initialize_multi_packet_client(client, packets, CALENDAR_ID, 0_int64, ok, reason)
    call assert_true(ok, 'real missing provider init')
    call make_time(0_int64, t0)
    call make_time(9_int64, t9)
    call initialize_probe_store(store, 'KT11_REAL_MISSING', t0, 109_int64, ok)
    call assert_true(ok, 'real missing store init')
    request(1)%endpoint_time = t9
    call run_interval(store, client, t9, request, 1, trace, success, reason)
    call assert_true(.not. success, 'real missing interval rejected')
    call assert_true(accepted_store_generation(store) == 0_int64, 'real missing generation')
    call assert_store_time(store, t0, 'real missing time')
  end subroutine test_missing_real_interval_fails_closed

end program test_kt11_multi_packet_hydrology_provider
