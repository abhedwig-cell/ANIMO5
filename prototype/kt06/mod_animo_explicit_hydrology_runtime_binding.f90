module mod_animo_explicit_hydrology_runtime_binding
  use iso_fortran_env, only: int64, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  use mod_transient_time, only: TimeCoordinate
  use mod_transient_contracts, only: transient_payload_t, admissibility_t
  use mod_transient_transactions, only: accepted_store_t, initialize_accepted_store
  use mod_transient_interval_runtime, only: transient_client_t
  use mod_animo_hydrology_adapter, only: hydrology_step_t, &
    hydro_detailed_external_t, validate_hydrology_step_explicit, &
    project_hydro_detailed_explicit, KT05_OK
  implicit none
  private

  integer(int64), parameter :: MAX_EXACT_REAL64_INTEGER = 9007199254740991_int64

  type, extends(transient_payload_t), public :: animo_runtime_probe_state_t
    integer(int64) :: state_token = 0_int64
  contains
    procedure :: clone_payload => probe_clone_payload
    procedure :: is_valid => probe_payload_valid
  end type animo_runtime_probe_state_t

  type, extends(transient_client_t), public :: &
      animo_explicit_hydrology_runtime_client_t
    type(hydrology_step_t) :: forcing
    logical :: forcing_present = .false.
    character(len=48) :: runtime_calendar_contract_id = ''
    integer(int64) :: producer_day_offset = 0_int64
  contains
    procedure :: execute_attempt => execute_explicit_hydrology_attempt
  end type animo_explicit_hydrology_runtime_client_t

  public :: initialize_probe_store

contains

  subroutine probe_clone_payload(self, copy)
    class(animo_runtime_probe_state_t), intent(in) :: self
    class(transient_payload_t), allocatable, intent(out) :: copy

    allocate(animo_runtime_probe_state_t :: copy)
    select type (typed => copy)
    type is (animo_runtime_probe_state_t)
      typed%state_token = self%state_token
    end select
  end subroutine probe_clone_payload

  logical function probe_payload_valid(self)
    class(animo_runtime_probe_state_t), intent(in) :: self
    probe_payload_valid = self%state_token >= 0_int64
  end function probe_payload_valid

  subroutine initialize_probe_store(store, lineage_id, time, state_token, ok)
    type(accepted_store_t), intent(out) :: store
    character(len=*), intent(in) :: lineage_id
    type(TimeCoordinate), intent(in) :: time
    integer(int64), intent(in) :: state_token
    logical, intent(out) :: ok
    type(animo_runtime_probe_state_t) :: payload

    ok = .false.
    if (state_token < 0_int64) return
    payload%state_token = state_token
    call initialize_accepted_store(lineage_id, time, payload, store, ok)
  end subroutine initialize_probe_store

  subroutine exact_nonnegative_integer(value, integer_value, ok)
    real(real64), intent(in) :: value
    integer(int64), intent(out) :: integer_value
    logical, intent(out) :: ok

    integer_value = 0_int64
    ok = .false.
    if (.not. ieee_is_finite(value)) return
    if (value < 0.0_real64) return
    if (value > real(MAX_EXACT_REAL64_INTEGER, real64)) return

    integer_value = nint(value, kind=int64)
    if (transfer(value, 0_int64) /= &
        transfer(real(integer_value, real64), 0_int64)) then
      integer_value = 0_int64
      return
    end if
    ok = .true.
  end subroutine exact_nonnegative_integer

  subroutine execute_explicit_hydrology_attempt( &
      self, origin_payload, origin_time, endpoint_time, candidate_payload, &
      admissibility, ok, reason)
    class(animo_explicit_hydrology_runtime_client_t), intent(inout) :: self
    class(transient_payload_t), intent(in) :: origin_payload
    type(TimeCoordinate), intent(in) :: origin_time, endpoint_time
    class(transient_payload_t), allocatable, intent(out) :: candidate_payload
    type(admissibility_t), intent(out) :: admissibility
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    type(hydro_detailed_external_t) :: projection
    integer :: kt05_status
    integer(int64) :: producer_endpoint, producer_step
    integer(int64) :: runtime_step, expected_endpoint
    logical :: endpoint_ok, step_ok

    admissibility = admissibility_t()
    ok = .false.
    reason = 'UNSET'

    if (.not. self%forcing_present) then
      reason = 'MISSING_HYDROLOGY_FORCING'
      return
    end if
    if (len_trim(self%runtime_calendar_contract_id) == 0) then
      reason = 'MISSING_RUNTIME_CALENDAR_BINDING'
      return
    end if
    if (self%producer_day_offset < 0_int64) then
      reason = 'INVALID_PRODUCER_DAY_OFFSET'
      return
    end if
    if (trim(origin_time%calendar_contract_id) /= &
        trim(self%runtime_calendar_contract_id)) then
      reason = 'RUNTIME_CALENDAR_BINDING_MISMATCH'
      return
    end if
    if (trim(endpoint_time%calendar_contract_id) /= &
        trim(self%runtime_calendar_contract_id)) then
      reason = 'RUNTIME_CALENDAR_BINDING_MISMATCH'
      return
    end if
    if (origin_time%subday_numerator /= 0_int64 .or. &
        endpoint_time%subday_numerator /= 0_int64) then
      reason = 'SUBDAY_MAPPING_NOT_QUALIFIED'
      return
    end if
    if (origin_time%day_index < 0_int64 .or. &
        endpoint_time%day_index <= origin_time%day_index) then
      reason = 'INVALID_RUNTIME_INTERVAL'
      return
    end if

    call validate_hydrology_step_explicit(self%forcing, kt05_status)
    if (kt05_status /= KT05_OK) then
      reason = 'INVALID_KT05_EXPLICIT_HYDROLOGY_STEP'
      return
    end if

    call exact_nonnegative_integer( &
      self%forcing%producer_endpoint_day, producer_endpoint, endpoint_ok)
    call exact_nonnegative_integer( &
      self%forcing%producer_step_days, producer_step, step_ok)
    if (.not. endpoint_ok .or. .not. step_ok) then
      reason = 'NONEXACT_PRODUCER_TIME_METADATA'
      return
    end if

    runtime_step = endpoint_time%day_index - origin_time%day_index
    if (producer_step /= runtime_step) then
      reason = 'PRODUCER_STEP_MISMATCH'
      return
    end if
    if (endpoint_time%day_index > &
        huge(expected_endpoint) - self%producer_day_offset) then
      reason = 'PRODUCER_TIME_MAPPING_OVERFLOW'
      return
    end if
    expected_endpoint = endpoint_time%day_index + self%producer_day_offset
    if (producer_endpoint /= expected_endpoint) then
      reason = 'PRODUCER_ENDPOINT_MISMATCH'
      return
    end if

    call project_hydro_detailed_explicit(self%forcing, projection, kt05_status)
    if (kt05_status /= KT05_OK) then
      reason = 'KT05_HYDROLOGY_PROJECTION_FAILED'
      return
    end if

    select type (origin => origin_payload)
    type is (animo_runtime_probe_state_t)
      allocate(animo_runtime_probe_state_t :: candidate_payload)
      select type (candidate => candidate_payload)
      type is (animo_runtime_probe_state_t)
        candidate%state_token = origin%state_token
      end select
    class default
      reason = 'INVALID_ANIMO_ACCEPTED_PAYLOAD'
      return
    end select

    admissibility%evidence_complete = .true.
    admissibility%admissible = .true.
    ok = .true.
    reason = 'BOUND_AND_PROJECTED'
  end subroutine execute_explicit_hydrology_attempt

end module mod_animo_explicit_hydrology_runtime_binding
