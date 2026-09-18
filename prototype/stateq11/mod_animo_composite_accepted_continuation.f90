module mod_animo_composite_accepted_continuation
  use iso_fortran_env, only: int64, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  use mod_transient_time, only: TimeCoordinate, time_equal, time_compare, time_is_valid
  use mod_transient_contracts, only: identity_argument_valid, TRANSIENT_ID_LEN
  use mod_transient_transactions, only: accepted_store_t, accepted_store_ready, &
    accepted_store_generation, accepted_store_lineage, accepted_store_time
  use mod_animo_detailed_hydrology_origin_state, only: &
    detailed_hydrology_origin_state_t, make_detailed_hydrology_origin_state, &
    advance_origin_from_accepted_endpoint, validate_detailed_hydrology_origin_state
  use mod_animo_first_detailed_hydrology_origin, only: &
    first_detailed_hydrology_origin_t, validate_first_detailed_hydrology_origin
  use mod_animo_static_boundary_year_binding, only: &
    boundary_year_cursor_t, BOUNDQ02_CURSOR_SCHEMA
  implicit none
  private

  character(len=*), parameter, public :: COMPOSITE_CONTINUATION_SCHEMA = &
    'ANIMO_TCD042_COMPOSITE_ACCEPTED_CONTINUATION_V1'

  type, public :: composite_accepted_continuation_t
    character(len=64) :: schema_id = ''
    character(len=TRANSIENT_ID_LEN) :: lineage_id = ''
    integer(int64) :: generation = -1_int64
    type(TimeCoordinate) :: accepted_time
    type(detailed_hydrology_origin_state_t) :: hydrology_origin
    real(real64) :: runinu_call_entry = 0.0_real64
    type(boundary_year_cursor_t) :: boundary_cursor
  end type composite_accepted_continuation_t

  public :: initialize_composite_from_first_origin
  public :: initialize_composite_continuation
  public :: prepare_next_composite_continuation
  public :: validate_composite_continuation
  public :: validate_composite_against_accepted_store

