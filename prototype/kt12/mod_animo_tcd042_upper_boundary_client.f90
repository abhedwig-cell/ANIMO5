module mod_animo_tcd042_upper_boundary_client
  use iso_fortran_env, only: int64, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  use mod_transient_time, only: TimeCoordinate, time_compare
  use mod_transient_contracts, only: transient_payload_t, admissibility_t
  use mod_transient_transactions, only: accepted_store_t, initialize_accepted_store
  use mod_transient_interval_runtime, only: transient_client_t
  implicit none
  private

  character(len=*), parameter, public :: TCD042_RESOLVED_HYDROLOGY_SCHEMA = &
    'ANIMO_TCD042_RESOLVED_UPPER_HYDROLOGY_V0'
  real(real64), parameter, public :: TCD042_FLUX_THRESHOLD = 1.0e-8_real64
  real(real64), parameter, public :: TCD042_P_MAX = 3.8510200002999744e-7_real64
  integer(int64), parameter :: MAX_EXACT_REAL64_INTEGER = 9007199254740991_int64

  integer, parameter, public :: TCD042_BRANCH_NONE = 0
  integer, parameter, public :: TCD042_BRANCH_B1_EXACT_ZERO = 1
  integer, parameter, public :: TCD042_BRANCH_E1_NQ03 = 2

  type, public :: tcd042_resolved_hydrology_t
    character(len=48) :: schema_id = ''
    integer :: flpn = -1
    real(real64) :: flib_top = 0.0_real64
    real(real64) :: rurv = 0.0_real64
  end type tcd042_resolved_hydrology_t

  type, extends(transient_payload_t), public :: tcd042_top_state_t
    real(real64) :: concentration = 0.0_real64
  contains
    procedure :: clone_payload => tcd042_clone_payload
    procedure :: is_valid => tcd042_payload_valid
  end type tcd042_top_state_t

  type, extends(transient_client_t), public :: tcd042_upper_boundary_client_t
    private
    type(tcd042_resolved_hydrology_t) :: hydrology
    logical :: hydrology_present = .false.
    real(real64) :: hetop = 0.0_real64
    real(real64) :: load_rate = 0.0_real64
    logical :: process_forcing_present = .false.
    real(real64) :: last_average_concentration = 0.0_real64
    real(real64) :: last_flux = 0.0_real64
    real(real64) :: last_p = 0.0_real64
    integer :: last_branch = TCD042_BRANCH_NONE
    logical :: last_diagnostic_valid = .false.
  contains
    procedure :: execute_attempt => execute_tcd042_attempt
  end type tcd042_upper_boundary_client_t

  public :: initialize_tcd042_store
  public :: configure_tcd042_client
  public :: tcd042_last_diagnostics

