module mod_transient_transactions
  use iso_fortran_env, only: int64
  use mod_transient_time, only: time_equal, time_compare, time_is_valid
  use mod_transient_contracts, only: accepted_store_t, trial_state_t, trial_result_t, &
    transient_payload_t, accepted_store_ready, identity_argument_valid
  implicit none
  private

  public :: begin_trial
  public :: commit_trial
  public :: reject_trial

contains

  subroutine begin_trial(accepted, endpoint_time, trial, ok)
    use mod_transient_time, only: TimeCoordinate
    type(accepted_store_t), intent(in) :: accepted
    type(TimeCoordinate), intent(in) :: endpoint_time
    type(trial_state_t), intent(out) :: trial
    logical, intent(out) :: ok
    integer :: ordering
    logical :: compare_ok

    trial = trial_state_t()
    ok = .false.
    if (.not. accepted_store_ready(accepted)) return
    call time_compare(endpoint_time, accepted%accepted_time, ordering, compare_ok)
    if (.not. compare_ok .or. ordering <= 0) return

    trial%origin_lineage_id = accepted%lineage_id
    trial%origin_generation = accepted%generation
    trial%origin_time = accepted%accepted_time
    trial%endpoint_time = endpoint_time
    call accepted%payload%clone_payload(trial%payload)
    if (.not. allocated(trial%payload)) return
    if (.not. trial%payload%is_valid()) then
      deallocate(trial%payload)
      return
    end if
    ok = .true.
  end subroutine begin_trial

  subroutine commit_trial(accepted, result, ok, reason)
    type(accepted_store_t), intent(inout) :: accepted
    type(trial_result_t), intent(in) :: result
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    class(transient_payload_t), allocatable :: next_payload
    logical :: equal, time_ok
    integer :: ordering

    ok = .false.
    reason = 'UNSET'

    if (.not. accepted_store_ready(accepted)) then
      reason = 'INVALID_ACCEPTED_ORIGIN'
      return
    end if
    if (.not. identity_argument_valid(result%provenance_id)) then
      reason = 'MISSING_OR_INVALID_TRIAL_PROVENANCE'
      return
    end if
    if (.not. identity_argument_valid(result%candidate%origin_lineage_id)) then
      reason = 'INVALID_CANDIDATE_ORIGIN'
      return
    end if
    if (trim(result%candidate%origin_lineage_id) /= trim(accepted%lineage_id)) then
      reason = 'LINEAGE_MISMATCH'
      return
    end if
    if (result%candidate%origin_generation /= accepted%generation) then
      reason = 'STALE_ORIGIN_GENERATION'
      return
    end if
    call time_equal(result%candidate%origin_time, accepted%accepted_time, equal, time_ok)
    if (.not. time_ok .or. .not. equal) then
      reason = 'ORIGIN_TIME_MISMATCH'
      return
    end if
    call time_compare(result%candidate%endpoint_time, accepted%accepted_time, ordering, time_ok)
    if (.not. time_ok .or. ordering <= 0) then
      reason = 'NONFORWARD_ENDPOINT'
      return
    end if
    if (.not. result%admissibility%evidence_complete .or. .not. result%admissibility%admissible) then
      reason = 'ACCEPTANCE_REJECTED_OR_INCOMPLETE'
      return
    end if
    if (.not. allocated(result%candidate%payload)) then
      reason = 'MISSING_CANDIDATE_PAYLOAD'
      return
    end if
    if (.not. result%candidate%payload%is_valid()) then
      reason = 'INVALID_CANDIDATE_PAYLOAD'
      return
    end if
    if (accepted%generation == huge(accepted%generation)) then
      reason = 'GENERATION_OVERFLOW'
      return
    end if

    call result%candidate%payload%clone_payload(next_payload)
    if (.not. allocated(next_payload)) then
      reason = 'CANDIDATE_CLONE_FAILED'
      return
    end if
    if (.not. next_payload%is_valid()) then
      deallocate(next_payload)
      reason = 'CANDIDATE_CLONE_INVALID'
      return
    end if

    if (allocated(accepted%payload)) deallocate(accepted%payload)
    call move_alloc(next_payload, accepted%payload)
    accepted%generation = accepted%generation + 1_int64
    accepted%accepted_time = result%candidate%endpoint_time

    ok = .true.
    reason = 'COMMITTED'
  end subroutine commit_trial

  subroutine reject_trial(result)
    type(trial_result_t), intent(inout) :: result
    result = trial_result_t()
  end subroutine reject_trial

end module mod_transient_transactions
