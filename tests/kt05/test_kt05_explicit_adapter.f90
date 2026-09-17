program test_kt05_explicit_adapter
  use, intrinsic :: iso_fortran_env, only : real64
  use, intrinsic :: ieee_arithmetic, only : ieee_value, ieee_quiet_nan
  use mod_animo_hydrology_adapter
  implicit none

  type(hydrology_step_t) :: step
  type(hydro_detailed_external_t) :: projection
  integer :: status
  real(real64) :: legacy_mofrt(0:2), legacy_flev(0:2), legacy_flab(0:3)
  real(real64) :: legacy_fldr(1,0:2)
  real(real64) :: zero_mofrt(0:2), zero_flev(0:2), zero_flab(0:3)
  real(real64), allocatable :: zero_fldr(:,:)

  call make_valid_step(step)
  call project_hydro_detailed_explicit(step, projection, status)
  call assert_equal_int(status, KT05_OK, 'valid projection status')
  call assert_equal_real(projection%sict, 0.0015_real64, 'Sict projection')
  call assert_equal_real(projection%st, 1.0_real64, 'St projection')
  call assert_equal_real(projection%flab(3), -0.0002_real64, 'Flab projection')
  call assert_equal_real(projection%fldr(1, 2), 0.00002_real64, 'Fldr projection')
  call assert_equal_real(projection%mofrt(2), 0.28_real64, 'Mofrt projection')

  legacy_mofrt = -999.0_real64
  legacy_flev = -999.0_real64
  legacy_flab = -999.0_real64
  legacy_fldr = -999.0_real64
  call apply_projection_to_legacy_slices( &
    projection, legacy_mofrt, legacy_flev, legacy_flab, legacy_fldr, status)
  call assert_equal_int(status, KT05_OK, 'legacy slice mapping status')
  call assert_equal_real(legacy_mofrt(0), -999.0_real64, 'Mofrt index zero preserved')
  call assert_equal_real(legacy_flev(0), -999.0_real64, 'Flev index zero preserved')
  call assert_equal_real(legacy_flab(0), -999.0_real64, 'Flab index zero preserved')
  call assert_equal_real(legacy_fldr(1,0), -999.0_real64, 'Fldr index zero preserved')
  call assert_equal_real(legacy_mofrt(1), 0.30_real64, 'Mofrt index one mapping')
  call assert_equal_real(legacy_flev(2), 0.0006_real64, 'Flev index two mapping')
  call assert_equal_real(legacy_flab(3), -0.0002_real64, 'Flab Nl+1 mapping')
  call assert_equal_real(legacy_fldr(1,2), 0.00002_real64, 'Fldr layer mapping')

  projection%prr = ieee_value(projection%prr, ieee_quiet_nan)
  legacy_mofrt = -777.0_real64
  call apply_projection_to_legacy_slices( &
    projection, legacy_mofrt, legacy_flev, legacy_flab, legacy_fldr, status)
  call assert_equal_int(status, KT05_ERR_NONFINITE, 'corrupt public projection rejected')
  call assert_equal_real(legacy_mofrt(1), -777.0_real64, 'corrupt projection copied nothing')

  step%schema_id = 'WRONG'
  call validate_hydrology_step_explicit(step, status)
  call assert_equal_int(status, KT05_ERR_SCHEMA, 'schema mismatch')

  call make_valid_step(step)
  step%unit_contract_id = 'WRONG'
  call validate_hydrology_step_explicit(step, status)
  call assert_equal_int(status, KT05_ERR_UNITS, 'unit mismatch')

  call make_valid_step(step)
  step%has_interception_storage_end = .false.
  call validate_hydrology_step_explicit(step, status)
  call assert_equal_int(status, KT05_ERR_EXPLICIT_INTERCEPTION, 'missing explicit interception')

  call make_valid_step(step)
  deallocate(step%flev)
  allocate(step%flev(1))
  step%flev = 0.0_real64
  call validate_hydrology_step_explicit(step, status)
  call assert_equal_int(status, KT05_ERR_DIMENSIONS, 'dimension mismatch')

  call make_valid_step(step)
  step%producer_step_days = 0.0_real64
  call validate_hydrology_step_explicit(step, status)
  call assert_equal_int(status, KT05_ERR_TIME, 'non-positive producer timestep')

  call make_valid_step(step)
  step%prr = ieee_value(step%prr, ieee_quiet_nan)
  call validate_hydrology_step_explicit(step, status)
  call assert_equal_int(status, KT05_ERR_NONFINITE, 'nonfinite scalar')

  call make_valid_step(step)
  step%fldr(1, 1) = ieee_value(step%fldr(1, 1), ieee_quiet_nan)
  call validate_hydrology_step_explicit(step, status)
  call assert_equal_int(status, KT05_ERR_NONFINITE, 'nonfinite profile')

  call make_zero_optional_step(step)
  call project_hydro_detailed_explicit(step, projection, status)
  call assert_equal_int(status, KT05_OK, 'zero optional projection status')
  call assert_equal_int(projection%drainage_count, 0, 'zero drainage projection')
  call assert_equal_int(size(projection%fldr, 1), 0, 'zero drainage extent')
  zero_mofrt = -555.0_real64
  zero_flev = -555.0_real64
  zero_flab = -555.0_real64
  allocate(zero_fldr(0,0:2))
  call apply_projection_to_legacy_slices( &
    projection, zero_mofrt, zero_flev, zero_flab, zero_fldr, status)
  call assert_equal_int(status, KT05_OK, 'zero drainage slice mapping status')
  call assert_equal_int(size(zero_fldr, 1), 0, 'zero drainage target remains empty')
  call assert_equal_real(zero_mofrt(0), -555.0_real64, 'zero drainage Mofrt index zero preserved')
  call assert_equal_real(zero_flev(0), -555.0_real64, 'zero drainage Flev index zero preserved')
  call assert_equal_real(zero_flab(0), -555.0_real64, 'zero drainage Flab index zero preserved')
  call assert_equal_real(zero_mofrt(1), step%mofrt(1), 'zero drainage Mofrt mapping')

  print '(A)', 'KT05 explicit Fortran hydrology adapter tests: PASS'

