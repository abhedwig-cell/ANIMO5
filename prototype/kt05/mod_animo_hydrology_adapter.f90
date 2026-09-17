module mod_animo_hydrology_adapter
  use, intrinsic :: iso_fortran_env, only : real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none
  private

  character(len=*), parameter, public :: HYDROLOGY_SCHEMA_ID = 'ANIMO_HYDROLOGY_STEP_V1'
  character(len=*), parameter, public :: HYDROLOGY_UNIT_CONTRACT_ID = 'ANIMO_HYDROLOGY_UNITS_V1'

  integer, parameter, public :: KT05_OK = 0
  integer, parameter, public :: KT05_ERR_SCHEMA = 1
  integer, parameter, public :: KT05_ERR_UNITS = 2
  integer, parameter, public :: KT05_ERR_DIMENSIONS = 3
  integer, parameter, public :: KT05_ERR_NONFINITE = 4
  integer, parameter, public :: KT05_ERR_EXPLICIT_INTERCEPTION = 5

  type, public :: hydrology_step_t
    character(len=32) :: schema_id = ''
    character(len=32) :: unit_contract_id = ''
    integer :: layer_count = 0
    integer :: drainage_count = 0
    real(real64) :: producer_endpoint_day = 0.0_real64
    real(real64) :: producer_step_days = 0.0_real64
    real(real64) :: prr = 0.0_real64
    real(real64) :: prsn = 0.0_real64
    real(real64) :: prirr = 0.0_real64
    real(real64) :: evicpr = 0.0_real64
    real(real64) :: evicirr = 0.0_real64
    real(real64) :: evsn = 0.0_real64
    real(real64) :: evso = 0.0_real64
    real(real64) :: evpn = 0.0_real64
    real(real64) :: evsoma = 0.0_real64
    real(real64) :: evtrma = 0.0_real64
    real(real64) :: runon = 0.0_real64
    real(real64) :: runoff = 0.0_real64
    real(real64) :: groundwater_level = 0.0_real64
    real(real64) :: ponding_end = 0.0_real64
    real(real64) :: snow_storage_end = 0.0_real64
    real(real64) :: water_balance_aeration = 0.0_real64
    real(real64), allocatable :: sc(:)
    real(real64), allocatable :: mofrt(:)
    real(real64), allocatable :: flev(:)
    real(real64), allocatable :: flab(:)
    real(real64), allocatable :: fldr(:,:)
    logical :: has_interception_storage_end = .false.
    real(real64) :: interception_storage_end = 0.0_real64
    logical :: has_soil_temperature = .false.
    real(real64), allocatable :: soil_temperature(:)
  end type hydrology_step_t

  type, public :: hydro_detailed_external_t
    integer :: layer_count = 0
    integer :: drainage_count = 0
    real(real64) :: evicirr = 0.0_real64
    real(real64) :: evicpr = 0.0_real64
    real(real64) :: evpn = 0.0_real64
    real(real64) :: evsn = 0.0_real64
    real(real64) :: evso = 0.0_real64
    real(real64) :: evsoma = 0.0_real64
    real(real64) :: evtrma = 0.0_real64
    real(real64), allocatable :: flab(:)
    real(real64), allocatable :: fldr(:,:)
    real(real64), allocatable :: flev(:)
    real(real64), allocatable :: mofrt(:)
    real(real64) :: pnt = 0.0_real64
    real(real64) :: prirr = 0.0_real64
    real(real64) :: prr = 0.0_real64
    real(real64) :: prsn = 0.0_real64
    real(real64) :: ru = 0.0_real64
    real(real64) :: runon = 0.0_real64
    real(real64) :: sict = 0.0_real64
    real(real64) :: snt = 0.0_real64
    real(real64) :: st = 0.0_real64
  end type hydro_detailed_external_t

  public :: validate_hydrology_step_explicit
  public :: project_hydro_detailed_explicit

