module mod_animo_like_client
  use iso_fortran_env, only: int64
  use mod_transient_time, only: TimeCoordinate, time_compare
  use mod_transient_contracts, only: transient_payload_t, accepted_store_t, admissibility_t
  use mod_transient_interval_runtime, only: transient_client_t
  implicit none
  private

  type, extends(transient_payload_t), public :: animo_like_payload_t
    integer(int64) :: store_a = 0_int64
    integer(int64) :: store_b = 0_int64
  contains
    procedure :: clone_payload => animo_like_clone_payload
    procedure :: is_valid => animo_like_payload_valid
  end type animo_like_payload_t

  type, extends(transient_client_t), public :: animo_like_client_t
    integer(int64) :: transfer_per_accepted_attempt = 1_int64
    logical :: reject_first_attempt = .false.
    integer :: call_count = 0
  contains
    procedure :: execute_attempt => animo_like_execute_attempt
  end type animo_like_client_t

  public :: initialize_animo_like_store

contains

  subroutine animo_like_clone_payload(self, copy)
    class(animo_like_payload_t), intent(in) :: self
    class(transient_payload_t), allocatable, intent(out) :: copy
    allocate(animo_like_payload_t :: copy)
    select type (typed => copy)
    type is (animo_like_payload_t)
      typed%store_a = self%store_a
      typed%store_b = self%store_b
    end select
  end subroutine animo_like_clone_payload

  logical function animo_like_payload_valid(self)
    class(animo_like_payload_t), intent(in) :: self
    animo_like_payload_valid = self%store_a >= 0_int64 .and. self%store_b >= 0_int64
  end function animo_like_payload_valid

  subroutine initialize_animo_like_store(store, lineage_id, time, store_a, store_b, ok)
    type(accepted_store_t), intent(out) :: store
    character(len=*), intent(in) :: lineage_id
    type(TimeCoordinate), intent(in) :: time
    integer(int64), intent(in) :: store_a, store_b
    logical, intent(out) :: ok

    store = accepted_store_t()
    ok = .false.
    if (len_trim(lineage_id) == 0 .or. len_trim(lineage_id) > len(store%lineage_id)) return
    if (store_a < 0_int64 .or. store_b < 0_int64) return
    store%lineage_id = trim(lineage_id)
    store%generation = 0_int64
    store%accepted_time = time
    allocate(animo_like_payload_t :: store%payload)
    select type (payload => store%payload)
    type is (animo_like_payload_t)
      payload%store_a = store_a
      payload%store_b = store_b
    end select
    ok = store%payload%is_valid()
  end subroutine initialize_animo_like_store

  subroutine animo_like_execute_attempt(self, origin_payload, origin_time, endpoint_time, candidate_payload, &
      admissibility, ok, reason)
    class(animo_like_client_t), intent(inout) :: self
    class(transient_payload_t), intent(in) :: origin_payload
    type(TimeCoordinate), intent(in) :: origin_time, endpoint_time
    class(transient_payload_t), allocatable, intent(out) :: candidate_payload
    type(admissibility_t), intent(out) :: admissibility
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    integer(int64) :: total_before, total_after
    integer :: ordering
    logical :: time_ok

    admissibility = admissibility_t()
    ok = .false.
    reason = 'INVALID_ORIGIN_PAYLOAD'
    self%call_count = self%call_count + 1
    call time_compare(endpoint_time, origin_time, ordering, time_ok)
    if (.not. time_ok .or. ordering <= 0) then
      reason = 'INVALID_ATTEMPT_INTERVAL'
      return
    end if

    select type (origin => origin_payload)
    type is (animo_like_payload_t)
      if (self%transfer_per_accepted_attempt < 0_int64) then
        reason = 'NEGATIVE_TRANSFER_POLICY'
        return
      end if
      if (origin%store_a < self%transfer_per_accepted_attempt) then
        reason = 'INSUFFICIENT_SOURCE_STORE'
        return
      end if
      allocate(animo_like_payload_t :: candidate_payload)
      select type (candidate => candidate_payload)
      type is (animo_like_payload_t)
        candidate%store_a = origin%store_a - self%transfer_per_accepted_attempt
        candidate%store_b = origin%store_b + self%transfer_per_accepted_attempt
        if (.not. candidate%is_valid()) then
          reason = 'INVALID_CANDIDATE'
          return
        end if
        total_before = origin%store_a + origin%store_b
        total_after = candidate%store_a + candidate%store_b
        admissibility%evidence_complete = .true.
        admissibility%admissible = total_before == total_after
      end select
    class default
      return
    end select

    if (self%reject_first_attempt .and. self%call_count == 1) admissibility%admissible = .false.
    ok = .true.
    reason = 'CALCULATED'
  end subroutine animo_like_execute_attempt

end module mod_animo_like_client
