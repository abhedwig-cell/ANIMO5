module mod_animo_resolved_upper_hydrology_contract
  use iso_fortran_env, only: int64, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  use mod_transient_time, only: TimeCoordinate, time_equal, time_is_valid
  implicit none
  private

  character(len=*), parameter, public :: RESOLVED_UPPER_HYDROLOGY_SCHEMA = &
    'ANIMO_TCD042_RESOLVED_UPPER_HYDROLOGY_V1'
  character(len=*), parameter, public :: RESOLVED_HYDROLOGY_UNITS = &
    'ANIMO_RESOLVED_HYDROLOGY_UNITS_V1'
  character(len=*), parameter, public :: RESOLUTION_STAGE = &
    'REV53_HYDRO_DETAILED_THEN_MODFLUX'

  type, public :: resolved_upper_hydrology_t
    character(len=48) :: schema_id = ''
    character(len=48) :: unit_contract_id = ''
    character(len=64) :: resolution_stage_id = ''
    character(len=96) :: execution_id = ''
    type(TimeCoordinate) :: origin_time
    type(TimeCoordinate) :: endpoint_time
    integer :: flpn = -1
    real(real64) :: flib_top = 0.0_real64
    real(real64) :: rurv = 0.0_real64
  end type resolved_upper_hydrology_t

  public :: make_resolved_upper_hydrology
  public :: validate_tcd042_resolved_upper_hydrology

contains

  logical function exact_binary_zero(value)
    real(real64), intent(in) :: value
    integer(int64) :: bits
    bits = transfer(value, bits)
    exact_binary_zero = iand(bits, int(z'7FFFFFFFFFFFFFFF', int64)) == 0_int64
  end function exact_binary_zero

  subroutine make_resolved_upper_hydrology(execution_id, origin_time, endpoint_time, &
      flpn, flib_top, rurv, value, ok, reason)
    character(len=*), intent(in) :: execution_id
    type(TimeCoordinate), intent(in) :: origin_time, endpoint_time
    integer, intent(in) :: flpn
    real(real64), intent(in) :: flib_top, rurv
    type(resolved_upper_hydrology_t), intent(out) :: value
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    value = resolved_upper_hydrology_t()
    value%schema_id = RESOLVED_UPPER_HYDROLOGY_SCHEMA
    value%unit_contract_id = RESOLVED_HYDROLOGY_UNITS
    value%resolution_stage_id = RESOLUTION_STAGE
    value%execution_id = execution_id
    value%origin_time = origin_time
    value%endpoint_time = endpoint_time
    value%flpn = flpn
    value%flib_top = flib_top
    value%rurv = rurv

    call validate_intrinsic(value, ok, reason)
  end subroutine make_resolved_upper_hydrology

  subroutine validate_tcd042_resolved_upper_hydrology(value, expected_origin, expected_endpoint, ok, reason)
    type(resolved_upper_hydrology_t), intent(in) :: value
    type(TimeCoordinate), intent(in) :: expected_origin, expected_endpoint
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    logical :: equal, compare_ok

    call validate_intrinsic(value, ok, reason)
    if (.not. ok) return

    call time_equal(value%origin_time, expected_origin, equal, compare_ok)
    if (.not. compare_ok .or. .not. equal) then
      ok = .false.
      reason = 'RESOLVED_HYDROLOGY_ORIGIN_MISMATCH'
      return
    end if

    call time_equal(value%endpoint_time, expected_endpoint, equal, compare_ok)
    if (.not. compare_ok .or. .not. equal) then
      ok = .false.
      reason = 'RESOLVED_HYDROLOGY_ENDPOINT_MISMATCH'
      return
    end if

    ok = .true.
    reason = 'VALID_TCD042_RESOLVED_UPPER_HYDROLOGY'
  end subroutine validate_tcd042_resolved_upper_hydrology

  subroutine validate_intrinsic(value, ok, reason)
    type(resolved_upper_hydrology_t), intent(in) :: value
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    ok = .false.
    reason = 'UNSET'

    if (trim(value%schema_id) /= RESOLVED_UPPER_HYDROLOGY_SCHEMA) then
      reason = 'RESOLVED_HYDROLOGY_SCHEMA_MISMATCH'
      return
    end if
    if (trim(value%unit_contract_id) /= RESOLVED_HYDROLOGY_UNITS) then
      reason = 'RESOLVED_HYDROLOGY_UNIT_CONTRACT_MISMATCH'
      return
    end if
    if (trim(value%resolution_stage_id) /= RESOLUTION_STAGE) then
      reason = 'RESOLUTION_STAGE_MISMATCH'
      return
    end if
    if (len_trim(value%execution_id) == 0) then
      reason = 'MISSING_HYDROLOGY_EXECUTION_ID'
      return
    end if
    if (.not. time_is_valid(value%origin_time) .or. .not. time_is_valid(value%endpoint_time)) then
      reason = 'INVALID_RESOLVED_HYDROLOGY_TIME'
      return
    end if
    if (value%origin_time%subday_numerator /= 0_int64 .or. &
        value%endpoint_time%subday_numerator /= 0_int64) then
      reason = 'SUBDAY_RESOLVED_HYDROLOGY_NOT_QUALIFIED'
      return
    end if
    if (trim(value%origin_time%calendar_contract_id) /= trim(value%endpoint_time%calendar_contract_id)) then
      reason = 'RESOLVED_HYDROLOGY_CALENDAR_MISMATCH'
      return
    end if
    if (value%endpoint_time%day_index <= value%origin_time%day_index) then
      reason = 'RESOLVED_HYDROLOGY_INTERVAL_NOT_FORWARD'
      return
    end if

    ! HYDROQ01 is intentionally bounded to the admitted TCD-042 no-ponding branch.
    if (value%flpn /= 0) then
      reason = 'FLPN_OUTSIDE_TCD042_RESOLVED_CONTRACT'
      return
    end if
    if (.not. ieee_is_finite(value%flib_top) .or. value%flib_top < 0.0_real64) then
      reason = 'INVALID_POST_MODFLUX_FLIB_TOP'
      return
    end if
    if (.not. ieee_is_finite(value%rurv) .or. .not. exact_binary_zero(value%rurv)) then
      reason = 'RURV_MUST_BE_EXACT_ZERO_FOR_REV53_FLPN_ZERO'
      return
    end if

    ok = .true.
    reason = 'VALID_INTRINSIC_RESOLVED_UPPER_HYDROLOGY'
  end subroutine validate_intrinsic

end module mod_animo_resolved_upper_hydrology_contract
