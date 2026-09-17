module mod_animo_explicit_hydrology_runtime_adapter
  use iso_fortran_env, only: int64, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  use mod_transient_time, only: TimeCoordinate
  use mod_transient_contracts, only: transient_payload_t, admissibility_t
  use mod_transient_transactions, only: accepted_store_t, initialize_accepted_store
  use mod_transient_interval_runtime, only: transient_client_t
  implicit none
  private

  character(len=*), parameter, public :: HYDROLOGY_SCHEMA_ID = 'ANIMO_HYDROLOGY_STEP_V1'
  character(len=*), parameter, public :: HYDROLOGY_UNIT_ID = 'ANIMO_HYDROLOGY_UNITS_V1'
  integer(int64), parameter :: MAX_EXACT_REAL64_INTEGER = 9007199254740991_int64

  type, public :: hydrology_interval_binding_t
    character(len=48) :: schema_id = ''
    character(len=48) :: unit_contract_id = ''
    real(real64) :: producer_endpoint_day = 0.0_real64
    real(real64) :: producer_step_days = 0.0_real64
    logical :: has_interception_storage_end = .false.
    real(real64) :: interception_storage_end = 0.0_real64
  end type hydrology_interval_binding_t

  type, extends(transient_payload_t), public :: animo_runtime_probe_state_t
    integer(int64) :: state_token = 0_int64
  contains
    procedure :: clone_payload => probe_clone_payload
    procedure :: is_valid => probe_payload_valid
  end type animo_runtime_probe_state_t

  type, extends(transient_client_t), public :: animo_explicit_hydrology_client_t
    type(hydrology_interval_binding_t) :: forcing
    logical :: forcing_present = .false.
    integer(int64) :: producer_day_offset = 0_int64
  contains
    procedure :: execute_attempt => execute_explicit_hydrology_attempt
  end type animo_explicit_hydrology_client_t

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
    if (value /= real(integer_value, real64)) then
      integer_value = 0_int64
      return
    end if
    ok = .true.
  end subroutine exact_nonnegative_integer

  logical function binding_valid(binding)
    type(hydrology_interval_binding_t), intent(in) :: binding
    integer(int64) :: endpoint_day, step_days
    logical :: endpoint_ok, step_ok

    binding_valid = .false.
    if (trim(binding%schema_id) /= HYDROLOGY_SCHEMA_ID) return
    if (trim(binding%unit_contract_id) /= HYDROLOGY_UNIT_ID) return
    if (.not. binding%has_interception_storage_end) return
    if (.not. ieee_is_finite(binding%interception_storage_end)) return
    call exact_nonnegative_integer(binding%producer_endpoint_day, endpoint_day, endpoint_ok)
    call exact_nonnegative_integer(binding%producer_step_days, step_days, step_ok)
    if (.not. endpoint_ok .or. .not. step_ok) return
    if (step_days <= 0_int64) return
    binding_valid = .true.
  end function binding_valid

  subroutine execute_explicit_hydrology_attempt(self, origin_payload, origin_time, endpoint_time, candidate_payload, &
      admissibility, ok, reason)
    class(animo_explicit_hydrology_client_t), intent(inout) :: self
    class(transient_payload_t), intent(in) :: origin_payload
    type(TimeCoordinate), intent(in) :: origin_time, endpoint_time
    class(transient_payload_t), allocatable, intent(out) :: candidate_payload
    type(admissibility_t), intent(out) :: admissibility
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    integer(int64) :: producer_endpoint, producer_step, runtime_step, expected_endpoint
    logical :: endpoint_ok, step_ok

    admissibility = admissibility_t()
    ok = .false.
    reason = 'UNSET'

    if (.not. self%forcing_present) then
      reason = 'MISSING_HYDROLOGY_FORCING'
      return
    end if
    if (self%producer_day_offset < 0_int64) then
      reason = 'INVALID_PRODUCER_DAY_OFFSET'
      return
    end if
    if (trim(origin_time%calendar_contract_id) /= trim(endpoint_time%calendar_contract_id)) then
      reason = 'RUNTIME_CALENDAR_MISMATCH'
      return
    end if
    if (origin_time%subday_numerator /= 0_int64 .or. endpoint_time%subday_numerator /= 0_int64) then
      reason = 'SUBDAY_MAPPING_NOT_QUALIFIED'
      return
    end if
    if (origin_time%day_index < 0_int64 .or. endpoint_time%day_index <= origin_time%day_index) then
      reason = 'INVALID_RUNTIME_INTERVAL'
      return
    end if
    if (.not. binding_valid(self%forcing)) then
      reason = 'INVALID_EXPLICIT_HYDROLOGY_BINDING'
      return
    end if

    call exact_nonnegative_integer(self%forcing%producer_endpoint_day, producer_endpoint, endpoint_ok)
    call exact_nonnegative_integer(self%forcing%producer_step_days, producer_step, step_ok)
    if (.not. endpoint_ok .or. .not. step_ok) then
      reason = 'NONEXACT_PRODUCER_TIME_METADATA'
      return
    end if

    runtime_step = endpoint_time%day_index - origin_time%day_index
    if (producer_step /= runtime_step) then
      reason = 'PRODUCER_STEP_MISMATCH'
      return
    end if
    if (endpoint_time%day_index > huge(expected_endpoint) - self%producer_day_offset) then
      reason = 'PRODUCER_TIME_MAPPING_OVERFLOW'
      return
    end if
    expected_endpoint = endpoint_time%day_index + self%producer_day_offset
    if (producer_endpoint /= expected_endpoint) then
      reason = 'PRODUCER_ENDPOINT_MISMATCH'
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
    reason = 'BOUND_AND_CALCULATED'
  end subroutine execute_explicit_hydrology_attempt

end module mod_animo_explicit_hydrology_runtime_adapter
