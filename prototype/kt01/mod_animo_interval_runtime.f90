! ANIMO-KT01 nonproduction prototype.
! Adapted control-structure provenance: SWAP5 src/runtime/mod_canonical_interval_runtime.f90
! @50346642bd565f79134ea17d5462e544b354998c blob 0b50dda5caf3b73a82561d7b0ba1e92386a08fee, classified PORT_WITH_ANIMO_ADAPTATION.
! Exact ANIMO time and supplied acceptance replace SWAP-specific policy and physics.
module mod_animo_interval_runtime
  use iso_fortran_env, only: int64
  use mod_animo_time_coordinate, only: TimeCoordinate, time_compare, time_equal, time_is_valid
  use mod_animo_runtime_contracts, only: AcceptedState, TrialState, TrialResult, &
    ConservationAssessment, append_transfer_event
  use mod_animo_kernel_transactions, only: begin_trial, commit_trial, checked_add_storage
  implicit none
  private

  integer, parameter, public :: MAX_RUNTIME_TRACE = 64

  type, public :: SyntheticAttemptPlan
    type(TimeCoordinate) :: endpoint_time
    integer(int64) :: storage_delta = 0_int64
    integer(int64) :: transfer_amount = 0_int64
    logical :: conservation_complete = .true.
    logical :: conservation_admissible = .true.
    logical :: retry_permitted_after_reject = .false.
  end type SyntheticAttemptPlan

  type, public :: RuntimeTrace
    integer :: attempt_count = 0
    integer :: commit_count = 0
    integer(int64) :: origin_generation(MAX_RUNTIME_TRACE) = 0_int64
    type(TimeCoordinate) :: origin_time(MAX_RUNTIME_TRACE)
    logical :: accepted_attempt(MAX_RUNTIME_TRACE) = .false.
  end type RuntimeTrace

  public :: run_synthetic_interval

contains

  subroutine run_synthetic_interval(external_accepted, requested_target, plans, max_attempts, &
      trace, success, reason)
    type(AcceptedState), intent(inout) :: external_accepted
    type(TimeCoordinate), intent(in) :: requested_target
    type(SyntheticAttemptPlan), intent(in) :: plans(:)
    integer, intent(in) :: max_attempts
    type(RuntimeTrace), intent(out) :: trace
    logical, intent(out) :: success
    character(len=*), intent(out) :: reason

    type(AcceptedState) :: working
    type(TrialState) :: trial
    type(TrialResult) :: result
    integer :: target_order, endpoint_order, endpoint_vs_target, plan_index
    logical :: ok, compare_ok, equal, event_ok, storage_ok
    character(len=64) :: commit_reason
    integer(int64) :: candidate_storage

    trace = RuntimeTrace()
    success = .false.
    reason = 'UNSET'

    if (.not. time_is_valid(external_accepted%accepted_time)) then
      reason = 'INVALID_ACCEPTED_ORIGIN_TIME'
      return
    end if
    if (.not. time_is_valid(requested_target)) then
      reason = 'INVALID_TARGET_TIME'
      return
    end if
    call time_compare(requested_target, external_accepted%accepted_time, target_order, compare_ok)
    if (.not. compare_ok .or. target_order <= 0) then
      reason = 'INVALID_INTERVAL_ORDERING'
      return
    end if
    if (max_attempts <= 0) then
      reason = 'ATTEMPT_BUDGET_EXHAUSTED'
      return
    end if

    working = external_accepted
    plan_index = 0

    do
      call time_equal(working%accepted_time, requested_target, equal, compare_ok)
      if (.not. compare_ok) then
        reason = 'TIME_COMPARISON_FAILED'
        return
      end if
      if (equal) exit

      if (trace%attempt_count >= max_attempts) then
        reason = 'ATTEMPT_BUDGET_EXHAUSTED'
        return
      end if
      if (plan_index >= size(plans)) then
        reason = 'INCOMPLETE_INTERVAL_COMPLETION'
        return
      end if
      if (trace%attempt_count >= MAX_RUNTIME_TRACE) then
        reason = 'TRACE_CAPACITY_EXHAUSTED'
        return
      end if

      plan_index = plan_index + 1
      trace%attempt_count = trace%attempt_count + 1
      trace%origin_generation(trace%attempt_count) = working%generation
      trace%origin_time(trace%attempt_count) = working%accepted_time

      call time_compare(plans(plan_index)%endpoint_time, working%accepted_time, endpoint_order, compare_ok)
      if (.not. compare_ok .or. endpoint_order <= 0) then
        reason = 'NO_OR_BACKWARD_PROGRESS'
        return
      end if
      call time_compare(plans(plan_index)%endpoint_time, requested_target, endpoint_vs_target, compare_ok)
      if (.not. compare_ok .or. endpoint_vs_target > 0) then
        reason = 'ENDPOINT_BEYOND_REQUESTED_TARGET'
        return
      end if

      call begin_trial(working, plans(plan_index)%endpoint_time, trial, ok)
      if (.not. ok) then
        reason = 'BEGIN_TRIAL_FAILED'
        return
      end if
      storage_ok = checked_add_storage(trial%synthetic_storage, plans(plan_index)%storage_delta, candidate_storage)
      if (.not. storage_ok) then
        reason = 'SYNTHETIC_STATE_ARITHMETIC_UNREPRESENTABLE'
        return
      end if
      trial%synthetic_storage = candidate_storage
      call append_transfer_event(trial%trial_journal, 'SYNTHETIC_Q', 'CV_OUTSIDE', 'CV_PRIMARY', &
        plans(plan_index)%transfer_amount, event_ok)
      if (.not. event_ok) then
        reason = 'TRIAL_JOURNAL_CAPACITY_OR_ID_FAILURE'
        return
      end if

      result = TrialResult()
      result%candidate = trial
      result%n_assessments = 1
      result%assessments(1) = ConservationAssessment( &
        quantity_id='SYNTHETIC_Q', control_volume_id='CV_PRIMARY', &
        beginning_storage=working%synthetic_storage, ending_storage=candidate_storage, &
        inbound_transfer=plans(plan_index)%transfer_amount, outbound_transfer=0_int64, &
        diagnostic_nonclosure=0_int64, complete=plans(plan_index)%conservation_complete, &
        admissible=plans(plan_index)%conservation_admissible)
      result%provenance_id = 'KT01_SYNTHETIC_ATTEMPT'

      call commit_trial(working, result, ok, commit_reason)
      if (ok) then
        trace%accepted_attempt(trace%attempt_count) = .true.
        trace%commit_count = trace%commit_count + 1
      else
        trace%accepted_attempt(trace%attempt_count) = .false.
        if (.not. plans(plan_index)%retry_permitted_after_reject) then
          reason = 'FAILED_ACCEPTANCE_AND_RETRY_POLICY'
          return
        end if
      end if
    end do

    call time_equal(working%accepted_time, requested_target, equal, compare_ok)
    if (.not. compare_ok .or. .not. equal) then
      reason = 'INCOMPLETE_INTERVAL_COMPLETION'
      return
    end if

    external_accepted = working
    success = .true.
    reason = 'INTERVAL_COMMITTED'
  end subroutine run_synthetic_interval

end module mod_animo_interval_runtime
