module mod_animo_tcd042_runoff_load_context
  use iso_fortran_env, only: real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  use mod_transient_time, only: TimeCoordinate, time_equal, time_is_valid
  implicit none
  private

  character(len=*), parameter, public :: TCD042_RUNOFF_CONTEXT_SCHEMA = &
    'ANIMO_TCD042_RUNOFF_LOAD_CONTEXT_V1'
  character(len=*), parameter, public :: TCD042_RUNOFF_CONTEXT_STAGE = &
    'REV53_POST_HYDRO_DETAILED_RUNOFF_PARTITION'

  type, public :: tcd042_runoff_load_context_t
    character(len=48) :: schema_id = ''
    character(len=64) :: resolution_stage_id = ''
    character(len=96) :: hydrology_execution_id = ''
    type(TimeCoordinate) :: origin_time
    type(TimeCoordinate) :: endpoint_time
    real(real64) :: rupr = 0.0_real64
    real(real64) :: runinu = 0.0_real64
  end type tcd042_runoff_load_context_t

  public :: make_tcd042_runoff_load_context
  public :: validate_tcd042_runoff_load_context

contains

  subroutine make_tcd042_runoff_load_context(hydrology_execution_id, origin_time, endpoint_time, &
      rupr, runinu, value, ok, reason)
    character(len=*), intent(in) :: hydrology_execution_id
    type(TimeCoordinate), intent(in) :: origin_time, endpoint_time
    real(real64), intent(in) :: rupr, runinu
    type(tcd042_runoff_load_context_t), intent(out) :: value
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    value = tcd042_runoff_load_context_t()
    value%schema_id = TCD042_RUNOFF_CONTEXT_SCHEMA
    value%resolution_stage_id = TCD042_RUNOFF_CONTEXT_STAGE
    value%hydrology_execution_id = hydrology_execution_id
    value%origin_time = origin_time
    value%endpoint_time = endpoint_time
    value%rupr = rupr
    value%runinu = runinu

    call validate_intrinsic(value, ok, reason)
  end subroutine make_tcd042_runoff_load_context

  subroutine validate_tcd042_runoff_load_context(value, expected_origin, expected_endpoint, &
      expected_execution_id, ok, reason)
    type(tcd042_runoff_load_context_t), intent(in) :: value
    type(TimeCoordinate), intent(in) :: expected_origin, expected_endpoint
    character(len=*), intent(in) :: expected_execution_id
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    logical :: equal, compare_ok

    call validate_intrinsic(value, ok, reason)
    if (.not. ok) return

    if (trim(value%hydrology_execution_id) /= trim(expected_execution_id)) then
      ok = .false.
      reason = 'RUNOFF_CONTEXT_EXECUTION_ID_MISMATCH'
      return
    end if

    call time_equal(value%origin_time, expected_origin, equal, compare_ok)
    if (.not. compare_ok .or. .not. equal) then
      ok = .false.
      reason = 'RUNOFF_CONTEXT_ORIGIN_MISMATCH'
      return
    end if

    call time_equal(value%endpoint_time, expected_endpoint, equal, compare_ok)
    if (.not. compare_ok .or. .not. equal) then
      ok = .false.
      reason = 'RUNOFF_CONTEXT_ENDPOINT_MISMATCH'
      return
    end if

    ok = .true.
    reason = 'VALID_TCD042_RUNOFF_LOAD_CONTEXT'
  end subroutine validate_tcd042_runoff_load_context

  subroutine validate_intrinsic(value, ok, reason)
    type(tcd042_runoff_load_context_t), intent(in) :: value
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    ok = .false.
    reason = 'UNSET'

    if (trim(value%schema_id) /= TCD042_RUNOFF_CONTEXT_SCHEMA) then
      reason = 'RUNOFF_CONTEXT_SCHEMA_MISMATCH'
      return
    end if
    if (trim(value%resolution_stage_id) /= TCD042_RUNOFF_CONTEXT_STAGE) then
      reason = 'RUNOFF_CONTEXT_STAGE_MISMATCH'
      return
    end if
    if (len_trim(value%hydrology_execution_id) == 0) then
      reason = 'MISSING_RUNOFF_CONTEXT_EXECUTION_ID'
      return
    end if
    if (.not. time_is_valid(value%origin_time) .or. .not. time_is_valid(value%endpoint_time)) then
      reason = 'INVALID_RUNOFF_CONTEXT_TIME'
      return
    end if
    if (value%origin_time%subday_numerator /= 0 .or. value%endpoint_time%subday_numerator /= 0) then
      reason = 'SUBDAY_RUNOFF_CONTEXT_NOT_QUALIFIED'
      return
    end if
    if (trim(value%origin_time%calendar_contract_id) /= trim(value%endpoint_time%calendar_contract_id)) then
      reason = 'RUNOFF_CONTEXT_CALENDAR_MISMATCH'
      return
    end if
    if (value%endpoint_time%day_index <= value%origin_time%day_index) then
      reason = 'RUNOFF_CONTEXT_INTERVAL_NOT_FORWARD'
      return
    end if
    if (.not. ieee_is_finite(value%rupr) .or. .not. ieee_is_finite(value%runinu)) then
      reason = 'NONFINITE_RUNOFF_CONTEXT'
      return
    end if

    ! No additional sign or reconstruction rule is imposed here.
    ! These are captured outputs from the qualified hydrology responsibility.
    ok = .true.
    reason = 'VALID_INTRINSIC_TCD042_RUNOFF_LOAD_CONTEXT'
  end subroutine validate_intrinsic

end module mod_animo_tcd042_runoff_load_context
