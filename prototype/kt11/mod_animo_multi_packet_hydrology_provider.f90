module mod_animo_multi_packet_hydrology_provider
  use iso_fortran_env, only: int64, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  use mod_transient_time, only: TimeCoordinate
  use mod_transient_contracts, only: transient_payload_t, admissibility_t
  use mod_transient_interval_runtime, only: transient_client_t
  use mod_animo_hydrology_adapter, only: hydrology_step_t, &
    validate_hydrology_step_explicit, KT05_OK
  use mod_animo_explicit_hydrology_runtime_binding, only: &
    animo_explicit_hydrology_runtime_probe_client_t
  implicit none
  private

  integer(int64), parameter :: MAX_EXACT_REAL64_INTEGER = 9007199254740991_int64

  type, extends(transient_client_t), public :: &
      animo_multi_packet_hydrology_runtime_probe_client_t
    private
    type(hydrology_step_t), allocatable :: packets(:)
    integer(int64), allocatable :: producer_endpoint_key(:)
    integer(int64), allocatable :: producer_step_key(:)
    character(len=48) :: runtime_calendar_contract_id = ''
    integer(int64) :: producer_day_offset = 0_int64
    logical :: configured = .false.
  contains
    procedure :: execute_attempt => execute_multi_packet_attempt
  end type animo_multi_packet_hydrology_runtime_probe_client_t

  public :: initialize_multi_packet_client
  public :: multi_packet_client_ready
  public :: multi_packet_packet_count

