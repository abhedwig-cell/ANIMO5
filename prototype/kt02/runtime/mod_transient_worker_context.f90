module mod_transient_worker_context
  use iso_fortran_env, only: int64
  use mod_transient_contracts, only: identity_argument_valid, TRANSIENT_ID_LEN
  implicit none
  private

  type, public :: worker_context_t
    character(len=TRANSIENT_ID_LEN) :: worker_id = ''
    character(len=TRANSIENT_ID_LEN) :: logical_model_id = ''
    character(len=TRANSIENT_ID_LEN) :: attempt_id = ''
    integer(int64) :: scratch_counter = 0_int64
    integer(int64) :: diagnostic_counter = 0_int64
  end type worker_context_t

  public :: initialize_worker_context
  public :: prepare_worker_attempt

contains

  subroutine initialize_worker_context(context, worker_id, ok)
    type(worker_context_t), intent(out) :: context
    character(len=*), intent(in) :: worker_id
    logical, intent(out) :: ok

    context = worker_context_t()
    ok = .false.
    if (.not. identity_argument_valid(worker_id)) return
    context%worker_id = trim(worker_id)
    ok = .true.
  end subroutine initialize_worker_context

  subroutine prepare_worker_attempt(context, logical_model_id, attempt_id, ok)
    type(worker_context_t), intent(inout) :: context
    character(len=*), intent(in) :: logical_model_id, attempt_id
    logical, intent(out) :: ok

    ok = .false.
    if (.not. identity_argument_valid(context%worker_id)) return
    if (.not. identity_argument_valid(logical_model_id)) return
    if (.not. identity_argument_valid(attempt_id)) return
    context%logical_model_id = trim(logical_model_id)
    context%attempt_id = trim(attempt_id)
    context%scratch_counter = 0_int64
    context%diagnostic_counter = 0_int64
    ok = .true.
  end subroutine prepare_worker_attempt

end module mod_transient_worker_context
