module mod_transient_transactions
  use iso_fortran_env, only: int64
  use mod_transient_time, only: TimeCoordinate, time_equal, time_compare, time_is_valid
  use mod_transient_contracts, only: transient_payload_t, admissibility_t, &
    identity_argument_valid, TRANSIENT_ID_LEN
  implicit none
  private

  type, public :: accepted_store_t
    private
    character(len=TRANSIENT_ID_LEN) :: lineage_id = ''
    integer(int64) :: generation = 0_int64
    type(TimeCoordinate) :: accepted_time
    class(transient_payload_t), allocatable :: payload
  end type accepted_store_t

  type, public :: trial_state_t
    private
    character(len=TRANSIENT_ID_LEN) :: origin_lineage_id = ''
    integer(int64) :: origin_generation = 0_int64
    type(TimeCoordinate) :: origin_time
    type(TimeCoordinate) :: endpoint_time
    class(transient_payload_t), allocatable :: payload
  end type trial_state_t

  type, public :: trial_result_t
    private
    type(trial_state_t) :: candidate
    type(admissibility_t) :: admissibility
    character(len=TRANSIENT_ID_LEN) :: provenance_id = ''
  end type trial_result_t

  public :: initialize_accepted_store
  public :: reconstruct_accepted_store_trusted
  public :: accepted_store_ready
  public :: accepted_store_generation
  public :: accepted_store_lineage
  public :: accepted_store_time
  public :: snapshot_accepted_payload
  public :: begin_trial
  public :: snapshot_trial_payload
  public :: make_trial_result
  public :: commit_trial
  public :: reject_trial

contains

  subroutine initialize_accepted_store(lineage_id, accepted_time, payload, store, ok)
    character(len=*), intent(in) :: lineage_id
    type(TimeCoordinate), intent(in) :: accepted_time
    class(transient_payload_t), intent(in) :: payload
    type(accepted_store_t), intent(out) :: store
    logical, intent(out) :: ok
    class(transient_payload_t), allocatable :: payload_copy

    store = accepted_store_t()
    ok = .false.
    if (.not. identity_argument_valid(lineage_id)) return
    if (.not. time_is_valid(accepted_time)) return
    if (.not. payload%is_valid()) return
    call payload%clone_payload(payload_copy)
    if (.not. allocated(payload_copy)) return
    if (.not. payload_copy%is_valid()) then
      deallocate(payload_copy)
      return
    end if

    store%lineage_id = trim(lineage_id)
    store%generation = 0_int64
    store%accepted_time = accepted_time
    call move_alloc(payload_copy, store%payload)
    ok = .true.
  end subroutine initialize_accepted_store

  subroutine reconstruct_accepted_store_trusted(lineage_id, generation, accepted_time, payload, store, ok)
    character(len=*), intent(in) :: lineage_id
    integer(int64), intent(in) :: generation
    type(TimeCoordinate), intent(in) :: accepted_time
    class(transient_payload_t), intent(in) :: payload
    type(accepted_store_t), intent(out) :: store
    logical, intent(out) :: ok
    class(transient_payload_t), allocatable :: payload_copy

    store = accepted_store_t()
    ok = .false.
    if (.not. identity_argument_valid(lineage_id)) return
    if (generation < 0_int64) return
    if (.not. time_is_valid(accepted_time)) return
    if (.not. payload%is_valid()) return
    call payload%clone_payload(payload_copy)
    if (.not. allocated(payload_copy)) return
    if (.not. payload_copy%is_valid()) then
      deallocate(payload_copy)
      return
    end if

    store%lineage_id = trim(lineage_id)
    store%generation = generation
    store%accepted_time = accepted_time
    call move_alloc(payload_copy, store%payload)
    ok = .true.
  end subroutine reconstruct_accepted_store_trusted

  logical function accepted_store_ready(store)
    type(accepted_store_t), intent(in) :: store
    accepted_store_ready = .false.
    if (.not. identity_argument_valid(store%lineage_id)) return
    if (store%generation < 0_int64) return
    if (.not. time_is_valid(store%accepted_time)) return
    if (.not. allocated(store%payload)) return
    if (.not. store%payload%is_valid()) return
    accepted_store_ready = .true.
  end function accepted_store_ready

  integer(int64) function accepted_store_generation(store) result(value)
    type(accepted_store_t), intent(in) :: store
    value = store%generation
  end function accepted_store_generation

  function accepted_store_lineage(store) result(value)
    type(accepted_store_t), intent(in) :: store
    character(len=TRANSIENT_ID_LEN) :: value
    value = store%lineage_id
  end function accepted_store_lineage

  subroutine accepted_store_time(store, value, ok)
    type(accepted_store_t), intent(in) :: store
    type(TimeCoordinate), intent(out) :: value
    logical, intent(out) :: ok
    value = TimeCoordinate()
    ok = accepted_store_ready(store)
    if (ok) value = store%accepted_time
  end subroutine accepted_store_time

  subroutine snapshot_accepted_payload(store, copy, ok)
    type(accepted_store_t), intent(in) :: store
    class(transient_payload_t), allocatable, intent(out) :: copy
    logical, intent(out) :: ok
    ok = accepted_store_ready(store)
    if (.not. ok) return
    call store%payload%clone_payload(copy)
    ok = allocated(copy)
    if (ok) ok = copy%is_valid()
    if (.not. ok .and. allocated(copy)) deallocate(copy)
  end subroutine snapshot_accepted_payload

  subroutine begin_trial(accepted, endpoint_time, trial, ok)
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

  subroutine snapshot_trial_payload(trial, copy, ok)
    type(trial_state_t), intent(in) :: trial
    class(transient_payload_t), allocatable, intent(out) :: copy
    logical, intent(out) :: ok
    ok = allocated(trial%payload)
    if (.not. ok) return
    if (.not. trial%payload%is_valid()) then
      ok = .false.
      return
    end if
    call trial%payload%clone_payload(copy)
    ok = allocated(copy)
    if (ok) ok = copy%is_valid()
    if (.not. ok .and. allocated(copy)) deallocate(copy)
  end subroutine snapshot_trial_payload

  subroutine make_trial_result(trial, candidate_payload, admissibility, provenance_id, result, ok)
    type(trial_state_t), intent(in) :: trial
    class(transient_payload_t), intent(in) :: candidate_payload
    type(admissibility_t), intent(in) :: admissibility
    character(len=*), intent(in) :: provenance_id
    type(trial_result_t), intent(out) :: result
    logical, intent(out) :: ok
    class(transient_payload_t), allocatable :: payload_copy

    result = trial_result_t()
    ok = .false.
    if (.not. identity_argument_valid(trial%origin_lineage_id)) return
    if (trial%origin_generation < 0_int64) return
    if (.not. time_is_valid(trial%origin_time) .or. .not. time_is_valid(trial%endpoint_time)) return
    if (.not. allocated(trial%payload) .or. .not. trial%payload%is_valid()) return
    if (.not. identity_argument_valid(provenance_id)) return
    if (.not. candidate_payload%is_valid()) return

    call candidate_payload%clone_payload(payload_copy)
    if (.not. allocated(payload_copy)) return
    if (.not. payload_copy%is_valid()) then
      deallocate(payload_copy)
      return
    end if

    result%candidate = trial
    if (allocated(result%candidate%payload)) deallocate(result%candidate%payload)
    call move_alloc(payload_copy, result%candidate%payload)
    result%admissibility = admissibility
    result%provenance_id = trim(provenance_id)
    ok = .true.
  end subroutine make_trial_result

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
