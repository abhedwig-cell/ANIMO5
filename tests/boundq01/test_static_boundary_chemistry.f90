program test_boundq01_static_boundary
  use iso_fortran_env, only: int64, real64
  use mod_animo_static_boundary_chemistry_adapter, only: &
    static_boundary_chemistry_t, read_rev53_static_boundary_chemistry, &
    BOUNDQ01_OK, BOUNDQ01_ERR_OPTION, BOUNDQ01_ERR_RANGE
  implicit none

  type(static_boundary_chemistry_t) :: v
  integer :: status

  call read_rev53_static_boundary_chemistry('tests/boundq01/fixtures/static_no_p.inp',3,0,v,status)
  call assert_int(status,BOUNDQ01_OK,'no-P fixture parses')
  call assert_bits(v%precipitation_nh(2),transfer(0.002_real64,0_int64),'year array exact')
  call assert_bits(v%runon%nh,transfer(0.10_real64,0_int64),'runon NH exact')
  call assert_bits(v%irrigation%don,transfer(0.80_real64,0_int64),'irrigation DON exact')
  call assert_bits(v%runin%doma,transfer(0.13_real64,0_int64),'runin DOM exact')
  call assert_true(.not.v%phosphorus_enabled,'no-P presence')

  call read_rev53_static_boundary_chemistry('tests/boundq01/fixtures/static_p.inp',2,1,v,status)
  call assert_int(status,BOUNDQ01_OK,'P fixture parses')
  call assert_bits(v%precipitation_po(2),transfer(0.006_real64,0_int64),'P yearly exact')
  call assert_bits(v%runon%po,transfer(0.30_real64,0_int64),'runon PO exact')
  call assert_bits(v%runon%dop,transfer(0.60_real64,0_int64),'runon DOP exact')
  call assert_bits(v%irrigation%po,transfer(0.90_real64,0_int64),'irrigation PO exact')
  call assert_bits(v%runin%dop,transfer(0.016_real64,0_int64),'runin DOP exact')
  call assert_true(v%phosphorus_enabled,'P presence')

  call write_bad_option()
  call read_rev53_static_boundary_chemistry('tests/boundq01/fixtures/bad_option.inp',1,0,v,status)
  call assert_int(status,BOUNDQ01_ERR_OPTION,'dynamic option rejected by bounded adapter')

  call write_bad_range()
  call read_rev53_static_boundary_chemistry('tests/boundq01/fixtures/bad_range.inp',1,0,v,status)
  call assert_int(status,BOUNDQ01_ERR_RANGE,'source range violation rejected')

  call write_duplicate_labels()
  call read_rev53_static_boundary_chemistry('tests/boundq01/fixtures/duplicate_labels.inp',1,0,v,status)
  call assert_int(status,BOUNDQ01_OK,'duplicate fixture parses first labels')
  call assert_bits(v%runon%nh,transfer(0.10_real64,0_int64),'first matching topbou wins')

  call write_case_mismatch()
  call read_rev53_static_boundary_chemistry('tests/boundq01/fixtures/case_mismatch.inp',1,0,v,status)
  call assert_int(status,2,'label comparison is exact and case-sensitive')

  print *, 'PASS_BOUNDQ01_STATIC_BOUNDARY_CHEMISTRY'

contains

  subroutine assert_true(x,msg)
    logical,intent(in)::x
    character(len=*),intent(in)::msg
    if(.not.x)then
      print *,'ASSERTION FAILED: ',trim(msg)
      error stop 1
    end if
  end subroutine assert_true

  subroutine assert_int(actual,expected,msg)
    integer,intent(in)::actual,expected
    character(len=*),intent(in)::msg
    call assert_true(actual==expected,msg)
  end subroutine assert_int

  subroutine assert_bits(actual,expected,msg)
    real(real64),intent(in)::actual
    integer(int64),intent(in)::expected
    character(len=*),intent(in)::msg
    call assert_true(transfer(actual,0_int64)==expected,msg)
  end subroutine assert_bits

  subroutine write_bad_option()
    integer::u
    open(newunit=u,file='tests/boundq01/fixtures/bad_option.inp',status='replace')
    write(u,'(a)') '>optibc:'
    write(u,'(a)') '1 0'
    close(u)
  end subroutine write_bad_option

  subroutine write_duplicate_labels()
    integer::u
    open(newunit=u,file='tests/boundq01/fixtures/duplicate_labels.inp',status='replace')
    write(u,'(a)') '>optibc:'
    write(u,'(a)') '0 0'
    write(u,'(a)') '>topbou:'
    write(u,'(a)') '0.001'
    write(u,'(a)') '0.002'
    write(u,'(a)') '0.0'
    write(u,'(a)') '0.0'
    write(u,'(a)') '0.10 0.20'
    write(u,'(a)') '0.30 0.40'
    write(u,'(a)') '0.50 0.60'
    write(u,'(a)') '0.70 0.80'
    write(u,'(a)') '>topbou:'
    write(u,'(a)') '0.9'
    write(u,'(a)') '0.9'
    write(u,'(a)') '>latbou:'
    write(u,'(a)') '0.0 0.0'
    write(u,'(a)') '0.0 0.0'
    close(u)
  end subroutine write_duplicate_labels

  subroutine write_case_mismatch()
    integer::u
    open(newunit=u,file='tests/boundq01/fixtures/case_mismatch.inp',status='replace')
    write(u,'(a)') '>optibc:'
    write(u,'(a)') '0 0'
    write(u,'(a)') '>TOPBOU:'
    write(u,'(a)') '0.0'
    close(u)
  end subroutine write_case_mismatch

  subroutine write_bad_range()
    integer::u
    open(newunit=u,file='tests/boundq01/fixtures/bad_range.inp',status='replace')
    write(u,'(a)') '>optibc:'
    write(u,'(a)') '0 0'
    write(u,'(a)') '>topbou:'
    write(u,'(a)') '1.1'
    write(u,'(a)') '0.0'
    write(u,'(a)') '0.0'
    write(u,'(a)') '0.0'
    write(u,'(a)') '0.0 0.0'
    write(u,'(a)') '0.0 0.0'
    write(u,'(a)') '0.0 0.0'
    write(u,'(a)') '0.0 0.0'
    write(u,'(a)') '>latbou:'
    write(u,'(a)') '0.0 0.0'
    write(u,'(a)') '0.0 0.0'
    close(u)
  end subroutine write_bad_range

end program test_boundq01_static_boundary
