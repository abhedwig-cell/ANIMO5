program test_kt10_kt06_adversarial_boundaries
  use iso_fortran_env, only: int64, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_value, ieee_quiet_nan, ieee_positive_inf
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate, time_equal
  use mod_transient_contracts, only: transient_payload_t, admissibility_t
  use mod_transient_transactions, only: accepted_store_t, reconstruct_accepted_store_trusted, &
    accepted_store_generation, accepted_store_time, snapshot_accepted_payload
  use mod_transient_interval_runtime, only: attempt_request_t, runtime_trace_t, run_interval
  use mod_animo_hydrology_adapter, only: hydrology_step_t, HYDROLOGY_SCHEMA_ID, &
    HYDROLOGY_UNIT_CONTRACT_ID
  use mod_animo_explicit_hydrology_runtime_binding, only: animo_runtime_probe_state_t, &
    animo_explicit_hydrology_runtime_probe_client_t, initialize_probe_store
  implicit none

  integer(int64), parameter :: MAX_EXACT_REAL64_INTEGER = 9007199254740991_int64
  character(len=*), parameter :: CALENDAR_ID = 'ANIMO_KT10_DAILY_V1'

  type(TimeCoordinate) :: tneg1, t0, t9, t10, t10half, tmax, tabove
  logical :: ok

  call make_time_coordinate(CALENDAR_ID, -1_int64, 0_int64, 1_int64, tneg1, ok)
  call assert_true(ok, 'negative-day coordinate construction')
  call make_time_coordinate(CALENDAR_ID, 0_int64, 0_int64, 1_int64, t0, ok)
  call assert_true(ok, 't0 construction')
  call make_time_coordinate(CALENDAR_ID, 9_int64, 0_int64, 1_int64, t9, ok)
  call assert_true(ok, 't9 construction')
  call make_time_coordinate(CALENDAR_ID, 10_int64, 0_int64, 1_int64, t10, ok)
  call assert_true(ok, 't10 construction')
  call make_time_coordinate(CALENDAR_ID, 10_int64, 1_int64, 2_int64, t10half, ok)
  call assert_true(ok, 't10half construction')
  call make_time_coordinate( &
    CALENDAR_ID, MAX_EXACT_REAL64_INTEGER, 0_int64, 1_int64, tmax, ok)
  call assert_true(ok, 'max-exact construction')
  call make_time_coordinate( &
    CALENDAR_ID, MAX_EXACT_REAL64_INTEGER + 1_int64, 0_int64, 1_int64, tabove, ok)
  call assert_true(ok, 'above-exact construction')

  call test_missing_forcing(t0, t10)
  call test_missing_calendar_binding(t0, t10)
  call test_negative_offset(t0, t10)
  call test_negative_runtime_origin(tneg1, t9)
  call test_offset_overflow(t0, t10)
  call test_fractional_endpoint(t0, t10)
  call test_negative_endpoint(t0, t10)
  call test_negative_zero_endpoint(t0, t10)
  call test_nan_endpoint(t0, t10)
  call test_infinite_step(t0, t10)
  call test_calendar_mismatch(t0, t10)
  call test_subday_endpoint(t0, t10half)
  call test_max_exact_integer_success(t0, tmax)
  call test_above_max_exact_integer_rejected(t0, tabove)
  call test_generation_overflow_no_publication(t0, t10)
  call test_retry_flag_cannot_mask_client_failure(t0, t10)

  print *, 'KT10 KT06 adversarial boundary harness: PASS'

