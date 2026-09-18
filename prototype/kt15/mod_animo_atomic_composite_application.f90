module mod_animo_atomic_composite_application
  use iso_fortran_env, only: int64, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  use mod_transient_time, only: TimeCoordinate
  use mod_transient_contracts, only: transient_payload_t
  use mod_transient_transactions, only: accepted_store_t, accepted_store_ready, &
    accepted_store_generation, accepted_store_time, snapshot_accepted_payload
  use mod_animo_hydrology_adapter, only: hydrology_step_t
  use mod_animo_bounded_no_ponding_upper_hydrology, only: &
    hydroexec01_start_context_t, make_hydroexec01_start_context
  use mod_animo_static_boundary_chemistry_adapter, only: static_boundary_chemistry_t
  use mod_animo_static_boundary_year_binding, only: boundary_year_cursor_t
  use mod_animo_immutable_static_boundary_frame, only: &
    immutable_static_boundary_interval_frame_t, make_immutable_static_boundary_interval_frame
  use mod_animo_tcd042_boundary_frame_composition, only: &
    kt14_composition_trace_t, execute_boundary_frame_tcd042_interval
  use mod_animo_composite_accepted_continuation, only: &
    composite_accepted_continuation_t, validate_composite_continuation, &
    validate_composite_against_accepted_store, prepare_next_composite_continuation
  implicit none
  private

  character(len=*), parameter, public :: KT15_APPLICATION_SCHEMA = &
    'ANIMO_KT15_ATOMIC_COMPOSITE_APPLICATION_V1'

  type, public :: kt15_static_hydrology_config_t
    real(real64) :: he_top = 0.0_real64
    real(real64) :: lefrrv = 0.0_real64
    real(real64) :: lefrso = 0.0_real64
  end type kt15_static_hydrology_config_t

  type, public :: kt15_application_state_t
    private
    character(len=64) :: schema_id = ''
    type(accepted_store_t) :: science_store
    type(composite_accepted_continuation_t) :: continuation
  end type kt15_application_state_t

  type, public :: kt15_atomic_trace_t
    logical :: origin_coherent = .false.
    logical :: boundary_bound = .false.
    logical :: working_science_committed = .false.
    logical :: next_continuation_ready = .false.
    logical :: external_group_published = .false.
    character(len=64) :: boundary_content_sha256 = ''
    integer(int64) :: origin_generation = -1_int64
    integer(int64) :: published_generation = -1_int64
    integer :: selected_boundary_year = 0
    integer :: selected_boundary_slot = 0
    type(kt14_composition_trace_t) :: composition
  end type kt15_atomic_trace_t

  public :: initialize_kt15_application_state
  public :: validate_kt15_application_state
  public :: execute_kt15_atomic_interval
  public :: kt15_application_generation
  public :: kt15_application_time
  public :: snapshot_kt15_science_payload
  public :: snapshot_kt15_continuation

