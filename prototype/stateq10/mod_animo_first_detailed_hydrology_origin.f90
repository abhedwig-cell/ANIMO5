module mod_animo_first_detailed_hydrology_origin
  use iso_fortran_env, only: int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  private

  character(len=*), parameter, public :: FIRST_DETAILED_ORIGIN_SCHEMA = &
    'ANIMO_FIRST_DETAILED_HYDROLOGY_ORIGIN_V1'
  character(len=*), parameter, public :: FIRST_DETAILED_ORIGIN_SOURCE = &
    'REV53_INPUT1_HLPIMP11_IOPTHYVS1'

  type, public :: first_detailed_hydrology_origin_t
    character(len=48) :: schema_id = ''
    character(len=64) :: source_contract_id = ''
    real(real64) :: pn = 0.0_real64
    real(real64) :: sic = 0.0_real64
    real(real64) :: snla = 0.0_real64
    real(real64), allocatable :: mofro(:)
  end type first_detailed_hydrology_origin_t

  public :: normalize_rev53_real4
  public :: make_first_detailed_hydrology_origin
  public :: validate_first_detailed_hydrology_origin

contains

  function normalize_rev53_real4(r4) result(value)
    real(real32), intent(in) :: r4
    real(real64) :: value
    integer(int32) :: i4
    integer(int64) :: i, rounded
    real(real32) :: r, one, help, scale4
    real(real64) :: r8

    ! Exact source mapping of Function.for Dble_trunc for an already-read
    ! REAL(4) value. KINT truncates to INTEGER(8); KIDNNT rounds a REAL(8).
    one = 1.0_real32
    i = int(r4, kind=int64)
    r = mod(r4, one)

    if (r == 0.0_real32) then
      i4 = 0_int32
    else
      help = -log10(abs(r))
      if (help < 0.0_real32) then
        i4 = int(help - 0.9999999_real32, kind=int32)
      else
        i4 = int(help, kind=int32)
      end if
    end if

    scale4 = 10.0_real32 ** (i4 + 7_int32)
    r8 = real(scale4 * r, real64)
    rounded = nint(r8, kind=int64)
    value = real(rounded, real64) / real(scale4, real64) + real(i, real64)
  end function normalize_rev53_real4

  subroutine make_first_detailed_hydrology_origin(smofro, ssic, spn, ssnla, value, ok, reason)
    real(real32), intent(in) :: smofro(:)
    real(real32), intent(in) :: ssic, spn, ssnla
    type(first_detailed_hydrology_origin_t), intent(out) :: value
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    integer :: ln

    value = first_detailed_hydrology_origin_t()
    ok = .false.
    reason = 'UNSET'

    if (size(smofro) <= 0) then
      reason = 'EMPTY_FIRST_MOFRO_PROFILE'
      return
    end if
    if (.not. all(ieee_is_finite(smofro)) .or. .not. ieee_is_finite(ssic) .or. &
        .not. ieee_is_finite(spn) .or. .not. ieee_is_finite(ssnla)) then
      reason = 'NONFINITE_FIRST_DETAILED_HYDROLOGY_INPUT'
      return
    end if

    value%schema_id = FIRST_DETAILED_ORIGIN_SCHEMA
    value%source_contract_id = FIRST_DETAILED_ORIGIN_SOURCE
    value%pn = normalize_rev53_real4(spn)
    value%sic = normalize_rev53_real4(ssic)
    value%snla = normalize_rev53_real4(ssnla)
    allocate(value%mofro(size(smofro)))
    do ln = 1, size(smofro)
      value%mofro(ln) = normalize_rev53_real4(smofro(ln))
    end do

    call validate_first_detailed_hydrology_origin(value, ok, reason)
  end subroutine make_first_detailed_hydrology_origin

  subroutine validate_first_detailed_hydrology_origin(value, ok, reason)
    type(first_detailed_hydrology_origin_t), intent(in) :: value
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    ok = .false.
    reason = 'UNSET'

    if (trim(value%schema_id) /= FIRST_DETAILED_ORIGIN_SCHEMA) then
      reason = 'FIRST_DETAILED_ORIGIN_SCHEMA_MISMATCH'
      return
    end if
    if (trim(value%source_contract_id) /= FIRST_DETAILED_ORIGIN_SOURCE) then
      reason = 'FIRST_DETAILED_ORIGIN_SOURCE_MISMATCH'
      return
    end if
    if (.not. allocated(value%mofro) .or. size(value%mofro) <= 0) then
      reason = 'MISSING_FIRST_MOFRO_PROFILE'
      return
    end if
    if (.not. ieee_is_finite(value%pn) .or. .not. ieee_is_finite(value%sic) .or. &
        .not. ieee_is_finite(value%snla) .or. .not. all(ieee_is_finite(value%mofro))) then
      reason = 'NONFINITE_NORMALIZED_FIRST_DETAILED_ORIGIN'
      return
    end if

    ok = .true.
    reason = 'VALID_FIRST_DETAILED_HYDROLOGY_ORIGIN'
  end subroutine validate_first_detailed_hydrology_origin

end module mod_animo_first_detailed_hydrology_origin
