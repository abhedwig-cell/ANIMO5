module mod_animo_bounded_no_ponding_upper_hydrology
  use iso_fortran_env, only: int64, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  use mod_transient_time, only: TimeCoordinate, time_compare
  use mod_animo_hydrology_adapter, only: hydro_detailed_external_t, &
    validate_hydro_detailed_external, KT05_OK
  use mod_animo_resolved_upper_hydrology_contract, only: &
    resolved_upper_hydrology_t, make_resolved_upper_hydrology
  use mod_animo_tcd042_runoff_load_context, only: &
    tcd042_runoff_load_context_t, make_tcd042_runoff_load_context
  implicit none
  private

  character(len=*), parameter, public :: HYDROEXEC01_SCHEMA = &
    'ANIMO_REV53_NO_PONDING_UPPER_HYDROLOGY_V1'
  real(real64), parameter, public :: REV53_PONDING_THRESHOLD = 1.0e-4_real64
  real(real64), parameter, public :: REV53_RUNOFF_NEAR_ZERO = 1.0e-8_real64
  integer(int64), parameter :: MAX_EXACT_REAL64_INTEGER = 9007199254740991_int64

  type, public :: hydroexec01_start_context_t
    character(len=48) :: schema_id = ''
    real(real64) :: pn = 0.0_real64
    real(real64) :: sic = 0.0_real64
    real(real64) :: snla = 0.0_real64
    real(real64) :: mofro_top = 0.0_real64
    real(real64) :: he_top = 0.0_real64
    real(real64) :: lefrrv = 0.0_real64
    real(real64) :: lefrso = 0.0_real64
    real(real64) :: runinu_call_entry = 0.0_real64
  end type hydroexec01_start_context_t

  type, public :: hydroexec01_diagnostics_t
    integer :: flpn = -1
    real(real64) :: runinu = 0.0_real64
    real(real64) :: rupr = 0.0_real64
    real(real64) :: rurv = 0.0_real64
    real(real64) :: ruso = 0.0_real64
    real(real64) :: dif = 0.0_real64
    real(real64) :: evso_resolved = 0.0_real64
    real(real64) :: flab_top_resolved = 0.0_real64
    real(real64) :: flib_top_resolved = 0.0_real64
  end type hydroexec01_diagnostics_t

  public :: make_hydroexec01_start_context
  public :: resolve_rev53_no_ponding_upper_hydrology

