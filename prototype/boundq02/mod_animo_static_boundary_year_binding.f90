module mod_animo_static_boundary_year_binding
  use iso_fortran_env, only: int64, real64
  use mod_transient_time, only: TimeCoordinate, time_compare, time_equal, time_is_valid
  use mod_animo_static_boundary_chemistry_adapter, only: &
    static_boundary_chemistry_t, validate_rev53_static_boundary_chemistry, BOUNDQ01_OK
  use mod_animo_tcd042_upper_solute_load_resolver, only: &
    tcd042_precip_chemistry_t, tcd042_six_channel_chemistry_t, &
    tcd042_upper_chemistry_forcing_t, make_tcd042_upper_chemistry_forcing
  implicit none
  private

  character(len=*), parameter, public :: BOUNDQ02_CALENDAR_ID = &
    'ANIMO_PG_86400_NOLEAPSECONDS_V1'
  character(len=*), parameter, public :: BOUNDQ02_CURSOR_SCHEMA = &
    'ANIMO_REV53_BOUNDARY_YEAR_CURSOR_V1'
  character(len=*), parameter, public :: BOUNDQ02_FRAME_SCHEMA = &
    'ANIMO_REV53_STATIC_BOUNDARY_INTERVAL_FRAME_V1'
  integer, parameter, public :: BOUNDQ02_MAX_LEGACY_YEAR = 3000

  type, public :: boundary_year_cursor_t
    character(len=48) :: schema_id = ''
    logical :: initialized = .false.
    integer :: active_year = 0
    integer :: active_slot = 0
  end type boundary_year_cursor_t

  type, public :: static_boundary_interval_frame_t
    character(len=48) :: schema_id = ''
    character(len=96) :: boundary_source_id = ''
    type(TimeCoordinate) :: origin_time
    type(TimeCoordinate) :: endpoint_time
    integer :: selected_year = 0
    integer :: selected_slot = 0
    type(tcd042_upper_chemistry_forcing_t) :: chemistry
    real(real64) :: dry_deposition_nh = 0.0_real64
    real(real64) :: dry_deposition_ni = 0.0_real64
  end type static_boundary_interval_frame_t

  public :: initialize_boundary_year_cursor
  public :: bind_static_boundary_interval
  public :: validate_static_boundary_interval_frame
  public :: civil_date_from_time

