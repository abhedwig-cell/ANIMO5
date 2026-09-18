program test_stateq10_first_detailed_hydrology_origin
  use iso_fortran_env, only: int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_value, ieee_quiet_nan
  use mod_animo_first_detailed_hydrology_origin, only: &
    first_detailed_hydrology_origin_t, normalize_rev53_real4, &
    make_first_detailed_hydrology_origin, validate_first_detailed_hydrology_origin
  implicit none

  call test_dble_trunc_exact_oracles()
  call test_first_origin_normalization()
  call test_nonfinite_rejected()
  call test_unallocated_profile_rejected()
  print *, 'PASS_STATEQ10_FIRST_DETAILED_HYDROLOGY_ORIGIN'

contains

  subroutine assert_true(value,message)
    logical,intent(in)::value
    character(len=*),intent(in)::message
    if(.not.value)then
      print *,'ASSERTION FAILED: ',trim(message)
      error stop 1
    end if
  end subroutine assert_true

  subroutine test_dble_trunc_exact_oracles()
    real(real64)::v

    v=normalize_rev53_real4(0.123456789_real32)
    call assert_true(transfer(v,0_int64)==int(z'3FBF9ADD6678041E',int64), &
      'Dble_trunc 0.123456789 exact')

    v=normalize_rev53_real4(123.45678_real32)
    call assert_true(transfer(v,0_int64)==int(z'405EDD3BE0157EED',int64), &
      'Dble_trunc 123.45678 exact')

    v=normalize_rev53_real4(-0.000123456789_real32)
    call assert_true(transfer(v,0_int64)==int(z'BF202E85D6418B53',int64), &
      'Dble_trunc negative small exact')

    v=normalize_rev53_real4(1.0_real32)
    call assert_true(transfer(v,0_int64)==int(z'3FF0000000000000',int64), &
      'Dble_trunc integer exact')
  end subroutine test_dble_trunc_exact_oracles

  subroutine test_first_origin_normalization()
    type(first_detailed_hydrology_origin_t)::s
    real(real32)::m(2)
    logical::ok
    character(len=96)::reason

    m=[0.123456789_real32,0.2500000_real32]
    call make_first_detailed_hydrology_origin(m,0.00123456789_real32, &
      0.000123456789_real32,0.0123456789_real32,s,ok,reason)
    call assert_true(ok,'first origin normalized')
    call assert_true(size(s%mofro)==2,'profile extent')
    call assert_true(transfer(s%mofro(1),0_int64)==int(z'3FBF9ADD6678041E',int64), &
      'Mofro Dble_trunc exact')
    call assert_true(transfer(s%mofro(2),0_int64)==int(z'3FD0000000000000',int64),'Mofro quarter exact')
    call assert_true(transfer(s%pn,0_int64)==transfer(normalize_rev53_real4( &
      0.000123456789_real32),0_int64),'Pn normalized')
    call assert_true(transfer(s%sic,0_int64)==transfer(normalize_rev53_real4( &
      0.00123456789_real32),0_int64),'Sic normalized')
    call assert_true(transfer(s%snla,0_int64)==transfer(normalize_rev53_real4( &
      0.0123456789_real32),0_int64),'Snla normalized')
  end subroutine test_first_origin_normalization

  subroutine test_nonfinite_rejected()
    type(first_detailed_hydrology_origin_t)::s
    real(real32)::m(1),nanv
    logical::ok
    character(len=96)::reason

    nanv=ieee_value(0.0_real32,ieee_quiet_nan)
    m=[nanv]
    call make_first_detailed_hydrology_origin(m,0.0_real32,0.0_real32,0.0_real32,s,ok,reason)
    call assert_true(.not.ok,'NaN input rejected')
  end subroutine test_nonfinite_rejected

  subroutine test_unallocated_profile_rejected()
    type(first_detailed_hydrology_origin_t)::s
    logical::ok
    character(len=96)::reason

    s%schema_id='ANIMO_FIRST_DETAILED_HYDROLOGY_ORIGIN_V1'
    s%source_contract_id='REV53_INPUT1_HLPIMP11_IOPTHYVS1'
    call validate_first_detailed_hydrology_origin(s,ok,reason)
    call assert_true(.not.ok,'unallocated profile rejected')
  end subroutine test_unallocated_profile_rejected

end program test_stateq10_first_detailed_hydrology_origin
