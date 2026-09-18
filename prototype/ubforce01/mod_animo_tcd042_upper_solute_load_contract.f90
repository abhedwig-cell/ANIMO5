module mod_animo_tcd042_upper_solute_load_contract
  use iso_fortran_env, only: int64, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  use mod_transient_time, only: TimeCoordinate, time_equal, time_is_valid
  implicit none
  private

  character(len=*), parameter, public :: TCD042_UPPER_LOAD_SCHEMA = &
    'ANIMO_TCD042_UPPER_SOLUTE_LOADS_V1'
  character(len=*), parameter, public :: TCD042_UPPER_LOAD_UNITS = &
    'KG_CONSTITUENT_M-2_D-1'
  character(len=*), parameter, public :: TCD042_UPPER_LOAD_MODE = &
    'REV53_IWA2_IOPTHYVS1_DETAILED'

  type, public :: tcd042_upper_loads_t
    character(len=48) :: schema_id = ''
    character(len=48) :: unit_contract_id = ''
    character(len=64) :: forcing_mode_id = ''
    character(len=96) :: forcing_execution_id = ''
    type(TimeCoordinate) :: origin_time
    type(TimeCoordinate) :: endpoint_time
    real(real64) :: load1_nh = 0.0_real64
    real(real64) :: load2_ni = 0.0_real64
    real(real64) :: load3_diorma = 0.0_real64
    real(real64) :: load4_diorni = 0.0_real64
    logical :: phosphorus_enabled = .false.
    logical :: has_phosphorus_loads = .false.
    real(real64) :: load5_po = 0.0_real64
    real(real64) :: load6_diorpo = 0.0_real64
  end type tcd042_upper_loads_t

  public :: make_tcd042_upper_loads
  public :: validate_tcd042_upper_loads
  public :: select_tcd042_load_channel

