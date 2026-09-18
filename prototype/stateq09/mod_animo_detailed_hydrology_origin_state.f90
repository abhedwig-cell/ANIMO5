module mod_animo_detailed_hydrology_origin_state
  use iso_fortran_env, only: real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  private

  character(len=*), parameter, public :: DETAILED_HYDROLOGY_ORIGIN_SCHEMA = &
    'ANIMO_DETAILED_HYDROLOGY_ORIGIN_STATE_V1'
  character(len=*), parameter, public :: DETAILED_HYDROLOGY_TRANSFER_ID = &
    'REV53_INIT_IWA2_IOPTHYVS1_HLPIMP11'

  type, public :: detailed_hydrology_origin_state_t
    character(len=48) :: schema_id = ''
    character(len=64) :: transfer_contract_id = ''
    real(real64) :: pn = 0.0_real64
    real(real64) :: sic = 0.0_real64
    real(real64) :: snla = 0.0_real64
    real(real64), allocatable :: mofro(:)
  end type detailed_hydrology_origin_state_t

  public :: make_detailed_hydrology_origin_state
  public :: advance_origin_from_accepted_endpoint
  public :: validate_detailed_hydrology_origin_state

contains

  subroutine make_detailed_hydrology_origin_state(pn, sic, snla, mofro, value, ok, reason)
    real(real64), intent(in) :: pn, sic, snla
    real(real64), intent(in) :: mofro(:)
    type(detailed_hydrology_origin_state_t), intent(out) :: value
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    value = detailed_hydrology_origin_state_t()
    value%schema_id = DETAILED_HYDROLOGY_ORIGIN_SCHEMA
    value%transfer_contract_id = DETAILED_HYDROLOGY_TRANSFER_ID
    value%pn = pn
    value%sic = sic
    value%snla = snla
    allocate(value%mofro(size(mofro)))
    value%mofro = mofro

    call validate_detailed_hydrology_origin_state(value, ok, reason)
  end subroutine make_detailed_hydrology_origin_state

  subroutine advance_origin_from_accepted_endpoint(pnt, sict, snt, mofrt, next_origin, ok, reason)
    real(real64), intent(in) :: pnt, sict, snt
    real(real64), intent(in) :: mofrt(:)
    type(detailed_hydrology_origin_state_t), intent(out) :: next_origin
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    ! Frozen revision-53 Init.for, detailed SWAP route with
    ! Iopthyvs=1 and Hlpimp=11:
    !   Mofro(Ln) = Mofrt(Ln), Ln=1..Nl
    !   Snla = Snt
    !   Sic  = Sict
    !   Pn   = Pnt
    call make_detailed_hydrology_origin_state( &
      pnt, sict, snt, mofrt, next_origin, ok, reason)
    if (ok) reason = 'REV53_DETAILED_HYDROLOGY_ORIGIN_ADVANCED'
  end subroutine advance_origin_from_accepted_endpoint

  subroutine validate_detailed_hydrology_origin_state(value, ok, reason)
    type(detailed_hydrology_origin_state_t), intent(in) :: value
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    ok = .false.
    reason = 'UNSET'

    if (trim(value%schema_id) /= DETAILED_HYDROLOGY_ORIGIN_SCHEMA) then
      reason = 'DETAILED_HYDROLOGY_ORIGIN_SCHEMA_MISMATCH'
      return
    end if
    if (trim(value%transfer_contract_id) /= DETAILED_HYDROLOGY_TRANSFER_ID) then
      reason = 'DETAILED_HYDROLOGY_TRANSFER_CONTRACT_MISMATCH'
      return
    end if
    if (.not. allocated(value%mofro) .or. size(value%mofro) <= 0) then
      reason = 'MISSING_DETAILED_HYDROLOGY_MOFRO_PROFILE'
      return
    end if
    if (.not. ieee_is_finite(value%pn) .or. .not. ieee_is_finite(value%sic) .or. &
        .not. ieee_is_finite(value%snla) .or. .not. all(ieee_is_finite(value%mofro))) then
      reason = 'NONFINITE_DETAILED_HYDROLOGY_ORIGIN_STATE'
      return
    end if

    ok = .true.
    reason = 'VALID_DETAILED_HYDROLOGY_ORIGIN_STATE'
  end subroutine validate_detailed_hydrology_origin_state

end module mod_animo_detailed_hydrology_origin_state
