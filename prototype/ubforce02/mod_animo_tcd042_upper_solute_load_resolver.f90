module mod_animo_tcd042_upper_solute_load_resolver
  use iso_fortran_env, only: real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  use mod_transient_time, only: TimeCoordinate
  use mod_animo_tcd042_upper_solute_load_contract, only: &
    tcd042_upper_loads_t, make_tcd042_upper_loads
  implicit none
  private

  character(len=*), parameter, public :: TCD042_LOAD_RESOLVER_SCHEMA = &
    'ANIMO_TCD042_UPPER_LOAD_RESOLVER_V1'
  character(len=*), parameter, public :: TCD042_LOAD_RESOLVER_ROUTE = &
    'REV53_IWA2_IOPTHYVS1_DETAILED'

  type, public :: tcd042_load_hydrology_context_t
    real(real64) :: prr = 0.0_real64
    real(real64) :: prsn = 0.0_real64
    real(real64) :: prirr = 0.0_real64
    real(real64) :: runon = 0.0_real64
    real(real64) :: rupr = 0.0_real64
    real(real64) :: runinu = 0.0_real64
  end type tcd042_load_hydrology_context_t

  type, public :: tcd042_precip_chemistry_t
    real(real64) :: nh = 0.0_real64
    real(real64) :: ni = 0.0_real64
    real(real64) :: po = 0.0_real64
  end type tcd042_precip_chemistry_t

  type, public :: tcd042_six_channel_chemistry_t
    real(real64) :: nh = 0.0_real64
    real(real64) :: ni = 0.0_real64
    real(real64) :: doma = 0.0_real64
    real(real64) :: don = 0.0_real64
    real(real64) :: po = 0.0_real64
    real(real64) :: dop = 0.0_real64
  end type tcd042_six_channel_chemistry_t

  type, public :: tcd042_upper_chemistry_forcing_t
    character(len=48) :: schema_id = ''
    character(len=96) :: forcing_id = ''
    logical :: phosphorus_enabled = .false.
    type(tcd042_precip_chemistry_t) :: precipitation
    type(tcd042_six_channel_chemistry_t) :: irrigation
    type(tcd042_six_channel_chemistry_t) :: runon
    type(tcd042_six_channel_chemistry_t) :: runin
  end type tcd042_upper_chemistry_forcing_t

  public :: make_tcd042_upper_chemistry_forcing
  public :: resolve_tcd042_upper_loads