contains

  logical function exact_binary_zero(value)
    real(real64), intent(in) :: value
    integer(int64) :: bits
    bits = transfer(value, bits)
    exact_binary_zero = iand(bits, int(z'7FFFFFFFFFFFFFFF', int64)) == 0_int64
  end function exact_binary_zero

  logical function exact_binary64_equal(left, right)
    real(real64), intent(in) :: left, right
    integer(int64) :: a, b
    a = transfer(left, a)
    b = transfer(right, b)
    exact_binary64_equal = a == b
  end function exact_binary64_equal

  subroutine make_hydroexec01_start_context(pn, sic, snla, mofro_top, he_top, &
      lefrrv, lefrso, runinu_call_entry, value, ok, reason)
    real(real64), intent(in) :: pn, sic, snla, mofro_top, he_top
    real(real64), intent(in) :: lefrrv, lefrso, runinu_call_entry
    type(hydroexec01_start_context_t), intent(out) :: value
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    value = hydroexec01_start_context_t()
    value%schema_id = HYDROEXEC01_SCHEMA
    value%pn = pn
    value%sic = sic
    value%snla = snla
    value%mofro_top = mofro_top
    value%he_top = he_top
    value%lefrrv = lefrrv
    value%lefrso = lefrso
    value%runinu_call_entry = runinu_call_entry

    call validate_start_context(value, ok, reason)
  end subroutine make_hydroexec01_start_context

  subroutine resolve_rev53_no_ponding_upper_hydrology(execution_id, origin_time, endpoint_time, &
      projection, start_context, resolved_hydrology, runoff_context, diagnostics, ok, reason)
    character(len=*), intent(in) :: execution_id
    type(TimeCoordinate), intent(in) :: origin_time, endpoint_time
    type(hydro_detailed_external_t), intent(in) :: projection
    type(hydroexec01_start_context_t), intent(in) :: start_context
    type(resolved_upper_hydrology_t), intent(out) :: resolved_hydrology
    type(tcd042_runoff_load_context_t), intent(out) :: runoff_context
    type(hydroexec01_diagnostics_t), intent(out) :: diagnostics
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    integer :: kt05_status, ordering, drn
    logical :: compare_ok, make_ok
    integer(int64) :: step_days_i
    real(real64) :: st, fl_dr_to1, denom, provisional_flab_top
    character(len=96) :: local_reason

    diagnostics = hydroexec01_diagnostics_t()
    resolved_hydrology = resolved_upper_hydrology_t()
    runoff_context = tcd042_runoff_load_context_t()
    ok = .false.
    reason = 'UNSET'

    if (len_trim(execution_id) == 0) then
      reason = 'MISSING_HYDROEXEC01_EXECUTION_ID'
      return
    end if

    call validate_hydro_detailed_external(projection, kt05_status)
    if (kt05_status /= KT05_OK) then
      reason = 'INVALID_KT05_HYDRO_DETAILED_PROJECTION'
      return
    end if

    call validate_start_context(start_context, ok, local_reason)
    if (.not. ok) then
      reason = trim(local_reason)
      return
    end if
    ! From here onward every early return remains a rejection until the
    ! complete bounded source path has produced both typed outputs.
    ok = .false.

    if (trim(origin_time%calendar_contract_id) /= trim(endpoint_time%calendar_contract_id)) then
      reason = 'HYDROEXEC01_CALENDAR_MISMATCH'
      return
    end if
    if (origin_time%subday_numerator /= 0_int64 .or. endpoint_time%subday_numerator /= 0_int64) then
      reason = 'SUBDAY_HYDROEXEC01_NOT_QUALIFIED'
      return
    end if

    call time_compare(endpoint_time, origin_time, ordering, compare_ok)
    if (.not. compare_ok .or. ordering <= 0) then
      reason = 'INVALID_HYDROEXEC01_INTERVAL'
      return
    end if

    step_days_i = endpoint_time%day_index - origin_time%day_index
    if (step_days_i <= 0_int64 .or. step_days_i > MAX_EXACT_REAL64_INTEGER) then
      reason = 'HYDROEXEC01_INTERVAL_NOT_EXACT_REAL64_DAY'
      return
    end if
    st = real(step_days_i, real64)

    if (.not. exact_binary64_equal(projection%st, st)) then
      reason = 'PRODUCER_STEP_DOES_NOT_MATCH_KT02_INTERVAL'
      return
    end if

    if ((projection%pnt + projection%snt) > REV53_PONDING_THRESHOLD .or. &
        (start_context%pn + start_context%snla) > REV53_PONDING_THRESHOLD) then
      reason = 'PONDING_OUTSIDE_HYDROEXEC01_SCOPE'
      return
    end if
    diagnostics%flpn = 0

    if (projection%ru < 0.0_real64) then
      diagnostics%runinu = -projection%ru
      diagnostics%rupr = 0.0_real64
      diagnostics%rurv = 0.0_real64
      diagnostics%ruso = 0.0_real64
    else if (projection%ru > -REV53_RUNOFF_NEAR_ZERO .and. &
             projection%ru < REV53_RUNOFF_NEAR_ZERO) then
      ! Exact revision-53 call semantics: this branch does not assign Runinu.
      diagnostics%runinu = start_context%runinu_call_entry
      diagnostics%rupr = 0.0_real64
      diagnostics%rurv = 0.0_real64
      diagnostics%ruso = 0.0_real64
    else
      diagnostics%runinu = 0.0_real64
      diagnostics%rupr = (1.0_real64 - start_context%lefrrv) * projection%ru
      diagnostics%rurv = (1.0_real64 - start_context%lefrso) * &
        start_context%lefrrv * projection%ru
      diagnostics%ruso = start_context%lefrso * start_context%lefrrv * projection%ru

      denom = diagnostics%rupr + diagnostics%ruso
      if (exact_binary_zero(denom)) then
        reason = 'UNQUALIFIED_REV53_RUPR_PARTITION_SINGULARITY'
        return
      end if

      diagnostics%rupr = min(diagnostics%rupr + &
        diagnostics%rurv * diagnostics%rupr / denom, projection%prr)
      diagnostics%rurv = 0.0_real64
      diagnostics%ruso = projection%ru - diagnostics%rupr
    end if

    fl_dr_to1 = 0.0_real64
    do drn = 1, projection%drainage_count
      fl_dr_to1 = fl_dr_to1 + projection%fldr(drn,1)
    end do

    provisional_flab_top = projection%flab(2) + diagnostics%ruso + projection%evso + &
      (projection%mofrt(1) - start_context%mofro_top) * start_context%he_top / st + &
      fl_dr_to1 + projection%flev(1)

    diagnostics%dif = provisional_flab_top - ( &
      projection%prr - projection%evicpr + projection%prirr - projection%evicirr - &
      (projection%sict - start_context%sic) / st + projection%prsn - projection%evsn - &
      (projection%snt - start_context%snla) / st - projection%evpn - &
      (projection%pnt - start_context%pn) / st + projection%runon + diagnostics%runinu - &
      diagnostics%rupr - diagnostics%rurv )

    diagnostics%evso_resolved = max(0.0_real64, projection%evso - diagnostics%dif)

    diagnostics%flab_top_resolved = projection%flab(2) + diagnostics%ruso + &
      diagnostics%evso_resolved + fl_dr_to1 + projection%flev(1) + &
      (projection%mofrt(1) - start_context%mofro_top) * start_context%he_top / st

    diagnostics%flib_top_resolved = max(0.0_real64, diagnostics%flab_top_resolved)

    if (.not. all(ieee_is_finite([diagnostics%runinu, diagnostics%rupr, diagnostics%rurv, &
        diagnostics%ruso, diagnostics%dif, diagnostics%evso_resolved, &
        diagnostics%flab_top_resolved, diagnostics%flib_top_resolved]))) then
      reason = 'NONFINITE_HYDROEXEC01_RESULT'
      return
    end if

    call make_resolved_upper_hydrology(execution_id, origin_time, endpoint_time, 0, &
      diagnostics%flib_top_resolved, diagnostics%rurv, resolved_hydrology, make_ok, local_reason)
    if (.not. make_ok) then
      reason = trim(local_reason)
      return
    end if

    call make_tcd042_runoff_load_context(execution_id, origin_time, endpoint_time, &
      diagnostics%rupr, diagnostics%runinu, runoff_context, make_ok, local_reason)
    if (.not. make_ok) then
      reason = trim(local_reason)
      return
    end if

    ok = .true.
    reason = 'REV53_NO_PONDING_UPPER_HYDROLOGY_RESOLVED'
  end subroutine resolve_rev53_no_ponding_upper_hydrology

  subroutine validate_start_context(value, ok, reason)
    type(hydroexec01_start_context_t), intent(in) :: value
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    real(real64) :: values(8)

    values = [value%pn, value%sic, value%snla, value%mofro_top, value%he_top, &
      value%lefrrv, value%lefrso, value%runinu_call_entry]

    if (trim(value%schema_id) /= HYDROEXEC01_SCHEMA) then
      ok = .false.
      reason = 'HYDROEXEC01_START_SCHEMA_MISMATCH'
      return
    end if
    if (.not. all(ieee_is_finite(values))) then
      ok = .false.
      reason = 'NONFINITE_HYDROEXEC01_START_CONTEXT'
      return
    end if
    if (value%he_top <= 0.0_real64) then
      ok = .false.
      reason = 'NONPOSITIVE_HYDROEXEC01_TOP_THICKNESS'
      return
    end if

    ok = .true.
    reason = 'VALID_HYDROEXEC01_START_CONTEXT'
  end subroutine validate_start_context

end module mod_animo_bounded_no_ponding_upper_hydrology
