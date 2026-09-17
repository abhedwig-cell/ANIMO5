module mod_swap_like_client
  use iso_fortran_env, only: real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  use mod_transient_time, only: TimeCoordinate, time_compare
  use mod_transient_contracts, only: transient_payload_t, admissibility_t
  use mod_transient_transactions, only: accepted_store_t, initialize_accepted_store
  use mod_transient_interval_runtime, only: transient_client_t
  implicit none
  private

  type, extends(transient_payload_t), public :: swap_like_payload_t
    real(real64) :: state_value = 0.0_real64
  contains
    procedure :: clone_payload => swap_like_clone_payload
    procedure :: is_valid => swap_like_payload_valid
  end type swap_like_payload_t

  type, extends(transient_client_t), public :: swap_like_client_t
    real(real64) :: delta_per_accepted_attempt = 1.0_real64
    logical :: reject_first_attempt = .false.
    integer :: call_count = 0
  contains
    procedure :: execute_attempt => swap_like_execute_attempt
  end type swap_like_client_t

  public :: initialize_swap_like_store

contains

  subroutine swap_like_clone_payload(self, copy)
    class(swap_like_payload_t), intent(in) :: self
    class(transient_payload_t), allocatable, intent(out) :: copy
    allocate(swap_like_payload_t :: copy)
    select type (typed => copy)
    type is (swap_like_payload_t)
      typed%state_value = self%state_value
    end select
  end subroutine swap_like_clone_payload

  logical function swap_like_payload_valid(self)
    class(swap_like_payload_t), intent(in) :: self
    swap_like_payload_valid = ieee_is_finite(self%state_value)
  end function swap_like_payload_valid

  subroutine initialize_swap_like_store(store, lineage_id, time, initial_value, ok)
    type(accepted_store_t), intent(out) :: store
    character(len=*), intent(in) :: lineage_id
    type(TimeCoordinate), intent(in) :: time
    real(real64), intent(in) :: initial_value
    logical, intent(out) :: ok
    type(swap_like_payload_t) :: payload

    ok = .false.
    if (.not. ieee_is_finite(initial_value)) return
    payload%state_value = initial_value
    call initialize_accepted_store(lineage_id, time, payload, store, ok)
  end subroutine initialize_swap_like_store

  subroutine swap_like_execute_attempt(self, origin_payload, origin_time, endpoint_time, candidate_payload, &
      admissibility, ok, reason)
    class(swap_like_client_t), intent(inout) :: self
    class(transient_payload_t), intent(in) :: origin_payload
    type(TimeCoordinate), intent(in) :: origin_time, endpoint_time
    class(transient_payload_t), allocatable, intent(out) :: candidate_payload
    type(admissibility_t), intent(out) :: admissibility
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
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
    type is (swap_like_payload_t)
      allocate(swap_like_payload_t :: candidate_payload)
      select type (candidate => candidate_payload)
      type is (swap_like_payload_t)
        candidate%state_value = origin%state_value + self%delta_per_accepted_attempt
        if (.not. candidate%is_valid()) then
          reason = 'INVALID_CANDIDATE'
          return
        end if
      end select
    class default
      return
    end select

    admissibility%evidence_complete = .true.
    admissibility%admissible = .true.
    if (self%reject_first_attempt .and. self%call_count == 1) admissibility%admissible = .false.
    ok = .true.
    reason = 'CALCULATED'
  end subroutine swap_like_execute_attempt

end module mod_swap_like_client