contains

  subroutine make_valid_step(value)
    type(hydrology_step_t), intent(out) :: value

    value%schema_id = HYDROLOGY_SCHEMA_ID
    value%unit_contract_id = HYDROLOGY_UNIT_CONTRACT_ID
    value%layer_count = 2
    value%drainage_count = 1
    value%producer_endpoint_day = 10.0_real64
    value%producer_step_days = 1.0_real64
    value%prr = 0.002_real64
    value%prsn = 0.0_real64
    value%prirr = 0.0_real64
    value%evicpr = 0.0002_real64
    value%evicirr = 0.0_real64
    value%evsn = 0.0_real64
    value%evso = 0.0005_real64
    value%evpn = 0.0_real64
    value%evsoma = 0.0006_real64
    value%evtrma = 0.001_real64
    value%runon = 0.0_real64
    value%runoff = 0.0001_real64
    value%groundwater_level = 1.2_real64
    value%ponding_end = 0.0_real64
    value%snow_storage_end = 0.0_real64
    value%water_balance_aeration = 0.0_real64
    allocate(value%sc(2), value%mofrt(2), value%flev(2), value%flab(3))
    allocate(value%fldr(1, 2), value%soil_temperature(2))
    value%sc = [-10.0_real64, -20.0_real64]
    value%mofrt = [0.30_real64, 0.28_real64]
    value%flev = [0.0004_real64, 0.0006_real64]
    value%flab = [0.0003_real64, 0.0001_real64, -0.0002_real64]
    value%fldr = reshape([0.00001_real64, 0.00002_real64], [1, 2])
    value%has_interception_storage_end = .true.
    value%interception_storage_end = 0.0015_real64
    value%has_soil_temperature = .true.
    value%soil_temperature = [8.0_real64, 8.5_real64]
  end subroutine make_valid_step

  subroutine make_zero_optional_step(value)
    type(hydrology_step_t), intent(out) :: value

    value%schema_id = HYDROLOGY_SCHEMA_ID
    value%unit_contract_id = HYDROLOGY_UNIT_CONTRACT_ID
    value%layer_count = 2
    value%drainage_count = 0
    value%producer_endpoint_day = 11.0_real64
    value%producer_step_days = 1.0_real64
    value%groundwater_level = 1.0_real64
    allocate(value%sc(2), value%mofrt(2), value%flev(2), value%flab(3))
    allocate(value%fldr(0, 2), value%soil_temperature(0))
    value%sc = [-5.0_real64, -6.0_real64]
    value%mofrt = [0.31_real64, 0.29_real64]
    value%flev = [0.0_real64, 0.0_real64]
    value%flab = [0.0_real64, 0.0_real64, 0.0_real64]
    value%has_interception_storage_end = .true.
    value%interception_storage_end = 0.0_real64
    value%has_soil_temperature = .false.
  end subroutine make_zero_optional_step

  subroutine assert_equal_int(actual, expected, label)
    integer, intent(in) :: actual, expected
    character(len=*), intent(in) :: label
    if (actual /= expected) then
      write (*, '(A,": expected ",I0,", got ",I0)') trim(label), expected, actual
      error stop 1
    end if
  end subroutine assert_equal_int

  subroutine assert_equal_real(actual, expected, label)
    real(real64), intent(in) :: actual, expected
    character(len=*), intent(in) :: label
    if (abs(actual - expected) > 1.0e-14_real64) then
      write (*, '(A,": expected ",ES16.8,", got ",ES16.8)') trim(label), expected, actual
      error stop 1
    end if
  end subroutine assert_equal_real

end program test_kt05_explicit_adapter