contains

  subroutine tcd042_clone_payload(self, copy)
    class(tcd042_top_state_t), intent(in) :: self
    class(transient_payload_t), allocatable, intent(out) :: copy

    allocate(tcd042_top_state_t :: copy)
    select type (typed => copy)
    type is (tcd042_top_state_t)
      typed%concentration = self%concentration
    end select
  end subroutine tcd042_clone_payload

  logical function tcd042_payload_valid(self)
    class(tcd042_top_state_t), intent(in) :: self
    tcd042_payload_valid = ieee_is_finite(self%concentration)
  end function tcd042_payload_valid

  subroutine initialize_tcd042_store(store, lineage_id, time, concentration, ok)
    type(accepted_store_t), intent(out) :: store
    character(len=*), intent(in) :: lineage_id
    type(TimeCoordinate), intent(in) :: time
    real(real64), intent(in) :: concentration
    logical, intent(out) :: ok
    type(tcd042_top_state_t) :: payload

    payload%concentration = concentration
    call initialize_accepted_store(lineage_id, time, payload, store, ok)
  end subroutine initialize_tcd042_store

  subroutine configure_tcd042_client(client, hydrology, hetop, load_rate, ok)
    type(tcd042_upper_boundary_client_t), intent(inout) :: client
    type(tcd042_resolved_hydrology_t), intent(in) :: hydrology
    real(real64), intent(in) :: hetop, load_rate
    logical, intent(out) :: ok

    client%hydrology = tcd042_resolved_hydrology_t()
    client%hydrology_present = .false.
    client%process_forcing_present = .false.
    client%hetop = 0.0_real64
    client%load_rate = 0.0_real64
    call reset_diagnostics(client)

    ok = resolved_hydrology_valid(hydrology)
    if (.not. ok) return
    if (.not. ieee_is_finite(hetop) .or. hetop <= 0.0_real64) then
      ok = .false.
      return
    end if
    if (.not. ieee_is_finite(load_rate)) then
      ok = .false.
      return
    end if

    client%hydrology = hydrology
    client%hydrology_present = .true.
    client%hetop = hetop
    client%load_rate = load_rate
    client%process_forcing_present = .true.
    ok = .true.
  end subroutine configure_tcd042_client

  subroutine tcd042_last_diagnostics(client, average_concentration, flux, p, branch_id, valid)
    type(tcd042_upper_boundary_client_t), intent(in) :: client
    real(real64), intent(out) :: average_concentration, flux, p
    integer, intent(out) :: branch_id
    logical, intent(out) :: valid

    average_concentration = client%last_average_concentration
    flux = client%last_flux
    p = client%last_p
    branch_id = client%last_branch
    valid = client%last_diagnostic_valid
  end subroutine tcd042_last_diagnostics

  logical function resolved_hydrology_valid(hydrology)
    type(tcd042_resolved_hydrology_t), intent(in) :: hydrology

    resolved_hydrology_valid = .false.
    if (trim(hydrology%schema_id) /= TCD042_RESOLVED_HYDROLOGY_SCHEMA) return
    if (hydrology%flpn /= 0) return
    if (.not. ieee_is_finite(hydrology%flib_top)) return
    if (.not. ieee_is_finite(hydrology%rurv)) return
    if (hydrology%flib_top < 0.0_real64) return
    ! Frozen revision-53 Hydro_detailed forces Rurv to exact zero when Flpn=0.
    if (hydrology%rurv /= 0.0_real64) return
    resolved_hydrology_valid = .true.
  end function resolved_hydrology_valid

  subroutine reset_diagnostics(client)
    type(tcd042_upper_boundary_client_t), intent(inout) :: client
    client%last_average_concentration = 0.0_real64
    client%last_flux = 0.0_real64
    client%last_p = 0.0_real64
    client%last_branch = TCD042_BRANCH_NONE
    client%last_diagnostic_valid = .false.
  end subroutine reset_diagnostics

  subroutine execute_tcd042_attempt(self, origin_payload, origin_time, endpoint_time, &
      candidate_payload, admissibility, ok, reason)
    class(tcd042_upper_boundary_client_t), intent(inout) :: self
    class(transient_payload_t), intent(in) :: origin_payload
    type(TimeCoordinate), intent(in) :: origin_time, endpoint_time
    class(transient_payload_t), allocatable, intent(out) :: candidate_payload
    type(admissibility_t), intent(out) :: admissibility
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    integer :: ordering
    logical :: compare_ok
    integer(int64) :: step_days_i
    real(real64) :: st, flux, p, a1, a2, b1, b2, f, g
    real(real64) :: c0, c1, cavg, flux_sum

    call reset_diagnostics(self)
    admissibility = admissibility_t()
    ok = .false.
    reason = 'UNSET'

    if (.not. self%hydrology_present .or. .not. self%process_forcing_present) then
      reason = 'MISSING_TCD042_FORCING'
      return
    end if
    if (.not. resolved_hydrology_valid(self%hydrology)) then
      reason = 'INVALID_RESOLVED_HYDROLOGY'
      return
    end if
    if (trim(origin_time%calendar_contract_id) /= trim(endpoint_time%calendar_contract_id)) then
      reason = 'TIME_CALENDAR_MISMATCH'
      return
    end if
    if (origin_time%subday_numerator /= 0_int64 .or. endpoint_time%subday_numerator /= 0_int64) then
      reason = 'SUBDAY_TCD042_RUNTIME_NOT_QUALIFIED'
      return
    end if

    call time_compare(endpoint_time, origin_time, ordering, compare_ok)
    if (.not. compare_ok .or. ordering <= 0) then
      reason = 'INVALID_TCD042_INTERVAL'
      return
    end if
    step_days_i = endpoint_time%day_index - origin_time%day_index
    if (step_days_i <= 0_int64 .or. step_days_i > MAX_EXACT_REAL64_INTEGER) then
      reason = 'TCD042_INTERVAL_NOT_EXACT_REAL64_DAY'
      return
    end if
    st = real(step_days_i, real64)

    flux_sum = self%hydrology%flib_top + self%hydrology%rurv
    if (.not. ieee_is_finite(flux_sum)) then
      reason = 'NONFINITE_TCD042_FLUX'
      return
    end if
    flux = max(0.0_real64, flux_sum)

    select type (origin => origin_payload)
    type is (tcd042_top_state_t)
      c0 = origin%concentration
    class default
      reason = 'INVALID_TCD042_ACCEPTED_PAYLOAD'
      return
    end select
    if (.not. ieee_is_finite(c0)) then
      reason = 'NONFINITE_TCD042_ACCEPTED_CONCENTRATION'
      return
    end if

    if (flux == 0.0_real64) then
      a1 = 1.0_real64
      a2 = st / self%hetop
      b1 = 1.0_real64
      b2 = st / (2.0_real64 * self%hetop)
      p = 0.0_real64
      self%last_branch = TCD042_BRANCH_B1_EXACT_ZERO
    else
      if (flux >= TCD042_FLUX_THRESHOLD) then
        reason = 'TCD042_FLUX_OUTSIDE_ADMITTED_PARENT_SCOPE'
        return
      end if
      p = st * flux / self%hetop
      if (.not. ieee_is_finite(p) .or. p <= 0.0_real64 .or. p > TCD042_P_MAX) then
        reason = 'TCD042_P_OUTSIDE_NQ03_ADMITTED_ENVELOPE'
        return
      end if
      a1 = exp(-p)
      f = 1.0_real64 - p / 2.0_real64 + p * p / 6.0_real64
      g = 0.5_real64 - p / 6.0_real64 + p * p / 24.0_real64
      a2 = (st / self%hetop) * f
      b1 = f
      b2 = (st / self%hetop) * g
      self%last_branch = TCD042_BRANCH_E1_NQ03
    end if

    c1 = c0 * a1 + self%load_rate * a2
    cavg = c0 * b1 + self%load_rate * b2
    if (.not. ieee_is_finite(c1) .or. .not. ieee_is_finite(cavg)) then
      self%last_branch = TCD042_BRANCH_NONE
      reason = 'NONFINITE_TCD042_RESULT'
      return
    end if

    allocate(tcd042_top_state_t :: candidate_payload)
    select type (candidate => candidate_payload)
    type is (tcd042_top_state_t)
      candidate%concentration = c1
    end select

    self%last_average_concentration = cavg
    self%last_flux = flux
    self%last_p = p
    self%last_diagnostic_valid = .true.

    admissibility%evidence_complete = .true.
    admissibility%admissible = .true.
    ok = .true.
    if (self%last_branch == TCD042_BRANCH_B1_EXACT_ZERO) then
      reason = 'TCD042_B1_EXACT_ZERO_CANDIDATE'
    else
      reason = 'TCD042_E1_NQ03_CANDIDATE'
    end if
  end subroutine execute_tcd042_attempt

end module mod_animo_tcd042_upper_boundary_client
