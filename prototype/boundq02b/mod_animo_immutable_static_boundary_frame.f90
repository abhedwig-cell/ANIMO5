module mod_animo_immutable_static_boundary_frame
  use iso_fortran_env, only: real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  use mod_transient_time, only: TimeCoordinate, time_equal
  use mod_animo_static_boundary_chemistry_adapter, only: static_boundary_chemistry_t
  use mod_animo_static_boundary_year_binding, only: &
    boundary_year_cursor_t, static_boundary_interval_frame_t, &
    bind_static_boundary_interval, validate_static_boundary_interval_frame
  use mod_animo_tcd042_upper_solute_load_resolver, only: &
    tcd042_upper_chemistry_forcing_t, make_tcd042_upper_chemistry_forcing
  implicit none
  private

  character(len=*), parameter, public :: BOUNDQ02B_FRAME_SCHEMA = &
    'ANIMO_IMMUTABLE_STATIC_BOUNDARY_FRAME_V1'

  type, public :: immutable_static_boundary_interval_frame_t
    private
    character(len=48) :: schema_id = ''
    character(len=64) :: boundary_content_sha256 = ''
    type(TimeCoordinate) :: origin_time
    type(TimeCoordinate) :: endpoint_time
    integer :: simulation_start_year = 0
    integer :: boundary_nuyr = 0
    integer :: selected_year = 0
    integer :: selected_slot = 0
    type(tcd042_upper_chemistry_forcing_t) :: chemistry
    real(real64) :: dry_deposition_nh = 0.0_real64
    real(real64) :: dry_deposition_ni = 0.0_real64
  end type immutable_static_boundary_interval_frame_t

  public :: make_immutable_static_boundary_interval_frame
  public :: validate_immutable_static_boundary_interval_frame
  public :: inspect_immutable_static_boundary_interval_frame