contains

  subroutine initialize_kt15_application_state(science_store, continuation, state, ok, reason)
    type(accepted_store_t), intent(in) :: science_store
    type(composite_accepted_continuation_t), intent(in) :: continuation
    type(kt15_application_state_t), intent(out) :: state
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    state = kt15_application_state_t()
    ok = .false.
    reason = 'UNSET'

    call validate_composite_against_accepted_store(continuation, science_store, ok, reason)
    if (.not. ok) then
      reason = 'KT15_INITIAL_SCIENCE_CONTINUATION_INCOHERENT'
      return
    end if

    state%schema_id = KT15_APPLICATION_SCHEMA
    state%science_store = science_store
    state%continuation = continuation
    call validate_kt15_application_state(state, ok, reason)
    if (ok) reason = 'KT15_APPLICATION_STATE_INITIALIZED'
  end subroutine initialize_kt15_application_state

  subroutine validate_kt15_application_state(state, ok, reason)
    type(kt15_application_state_t), intent(in) :: state
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    ok = .false.
    reason = 'UNSET'

    if (trim(state%schema_id) /= KT15_APPLICATION_SCHEMA) then
      reason = 'KT15_APPLICATION_SCHEMA_MISMATCH'
      return
    end if
    if (.not. accepted_store_ready(state%science_store)) then
      reason = 'KT15_INVALID_SCIENCE_STORE'
      return
    end if
    call validate_composite_against_accepted_store(state%continuation, state%science_store, ok, reason)
    if (.not. ok) then
      reason = 'KT15_SCIENCE_CONTINUATION_INCOHERENT'
      return
    end if

    ok = .true.
    reason = 'VALID_KT15_APPLICATION_STATE'
  end subroutine validate_kt15_application_state

  subroutine execute_kt15_atomic_interval(state, selected_packet, runtime_calendar_contract_id, &
      producer_day_offset, endpoint_time, execution_id, static_hydrology, boundary, &
      boundary_content_sha256, simulation_start_year, load_channel, trace, success, reason)
    type(kt15_application_state_t), intent(inout) :: state
    type(hydrology_step_t), intent(in) :: selected_packet
    character(len=*), intent(in) :: runtime_calendar_contract_id
    integer(int64), intent(in) :: producer_day_offset
    type(TimeCoordinate), intent(in) :: endpoint_time
    character(len=*), intent(in) :: execution_id
    type(kt15_static_hydrology_config_t), intent(in) :: static_hydrology
    type(static_boundary_chemistry_t), intent(in) :: boundary
    character(len=*), intent(in) :: boundary_content_sha256
    integer, intent(in) :: simulation_start_year
    integer, intent(in) :: load_channel
    type(kt15_atomic_trace_t), intent(out) :: trace
    logical, intent(out) :: success
    character(len=*), intent(out) :: reason

    type(kt15_application_state_t) :: working
    type(composite_accepted_continuation_t) :: next_continuation
    type(immutable_static_boundary_interval_frame_t) :: boundary_frame
    type(boundary_year_cursor_t) :: next_cursor
    type(hydroexec01_start_context_t) :: start_context
    type(TimeCoordinate) :: origin_time
    character(len=128) :: local_reason
    integer(int64) :: generation
    logical :: ok
    real(real64) :: hetop

    trace = kt15_atomic_trace_t()
    success = .false.
    reason = 'UNSET'

    call validate_kt15_application_state(state, ok, local_reason)
    if (.not. ok) then
      reason = 'KT15_INVALID_ACCEPTED_APPLICATION_STATE'
      return
    end if
    trace%origin_coherent = .true.
    generation = accepted_store_generation(state%science_store)
    trace%origin_generation = generation

    if (.not. ieee_is_finite(static_hydrology%he_top) .or. static_hydrology%he_top <= 0.0_real64 .or. &
        .not. ieee_is_finite(static_hydrology%lefrrv) .or. &
        .not. ieee_is_finite(static_hydrology%lefrso)) then
      reason = 'KT15_INVALID_STATIC_HYDROLOGY_CONFIG'
      return
    end if
    if (.not. allocated(state%continuation%hydrology_origin%mofro)) then
      reason = 'KT15_MISSING_HYDROLOGY_ORIGIN_PROFILE'
      return
    end if
    if (selected_packet%layer_count <= 0 .or. &
        size(state%continuation%hydrology_origin%mofro) /= selected_packet%layer_count) then
      reason = 'KT15_HYDROLOGY_PROFILE_LAYER_MISMATCH'
      return
    end if

    call accepted_store_time(state%science_store, origin_time, ok)
    if (.not. ok) then
      reason = 'KT15_ACCEPTED_ORIGIN_TIME_UNAVAILABLE'
      return
    end if

    call make_hydroexec01_start_context( &
      state%continuation%hydrology_origin%pn, &
      state%continuation%hydrology_origin%sic, &
      state%continuation%hydrology_origin%snla, &
      state%continuation%hydrology_origin%mofro(1), &
      static_hydrology%he_top, static_hydrology%lefrrv, static_hydrology%lefrso, &
      state%continuation%runinu_call_entry, start_context, ok, local_reason)
    if (.not. ok) then
      reason = 'KT15_START_CONTEXT_CONSTRUCTION_FAILED'
      return
    end if
    hetop = static_hydrology%he_top

    call make_immutable_static_boundary_interval_frame(boundary, boundary_content_sha256, &
      simulation_start_year, state%continuation%boundary_cursor, origin_time, endpoint_time, &
      boundary_frame, next_cursor, ok, local_reason)
    if (.not. ok) then
      reason = 'KT15_OPAQUE_BOUNDARY_BINDING_FAILED'
      return
    end if
    trace%boundary_bound = .true.
    trace%boundary_content_sha256 = boundary_content_sha256

    ! Work only on a private application-state copy. External accepted state
    ! remains untouched until science, continuation and group identity all pass.
    working = state

    call execute_boundary_frame_tcd042_interval(working%science_store, selected_packet, &
      runtime_calendar_contract_id, producer_day_offset, origin_time, endpoint_time, &
      execution_id, boundary_frame, load_channel, hetop, start_context, &
      trace%composition, ok, local_reason)
    if (.not. ok) then
      reason = 'KT15_WORKING_SCIENCE_COMPOSITION_FAILED'
      return
    end if
    trace%working_science_committed = .true.
    trace%selected_boundary_year = trace%composition%boundary_selected_year
    trace%selected_boundary_slot = trace%composition%boundary_selected_slot

    call prepare_next_composite_continuation(state%continuation, endpoint_time, &
      selected_packet%ponding_end, selected_packet%interception_storage_end, &
      selected_packet%snow_storage_end, selected_packet%mofrt, &
      trace%composition%science%runinu, next_cursor, next_continuation, ok, local_reason)
    if (.not. ok) then
      reason = 'KT15_NEXT_CONTINUATION_PREPARATION_FAILED'
      return
    end if
    trace%next_continuation_ready = .true.

    call validate_composite_against_accepted_store(next_continuation, working%science_store, ok, local_reason)
    if (.not. ok) then
      reason = 'KT15_WORKING_GROUP_IDENTITY_MISMATCH'
      return
    end if

    working%continuation = next_continuation
    call validate_kt15_application_state(working, ok, local_reason)
    if (.not. ok) then
      reason = 'KT15_WORKING_APPLICATION_INVALID'
      return
    end if

    ! One intrinsic assignment publishes the complete validated aggregate.
    state = working

    trace%external_group_published = .true.
    trace%published_generation = accepted_store_generation(state%science_store)
    success = .true.
    reason = 'KT15_ATOMIC_OPAQUE_FRAME_APPLICATION_INTERVAL_COMMITTED'
  end subroutine execute_kt15_atomic_interval

  integer(int64) function kt15_application_generation(state) result(value)
    type(kt15_application_state_t), intent(in) :: state
    value = -1_int64
    if (trim(state%schema_id) /= KT15_APPLICATION_SCHEMA) return
    value = accepted_store_generation(state%science_store)
  end function kt15_application_generation

  subroutine kt15_application_time(state, value, ok)
    type(kt15_application_state_t), intent(in) :: state
    type(TimeCoordinate), intent(out) :: value
    logical, intent(out) :: ok
    value = TimeCoordinate()
    ok = .false.
    if (trim(state%schema_id) /= KT15_APPLICATION_SCHEMA) return
    call accepted_store_time(state%science_store, value, ok)
  end subroutine kt15_application_time

  subroutine snapshot_kt15_science_payload(state, copy, ok)
    type(kt15_application_state_t), intent(in) :: state
    class(transient_payload_t), allocatable, intent(out) :: copy
    logical, intent(out) :: ok
    ok = .false.
    if (trim(state%schema_id) /= KT15_APPLICATION_SCHEMA) return
    call snapshot_accepted_payload(state%science_store, copy, ok)
  end subroutine snapshot_kt15_science_payload

  subroutine snapshot_kt15_continuation(state, copy, ok)
    type(kt15_application_state_t), intent(in) :: state
    type(composite_accepted_continuation_t), intent(out) :: copy
    logical, intent(out) :: ok
    character(len=128) :: local_reason
    copy = composite_accepted_continuation_t()
    ok = .false.
    if (trim(state%schema_id) /= KT15_APPLICATION_SCHEMA) return
    copy = state%continuation
    call validate_composite_continuation(copy, ok, local_reason)
  end subroutine snapshot_kt15_continuation

end module mod_animo_atomic_composite_application
