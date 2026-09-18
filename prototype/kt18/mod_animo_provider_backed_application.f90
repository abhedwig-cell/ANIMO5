module mod_animo_provider_backed_application
  use iso_fortran_env, only: int64, real64
  use mod_transient_time, only: TimeCoordinate
  use mod_animo_hydrology_adapter, only: hydrology_step_t
  use mod_animo_multi_packet_hydrology_provider, only: &
    animo_multi_packet_hydrology_runtime_probe_client_t, &
    select_multi_packet_hydrology_step_copy
  use mod_animo_static_boundary_chemistry_adapter, only: static_boundary_chemistry_t
  use mod_animo_atomic_composite_application, only: &
    kt15_application_state_t, kt15_atomic_trace_t, &
    validate_kt15_application_state, kt15_application_time, &
    execute_kt15_atomic_interval, kt15_application_generation
  implicit none
  private

  character(len=*), parameter, public :: KT18_COMPOSITION_SCHEMA = &
    'ANIMO_KT18_PROVIDER_BACKED_APPLICATION_V1'

  type, public :: kt18_provider_application_trace_t
    character(len=48) :: schema_id = ''
    logical :: accepted_application_valid = .false.
    logical :: provider_packet_selected = .false.
    logical :: application_interval_committed = .false.
    integer(int64) :: origin_generation = -1_int64
    integer(int64) :: published_generation = -1_int64
    real(real64) :: selected_producer_endpoint_day = 0.0_real64
    real(real64) :: selected_producer_step_days = 0.0_real64
    type(kt15_atomic_trace_t) :: application
  end type kt18_provider_application_trace_t

  public :: execute_provider_backed_application_interval

contains

  subroutine execute_provider_backed_application_interval(provider,state,endpoint_time, &
      execution_id,boundary,trace,success,reason)
    type(animo_multi_packet_hydrology_runtime_probe_client_t), intent(in) :: provider
    type(kt15_application_state_t), intent(inout) :: state
    type(TimeCoordinate), intent(in) :: endpoint_time
    character(len=*), intent(in) :: execution_id
    type(static_boundary_chemistry_t), intent(in) :: boundary
    type(kt18_provider_application_trace_t), intent(out) :: trace
    logical, intent(out) :: success
    character(len=*), intent(out) :: reason

    type(TimeCoordinate) :: origin_time
    type(hydrology_step_t) :: selected_packet
    character(len=128) :: local_reason
    logical :: ok

    trace = kt18_provider_application_trace_t()
    trace%schema_id = KT18_COMPOSITION_SCHEMA
    success = .false.
    reason = 'UNSET'

    call validate_kt15_application_state(state,ok,local_reason)
    if(.not.ok) then
      reason = 'KT18_INVALID_ACCEPTED_APPLICATION_STATE'
      return
    end if
    trace%accepted_application_valid = .true.

    call kt15_application_time(state,origin_time,ok)
    if(.not.ok) then
      reason = 'KT18_ACCEPTED_ORIGIN_TIME_UNAVAILABLE'
      return
    end if

    trace%origin_generation = state_generation(state)

    call select_multi_packet_hydrology_step_copy(provider,origin_time,endpoint_time, &
      selected_packet,ok,local_reason)
    if(.not.ok) then
      reason = 'KT18_PROVIDER_SELECTION_FAILED:'//trim(local_reason)
      return
    end if
    trace%provider_packet_selected = .true.
    trace%selected_producer_endpoint_day = selected_packet%producer_endpoint_day
    trace%selected_producer_step_days = selected_packet%producer_step_days

    call execute_kt15_atomic_interval(state,selected_packet,endpoint_time,execution_id, &
      boundary,trace%application,success,local_reason)
    if(.not.success) then
      reason = 'KT18_APPLICATION_INTERVAL_FAILED:'//trim(local_reason)
      return
    end if

    trace%application_interval_committed = .true.
    trace%published_generation = state_generation(state)
    reason = 'KT18_PROVIDER_BACKED_APPLICATION_INTERVAL_COMMITTED'
  end subroutine execute_provider_backed_application_interval

  integer(int64) function state_generation(state) result(value)
    type(kt15_application_state_t), intent(in) :: state
    value = kt15_application_generation(state)
  end function state_generation

end module mod_animo_provider_backed_application
