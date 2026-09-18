module mod_animo_tcd042_bounded_composition
  use iso_fortran_env, only: int64, real64
  use mod_transient_time, only: TimeCoordinate, time_equal
  use mod_transient_contracts, only: transient_payload_t, admissibility_t
  use mod_transient_transactions, only: accepted_store_t, accepted_store_time
  use mod_transient_interval_runtime, only: attempt_request_t, runtime_trace_t, run_interval
  use mod_animo_hydrology_adapter, only: hydrology_step_t, hydro_detailed_external_t, &
    project_hydro_detailed_explicit, KT05_OK
  use mod_animo_explicit_hydrology_runtime_binding, only: &
    animo_runtime_probe_state_t, animo_explicit_hydrology_runtime_probe_client_t
  use mod_animo_resolved_upper_hydrology_contract, only: resolved_upper_hydrology_t
  use mod_animo_tcd042_runoff_load_context, only: tcd042_runoff_load_context_t
  use mod_animo_bounded_no_ponding_upper_hydrology, only: &
    hydroexec01_start_context_t, hydroexec01_diagnostics_t, &
    resolve_rev53_no_ponding_upper_hydrology
  use mod_animo_tcd042_upper_solute_load_contract, only: &
    tcd042_upper_loads_t, select_tcd042_load_channel
  use mod_animo_tcd042_upper_solute_load_resolver, only: &
    tcd042_load_hydrology_context_t, tcd042_upper_chemistry_forcing_t, &
    resolve_tcd042_upper_loads
  use mod_animo_tcd042_upper_boundary_client, only: &
    tcd042_resolved_hydrology_t, tcd042_upper_boundary_client_t, &
    TCD042_RESOLVED_HYDROLOGY_SCHEMA, configure_tcd042_client, &
    tcd042_last_diagnostics
  implicit none
  private

  type, public :: kt13_composition_trace_t
    logical :: kt06_binding_passed = .false.
    logical :: hydroexec_passed = .false.
    logical :: load_resolution_passed = .false.
    logical :: science_runtime_committed = .false.
    real(real64) :: flib_top = 0.0_real64
    real(real64) :: rurv = 0.0_real64
    real(real64) :: rupr = 0.0_real64
    real(real64) :: runinu = 0.0_real64
    real(real64) :: selected_load_rate = 0.0_real64
    real(real64) :: average_concentration = 0.0_real64
    real(real64) :: tcd042_flux = 0.0_real64
    real(real64) :: tcd042_p = 0.0_real64
    integer :: tcd042_branch = 0
    integer :: commit_count = 0
  end type kt13_composition_trace_t

  public :: execute_bounded_tcd042_composed_interval

