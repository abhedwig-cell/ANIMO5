program test_kt09_real_anchor_projection
  use, intrinsic :: iso_fortran_env, only : real64
  use mod_animo_hydrology_adapter
  use mod_kt09_real_lwkm_anchors
  implicit none

  type(hydrology_step_t) :: step
  type(hydro_detailed_external_t) :: projection
  integer :: status, i, nl, nudr
  logical :: seen8, seen9, seen10, seen11, seen_nonzero_sict
  real(real64), allocatable :: legacy_mofrt(:), legacy_flev(:)
  real(real64), allocatable :: legacy_flab(:), legacy_fldr(:,:)

  seen8 = .false.
  seen9 = .false.
  seen10 = .false.
  seen11 = .false.
  seen_nonzero_sict = .false.

  do i = 1, KT09_ANCHOR_COUNT
    call make_kt09_anchor_step(i, step)
    call validate_hydrology_step_explicit(step, status)
    call assert_equal_int(status, KT05_OK, 'anchor validation')
    call assert_equal_real(step%producer_endpoint_day, KT09_ENDPOINT(i), 'endpoint identity')
    call assert_equal_real(step%producer_step_days, KT09_DURATION(i), 'duration identity')

    select case (nint(step%producer_step_days))
    case (8)
      seen8 = .true.
    case (9)
      seen9 = .true.
    case (10)
      seen10 = .true.
    case (11)
      seen11 = .true.
    case default
      call assert_true(.false., 'unexpected duration class')
    end select
    if (step%interception_storage_end /= 0.0_real64) seen_nonzero_sict = .true.

    call project_hydro_detailed_explicit(step, projection, status)
    call assert_equal_int(status, KT05_OK, 'anchor projection')

    call assert_equal_int(projection%layer_count, step%layer_count, 'layer count')
    call assert_equal_int(projection%drainage_count, step%drainage_count, 'drainage count')
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
    call assert_same_vector(projection%mofrt, step%mofrt, 'Mofrt')
    call assert_same_vector(projection%flev, step%flev, 'Flev')
    call assert_same_vector(projection%flab, step%flab, 'Flab')
    call assert_same_matrix(projection%fldr, step%fldr, 'Fldr')

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
    call assert_equal_int(status, KT05_OK, 'legacy slice mapping')
    call assert_equal_real(legacy_mofrt(0), -999.0_real64, 'Mofrt zero preserved')
    call assert_equal_real(legacy_flev(0), -999.0_real64, 'Flev zero preserved')
    call assert_equal_real(legacy_flab(0), -999.0_real64, 'Flab zero preserved')
    call assert_constant_vector(legacy_fldr(:,0), -999.0_real64, 'Fldr zero preserved')
    call assert_same_vector(legacy_mofrt(1:nl), step%mofrt, 'Mofrt slices')
    call assert_same_vector(legacy_flev(1:nl), step%flev, 'Flev slices')
    call assert_same_vector(legacy_flab(1:nl + 1), step%flab, 'Flab slices')
    call assert_same_matrix(legacy_fldr(1:nudr,1:nl), step%fldr, 'Fldr slices')

    deallocate(legacy_mofrt, legacy_flev, legacy_flab, legacy_fldr)
  end do

  call assert_true(seen8 .and. seen9 .and. seen10 .and. seen11, 'all duration classes')
  call assert_true(seen_nonzero_sict, 'nonzero explicit interception represented')
  print '(A)', 'KT09 representative real LWKM packets through frozen KT05: PASS'

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
      write (*, '(A)') 'ASSERTION FAILED: '//trim(label)
      error stop 1
    end if
  end subroutine assert_equal_int

  subroutine assert_equal_real(actual, expected, label)
    real(real64), intent(in) :: actual, expected
    character(len=*), intent(in) :: label
    if (abs(actual - expected) > 0.0_real64) then
      write (*, '(A)') 'ASSERTION FAILED: '//trim(label)
      error stop 1
    end if
  end subroutine assert_equal_real

  subroutine assert_same_vector(actual, expected, label)
    real(real64), intent(in) :: actual(:), expected(:)
    character(len=*), intent(in) :: label
    call assert_true(size(actual) == size(expected), trim(label)//' size')
    if (size(actual) > 0) then
      call assert_true(maxval(abs(actual - expected)) <= 0.0_real64, label)
    end if
  end subroutine assert_same_vector

  subroutine assert_same_matrix(actual, expected, label)
    real(real64), intent(in) :: actual(:,:), expected(:,:)
    character(len=*), intent(in) :: label
    call assert_true(all(shape(actual) == shape(expected)), trim(label)//' shape')
    if (size(actual) > 0) then
      call assert_true(maxval(abs(actual - expected)) <= 0.0_real64, label)
    end if
  end subroutine assert_same_matrix

  subroutine assert_constant_vector(actual, expected, label)
    real(real64), intent(in) :: actual(:), expected
    character(len=*), intent(in) :: label
    if (size(actual) > 0) then
      call assert_true(maxval(abs(actual - expected)) <= 0.0_real64, label)
    end if
  end subroutine assert_constant_vector

end program test_kt09_real_anchor_projection
