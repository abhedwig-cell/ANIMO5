module mod_animo_tcd042_boundary_frame_composition
  use iso_fortran_env, only: int64, real64
  use mod_transient_time, only: TimeCoordinate
  use mod_transient_transactions, only: accepted_store_t
  use mod_animo_hydrology_adapter, only: hydrology_step_t
  use mod_animo_bounded_no_ponding_upper_hydrology, only: hydroexec01_start_context_t
  use mod_animo_static_boundary_year_binding, only: static_boundary_interval_frame_t, &
    validate_static_boundary_interval_frame
  use mod_animo_tcd042_bounded_composition, only: kt13_composition_trace_t, &
    execute_bounded_tcd042_composed_interval
  implicit none
  private

  type, public :: kt14_composition_trace_t
    logical :: boundary_frame_validated = .false.
    integer :: boundary_selected_year = 0
    integer :: boundary_selected_slot = 0
    real(real64) :: dry_deposition_nh = 0.0_real64
    real(real64) :: dry_deposition_ni = 0.0_real64
    type(kt13_composition_trace_t) :: science
  end type kt14_composition_trace_t

  public :: execute_boundary_frame_tcd042_interval

contains

  subroutine execute_boundary_frame_tcd042_interval( &
      store, selected_packet, runtime_calendar_contract_id, producer_day_offset, &
      origin_time, endpoint_time, execution_id, start_context, boundary_frame, &
      load_channel, hetop, trace, success, reason)
    type(accepted_store_t), intent(inout) :: store
    type(hydrology_step_t), intent(in) :: selected_packet
    character(len=*), intent(in) :: runtime_calendar_contract_id
    integer(int64), intent(in) :: producer_day_offset
    type(TimeCoordinate), intent(in) :: origin_time, endpoint_time
    character(len=*), intent(in) :: execution_id
    type(hydroexec01_start_context_t), intent(in) :: start_context
    type(static_boundary_interval_frame_t), intent(in) :: boundary_frame
    integer, intent(in) :: load_channel
    real(real64), intent(in) :: hetop
    type(kt14_composition_trace_t), intent(out) :: trace
    logical, intent(out) :: success
    character(len=*), intent(out) :: reason

    logical :: frame_ok
    character(len=128) :: frame_reason, science_reason

    trace = kt14_composition_trace_t()
    success = .false.
    reason = 'UNSET'

    call validate_static_boundary_interval_frame( &
      boundary_frame, origin_time, endpoint_time, frame_ok, frame_reason)
    if (.not. frame_ok) then
      reason = 'KT14_BOUNDARY_INTERVAL_FRAME_INVALID'
      return
    end if

    if (trim(runtime_calendar_contract_id) /= trim(origin_time%calendar_contract_id)) then
      reason = 'KT14_RUNTIME_CALENDAR_MISMATCH'
      return
    end if

    trace%boundary_frame_validated = .true.
    trace%boundary_selected_year = boundary_frame%selected_year
    trace%boundary_selected_slot = boundary_frame%selected_slot
    trace%dry_deposition_nh = boundary_frame%dry_deposition_nh
    trace%dry_deposition_ni = boundary_frame%dry_deposition_ni

    ! Dry deposition remains intentionally outside the wet/advective TCD-042
    ! forcing path. Only the validated interval-bound chemistry payload is
    ! supplied to the already-qualified KT13A composition.
    call execute_bounded_tcd042_composed_interval( &
      store, selected_packet, runtime_calendar_contract_id, producer_day_offset, &
      origin_time, endpoint_time, execution_id, start_context, boundary_frame%chemistry, &
      load_channel, hetop, trace%science, success, science_reason)

    if (.not. success) then
      reason = 'KT14_TCD042_COMPOSITION_FAILED'
      return
    end if

    reason = 'KT14_BOUNDARY_FRAME_TCD042_INTERVAL_COMMITTED'
  end subroutine execute_boundary_frame_tcd042_interval

end module mod_animo_tcd042_boundary_frame_composition