contains

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

  subroutine initialize_multi_packet_client( &
      client, packets, runtime_calendar_contract_id, producer_day_offset, ok, reason)
    type(animo_multi_packet_hydrology_runtime_probe_client_t), intent(out) :: client
    type(hydrology_step_t), intent(in) :: packets(:)
    character(len=*), intent(in) :: runtime_calendar_contract_id
    integer(int64), intent(in) :: producer_day_offset
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    integer :: i, j, kt05_status
    integer(int64) :: endpoint_key, step_key
    logical :: endpoint_ok, step_ok

    ok = .false.
    reason = 'UNSET'

    if (size(packets) <= 0) then
      reason = 'EMPTY_HYDROLOGY_PACKET_PROVIDER'
      return
    end if
    if (len_trim(runtime_calendar_contract_id) == 0) then
      reason = 'MISSING_RUNTIME_CALENDAR_BINDING'
      return
    end if
    if (len_trim(runtime_calendar_contract_id) > len(client%runtime_calendar_contract_id)) then
      reason = 'RUNTIME_CALENDAR_BINDING_TOO_LONG'
      return
    end if
    if (producer_day_offset < 0_int64) then
      reason = 'INVALID_PRODUCER_DAY_OFFSET'
      return
    end if

    allocate(client%packets(size(packets)))
    allocate(client%producer_endpoint_key(size(packets)))
    allocate(client%producer_step_key(size(packets)))

    do i = 1, size(packets)
      call validate_hydrology_step_explicit(packets(i), kt05_status)
      if (kt05_status /= KT05_OK) then
        reason = 'INVALID_KT05_PROVIDER_PACKET'
        return
      end if

      call exact_nonnegative_integer( &
        packets(i)%producer_endpoint_day, endpoint_key, endpoint_ok)
      call exact_nonnegative_integer( &
        packets(i)%producer_step_days, step_key, step_ok)
      if (.not. endpoint_ok .or. .not. step_ok) then
        reason = 'NONEXACT_PACKET_TIME_METADATA'
        return
      end if

      do j = 1, i - 1
        if (client%producer_endpoint_key(j) == endpoint_key .and. &
            client%producer_step_key(j) == step_key) then
          reason = 'DUPLICATE_PRODUCER_INTERVAL_KEY'
          return
        end if
      end do

      client%packets(i) = packets(i)
      client%producer_endpoint_key(i) = endpoint_key
      client%producer_step_key(i) = step_key
    end do

    client%runtime_calendar_contract_id = trim(runtime_calendar_contract_id)
    client%producer_day_offset = producer_day_offset
    client%configured = .true.
    ok = .true.
    reason = 'MULTI_PACKET_PROVIDER_READY'
  end subroutine initialize_multi_packet_client

  logical function multi_packet_client_ready(client)
    type(animo_multi_packet_hydrology_runtime_probe_client_t), intent(in) :: client

    multi_packet_client_ready = .false.
    if (.not. client%configured) return
    if (.not. allocated(client%packets)) return
    if (.not. allocated(client%producer_endpoint_key)) return
    if (.not. allocated(client%producer_step_key)) return
    if (size(client%packets) <= 0) return
    if (size(client%producer_endpoint_key) /= size(client%packets)) return
    if (size(client%producer_step_key) /= size(client%packets)) return
    if (len_trim(client%runtime_calendar_contract_id) == 0) return
    if (client%producer_day_offset < 0_int64) return
    multi_packet_client_ready = .true.
  end function multi_packet_client_ready

  integer function multi_packet_packet_count(client) result(count)
    type(animo_multi_packet_hydrology_runtime_probe_client_t), intent(in) :: client

    count = 0
    if (allocated(client%packets)) count = size(client%packets)
  end function multi_packet_packet_count

  subroutine execute_multi_packet_attempt( &
      self, origin_payload, origin_time, endpoint_time, candidate_payload, &
      admissibility, ok, reason)
    class(animo_multi_packet_hydrology_runtime_probe_client_t), intent(inout) :: self
    class(transient_payload_t), intent(in) :: origin_payload
    type(TimeCoordinate), intent(in) :: origin_time, endpoint_time
    class(transient_payload_t), allocatable, intent(out) :: candidate_payload
    type(admissibility_t), intent(out) :: admissibility
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    type(animo_explicit_hydrology_runtime_probe_client_t) :: delegate
    integer(int64) :: runtime_step, expected_endpoint
    integer :: i, selected_index, match_count
    logical :: delegate_ok
    character(len=128) :: delegate_reason

    admissibility = admissibility_t()
    ok = .false.
    reason = 'UNSET'

    if (.not. multi_packet_client_ready(self)) then
      reason = 'MULTI_PACKET_PROVIDER_NOT_READY'
      return
    end if
    if (trim(origin_time%calendar_contract_id) /= &
        trim(self%runtime_calendar_contract_id) .or. &
        trim(endpoint_time%calendar_contract_id) /= &
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
    if (endpoint_time%day_index > &
        huge(expected_endpoint) - self%producer_day_offset) then
      reason = 'PRODUCER_TIME_MAPPING_OVERFLOW'
      return
    end if

    runtime_step = endpoint_time%day_index - origin_time%day_index
    expected_endpoint = endpoint_time%day_index + self%producer_day_offset

    selected_index = 0
    match_count = 0
    do i = 1, size(self%packets)
      if (self%producer_endpoint_key(i) == expected_endpoint .and. &
          self%producer_step_key(i) == runtime_step) then
        selected_index = i
        match_count = match_count + 1
      end if
    end do

    if (match_count == 0) then
      reason = 'HYDROLOGY_PACKET_NOT_FOUND'
      return
    end if
    if (match_count /= 1 .or. selected_index <= 0) then
      reason = 'AMBIGUOUS_HYDROLOGY_PACKET_SELECTION'
      return
    end if

    delegate%forcing = self%packets(selected_index)
    delegate%forcing_present = .true.
    delegate%runtime_calendar_contract_id = self%runtime_calendar_contract_id
    delegate%producer_day_offset = self%producer_day_offset

    call delegate%execute_attempt( &
      origin_payload, origin_time, endpoint_time, candidate_payload, &
      admissibility, delegate_ok, delegate_reason)

    if (.not. delegate_ok) then
      reason = trim(delegate_reason)
      return
    end if

    ok = .true.
    reason = trim(delegate_reason)
  end subroutine execute_multi_packet_attempt

end module mod_animo_multi_packet_hydrology_provider