contains

  logical function exact_binary_zero(value)
    real(real64), intent(in) :: value
    integer(int64) :: bits
    bits = transfer(value, bits)
    exact_binary_zero = iand(bits, int(z'7FFFFFFFFFFFFFFF', int64)) == 0_int64
  end function exact_binary_zero

  subroutine make_tcd042_upper_loads(forcing_execution_id, origin_time, endpoint_time, &
      load1_nh, load2_ni, load3_diorma, load4_diorni, phosphorus_enabled, &
      load5_po, load6_diorpo, value, ok, reason)
    character(len=*), intent(in) :: forcing_execution_id
    type(TimeCoordinate), intent(in) :: origin_time, endpoint_time
    real(real64), intent(in) :: load1_nh, load2_ni, load3_diorma, load4_diorni
    logical, intent(in) :: phosphorus_enabled
    real(real64), intent(in) :: load5_po, load6_diorpo
    type(tcd042_upper_loads_t), intent(out) :: value
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    value = tcd042_upper_loads_t()
    value%schema_id = TCD042_UPPER_LOAD_SCHEMA
    value%unit_contract_id = TCD042_UPPER_LOAD_UNITS
    value%forcing_mode_id = TCD042_UPPER_LOAD_MODE
    value%forcing_execution_id = forcing_execution_id
    value%origin_time = origin_time
    value%endpoint_time = endpoint_time
    value%load1_nh = load1_nh
    value%load2_ni = load2_ni
    value%load3_diorma = load3_diorma
    value%load4_diorni = load4_diorni
    value%phosphorus_enabled = phosphorus_enabled
    value%has_phosphorus_loads = phosphorus_enabled
    value%load5_po = load5_po
    value%load6_diorpo = load6_diorpo

    call validate_intrinsic(value, ok, reason)
  end subroutine make_tcd042_upper_loads

  subroutine validate_tcd042_upper_loads(value, expected_origin, expected_endpoint, ok, reason)
    type(tcd042_upper_loads_t), intent(in) :: value
    type(TimeCoordinate), intent(in) :: expected_origin, expected_endpoint
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    logical :: equal, compare_ok

    call validate_intrinsic(value, ok, reason)
    if (.not. ok) return

    call time_equal(value%origin_time, expected_origin, equal, compare_ok)
    if (.not. compare_ok .or. .not. equal) then
      ok = .false.
      reason = 'UPPER_LOAD_ORIGIN_MISMATCH'
      return
    end if
    call time_equal(value%endpoint_time, expected_endpoint, equal, compare_ok)
    if (.not. compare_ok .or. .not. equal) then
      ok = .false.
      reason = 'UPPER_LOAD_ENDPOINT_MISMATCH'
      return
    end if

    ok = .true.
    reason = 'VALID_TCD042_UPPER_SOLUTE_LOADS'
  end subroutine validate_tcd042_upper_loads

  subroutine select_tcd042_load_channel(value, channel_id, load_rate, ok, reason)
    type(tcd042_upper_loads_t), intent(in) :: value
    integer, intent(in) :: channel_id
    real(real64), intent(out) :: load_rate
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    load_rate = 0.0_real64
    call validate_intrinsic(value, ok, reason)
    if (.not. ok) return

    select case(channel_id)
    case(1)
      load_rate = value%load1_nh
    case(2)
      load_rate = value%load2_ni
    case(3)
      load_rate = value%load3_diorma
    case(4)
      load_rate = value%load4_diorni
    case(5)
      if (.not. value%has_phosphorus_loads) then
        ok = .false.
        reason = 'PHOSPHORUS_LOADS_UNAVAILABLE'
        return
      end if
      load_rate = value%load5_po
    case(6)
      if (.not. value%has_phosphorus_loads) then
        ok = .false.
        reason = 'PHOSPHORUS_LOADS_UNAVAILABLE'
        return
      end if
      load_rate = value%load6_diorpo
    case default
      ok = .false.
      reason = 'INVALID_TCD042_LOAD_CHANNEL'
      return
    end select

    ok = .true.
    reason = 'TCD042_LOAD_CHANNEL_SELECTED'
  end subroutine select_tcd042_load_channel

  subroutine validate_intrinsic(value, ok, reason)
    type(tcd042_upper_loads_t), intent(in) :: value
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    real(real64) :: core(4), pvals(2)

    ok = .false.
    reason = 'UNSET'

    if (trim(value%schema_id) /= TCD042_UPPER_LOAD_SCHEMA) then
      reason = 'UPPER_LOAD_SCHEMA_MISMATCH'
      return
    end if
    if (trim(value%unit_contract_id) /= TCD042_UPPER_LOAD_UNITS) then
      reason = 'UPPER_LOAD_UNIT_CONTRACT_MISMATCH'
      return
    end if
    if (trim(value%forcing_mode_id) /= TCD042_UPPER_LOAD_MODE) then
      reason = 'UPPER_LOAD_MODE_MISMATCH'
      return
    end if
    if (len_trim(value%forcing_execution_id) == 0) then
      reason = 'MISSING_UPPER_LOAD_EXECUTION_ID'
      return
    end if
    if (.not. time_is_valid(value%origin_time) .or. .not. time_is_valid(value%endpoint_time)) then
      reason = 'INVALID_UPPER_LOAD_TIME'
      return
    end if
    if (value%origin_time%subday_numerator /= 0_int64 .or. &
        value%endpoint_time%subday_numerator /= 0_int64) then
      reason = 'SUBDAY_UPPER_LOAD_FORCING_NOT_QUALIFIED'
      return
    end if
    if (trim(value%origin_time%calendar_contract_id) /= trim(value%endpoint_time%calendar_contract_id)) then
      reason = 'UPPER_LOAD_CALENDAR_MISMATCH'
      return
    end if
    if (value%endpoint_time%day_index <= value%origin_time%day_index) then
      reason = 'UPPER_LOAD_INTERVAL_NOT_FORWARD'
      return
    end if

    core = [value%load1_nh, value%load2_ni, value%load3_diorma, value%load4_diorni]
    if (.not. all(ieee_is_finite(core))) then
      reason = 'NONFINITE_CORE_UPPER_LOAD'
      return
    end if

    if (value%phosphorus_enabled .neqv. value%has_phosphorus_loads) then
      reason = 'PHOSPHORUS_LOAD_PRESENCE_MISMATCH'
      return
    end if
    pvals = [value%load5_po, value%load6_diorpo]
    if (.not. all(ieee_is_finite(pvals))) then
      reason = 'NONFINITE_PHOSPHORUS_UPPER_LOAD'
      return
    end if
    if (.not. value%phosphorus_enabled) then
      if (.not. exact_binary_zero(value%load5_po) .or. &
          .not. exact_binary_zero(value%load6_diorpo)) then
        reason = 'INACTIVE_PHOSPHORUS_LOADS_MUST_BE_EXACT_ZERO'
        return
      end if
    end if

    ok = .true.
    reason = 'VALID_INTRINSIC_TCD042_UPPER_SOLUTE_LOADS'
  end subroutine validate_intrinsic

end module mod_animo_tcd042_upper_solute_load_contract
