program test_kt05_explicit_runtime_adapter
  use iso_fortran_env, only: int64, real64
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate, time_equal
  use mod_transient_contracts, only: transient_payload_t
  use mod_transient_transactions, only: accepted_store_t, accepted_store_generation, accepted_store_time, &
    snapshot_accepted_payload
  use mod_transient_interval_runtime, only: attempt_request_t, runtime_trace_t, run_interval
  use mod_animo_explicit_hydrology_runtime_adapter, only: HYDROLOGY_SCHEMA_ID, HYDROLOGY_UNIT_ID, &
    animo_runtime_probe_state_t, animo_explicit_hydrology_client_t, initialize_probe_store
  implicit none

  type(TimeCoordinate) :: t100, t108, t108half
  logical :: ok

  call make_time_coordinate('ANIMO_RUNTIME_V1', 100_int64, 0_int64, 1_int64, t100, ok)
  call assert_true(ok, 't100 construction')
  call make_time_coordinate('ANIMO_RUNTIME_V1', 108_int64, 0_int64, 1_int64, t108, ok)
  call assert_true(ok, 't108 construction')
  call make_time_coordinate('ANIMO_RUNTIME_V1', 108_int64, 1_int64, 2_int64, t108half, ok)
  call assert_true(ok, 't108half construction')

  call test_exact_explicit_binding_commits(t100, t108)
  call test_endpoint_mismatch_fails_closed(t100, t108)
  call test_missing_explicit_state_fails_closed(t100, t108)
  call test_fractional_producer_metadata_fails_closed(t100, t108)
  call test_subday_runtime_mapping_fails_closed(t100, t108half)

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

  subroutine configure_valid_client(client)
    type(animo_explicit_hydrology_client_t), intent(out) :: client
    client%forcing_present = .true.
    client%producer_day_offset = 1000_int64
    client%forcing%schema_id = HYDROLOGY_SCHEMA_ID
    client%forcing%unit_contract_id = HYDROLOGY_UNIT_ID
    client%forcing%producer_endpoint_day = 1108.0_real64
    client%forcing%producer_step_days = 8.0_real64
    client%forcing%has_interception_storage_end = .true.
    client%forcing%interception_storage_end = 0.0002_real64
  end subroutine configure_valid_client

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

  subroutine test_exact_explicit_binding_commits(t0, t1)
    type(TimeCoordinate), intent(in) :: t0, t1
    type(accepted_store_t) :: store
    type(animo_explicit_hydrology_client_t) :: client
    logical :: ok, success
    character(len=64) :: reason

    call initialize_probe_store(store, 'ANIMO_KT05_EXPLICIT', t0, 7_int64, ok)
    call assert_true(ok, 'explicit store initialize')
    call configure_valid_client(client)
    call run_one(store, client, t1, success, reason)

    call assert_true(success, 'explicit interval success')
    call assert_true(trim(reason) == 'INTERVAL_COMMITTED', 'explicit interval reason')
    call assert_true(accepted_store_generation(store) == 1_int64, 'explicit generation')
    call assert_store_time(store, t1, 'explicit exact runtime target')
    call assert_state_token(store, 7_int64, 'forcing not accepted state')
  end subroutine test_exact_explicit_binding_commits

  subroutine test_endpoint_mismatch_fails_closed(t0, t1)
    type(TimeCoordinate), intent(in) :: t0, t1
    type(accepted_store_t) :: store
    type(animo_explicit_hydrology_client_t) :: client
    logical :: ok, success
    character(len=64) :: reason

    call initialize_probe_store(store, 'ANIMO_KT05_ENDPOINT', t0, 11_int64, ok)
    call assert_true(ok, 'endpoint store initialize')
    call configure_valid_client(client)
    client%forcing%producer_endpoint_day = 1109.0_real64
    call run_one(store, client, t1, success, reason)

    call assert_true(.not. success, 'endpoint mismatch rejected')
    call assert_true(trim(reason) == 'CLIENT_ATTEMPT_FAILED', 'endpoint mismatch runtime reason')
    call assert_true(accepted_store_generation(store) == 0_int64, 'endpoint generation unchanged')
    call assert_store_time(store, t0, 'endpoint time unchanged')
    call assert_state_token(store, 11_int64, 'endpoint payload unchanged')
  end subroutine test_endpoint_mismatch_fails_closed

  subroutine test_missing_explicit_state_fails_closed(t0, t1)
    type(TimeCoordinate), intent(in) :: t0, t1
    type(accepted_store_t) :: store
    type(animo_explicit_hydrology_client_t) :: client
    logical :: ok, success
    character(len=64) :: reason

    call initialize_probe_store(store, 'ANIMO_KT05_SICT', t0, 13_int64, ok)
    call assert_true(ok, 'Sict store initialize')
    call configure_valid_client(client)
    client%forcing%has_interception_storage_end = .false.
    call run_one(store, client, t1, success, reason)

    call assert_true(.not. success, 'missing explicit state rejected')
    call assert_true(accepted_store_generation(store) == 0_int64, 'Sict generation unchanged')
    call assert_store_time(store, t0, 'Sict time unchanged')
  end subroutine test_missing_explicit_state_fails_closed

  subroutine test_fractional_producer_metadata_fails_closed(t0, t1)
    type(TimeCoordinate), intent(in) :: t0, t1
    type(accepted_store_t) :: store
    type(animo_explicit_hydrology_client_t) :: client
    logical :: ok, success
    character(len=64) :: reason

    call initialize_probe_store(store, 'ANIMO_KT05_META', t0, 17_int64, ok)
    call assert_true(ok, 'metadata store initialize')
    call configure_valid_client(client)
    client%forcing%producer_endpoint_day = 1108.5_real64
    call run_one(store, client, t1, success, reason)

    call assert_true(.not. success, 'fractional metadata rejected')
    call assert_true(accepted_store_generation(store) == 0_int64, 'metadata generation unchanged')
    call assert_store_time(store, t0, 'metadata time unchanged')
  end subroutine test_fractional_producer_metadata_fails_closed

  subroutine test_subday_runtime_mapping_fails_closed(t0, target)
    type(TimeCoordinate), intent(in) :: t0, target
    type(accepted_store_t) :: store
    type(animo_explicit_hydrology_client_t) :: client
    logical :: ok, success
    character(len=64) :: reason

    call initialize_probe_store(store, 'ANIMO_KT05_SUBDAY', t0, 19_int64, ok)
    call assert_true(ok, 'subday store initialize')
    call configure_valid_client(client)
    call run_one(store, client, target, success, reason)

    call assert_true(.not. success, 'subday mapping rejected')
    call assert_true(accepted_store_generation(store) == 0_int64, 'subday generation unchanged')
    call assert_store_time(store, t0, 'subday time unchanged')
  end subroutine test_subday_runtime_mapping_fails_closed

end program test_kt05_explicit_runtime_adapter
