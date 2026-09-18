program test_stateq09_detailed_hydrology_origin
  use iso_fortran_env, only: int64, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_value, ieee_quiet_nan
  use mod_animo_detailed_hydrology_origin_state, only: &
    detailed_hydrology_origin_state_t, make_detailed_hydrology_origin_state, &
    advance_origin_from_accepted_endpoint, validate_detailed_hydrology_origin_state
  implicit none

  call test_exact_endpoint_to_origin_transfer()
  call test_profile_length_preserved()
  call test_nonfinite_rejected()
  call test_unallocated_profile_rejected()
  print *, 'PASS_STATEQ09_DETAILED_HYDROLOGY_ORIGIN_CONTINUATION'

contains

  subroutine assert_true(value,message)
    logical,intent(in)::value
    character(len=*),intent(in)::message
    if(.not.value)then
      print *,'ASSERTION FAILED: ',trim(message)
      error stop 1
    end if
  end subroutine assert_true

  subroutine test_exact_endpoint_to_origin_transfer()
    type(detailed_hydrology_origin_state_t)::s
    real(real64)::mofrt(2)
    logical::ok
    character(len=96)::reason

    mofrt=[0.30_real64,0.28_real64]
    call advance_origin_from_accepted_endpoint(0.001_real64,0.002_real64,0.003_real64, &
      mofrt,s,ok,reason)
    call assert_true(ok,'endpoint transfer')
    call assert_true(transfer(s%pn,0_int64)==transfer(0.001_real64,0_int64),'Pn=Pnt exact')
    call assert_true(transfer(s%sic,0_int64)==transfer(0.002_real64,0_int64),'Sic=Sict exact')
    call assert_true(transfer(s%snla,0_int64)==transfer(0.003_real64,0_int64),'Snla=Snt exact')
    call assert_true(all(transfer(s%mofro,[0_int64,0_int64])== &
      transfer(mofrt,[0_int64,0_int64])),'Mofro=Mofrt exact')
  end subroutine test_exact_endpoint_to_origin_transfer

  subroutine test_profile_length_preserved()
    type(detailed_hydrology_origin_state_t)::s
    real(real64)::mofrt(3)
    logical::ok
    character(len=96)::reason

    mofrt=[0.1_real64,0.2_real64,0.3_real64]
    call make_detailed_hydrology_origin_state(0.0_real64,0.0_real64,0.0_real64,mofrt,s,ok,reason)
    call assert_true(ok,'three-layer origin')
    call assert_true(size(s%mofro)==3,'profile length preserved')
  end subroutine test_profile_length_preserved

  subroutine test_nonfinite_rejected()
    type(detailed_hydrology_origin_state_t)::s
    real(real64)::mofrt(1),nan_value
    logical::ok
    character(len=96)::reason

    nan_value=ieee_value(0.0_real64,ieee_quiet_nan)
    mofrt=[nan_value]
    call make_detailed_hydrology_origin_state(0.0_real64,0.0_real64,0.0_real64,mofrt,s,ok,reason)
    call assert_true(.not.ok,'NaN Mofro rejected')
  end subroutine test_nonfinite_rejected

  subroutine test_unallocated_profile_rejected()
    type(detailed_hydrology_origin_state_t)::s
    logical::ok
    character(len=96)::reason

    s%schema_id='ANIMO_DETAILED_HYDROLOGY_ORIGIN_STATE_V1'
    s%transfer_contract_id='REV53_INIT_IWA2_IOPTHYVS1_HLPIMP11'
    call validate_detailed_hydrology_origin_state(s,ok,reason)
    call assert_true(.not.ok,'unallocated Mofro rejected')
  end subroutine test_unallocated_profile_rejected

end program test_stateq09_detailed_hydrology_origin
