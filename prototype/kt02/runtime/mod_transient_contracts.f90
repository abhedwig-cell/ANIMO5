module mod_transient_contracts
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

  type, public :: admissibility_t
    logical :: evidence_complete = .false.
    logical :: admissible = .false.
  end type admissibility_t

  public :: identity_argument_valid

contains

  logical function identity_argument_valid(value)
    character(len=*), intent(in) :: value
    integer :: n
    n = len_trim(value)
    identity_argument_valid = n > 0 .and. n <= TRANSIENT_ID_LEN
  end function identity_argument_valid

end module mod_transient_contracts
