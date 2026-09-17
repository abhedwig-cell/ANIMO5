program test_kt02_dual_client
  use iso_fortran_env, only: int64, real64
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate, time_equal
  use mod_transient_contracts, only: accepted_store_t, trial_state_t, trial_result_t, admissibility_t
  use mod_transient_transactions, only: begin_trial, commit_trial
  use mod_transient_interval_runtime, only: attempt_request_t, runtime_trace_t, run_interval
  use mod_transient_persistence, only: accepted_checkpoint_t, make_checkpoint, restore_checkpoint
  use mod_transient_worker_context, only: worker_context_t, initialize_worker_context, prepare_worker_attempt
  use mod_swap_like_client, only: swap_like_payload_t, swap_like_client_t, initialize_swap_like_store
  use mod_animo_like_client, only: animo_like_payload_t, animo_like_client_t, initialize_animo_like_store
  implicit none

  type(TimeCoordinate) :: t0, thalf, tone
  logical :: ok

  call make_time_coordinate('TEST_CAL', 0_int64, 0_int64, 1_int64, t0, ok)
  call assert_true(ok, 't0 construction')
  call make_time_coordinate('TEST_CAL', 0_int64, 1_int64, 2_int64, thalf, ok)
  call assert_true(ok, 'thalf construction')
  call make_time_coordinate('TEST_CAL', 0_int64, 1_int64, 1_int64, tone, ok)
  call assert_true(ok, 'tone construction')

  call test_swap_like_success_retry_and_checkpoint(t0, thalf, tone)
  call test_incomplete_interval_no_publication(t0, thalf, tone)
  call test_stale_commit_rejects(t0, thalf)
  call test_animo_like_success_retry(t0, thalf, tone)
  call test_worker_reset()

  print *, 'KT02 dual-client runtime tests: PASS'