contains

  subroutine assert_true(condition, label)
    logical, intent(in) :: condition
    character(len=*), intent(in) :: label
    if (.not. condition) then
      print *, 'ASSERTION FAILED: ', trim(label)
      error stop 1
    end if
  end subroutine assert_true

  subroutine configure_valid_client(client)
    type(animo_explicit_hydrology_runtime_probe_client_t), intent(out) :: client
    type(hydrology_step_t) :: step

    step%schema_id = HYDROLOGY_SCHEMA_ID
    step%unit_contract_id = HYDROLOGY_UNIT_CONTRACT_ID
    step%layer_count = 2
    step%drainage_count = 1
    step%producer_endpoint_day = 10.0_real64
    step%producer_step_days = 10.0_real64
    step%has_interception_storage_end = .true.
    step%interception_storage_end = 0.0_real64
    step%has_soil_temperature = .false.

    allocate(step%sc(2), step%mofrt(2), step%flev(2), step%flab(3))
    allocate(step%fldr(1, 2), step%soil_temperature(0))
    step%sc = 0.0_real64
    step%mofrt = 0.0_real64
    step%flev = 0.0_real64
    step%flab = 0.0_real64
    step%fldr = 0.0_real64

    client%forcing = step
    client%forcing_present = .true.
    client%runtime_calendar_contract_id = CALENDAR_ID
    client%producer_day_offset = 0_int64
  end subroutine configure_valid_client

  subroutine assert_direct_failure(client, origin_time, endpoint_time, expected_reason, label)
    type(animo_explicit_hydrology_runtime_probe_client_t), intent(inout) :: client
    type(TimeCoordinate), intent(in) :: origin_time, endpoint_time
    character(len=*), intent(in) :: expected_reason, label
    type(animo_runtime_probe_state_t) :: origin
    class(transient_payload_t), allocatable :: candidate
    type(admissibility_t) :: admissibility
    logical :: attempt_ok
    character(len=64) :: reason

    origin%state_token = 41_int64
    call client%execute_attempt( &
      origin, origin_time, endpoint_time, candidate, admissibility, attempt_ok, reason)

    call assert_true(.not. attempt_ok, trim(label)//' rejected')
    call assert_true(.not. allocated(candidate), trim(label)//' no candidate')
    call assert_true(trim(reason) == trim(expected_reason), trim(label)//' reason')
    call assert_true(.not. admissibility%evidence_complete, trim(label)//' no complete evidence')
    call assert_true(.not. admissibility%admissible, trim(label)//' not admissible')
  end subroutine assert_direct_failure

  subroutine test_missing_forcing(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(animo_explicit_hydrology_runtime_probe_client_t) :: client
    call configure_valid_client(client)
    client%forcing_present = .false.
    call assert_direct_failure( &
      client, t_start, t_end, 'MISSING_HYDROLOGY_FORCING', 'missing forcing')
  end subroutine test_missing_forcing

  subroutine test_missing_calendar_binding(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(animo_explicit_hydrology_runtime_probe_client_t) :: client
    call configure_valid_client(client)
    client%runtime_calendar_contract_id = ''
    call assert_direct_failure( &
      client, t_start, t_end, 'MISSING_RUNTIME_CALENDAR_BINDING', 'missing calendar')
  end subroutine test_missing_calendar_binding

  subroutine test_negative_offset(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(animo_explicit_hydrology_runtime_probe_client_t) :: client
    call configure_valid_client(client)
    client%producer_day_offset = -1_int64
    call assert_direct_failure( &
      client, t_start, t_end, 'INVALID_PRODUCER_DAY_OFFSET', 'negative offset')
  end subroutine test_negative_offset

  subroutine test_negative_runtime_origin(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(animo_explicit_hydrology_runtime_probe_client_t) :: client
    call configure_valid_client(client)
    call assert_direct_failure( &
      client, t_start, t_end, 'INVALID_RUNTIME_INTERVAL', 'negative runtime origin')
  end subroutine test_negative_runtime_origin

  subroutine test_offset_overflow(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(animo_explicit_hydrology_runtime_probe_client_t) :: client
    call configure_valid_client(client)
    client%producer_day_offset = huge(0_int64)
    call assert_direct_failure( &
      client, t_start, t_end, 'PRODUCER_TIME_MAPPING_OVERFLOW', 'offset overflow')
  end subroutine test_offset_overflow

  subroutine test_fractional_endpoint(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(animo_explicit_hydrology_runtime_probe_client_t) :: client
    call configure_valid_client(client)
    client%forcing%producer_endpoint_day = 10.5_real64
    call assert_direct_failure( &
      client, t_start, t_end, 'NONEXACT_PRODUCER_TIME_METADATA', 'fractional endpoint')
  end subroutine test_fractional_endpoint

  subroutine test_negative_endpoint(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(animo_explicit_hydrology_runtime_probe_client_t) :: client
    call configure_valid_client(client)
    client%forcing%producer_endpoint_day = -1.0_real64
    call assert_direct_failure( &
      client, t_start, t_end, 'NONEXACT_PRODUCER_TIME_METADATA', 'negative endpoint')
  end subroutine test_negative_endpoint

  subroutine test_negative_zero_endpoint(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(animo_explicit_hydrology_runtime_probe_client_t) :: client
    call configure_valid_client(client)
    client%forcing%producer_endpoint_day = -0.0_real64
    call assert_direct_failure( &
      client, t_start, t_end, 'NONEXACT_PRODUCER_TIME_METADATA', 'negative zero endpoint')
  end subroutine test_negative_zero_endpoint

  subroutine test_nan_endpoint(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(animo_explicit_hydrology_runtime_probe_client_t) :: client
    call configure_valid_client(client)
    client%forcing%producer_endpoint_day = ieee_value(0.0_real64, ieee_quiet_nan)
    call assert_direct_failure( &
      client, t_start, t_end, 'INVALID_KT05_EXPLICIT_HYDROLOGY_STEP', 'NaN endpoint')
  end subroutine test_nan_endpoint

  subroutine test_infinite_step(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(animo_explicit_hydrology_runtime_probe_client_t) :: client
    call configure_valid_client(client)
    client%forcing%producer_step_days = ieee_value(0.0_real64, ieee_positive_inf)
    call assert_direct_failure( &
      client, t_start, t_end, 'INVALID_KT05_EXPLICIT_HYDROLOGY_STEP', 'infinite step')
  end subroutine test_infinite_step

  subroutine test_calendar_mismatch(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(animo_explicit_hydrology_runtime_probe_client_t) :: client
    call configure_valid_client(client)
    client%runtime_calendar_contract_id = 'ANOTHER_CALENDAR'
    call assert_direct_failure( &
      client, t_start, t_end, 'RUNTIME_CALENDAR_BINDING_MISMATCH', 'calendar mismatch')
  end subroutine test_calendar_mismatch

  subroutine test_subday_endpoint(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(animo_explicit_hydrology_runtime_probe_client_t) :: client
    call configure_valid_client(client)
    call assert_direct_failure( &
      client, t_start, t_end, 'SUBDAY_MAPPING_NOT_QUALIFIED', 'subday endpoint')
  end subroutine test_subday_endpoint

  subroutine test_max_exact_integer_success(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(animo_explicit_hydrology_runtime_probe_client_t) :: client
    type(animo_runtime_probe_state_t) :: origin
    class(transient_payload_t), allocatable :: candidate
    type(admissibility_t) :: admissibility
    logical :: attempt_ok
    character(len=64) :: reason

    call configure_valid_client(client)
    client%forcing%producer_endpoint_day = real(MAX_EXACT_REAL64_INTEGER, real64)
    client%forcing%producer_step_days = real(MAX_EXACT_REAL64_INTEGER, real64)
    origin%state_token = 43_int64

    call client%execute_attempt( &
      origin, t_start, t_end, candidate, admissibility, attempt_ok, reason)

    call assert_true(attempt_ok, 'max exact integer accepted')
    call assert_true(allocated(candidate), 'max exact integer candidate')
    call assert_true(admissibility%evidence_complete, 'max exact evidence complete')
    call assert_true(admissibility%admissible, 'max exact admissible')
    call assert_true(trim(reason) == 'BOUND_AND_PROJECTED', 'max exact reason')
  end subroutine test_max_exact_integer_success

  subroutine test_above_max_exact_integer_rejected(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(animo_explicit_hydrology_runtime_probe_client_t) :: client
    call configure_valid_client(client)
    client%forcing%producer_endpoint_day = real(MAX_EXACT_REAL64_INTEGER + 1_int64, real64)
    client%forcing%producer_step_days = real(MAX_EXACT_REAL64_INTEGER + 1_int64, real64)
    call assert_direct_failure( &
      client, t_start, t_end, 'NONEXACT_PRODUCER_TIME_METADATA', 'above exact integer')
  end subroutine test_above_max_exact_integer_rejected

  subroutine assert_store_time(store, expected, label)
    type(accepted_store_t), intent(in) :: store
    type(TimeCoordinate), intent(in) :: expected
    character(len=*), intent(in) :: label
    type(TimeCoordinate) :: actual
    logical :: got_time, equal, compare_ok

    call accepted_store_time(store, actual, got_time)
    call assert_true(got_time, trim(label)//' time available')
    call time_equal(actual, expected, equal, compare_ok)
    call assert_true(compare_ok .and. equal, trim(label)//' time unchanged')
  end subroutine assert_store_time

  subroutine assert_store_token(store, expected, label)
    type(accepted_store_t), intent(in) :: store
    integer(int64), intent(in) :: expected
    character(len=*), intent(in) :: label
    class(transient_payload_t), allocatable :: payload
    logical :: snapshot_ok

    call snapshot_accepted_payload(store, payload, snapshot_ok)
    call assert_true(snapshot_ok, trim(label)//' snapshot')
    select type (typed => payload)
    type is (animo_runtime_probe_state_t)
      call assert_true(typed%state_token == expected, trim(label)//' token')
    class default
      call assert_true(.false., trim(label)//' payload type')
    end select
  end subroutine assert_store_token

  subroutine test_generation_overflow_no_publication(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(accepted_store_t) :: store
    type(animo_runtime_probe_state_t) :: payload
    type(animo_explicit_hydrology_runtime_probe_client_t) :: client
    type(attempt_request_t) :: requests(1)
    type(runtime_trace_t) :: trace
    logical :: store_ok, success
    character(len=64) :: reason

    payload%state_token = 47_int64
    call reconstruct_accepted_store_trusted( &
      'ANIMO_KT10_GENERATION', huge(0_int64), t_start, payload, store, store_ok)
    call assert_true(store_ok, 'generation-overflow store reconstruction')
    call configure_valid_client(client)
    requests(1)%endpoint_time = t_end
    requests(1)%retry_permitted_after_reject = .false.

    call run_interval(store, client, t_end, requests, 1, trace, success, reason)

    call assert_true(.not. success, 'generation overflow rejected')
    call assert_true(trim(reason) == 'TRANSACTION_COMMIT_FAILED', 'generation overflow reason')
    call assert_true( &
      accepted_store_generation(store) == huge(0_int64), 'generation unchanged at maximum')
    call assert_store_time(store, t_start, 'generation overflow')
    call assert_store_token(store, 47_int64, 'generation overflow')
  end subroutine test_generation_overflow_no_publication

  subroutine test_retry_flag_cannot_mask_client_failure(t_start, t_end)
    type(TimeCoordinate), intent(in) :: t_start, t_end
    type(accepted_store_t) :: store
    type(animo_explicit_hydrology_runtime_probe_client_t) :: client
    type(attempt_request_t) :: requests(1)
    type(runtime_trace_t) :: trace
    logical :: store_ok, success
    character(len=64) :: reason

    call initialize_probe_store(store, 'ANIMO_KT10_RETRY', t_start, 53_int64, store_ok)
    call assert_true(store_ok, 'retry store initialize')
    call configure_valid_client(client)
    client%forcing%producer_step_days = 9.0_real64
    requests(1)%endpoint_time = t_end
    requests(1)%retry_permitted_after_reject = .true.

    call run_interval(store, client, t_end, requests, 1, trace, success, reason)

    call assert_true(.not. success, 'client failure not masked by retry flag')
    call assert_true(trim(reason) == 'CLIENT_ATTEMPT_FAILED', 'client failure reason')
    call assert_true(trace%attempt_count == 1, 'single failed client attempt')
    call assert_true(trace%commit_count == 0, 'no retry-path commit')
    call assert_true(accepted_store_generation(store) == 0_int64, 'retry generation unchanged')
    call assert_store_time(store, t_start, 'retry client failure')
    call assert_store_token(store, 53_int64, 'retry client failure')
  end subroutine test_retry_flag_cannot_mask_client_failure

end program test_kt10_kt06_adversarial_boundaries
