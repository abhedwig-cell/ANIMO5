program test_kt01_runtime
  use iso_fortran_env, only: int64, real64
  use mod_animo_time_coordinate
  use mod_animo_runtime_contracts
  use mod_animo_kernel_transactions
  use mod_animo_committed_persistence
  use mod_animo_worker_context
  use mod_animo_interval_runtime
  implicit none

  integer :: failures
  failures = 0
  call run_tests(failures)
  if (failures /= 0) then
    write(*,'(A,I0)') 'KT01 FORTRAN TEST FAILURES: ', failures
    error stop 1
  end if
  write(*,'(A)') 'KT01 FORTRAN TESTS 01-23, 26-29 AND 36-38: PASS'

contains

  subroutine assert_true(condition, label, failures)
    logical, intent(in) :: condition
    character(len=*), intent(in) :: label
    integer, intent(inout) :: failures
    if (condition) then
      write(*,'(A)') 'PASS '//trim(label)
    else
      write(*,'(A)') 'FAIL '//trim(label)
      failures = failures + 1
    end if
  end subroutine assert_true

  subroutine make_time(day, numerator, denominator, value)
    integer(int64), intent(in) :: day, numerator, denominator
    type(TimeCoordinate), intent(out) :: value
    logical :: ok
    call make_time_coordinate('ANIMO_PG_86400_NOLEAPSECONDS_V1', day, numerator, denominator, value, ok)
    if (.not. ok) error stop 'invalid test time fixture'
  end subroutine make_time

  subroutine init_state(state, day, storage)
    type(AcceptedState), intent(out) :: state
    integer(int64), intent(in) :: day, storage
    state = AcceptedState()
    state%lineage_id = 'LINEAGE-A'
    state%generation = 7_int64
    call make_time(day, 0_int64, 1_int64, state%accepted_time)
    state%synthetic_storage = storage
  end subroutine init_state

  subroutine make_result(state, endpoint, delta, transfer_amount, complete, admissible, result, ok)
    type(AcceptedState), intent(in) :: state
    type(TimeCoordinate), intent(in) :: endpoint
    integer(int64), intent(in) :: delta, transfer_amount
    logical, intent(in) :: complete, admissible
    type(TrialResult), intent(out) :: result
    logical, intent(out) :: ok
    type(TrialState) :: trial
    integer(int64) :: candidate_storage
    logical :: event_ok

    result = TrialResult()
    call begin_trial(state, endpoint, trial, ok)
    if (.not. ok) return
    if (.not. checked_add_storage(trial%synthetic_storage, delta, candidate_storage)) then
      ok = .false.
      return
    end if
    trial%synthetic_storage = candidate_storage
    call append_transfer_event(trial%trial_journal, 'SYNTHETIC_Q', 'CV_OUTSIDE', 'CV_PRIMARY', &
      transfer_amount, event_ok)
    if (.not. event_ok) then
      ok = .false.
      return
    end if
    result%candidate = trial
    result%n_assessments = 1
    result%assessments(1)%quantity_id = 'SYNTHETIC_Q'
    result%assessments(1)%control_volume_id = 'CV_PRIMARY'
    result%assessments(1)%beginning_storage = state%synthetic_storage
    result%assessments(1)%ending_storage = candidate_storage
    result%assessments(1)%inbound_transfer = transfer_amount
    result%assessments(1)%complete = complete
    result%assessments(1)%admissible = admissible
    result%provenance_id = 'KT01_TEST_ATTEMPT'
    ok = .true.
  end subroutine make_result

  logical function states_equal(left, right)
    type(AcceptedState), intent(in) :: left, right
    logical :: equal_time, time_ok
    call time_equal(left%accepted_time, right%accepted_time, equal_time, time_ok)
    states_equal = time_ok .and. equal_time .and. &
      trim(left%lineage_id) == trim(right%lineage_id) .and. &
      left%generation == right%generation .and. &
      left%synthetic_storage == right%synthetic_storage
  end function states_equal

  logical function ledgers_equal(left, right)
    type(CommittedEventLedger), intent(in) :: left, right
    integer :: i
    ledgers_equal = .false.
    if (left%count /= right%count) return
    do i = 1, left%count
      if (trim(left%events(i)%quantity_id) /= trim(right%events(i)%quantity_id)) return
      if (trim(left%events(i)%source_id) /= trim(right%events(i)%source_id)) return
      if (trim(left%events(i)%sink_id) /= trim(right%events(i)%sink_id)) return
      if (left%events(i)%amount /= right%events(i)%amount) return
    end do
    ledgers_equal = .true.
  end function ledgers_equal

  subroutine run_tests(failures)
    integer, intent(inout) :: failures
    type(AcceptedState) :: state, before, restored, uninterrupted, split_state
    type(CommittedEventLedger) :: ledger, before_ledger, ledger_uninterrupted, ledger_split
    type(TimeCoordinate) :: target, halfway, other_time, overflow_time
    type(TrialResult) :: result
    type(SyntheticAttemptPlan) :: plans2(2), plan1(1)
    type(RuntimeTrace) :: trace
    type(AcceptedCheckpoint) :: checkpoint
    type(WorkerContext) :: worker
    logical :: ok, success, equal, ok2
    character(len=80) :: reason
    integer :: ordering
    integer(int64) :: generation_before, bits_a, bits_b
    real(real64) :: real_a, real_b

    call init_state(state, 10_int64, 100_int64)
    call clear_committed_ledger(ledger)
    before = state
    before_ledger = ledger
    call make_time(11_int64, 0_int64, 1_int64, target)
    call make_result(state, target, 9_int64, 9_int64, .true., .false., result, ok)
    call commit_trial(state, ledger, result, ok, reason)
    call assert_true(.not. ok .and. states_equal(state, before) .and. ledgers_equal(ledger, before_ledger), &
      '01 reject preserves accepted physical state', failures)

    call init_state(state, 20_int64, 50_int64)
    call clear_committed_ledger(ledger)
    call make_time(21_int64, 0_int64, 1_int64, target)
    plans2 = SyntheticAttemptPlan()
    plans2(1)%endpoint_time = target
    plans2(1)%storage_delta = 1_int64
    plans2(1)%transfer_amount = 1_int64
    plans2(1)%conservation_admissible = .false.
    plans2(1)%retry_permitted_after_reject = .true.
    plans2(2)%endpoint_time = target
    plans2(2)%storage_delta = 2_int64
    plans2(2)%transfer_amount = 2_int64
    call run_synthetic_interval(state, ledger, target, plans2, 2, trace, success, reason)
    call time_equal(trace%origin_time(1), trace%origin_time(2), equal, ok)
    call assert_true(success .and. ok .and. equal .and. &
      trace%origin_generation(1) == trace%origin_generation(2), '02 retry same origin', failures)

    call init_state(state, 30_int64, 10_int64)
    call clear_committed_ledger(ledger)
    call make_time(31_int64, 0_int64, 1_int64, target)
    call make_result(state, target, 5_int64, 5_int64, .true., .true., result, ok)
    call commit_trial(state, ledger, result, ok, reason)
    call assert_true(ok .and. state%synthetic_storage == 15_int64 .and. ledger%count == 1, &
      '03 atomic physical and event publication', failures)

    call init_state(state, 40_int64, 10_int64)
    call clear_committed_ledger(ledger)
    generation_before = state%generation
    call make_time(41_int64, 0_int64, 1_int64, target)
    call make_result(state, target, 1_int64, 1_int64, .true., .true., result, ok)
    call commit_trial(state, ledger, result, ok, reason)
    call assert_true(ok .and. state%generation == generation_before + 1_int64, '04 generation once', failures)

    call init_state(state, 50_int64, 10_int64)
    call clear_committed_ledger(ledger)
    call make_time(51_int64, 0_int64, 1_int64, target)
    call make_result(state, target, 1_int64, 1_int64, .true., .true., result, ok)
    result%candidate%origin_generation = result%candidate%origin_generation - 1_int64
    before = state
    call commit_trial(state, ledger, result, ok, reason)
    call assert_true(.not. ok .and. trim(reason) == 'STALE_ORIGIN_GENERATION' .and. states_equal(state, before), &
      '05 stale revision rejects', failures)

    call init_state(state, 60_int64, 10_int64)
    call clear_committed_ledger(ledger)
    call make_time(61_int64, 0_int64, 1_int64, target)
    call make_result(state, target, 1_int64, 1_int64, .true., .true., result, ok)
    result%candidate%origin_lineage_id = 'OTHER'
    call commit_trial(state, ledger, result, ok, reason)
    call assert_true(.not. ok .and. trim(reason) == 'LINEAGE_MISMATCH', '06 lineage mismatch rejects', failures)

    call init_state(state, 70_int64, 10_int64)
    call clear_committed_ledger(ledger)
    call make_time(71_int64, 0_int64, 1_int64, target)
    call make_result(state, target, 1_int64, 1_int64, .true., .true., result, ok)
    call make_time(69_int64, 0_int64, 1_int64, other_time)
    result%candidate%origin_time = other_time
    call commit_trial(state, ledger, result, ok, reason)
    call assert_true(.not. ok .and. trim(reason) == 'ORIGIN_TIME_MISMATCH', '07 wrong origin time rejects', failures)

    call init_state(state, 80_int64, 10_int64)
    call clear_committed_ledger(ledger)
    call make_time(81_int64, 0_int64, 1_int64, target)
    call make_result(state, target, 3_int64, 3_int64, .true., .false., result, ok)
    call commit_trial(state, ledger, result, ok, reason)
    call assert_true(.not. ok .and. result%candidate%trial_journal%count == 1 .and. ledger%count == 0, &
      '08 rejected journal uncommitted', failures)

    call init_state(state, 90_int64, 10_int64)
    before = state
    call initialize_worker_context(worker, 'WORKER', ok)
    call prepare_worker_attempt(worker, 'MODEL-A', 'ATTEMPT-1', ok)
    worker%scratch_value = 999_int64
    worker%attempt_diagnostic_counter = 123_int64
    call assert_true(states_equal(state, before), '09 scratch diagnostics nonphysical', failures)

    call init_state(state, 100_int64, 10_int64)
    call clear_committed_ledger(ledger)
    call append_transfer_event(result%candidate%trial_journal, 'SYNTHETIC_Q', 'A', 'B', 1_int64, ok)
    call make_accepted_checkpoint(state, 'CP1', 'L1', 'C1', 'F1', checkpoint, ok)
    call restore_accepted_checkpoint(checkpoint, 'CP1', 'L1', 'C1', 'F1', restored, ok, reason)
    call assert_true(ok .and. states_equal(state, restored), '10 checkpoint represents accepted physical state only', failures)

    call init_state(state, 110_int64, 22_int64)
    call make_accepted_checkpoint(state, 'CP1', 'L1', 'C1', 'F1', checkpoint, ok)
    call restore_accepted_checkpoint(checkpoint, 'CP1', 'L1', 'C1', 'F1', restored, ok, reason)
    call assert_true(ok .and. states_equal(state, restored), '11 restore identity', failures)

    call init_state(state, 120_int64, 22_int64)
    call make_accepted_checkpoint(state, 'CP1', 'L1', 'C1', 'F1', checkpoint, ok)
    call restore_accepted_checkpoint(checkpoint, 'CP2', 'L1', 'C1', 'F1', restored, ok, reason)
    ok2 = .not. ok .and. trim(reason) == 'CHECKPOINT_SCHEMA_MISMATCH'
    call restore_accepted_checkpoint(checkpoint, 'CP1', 'L2', 'C1', 'F1', restored, ok, reason)
    call assert_true(ok2 .and. .not. ok .and. trim(reason) == 'STATE_LAYOUT_MISMATCH', &
      '12 incompatible checkpoint rejects', failures)

    call make_time(130_int64, 1_int64, 3_int64, target)
    call make_time(130_int64, 2_int64, 6_int64, halfway)
    call time_equal(target, halfway, equal, ok)
    call assert_true(ok .and. equal, '13 exact time equality', failures)

    call make_time(140_int64, 6_int64, 4_int64, target)
    call assert_true(target%day_index == 141_int64 .and. target%subday_numerator == 1_int64 .and. &
      target%subday_denominator == 2_int64, '14 rational normalization', failures)

    block
      character(len=256) :: serialized
      call make_time(150_int64, 7_int64, 11_int64, target)
      call serialize_time_coordinate(target, serialized, ok)
      call deserialize_time_coordinate(trim(serialized), halfway, ok2)
      call time_equal(target, halfway, equal, ok)
      call assert_true(ok .and. ok2 .and. equal .and. &
        trim(serialized) == 'ANIMO_PG_86400_NOLEAPSECONDS_V1|150|7|11', &
        '15 exact prototype time serialization', failures)
    end block

    call make_time(1000_int64, 1_int64, 18014398509481984_int64, target)
    call make_time(1000_int64, 2_int64, 18014398509481984_int64, halfway)
    call time_compare(target, halfway, ordering, ok)
    real_a = real(target%day_index, real64) + real(target%subday_numerator, real64) / &
      real(target%subday_denominator, real64)
    real_b = real(halfway%day_index, real64) + real(halfway%subday_numerator, real64) / &
      real(halfway%subday_denominator, real64)
    bits_a = transfer(real_a, bits_a)
    bits_b = transfer(real_b, bits_b)
    call assert_true(ok .and. ordering < 0 .and. bits_a == bits_b, &
      '16 rationals distinct despite REAL collapse', failures)

    call make_time_coordinate('ANIMO_PG_86400_NOLEAPSECONDS_V1', 170_int64, 0_int64, 0_int64, target, ok)
    call make_time(huge(0_int64), 0_int64, 1_int64, overflow_time)
    call time_add_fraction(overflow_time, 1_int64, 1_int64, halfway, ok2)
    call assert_true(.not. ok .and. .not. ok2, '17 invalid overflow time fails', failures)

    call init_state(state, 180_int64, 10_int64)
    call clear_committed_ledger(ledger)
    before = state
    before_ledger = ledger
    call make_time(180_int64, 1_int64, 2_int64, halfway)
    call make_time(181_int64, 0_int64, 1_int64, target)
    plan1 = SyntheticAttemptPlan()
    plan1(1)%endpoint_time = halfway
    plan1(1)%storage_delta = 1_int64
    plan1(1)%transfer_amount = 1_int64
    call run_synthetic_interval(state, ledger, target, plan1, 2, trace, success, reason)
    call assert_true(.not. success .and. trim(reason) == 'INCOMPLETE_INTERVAL_COMPLETION' .and. &
      states_equal(state, before) .and. ledgers_equal(ledger, before_ledger), '18 exact target required', failures)

    call init_state(state, 190_int64, 10_int64)
    call clear_committed_ledger(ledger)
    call make_time(191_int64, 0_int64, 1_int64, target)
    plan1 = SyntheticAttemptPlan()
    plan1(1)%endpoint_time = state%accepted_time
    plan1(1)%conservation_admissible = .false.
    plan1(1)%retry_permitted_after_reject = .true.
    call run_synthetic_interval(state, ledger, target, plan1, 1, trace, success, reason)
    call assert_true(.not. success .and. trim(reason) == 'NO_OR_BACKWARD_PROGRESS', &
      '19 no-progress retry fails', failures)

    call initialize_worker_context(worker, 'WORKER', ok)
    call prepare_worker_attempt(worker, 'MODEL-A', 'ATTEMPT-1', ok)
    worker%scratch_value = 77_int64
    worker%attempt_diagnostic_counter = 9_int64
    call prepare_worker_attempt(worker, 'MODEL-B', 'ATTEMPT-1', ok)
    call assert_true(ok .and. trim(worker%logical_model_id) == 'MODEL-B' .and. &
      worker%scratch_value == 0_int64 .and. worker%attempt_diagnostic_counter == 0_int64, &
      '20 worker reuse isolated', failures)

    call init_state(state, 210_int64, 10_int64)
    call clear_committed_ledger(ledger)
    call make_time(211_int64, 0_int64, 1_int64, target)
    call make_result(state, target, 1_int64, 1_int64, .true., .true., result, ok)
    result%n_assessments = 2
    result%assessments(2)%quantity_id = 'Q2'
    result%assessments(2)%control_volume_id = 'CV2'
    result%assessments(2)%complete = .true.
    result%assessments(2)%admissible = .true.
    call commit_trial(state, ledger, result, ok, reason)
    call assert_true(ok .and. state%generation == 8_int64, '21 multiple conserved quantities', failures)

    call init_state(state, 220_int64, 10_int64)
    call clear_committed_ledger(ledger)
    call make_time(221_int64, 0_int64, 1_int64, target)
    call make_result(state, target, 1_int64, 1_int64, .false., .true., result, ok)
    call commit_trial(state, ledger, result, ok, reason)
    call assert_true(.not. ok .and. trim(reason) == 'ACCEPTANCE_REJECTED_OR_INCOMPLETE', &
      '22 incomplete conservation rejects', failures)

    call init_state(state, 230_int64, 10_int64)
    call clear_committed_ledger(ledger)
    call make_time(231_int64, 0_int64, 1_int64, target)
    call make_result(state, target, 5_int64, 5_int64, .true., .true., result, ok)
    call commit_trial(state, ledger, result, ok, reason)
    call assert_true(ok .and. ledger%count == 1 .and. ledger%events(1)%amount == 5_int64, &
      '23 no balancing event', failures)

    call init_state(state, 260_int64, 10_int64)
    call clear_committed_ledger(ledger)
    before = state
    call make_time(261_int64, 0_int64, 1_int64, target)
    plan1 = SyntheticAttemptPlan()
    plan1(1)%endpoint_time = target
    plan1(1)%storage_delta = 1_int64
    plan1(1)%transfer_amount = 1_int64
    plan1(1)%conservation_admissible = .false.
    call run_synthetic_interval(state, ledger, target, plan1, 1, trace, success, reason)
    call assert_true(.not. success .and. trim(reason) == 'FAILED_ACCEPTANCE_AND_RETRY_POLICY' .and. &
      states_equal(state, before), '26 failed retry policy fails', failures)

    call init_state(state, 270_int64, 10_int64)
    call clear_committed_ledger(ledger)
    before = state
    before_ledger = ledger
    call make_time(270_int64, 1_int64, 2_int64, halfway)
    call make_time(271_int64, 0_int64, 1_int64, target)
    plans2 = SyntheticAttemptPlan()
    plans2(1)%endpoint_time = halfway
    plans2(1)%storage_delta = 1_int64
    plans2(1)%transfer_amount = 1_int64
    plans2(2)%endpoint_time = target
    plans2(2)%storage_delta = 1_int64
    plans2(2)%transfer_amount = 1_int64
    call run_synthetic_interval(state, ledger, target, plans2, 1, trace, success, reason)
    call assert_true(.not. success .and. trim(reason) == 'ATTEMPT_BUDGET_EXHAUSTED' .and. &
      states_equal(state, before) .and. ledgers_equal(ledger, before_ledger), &
      '27 attempt exhaustion no publication', failures)

    call init_state(state, 280_int64, 10_int64)
    call clear_committed_ledger(ledger)
    call make_time(281_int64, 0_int64, 1_int64, target)
    call make_time(282_int64, 0_int64, 1_int64, other_time)
    plan1 = SyntheticAttemptPlan()
    plan1(1)%endpoint_time = other_time
    call run_synthetic_interval(state, ledger, target, plan1, 1, trace, success, reason)
    call assert_true(.not. success .and. trim(reason) == 'ENDPOINT_BEYOND_REQUESTED_TARGET', &
      '28 beyond target fails', failures)

    call init_state(state, 290_int64, huge(0_int64))
    call clear_committed_ledger(ledger)
    call make_time(291_int64, 0_int64, 1_int64, target)
    plan1 = SyntheticAttemptPlan()
    plan1(1)%endpoint_time = target
    plan1(1)%storage_delta = 1_int64
    call run_synthetic_interval(state, ledger, target, plan1, 1, trace, success, reason)
    call assert_true(.not. success .and. trim(reason) == 'SYNTHETIC_STATE_ARITHMETIC_UNREPRESENTABLE', &
      '29 unrepresentable state arithmetic fails', failures)

    call init_state(state, 360_int64, 10_int64)
    call clear_committed_ledger(ledger)
    before = state
    before_ledger = ledger
    call make_time(360_int64, 1_int64, 2_int64, halfway)
    call make_time(361_int64, 0_int64, 1_int64, target)
    plans2 = SyntheticAttemptPlan()
    plans2(1)%endpoint_time = halfway
    plans2(1)%storage_delta = 2_int64
    plans2(1)%transfer_amount = 2_int64
    plans2(2)%endpoint_time = target
    plans2(2)%storage_delta = 3_int64
    plans2(2)%transfer_amount = 3_int64
    plans2(2)%conservation_admissible = .false.
    call run_synthetic_interval(state, ledger, target, plans2, 2, trace, success, reason)
    call assert_true(.not. success .and. states_equal(state, before) .and. ledgers_equal(ledger, before_ledger), &
      '36 failed outer interval publishes neither state nor events', failures)

    call init_state(state, 370_int64, 10_int64)
    call clear_committed_ledger(ledger)
    call make_time(370_int64, 1_int64, 2_int64, halfway)
    call make_time(371_int64, 0_int64, 1_int64, target)
    plans2 = SyntheticAttemptPlan()
    plans2(1)%endpoint_time = halfway
    plans2(1)%storage_delta = 2_int64
    plans2(1)%transfer_amount = 2_int64
    plans2(2)%endpoint_time = target
    plans2(2)%storage_delta = 3_int64
    plans2(2)%transfer_amount = 3_int64
    call run_synthetic_interval(state, ledger, target, plans2, 2, trace, success, reason)
    call assert_true(success .and. ledger%count == 2 .and. ledger%events(1)%amount == 2_int64 .and. &
      ledger%events(2)%amount == 3_int64, '37 accepted substep events accumulate before publication', failures)

    call init_state(uninterrupted, 400_int64, 10_int64)
    split_state = uninterrupted
    call clear_committed_ledger(ledger_uninterrupted)
    call clear_committed_ledger(ledger_split)
    call make_time(401_int64, 0_int64, 1_int64, halfway)
    call make_time(402_int64, 0_int64, 1_int64, target)
    plans2 = SyntheticAttemptPlan()
    plans2(1)%endpoint_time = halfway
    plans2(1)%storage_delta = 2_int64
    plans2(1)%transfer_amount = 2_int64
    plans2(2)%endpoint_time = target
    plans2(2)%storage_delta = 3_int64
    plans2(2)%transfer_amount = 3_int64
    call run_synthetic_interval(uninterrupted, ledger_uninterrupted, target, plans2, 2, trace, success, reason)
    if (.not. success) error stop 'uninterrupted split-run fixture failed'

    plan1 = SyntheticAttemptPlan()
    plan1(1) = plans2(1)
    call run_synthetic_interval(split_state, ledger_split, halfway, plan1, 1, trace, success, reason)
    if (.not. success) error stop 'first split-run segment failed'
    call make_accepted_checkpoint(split_state, 'CP1', 'L1', 'C1', 'F1', checkpoint, ok)
    if (.not. ok) error stop 'split-run checkpoint failed'
    call restore_accepted_checkpoint(checkpoint, 'CP1', 'L1', 'C1', 'F1', restored, ok, reason)
    if (.not. ok) error stop 'split-run restore failed'
    plan1(1) = plans2(2)
    call run_synthetic_interval(restored, ledger_split, target, plan1, 1, trace, success, reason)
    call assert_true(success .and. states_equal(uninterrupted, restored) .and. &
      ledgers_equal(ledger_uninterrupted, ledger_split), '38 exact split-run restart continuation equivalence', failures)
  end subroutine run_tests

end program test_kt01_runtime