contains

  subroutine assert_true(condition, label)
    logical, intent(in) :: condition
    character(len=*), intent(in) :: label
    if (.not. condition) then
      print *, 'ASSERTION FAILED: ', trim(label)
      error stop 1
    end if
  end subroutine assert_true

  subroutine test_swap_like_success_retry_and_checkpoint(t0, thalf, tone)
    type(TimeCoordinate), intent(in) :: t0, thalf, tone
    type(accepted_store_t) :: store, restored
    type(swap_like_client_t) :: client
    type(attempt_request_t) :: requests(3)
    type(runtime_trace_t) :: trace
    type(accepted_checkpoint_t) :: checkpoint
    logical :: success, ok, equal, time_ok
    character(len=64) :: reason

    call initialize_swap_like_store(store, 'SWAP_LIKE_A', t0, 0.0_real64, ok)
    call assert_true(ok, 'swap store initialize')
    client%delta_per_accepted_attempt = 1.0_real64
    client%reject_first_attempt = .true.

    requests(1)%endpoint_time = thalf
    requests(1)%retry_permitted_after_reject = .true.
    requests(2)%endpoint_time = thalf
    requests(2)%retry_permitted_after_reject = .false.
    requests(3)%endpoint_time = tone
    requests(3)%retry_permitted_after_reject = .false.

    call run_interval(store, client, tone, requests, 3, trace, success, reason)
    call assert_true(success, 'swap interval success')
    call assert_true(trim(reason) == 'INTERVAL_COMMITTED', 'swap interval reason')
    call assert_true(trace%attempt_count == 3, 'swap attempt count')
    call assert_true(trace%commit_count == 2, 'swap commit count')
    call assert_true(.not. trace%accepted_attempt(1), 'swap first rejected')
    call assert_true(trace%accepted_attempt(2), 'swap retry accepted')
    call assert_true(trace%origin_generation(1) == 0_int64, 'swap rejected origin generation')
    call assert_true(trace%origin_generation(2) == 0_int64, 'swap retry same origin generation')
    call assert_true(store%generation == 2_int64, 'swap final generation')
    call time_equal(store%accepted_time, tone, equal, time_ok)
    call assert_true(time_ok .and. equal, 'swap final exact target')
    select type (payload => store%payload)
    type is (swap_like_payload_t)
      call assert_true(abs(payload%state_value - 2.0_real64) < epsilon(1.0_real64), 'swap final payload')
    class default
      call assert_true(.false., 'swap payload dynamic type')
    end select

    call make_checkpoint(store, 'KT02_SCHEMA', 'SWAP_LAYOUT', 'SWAP_CFG', 'SWAP_FEATURES', checkpoint, ok)
    call assert_true(ok, 'swap checkpoint make')
    call restore_checkpoint(checkpoint, 'KT02_SCHEMA', 'SWAP_LAYOUT', 'SWAP_CFG', 'SWAP_FEATURES', restored, ok, reason)
    call assert_true(ok, 'swap checkpoint restore')
    call assert_true(restored%generation == store%generation, 'swap restored generation')
    call time_equal(restored%accepted_time, store%accepted_time, equal, time_ok)
    call assert_true(time_ok .and. equal, 'swap restored time')
    select type (payload => restored%payload)
    type is (swap_like_payload_t)
      call assert_true(abs(payload%state_value - 2.0_real64) < epsilon(1.0_real64), 'swap restored payload')
    class default
      call assert_true(.false., 'swap restored payload type')
    end select
  end subroutine test_swap_like_success_retry_and_checkpoint

  subroutine test_incomplete_interval_no_publication(t0, thalf, tone)
    type(TimeCoordinate), intent(in) :: t0, thalf, tone
    type(accepted_store_t) :: store
    type(swap_like_client_t) :: client
    type(attempt_request_t) :: requests(1)
    type(runtime_trace_t) :: trace
    logical :: success, ok, equal, time_ok
    character(len=64) :: reason

    call initialize_swap_like_store(store, 'SWAP_LIKE_INCOMPLETE', t0, 5.0_real64, ok)
    call assert_true(ok, 'incomplete store initialize')
    requests(1)%endpoint_time = thalf
    requests(1)%retry_permitted_after_reject = .false.

    call run_interval(store, client, tone, requests, 2, trace, success, reason)
    call assert_true(.not. success, 'incomplete interval fails')
    call assert_true(trim(reason) == 'INCOMPLETE_INTERVAL_COMPLETION', 'incomplete interval reason')
    call assert_true(store%generation == 0_int64, 'incomplete external generation unchanged')
    call time_equal(store%accepted_time, t0, equal, time_ok)
    call assert_true(time_ok .and. equal, 'incomplete external time unchanged')
    select type (payload => store%payload)
    type is (swap_like_payload_t)
      call assert_true(abs(payload%state_value - 5.0_real64) < epsilon(1.0_real64), 'incomplete payload unchanged')
    class default
      call assert_true(.false., 'incomplete payload type')
    end select
  end subroutine test_incomplete_interval_no_publication

  subroutine test_stale_commit_rejects(t0, thalf)
    type(TimeCoordinate), intent(in) :: t0, thalf
    type(accepted_store_t) :: store
    type(trial_state_t) :: trial
    type(trial_result_t) :: result
    logical :: ok
    character(len=64) :: reason

    call initialize_swap_like_store(store, 'SWAP_STALE', t0, 3.0_real64, ok)
    call assert_true(ok, 'stale store initialize')
    call begin_trial(store, thalf, trial, ok)
    call assert_true(ok, 'stale begin trial')
    select type (payload => trial%payload)
    type is (swap_like_payload_t)
      payload%state_value = 9.0_real64
    class default
      call assert_true(.false., 'stale trial payload type')
    end select
    result = trial_result_t()
    result%candidate = trial
    result%candidate%origin_generation = 1_int64
    result%admissibility = admissibility_t(evidence_complete=.true., admissible=.true.)
    result%provenance_id = 'STALE_ATTEMPT'

    call commit_trial(store, result, ok, reason)
    call assert_true(.not. ok, 'stale commit rejects')
    call assert_true(trim(reason) == 'STALE_ORIGIN_GENERATION', 'stale commit reason')
    call assert_true(store%generation == 0_int64, 'stale external generation unchanged')
    select type (payload => store%payload)
    type is (swap_like_payload_t)
      call assert_true(abs(payload%state_value - 3.0_real64) < epsilon(1.0_real64), 'stale payload unchanged')
    class default
      call assert_true(.false., 'stale payload type')
    end select
  end subroutine test_stale_commit_rejects

  subroutine test_animo_like_success_retry(t0, thalf, tone)
    type(TimeCoordinate), intent(in) :: t0, thalf, tone
    type(accepted_store_t) :: store
    type(animo_like_client_t) :: client
    type(attempt_request_t) :: requests(3)
    type(runtime_trace_t) :: trace
    logical :: success, ok, equal, time_ok
    character(len=64) :: reason

    call initialize_animo_like_store(store, 'ANIMO_LIKE_A', t0, 10_int64, 0_int64, ok)
    call assert_true(ok, 'animo store initialize')
    client%transfer_per_accepted_attempt = 2_int64
    client%reject_first_attempt = .true.

    requests(1)%endpoint_time = thalf
    requests(1)%retry_permitted_after_reject = .true.
    requests(2)%endpoint_time = thalf
    requests(2)%retry_permitted_after_reject = .false.
    requests(3)%endpoint_time = tone
    requests(3)%retry_permitted_after_reject = .false.

    call run_interval(store, client, tone, requests, 3, trace, success, reason)
    call assert_true(success, 'animo interval success')
    call assert_true(trace%commit_count == 2, 'animo commit count')
    call assert_true(trace%origin_generation(1) == 0_int64, 'animo rejected origin generation')
    call assert_true(trace%origin_generation(2) == 0_int64, 'animo retry same origin generation')
    call assert_true(store%generation == 2_int64, 'animo final generation')
    call time_equal(store%accepted_time, tone, equal, time_ok)
    call assert_true(time_ok .and. equal, 'animo final exact target')
    select type (payload => store%payload)
    type is (animo_like_payload_t)
      call assert_true(payload%store_a == 6_int64, 'animo store a')
      call assert_true(payload%store_b == 4_int64, 'animo store b')
      call assert_true(payload%store_a + payload%store_b == 10_int64, 'animo conserved total')
    class default
      call assert_true(.false., 'animo payload dynamic type')
    end select
  end subroutine test_animo_like_success_retry

  subroutine test_worker_reset()
    type(worker_context_t) :: context
    logical :: ok
    call initialize_worker_context(context, 'WORKER_A', ok)
    call assert_true(ok, 'worker initialize')
    call prepare_worker_attempt(context, 'MODEL_A', 'ATTEMPT_1', ok)
    call assert_true(ok, 'worker attempt 1')
    context%scratch_counter = 77_int64
    context%diagnostic_counter = 9_int64
    call prepare_worker_attempt(context, 'MODEL_B', 'ATTEMPT_2', ok)
    call assert_true(ok, 'worker attempt 2')
    call assert_true(context%scratch_counter == 0_int64, 'worker scratch reset')
    call assert_true(context%diagnostic_counter == 0_int64, 'worker diagnostics reset')
  end subroutine test_worker_reset

end program test_kt02_dual_client