contains

  logical function canonical_sha256(value)
    character(len=*), intent(in) :: value
    integer :: i, code

    canonical_sha256 = .false.
    if (len_trim(value) /= 64) return
    do i = 1, 64
      code = iachar(value(i:i))
      if (.not. ((code >= iachar('0') .and. code <= iachar('9')) .or. &
                 (code >= iachar('a') .and. code <= iachar('f')))) return
    end do
    canonical_sha256 = .true.
  end function canonical_sha256

  subroutine expected_forcing_id(content_sha256, slot, forcing_id, ok)
    character(len=*), intent(in) :: content_sha256
    integer, intent(in) :: slot
    character(len=*), intent(out) :: forcing_id
    logical, intent(out) :: ok
    character(len=32) :: slot_text
    integer :: required

    forcing_id = ''
    ok = .false.
    if (.not. canonical_sha256(content_sha256)) return
    if (slot <= 0) return

    write(slot_text,'(I0)') slot
    required = len('SHA256=') + 64 + len(':SLOT=') + len_trim(slot_text)
    if (required > len(forcing_id)) return
    forcing_id = 'SHA256='//trim(content_sha256)//':SLOT='//trim(slot_text)
    ok = .true.
  end subroutine expected_forcing_id

  subroutine make_immutable_static_boundary_interval_frame(boundary, boundary_content_sha256, &
      simulation_start_year, accepted_cursor, origin_time, endpoint_time, frame, next_cursor, ok, reason)
    type(static_boundary_chemistry_t), intent(in) :: boundary
    character(len=*), intent(in) :: boundary_content_sha256
    integer, intent(in) :: simulation_start_year
    type(boundary_year_cursor_t), intent(in) :: accepted_cursor
    type(TimeCoordinate), intent(in) :: origin_time, endpoint_time
    type(immutable_static_boundary_interval_frame_t), intent(out) :: frame
    type(boundary_year_cursor_t), intent(out) :: next_cursor
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    type(static_boundary_interval_frame_t) :: mutable_frame
    character(len=80) :: source_id
    character(len=128) :: local_reason
    logical :: mutable_ok

    frame = immutable_static_boundary_interval_frame_t()
    next_cursor = accepted_cursor
    ok = .false.
    reason = 'UNSET'

    if (.not. canonical_sha256(boundary_content_sha256)) then
      reason = 'BOUNDQ02B_NONCANONICAL_CONTENT_SHA256'
      return
    end if

    source_id = 'SHA256='//trim(boundary_content_sha256)
    call bind_static_boundary_interval(boundary, trim(source_id), simulation_start_year, &
      accepted_cursor, origin_time, endpoint_time, mutable_frame, next_cursor, mutable_ok, local_reason)
    if (.not. mutable_ok) then
      reason = 'BOUNDQ02B_BOUNDQ02_BIND_FAILED'
      return
    end if

    call validate_static_boundary_interval_frame(mutable_frame, origin_time, endpoint_time, &
      mutable_ok, local_reason)
    if (.not. mutable_ok) then
      reason = 'BOUNDQ02B_BOUNDQ02_FRAME_INVALID'
      return
    end if

    frame%schema_id = BOUNDQ02B_FRAME_SCHEMA
    frame%boundary_content_sha256 = boundary_content_sha256(1:64)
    frame%origin_time = mutable_frame%origin_time
    frame%endpoint_time = mutable_frame%endpoint_time
    frame%simulation_start_year = mutable_frame%simulation_start_year
    frame%boundary_nuyr = mutable_frame%boundary_nuyr
    frame%selected_year = mutable_frame%selected_year
    frame%selected_slot = mutable_frame%selected_slot
    frame%chemistry = mutable_frame%chemistry
    frame%dry_deposition_nh = mutable_frame%dry_deposition_nh
    frame%dry_deposition_ni = mutable_frame%dry_deposition_ni

    call validate_immutable_static_boundary_interval_frame(frame, origin_time, endpoint_time, ok, local_reason)
    if (.not. ok) then
      reason = trim(local_reason)
      return
    end if

    reason = 'IMMUTABLE_STATIC_BOUNDARY_INTERVAL_FRAME_CREATED'
  end subroutine make_immutable_static_boundary_interval_frame

  subroutine validate_immutable_static_boundary_interval_frame(frame, expected_origin, expected_endpoint, ok, reason)
    type(immutable_static_boundary_interval_frame_t), intent(in) :: frame
    type(TimeCoordinate), intent(in) :: expected_origin, expected_endpoint
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    logical :: equal, compare_ok, id_ok, chemistry_ok
    character(len=96) :: forcing_id
    character(len=128) :: chemistry_reason
    type(tcd042_upper_chemistry_forcing_t) :: rebuilt

    ok = .false.
    reason = 'UNSET'

    if (trim(frame%schema_id) /= BOUNDQ02B_FRAME_SCHEMA) then
      reason = 'BOUNDQ02B_FRAME_SCHEMA_MISMATCH'
      return
    end if
    if (.not. canonical_sha256(frame%boundary_content_sha256)) then
      reason = 'BOUNDQ02B_FRAME_CONTENT_ID_INVALID'
      return
    end if
    if (frame%simulation_start_year < 1 .or. frame%boundary_nuyr <= 0 .or. &
        frame%selected_slot < 1 .or. frame%selected_slot > frame%boundary_nuyr) then
      reason = 'BOUNDQ02B_FRAME_YEAR_SLOT_INVALID'
      return
    end if
    if (frame%selected_year /= frame%simulation_start_year + frame%selected_slot - 1) then
      reason = 'BOUNDQ02B_FRAME_YEAR_SLOT_INCOHERENT'
      return
    end if
    if (.not. ieee_is_finite(frame%dry_deposition_nh) .or. &
        .not. ieee_is_finite(frame%dry_deposition_ni)) then
      reason = 'BOUNDQ02B_FRAME_DRY_DEPOSITION_NONFINITE'
      return
    end if

    call expected_forcing_id(frame%boundary_content_sha256, frame%selected_slot, forcing_id, id_ok)
    if (.not. id_ok .or. trim(frame%chemistry%forcing_id) /= trim(forcing_id)) then
      reason = 'BOUNDQ02B_FRAME_CONTENT_FORCING_ID_MISMATCH'
      return
    end if

    call make_tcd042_upper_chemistry_forcing(trim(frame%chemistry%forcing_id), &
      frame%chemistry%phosphorus_enabled, frame%chemistry%precipitation, &
      frame%chemistry%irrigation, frame%chemistry%runon, frame%chemistry%runin, &
      rebuilt, chemistry_ok, chemistry_reason)
    if (.not. chemistry_ok) then
      reason = 'BOUNDQ02B_FRAME_CHEMISTRY_INVALID'
      return
    end if

    call time_equal(frame%origin_time, expected_origin, equal, compare_ok)
    if (.not. compare_ok .or. .not. equal) then
      reason = 'BOUNDQ02B_FRAME_ORIGIN_MISMATCH'
      return
    end if
    call time_equal(frame%endpoint_time, expected_endpoint, equal, compare_ok)
    if (.not. compare_ok .or. .not. equal) then
      reason = 'BOUNDQ02B_FRAME_ENDPOINT_MISMATCH'
      return
    end if

    ok = .true.
    reason = 'VALID_IMMUTABLE_STATIC_BOUNDARY_INTERVAL_FRAME'
  end subroutine validate_immutable_static_boundary_interval_frame

  subroutine inspect_immutable_static_boundary_interval_frame(frame, expected_origin, expected_endpoint, &
      boundary_content_sha256, simulation_start_year, boundary_nuyr, selected_year, selected_slot, &
      chemistry, dry_deposition_nh, dry_deposition_ni, ok, reason)
    type(immutable_static_boundary_interval_frame_t), intent(in) :: frame
    type(TimeCoordinate), intent(in) :: expected_origin, expected_endpoint
    character(len=*), intent(out) :: boundary_content_sha256
    integer, intent(out) :: simulation_start_year, boundary_nuyr, selected_year, selected_slot
    type(tcd042_upper_chemistry_forcing_t), intent(out) :: chemistry
    real(real64), intent(out) :: dry_deposition_nh, dry_deposition_ni
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    character(len=128) :: local_reason

    boundary_content_sha256 = ''
    simulation_start_year = 0
    boundary_nuyr = 0
    selected_year = 0
    selected_slot = 0
    chemistry = tcd042_upper_chemistry_forcing_t()
    dry_deposition_nh = 0.0_real64
    dry_deposition_ni = 0.0_real64

    call validate_immutable_static_boundary_interval_frame(frame, expected_origin, expected_endpoint, ok, local_reason)
    if (.not. ok) then
      reason = trim(local_reason)
      return
    end if

    if (len(boundary_content_sha256) < 64) then
      ok = .false.
      reason = 'BOUNDQ02B_CONTENT_ID_OUTPUT_TOO_SHORT'
      return
    end if

    boundary_content_sha256 = frame%boundary_content_sha256
    simulation_start_year = frame%simulation_start_year
    boundary_nuyr = frame%boundary_nuyr
    selected_year = frame%selected_year
    selected_slot = frame%selected_slot
    chemistry = frame%chemistry
    dry_deposition_nh = frame%dry_deposition_nh
    dry_deposition_ni = frame%dry_deposition_ni
    ok = .true.
    reason = 'IMMUTABLE_STATIC_BOUNDARY_INTERVAL_FRAME_INSPECTED'
  end subroutine inspect_immutable_static_boundary_interval_frame

end module mod_animo_immutable_static_boundary_frame
