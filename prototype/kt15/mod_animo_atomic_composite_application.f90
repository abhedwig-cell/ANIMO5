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
  use mod_animo_static_boundary_year_binding, only: boundary_year_cursor_t, BOUNDQ02_MAX_LEGACY_YEAR
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
    'ANIMO_KT15_ATOMIC_COMPOSITE_APPLICATION_V2'
  character(len=*), parameter, public :: KT15_CONFIG_SCHEMA = &
    'ANIMO_KT15_IMMUTABLE_APPLICATION_CONFIG_V1'

  type, public :: kt15_static_hydrology_config_t
    real(real64) :: he_top = 0.0_real64
    real(real64) :: lefrrv = 0.0_real64
    real(real64) :: lefrso = 0.0_real64
  end type kt15_static_hydrology_config_t

  type, public :: kt15_application_config_t
    private
    character(len=56) :: schema_id = ''
    character(len=64) :: runtime_calendar_contract_id = ''
    integer(int64) :: producer_day_offset = 0_int64
    type(kt15_static_hydrology_config_t) :: static_hydrology
    character(len=64) :: boundary_content_sha256 = ''
    integer :: simulation_start_year = 0
    integer :: load_channel = 0
  end type kt15_application_config_t

  type, public :: kt15_application_state_t
    private
    character(len=64) :: schema_id = ''
    type(kt15_application_config_t) :: config
    type(accepted_store_t) :: science_store
    type(composite_accepted_continuation_t) :: continuation
  end type kt15_application_state_t

  type, public :: kt15_atomic_trace_t
    logical :: origin_coherent = .false.
    logical :: config_bound = .false.
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

  public :: make_kt15_application_config
  public :: validate_kt15_application_config
  public :: same_kt15_application_config
  public :: initialize_kt15_application_state
  public :: validate_kt15_application_state
  public :: execute_kt15_atomic_interval
  public :: kt15_application_generation
  public :: kt15_application_time
  public :: snapshot_kt15_science_payload
  public :: snapshot_kt15_continuation
  public :: snapshot_kt15_application_config
  public :: inspect_kt15_application_config

