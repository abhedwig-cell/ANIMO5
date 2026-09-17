program test_kt07_real_packet_projection
  use, intrinsic :: iso_fortran_env, only : real64
  use mod_animo_hydrology_adapter
  use mod_kt07_real_lwkm_fixture, only : make_kt07_lwkm_step
  implicit none

  type(hydrology_step_t) :: step
  type(hydro_detailed_external_t) :: projection
  integer :: status, nl, nudr
  real(real64), allocatable :: legacy_mofrt(:), legacy_flev(:)
  real(real64), allocatable :: legacy_flab(:), legacy_fldr(:,:)

  call make_kt07_lwkm_step(step)
  call validate_hydrology_step_explicit(step, status)
  call assert_equal_int(status, KT05_OK, 'real packet validation')

  call project_hydro_detailed_explicit(step, projection, status)
  call assert_equal_int(status, KT05_OK, 'real packet projection')

  call assert_equal_int(projection%layer_count, 30, 'LWKM layer count')
  call assert_equal_int(projection%drainage_count, 5, 'LWKM drainage count')
  call assert_equal_real(projection%st, step%producer_step_days, 'St')
  call assert_equal_real(projection%sict, step%interception_storage_end, 'Sict')
  call assert_equal_real(projection%prr, step%prr, 'Prr')
  call assert_equal_real(projection%prsn, step%prsn, 'Prsn')
  call assert_equal_real(projection%prirr, step%prirr, 'Prirr')
  call assert_equal_real(projection%evicpr, step%evicpr, 'Evicpr')
  call assert_equal_real(projection%evicirr, step%evicirr, 'Evicirr')
  call assert_equal_real(projection%evsn, step%evsn, 'Evsn')
  call assert_equal_real(projection%evso, step%evso, 'Evso')
  call assert_equal_real(projection%evpn, step%evpn, 'Evpn')
  call assert_equal_real(projection%evsoma, step%evsoma, 'Evsoma')
  call assert_equal_real(projection%evtrma, step%evtrma, 'Evtrma')
  call assert_equal_real(projection%runon, step%runon, 'Runon')
  call assert_equal_real(projection%ru, step%runoff, 'Ru')
  call assert_equal_real(projection%pnt, step%ponding_end, 'Pnt')
  call assert_equal_real(projection%snt, step%snow_storage_end, 'Snt')

  call assert_same_vector(projection%mofrt, step%mofrt, 'Mofrt projection')
  call assert_same_vector(projection%flev, step%flev, 'Flev projection')
  call assert_same_vector(projection%flab, step%flab, 'Flab projection')
  call assert_same_matrix(projection%fldr, step%fldr, 'Fldr projection')

  nl = step%layer_count
  nudr = step%drainage_count
  allocate(legacy_mofrt(0:nl), legacy_flev(0:nl))
  allocate(legacy_flab(0:nl + 1), legacy_fldr(nudr, 0:nl))
  legacy_mofrt = -999.0_real64
  legacy_flev = -999.0_real64
  legacy_flab = -999.0_real64
  legacy_fldr = -999.0_real64

  call apply_projection_to_legacy_slices( &
    projection, legacy_mofrt, legacy_flev, legacy_flab, legacy_fldr, status)
  call assert_equal_int(status, KT05_OK, 'real packet legacy mapping')
  call assert_equal_real(legacy_mofrt(0), -999.0_real64, 'Mofrt zero preserved')
  call assert_equal_real(legacy_flev(0), -999.0_real64, 'Flev zero preserved')
  call assert_equal_real(legacy_flab(0), -999.0_real64, 'Flab zero preserved')
  call assert_constant_vector(legacy_fldr(:,0), -999.0_real64, 'Fldr zero preserved')
  call assert_same_vector(legacy_mofrt(1:nl), step%mofrt, 'Mofrt slices')
  call assert_same_vector(legacy_flev(1:nl), step%flev, 'Flev slices')
  call assert_same_vector(legacy_flab(1:nl + 1), step%flab, 'Flab slices')
  call assert_same_matrix(legacy_fldr(1:nudr,1:nl), step%fldr, 'Fldr slices')

  print '(A)', 'KT07 full derived LWKM packet projection: PASS'

contains

  subroutine assert_true(condition, label)
    logical, intent(in) :: condition
    character(len=*), intent(in) :: label
    if (.not. condition) then
      write (*, '(A)') 'ASSERTION FAILED: '//trim(label)
      error stop 1
    end if
  end subroutine assert_true

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
    if (abs(actual - expected) > 0.0_real64) then
      write (*, '(A,": expected ",ES16.8,", got ",ES16.8)') trim(label), expected, actual
      error stop 1
    end if
  end subroutine assert_equal_real

  subroutine assert_same_vector(actual, expected, label)
    real(real64), intent(in) :: actual(:), expected(:)
    character(len=*), intent(in) :: label
    call assert_true(size(actual) == size(expected), trim(label)//' size')
    if (size(actual) > 0) then
      if (maxval(abs(actual - expected)) > 0.0_real64) then
        write (*, '(A)') 'ASSERTION FAILED: '//trim(label)
        error stop 1
      end if
    end if
  end subroutine assert_same_vector

  subroutine assert_same_matrix(actual, expected, label)
    real(real64), intent(in) :: actual(:,:), expected(:,:)
    character(len=*), intent(in) :: label
    call assert_true(all(shape(actual) == shape(expected)), trim(label)//' shape')
    if (size(actual) > 0) then
      if (maxval(abs(actual - expected)) > 0.0_real64) then
        write (*, '(A)') 'ASSERTION FAILED: '//trim(label)
        error stop 1
      end if
    end if
  end subroutine assert_same_matrix

  subroutine assert_constant_vector(actual, expected, label)
    real(real64), intent(in) :: actual(:), expected
    character(len=*), intent(in) :: label
    if (size(actual) > 0) then
      if (maxval(abs(actual - expected)) > 0.0_real64) then
        write (*, '(A)') 'ASSERTION FAILED: '//trim(label)
        error stop 1
      end if
    end if
  end subroutine assert_constant_vector

end program test_kt07_real_packet_projection
