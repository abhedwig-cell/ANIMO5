module mod_transient_interval_runtime
  use iso_fortran_env, only: int64
  use mod_transient_time, only: TimeCoordinate, time_compare, time_equal, time_is_valid
  use mod_transient_contracts, only: accepted_store_t, trial_state_t, trial_result_t, &
    transient_payload_t, admissibility_t, accepted_store_ready, TRANSIENT_ID_LEN
  use mod_transient_transactions, only: begin_trial, commit_trial
  implicit none
  private

  integer, parameter, public :: MAX_RUNTIME_TRACE = 64

  type, public :: attempt_request_t
    type(TimeCoordinate) :: endpoint_time
    logical :: retry_permitted_after_reject = .false.
  end type attempt_request_t

  type, public :: runtime_trace_t
    integer :: attempt_count = 0
    integer :: commit_count = 0
    integer(int64) :: origin_generation(MAX_RUNTIME_TRACE) = 0_int64
    type(TimeCoordinate) :: origin_time(MAX_RUNTIME_TRACE)
    logical :: accepted_attempt(MAX_RUNTIME_TRACE) = .false.
  end type runtime_trace_t

  type, abstract, public :: transient_client_t
  contains
    procedure(execute_attempt_iface), deferred :: execute_attempt
  end type transient_client_t

  abstract interface
    subroutine execute_attempt_iface(self, origin_payload, origin_time, endpoint_time, candidate_payload, &
        admissibility, ok, reason)
      import :: transient_client_t, transient_payload_t, TimeCoordinate, admissibility_t
      class(transient_client_t), intent(inout) :: self
      class(transient_payload_t), intent(in) :: origin_payload
      type(TimeCoordinate), intent(in) :: origin_time, endpoint_time
      class(transient_payload_t), allocatable, intent(out) :: candidate_payload
      type(admissibility_t), intent(out) :: admissibility
      logical, intent(out) :: ok
      character(len=*), intent(out) :: reason
    end subroutine execute_attempt_iface
  end interface

  public :: run_interval

contains

  subroutine run_interval(external_accepted, client, requested_target, requests, max_attempts, trace, success, reason)
    type(accepted_store_t), intent(inout) :: external_accepted
    class(transient_client_t), intent(inout) :: client
    type(TimeCoordinate), intent(in) :: requested_target
    type(attempt_request_t), intent(in) :: requests(:)
    integer, intent(in) :: max_attempts
    type(runtime_trace_t), intent(out) :: trace
    logical, intent(out) :: success
    character(len=*), intent(out) :: reason

    type(accepted_store_t) :: working
    type(trial_state_t) :: trial
    type(trial_result_t) :: result
    class(transient_payload_t), allocatable :: candidate_payload
    type(admissibility_t) :: admissibility
    integer :: target_order, endpoint_order, endpoint_vs_target, request_index
    logical :: ok, compare_ok, equal, client_ok
    character(len=TRANSIENT_ID_LEN) :: commit_reason, client_reason

    trace = runtime_trace_t()
    success = .false.
    reason = 'UNSET'

    if (.not. accepted_store_ready(external_accepted)) then
      reason = 'INVALID_ACCEPTED_ORIGIN'
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
    request_index = 0

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
      if (request_index >= size(requests)) then
        reason = 'INCOMPLETE_INTERVAL_COMPLETION'
        return
      end if
      if (trace%attempt_count >= MAX_RUNTIME_TRACE) then
        reason = 'TRACE_CAPACITY_EXHAUSTED'
        return
      end if

      request_index = request_index + 1
      trace%attempt_count = trace%attempt_count + 1
      trace%origin_generation(trace%attempt_count) = working%generation
      trace%origin_time(trace%attempt_count) = working%accepted_time

      call time_compare(requests(request_index)%endpoint_time, working%accepted_time, endpoint_order, compare_ok)
      if (.not. compare_ok .or. endpoint_order <= 0) then
        reason = 'NO_OR_BACKWARD_PROGRESS'
        return
      end if
      call time_compare(requests(request_index)%endpoint_time, requested_target, endpoint_vs_target, compare_ok)
      if (.not. compare_ok .or. endpoint_vs_target > 0) then
        reason = 'ENDPOINT_BEYOND_REQUESTED_TARGET'
        return
      end if

      call begin_trial(working, requests(request_index)%endpoint_time, trial, ok)
      if (.not. ok) then
        reason = 'BEGIN_TRIAL_FAILED'
        return
      end if

      call client%execute_attempt(trial%payload, trial%origin_time, trial%endpoint_time, candidate_payload, &
        admissibility, client_ok, client_reason)
      if (.not. client_ok .or. .not. allocated(candidate_payload)) then
        reason = 'CLIENT_ATTEMPT_FAILED'
        return
      end if

      if (allocated(trial%payload)) deallocate(trial%payload)
      call move_alloc(candidate_payload, trial%payload)

      result = trial_result_t()
      result%candidate = trial
      result%admissibility = admissibility
      result%provenance_id = 'KT02_SHARED_CLIENT_ATTEMPT'

      call commit_trial(working, result, ok, commit_reason)
      if (ok) then
        trace%accepted_attempt(trace%attempt_count) = .true.
        trace%commit_count = trace%commit_count + 1
      else
        trace%accepted_attempt(trace%attempt_count) = .false.
        if (trim(commit_reason) /= 'ACCEPTANCE_REJECTED_OR_INCOMPLETE') then
          reason = 'TRANSACTION_COMMIT_FAILED'
          return
        end if
        if (.not. requests(request_index)%retry_permitted_after_reject) then
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
  end subroutine run_interval

end module mod_transient_interval_runtime
