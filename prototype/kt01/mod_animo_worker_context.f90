! ANIMO-KT01 nonproduction prototype.
! Structural derivation provenance: SWAP5 src/runtime/mod_a23bu_worker_execution_context.f90
! @50346642bd565f79134ea17d5462e544b354998c blob f96a66c0185d96ba48258f8560db275fa7fed58c, classified DESIGN_ONLY.
! Only worker-owned reset/isolation mechanics are retained.
module mod_animo_worker_context
  use iso_fortran_env, only: int64
  implicit none
  private

  integer, parameter :: ID_LEN = 48

  type, public :: WorkerContext
    character(len=ID_LEN) :: worker_id = ''
    character(len=ID_LEN) :: logical_model_id = ''
    character(len=ID_LEN) :: attempt_id = ''
    integer(int64) :: scratch_value = 0_int64
    integer(int64) :: attempt_diagnostic_counter = 0_int64
  end type WorkerContext

  public :: initialize_worker_context
  public :: prepare_worker_attempt

contains

  logical function identity_argument_valid(value)
    character(len=*), intent(in) :: value
    integer :: n

    n = len_trim(value)
    identity_argument_valid = n > 0 .and. n <= ID_LEN
  end function identity_argument_valid

  subroutine initialize_worker_context(context, worker_id, ok)
    type(WorkerContext), intent(out) :: context
    character(len=*), intent(in) :: worker_id
    logical, intent(out) :: ok

    context = WorkerContext()
    ok = .false.
    if (.not. identity_argument_valid(worker_id)) return
    context%worker_id = trim(worker_id)
    ok = .true.
  end subroutine initialize_worker_context

  subroutine prepare_worker_attempt(context, logical_model_id, attempt_id, ok)
    type(WorkerContext), intent(inout) :: context
    character(len=*), intent(in) :: logical_model_id, attempt_id
    logical, intent(out) :: ok

    ok = .false.
    if (len_trim(context%worker_id) == 0) return
    if (.not. identity_argument_valid(logical_model_id)) return
    if (.not. identity_argument_valid(attempt_id)) return

    context%logical_model_id = trim(logical_model_id)
    context%attempt_id = trim(attempt_id)
    context%scratch_value = 0_int64
    context%attempt_diagnostic_counter = 0_int64
    ok = .true.
  end subroutine prepare_worker_attempt

end module mod_animo_worker_context