contains

  subroutine validate_hydrology_step_explicit(step, status)
    type(hydrology_step_t), intent(in) :: step
    integer, intent(out) :: status

    status = KT05_OK

    if (trim(step%schema_id) /= HYDROLOGY_SCHEMA_ID) then
      status = KT05_ERR_SCHEMA
      return
    end if
    if (trim(step%unit_contract_id) /= HYDROLOGY_UNIT_CONTRACT_ID) then
      status = KT05_ERR_UNITS
      return
    end if
    if (step%layer_count <= 0 .or. step%drainage_count < 0) then
      status = KT05_ERR_DIMENSIONS
      return
    end if
    if (.not. allocated(step%sc) .or. .not. allocated(step%mofrt) .or. &
        .not. allocated(step%flev) .or. .not. allocated(step%flab) .or. &
        .not. allocated(step%fldr) .or. .not. allocated(step%soil_temperature)) then
      status = KT05_ERR_DIMENSIONS
      return
    end if
    if (size(step%sc) /= step%layer_count .or. &
        size(step%mofrt) /= step%layer_count .or. &
        size(step%flev) /= step%layer_count .or. &
        size(step%flab) /= step%layer_count + 1) then
      status = KT05_ERR_DIMENSIONS
      return
    end if
    if (size(step%fldr, 1) /= step%drainage_count .or. &
        size(step%fldr, 2) /= step%layer_count) then
      status = KT05_ERR_DIMENSIONS
      return
    end if
    if (step%has_soil_temperature) then
      if (size(step%soil_temperature) /= step%layer_count) then
        status = KT05_ERR_DIMENSIONS
        return
      end if
    else
      if (size(step%soil_temperature) /= 0) then
        status = KT05_ERR_DIMENSIONS
        return
      end if
    end if
    if (.not. step%has_interception_storage_end) then
      status = KT05_ERR_EXPLICIT_INTERCEPTION
      return
    end if
    if (.not. scalars_are_finite(step)) then
      status = KT05_ERR_NONFINITE
      return
    end if
    if (.not. all(ieee_is_finite(step%sc)) .or. &
        .not. all(ieee_is_finite(step%mofrt)) .or. &
        .not. all(ieee_is_finite(step%flev)) .or. &
        .not. all(ieee_is_finite(step%flab)) .or. &
        .not. all(ieee_is_finite(step%fldr)) .or. &
        .not. all(ieee_is_finite(step%soil_temperature))) then
      status = KT05_ERR_NONFINITE
      return
    end if
    if (step%producer_step_days <= 0.0_real64) then
      status = KT05_ERR_DIMENSIONS
    end if
  end subroutine validate_hydrology_step_explicit

  logical function scalars_are_finite(step)
    type(hydrology_step_t), intent(in) :: step
    real(real64) :: values(19)

    values = [ &
      step%producer_endpoint_day, step%producer_step_days, step%prr, &
      step%prsn, step%prirr, step%evicpr, step%evicirr, step%evsn, &
      step%evso, step%evpn, step%evsoma, step%evtrma, step%runon, &
      step%runoff, step%groundwater_level, step%ponding_end, &
      step%snow_storage_end, step%water_balance_aeration, &
      step%interception_storage_end ]
    scalars_are_finite = all(ieee_is_finite(values))
  end function scalars_are_finite

  subroutine project_hydro_detailed_explicit(step, projection, status)
    type(hydrology_step_t), intent(in) :: step
    type(hydro_detailed_external_t), intent(out) :: projection
    integer, intent(out) :: status

    call validate_hydrology_step_explicit(step, status)
    if (status /= KT05_OK) return

    projection%layer_count = step%layer_count
    projection%drainage_count = step%drainage_count
    projection%evicirr = step%evicirr
    projection%evicpr = step%evicpr
    projection%evpn = step%evpn
    projection%evsn = step%evsn
    projection%evso = step%evso
    projection%evsoma = step%evsoma
    projection%evtrma = step%evtrma
    allocate(projection%flab(size(step%flab)))
    allocate(projection%fldr(size(step%fldr, 1), size(step%fldr, 2)))
    allocate(projection%flev(size(step%flev)))
    allocate(projection%mofrt(size(step%mofrt)))
    projection%flab = step%flab
    projection%fldr = step%fldr
    projection%flev = step%flev
    projection%mofrt = step%mofrt
    projection%pnt = step%ponding_end
    projection%prirr = step%prirr
    projection%prr = step%prr
    projection%prsn = step%prsn
    projection%ru = step%runoff
    projection%runon = step%runon
    projection%sict = step%interception_storage_end
    projection%snt = step%snow_storage_end
    projection%st = step%producer_step_days
  end subroutine project_hydro_detailed_explicit

end module mod_animo_hydrology_adapter
