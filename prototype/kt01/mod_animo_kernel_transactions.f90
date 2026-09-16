! ANIMO-KT01 nonproduction prototype.
! Adapted control-structure provenance: SWAP5 src/kernel/mod_kernel_transactions.f90
! @50346642bd565f79134ea17d5462e544b354998c blob e4db4ede8162c8be877c8cad9f1babd57ba451b6, classified PORT_WITH_ANIMO_ADAPTATION.
! SWAP physical state, water acceptance and floating-time semantics are excluded.
module mod_animo_kernel_transactions
  use iso_fortran_env, only: int64
  use mod_animo_time_coordinate, only: TimeCoordinate, time_equal, time_compare, time_is_valid
  use mod_animo_runtime_contracts, only: AcceptedState, TrialState, TrialResult, &
    clear_journal, assessments_allow_commit
  implicit none
  private

  public :: begin_trial
  public :: commit_trial
  public :: reject_trial
  public :: checked_add_storage

contains

  subroutine begin_trial(accepted, endpoint_time, trial, ok)
    type(AcceptedState), intent(in) :: accepted
    type(TimeCoordinate), intent(in) :: endpoint_time
    type(TrialState), intent(out) :: trial
    logical, intent(out) :: ok
    integer :: ordering
    logical :: compare_ok

    trial = TrialState()
    ok = .false.
    if (len_trim(accepted%lineage_id) == 0) return
    if (accepted%generation < 0_int64) return
    if (.not. time_is_valid(accepted%accepted_time)) return
    call time_compare(endpoint_time, accepted%accepted_time, ordering, compare_ok)
    if (.not. compare_ok .or. ordering <= 0) return

    trial%origin_lineage_id = accepted%lineage_id
    trial%origin_generation = accepted%generation
    trial%origin_time = accepted%accepted_time
    trial%endpoint_time = endpoint_time
    trial%synthetic_storage = accepted%synthetic_storage
    call clear_journal(trial%trial_journal)
    ok = .true.
  end subroutine begin_trial

  subroutine commit_trial(accepted, result, ok, reason)
    type(AcceptedState), intent(inout) :: accepted
    type(TrialResult), intent(in) :: result
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    type(AcceptedState) :: next_state
    logical :: equal, time_ok
    integer :: ordering

    ok = .false.
    reason = 'UNSET'

    if (len_trim(accepted%lineage_id) == 0 .or. accepted%generation < 0_int64 .or. &
        .not. time_is_valid(accepted%accepted_time)) then
      reason = 'INVALID_ACCEPTED_ORIGIN'
      return
    end if
    if (len_trim(result%provenance_id) == 0) then
      reason = 'MISSING_TRIAL_PROVENANCE'
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
    if (.not. assessments_allow_commit(result)) then
      reason = 'ACCEPTANCE_REJECTED_OR_INCOMPLETE'
      return
    end if
    if (accepted%generation == huge(accepted%generation)) then
      reason = 'GENERATION_OVERFLOW'
      return
    end if

    next_state = accepted
    next_state%generation = accepted%generation + 1_int64
    next_state%accepted_time = result%candidate%endpoint_time
    next_state%synthetic_storage = result%candidate%synthetic_storage
    next_state%committed_journal = result%candidate%trial_journal

    accepted = next_state
    ok = .true.
    reason = 'COMMITTED'
  end subroutine commit_trial

  subroutine reject_trial(result)
    type(TrialResult), intent(inout) :: result

    result = TrialResult()
  end subroutine reject_trial

  logical function checked_add_storage(base, delta, value)
    integer(int64), intent(in) :: base, delta
    integer(int64), intent(out) :: value

    value = 0_int64
    checked_add_storage = .false.
    if (delta > 0_int64) then
      if (base > huge(base) - delta) return
    else if (delta < 0_int64) then
      if (base < -huge(base) - delta - 1_int64) return
    end if
    value = base + delta
    checked_add_storage = .true.
  end function checked_add_storage

end module mod_animo_kernel_transactions