contains

  subroutine initialize_boundary_year_cursor(cursor)
    type(boundary_year_cursor_t), intent(out) :: cursor
    cursor = boundary_year_cursor_t()
    cursor%schema_id = BOUNDQ02_CURSOR_SCHEMA
  end subroutine initialize_boundary_year_cursor

  logical function leap_year(year)
    integer, intent(in) :: year
    leap_year = mod(year,4) == 0 .and. (mod(year,100) /= 0 .or. mod(year,400) == 0)
  end function leap_year

  integer function days_in_month(year, month) result(value)
    integer, intent(in) :: year, month
    integer, parameter :: common_days(12) = [31,28,31,30,31,30,31,31,30,31,30,31]
    value = 0
    if (month < 1 .or. month > 12) return
    value = common_days(month)
    if (month == 2 .and. leap_year(year)) value = 29
  end function days_in_month

  subroutine civil_date_from_time(time, year, month, day, ok, reason)
    type(TimeCoordinate), intent(in) :: time
    integer, intent(out) :: year, month, day
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    integer(int64) :: remaining
    integer :: y, m, dy

    year = 0
    month = 0
    day = 0
    ok = .false.
    reason = 'UNSET'

    if (.not. time_is_valid(time)) then
      reason = 'INVALID_TIME_COORDINATE'
      return
    end if
    if (trim(time%calendar_contract_id) /= BOUNDQ02_CALENDAR_ID) then
      reason = 'BOUNDQ02_CALENDAR_CONTRACT_MISMATCH'
      return
    end if
    if (time%subday_numerator /= 0_int64) then
      reason = 'SUBDAY_BOUNDARY_YEAR_SELECTION_NOT_QUALIFIED'
      return
    end if
    if (time%day_index < 0_int64) then
      reason = 'BOUNDQ02_YEAR_BEFORE_LEGACY_ENVELOPE'
      return
    end if

    remaining = time%day_index
    do y = 1, BOUNDQ02_MAX_LEGACY_YEAR
      dy = 365
      if (leap_year(y)) dy = 366
      if (remaining < int(dy,int64)) then
        year = y
        exit
      end if
      remaining = remaining - int(dy,int64)
    end do
    if (year == 0) then
      reason = 'BOUNDQ02_YEAR_AFTER_LEGACY_ENVELOPE'
      return
    end if

    do m = 1, 12
      dy = days_in_month(year,m)
      if (remaining < int(dy,int64)) then
        month = m
        day = int(remaining) + 1
        ok = .true.
        reason = 'VALID_BOUNDQ02_CIVIL_DATE'
        return
      end if
      remaining = remaining - int(dy,int64)
    end do

    reason = 'BOUNDQ02_CIVIL_DATE_CONVERSION_FAILED'
  end subroutine civil_date_from_time

  subroutine bind_static_boundary_interval(boundary, boundary_source_id, simulation_start_year, &
      accepted_cursor, origin_time, endpoint_time, frame, next_cursor, ok, reason)
    type(static_boundary_chemistry_t), intent(in) :: boundary
    character(len=*), intent(in) :: boundary_source_id
    integer, intent(in) :: simulation_start_year
    type(boundary_year_cursor_t), intent(in) :: accepted_cursor
    type(TimeCoordinate), intent(in) :: origin_time, endpoint_time
    type(static_boundary_interval_frame_t), intent(out) :: frame
    type(boundary_year_cursor_t), intent(out) :: next_cursor
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    integer :: source_status, ordering
    integer :: origin_year, origin_month, origin_day, endpoint_year, endpoint_month, endpoint_day
    integer :: slot
    logical :: compare_ok, chemistry_ok
    character(len=32) :: slot_text
    character(len=96) :: forcing_id
    character(len=128) :: local_reason
    type(tcd042_precip_chemistry_t) :: precipitation
    type(tcd042_six_channel_chemistry_t) :: irrigation, runon_chemistry, runin

    frame = static_boundary_interval_frame_t()
    next_cursor = accepted_cursor
    ok = .false.
    reason = 'UNSET'

    if (trim(accepted_cursor%schema_id) /= BOUNDQ02_CURSOR_SCHEMA) then
      reason = 'BOUNDQ02_CURSOR_SCHEMA_MISMATCH'
      return
    end if
    if (len_trim(boundary_source_id) == 0) then
      reason = 'MISSING_BOUNDARY_SOURCE_ID'
      return
    end if
    if (simulation_start_year < 1 .or. simulation_start_year > BOUNDQ02_MAX_LEGACY_YEAR) then
      reason = 'INVALID_BOUNDQ02_SIMULATION_START_YEAR'
      return
    end if

    call validate_rev53_static_boundary_chemistry(boundary, source_status)
    if (source_status /= BOUNDQ01_OK) then
      reason = 'INVALID_BOUNDQ01_STATIC_BOUNDARY'
      return
    end if

    call civil_date_from_time(origin_time, origin_year, origin_month, origin_day, compare_ok, local_reason)
    if (.not. compare_ok) then
      reason = trim(local_reason)
      return
    end if
    call civil_date_from_time(endpoint_time, endpoint_year, endpoint_month, endpoint_day, compare_ok, local_reason)
    if (.not. compare_ok) then
      reason = trim(local_reason)
      return
    end if
    call time_compare(endpoint_time, origin_time, ordering, compare_ok)
    if (.not. compare_ok .or. ordering <= 0) then
      reason = 'INVALID_BOUNDQ02_INTERVAL'
      return
    end if

    ! Exact revision-53 Init semantics:
    ! the yearly chemistry scalars are refreshed on the first interval and
    ! thereafter only when the interval origin is exactly 1 January.
    if (.not. accepted_cursor%initialized) then
      slot = origin_year - simulation_start_year + 1
    else if (origin_month == 1 .and. origin_day == 1) then
      slot = origin_year - simulation_start_year + 1
    else
      slot = accepted_cursor%active_slot
    end if

    if (slot < 1 .or. slot > boundary%nuyr) then
      reason = 'BOUNDQ02_YEAR_SLOT_OUT_OF_RANGE'
      return
    end if

    next_cursor%schema_id = BOUNDQ02_CURSOR_SCHEMA
    next_cursor%initialized = .true.
    next_cursor%active_slot = slot
    next_cursor%active_year = simulation_start_year + slot - 1

    precipitation = tcd042_precip_chemistry_t()
    precipitation%nh = boundary%precipitation_nh(slot)
    precipitation%ni = boundary%precipitation_ni(slot)
    if (boundary%phosphorus_enabled) precipitation%po = boundary%precipitation_po(slot)

    irrigation = tcd042_six_channel_chemistry_t()
    irrigation%nh = boundary%irrigation%nh
    irrigation%ni = boundary%irrigation%ni
    irrigation%doma = boundary%irrigation%doma
    irrigation%don = boundary%irrigation%don
    irrigation%po = boundary%irrigation%po
    irrigation%dop = boundary%irrigation%dop

    runon_chemistry = tcd042_six_channel_chemistry_t()
    runon_chemistry%nh = boundary%runon%nh
    runon_chemistry%ni = boundary%runon%ni
    runon_chemistry%doma = boundary%runon%doma
    runon_chemistry%don = boundary%runon%don
    runon_chemistry%po = boundary%runon%po
    runon_chemistry%dop = boundary%runon%dop

    runin = tcd042_six_channel_chemistry_t()
    runin%nh = boundary%runin%nh
    runin%ni = boundary%runin%ni
    runin%doma = boundary%runin%doma
    runin%don = boundary%runin%don
    runin%po = boundary%runin%po
    runin%dop = boundary%runin%dop

    write(slot_text,'(I0)') slot
    if (len_trim(boundary_source_id) + len(':SLOT=') + len_trim(slot_text) > len(forcing_id)) then
      reason = 'BOUNDQ02_FORCING_ID_TOO_LONG'
      return
    end if
    forcing_id = trim(boundary_source_id)//':SLOT='//trim(slot_text)

    call make_tcd042_upper_chemistry_forcing(trim(forcing_id), boundary%phosphorus_enabled, &
      precipitation, irrigation, runon_chemistry, runin, frame%chemistry, chemistry_ok, local_reason)
    if (.not. chemistry_ok) then
      reason = 'BOUNDQ02_UBFORCE02_CHEMISTRY_CONSTRUCTION_FAILED'
      return
    end if

    frame%schema_id = BOUNDQ02_FRAME_SCHEMA
    frame%boundary_source_id = boundary_source_id
    frame%origin_time = origin_time
    frame%endpoint_time = endpoint_time
    frame%selected_year = next_cursor%active_year
    frame%selected_slot = slot
    frame%dry_deposition_nh = boundary%dry_deposition_nh(slot)
    frame%dry_deposition_ni = boundary%dry_deposition_ni(slot)

    call validate_static_boundary_interval_frame(frame, origin_time, endpoint_time, ok, local_reason)
    if (.not. ok) then
      reason = trim(local_reason)
      return
    end if

    reason = 'REV53_STATIC_BOUNDARY_INTERVAL_BOUND'
  end subroutine bind_static_boundary_interval

  subroutine validate_static_boundary_interval_frame(frame, expected_origin, expected_endpoint, ok, reason)
    type(static_boundary_interval_frame_t), intent(in) :: frame
    type(TimeCoordinate), intent(in) :: expected_origin, expected_endpoint
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    logical :: equal, compare_ok

    ok = .false.
    reason = 'UNSET'

    if (trim(frame%schema_id) /= BOUNDQ02_FRAME_SCHEMA) then
      reason = 'BOUNDQ02_FRAME_SCHEMA_MISMATCH'
      return
    end if
    if (len_trim(frame%boundary_source_id) == 0) then
      reason = 'MISSING_BOUNDQ02_FRAME_SOURCE_ID'
      return
    end if
    if (frame%selected_year < 1 .or. frame%selected_year > BOUNDQ02_MAX_LEGACY_YEAR .or. &
        frame%selected_slot < 1) then
      reason = 'INVALID_BOUNDQ02_FRAME_YEAR_SLOT'
      return
    end if
    call time_equal(frame%origin_time, expected_origin, equal, compare_ok)
    if (.not. compare_ok .or. .not. equal) then
      reason = 'BOUNDQ02_FRAME_ORIGIN_MISMATCH'
      return
    end if
    call time_equal(frame%endpoint_time, expected_endpoint, equal, compare_ok)
    if (.not. compare_ok .or. .not. equal) then
      reason = 'BOUNDQ02_FRAME_ENDPOINT_MISMATCH'
      return
    end if

    ok = .true.
    reason = 'VALID_BOUNDQ02_STATIC_BOUNDARY_INTERVAL_FRAME'
  end subroutine validate_static_boundary_interval_frame

end module mod_animo_static_boundary_year_binding