contains

  subroutine make_tcd042_upper_chemistry_forcing(forcing_id, phosphorus_enabled, &
      precipitation, irrigation, runon_chemistry, runin, forcing, ok, reason)
    character(len=*), intent(in) :: forcing_id
    logical, intent(in) :: phosphorus_enabled
    type(tcd042_precip_chemistry_t), intent(in) :: precipitation
    type(tcd042_six_channel_chemistry_t), intent(in) :: irrigation, runon_chemistry, runin
    type(tcd042_upper_chemistry_forcing_t), intent(out) :: forcing
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    forcing = tcd042_upper_chemistry_forcing_t()
    forcing%schema_id = TCD042_LOAD_RESOLVER_SCHEMA
    forcing%forcing_id = forcing_id
    forcing%phosphorus_enabled = phosphorus_enabled
    forcing%precipitation = precipitation
    forcing%irrigation = irrigation
    forcing%runon = runon_chemistry
    forcing%runin = runin

    call validate_chemistry(forcing, ok, reason)
  end subroutine make_tcd042_upper_chemistry_forcing

  subroutine resolve_tcd042_upper_loads(execution_id, origin_time, endpoint_time, &
      hydrology, chemistry, loads, ok, reason)
    character(len=*), intent(in) :: execution_id
    type(TimeCoordinate), intent(in) :: origin_time, endpoint_time
    type(tcd042_load_hydrology_context_t), intent(in) :: hydrology
    type(tcd042_upper_chemistry_forcing_t), intent(in) :: chemistry
    type(tcd042_upper_loads_t), intent(out) :: loads
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    real(real64) :: precipitation_term
    real(real64) :: load1, load2, load3, load4, load5, load6

    ok = .false.
    reason = 'UNSET'

    call validate_hydrology(hydrology, ok, reason)
    if (.not. ok) return
    call validate_chemistry(chemistry, ok, reason)
    if (.not. ok) return
    if (len_trim(execution_id) == 0) then
      ok = .false.
      reason = 'MISSING_LOAD_RESOLVER_EXECUTION_ID'
      return
    end if

    ! Exact revision-53 UBoundconc route:
    ! Iwa=2 AND Iopthyvs=1.
    precipitation_term = hydrology%prr - hydrology%rupr + hydrology%prsn

    load1 = precipitation_term * chemistry%precipitation%nh + &
      hydrology%prirr * chemistry%irrigation%nh + &
      hydrology%runon * chemistry%runon%nh + &
      hydrology%runinu * chemistry%runin%nh

    load2 = precipitation_term * chemistry%precipitation%ni + &
      hydrology%prirr * chemistry%irrigation%ni + &
      hydrology%runon * chemistry%runon%ni + &
      hydrology%runinu * chemistry%runin%ni

    load3 = hydrology%prirr * chemistry%irrigation%doma + &
      hydrology%runon * chemistry%runon%doma + &
      hydrology%runinu * chemistry%runin%doma

    load4 = hydrology%prirr * chemistry%irrigation%don + &
      hydrology%runon * chemistry%runon%don + &
      hydrology%runinu * chemistry%runin%don

    if (chemistry%phosphorus_enabled) then
      load5 = precipitation_term * chemistry%precipitation%po + &
        hydrology%prirr * chemistry%irrigation%po + &
        hydrology%runon * chemistry%runon%po + &
        hydrology%runinu * chemistry%runin%po

      load6 = hydrology%prirr * chemistry%irrigation%dop + &
        hydrology%runon * chemistry%runon%dop + &
        hydrology%runinu * chemistry%runin%dop
    else
      load5 = 0.0_real64
      load6 = 0.0_real64
    end if

    if (.not. all(ieee_is_finite([load1,load2,load3,load4,load5,load6]))) then
      ok = .false.
      reason = 'NONFINITE_RESOLVED_TCD042_LOAD'
      return
    end if

    call make_tcd042_upper_loads(execution_id, origin_time, endpoint_time, &
      load1, load2, load3, load4, chemistry%phosphorus_enabled, load5, load6, &
      loads, ok, reason)
    if (.not. ok) return

    reason = 'TCD042_UPPER_LOADS_RESOLVED_FROM_PINNED_REV53_FORMULAS'
  end subroutine resolve_tcd042_upper_loads

  subroutine validate_hydrology(hydrology, ok, reason)
    type(tcd042_load_hydrology_context_t), intent(in) :: hydrology
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    real(real64) :: values(6)

    values = [hydrology%prr, hydrology%prsn, hydrology%prirr, hydrology%runon, &
      hydrology%rupr, hydrology%runinu]
    if (.not. all(ieee_is_finite(values))) then
      ok = .false.
      reason = 'NONFINITE_LOAD_HYDROLOGY_CONTEXT'
      return
    end if

    ! Do not add sign/range assumptions here that are not owned by this resolver.
    ok = .true.
    reason = 'VALID_LOAD_HYDROLOGY_CONTEXT'
  end subroutine validate_hydrology

  subroutine validate_chemistry(forcing, ok, reason)
    type(tcd042_upper_chemistry_forcing_t), intent(in) :: forcing
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    real(real64) :: core(18), phosphorus(3)

    if (trim(forcing%schema_id) /= TCD042_LOAD_RESOLVER_SCHEMA) then
      ok = .false.
      reason = 'UPPER_CHEMISTRY_SCHEMA_MISMATCH'
      return
    end if
    if (len_trim(forcing%forcing_id) == 0) then
      ok = .false.
      reason = 'MISSING_UPPER_CHEMISTRY_FORCING_ID'
      return
    end if

    core = [ &
      forcing%precipitation%nh, forcing%precipitation%ni, &
      forcing%irrigation%nh, forcing%irrigation%ni, forcing%irrigation%doma, &
      forcing%irrigation%don, forcing%runon%nh, forcing%runon%ni, &
      forcing%runon%doma, forcing%runon%don, forcing%runin%nh, forcing%runin%ni, &
      forcing%runin%doma, forcing%runin%don, forcing%irrigation%po, &
      forcing%runon%po, forcing%runin%po, forcing%precipitation%po ]

    if (.not. all(ieee_is_finite(core))) then
      ok = .false.
      reason = 'NONFINITE_UPPER_CHEMISTRY_FORCING'
      return
    end if

    phosphorus = [forcing%precipitation%po, forcing%irrigation%dop, &
      forcing%runon%dop]
    if (.not. all(ieee_is_finite(phosphorus)) .or. &
        .not. ieee_is_finite(forcing%runin%dop)) then
      ok = .false.
      reason = 'NONFINITE_UPPER_PHOSPHORUS_CHEMISTRY'
      return
    end if

    ok = .true.
    reason = 'VALID_TCD042_UPPER_CHEMISTRY_FORCING'
  end subroutine validate_chemistry

end module mod_animo_tcd042_upper_solute_load_resolver
