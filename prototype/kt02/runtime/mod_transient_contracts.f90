module mod_transient_contracts
  use iso_fortran_env, only: int64
  use mod_transient_time, only: TimeCoordinate, time_is_valid
  implicit none
  private

  integer, parameter, public :: TRANSIENT_ID_LEN = 48

  type, abstract, public :: transient_payload_t
  contains
    procedure(clone_payload_iface), deferred :: clone_payload
    procedure(payload_valid_iface), deferred :: is_valid
  end type transient_payload_t

  abstract interface
    subroutine clone_payload_iface(self, copy)
      import :: transient_payload_t
      class(transient_payload_t), intent(in) :: self
      class(transient_payload_t), allocatable, intent(out) :: copy
    end subroutine clone_payload_iface

    logical function payload_valid_iface(self)
      import :: transient_payload_t
      class(transient_payload_t), intent(in) :: self
    end function payload_valid_iface
  end interface

  type, public :: accepted_store_t
    character(len=TRANSIENT_ID_LEN) :: lineage_id = ''
    integer(int64) :: generation = 0_int64
    type(TimeCoordinate) :: accepted_time
    class(transient_payload_t), allocatable :: payload
  end type accepted_store_t

  type, public :: trial_state_t
    character(len=TRANSIENT_ID_LEN) :: origin_lineage_id = ''
    integer(int64) :: origin_generation = 0_int64
    type(TimeCoordinate) :: origin_time
    type(TimeCoordinate) :: endpoint_time
    class(transient_payload_t), allocatable :: payload
  end type trial_state_t

  type, public :: admissibility_t
    logical :: evidence_complete = .false.
    logical :: admissible = .false.
  end type admissibility_t

  type, public :: trial_result_t
    type(trial_state_t) :: candidate
    type(admissibility_t) :: admissibility
    character(len=TRANSIENT_ID_LEN) :: provenance_id = ''
  end type trial_result_t

  public :: accepted_store_ready
  public :: identity_argument_valid

contains

  logical function identity_argument_valid(value)
    character(len=*), intent(in) :: value
    integer :: n
    n = len_trim(value)
    identity_argument_valid = n > 0 .and. n <= TRANSIENT_ID_LEN
  end function identity_argument_valid

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

end module mod_transient_contracts
