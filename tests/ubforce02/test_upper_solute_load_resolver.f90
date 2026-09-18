program test_ubforce02_upper_solute_load_resolver
  use iso_fortran_env, only: int64, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_value, ieee_quiet_nan
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate
  use mod_animo_tcd042_upper_solute_load_contract, only: &
    tcd042_upper_loads_t, select_tcd042_load_channel
  use mod_animo_tcd042_upper_solute_load_resolver, only: &
    tcd042_load_hydrology_context_t, tcd042_precip_chemistry_t, &
    tcd042_six_channel_chemistry_t, tcd042_upper_chemistry_forcing_t, &
    make_tcd042_upper_chemistry_forcing, resolve_tcd042_upper_loads
  implicit none

  call test_exact_source_equations_without_p()
  call test_exact_source_equations_with_p()
  call test_fail_closed_nonfinite()
  print *, 'PASS_UBFORCE02_TCD042_UPPER_SOLUTE_LOAD_RESOLVER'

contains

  subroutine assert_true(value,message)
    logical,intent(in)::value
    character(len=*),intent(in)::message
    if(.not.value)then
      print *,'ASSERTION FAILED: ',trim(message)
      error stop 1
    end if
  end subroutine assert_true

  subroutine make_day(day,value)
    integer(int64),intent(in)::day
    type(TimeCoordinate),intent(out)::value
    logical::ok
    call make_time_coordinate('ANIMO_TEST_CALENDAR',day,0_int64,1_int64,value,ok)
    call assert_true(ok,'make day')
  end subroutine make_day

  subroutine chemistry_fixture(p_enabled,forcing)
    logical,intent(in)::p_enabled
    type(tcd042_upper_chemistry_forcing_t),intent(out)::forcing
    type(tcd042_precip_chemistry_t)::pr
    type(tcd042_six_channel_chemistry_t)::irr,ron,rin
    logical::ok
    character(len=64)::reason

    pr%nh=1.0_real64; pr%ni=2.0_real64; pr%po=3.0_real64
    irr%nh=4.0_real64; irr%ni=5.0_real64; irr%doma=6.0_real64
    irr%don=7.0_real64; irr%po=8.0_real64; irr%dop=9.0_real64
    ron%nh=10.0_real64; ron%ni=11.0_real64; ron%doma=12.0_real64
    ron%don=13.0_real64; ron%po=14.0_real64; ron%dop=15.0_real64
    rin%nh=16.0_real64; rin%ni=17.0_real64; rin%doma=18.0_real64
    rin%don=19.0_real64; rin%po=20.0_real64; rin%dop=21.0_real64

    call make_tcd042_upper_chemistry_forcing('CHEM-1',p_enabled,pr,irr,ron,rin,forcing,ok,reason)
    call assert_true(ok,'chemistry fixture')
  end subroutine chemistry_fixture

  subroutine test_exact_source_equations_without_p()
    type(TimeCoordinate)::t0,t1
    type(tcd042_load_hydrology_context_t)::h
    type(tcd042_upper_chemistry_forcing_t)::chem
    type(tcd042_upper_loads_t)::loads
    logical::ok
    character(len=80)::reason
    real(real64)::v

    call make_day(0_int64,t0); call make_day(1_int64,t1)
    h%prr=0.10_real64; h%prsn=0.02_real64; h%prirr=0.03_real64
    h%runon=0.04_real64; h%rupr=0.01_real64; h%runinu=0.05_real64
    call chemistry_fixture(.false.,chem)

    call resolve_tcd042_upper_loads('RESOLVE-1',t0,t1,h,chem,loads,ok,reason)
    call assert_true(ok,'resolve non-P')

    call select_tcd042_load_channel(loads,1,v,ok,reason)
    call assert_true(ok,'select load1')
    call assert_true(abs(v-1.36_real64)<1.0e-14_real64,'load1 equation')

    call select_tcd042_load_channel(loads,2,v,ok,reason)
    call assert_true(ok,'select load2')
    call assert_true(abs(v-1.57_real64)<1.0e-14_real64,'load2 equation')

    call select_tcd042_load_channel(loads,3,v,ok,reason)
    call assert_true(ok,'select load3')
    call assert_true(abs(v-1.56_real64)<1.0e-14_real64,'load3 equation')

    call select_tcd042_load_channel(loads,4,v,ok,reason)
    call assert_true(ok,'select load4')
    call assert_true(abs(v-1.74_real64)<1.0e-14_real64,'load4 equation')

    call select_tcd042_load_channel(loads,5,v,ok,reason)
    call assert_true(.not.ok,'P channel unavailable when disabled')
  end subroutine test_exact_source_equations_without_p

  subroutine test_exact_source_equations_with_p()
    type(TimeCoordinate)::t0,t1
    type(tcd042_load_hydrology_context_t)::h
    type(tcd042_upper_chemistry_forcing_t)::chem
    type(tcd042_upper_loads_t)::loads
    logical::ok
    character(len=80)::reason
    real(real64)::v

    call make_day(10_int64,t0); call make_day(20_int64,t1)
    h%prr=0.10_real64; h%prsn=0.02_real64; h%prirr=0.03_real64
    h%runon=0.04_real64; h%rupr=0.01_real64; h%runinu=0.05_real64
    call chemistry_fixture(.true.,chem)

    call resolve_tcd042_upper_loads('RESOLVE-P',t0,t1,h,chem,loads,ok,reason)
    call assert_true(ok,'resolve P')

    call select_tcd042_load_channel(loads,5,v,ok,reason)
    call assert_true(ok,'select load5')
    call assert_true(abs(v-2.20_real64)<1.0e-14_real64,'load5 equation')

    call select_tcd042_load_channel(loads,6,v,ok,reason)
    call assert_true(ok,'select load6')
    call assert_true(abs(v-1.92_real64)<1.0e-14_real64,'load6 equation')
  end subroutine test_exact_source_equations_with_p

  subroutine test_fail_closed_nonfinite()
    type(TimeCoordinate)::t0,t1
    type(tcd042_load_hydrology_context_t)::h
    type(tcd042_upper_chemistry_forcing_t)::chem
    type(tcd042_upper_loads_t)::loads
    type(tcd042_precip_chemistry_t)::pr
    type(tcd042_six_channel_chemistry_t)::irr,ron,rin
    logical::ok
    character(len=80)::reason
    real(real64)::nan_value

    call make_day(0_int64,t0); call make_day(1_int64,t1)
    call chemistry_fixture(.false.,chem)
    nan_value=ieee_value(0.0_real64,ieee_quiet_nan)
    h%prr=nan_value
    call resolve_tcd042_upper_loads('BAD-HYDRO',t0,t1,h,chem,loads,ok,reason)
    call assert_true(.not.ok,'NaN hydrology rejected')

    pr=tcd042_precip_chemistry_t()
    irr=tcd042_six_channel_chemistry_t()
    ron=tcd042_six_channel_chemistry_t()
    rin=tcd042_six_channel_chemistry_t()
    pr%nh=nan_value
    call make_tcd042_upper_chemistry_forcing('BAD-CHEM',.false.,pr,irr,ron,rin,chem,ok,reason)
    call assert_true(.not.ok,'NaN chemistry rejected')
  end subroutine test_fail_closed_nonfinite

end program test_ubforce02_upper_solute_load_resolver