contains

  subroutine initialize_composite_from_first_origin(lineage_id, accepted_time, first_origin, &
      runinu_call_entry, boundary_cursor, continuation, ok, reason)
    character(len=*), intent(in) :: lineage_id
    type(TimeCoordinate), intent(in) :: accepted_time
    type(first_detailed_hydrology_origin_t), intent(in) :: first_origin
    real(real64), intent(in) :: runinu_call_entry
    type(boundary_year_cursor_t), intent(in) :: boundary_cursor
    type(composite_accepted_continuation_t), intent(out) :: continuation
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    type(detailed_hydrology_origin_state_t) :: origin
    character(len=128) :: local_reason

    continuation = composite_accepted_continuation_t()
    ok = .false.
    reason = 'UNSET'

    call validate_first_detailed_hydrology_origin(first_origin, ok, local_reason)
    if (.not. ok) then
      reason = 'INVALID_STATEQ10_FIRST_ORIGIN'
      return
    end if

    call make_detailed_hydrology_origin_state(first_origin%pn, first_origin%sic, &
      first_origin%snla, first_origin%mofro, origin, ok, local_reason)
    if (.not. ok) then
      reason = 'STATEQ10_TO_STATEQ09_ORIGIN_CONVERSION_FAILED'
      return
    end if

    call initialize_composite_continuation(lineage_id, accepted_time, origin, &
      runinu_call_entry, boundary_cursor, continuation, ok, reason)
  end subroutine initialize_composite_from_first_origin

  subroutine initialize_composite_continuation(lineage_id, accepted_time, hydrology_origin, &
      runinu_call_entry, boundary_cursor, continuation, ok, reason)
    character(len=*), intent(in) :: lineage_id
    type(TimeCoordinate), intent(in) :: accepted_time
    type(detailed_hydrology_origin_state_t), intent(in) :: hydrology_origin
    real(real64), intent(in) :: runinu_call_entry
    type(boundary_year_cursor_t), intent(in) :: boundary_cursor
    type(composite_accepted_continuation_t), intent(out) :: continuation
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    continuation = composite_accepted_continuation_t()
    continuation%schema_id = COMPOSITE_CONTINUATION_SCHEMA
    continuation%lineage_id = lineage_id
    continuation%generation = 0_int64
    continuation%accepted_time = accepted_time
    continuation%hydrology_origin = hydrology_origin
    continuation%runinu_call_entry = runinu_call_entry
    continuation%boundary_cursor = boundary_cursor

    call validate_composite_continuation(continuation, ok, reason)
  end subroutine initialize_composite_continuation

  subroutine prepare_next_composite_continuation(current, endpoint_time, pnt, sict, snt, &
      mofrt, runinu_next, next_boundary_cursor, candidate, ok, reason)
    type(composite_accepted_continuation_t), intent(in) :: current
    type(TimeCoordinate), intent(in) :: endpoint_time
    real(real64), intent(in) :: pnt, sict, snt
    real(real64), intent(in) :: mofrt(:)
    real(real64), intent(in) :: runinu_next
    type(boundary_year_cursor_t), intent(in) :: next_boundary_cursor
    type(composite_accepted_continuation_t), intent(out) :: candidate
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    type(detailed_hydrology_origin_state_t) :: next_origin
    integer :: ordering
    logical :: compare_ok
    character(len=128) :: local_reason

    candidate = composite_accepted_continuation_t()
    ok = .false.
    reason = 'UNSET'

    call validate_composite_continuation(current, ok, local_reason)
    if (.not. ok) then
      reason = 'INVALID_CURRENT_COMPOSITE_CONTINUATION'
      return
    end if
    ok = .false.

    call time_compare(endpoint_time, current%accepted_time, ordering, compare_ok)
    if (.not. compare_ok .or. ordering <= 0) then
      reason = 'NONFORWARD_COMPOSITE_ENDPOINT'
      return
    end if
    if (current%generation == huge(current%generation)) then
      reason = 'COMPOSITE_GENERATION_OVERFLOW'
      return
    end if
    if (.not. ieee_is_finite(runinu_next)) then
      reason = 'NONFINITE_NEXT_RUNINU_CONTINUATION'
      return
    end if
    if (trim(next_boundary_cursor%schema_id) /= BOUNDQ02_CURSOR_SCHEMA) then
      reason = 'NEXT_BOUNDARY_CURSOR_SCHEMA_MISMATCH'
      return
    end if
    if (.not. next_boundary_cursor%initialized .or. &
        next_boundary_cursor%active_year <= 0 .or. next_boundary_cursor%active_slot <= 0) then
      reason = 'NEXT_BOUNDARY_CURSOR_NOT_ACCEPTABLE'
      return
    end if

    call advance_origin_from_accepted_endpoint(pnt, sict, snt, mofrt, &
      next_origin, ok, local_reason)
    if (.not. ok) then
      reason = 'STATEQ09_ENDPOINT_TO_ORIGIN_TRANSFER_FAILED'
      return
    end if

    candidate%schema_id = COMPOSITE_CONTINUATION_SCHEMA
    candidate%lineage_id = current%lineage_id
    candidate%generation = current%generation + 1_int64
    candidate%accepted_time = endpoint_time
    candidate%hydrology_origin = next_origin
    candidate%runinu_call_entry = runinu_next
    candidate%boundary_cursor = next_boundary_cursor

    call validate_composite_continuation(candidate, ok, local_reason)
    if (.not. ok) then
      reason = trim(local_reason)
      return
    end if

    reason = 'COMPOSITE_CONTINUATION_CANDIDATE_READY'
  end subroutine prepare_next_composite_continuation

  subroutine validate_composite_continuation(value, ok, reason)
    type(composite_accepted_continuation_t), intent(in) :: value
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    logical :: origin_ok
    character(len=128) :: local_reason

    ok = .false.
    reason = 'UNSET'

    if (trim(value%schema_id) /= COMPOSITE_CONTINUATION_SCHEMA) then
      reason = 'COMPOSITE_CONTINUATION_SCHEMA_MISMATCH'
      return
    end if
    if (.not. identity_argument_valid(value%lineage_id)) then
      reason = 'INVALID_COMPOSITE_LINEAGE'
      return
    end if
    if (value%generation < 0_int64) then
      reason = 'INVALID_COMPOSITE_GENERATION'
      return
    end if
    if (.not. time_is_valid(value%accepted_time)) then
      reason = 'INVALID_COMPOSITE_ACCEPTED_TIME'
      return
    end if

    call validate_detailed_hydrology_origin_state(value%hydrology_origin, origin_ok, local_reason)
    if (.not. origin_ok) then
      reason = 'INVALID_COMPOSITE_HYDROLOGY_ORIGIN'
      return
    end if
    if (.not. ieee_is_finite(value%runinu_call_entry)) then
      reason = 'NONFINITE_COMPOSITE_RUNINU_CONTINUATION'
      return
    end if

    if (trim(value%boundary_cursor%schema_id) /= BOUNDQ02_CURSOR_SCHEMA) then
      reason = 'COMPOSITE_BOUNDARY_CURSOR_SCHEMA_MISMATCH'
      return
    end if
    if (value%boundary_cursor%initialized) then
      if (value%boundary_cursor%active_year <= 0 .or. value%boundary_cursor%active_slot <= 0) then
        reason = 'INVALID_INITIALIZED_COMPOSITE_BOUNDARY_CURSOR'
        return
      end if
    else
      if (value%boundary_cursor%active_year /= 0 .or. value%boundary_cursor%active_slot /= 0) then
        reason = 'UNINITIALIZED_CURSOR_HAS_ACTIVE_IDENTITY'
        return
      end if
    end if

    ok = .true.
    reason = 'VALID_COMPOSITE_ACCEPTED_CONTINUATION'
  end subroutine validate_composite_continuation

  subroutine validate_composite_against_accepted_store(value, store, ok, reason)
    type(composite_accepted_continuation_t), intent(in) :: value
    type(accepted_store_t), intent(in) :: store
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    type(TimeCoordinate) :: store_time
    character(len=TRANSIENT_ID_LEN) :: store_lineage
    logical :: value_ok, equal, compare_ok

    ok = .false.
    reason = 'UNSET'

    call validate_composite_continuation(value, value_ok, reason)
    if (.not. value_ok) return
    if (.not. accepted_store_ready(store)) then
      reason = 'INVALID_ACCEPTED_STORE_FOR_COMPOSITE_BINDING'
      return
    end if

    store_lineage = accepted_store_lineage(store)
    if (trim(value%lineage_id) /= trim(store_lineage)) then
      reason = 'COMPOSITE_LINEAGE_MISMATCH'
      return
    end if
    if (value%generation /= accepted_store_generation(store)) then
      reason = 'COMPOSITE_GENERATION_MISMATCH'
      return
    end if

    call accepted_store_time(store, store_time, value_ok)
    if (.not. value_ok) then
      reason = 'ACCEPTED_STORE_TIME_UNAVAILABLE'
      return
    end if
    call time_equal(value%accepted_time, store_time, equal, compare_ok)
    if (.not. compare_ok .or. .not. equal) then
      reason = 'COMPOSITE_ACCEPTED_TIME_MISMATCH'
      return
    end if

    ok = .true.
    reason = 'COMPOSITE_CONTINUATION_MATCHES_ACCEPTED_STORE'
  end subroutine validate_composite_against_accepted_store

end module mod_animo_composite_accepted_continuation