contains

  logical function canonical_sha256(value)
    character(len=*), intent(in) :: value
    integer :: i, code
    canonical_sha256 = .false.
    if (len_trim(value) /= 64) return
    do i = 1, 64
      code = iachar(value(i:i))
      if (.not. ((code >= iachar('0') .and. code <= iachar('9')) .or. &
                 (code >= iachar('a') .and. code <= iachar('f')))) return
    end do
    canonical_sha256 = .true.
  end function canonical_sha256

  logical function exact_real64_equal(left, right)
    real(real64), intent(in) :: left, right
    integer(int64) :: a, b
    a = transfer(left, a)
    b = transfer(right, b)
    exact_real64_equal = a == b
  end function exact_real64_equal

  subroutine make_kt15_application_config(runtime_calendar_contract_id, producer_day_offset, &
      static_hydrology, boundary_content_sha256, simulation_start_year, load_channel, config, ok, reason)
    character(len=*), intent(in) :: runtime_calendar_contract_id
    integer(int64), intent(in) :: producer_day_offset
    type(kt15_static_hydrology_config_t), intent(in) :: static_hydrology
    character(len=*), intent(in) :: boundary_content_sha256
    integer, intent(in) :: simulation_start_year, load_channel
    type(kt15_application_config_t), intent(out) :: config
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    config = kt15_application_config_t()
    if (len_trim(runtime_calendar_contract_id) > len(config%runtime_calendar_contract_id)) then
      ok = .false.
      reason = 'KT15_CONFIG_CALENDAR_ID_TOO_LONG'
      return
    end if
    config%schema_id = KT15_CONFIG_SCHEMA
    config%runtime_calendar_contract_id = trim(runtime_calendar_contract_id)
    config%producer_day_offset = producer_day_offset
    config%static_hydrology = static_hydrology
    if (len_trim(boundary_content_sha256) == 64) then
      config%boundary_content_sha256 = boundary_content_sha256(1:64)
    end if
    config%simulation_start_year = simulation_start_year
    config%load_channel = load_channel
    call validate_kt15_application_config(config, ok, reason)
  end subroutine make_kt15_application_config

  subroutine validate_kt15_application_config(config, ok, reason)
    type(kt15_application_config_t), intent(in) :: config
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    ok = .false.
    reason = 'UNSET'
    if (trim(config%schema_id) /= KT15_CONFIG_SCHEMA) then
      reason = 'KT15_CONFIG_SCHEMA_MISMATCH'
      return
    end if
    if (len_trim(config%runtime_calendar_contract_id) == 0) then
      reason = 'KT15_CONFIG_MISSING_CALENDAR_ID'
      return
    end if
    if (.not. ieee_is_finite(config%static_hydrology%he_top) .or. &
        config%static_hydrology%he_top <= 0.0_real64 .or. &
        .not. ieee_is_finite(config%static_hydrology%lefrrv) .or. &
        .not. ieee_is_finite(config%static_hydrology%lefrso)) then
      reason = 'KT15_CONFIG_INVALID_STATIC_HYDROLOGY'
      return
    end if
    if (.not. canonical_sha256(config%boundary_content_sha256)) then
      reason = 'KT15_CONFIG_INVALID_BOUNDARY_CONTENT_SHA256'
      return
    end if
    if (config%simulation_start_year < 1 .or. &
        config%simulation_start_year > BOUNDQ02_MAX_LEGACY_YEAR) then
      reason = 'KT15_CONFIG_INVALID_SIMULATION_START_YEAR'
      return
    end if
    if (config%load_channel < 1 .or. config%load_channel > 6) then
      reason = 'KT15_CONFIG_INVALID_LOAD_CHANNEL'
      return
    end if
    ok = .true.
    reason = 'VALID_KT15_IMMUTABLE_APPLICATION_CONFIG'
  end subroutine validate_kt15_application_config

  logical function same_kt15_application_config(left, right)
    type(kt15_application_config_t), intent(in) :: left, right
    same_kt15_application_config = .false.
    if (trim(left%schema_id) /= trim(right%schema_id)) return
    if (trim(left%runtime_calendar_contract_id) /= trim(right%runtime_calendar_contract_id)) return
    if (left%producer_day_offset /= right%producer_day_offset) return
    if (.not. exact_real64_equal(left%static_hydrology%he_top, right%static_hydrology%he_top)) return
    if (.not. exact_real64_equal(left%static_hydrology%lefrrv, right%static_hydrology%lefrrv)) return
    if (.not. exact_real64_equal(left%static_hydrology%lefrso, right%static_hydrology%lefrso)) return
    if (trim(left%boundary_content_sha256) /= trim(right%boundary_content_sha256)) return
    if (left%simulation_start_year /= right%simulation_start_year) return
    if (left%load_channel /= right%load_channel) return
    same_kt15_application_config = .true.
  end function same_kt15_application_config

  subroutine initialize_kt15_application_state(science_store, continuation, config, state, ok, reason)
    type(accepted_store_t), intent(in) :: science_store
    type(composite_accepted_continuation_t), intent(in) :: continuation
    type(kt15_application_config_t), intent(in) :: config
    type(kt15_application_state_t), intent(out) :: state
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    state = kt15_application_state_t()
    ok = .false.
    reason = 'UNSET'

    call validate_kt15_application_config(config, ok, reason)
    if (.not. ok) return
    call validate_composite_against_accepted_store(continuation, science_store, ok, reason)
    if (.not. ok) then
      reason = 'KT15_INITIAL_SCIENCE_CONTINUATION_INCOHERENT'
      return
    end if

    state%schema_id = KT15_APPLICATION_SCHEMA
    state%config = config
    state%science_store = science_store
    state%continuation = continuation
    call validate_kt15_application_state(state, ok, reason)
    if (ok) reason = 'KT15_APPLICATION_STATE_INITIALIZED'
  end subroutine initialize_kt15_application_state

  subroutine validate_kt15_application_state(state, ok, reason)
    type(kt15_application_state_t), intent(in) :: state
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    type(TimeCoordinate) :: accepted_time

    ok = .false.
    reason = 'UNSET'

    if (trim(state%schema_id) /= KT15_APPLICATION_SCHEMA) then
      reason = 'KT15_APPLICATION_SCHEMA_MISMATCH'
      return
    end if
    call validate_kt15_application_config(state%config, ok, reason)
    if (.not. ok) return
    if (.not. accepted_store_ready(state%science_store)) then
      reason = 'KT15_INVALID_SCIENCE_STORE'
      return
    end if
    call accepted_store_time(state%science_store, accepted_time, ok)
    if (.not. ok) then
      reason = 'KT15_ACCEPTED_TIME_UNAVAILABLE'
      return
    end if
    if (trim(accepted_time%calendar_contract_id) /= trim(state%config%runtime_calendar_contract_id)) then
      ok = .false.
      reason = 'KT15_CONFIG_ACCEPTED_TIME_CALENDAR_MISMATCH'
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

  subroutine execute_kt15_atomic_interval(state, selected_packet, endpoint_time, execution_id, &
      boundary, trace, success, reason)
    type(kt15_application_state_t), intent(inout) :: state
    type(hydrology_step_t), intent(in) :: selected_packet
    type(TimeCoordinate), intent(in) :: endpoint_time
    character(len=*), intent(in) :: execution_id
    type(static_boundary_chemistry_t), intent(in) :: boundary
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
    trace%config_bound = .true.
    generation = accepted_store_generation(state%science_store)
    trace%origin_generation = generation

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
      state%config%static_hydrology%he_top, state%config%static_hydrology%lefrrv, &
      state%config%static_hydrology%lefrso, state%continuation%runinu_call_entry, &
      start_context, ok, local_reason)
    if (.not. ok) then
      reason = 'KT15_START_CONTEXT_CONSTRUCTION_FAILED'
      return
    end if
    hetop = state%config%static_hydrology%he_top

    call make_immutable_static_boundary_interval_frame(boundary, state%config%boundary_content_sha256, &
      state%config%simulation_start_year, state%continuation%boundary_cursor, origin_time, endpoint_time, &
      boundary_frame, next_cursor, ok, local_reason)
    if (.not. ok) then
      reason = 'KT15_OPAQUE_BOUNDARY_BINDING_FAILED'
      return
    end if
    trace%boundary_bound = .true.
    trace%boundary_content_sha256 = state%config%boundary_content_sha256

    working = state

    call execute_boundary_frame_tcd042_interval(working%science_store, selected_packet, &
      state%config%runtime_calendar_contract_id, state%config%producer_day_offset, &
      origin_time, endpoint_time, execution_id, boundary_frame, state%config%load_channel, &
      hetop, start_context, trace%composition, ok, local_reason)
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

    state = working

    trace%external_group_published = .true.
    trace%published_generation = accepted_store_generation(state%science_store)
    success = .true.
    reason = 'KT15_ATOMIC_IMMUTABLE_CONFIG_APPLICATION_INTERVAL_COMMITTED'
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

  subroutine inspect_kt15_application_config(config, runtime_calendar_contract_id, &
      producer_day_offset, static_hydrology, boundary_content_sha256, &
      simulation_start_year, load_channel, ok, reason)
    type(kt15_application_config_t), intent(in) :: config
    character(len=*), intent(out) :: runtime_calendar_contract_id
    integer(int64), intent(out) :: producer_day_offset
    type(kt15_static_hydrology_config_t), intent(out) :: static_hydrology
    character(len=*), intent(out) :: boundary_content_sha256
    integer, intent(out) :: simulation_start_year, load_channel
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    character(len=128) :: local_reason

    runtime_calendar_contract_id = ''
    producer_day_offset = 0_int64
    static_hydrology = kt15_static_hydrology_config_t()
    boundary_content_sha256 = ''
    simulation_start_year = 0
    load_channel = 0
    ok = .false.
    reason = 'UNSET'

    call validate_kt15_application_config(config, ok, local_reason)
    if (.not. ok) then
      reason = 'KT15_CONFIG_INSPECTION_INVALID_CONFIG'
      return
    end if
    if (len_trim(config%runtime_calendar_contract_id) > len(runtime_calendar_contract_id)) then
      ok = .false.
      reason = 'KT15_CONFIG_INSPECTION_CALENDAR_OUTPUT_TOO_SHORT'
      return
    end if
    if (len_trim(config%boundary_content_sha256) > len(boundary_content_sha256)) then
      ok = .false.
      reason = 'KT15_CONFIG_INSPECTION_HASH_OUTPUT_TOO_SHORT'
      return
    end if

    runtime_calendar_contract_id = trim(config%runtime_calendar_contract_id)
    producer_day_offset = config%producer_day_offset
    static_hydrology = config%static_hydrology
    boundary_content_sha256 = trim(config%boundary_content_sha256)
    simulation_start_year = config%simulation_start_year
    load_channel = config%load_channel
    ok = .true.
    reason = 'KT15_APPLICATION_CONFIG_INSPECTED_READ_ONLY'
  end subroutine inspect_kt15_application_config

  subroutine snapshot_kt15_application_config(state, copy, ok)
    type(kt15_application_state_t), intent(in) :: state
    type(kt15_application_config_t), intent(out) :: copy
    logical, intent(out) :: ok
    character(len=128) :: local_reason
    copy = kt15_application_config_t()
    ok = .false.
    if (trim(state%schema_id) /= KT15_APPLICATION_SCHEMA) return
    copy = state%config
    call validate_kt15_application_config(copy, ok, local_reason)
  end subroutine snapshot_kt15_application_config

end module mod_animo_atomic_composite_application