contains

  subroutine execute_bounded_tcd042_composed_interval( &
      store, selected_packet, runtime_calendar_contract_id, producer_day_offset, &
      origin_time, endpoint_time, execution_id, start_context, chemistry, &
      load_channel, hetop, trace, success, reason)
    type(accepted_store_t), intent(inout) :: store
    type(hydrology_step_t), intent(in) :: selected_packet
    character(len=*), intent(in) :: runtime_calendar_contract_id
    integer(int64), intent(in) :: producer_day_offset
    type(TimeCoordinate), intent(in) :: origin_time, endpoint_time
    character(len=*), intent(in) :: execution_id
    type(hydroexec01_start_context_t), intent(in) :: start_context
    type(tcd042_upper_chemistry_forcing_t), intent(in) :: chemistry
    integer, intent(in) :: load_channel
    real(real64), intent(in) :: hetop
    type(kt13_composition_trace_t), intent(out) :: trace
    logical, intent(out) :: success
    character(len=*), intent(out) :: reason

    type(animo_explicit_hydrology_runtime_probe_client_t) :: binding_client
    type(animo_runtime_probe_state_t) :: binding_origin
    class(transient_payload_t), allocatable :: binding_candidate
    type(admissibility_t) :: binding_admissibility
    type(hydro_detailed_external_t) :: projection
    type(resolved_upper_hydrology_t) :: resolved_hydrology
    type(tcd042_runoff_load_context_t) :: runoff_context
    type(hydroexec01_diagnostics_t) :: hydro_diagnostics
    type(tcd042_load_hydrology_context_t) :: load_hydrology
    type(tcd042_upper_loads_t) :: loads
    type(tcd042_resolved_hydrology_t) :: science_hydrology
    type(tcd042_upper_boundary_client_t) :: science_client
    type(attempt_request_t) :: requests(1)
    type(runtime_trace_t) :: runtime_trace
    type(TimeCoordinate) :: accepted_origin
    logical :: ok, equal, compare_ok, binding_ok, diag_valid
    integer :: kt05_status
    character(len=128) :: local_reason
    real(real64) :: load_rate

    trace = kt13_composition_trace_t()
    success = .false.
    reason = 'UNSET'

    call accepted_store_time(store, accepted_origin, ok)
    if (.not. ok) then
      reason = 'KT13_INVALID_ACCEPTED_STORE'
      return
    end if
    call time_equal(accepted_origin, origin_time, equal, compare_ok)
    if (.not. compare_ok .or. .not. equal) then
      reason = 'KT13_ACCEPTED_ORIGIN_TIME_MISMATCH'
      return
    end if
    if (len_trim(execution_id) == 0) then
      reason = 'KT13_MISSING_EXECUTION_ID'
      return
    end if

    ! Reuse admitted KT06 binding semantics rather than duplicating its
    ! producer/runtime time mapping in the science composition layer.
    binding_client%forcing = selected_packet
    binding_client%forcing_present = .true.
    binding_client%runtime_calendar_contract_id = runtime_calendar_contract_id
    binding_client%producer_day_offset = producer_day_offset
    binding_origin%state_token = 0_int64

    call binding_client%execute_attempt(binding_origin, origin_time, endpoint_time, &
      binding_candidate, binding_admissibility, binding_ok, local_reason)
    if (.not. binding_ok .or. .not. binding_admissibility%admissible) then
      reason = 'KT13_KT06_BINDING_FAILED'
      return
    end if
    trace%kt06_binding_passed = .true.

    call project_hydro_detailed_explicit(selected_packet, projection, kt05_status)
    if (kt05_status /= KT05_OK) then
      reason = 'KT13_KT05_PROJECTION_FAILED'
      return
    end if

    call resolve_rev53_no_ponding_upper_hydrology(execution_id, origin_time, endpoint_time, &
      projection, start_context, resolved_hydrology, runoff_context, hydro_diagnostics, ok, local_reason)
    if (.not. ok) then
      reason = 'KT13_HYDROEXEC01_FAILED'
      return
    end if
    trace%hydroexec_passed = .true.
    trace%flib_top = resolved_hydrology%flib_top
    trace%rurv = resolved_hydrology%rurv
    trace%rupr = runoff_context%rupr
    trace%runinu = runoff_context%runinu

    load_hydrology%prr = projection%prr
    load_hydrology%prsn = projection%prsn
    load_hydrology%prirr = projection%prirr
    load_hydrology%runon = projection%runon
    load_hydrology%rupr = runoff_context%rupr
    load_hydrology%runinu = runoff_context%runinu

    call resolve_tcd042_upper_loads(execution_id, origin_time, endpoint_time, &
      load_hydrology, chemistry, loads, ok, local_reason)
    if (.not. ok) then
      reason = 'KT13_UBFORCE02_FAILED'
      return
    end if
    call select_tcd042_load_channel(loads, load_channel, load_rate, ok, local_reason)
    if (.not. ok) then
      reason = 'KT13_LOAD_CHANNEL_SELECTION_FAILED'
      return
    end if
    trace%load_resolution_passed = .true.
    trace%selected_load_rate = load_rate

    science_hydrology%schema_id = TCD042_RESOLVED_HYDROLOGY_SCHEMA
    science_hydrology%flpn = resolved_hydrology%flpn
    science_hydrology%flib_top = resolved_hydrology%flib_top
    science_hydrology%rurv = resolved_hydrology%rurv

    call configure_tcd042_client(science_client, science_hydrology, hetop, load_rate, ok)
    if (.not. ok) then
      reason = 'KT13_TCD042_CONFIGURATION_FAILED'
      return
    end if

    requests(1)%endpoint_time = endpoint_time
    requests(1)%retry_permitted_after_reject = .false.
    call run_interval(store, science_client, endpoint_time, requests, 1, runtime_trace, success, local_reason)
    if (.not. success) then
      reason = 'KT13_TCD042_TRANSACTION_FAILED'
      return
    end if

    call tcd042_last_diagnostics(science_client, trace%average_concentration, &
      trace%tcd042_flux, trace%tcd042_p, trace%tcd042_branch, diag_valid)
    if (.not. diag_valid) then
      success = .false.
      reason = 'KT13_TCD042_DIAGNOSTICS_MISSING_AFTER_COMMIT'
      return
    end if

    trace%commit_count = runtime_trace%commit_count
    trace%science_runtime_committed = .true.
    success = .true.
    reason = 'KT13_BOUNDED_TCD042_INTERVAL_COMMITTED'
  end subroutine execute_bounded_tcd042_composed_interval

end module mod_animo_tcd042_bounded_composition
